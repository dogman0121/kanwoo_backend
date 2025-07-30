from werkzeug.datastructures import FileStorage

from app.domain.entities.file.upload_file import UploadFile


class UploadFileAdapter:
    @staticmethod
    def adapt(file: FileStorage) -> UploadFile:
        return UploadFile(
            filename=file.filename,
            content_type=file.content_type,
            bytes=file.read(),
        )