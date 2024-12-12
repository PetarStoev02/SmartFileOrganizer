from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import random
from datetime import datetime, timedelta

# Създаване на директория за документите, ако не съществува
if not os.path.exists("./incoming_documents"):
    os.makedirs("./incoming_documents")

# Примерни данни за документите
invoices = [
    "Фактура за предоставените услуги по проект XYZ. Общо за плащане: 1500 лв.",
    "Фактура за консултантски услуги предоставени през месец май 2023 г. Сума: 2500 лв.",
    "Фактура за ремонтни услуги извършени на 12.06.2023 г. Общо за плащане: 450 лв.",
    "Фактура за транспортни услуги, предоставени през месец юни 2023 г. Сума: 1200 лв."
]

protocols = [
    "Протокол от проведеното заседание на управителния съвет на фирма ABC на 15.09.2023 г. Дискутирани теми: нови проекти, бъдещи инвестиции и пазарни стратегии.",
    "Протокол от заседание на екип за развитие на продукта, проведено на 20.11.2023 г. Решени задачи: оптимизация на текущия код и план за нови функции.",
    "Протокол от заседание на комисията за подбор на нови служители, проведено на 01.12.2023 г. Дискутирани кандидати за позицията мениджър продажби."
]

reports = [
    "Годишен отчет за финансовото състояние на фирма XYZ за 2023 г. Приходи: 1 000 000 лв., разходи: 800 000 лв.",
    "Отчет за изпълнение на проект 'Анализ на пазара' през второто тримесечие на 2024 г. Резултати: успешно завършени 3 ключови етапа.",
    "Отчет за текущото състояние на проекта за изграждане на нов офис сграда. Завършени етапи: основи, стени, покрив."
]

# Функция за генериране на произволна дата в рамките на дадената година
def generate_random_date(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date

# Функция за генериране на документ с произволно съдържание
def create_pdf(doc_type, content, file_name, date):
    file_path = os.path.join("./incoming_documents", f"{file_name}.pdf")
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Извличане на месец и седмица
    month = date.strftime("%B")  # Месец на български
    day = date.day
    week_number = date.strftime("%U")  # Номер на седмицата от годината

    # Добавяне на информация в документа
    c.drawString(100, 750, f"Документ: {doc_type}")
    c.drawString(100, 730, f"Съдържание: {content}")
    c.drawString(100, 710, f"Дата: {date.strftime('%d-%m-%Y')}")
    c.drawString(100, 690, f"Месец: {month}")
    c.drawString(100, 670, f"Седмица: {week_number}")
    c.save()

    # Генериране на ново име на файл с включена дата
    file_name_with_date = f"{doc_type}_{date.strftime('%Y-%m-%d')}"
    return file_name_with_date

# Генериране на 10 документа (4 фактури, 3 протокола, 3 отчета)
for i in range(4):
    random_date = generate_random_date(2024)  # Генериране на произволна дата за 2024 година
    file_name = create_pdf("Фактура", random.choice(invoices), f"Фактура_{random_date.strftime('%Y-%m-%d')}", random_date)
    print(f"Документ създаден: {file_name}.pdf")

for i in range(3):
    random_date = generate_random_date(2024)  # Генериране на произволна дата за 2024 година
    file_name = create_pdf("Протокол", random.choice(protocols), f"Протокол_{random_date.strftime('%Y-%m-%d')}", random_date)
    print(f"Документ създаден: {file_name}.pdf")

for i in range(3):
    random_date = generate_random_date(2024)  # Генериране на произволна дата за 2024 година
    file_name = create_pdf("Отчет", random.choice(reports), f"Отчет_{random_date.strftime('%Y-%m-%d')}", random_date)
    print(f"Документ създаден: {file_name}.pdf")

print("PDF файловете са създадени в папката 'incoming_documents'.")
