from typing import Tuple

from app.domain.entities.manga import Manga
from app.domain.entities.file.upload_file import UploadFile
from app.domain.repositories.storage.manga_poster_file_storage import MangaPosterFileStorage
from app.infrastructure.storage import file_storage
from app.infrastructure.storage.pillow_file_image import PillowFileImage


class LocalMangaPosterFileStorage(MangaPosterFileStorage):
    @staticmethod
    def _prepare_image(img: PillowFileImage, poster_size: Tuple[int, int]) -> PillowFileImage:
        ratio = img.size[0] / img.size[1]

        # Check if image has horizontal or vertical align
        if ratio < 1:
            new_height = poster_size[1]
            new_width = int(poster_size[1] * ratio)
        else:
            new_height = int(poster_size[0] * ratio)
            new_width = poster_size[0]

        new_img = img.copy().convert("RGB").resize((new_width, new_height))

        return new_img

    def save(self, manga_id: int, poster_file: UploadFile, poster_size: Tuple[int, int]) -> str:
        img = PillowFileImage(poster_file)

        new_img = self._prepare_image(img, poster_size)

        uuid = file_storage.save(new_img, relative_path=f"posters/{manga_id}/", ext=".jpg")

        return uuid


    def delete(self, manga_id: int, file_uuid: str, file_ext: str) -> None:
        file_storage.delete(relative_path=f"posters/{manga_id}/{file_uuid}{file_ext}")

    def get_link(self, manga_id: int, file_uuid: str) -> str:
        return file_storage.get_link(f"/manga/{manga_id}/{file_uuid}.jpeg")