# from .parse_business_card import parse_business_card
# from .parse_notion import scroll_and_collect
# from .get_link_from_db import get_link_from_db
# from .processing_link import processing_link
# from .get_is_link import get_is_link
from .ai_tools.get_mentor_by_quizz import get_advice_from_quizz
from .files_utils.save_file import save_file, extract_text_from_word_file
from .ai_tools.get_mentor_by_resume import get_mentor_by_cv
from .states import UserStates, Pages, ChooseMentor
from .text_utils.get_mentors_list_from_advice import get_mentors_list_from_advice