from seek import scrape
from time import sleep
from datetime import datetime
from seek.keywords import generate_exports


def main():
    while True:
        scrape.scrape()
        print(datetime.now().isoformat())
        sleep(600)


if __name__ == '__main__':
    main()
        
