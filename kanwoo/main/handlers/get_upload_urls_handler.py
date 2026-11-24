from flask import request
from dataclasses import dataclass
from dependency_injector.wiring import Provide, inject

from kanwoo import AppContainer, respond
from kanwoo.unit_of_work import UnitOfWork
from kanwoo.uuid import UUIDGenerator
from kanwoo.file_storage import FileStorageMixin
from kanwoo.main.schemas import UploadFileSchema
from kanwoo.models import FileModel
from kanwoo.main.schemas import PresignedURLSchema

def get_megabytes_in_bytes(size: int | float):
    return int(size * 1024 * 1024)

MAX_FILE_SIZES = {
    "profile_avatar": get_megabytes_in_bytes(4),
    "chapter_page": get_megabytes_in_bytes(20)
}

@dataclass
class PresignedURLDTO:
    uuid: str
    url: str

@inject
def get_upload_urls_handler(
    uow: UnitOfWork = Provide[AppContainer.unit_of_work],
    storage: FileStorageMixin = Provide[AppContainer.file_storage]
):
    schema_data = UploadFileSchema(many=True).load(request.json)

    links_list = []
    with uow:
        for file_data in schema_data:
            uuid = UUIDGenerator.generate_uuid_v4()
            file_type = file_data.get("file_type")

            file = FileModel(
                uuid=uuid,
                filename=file_data.get("name"),
                mimetype=file_data.get("mimetype"),
                file_size=file_data.get("file_size")
            )

            file.add()

            presigned_url = storage.get_upload_url(
                uuid,
                min_file_size=0,
                max_file_Size=MAX_FILE_SIZES.get(
                    file_type, get_megabytes_in_bytes(20)
                ),
                expires_in=900
            )

            links_list.append(
                PresignedURLDTO(
                    uuid=uuid,
                    url=presigned_url
                )
            )

        return respond(data=PresignedURLSchema().dump(links_list, many=True))
    