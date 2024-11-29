

async def process_template(variables):
    file_path = "utils/text_utils/roadmap_template.txt"
    with open(file_path, "r") as file:
        template = file.read()
    return template.format(**variables)

variables = {
    "level": "junior",
    "experience": 2,
    "goal": "Получить работу в IT",
    "steck": "Python",
    "time_on_learning": 10
}
# 1. **Уровень владения Python:** {level}.
# 2. **Текущий опыт в IT:** {experience}.
# 3. **Цели пользователя:** {goal}.
# 4. **Предпочтительные технологии:** {steck}.
# 5. **Доступное время на обучение:** {time_on_learning}.

# print( process_template(variables))