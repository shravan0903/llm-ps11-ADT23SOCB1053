
from pathlib import Path
from pypdf import PdfReader

# Get the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Define PDF and output file paths
PDF_PATH = BASE_DIR / "data" / "raw" / "admission_handbook_2026_27.pdf"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "college_info.txt"


def extract_pdf_text():

    # Check whether the PDF exists
    if not PDF_PATH.exists():
        print("Error: PDF file not found!")
        return

    # Open the PDF
    reader = PdfReader(str(PDF_PATH))

    extracted_text = []

    # Extract text from every page
    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:
            extracted_text.append(
                f"\n--- Page {page_number} ---\n{text}"
            )

    # Combine all extracted pages
    final_text = "\n".join(extracted_text)

    # Create output folder if it doesn't exist
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save extracted text
    OUTPUT_PATH.write_text(final_text, encoding="utf-8")

    print("PDF text extraction completed!")
    print(f"Total pages: {len(reader.pages)}")
    print(f"Output saved at: {OUTPUT_PATH}")


if __name__ == "__main__":
    extract_pdf_text()
