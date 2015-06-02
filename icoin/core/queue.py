from psycopg2 import connect
from psycopg2.pool import ThreadedConnectionPool
from pq import PQ
from icoin import app

pq = None

def init():
    global pq

    dsn = get_dsn(app.config["DB_USER"], app.config["DB_PASSWORD"], 
        app.config["DB_HOST"], app.config["DB_PORT"], app.config["DB_NAME"])
    pool = ThreadedConnectionPool(0, 2, dsn) 
    
    pq = PQ(pool=pool)

    create_schema(dsn)
    

def create_schema(dsn):
    "Create queue schema if it does not exist"
    with connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT to_regclass('queue');")
            row = cur.fetchone()
            if not row[0]:
                app.logger.info("Creating queue schema")
                pq.create()

def get_dsn(user, password, host, port, name):
    dsn = ""

    if user:
        dsn += " user=" + user
        
    if password:
        dsn += " password=" + password
        
    if host:
        dsn += " host=" + host
        
    if port:
        dsn += " port=" + port
        
    if name:
        dsn += " dbname=" + name
    
    return dsn

