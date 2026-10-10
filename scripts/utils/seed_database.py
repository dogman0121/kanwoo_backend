from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import config

from kanwoo.models import Privacy
from kanwoo.auth.services import HashService
from kanwoo.user.models import User
from kanwoo.profile.models import Profile
from kanwoo.moderation.models import ModerationStatusType, MangaModerationStatus
from kanwoo.manga.models import Type, Status, Adult, Genre, Manga

def create_privacy(session: Session):
    privacy1 = Privacy(name="приватный")
    privacy2 = Privacy(name="публичный")
    privacy3 = Privacy(name="по ссылке")

    session.add_all([privacy1, privacy2, privacy3])

def create_moderation_status_type(session: Session):
    moderation_type1 = ModerationStatusType(name="подтверждено")
    moderation_type2 = ModerationStatusType(name="отклонено")
    moderation_type3 = ModerationStatusType(name="в ожидании")

    session.add_all([moderation_type1, moderation_type2, moderation_type3])

def create_adult(session: Session):
    adult1 = Adult(name="нет")
    adult2 = Adult(name="6+")
    adult3 = Adult(name="12+")
    adult4 = Adult(name="16+")
    adult5 = Adult(name="18+")

    session.add_all([adult1, adult2, adult3, adult4, adult5])

def create_users(session: Session):
    hash_service = HashService()

    user1 = User(email="x@email.com", password=hash_service.generate_password_hash("12345678")) # id = 1
    user2 = User(email="amogus@email.com", password=hash_service.generate_password_hash("qwerty")) # id = 2
    user3 = User(email="sveta.tsaregorogtseva@email.com", password=hash_service.generate_password_hash("q1w2e3r4t5y6")) # id = 3
    user4 = User(email="megakiller228@email.com", password=hash_service.generate_password_hash("dart-wader")) # id = 4
    user5 = User(email="pippop.boy5453@email.com", password=hash_service.generate_password_hash("ritazueva2005")) # id = 5

    session.add_all([user1, user2, user3, user4, user5])

    session.flush()

def create_profiles(session: Session):
    # without avatar and links
    profile1 = Profile(
        slug="booba1", 
        name="Mi bombo",
        about="Сегодня был сложный день: часы скуки на лекции вытянули из меня всю энергию...",
        creator_id=1,
        owner_id=1
    ) # id = 1

    session.add_all([profile1])

    session.flush()

def create_manga_lookup(session: Session):

    # types
    type1 = Type(name="нет")
    type2 = Type(name="манга")
    type3 = Type(name="манхва")
    type4 = Type(name="маньхуа")
    type5 = Type(name="комикс")
    type6 = Type(name="рукомикс")

    # statuses
    status1 = Status(name="нет")
    status2 = Status(name="ожидается")
    status3 = Status(name="выходит")
    status4 = Status(name="завершено")
    status5 = Status(name="заброшено")
    
    # adults


    # genres
    genre1 = Genre(name="драки")
    genre2 = Genre(name="романтика")
    genre3 = Genre(name="школа")
    genre4 = Genre(name="меха")
    genre5 = Genre(name="нигилизм")

    session.add_all([
        status1, status2, status3, status4, status5,
        type1, type2, type3, type4, type5, type6,
        genre1, genre2, genre3, genre4, genre5
    ])


def create_manga_moderation_status(session: Session):
    moderation_status1 = MangaModerationStatus(
        status_type_id=1,
        message="Статус модерации",
        manga_id=1,
        creator_id=1
    )

    session.add_all([moderation_status1])

    session.flush()

def create_manga(session: Session):

    manga1 = Manga(
        slug="attack-on-titan",
        name="Атака титанов",
        description=""" Мир людей пал под сокрушающей мощью Титанов. Принеся в жертву свою свободу, человечество укрылось в обнесенных высокими стенами городах, в надежде обезопасить выживших. Но в один страшный день появился колоссальный Титан, превосходящий размерами даже городские стены. И хрупкая надежда рассыпалась в прах. Вновь началась отчаянная битва за выживание.""",
        type_id=2,
        status_id=4,
        adult_id=1,
        year=1997,
        creator_id=1,
        author_id=1,
        privacy_id=2
    ) # id = 1

    session.add_all([manga1])

    session.flush()


def create_lookup_tables(session: Session):
    print("Создание справочных таблиц")
    
    create_privacy(session)

    create_moderation_status_type(session)

    create_adult(session)

    create_manga_lookup(session)

def create_entities(session: Session):
    print("Создание сущностей")

    create_users(session)

    create_profiles(session)

    create_manga(session)
    create_manga_moderation_status(session)

def seed_database():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

    session_factory = sessionmaker(bind=engine)
    with session_factory() as session:

        create_lookup_tables(session)

        session.flush()

        create_entities(session)

        session.commit()
    