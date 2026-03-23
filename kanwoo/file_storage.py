import os
from abc import abstractmethod, ABC


from kanwoo.entity import File

class FileExistException(Exception):
    pass

class FileStorage(ABC):
    
    @abstractmethod
    def __init__(self, app):
        pass
    
    @abstractmethod
    def init_app(self, app):
        pass

    @abstractmethod
    def save(self, file, relative_path):
        pass

    @abstractmethod
    def delete(self, relative_path):
        pass

    @abstractmethod
    def get_url(self, relative_path):
        pass

class LocalStorage(FileStorage):
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

    def save(self, file: File, relative_path):
        folders_path, _ = relative_path.rsplit("/", maxsplit=1)

        folder_path = os.path.join(self.upload_dir, folders_path)
        file_path = os.path.join(self.upload_dir, relative_path)

        if os.path.exists(file_path):
            raise FileExistException(f"File with path '{relative_path}' already exists.")
        
        if not os.path.exists(folder_path):
            os.makedirs(os.path.join(self.upload_dir, folders_path))

        with open(file_path, "wb") as f:
            f.write(file.bytes)

    def delete(self, relative_path):
        file_path = os.path.join(self.upload_dir, relative_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(file_path)

    def get_url(self, relative_path):
        return self.cdn_url + relative_path
