import os
from minio import Minio as MinioLib

class Minio:

    def __init__(self, endpoint: str = "", key: str = "", secret: str = "", secure: bool = False) -> None:
        self.endpoint = os.environ.get("MINIO_ENDPOINT") if len(endpoint) == 0 else endpoint
        self.key = os.environ.get("MINIO_ACCESS_KEY") if len(key) == 0 else key
        self.secret = os.environ.get("MINIO_SECRET_KEY") if len(secret) == 0 else secret
        self.secure = True if os.environ.get("MINIO_IS_HTTPS", secure) == "true" else False
        self.client = MinioLib(
            self.endpoint,
            self.key,
            self.secret,
            secure=self.secure
        )
