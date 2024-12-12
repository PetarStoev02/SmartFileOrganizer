import os
import shutil
import time
from datetime import datetime
import pdfplumber
from transformers import pipeline

# Параметри на директорията
INPUT_DIR = "./incoming_documents"
OUTPUT_DIR = "./sorted_documents"
CHECK_INTERVAL = 30  # секунди между проверки

# Създаване на структурата на директориите
DOCUMENT_TREE = ["Фактури", "Протоколи", "Отчети"]
for doc_type in DOCUMENT_TREE:
    for year in range(2020, 2031):  # Години от 2020 до 2030
        for month in range(1, 13):
            for week in range(1, 6):
                path = os.path.join(OUTPUT_DIR, doc_type, str(year), f"Месец_{month}", f"Седмица_{week}")
                os.makedirs(path, exist_ok=True)

os.makedirs(INPUT_DIR, exist_ok=True)

# Зареждаме предварително обучен модел за класификация на текст
classifier = pipeline("zero-shot-classification")

# Функция за извличане на текст от PDF документ
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Функция за класифициране на документ с невронна мрежа
def classify_document(file_path):
    # Извличаме текст от PDF файла
    text = extract_text_from_pdf(file_path)
    
    # Преглеждаме няколко категории и избираме най-подходящата
    candidate_labels = ["Фактура", "Протокол", "Отчет"]
    result = classifier(text, candidate_labels)

    # Връщаме категорията с най-висока вероятност
    doc_type = result['labels'][0]
    return doc_type

# Функция за изчисляване на седмица от месеца
def get_week_of_month(date):
    day_of_month = date.day
    week_of_month = (day_of_month - 1) // 7 + 1
    return week_of_month

# Функция за преместане на файл в правилната директория
def move_file_to_correct_directory(file_path, doc_type, document_date):
    if doc_type is None:
        return

    week_of_month = get_week_of_month(document_date)

    target_dir = os.path.join(OUTPUT_DIR, doc_type, str(document_date.year), f"Месец_{document_date.month}", f"Седмица_{week_of_month}")
    os.makedirs(target_dir, exist_ok=True)

    target_file_path = os.path.join(target_dir, os.path.basename(file_path))
    if os.path.exists(target_file_path):
        print(f"Намерено дублирано файл: {target_file_path}. Премахваме стария файл и добавяме новия.")
        os.remove(target_file_path)

    shutil.move(file_path, target_dir)
    print(f"Файлът {file_path} беше преместен в {target_dir}")

def display_sorting_progress(file_name, doc_type, remaining_time):
    print(f"\rСортиране на документ: {file_name} | Класифициран като: {doc_type} | Остатъчно време: {remaining_time}s", end="")

# Основен цикъл за сортиране на документи
while True:
    start_time = time.time()
    files = os.listdir(INPUT_DIR)

    if not files:
        print(f"\nНяма файлове за сортиране. Ще проверим отново след {CHECK_INTERVAL} секунди.")
        
        for remaining_time in range(CHECK_INTERVAL, 0, -1):
            display_sorting_progress("Няма файлове", "", remaining_time)
            time.sleep(1)
        continue

    for file_name in files:
        file_path = os.path.join(INPUT_DIR, file_name)

        # Класифицираме документа с невронната мрежа
        doc_type = classify_document(file_path)
        print(f"\nДокументът {file_name} беше класифициран като: {doc_type}")

        # Преместваме файла
        display_sorting_progress(file_name, doc_type, CHECK_INTERVAL)
        time.sleep(1)  # Симулираме известно време за анимация на сортирането
        move_file_to_correct_directory(file_path, doc_type, datetime.now())

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nВреме, необходимо за тази итерация: {elapsed_time:.2f} секунди.")

    for remaining_time in range(CHECK_INTERVAL, 0, -1):
        display_sorting_progress("Сортиране...", "Фактури", remaining_time)
        time.sleep(1)
