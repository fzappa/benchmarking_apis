#!/bin/bash

# Instalar o wrk no Ubuntu
# sudo apt install wrk

COMPOSE_FILE="docker-compose.yml"

# Nome do projeto (baseado no diretório atual ou definido explicitamente)
# PROJECT_NAME=$(basename $(pwd) | tr '[:upper:]' '[:lower:]') # Ex: "benchmark_all"
PROJECT_NAME="benchmark_all"

# Verificar se um comando falhou
check_error() {
    if [ $? -ne 0 ]; then
        echo "Erro: $1 falhou. Abortando o script."
        exit 1
    fi
}

# Iniciar os containers em modo detached com build
echo "Iniciando os containers..."
docker compose -f "$COMPOSE_FILE" up --build -d
check_error "docker compose up"

# Executar o benchmark
echo "Executando o benchmark..."
python benchmark_wrk.py --mode fast --reps 1 --timestamp
check_error "benchmark_wrk.py"

# Parar e remover os containers
echo "Parando e removendo os containers..."
docker compose -f "$COMPOSE_FILE" down
check_error "docker compose down"

# Remover as imagens geradas pelos serviços
SERVICES="fastapi drf ninja axum rocket actix"
for SERVICE in $SERVICES; do
    IMAGE_NAME="${PROJECT_NAME}-${SERVICE}:latest"
    echo "Tentando remover imagem: $IMAGE_NAME"
    docker image rm -f "$IMAGE_NAME" 2>/dev/null || echo "Imagem $IMAGE_NAME não encontrada ou já removida."
done

# Limpar imagens não utilizadas
echo "Limpando imagens dangling (não associadas)..."
docker image prune -f

echo "Teste concluído e limpeza realizada com sucesso!"