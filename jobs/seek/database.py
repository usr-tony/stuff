import mysql.connector
import sys
sys.path.append('../')
from config import db_password, local


def main():
    con, cur = create_connection()
    cur.execute('select count(*) from jobs')
    con.close()

def create_connection():
    con = mysql.connector.connect(
        host='database-1.cvatdti3ledc.ap-southeast-2.rds.amazonaws.com',
        user='admin',
        password=db_password
    )
    cur = con.cursor(dictionary=True)
    cur.execute('use jobs')
    return con, cur


def create_table(table_name='jobs', cur=None):
    if not cur:
        con, cur = create_connection()
        cur.execute('use jobs')

    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name}
        (
            id INT, 
            title TEXT, 
            company TEXT, 
            nation TEXT, 
            state TEXT, 
            city TEXT,
            area TEXT, 
            suburb TEXT, 
            sector_id INT, 
            sector TEXT, 
            industry_id INT, 
            industry TEXT, 
            work_type TEXT, 
            details TEXT, 
            time INT
        )
    ''')


if __name__ == '__main__':
    main()
