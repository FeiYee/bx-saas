from minio import Minio
from minio.error import S3Error


# Create a client with the MinIO server playground, its access key
# and secret key.
client = Minio(
    endpoint="play.min.io",
    access_key="Q3AM3UQ867SPQQA43P2F",
    secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
)
