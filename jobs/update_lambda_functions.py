import boto3
import os
from seek.keywords import generate_exports
import pandas as pd


def deploy_all():
    deploy_jobs()
    deploy_keywords()
    

def deploy_jobs():
    # generates data
    jobs = pd.read_sql('''
        SELECT id, title, company, nation, state, sector, industry, time FROM jobs''', 
        con='sqlite:///seek/jobs.db')
    jobs.to_parquet('seek/jobs.parquet')

    # rebuild jobs
    os.system('cp seek/jobs.parquet lambda-functions/jobs/jobs.parquet')
    run_commands('jobs')
    os.remove('lambda-functions/jobs/jobs.parquet')

    
def deploy_keywords():
    generate_exports()
    dest = 'lambda-functions/keywords/'
    os.system('cp seek/jobs.parquet lambda-functions/keywords/jobs.parquet')
    filenames = ['jobs.parquet', 'words-sm.parquet', 'words2id.parquet', 'idf.parquet']
    [os.system(f'cp seek/{name} {dest}') for name in filenames]
    run_commands('keywords')
    [os.remove(dest + name) for name in filenames]


def run_commands(name):
    os.system(f'''
        export AWS_PROFILE=personal
        cd lambda-functions/{name}
        docker build . -t {name}
        aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com
        docker tag {name} 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com/{name}:latest
        docker push 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com/{name}:latest
        aws lambda update-function-code --function-name {name} --image-uri 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com/{name}:latest --no-cli-pager
    ''')
    ecr = boto3.Session(profile_name='personal').client('ecr')
    images = ecr.list_images(repositoryName=name)
    images_to_delete = [row for row in images['imageIds'] if not row.get('imageTag')]
    ecr.batch_delete_image(imageIds=images_to_delete, repositoryName=name)
    os.system('yes | docker system prune -a')


if __name__ == '__main__':
    deploy_jobs() 

