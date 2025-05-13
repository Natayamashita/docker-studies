import os
import psycopg2
import redis
import json
from bottle import Bottle, request


class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)

        # Conexão com Redis
        redis_host = os.getenv("REDIS_HOST", "queue")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_db = int(os.getenv("REDIS_DB", 0))
        self.fila = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

        # Conexão com PostgreSQL
        db_name = os.getenv("POSTGRES_DB", "email_sender")
        db_user = os.getenv("POSTGRES_USER", "postgres")
        db_password = os.getenv("POSTGRES_PASSWORD", "senha_segura")
        db_host = os.getenv("POSTGRES_HOST", "db")
        DSN = f"dbname={db_name} user={db_user} password={db_password} host={db_host}"
        self.conn = psycopg2.connect(DSN)

    def register_message(self, assunto, mensagem):
        SQL = 'INSERT INTO emails (assunto, mensagem) VALUES (%s, %s)'
        cur = self.conn.cursor()
        cur.execute(SQL, (assunto, mensagem))
        self.conn.commit()
        cur.close()

        msg = {'assunto': assunto, 'mensagem': mensagem}
        self.fila.rpush('sender', json.dumps(msg))

    def send(self):
        subject = request.forms.get('subject')
        message = request.forms.get('message')
        self.register_message(subject, message)
        return f'Mensagem enfileirada ! Assunto: {subject} Mensagem: {message}'


if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)
