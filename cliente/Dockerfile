FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && DEBIAN_FRONTEND=nointeractive apt-get install -y --no-install-recommends python3 python3-pip && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["bash"]