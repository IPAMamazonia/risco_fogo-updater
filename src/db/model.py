import psycopg2
from configs import DB_NAME, PW, HOST, USER, TABLE_NAME


class DB_Model:

    def __init__(self):
        self.con = psycopg2.connect(
            host=HOST, database=DB_NAME,user=USER, password=PW)
        self.cur = self.con.cursor()

    def calculate(self):
        print 'Calculando...'
        self.cur.execute('''
            INSERT INTO risco_de_fogo (id_ti, risco, date)
                    SELECT 
                        p.id as id,
                        round(avg(r.risco_fogo)::decimal, 1) as risco,
                        current_date
                    FROM 
                        {} as r,
                        (SELECT id, geom FROM terras_indigenas WHERE id = 3751) as p
                    WHERE
                        ST_intersects(r.geom, p.geom)
                    AND r.risco_fogo > 0
                    GROUP BY p.id
        '''.format(TABLE_NAME))
        
        self.con.commit()
        print "Calculo concluido"

    def check_if_table_exists(self):

        self.cur.execute('''
        SELECT EXISTS (
   SELECT 1
   FROM   information_schema.tables 
   WHERE  table_schema = 'public'
   AND    table_name = '{}'
   );
'''.format(TABLE_NAME))

        exists = self.cur.fetchone()[0]

        return exists


    def drop_table(self):
        self.cur.execute('''
        DROP TABLE {};
        '''.format(TABLE_NAME))
        self.con.commit()
        print "Table dropada"
    def close_conn(self):
        self.con.close()

    def database_calculate_and_drop_table(self):

        self.calculate()
        self.drop_table()
        self.close_conn()
