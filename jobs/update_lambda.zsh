cd lambda_function
docker build . -t jobs
aws ecr get-login-password --region ap-southeast-2 --profile personal | docker login --username AWS --password-stdin 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com
docker tag jobs 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com/jobs:latest
docker push 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com/jobs:latest
yes | docker system prune -a
aws lambda update-function-code --function-name jobs --profile personal --image-uri 720957039806.dkr.ecr.ap-southeast-2.amazonaws.com/jobs:latest