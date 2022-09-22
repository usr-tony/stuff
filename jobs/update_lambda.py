import boto3
import os

os.system('''
    AWS_PROFILE=personal
    cd lambda_function
    docker build . -t jobs
    aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com
    docker tag jobs 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com/jobs:latest
    docker push 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com/jobs:latest
    yes | docker system prune -a
    aws lambda update-function-code --function-name jobs --image-uri 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com/jobs:latest --no-cli-pager
''')

# this deletes all untagged images
ecr = boto3.Session(profile_name='personal').client('ecr')
images = ecr.list_images(repositoryName='jobs')
images_to_delete = [row for row in images['imageIds'] if not row.get('imageTag')]
response = ecr.batch_delete_image(imageIds=images_to_delete, repositoryName='jobs')
print('images deleted', response['imageIds'])
print('failures', response['failures'] or None)