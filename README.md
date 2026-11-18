
# MIT ADT University College Enquiry Chatbot

## Problem Statement
Problem Statement 11 – College Enquiry Chatbot

## Project Overview
The MIT ADT University College Enquiry Chatbot is an AI-powered
conversational application designed to answer student queries
about university admissions and facilities.

The chatbot uses the MIT ADT University Admission Handbook
2026–27 as its knowledge source and Gemini API for generating
responses to relevant questions.

## Features

- Course eligibility information
- Programme fee structure
- Admission procedure and guidelines
- Required admission documents
- Scholarship and EWS information
- Hostel fees and facilities
- Seat intake information
- International and NRI admission guidance
- Conversational question answering
- Local fallback answers for frequently asked questions

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- PyPDF
- Python-dotenv

## Project Structure

College-Enquiry-Chatbot/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── admission_handbook_2026_27.pdf
│   │
│   └── processed/
│       └── college_info.txt
│
└── utils/
    ├── pdf_processor.py
    ├── retriever.py
    ├── gemini_client.py
    └── chatbot.py

## Installation and Setup

### 1. Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

### 2. Open the Project Folder

cd College-Enquiry-Chatbot

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Gemini API Key

Create a `.env` file in the project root directory.

Add the following configuration:

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_configured_gemini_model

Replace the placeholder values with your actual API credentials
and configured model.

### 5. Run the Application

streamlit run app.py

The application will open in your web browser.

## Knowledge Source

MIT Art, Design and Technology University
Admission Handbook 2026–27.

The handbook is processed into text and used for information
retrieval and answering university-related questions.

## Screenshots

Project screenshots are available in the `screenshots/` folder.

## Security

- API keys are stored in environment variables.
- The `.env` file is excluded using `.gitignore`.
- Virtual environment folders are excluded from Git.

## Project Information

Project: MIT ADT University College Enquiry Chatbot

Problem Statement: 11

Language: Python

Interface: Streamlit

LLM: Google Gemini

Knowledge Source: MIT ADT Admission Handbook 2026–27

## Author
SHRAVAN TUPE
ADT23SOCB1053
