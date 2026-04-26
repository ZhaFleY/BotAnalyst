from backend.modules.files.infrastructure.storage.minio_client import client

BUCKET_NAME = "files"


def init_bucket() -> None:
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)

