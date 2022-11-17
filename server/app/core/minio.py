from minio import Minio
from minio.error import S3Error, InvalidResponseError
import urllib3
import time, os
from datetime import datetime, timedelta


# Create a client with the MinIO server playground, its access key
# and secret key.
client = Minio(
    endpoint="play.min.io",
    access_key="Q3AM3UQ867SPQQA43P2F",
    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
)


class MinioStore:

    def __int__(self, endpoint, access_key, secret_key):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def make_bucket(self, bucket_name):
        exists = self.client.bucket_exists(bucket_name=bucket_name)
        if not exists:
            self.client.make_bucket(bucket_name=bucket_name)
            exists = self.client.bucket_exists(bucket_name=bucket_name)

        return exists

    def put_object(self, bucket_name, object_name, data):
        exists = self.make_bucket(bucket_name)
        if not exists:
            return False
        self.client.put_object(bucket_name=bucket_name, object_name=object_name, data=data)

    def get_object(self,  bucket_name, object_name, file_path):
        self.client.get_object(bucket_name=bucket_name, object_name=object_name)
        pass

    def put_file(self, bucket_name, object_name, file_path):
        exists = self.make_bucket(bucket_name)
        if not exists:
            return False

        result = self.client.fput_object(bucket_name=bucket_name, object_name=object_name, file_path=file_path)
        return result

    def get_file(self,  bucket_name, object_name, file_path):
        self.client.fget_object(bucket_name=bucket_name, object_name=object_name, file_path=file_path)

    # 生成一个用于HTTP GET操作的presigned URL
    def get_presigned_url(self, bucket_name, object_name, expiry=timedelta(days=7)):
        '''
        生成一个用于HTTP GET操作的presigned URL。浏览器/移动客户端可以在即使存储桶为私有的情况下也可以通过这个URL进行下载。
        这个presigned URL可以有一个过期时间，默认是7天。

        bucket_name	string	存储桶名称。
        object_name	string	对象名称。
        expiry	datetime.datetime	过期时间，单位是秒，默认是7天。
        '''
        return self.client.presigned_get_object(bucket_name, object_name, expiry)


minio_store = MinioStore()
