import math
import os
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from .config import PUBMED_DOWNLOAD_DIR, PUBMED_FILE_SERVER, POOL_COUNT


def fetch_file(filename: str):
    pid = os.getpid()
    print('Run task %s (%s)...' % (filename, pid))
    file = PUBMED_DOWNLOAD_DIR / filename
    url = PUBMED_FILE_SERVER + '/' + filename
    res = requests.get(url, stream=True)
    total = int(res.headers['Content-Length'])
    size = math.ceil(total / 1024)
    pbar = tqdm(total=size, desc=filename)
    with open(file, 'wb') as fd:
        for chunk in res.iter_content(chunk_size=1024):
            fd.write(chunk)
            pbar.update(1)

    pbar.close()


def fetch_multi(files: list):
    pool = Pool(POOL_COUNT)
    for file in files:
        file_name = str(file['file_name'])
        file_md5_name = str(file['file_md5_name'])
        file_stats_name = str(file['file_stats_name'])
        pool.apply_async(fetch_file, args=(file_name,))
        pool.apply_async(fetch_file, args=(file_md5_name,))
        pool.apply_async(fetch_file, args=(file_stats_name,))
    print('Waiting for all subprocesses done...')
    pool.close()
    pool.join()
    print('All subprocesses done.')


def fetch():
    res = requests.get(PUBMED_FILE_SERVER)
    # print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup.find_all('a'))
    # print(soup.pre.children)
    contents = soup.pre.contents
    contents = contents[6:]
    array = list()
    items = list()
    item = dict(
        file_name='',
        file_date='',
        file_size='',
        file_md5_name='',
        file_md5_date='',
        file_md5_size='',
        file_stats_name='',
        file_stats_date='',
        file_stats_size='',
    )

    for child in contents:
        # item = str(child)
        # items.append(child)
        text = child.string
        if len(items) == 0 or len(items) % 3 == 0:
            items.append(text)
        else:
            s = text.strip()
            a = s.split('  ')
            items.append(a[0])
            items.append(a[1])

        if len(items) == 9:
            item = dict()
            item['file_name'] = items[0]
            item['file_date'] = items[1]
            item['file_size'] = items[2]
            item['file_md5_name'] = items[3]
            item['file_md5_date'] = items[4]
            item['file_md5_size'] = items[5]
            item['file_stats_name'] = items[6]
            item['file_stats_date'] = items[7]
            item['file_stats_size'] = items[8]

            array.append(item)
            items = list()

    print(len(array))
    fetch_multi(array)


if __name__ == '__main__':
    fetch()
