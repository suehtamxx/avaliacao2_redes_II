# Segunda avaliação: Servidores Web Sequencial vs Competitivo

Este projeto foi implementado para comparar o desempenho desempenho de um servidor web sequencial e um servidor web competitivo (com o uso de threads) em um ambiente de rede simulado com docker.

## Requisitos
* Docker
* Docker Compose

## 1. Passo a passo como rodar os Servidores

1. Clone este repositório:
   ```bash
   git clone [link github]
   ```
2. Vá até a pasta do projeto e inicie os contêineres:
   ```bash
   cd avaliacao2_redes_II
   docker compose up -build
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

O teste de carga (Opção 3 do menu do cliente) irá gerar automaticamente os arquivos `tempo_Sequencial.csv` e `tempo_Competitivo.csv` na pasta `cliente/`.

Para gerar os gráficos `.png` a partir desses dados, execute o seguinte comando no terminal do **seu computador** (não dentro do contêiner), na pasta raiz do projeto:

```bash
python3 gerar_graficos.py
