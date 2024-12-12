import os
import shutil
import time
from datetime import datetime
import pdfplumber
from transformers import pipeline

# Parameters for the directories
INPUT_DIR = "./incoming_documents"
OUTPUT_DIR = "./sorted_documents"
CHECK_INTERVAL = 30  # seconds between checks

# Create the directory structure
DOCUMENT_TREE = ["Invoices", "Protocols", "Reports"]
for doc_type in DOCUMENT_TREE:
    for year in range(2020, 2031):  # Years from 2020 to 2030
        for month in range(1, 13):
            for week in range(1, 6):
                path = os.path.join(OUTPUT_DIR, doc_type, str(year), f"Month_{month}", f"Week_{week}")
                os.makedirs(path, exist_ok=True)

os.makedirs(INPUT_DIR, exist_ok=True)

# Load pre-trained model for text classification
classifier = pipeline("zero-shot-classification")

# Function to extract text from a PDF document
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

# Function to classify a document with a neural network
def classify_document(file_path):
    # Extract text from the PDF file
    text = extract_text_from_pdf(file_path)
    
    # If no text is found, return None (we can't classify the document)
    if not text:
        print(f"No text extracted from {file_path}. Skipping classification.")
        return None
    
    # Define candidate labels
    candidate_labels = ["Invoice", "Protocol", "Report"]
    
    # Use the classifier to classify the document
    result = classifier(text, candidate_labels)
    
    # Return the label with the highest score
    doc_type = result['labels'][0]
    return doc_type

# Function to calculate the week of the month
def get_week_of_month(date):
    day_of_month = date.day
    week_of_month = (day_of_month - 1) // 7 + 1
    return week_of_month

# Function to move a file to the correct directory
def move_file_to_correct_directory(file_path, doc_type, document_date):
    if doc_type is None:
        return
    
    week_of_month = get_week_of_month(document_date)
    
    # Build the target directory path
    target_dir = os.path.join(OUTPUT_DIR, doc_type, str(document_date.year), f"Month_{document_date.month}", f"Week_{week_of_month}")
    os.makedirs(target_dir, exist_ok=True)

    # Define the target file path
    target_file_path = os.path.join(target_dir, os.path.basename(file_path))
    
    # If the file already exists, don't overwrite it unless explicitly needed
    if os.path.exists(target_file_path):
        print(f"Found duplicate file: {target_file_path}. Renaming and adding new version.")
        base_name, ext = os.path.splitext(target_file_path)
        counter = 1
        while os.path.exists(f"{base_name}_{counter}{ext}"):
            counter += 1
        target_file_path = f"{base_name}_{counter}{ext}"
    
    # Move the file to the target directory
    shutil.move(file_path, target_file_path)
    print(f"File {file_path} moved to {target_file_path}")

def display_sorting_progress(file_name, doc_type, remaining_time):
    print(f"\rSorting document: {file_name} | Classified as: {doc_type} | Remaining time: {remaining_time}s", end="")

# Main loop for sorting documents
while True:
    start_time = time.time()
    files = os.listdir(INPUT_DIR)

    if not files:
        print(f"\nNo files to sort. Checking again in {CHECK_INTERVAL} seconds.")
        
        for remaining_time in range(CHECK_INTERVAL, 0, -1):
            display_sorting_progress("No files", "", remaining_time)
            time.sleep(1)
        continue

    for file_name in files:
        file_path = os.path.join(INPUT_DIR, file_name)

        # Classify the document using the neural network
        doc_type = classify_document(file_path)
        
        if doc_type is None:
            continue  # Skip files that could not be classified

        print(f"\nDocument {file_name} classified as: {doc_type}")

        # Move the file to the correct directory
        display_sorting_progress(file_name, doc_type, CHECK_INTERVAL)
        time.sleep(1)  # Simulate some sorting time
        move_file_to_correct_directory(file_path, doc_type, datetime.now())

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTime taken for this iteration: {elapsed_time:.2f} seconds.")

    for remaining_time in range(CHECK_INTERVAL, 0, -1):
        display_sorting_progress("Sorting...", "Invoices", remaining_time)
        time.sleep(1)
