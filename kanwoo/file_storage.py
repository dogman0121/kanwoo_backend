import os
from abc import abstractmethod, ABC
import boto3
from botocore.exceptions import ClientError


from kanwoo.entities import File

class FileExistException(Exception):
    pass

class FileStorageMixin(ABC):
    
    @abstractmethod
    def __init__(self, app):
        pass
    
    @abstractmethod
    def init_app(self, app):
        pass

    @abstractmethod
    def save(self, file, key):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def exists(self, key):
        pass

    @abstractmethod
    def get_url(self, key):
        pass

    @abstractmethod
    def get_upload_url(self, key):
        pass

class LocalStorage(FileStorageMixin):
    def __init__(self, app=None):
        self.app = app
        self.upload_dir = None
        self.cdn_url = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.upload_dir = app.config['UPLOAD_DIR']
        self.cdn_url = app.config['CDN_URL']

    def save(self, file: File, key: str):
        folders_path, _ = key.rsplit("/", maxsplit=1)

        folder_path = os.path.join(self.upload_dir, folders_path)
        file_path = os.path.join(self.upload_dir, key)

        if os.path.exists(file_path):
            raise FileExistException(f"File with path '{key}' already exists.")
        
        if not os.path.exists(folder_path):
            os.makedirs(os.path.join(self.upload_dir, folders_path))

        with open(file_path, "wb") as f:
            f.write(file.bytes)

    def delete(self, key: str):
        file_path = os.path.join(self.upload_dir, key)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path)

    def exists(self, key: str):
        return os.path.exists(os.path.join(self.upload_dir, key))

    def get_url(self, key: str):
        return os.path.join(self.cdn_url, key)

    def get_upload_url(self, key: str):
        return os.path.join(self.cdn_url, key)


class S3Storage(FileStorageMixin):
    def __init__(self, app=None):
        self.app = app
        self.bucket_name = None
        self.endpoint_url = None
        self.acccess_key_id = None
        self.access_secret_key = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.bucket_name = app.config['S3_BUCKET_NAME']
        self.endpoint_url = app.config['S3_ENDPOINT_URL']
        self.acccess_key_id = app.config['S3_ACCESS_KEY_ID']
        self.access_secret_key = app.config['S3_ACCESS_SECRET_KEY']

        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name='s3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.acccess_key_id,
            aws_secret_access_key=self.access_secret_key
        )

    def save(self, file: File, key: str):
        self.client.put_object(
            Bucket=self.bucket_name, 
            Key=key, 
            Body=file.bytes
        )

    def delete(self, key):
        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=key
        )

    def exists(self, key):
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            raise

    def get_object_url(self, key):
        return os.path.join(self.endpoint_url, key)

    def get_upload_url(self, key, min_file_size=0, max_file_size=100 * 1024^2, expires_in=3600):
        self.client.get_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": key
            },
            Conditions=[
                ["content-length-range", min_file_size, max_file_size]
            ],
            ExpiresIn=expires_in
        )