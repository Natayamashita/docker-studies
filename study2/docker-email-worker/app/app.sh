#!/bin/sh

echo "Aguardando banco subir..."
sleep 10  

echo "Criando banco e tabela se necessário..."
psql -U postgres -h db -c "CREATE DATABASE email_sender" || echo "Banco já existe"
psql -U postgres -h db -d email_sender -c "
CREATE TABLE IF NOT EXISTS emails (
  id SERIAL PRIMARY KEY,
  data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  assunto VARCHAR(100) NOT NULL,
  mensagem VARCHAR(250) NOT NULL
);"

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Iniciando aplicação Python..."
python -u sender.py
