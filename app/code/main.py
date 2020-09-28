import os
import shutil
from pathlib import Path
import io
import tempfile
import zipfile
import configargparse as argparse

from download import download

def clean_dir(path):
    os.makedirs(path, exist_ok=True)
    for file in os.listdir(path):
        subpath = Path(path, file)
        if subpath.is_dir():
            shutil.rmtree(subpath)
        else:
            subpath.unlink()

if __name__ == '__main__':
    parser = argparse.ArgParser()
    parser.add('--selenium-url', env_var='SELENIUM_URL', type=str, required=True)
    parser.add('--leaf-share-url', env_var='LEAF_SHARE_URL', type=str, required=True)
    parser.add_argument('--output', env_var='OUTPUT_DIR', type=str, default='./')
    options = parser.parse_args()

    zip_bio = io.BytesIO(download(
        selenium_url=options.selenium_url,
        leaf_share_url=options.leaf_share_url,
    ))

    output_dir = options.output
    clean_dir(output_dir)
    with tempfile.TemporaryDirectory() as tempdir:
        with zipfile.ZipFile(zip_bio) as zip:
            zip.extractall(output_dir)
