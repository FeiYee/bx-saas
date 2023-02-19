from pathlib import Path

BASE_DIR = Path(__file__).parent

PUBMED_FILE_SERVER = 'https://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/'
PUBMED_DOWNLOAD_DIR = BASE_DIR / 'download'

POOL_COUNT = 8
