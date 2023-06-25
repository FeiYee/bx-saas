
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).parent

SERVER_NAME = 'bx-saas-server'

SECRET_KEY: str = secrets.token_urlsafe(32)
# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

PASSWORD_DEFAULT = '123456'

GRAPH_SERVER = 'http://43.154.134.150:7096'

DATABASE_TYPE = 'mysql'
# DATABASE_TYPE = 'sqlite'

DATABASE_HOST = '43.154.134.150'
DATABASE_PORT = '3306'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'Emzujju12!'
DATABASE_DB = 'bx_saas'

# wechat
DATABASE_HOST = '152.136.129.64'

# miniprogram
DATABASE_HOST = 'database-1.cg2wude0gpbv.rds.cn-north-1.amazonaws.com.cn'

# MINIO_HOST = 'minio'
# MINIO_PORT = '7687'
# MINIO_USER = 'minio'
# MINIO_PASSWORD = 'Emzujju12!'


# NEO4J_HOST = 'neo4j'
# NEO4J_HOST = '116.198.202.249'
# NEO4J_PORT = '7687'
# NEO4J_USER = 'neo4j'
# NEO4J_PASSWORD = 'Emzujju12!'
