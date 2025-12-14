import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor, DictCursor



class PostgreSQLHandler:
    def __init__(self, URI):
        self.URI = URI
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(self.URI)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            
    def execute(self, query, params=None, dict_mode=True):
        with self.conn.cursor(cursor_factory=RealDictCursor if dict_mode else DictCursor) as cur:
            cur.execute(query, params)
            return dict(cur.fetchone())
        
    def insert_rows(self, query, params=None):
        with self.conn.cursor() as cur:
            cur.executemany(query, params)
            self.conn.commit()

