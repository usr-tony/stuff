import pandas as pd

def jobs():
    jobs = pd.read_sql('''
        SELECT id, title, company, nation, state, sector, industry, time FROM jobs''', 
        con='sqlite:///seek/jobs.db')
    jobs.to_parquet('seek/jobs.parquet')