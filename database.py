import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

def get_connection():
    port_val = os.getenv("POSTGRESQL_PORT")
    port = int(port_val) if port_val and port_val.isdigit() else 5432

    return psycopg2.connect(
        host=os.getenv("POSTGRESQL_HOST", "localhost"),
        port=port,
        user=os.getenv("POSTGRESQL_USER", "postgres"),
        password=os.getenv("POSTGRESQL_PASSWORD"),
        dbname=os.getenv("POSTGRESQL_DATABASE", "CampusGOBD"),
        sslmode=os.getenv("POSTGRESQL_SSLMODE", "require"),
        cursor_factory=RealDictCursor
    )