from seek.scrape import scrape
from time import sleep
from datetime import datetime
import os


def main():
    while True:
        scrape()
        print(datetime.now().isoformat())
        transfer_file()
        sleep(60 * 60 * 12)


def transfer_file():
    # command that transfers the file via ftp to another computer on the network in attempt to backup jobs.db
    try:
        with open('./transfer') as f:
            cmd = f.read()
    except:
        return

    os.system(cmd)

if __name__ == '__main__':
    main()
        
