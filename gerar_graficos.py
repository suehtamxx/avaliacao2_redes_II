import pandas as pd
import matplotlib.pyplot as plt
import os

print("Gerando gráficos\n")

base_path = 'cliente'
arquivo_seq = os.path.join(base_path, 'tempo_Sequencial.csv')
arquivo_comp = os.path.join(base_path, 'tempo_Concorrente.csv')

#verifica se os arquivos CSV existem
if not os.path.exists(arquivo_seq) or not os.path.exists(arquivo_comp):
    print(f"Erro: Arquivo CSV não encontrado em '{base_path}'.")
    print("Execute o teste de carga primeiro.\n")
    exit()

#leitura dos dados
try:
    df_seq = pd.read_csv(arquivo_seq)
    df_comp = pd.read_csv(arquivo_comp)
except pd.errors.EmptyDataError:
    print("Erro: Um dos arquivos CSV está vazio.\n")
    exit()

num_requisicoes = range(1, len(df_seq)+1)
num_clientes = len(df_seq)

#geração do gráfico de linhas
plt.figure(figsize=(12, 6))
plt.plot(num_requisicoes, df_seq['tempo_resposta'], marker='o', linestyle='-', label='Servidor Sequencial',color='#ee591e')
plt.plot(num_requisicoes, df_comp['tempo_resposta'], marker='x', linestyle='--', label='Servidor Concorrente', color='#4682b4')
plt.title(f'Comparação de Tempo de Resposta para {num_clientes} Clientes Simultâneos')
plt.xlabel('Requisição do Cliente (Nº)')
plt.ylabel('Tempo de Resposta Individual (segundos)')
plt.legend()
plt.grid(True)
plt.xticks(num_requisicoes)

nome_grafico_linhas = 'grafico_linhas_comparativo.png'
plt.savefig(nome_grafico_linhas)
print(f"Gráfico de linhas salvo como '{nome_grafico_linhas}\n'")

#gera o gráfico de barras baseado nas médias
media_seq = df_seq.sum()['tempo_resposta']/num_clientes
media_comp = df_comp.sum()['tempo_resposta']/num_clientes

plt.figure(figsize=(8, 6))
servidores = ['Sequencial', 'Concorrente']
medias = [media_seq, media_comp]

barras = plt.bar(servidores, medias, color=['#4682b4',"#ee591e"])
plt.title(f'Tempo Médio de Resposta ({num_clientes} Clientes Simultâneos)')
plt.ylabel('Tempo Médio (segundos)')

for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2.0, yval, f'{yval:.4f} s', va='bottom', ha='center') 

nome_grafico_barras = 'grafico_barras_media.png'
plt.savefig(nome_grafico_barras)
print(f"Gráfico de barras salvo como '{nome_grafico_barras}\n'")

print("Gráficos gerados!!\n")