```markdown
# SmartFileSorter

**SmartFileSorter** is an automated document sorting system that classifies and organizes files into categorized directories based on their content using AI. The system reads PDF files, extracts text, classifies the document using a machine learning model, and moves the file to an appropriate folder.

## Features:
- **Automatic Document Classification**: Uses a neural network to classify documents based on content.
- **File Organization**: Sorts files into directories categorized by document type, year, month, and week.
- **Zero-Shot Classification**: Leverages a pre-trained model for classification without the need for custom training.
- **PDF Parsing**: Extracts text from PDF documents to classify and organize them.

## Requirements

Before running the program, make sure you have the following Python libraries installed:

- `transformers`
- `torch`
- `pdfplumber`
- `shutil`
- `os`
- `time`
- `datetime`

You can install the required libraries using the following:

```bash
pip install transformers torch pdfplumber
```

## How It Works

1. **Document Classification**:  
   The program classifies documents based on their content using a neural network. It extracts text from PDF files and uses a pre-trained zero-shot classification model from the `transformers` library to classify the document into one of the predefined categories (e.g., **Фактура** (Invoice), **Протокол** (Protocol), **Отчет** (Report)).

2. **File Sorting**:  
   After classification, the document is moved to the appropriate directory structure. The directories are organized by:
   - Document Type (Invoice, Protocol, Report)
   - Year (from 2020 to 2030)
   - Month (1 to 12)
   - Week (1 to 5)

3. **Monitoring and Sorting Loop**:  
   The script runs in a loop, checking for new files in the `incoming_documents` folder every 30 seconds. If new files are found, they are processed and moved to the correct folder.

## How to Run

1. **Generating Documents** (optional):  
   If you need to generate PDF documents for testing or production, run the `documents.py` script. This script is responsible for creating PDF files that will be used for classification.

   Run it with the following command:
   ```bash
   python documents.py
   ```

2. **Running the Document Sorting System**:  
   After generating the documents, you can run the **SmartFileSorter** program. To start the sorting process, simply run the main script.

   ```bash
   python sorter.py
   ```

   - The program will automatically check the `incoming_documents` folder every 30 seconds.
   - It will classify and move any new documents to the appropriate directories based on their content.

## Directory Structure

The program expects the following directory structure:

```
./incoming_documents/    # Directory where incoming documents are placed
./sorted_documents/      # Directory where documents will be sorted into categorized folders
```

Documents will be moved to directories organized by the document type, year, month, and week, for example:

```
./sorted_documents/Фактури/2024/Месец_12/Седмица_1/
./sorted_documents/Протоколи/2024/Месец_12/Седмица_2/
```

## Configuration

You can modify the following parameters in the `sorter.py` script:
- `CHECK_INTERVAL`: Interval (in seconds) for checking the `incoming_documents` folder.
- `DOCUMENT_TREE`: List of document types (e.g., **Фактури**, **Протоколи**, **Отчети**).

## Example Output

When running the program, you'll see logs in the terminal like this:

```
Document Отчет_2024-11-07.pdf classified as: Report
Sorting document: Отчет_2024-11-07.pdf | Classified as: Report | Remaining time: 30sFile ./incoming_documents\Отчет_2024-11-07.pdf moved to ./sorted_documents\Report\2024\Month_12\Week_2\Отчет_2024-11-07.pdf
```

## Notes

- The program currently supports PDF files only.
- If the program encounters a duplicate file in the destination folder, it will automatically remove the older version and replace it with the new one.

## License

This project is licensed under the MIT License.
```

### Key sections in the `README.md`:
1. **Project Overview** – A brief description of the project and its features.
2. **Requirements** – Instructions to install necessary Python libraries.
3. **How It Works** – Detailed steps explaining the process of classification and sorting.
4. **How to Run** – Clear instructions on running the `documents.py` for document generation and how to run the sorting system.
5. **Directory Structure** – Information about the expected folder structure.
6. **Example Output** – Sample logs to show how the program behaves when sorting files.
7. **Notes** – Additional information about PDF file support and handling duplicates.
8. **License** – The project's license information.
