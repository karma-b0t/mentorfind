# from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup




class UserStates(StatesGroup):
    """Определяем состояния для работы с Users"""

    get_specialities_list = (
        State()
    )  # Состояние для получения списка специальностей, храним список специальностей в состоянии
    get_mentors_list_by_specialities = (
        State()
    )  # Состояние для получения списка менторов по специальности из callback, храним список менторов в состоянии
    get_mentor_info = (
        State()
    )  # Состояние для получения информации о менторе. Храним информацию о менторе в состоянии
    specific_speciality = State()  # Специфическая специальность


    """Определяем состояния для работы с анкетой"""
    start_quizz = State()  # Состояние для начала анкеты
    quiz_in_progress = State()  # Состояние для заполнения анкеты
    finish_quizz = State()  # Состояние для завершения анкеты   


class Pages(StatesGroup):
    next_page = State()  # Состояние для перехода на следующую страницу
    previous_page = State()  # Состояние для перехода на предыдущую страницу

class ChooseMentor(StatesGroup):
    choose_mentor = State()  # Состояние для выбора ментора, начало выбора ментора
    mentor_chosen = State()  # Состояние для выбора ментора, ментор выбран
    mentor_not_chosen = State()  # Состояние для выбора ментора, ментор не выбран
    mentor_info = State()  # Состояние для получения информации о менторе

class MentorStates(StatesGroup):
    """ Состояния для работы с менторами """
    start_quizz = State()  # Состояние для начала анкеты
    quiz_in_progress = State()  # Состояние для заполнения анкеты
    finish_quizz = State()  # Состояние для завершения анкеты
