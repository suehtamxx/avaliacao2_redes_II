import socket
import hashlib
import time
import threading

SERVER_HOST_SEQ = 'servidor_sequencial'
SERVER_HOST_CONC = 'servidor_concorrente'
SERVER_PORT = 80
NUM_CLIENTES_SIMULTANEOS = 10 

def calcular_hash(matricula, nome):
    dados = f"{matricula} {nome}"
    sha1 = hashlib.sha1()
    sha1.update(dados.encode('utf-8'))
    return sha1.hexdigest()

def enviar_requisicao_unica(host, port, method='GET', path='/', body=''):
    """Função que envia UMA única requisição (GET ou POST)."""
    minha_matricula = "20239019852"
    meu_nome = "Elder Matheus"
    custom_id = calcular_hash(minha_matricula, meu_nome)
    
    # Monta a requisição
    request_lines = [
        f"{method} {path} HTTP/1.1",
        f"Host: {host}",
        f"X-Custom-ID: {custom_id}",
        "Connection: close",
    ]
    
    if method == 'POST':
        request_lines.append("Content-Length: " + str(len(body)))
        request_lines.append("Content-Type: text/plain")
        request_lines.append('')
        request_lines.append(body)
    else:
        request_lines.append('')
        request_lines.append('')

    http_request = "\r\n".join(request_lines)

    print(f"\nEnviando Requisição {method} para {host}:{port}{path}\n")
    
    start_time = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(http_request.encode('utf-8'))
            
            resposta_completa = b""
            while True:
                dados = s.recv(4096)
                if not dados:
                    break
                resposta_completa += dados
        
        end_time = time.time()
        
        print("\nResposta Recebida")
        print(resposta_completa.decode('utf-8', errors='ignore'))
        print('\n')
        print(f"Tempo total: {end_time - start_time:.4f} segundos")

    except Exception as e:
        print(f"Erro na requisição: {e}")

def worker_carga(host, port, path, results_list):
    """Função 'ponte' para o teste de carga em threads."""
    
    minha_matricula = "20239019852"
    meu_nome = "Elder Matheus"
    custom_id = calcular_hash(minha_matricula, meu_nome)
    
    http_request = "\r\n".join([
        f"GET {path} HTTP/1.1",
        f"Host: {host}",
        f"X-Custom-ID: {custom_id}",
        "Connection: close",
        "", ""
    ])

    start_time = time.time()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(http_request.encode('utf-8'))
            while s.recv(4096):
                pass
        end_time = time.time()
        results_list.append(end_time - start_time)
    except Exception as e:
        print(f"Erro na thread: {e}")

def teste_simultaneo(nome_servidor, host):
    """Dispara N clientes simultaneamente usando o módulo threading."""
    print(f"\nIniciando Teste de Carga SIMULTÂNEO para o Servidor: {nome_servidor}")
    print(f"Disparando {NUM_CLIENTES_SIMULTANEOS} clientes para a rota /teste-carga.")

    threads = []
    tempos_individuais = [] 

    start_total_time = time.time()
    
    for _ in range(NUM_CLIENTES_SIMULTANEOS):
        thread = threading.Thread(target=worker_carga, args=(host, SERVER_PORT, '/teste-carga', tempos_individuais))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_total_time = time.time()
    
    nome_arquivo = f'tempo_{nome_servidor}.csv'
    with open(nome_arquivo, 'w') as f:
        f.write("tempo_resposta\n")
        for tempo in tempos_individuais:
            f.write(f"{tempo}\n")
    print(f"Resultados individuais salvos em '{nome_arquivo}'")
    
    total_time = end_total_time - start_total_time
    print(f"Servidor: {nome_servidor}")
    print(f"Tempo total para {NUM_CLIENTES_SIMULTANEOS} clientes: {total_time:.4f} segundos")

    return total_time

def rodar_teste_de_carga_completo():
    """Executa o teste nos dois servidores e chama o script de gráficos."""
    tempo_sequencial = teste_simultaneo("Sequencial", SERVER_HOST_SEQ)
    print("\n5 segundos até o próximo teste.\n")
    time.sleep(5)
    tempo_concorrente = teste_simultaneo("Concorrente", SERVER_HOST_CONC)

    print("\n\n Resultados do Teste de Carga")
    print(f"O servidor Sequencial levou {tempo_sequencial:.4f} segundos.")
    print(f"O servidor Concorrente levou {tempo_concorrente:.4f} segundos.")
    
    print("\nTeste concluído. Os arquivos CSV foram gerados.")
    print("Rode 'python3 gerar_graficos.py' no terminal do seu computador (host) para ver os gráficos.")

def main_menu():
    while True:
        print("\nMenu Interativo do Cliente")
        print("Qual servidor você quer testar?")
        print("  1. Servidor Sequencial")
        print("  2. Servidor Concorrente")
        print("\n  Outras Opções:")
        print("  3. Rodar Teste de Carga completo (ambos servidores)")
        print("  4. Sair")
        
        escolha_servidor = input("Escolha uma opção (1-4): ")

        if escolha_servidor == '1':
            host_escolhido = SERVER_HOST_SEQ
        elif escolha_servidor == '2':
            host_escolhido = SERVER_HOST_CONC
        elif escolha_servidor == '3':
            rodar_teste_de_carga_completo()
            continue
        elif escolha_servidor == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
            continue
        
        print(f"\nTestando '{host_escolhido}'")
        print("Qual requisição você quer enviar?")
        print("  1. GET / (Página Inicial)")
        print("  2. POST /dados (Enviar dados)")
        print("  3. Voltar ao menu anterior")
        
        escolha_rota = input("Escolha uma opção (1-3): ")
        
        if escolha_rota == '1':
            enviar_requisicao_unica(host_escolhido, SERVER_PORT, method='GET', path='/')
        elif escolha_rota == '2':
            dados_post = input("Digite os dados para enviar no POST (ex: nome=elder): ")
            enviar_requisicao_unica(host_escolhido, SERVER_PORT, method='POST', path='/dados', body=dados_post)
        elif escolha_rota == '3':
            continue
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main_menu()