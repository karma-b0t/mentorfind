import json
from pathlib import Path
from loguru import logger

from utils.parsers import parse_reviews
from .models import Mentor, User
from sqlalchemy import case, create_engine, or_
from sqlalchemy.orm import sessionmaker
from .models import DATABASE_URL
import datetime
from utils.ai_tools import get_mentor_by_quizz


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


current_datetime_str = datetime.datetime.now()


class AddDataToDB:

    def add_user_to_db(session, telegram_id, username, **kwargs):
        try:
            existing_user = (
                session.query(User).filter_by(telegram_id=telegram_id).first()
            )
            if existing_user:
                session.commit()
            else:
                new_user = User(telegram_id, username, **kwargs)
                session.add(new_user)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")


class ParseDataFromNet:
    def add_mentor_to_db(session, name, specialty, price, contact, description):
        try:
            existing_mentor = session.query(Mentor).filter_by(name=name).first()
            if existing_mentor:
                session.commit()
            else:
                new_mentor = Mentor(
                    name=name,
                    specialty=specialty,
                    price=price,
                    contact=contact,
                    description=description,
                )
                session.add(new_mentor)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")

    def add_prices_to_db(session):
        try:
            mentors = session.query(Mentor).all()
            for mentor in mentors:
                try:
                    price = mentor.price
                    if "http" in price:
                        price_data = get_mentor_by_quizz.get_advice_from_quizz(price)
                        mentor.price = json.dumps(price_data, ensure_ascii=False)
                    else:
                        print(f"Price for {mentor.name} is not a link")
                except Exception as e:
                    print(f"An error occurred in step add_prices_to_db: {e}")
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred in step add_prices_to_db: {e}")

    def add_description_to_db(session):
        try:
            mentors = session.query(Mentor).all()
            for mentor in mentors:
                try:
                    description = mentor.description
                    if "http" in description:
                        description_data = get_mentor_by_quizz.get_advice_from_quizz(
                            description
                        )
                        mentor.description = json.dumps(
                            description_data, ensure_ascii=False
                        )
                        # mentor.price = price

                        print(f"Description for {mentor.name} updated in DB")
                    else:
                        print(f"Description for {mentor.name} is not a link")
                except Exception as e:
                    print(f"An error occurred in step add_description_to_db: {e}")
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred in step add_description_to_db: {e}")

    async def add_reviews_to_db(session):
        try:
            mentors = session.query(Mentor).all()
            for mentor in mentors:
                try:
                    reviews = await parse_reviews.search_reviews(mentor.name)
                    """
                    Serialize reviews to JSON, иначе выскакивает ошибка бд
                    """
                    mentor.reviews = json.dumps(
                        reviews, ensure_ascii=False
                    )  # Serialize reviews to JSON
                    print(f"Reviews for {mentor.name} updated in DB")
                except Exception as e:
                    print(f"An error occurred in step add_reviews_to_db: {e}")
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred in step add_reviews_to_db: {e}")

    def add_grade_to_db(session):
        try:
            mentors = session.query(Mentor).all()
            with open("rate1.txt", "r") as f:
                lines = f.readlines()
            if len(lines) != len(mentors):
                print("Количество оценок не совпадает с количеством менторов")
            try:
                for i, mentor in enumerate(mentors):
                    if (
                        lines[i] != "None"
                        and lines[i]
                        != "An error occurred in 1 step add_grade_to_db: 'rating'\n"
                        and lines[i] != "None\n"
                    ):
                        mentor.rating = float(lines[i])
            except Exception as e:
                print(f"An error occurred in step 1 add_grade_to_db: {e}")
            finally:

                session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred in step 2 add_grade_to_db: {e}")

    def add_speciality_to_db(session):
        try:
            # Получаем всех менторов из базы данных
            mentors = session.query(Mentor).all()

            # Создаем словарь для хранения специальностей
            speciality_dict = {}

            # Открываем файл и читаем строки с данными менторов
            with open("mentors.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()

                # Заполняем словарь специальностями
                for line in lines:
                    try:
                        # Извлекаем имя и специальность из строки файла
                        mentor_name_from_file = (
                            line.split("name:")[1].split("specialty:")[0].strip()
                        )
                        speciality_from_file = (
                            line.split("specialty:")[1].split("price:")[0].strip()
                        )

                        # Добавляем в словарь
                        speciality_dict[mentor_name_from_file] = speciality_from_file
                    except Exception as e:
                        print(f"Ошибка при обработке строки: {line}. Ошибка: {e}")

            # Проходим по всем менторам в базе данных
            for mentor in mentors:
                # Проверяем, есть ли специальность в словаре по имени ментора
                if mentor.name in speciality_dict:
                    mentor.speciality = speciality_dict[mentor.name]
                    # print(f"Специальность для {mentor.name} обновлена: {mentor.speciality}")
                else:
                    print(f"Специальность для {mentor.name} не найдена в словаре.")

            # Сохраняем изменения в базе данных
            session.commit()
            # print("Специальности успешно добавлены в базу данных.")
        except Exception as e:
            # В случае ошибки откатываем транзакцию
            session.rollback()
            print(f"An error occurred in step add_speciality_to_db: {e}")


class GetDataFromDB:

    def get_mentors_by_speciality_from_db(session, speciality):
        """
        Посмотреть корректность возвращаемых данных, при необходимости сделать общую функцию -
        дергать имя ментора по специальности, дальше смотреть по логике бота

        """
        try:
            mentors_query = session.query(Mentor).filter(
                Mentor.speciality.ilike(f"%{speciality}%")
            )
            all_mentors = mentors_query.all()
            mentors_list = []
            for mentor in all_mentors:
                mentor = {
                    "id": mentor.id,
                    "name": mentor.name,
                    "speciality": mentor.speciality,
                    "description": mentor.description,
                }
                mentors_list.append(mentor)
            return mentors_list
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_mentors_by_speciality_from_json(session, speciality):
        try:
            if len(str(speciality).split(" ")) > 1:
                filepath = Path("utils") / "specialities.json"
                with open(filepath, "r") as f:
                    specialities = json.load(f)
                speciality_values = specialities[speciality]
                print("speciality_values:", speciality_values)
            if len(str(speciality).split(" ")) == 1:
                mentors_query = session.query(Mentor).filter(
                    Mentor.speciality.ilike(f"%{speciality}%")
                )
            else:
                mentors_query = session.query(Mentor).filter(
                    or_(
                        *(
                            Mentor.speciality.ilike(f"%{value.strip()}%")
                            for value in speciality_values
                        )
                    )
                )

            # Сортируем так, чтобы None были в конце списка
            query = mentors_query.order_by(
                case(
                    (
                        Mentor.reviews == None,
                        1,
                    ),  # Если рейтинг None, ставим его на последнее место
                    else_=0,  # Все остальные рейтинги будут на первом месте
                )
            )
            all_mentors = query.all()
            mentors_list = []
            for mentor in all_mentors:
                mentor = {
                    "id": mentor.id,
                    "name": mentor.name,
                    "speciality": mentor.speciality,
                    "description": mentor.description,
                }
                mentors_list.append(mentor)
            return mentors_list
        except Exception as e:
            print(f"An error occurred in get_mentors_by_speciality_from_db: {e}")

    def get_mentor_name_from_db(session, mentors_list):
        try:
            mentor_name = []
            for mentor in mentors_list:
                mentor_name.append(mentor.split(" ")[0])
            return mentor_name
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_specialities_from_db(session):
        try:
            specialities = session.query(Mentor.speciality).distinct().all()
            specialities_list = []
            for speciality in specialities:
                specialities_list.append(speciality)
            return specialities_list
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_specialities_list_from_json():
        specialities_list = []
        try:
            filepath = Path("utils") / "specialities.json"
            with open(filepath, "r") as f:
                specialities = json.load(f)
                for key, value in specialities.items():
                    specialities_list.append(key)
            return specialities
        except Exception as e:
            print(f"An error occurred n step get_specialities_list_from_json: {e}")

    def get_specific_specialities_list_from_db(session, mentor):
        try:
            mentor_query = session.query(Mentor).filter(
                Mentor.speciality.ilike(f"%{mentor}%")
            )
            all_mentors = mentor_query.all()
            mentors_list = []

            for mentor in all_mentors:
                mentor = {
                    "id": mentor.id,
                    "name": mentor.name,
                    "speciality": mentor.speciality,
                    "description": mentor.description,
                }
                mentors_list.append(mentor)
            return mentors_list
        except Exception as e:
            print(
                f"An error occurred on step get_specific_specialities_list_from_json: {e}"
            )
            return None

    def get_mentor_info_by_id_from_db(session, mentor_id):
        try:
            mentor = session.query(Mentor).filter_by(id=mentor_id).first()
            mentor_info = {
                "name": mentor.name,
                "speciality": mentor.speciality,
                "price": mentor.price,
                "contact": mentor.contact,
                "description": mentor.description,
                "reviews": mentor.reviews,
            }
            return f'{mentor_info["name"]}\nСпециальность: {mentor_info["speciality"]}\nЦена: {mentor_info["price"]}\nКонтакты: {mentor_info["contact"]}\nОписание: {mentor_info["description"]}'
        except Exception as e:
            print(f"An error occurred on step get_mentor_info_from_db: {e}")

    def get_mentor_reviews_from_db(session, mentor_id):
        try:
            mentor = session.query(Mentor).filter_by(id=mentor_id).first()
            reviews = mentor.reviews
            return reviews
        except Exception as e:
            print(f"An error occurred on step get_mentor_reviews_from_db: {e}")
            return None

    def get_all_mentors_from_db(session):
        try:
            mentors = session.query(Mentor).all()
            mentors_list = [
                {
                    "id": mentor.id,
                    "name": mentor.name,
                    "speciality": mentor.speciality,
                    "description": mentor.description,
                    "price": mentor.price,
                    "contact": mentor.contact,
                    "reviews": mentor.reviews,
                }
                for mentor in mentors
            ]

            # Запись в JSON-файл
            with open("downloads/mentors.json", "w", encoding="utf-8") as f:
                json.dump(mentors_list, f, ensure_ascii=False, indent=4)

            print("Data has been written to mentors.json")

        except Exception as e:
            print(f"An error occurred in get_all_mentors_from_db: {e}")
            return None

    def get_mentor_by_link_from_db(session, nick: str):
        try:
            mentor_query = session.query(Mentor).filter(
                Mentor.contact.ilike(f"%{nick}%")
            )
            mentor = mentor_query.first()
            
            if mentor is None:
                logger.info(f"No mentor found with nick: {nick}")
                return None
            
            mentor_info = {
                "id": mentor.id,
                "name": mentor.name,
                "speciality": mentor.speciality,
                "price": mentor.price,
                "contact": mentor.contact,
                "description": mentor.description,
            }
            session.commit()
            return {
                "description": f'Имя: {mentor_info["name"]}\nСпециальность: {mentor_info["speciality"]}\nОписание: {mentor_info["description"]}',
                "id": mentor_info["id"],
            }
        except Exception as e:
            session.rollback()  # Roll back the failed transaction
            logger.error(f"An error occurred on step get_mentor_by_nick_from_db: {e}")
            return None
        finally:
            session.close()  # Ensure the session is closed


if __name__ == '__main__':
    GetDataFromDB.get_mentor_by_link_from_db(session, 'artarba')