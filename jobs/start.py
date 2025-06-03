from seek.scrape import scrape
from time import sleep
from datetime import datetime, timedelta
import gzip
import shutil
import boto3
import os
from pathlib import Path


SLEEP_SECONDS = timedelta(hours=12).seconds
AWS_BUCKET_NAME = 'jobs--001'
SEEK_DB_PATH = './seek/jobs.db'
UPLOAD_PERIOD: timedelta = timedelta(days=1)


def main():
    last_uploaded = datetime.now()
    while True:
        scrape()
        if datetime.now() - last_uploaded > UPLOAD_PERIOD:
            create_kaggle_dset('jobs', ['seek/jobs.db'], version=True) 
        ptime('sleeping')
        sleep(SLEEP_SECONDS)


def create_kaggle_dset(name: str, files: list[str], description="v5.0", version=False):
    """
    Parameters
    ----
        name : str
            only a to z and - chars
        files: list[str|Path] - cannot handle files in subdirectories
    """
    from pathlib import Path
    import json
    import os
    import re

    KAGGLE_USERNAME = os.getenv('KAGGLE_USERNAME')
    KAGGLE_KEY = os.getenv('KAGGLE_KEY')

    assert re.match(r"^[\w\-]*$", name), 'invalid name, must be alphanumeric or "-"'
    path = Path(name)
    path.mkdir(exist_ok=True)
    meta = {
        "title": name,
        "id": f"{KAGGLE_USERNAME}/{name}",
        "licenses": [{"name": "CC0-1.0"}],
        "description": description,
    }
    with open(path / "dataset-metadata.json", "w") as f:
        f.write(json.dumps(meta))

    for file in files:
        cmd = f"gzip -c {file} > {path}/{file}.gz"
        os.system(cmd)

    cmd = f"kaggle d create {path}"
    if version:
        cmd = f"kaggle d version -p {path} -m update"

    os.system(f"""
        export {KAGGLE_KEY=}
        export {KAGGLE_USERNAME=}
        {cmd}
        rm -rf {path}
    """)



def compress_file(file_name=SEEK_DB_PATH):
    compressed_file_path = f'{file_name}.gz'
    ptime(f'creating compressed file ->', compressed_file_path)
    with gzip.open(compressed_file_path, 'wb') as fout:
        with open(file_name, 'rb') as fin:
            shutil.copyfileobj(fin, fout)

    return compressed_file_path


def ptime(*msgs: str) -> None:
    print(datetime.now().isoformat(), *msgs)


if __name__ == '__main__':
    main()
        
