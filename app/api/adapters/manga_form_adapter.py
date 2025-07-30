from dataclasses import dataclass
from marshmallow import ValidationError
from typing import Optional, List, Tuple

from app.api.adapters.upload_file_adapter import UploadFileAdapter
from app.api.schemas.manga.manga_form_schema import MangaFormSchema
from app.domain.entities.file.upload_file import UploadFile


@dataclass
class MangaFormDTO:
    name: str
    name_translations: Optional[List[Tuple[str, str]]]
    description: Optional[str]
    status: Optional[int]
    type: Optional[int]
    adult: Optional[int]
    genres: Optional[List[int]]
    year: Optional[int]
    main_poster: Optional[int]
    new_posters: Optional[List[UploadFile]]
    posters_order: Optional[List[str]]
    background: Optional[UploadFile]
    authors: Optional[List[int]]
    artists: Optional[List[int]]
    publishers: Optional[List[int]]


class MangaFormAdapter:
    @staticmethod
    def adapt(form: dict, files: dict):
        data = dict(form)

        file_adapter = UploadFileAdapter()

        data["new_posters"] = []
        for file in files.getlist("new_posters"):
            data["new_posters"].append(file_adapter.adapt(file))

        if files.get("background"):
            data["background"] = file_adapter.adapt(files["background"])
        else:
            data["background"] = None

        schema = MangaFormSchema()

        try:
            validated_data = schema.load(data)
        except ValidationError as e:
            raise ValueError(f"Invalid form data: {e.messages}")

        return MangaFormDTO(**validated_data)