#!/bin/bash

NETWORK_NAME=estagios-network
NETWORK_NAME_NGINX=fabrica-nginx-proxy-network

# Navegar até a pasta onde está o docker-compose
# cd E-Stagio\ Prod/

# Parar os containers em execução
docker compose down

# Voltar para a pasta anterior para fazer o git pull
# cd ..

# Puxar as últimas mudanças do GitHub
git pull origin main

# Navegar novamente para a pasta do docker-compose
# cd E-Stagio\ Prod/


# Subir os containers novamente com as novas mudanças
docker compose up -d --build

# Verificar se a rede NETWORK_NAME_NGINX está conectada ao container estagios-prod-web
# docker network connect $NETWORK_NAME_NGINX estagios-prod-web
