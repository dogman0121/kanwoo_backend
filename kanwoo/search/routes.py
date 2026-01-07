from flask import jsonify, request

from app.search import bp
from app.manga.models import Manga
from app.user.models import User
from app.utils import respond


def parse_manga_filters():
    types = request.args.getlist("type", type=int)
    genres = request.args.getlist("genre", type=int)
    statuses = request.args.getlist("status", type=int)
    adult = request.args.getlist("adult", type=int)


    return {
        "types": types,
        "genres": genres,
        "statuses": statuses,
        "adult": adult
    }

@bp.route('', methods=['GET'], strict_slashes=False)
def search_v1():
    # query = request.args.get('query')
    # section = request.args.get('section')

    # if section == "manga":
    #     return respond(data=[ i.to_dict() for i in Manga.get_with_filters(query, **parse_manga_filters()) ])

    # if section == "user":
    #     return respond(data=[i.to_dict() for i in User.search(query)])

    return respond(data=
        [{
            "adult": {
                "id": 4,
                "name": "18+"
            },
            "artists": [
                {
                    "avatar": "https://cdn.kanwoo.ru/user/4/e719bcfc-61a5-4f2a-a3b8-2fa800a6f8db.jpg",
                    "id": 4,
                    "login": "BednyGamer"
                },
                {
                    "avatar": "",
                    "id": 6,
                    "login": "halz3"
                }
            ],
            "authors": [
                {
                    "avatar": "https://cdn.kanwoo.ru/user/4/e719bcfc-61a5-4f2a-a3b8-2fa800a6f8db.jpg",
                    "id": 4,
                    "login": "BednyGamer"
                }
            ],
            "background": "https://cdn.kanwoo.ru/manga/1/035991c8-9d0a-4a41-8724-b9808ff3c7d7.jpg",
            "description": "Мир людей пал под сокрушающей мощью Титанов. Принеся в жертву свою свободу, человечество укрылось в обнесенных высокими стенами городах, в надежде обезопасить выживших. Но в один страшный день появился колоссальный Титан, превосходящий размерами даже городские стены. И хрупкая надежда рассыпалась в прах. Вновь началась отчаянная битва за выживание.",
            "genres": [
                {
                    "id": 1,
                    "name": "драки"
                },
                {
                    "id": 2,
                    "name": "романтика"
                }
            ],
            "id": 1,
            "main_poster": {
                "large": "https://cdn.kanwoo.ru/manga/1/527f919f-2bb0-41df-8520-08a4575a3e0e.jpg",
                "medium": "https://cdn.kanwoo.ru/manga/1/20dfb35e-dc13-4a36-800f-985c65e8faee.jpg",
                "original": "https://cdn.kanwoo.ru/manga/1/f62d271e-d317-43e7-b4a1-e0ec6d2dfa3f.jpg",
                "small": "https://cdn.kanwoo.ru/manga/1/0e7da863-b948-4928-95d7-e16c0c21c7bb.jpg",
                "thumbnail": "https://cdn.kanwoo.ru/manga/1/41095d3e-48ea-4089-93b8-b26e2916d4ef.jpg",
                "uuid": "53a2e945-1024-450c-9dff-7dda0b25cfba"
            },
            "name": "Атака титанов",
            "name_translations": [
                {
                    "lang": "en",
                    "name": "Attack on titan"
                },
                {
                    "lang": "jp",
                    "name": "進撃の巨人"
                }
            ],
            "permissions": {},
            "posters": [
                {
                    "large": "https://cdn.kanwoo.ru/manga/1/2bd44990-fc0a-4207-95d9-83ebc29872b6.jpg",
                    "medium": "https://cdn.kanwoo.ru/manga/1/9361da49-490c-4cb1-9253-09a8a0c83e16.jpg",
                    "original": "https://cdn.kanwoo.ru/manga/1/cefc3700-b658-4b48-b479-6d0f1c015cc0.jpg",
                    "small": "https://cdn.kanwoo.ru/manga/1/5fa2525d-bd2c-406a-88e4-880325ce29b4.jpg",
                    "thumbnail": "https://cdn.kanwoo.ru/manga/1/c3a413e0-fe44-495e-8e57-70209ff881b9.jpg",
                    "uuid": "4ee33a5c-411d-4662-9892-22315bff27a5"
                },
                {
                    "large": "https://cdn.kanwoo.ru/manga/1/527f919f-2bb0-41df-8520-08a4575a3e0e.jpg",
                    "medium": "https://cdn.kanwoo.ru/manga/1/20dfb35e-dc13-4a36-800f-985c65e8faee.jpg",
                    "original": "https://cdn.kanwoo.ru/manga/1/f62d271e-d317-43e7-b4a1-e0ec6d2dfa3f.jpg",
                    "small": "https://cdn.kanwoo.ru/manga/1/0e7da863-b948-4928-95d7-e16c0c21c7bb.jpg",
                    "thumbnail": "https://cdn.kanwoo.ru/manga/1/41095d3e-48ea-4089-93b8-b26e2916d4ef.jpg",
                    "uuid": "53a2e945-1024-450c-9dff-7dda0b25cfba"
                }
            ],
            "publishers": [
                {
                    "avatar": "",
                    "id": 5,
                    "login": "dogman_0121"
                },
                {
                    "avatar": "",
                    "id": 6,
                    "login": "halz3"
                }
            ],
            "rating": 9.5,
            "rating_count": 2,
            "saves": 0,
            "slug": "ataka-titanov",
            "status": {
                "id": 4,
                "name": "завершен"
            },
            "translations": [
                {
                    "chapters_count": 9,
                    "id": 2,
                    "permissions": {},
                    "translator": {
                        "avatar": "https://cdn.kanwoo.ru/user/1/3a757921-fc73-4ba5-a70f-afdebb882b38.jpg",
                        "id": 1,
                        "login": "ivanzolo2004"
                    },
                    "translator_type": "user"
                }
            ],
            "type": {
                "id": 2,
                "name": "манга"
            },
            "user_lists": [],
            "user_rating": None,
            "views": 2778,
            "year": 2009
        },
        {
            "adult": {
                "id": 3,
                "name": "16+"
            },
            "artists": [],
            "authors": [],
            "background": None,
            "description": "«Похоже, в будущем меня не ожидало ничего хорошего. Поэтому „стоимость“ моей жизни была всего 10000 иен за год. Разочаровавшись в своём будущем, я продал большую часть жизни и стал пытаться обрести счастье в то короткое время, что у меня осталось. На случай, если я впаду в отчаяние и начну создавать проблемы, ко мне послали девушку „наблюдателя“. Со временем я понял, что был бы счастливее, живя ради неё. Но у меня осталось меньше двух месяцев жизни…»",
            "genres": [],
            "id": 2,
            "main_poster": {
                "large": "https://cdn.kanwoo.ru/manga/2/e54d9dce-fa8b-468a-8db8-4bd3364f5450.jpg",
                "medium": "https://cdn.kanwoo.ru/manga/2/eeb2f638-e130-41d4-a000-a1a1b2e731b8.jpg",
                "original": "https://cdn.kanwoo.ru/manga/2/503d6678-ce7c-45f7-a041-0e2a34b5676a.jpg",
                "small": "https://cdn.kanwoo.ru/manga/2/f6223d07-bb59-42b8-9e4b-0ea7c2692f4b.jpg",
                "thumbnail": "https://cdn.kanwoo.ru/manga/2/5cc34ba1-289a-4c61-93b9-7be12ac80f61.jpg",
                "uuid": "64c1a122-01d1-44b8-a9f9-431d0eb9351d"
            },
            "name": "Я распродал свою жизнь. По десять тысяч иен за год.",
            "name_translations": [],
            "permissions": {},
            "posters": [
                {
                    "large": "https://cdn.kanwoo.ru/manga/2/e54d9dce-fa8b-468a-8db8-4bd3364f5450.jpg",
                    "medium": "https://cdn.kanwoo.ru/manga/2/eeb2f638-e130-41d4-a000-a1a1b2e731b8.jpg",
                    "original": "https://cdn.kanwoo.ru/manga/2/503d6678-ce7c-45f7-a041-0e2a34b5676a.jpg",
                    "small": "https://cdn.kanwoo.ru/manga/2/f6223d07-bb59-42b8-9e4b-0ea7c2692f4b.jpg",
                    "thumbnail": "https://cdn.kanwoo.ru/manga/2/5cc34ba1-289a-4c61-93b9-7be12ac80f61.jpg",
                    "uuid": "64c1a122-01d1-44b8-a9f9-431d0eb9351d"
                }
            ],
            "publishers": [],
            "rating": 9.0,
            "rating_count": 1,
            "saves": 0,
            "slug": "ya-rasprodal-svoyu-zhizn-po-desyat-tyisyach-ien-za-god",
            "status": {
                "id": 4,
                "name": "завершен"
            },
            "translations": [
                {
                    "chapters_count": 8,
                    "id": 7,
                    "permissions": {},
                    "translator": {
                        "avatar": "https://cdn.kanwoo.ru/user/1/3a757921-fc73-4ba5-a70f-afdebb882b38.jpg",
                        "id": 1,
                        "login": "ivanzolo2004"
                    },
                    "translator_type": "user"
                }
            ],
            "type": {
                "id": 2,
                "name": "манга"
            },
            "user_lists": [],
            "user_rating": None,
            "views": 298,
            "year": 2016
        },
        ]
    )