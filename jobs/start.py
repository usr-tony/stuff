from seek import scrape
from time import sleep
from datetime import datetime
import pandas as pd
from update_lambda import rebuild_and_deploy
from seek.keywords import generate_exports
import os


def main():
    while True:
        scrape.scrape()
        print(datetime.now().isoformat())
        sleep(60 * 60 * 12)


if __name__ == '__main__':
    main()
        
