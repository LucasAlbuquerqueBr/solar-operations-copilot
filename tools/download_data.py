"""Fetch the exact historical sources recorded in the repository manifest."""
from pathlib import Path
import hashlib
import json
import shutil
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def verify_file(path, item):
    """Return whether a file matches both recorded size and SHA-256."""
    if not path.is_file() or path.stat().st_size != item['bytes']:
        return False
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest() == item['sha256']


def download_file(path, item):
    if verify_file(path, item):
        print(f'Already verified: {path.name}')
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.part')
    try:
        with urlopen(item['url'], timeout=120) as response:
            with temporary.open('wb') as output:
                shutil.copyfileobj(response, output)
        if not verify_file(temporary, item):
            raise ValueError(f'Source integrity mismatch: {path.name}')
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    print(f'Downloaded and verified: {path.name}')


def main():
    manifest = json.loads((ROOT / 'data/download_manifest.json').read_text(encoding='utf-8'))
    for item in manifest:
        destination = (ROOT / item['file']).resolve()
        if not destination.is_relative_to(ROOT / 'data'):
            raise ValueError('Manifest destination must be inside data/')
        download_file(destination, item)


if __name__ == '__main__':
    main()
