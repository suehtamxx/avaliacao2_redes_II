import socket
import time
import threading

HOST = '0.0.0.0'
PORT = 80

def handle_request(conn, addr):
    """Função para processar uma requisição individual."""
    with conn: # 'with conn' garante que a conexão será fechada
        print(f"Conexão de {addr} sendo tratada pela Thread: {threading.current_thread().name}")
        
        data = conn.recv(2048)
        if not data:
            return

        request_str = data.decode('utf-8')
        # Não vamos printar a requisição aqui para não poluir o log concorrente

        header_lines = request_str.split('\r\n')
        request_line = header_lines[0]
        
        custom_id_header = ""
        for line in header_lines:
            if "X-Custom-ID:" in line:
                custom_id_header = line
                break
        
        try:
            method, path, version = request_line.split(' ')
        except ValueError:
            send_response(conn, '400 Bad Request', '<h1>400 Bad Request</h1>')
            return

        if not custom_id_header:
            send_response(conn, '400 Bad Request', '<h1>400 Bad Request: X-Custom-ID ausente</h1>')
            return

        if path == '/':
            if method == 'GET':
                body = "<h1>Pagina Inicial</h1><p>Servidor Competitivo funcionando.</p>"
                send_response(conn, '200 OK', body, custom_id_header)
            else:
                send_response(conn, '405 Method Not Allowed', '<h1>405 Method Not Allowed</h1>', custom_id_header)

        elif path == '/teste-carga':
            if method == 'GET':
                print(f"Thread {threading.current_thread().name} iniciando tarefa pesada...")
                time.sleep(5)
                print(f"Thread {threading.current_thread().name} concluiu.")
                body = "<h1>Teste de Carga</h1><p>Esta pagina demorou 5 segundos para carregar (Servidor Competitivo).</p>"
                send_response(conn, '200 OK', body, custom_id_header)
            else:
                send_response(conn, '405 Method Not Allowed', '<h1>405 Method Not Allowed</h1>', custom_id_header)
        
        elif path == '/dados': # Rota de POST (ADICIONADA)
            if method == 'POST':
                body_start = request_str.find('\r\n\r\n') + 4
                post_data = request_str[body_start:]
                response_body = f"<h1>Dados Recebidos</h1><p>Dados recebidos com sucesso:</p><pre>{post_data}</pre>"
                send_response(conn, '200 OK', response_body, custom_id_header)
            else:
                send_response(conn, '405 Method Not Allowed', '<h1>405 Method Not Allowed</h1>', custom_id_header)

        else:
            send_response(conn, '404 Not Found', '<h1>404 Not Found</h1>', custom_id_header)
        
        # print(f"Conexão com {addr} fechada pela thread.") # Opcional


def send_response(conn, status, body, custom_id_header=""):
    """Função para montar e enviar uma resposta HTTP completa."""
    headers = [
        f"HTTP/1.1 {status}",
        "Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(body.encode('utf-8'))}",
        "Connection: close"
    ]
    if custom_id_header:
        headers.append(custom_id_header)

    http_response = "\r\n".join(headers) + "\r\n\r\n" + body
    conn.sendall(http_response.encode('utf-8'))

# --- Lógica Principal do Servidor Competitivo ---
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor Competitivo escutando em {HOST}:{PORT}\n")
    
    while True:
        conn, addr = s.accept()
        # Inicia uma nova thread para cada conexão e volta a escutar
        client_thread = threading.Thread(target=handle_request, args=(conn, addr))
        client_thread.start()