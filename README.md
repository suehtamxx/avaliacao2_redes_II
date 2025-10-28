# Segunda avaliação: Servidores Web Sequencial vs. Concorrente

Este projeto foi implementado para comparar o desempenho desempenho de um servidor web sequencial e um servidor web concorrente (com o uso de threads) em um ambiente de rede simulado com docker.

## Requisitos
* Docker
* Docker Compose
* Python 3
* Bibliotecas Python: `pandas`e `matplotlib`(para gerar os gráficos)

## 1. Passo a passo como rodar os Servidores

1. Clone este repositório:
   ```bash
   git clone https://github.com/suehtamxx/avaliacao2_redes_II.git
   ```
2. Vá até a pasta do projeto e inicie os contêineres:
   ```bash
   cd avaliacao2_redes_II
   docker compose up --build
   ```
   Comando para construir as imagens dos servidores e do cliente, configurar a rede e iniciar os servidores(mantenha o terminal aberto).

## 2. Testes Interativos

1.  Abra um **novo terminal**.
2.  Acesse o contêiner do cliente:
    ```bash
    docker-compose exec cliente bash
    ```
3.  Execute o script do cliente para ver o menu interativo:
    ```bash
    python3 client.py
    ```
4.  A partir do menu, você pode:
    * Testar as rotas `GET /` e `POST /dados` individualmente em cada servidor.
    * Executar o teste de carga completo (Opção 3).

## 3. Como Gerar os Gráficos

O teste de carga (Opção 3 do menu do cliente) irá gerar automaticamente os arquivos `tempo_Sequencial.csv` e `tempo_Concorrente.csv` na pasta `cliente/`.

Para gerar os gráficos `.png` a partir desses dados,  precisa rodar o `gerar_graficos.py` no terminal do **seu computador** (não dentro do contêiner), na pasta raiz do projeto

1. (Opcional) Criar um ambiente virtual:
	```bash
	python3 -m venv venv
	source venv/bin/activate
	```
2. Instale as dependências a partir do arquivo `requirements.txt`:
	```bash
	pip install -r requirements.txt
	```
3. Agora execute este script para gerar os gŕaficos:
	```bash
	python3 gerar_graficos.py
	```
Isso irá criar os arquivos `grafico_linhas_comparativo.png` e `grafico_barras_media.png` na pasta raiz.
