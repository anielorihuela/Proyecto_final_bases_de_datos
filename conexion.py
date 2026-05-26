import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
NAME = os.getenv("DB_name")
USER = os.getenv("DB_user")
PASSWORD = os.getenv("DB_PASSWORD")


if not all([HOST, PORT, NAME, USER, PASSWORD]):
    raise ValueError("Faltan variables de entorno en .env")

DB_CONNECTION_STRING = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"