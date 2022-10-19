from seek import scrape
from time import sleep
from datetime import datetime
from update_lambda_functions import deploy_all


def main():
    while True:
        scrape.scrape()
        print(datetime.now().isoformat())
        sleep(60 * 60 * 12)


if __name__ == '__main__':
    main()
        
