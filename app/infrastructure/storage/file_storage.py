import os
import uuid

from app.utils import create_link


class FileStorage:
    def __init__(self, app=None):
        self.app = app
        self.upload_folder = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.upload_folder = app.config['UPLOAD_FOLDER']

    def save(self, file, relative_path, ext=None):
        if not os.path.exists(os.path.join(self.upload_folder, relative_path)):
            os.makedirs(os.path.join(self.upload_folder, relative_path))

        if not ext:
            name, ext = os.path.splitext(file.filename)

        identifier = str(uuid.uuid4())
        filename = identifier + ext

        file_path = os.path.join(self.upload_folder, relative_path, filename)

        file.save(file_path)
        return identifier

    def delete(self, relative_path):
        file_path = os.path.join(self.upload_folder, relative_path)
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def get_link(relative_path: str) -> str:
        return create_link(os.path.join("/uploads", relative_path))


file_storage = FileStorage()


class FileStorageAdapter:

    def __init__(self, app=None):
        file_storage.init_app(app)


def setup_file_storage(app):
    FileStorageAdapter(app)