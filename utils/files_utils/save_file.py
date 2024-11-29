import os

from docx import Document
from main import bot


async def save_file(message):
    # Получаем file_id документа
    file_id = message.document.file_id

    # Загружаем информацию о файле
    file_info = await bot.get_file(file_id)

    # Загружаем файл как байтовые данные
    file = await bot.download_file(file_info.file_path)

    # Указываем путь для сохранения файла
    file_name = message.document.file_name
    file_path = os.path.join('downloads', file_name)
    
    # Сохраняем файл локально
    try:
        with open(file_path, "wb") as f:
            f.write(file.read())  # Записываем байты

        print(f"Файл '{file_name}' успешно загружен и сохранен.")
    except Exception as e:
        print(f"Ошибка при сохранении файла '{file_name}': {e}")
    return file_path, file_name


async def extract_text_from_word_file(file_path, file_name):
    
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.docx':
            doc = Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)

            path = f"downloads/{file_name}.txt"

            string = "\n".join(full_text)
            with open(path, "w", encoding="utf-8") as f:
                f.write(string)
            print(
                f"Текст из файла '{file_name}' успешно извлечен и сохранен в файл '{file_path}.txt'."
            )
            print('path from extract_text_from_word_file:', path)
            return path
        path = await extract_text_with_pdfplumber(file_path, file_name)
        print('path from extract_text_from_pdf_file:', path)
        return path

    except Exception as e:
        print(f"Ошибка при извлечении текста из файла '{file_path}': {e}")
    

import pdfplumber

async def extract_text_with_pdfplumber(file_path, file_name):
    with pdfplumber.open(file_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    # print(full_text) # Выводим текст на экран
    try:
        path = f"downloads/{file_name}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print(f"Текст из файла '{file_name}' успешно извлечен и сохранен в файл {path}.")
        return path
    except Exception as e:
        print(f"Ошибка при извлечении текста из файла '{file_path}': {e}")




# import asyncio

# async def main():
#     file_path = r'downloads\Павел Кирсанов CV.pdf'
#     file_name = 'Павел Кирсанов CV'
#     await extract_text_with_pdfplumber(file_path, file_name)

# if __name__ == "__main__":
#     asyncio.run(main())