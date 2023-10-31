#! /Users/tony/miniconda3/envs/jobs/bin/python
from seek.scrape import scrape
from time import sleep
from datetime import datetime


def main():
    while True:
        scrape()
        print(datetime.now().isoformat())
        sleep(60 * 60 * 12)


if __name__ == '__main__':
    main()
        
