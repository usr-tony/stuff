#! /Users/tony/miniconda3/envs/jobs/bin/python
from seek.scrape import scrape
from time import sleep
from datetime import datetime, timedelta


SLEEP_SECONDS = timedelta(hours=6).seconds


def main():
    while True:
        scrape()
        print(datetime.now().isoformat())
        sleep(SLEEP_SECONDS)


if __name__ == '__main__':
    main()
        
