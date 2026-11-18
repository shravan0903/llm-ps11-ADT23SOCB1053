
from pathlib import Path
import re


# ==================================================
# 1. PROJECT PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "college_info.txt"
)


# ==================================================
# 2. LOAD UNIVERSITY INFORMATION
# ==================================================

def load_college_data():
    """Load extracted university information."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            "College information file not found! "
            "Run pdf_processor.py first."
        )

    return DATA_PATH.read_text(encoding="utf-8")


# ==================================================
# 3. SPLIT INFORMATION INTO PDF PAGES
# ==================================================

def split_into_pages(text):
    """Separate extracted text into individual PDF pages."""

    pattern = r"--- Page (\d+) ---"
    matches = list(re.finditer(pattern, text))

    pages = []

    for i, match in enumerate(matches):

        page_number = int(match.group(1))
        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        page_text = text[start:end].strip()

        pages.append((page_number, page_text))

    return pages


# ==================================================
# 4. IDENTIFY QUESTION CATEGORY
# ==================================================

def identify_question_category(question):

    question = question.lower()

    # Scholarship
    if any(word in question for word in [
        "scholarship",
        "scholarships",
        "financial aid",
        "financial support",
        "fee concession",
        "earn and learn"
    ]):
        return "scholarship"

    # Eligibility
    if any(word in question for word in [
        "eligibility",
        "eligible",
        "qualification",
        "qualifying criteria",
        "admission criteria"
    ]):
        return "eligibility"

    # Intake
    if any(word in question for word in [
        "intake",
        "seat",
        "seats",
        "capacity"
    ]):
        return "intake"

    # Hostel
    if any(word in question for word in [
        "hostel",
        "accommodation",
        "dormitory"
    ]):

        if any(word in question for word in [
            "fee",
            "fees",
            "cost",
            "charges",
            "price"
        ]):
            return "hostel_fee"

        return "hostel"

    # Programme fees
    if any(word in question for word in [
        "fee",
        "fees",
        "tuition",
        "cost",
        "payment"
    ]):
        return "fee"

    return "general"


# ==================================================
# 5. IDENTIFY PROGRAMME
# ==================================================

def identify_programme(question):

    question = question.lower()

    programmes = {
        "cse": [
            "cse",
            "computer science",
            "computer science and engineering"
        ],

        "food_technology": [
            "food technology"
        ],

        "mechanical": [
            "mechanical engineering"
        ],

        "marine": [
            "marine engineering"
        ],

        "electrical": [
            "electrical engineering"
        ],

        "civil": [
            "civil engineering"
        ],

        "electronics": [
            "electronics engineering",
            "electronics and communication"
        ]
    }

    for programme, keywords in programmes.items():

        if any(keyword in question for keyword in keywords):
            return programme

    return None


# ==================================================
# 6. SEARCH RELEVANT UNIVERSITY INFORMATION
# ==================================================

def search_college_info(question, pages, top_k=3):

    question_lower = question.lower()

    category = identify_question_category(question)

    programme = identify_programme(question)

    stop_words = {
        "what", "is", "the", "for", "of", "in",
        "a", "an", "are", "and", "to", "with",
        "at", "does", "do", "can", "i", "me",
        "tell", "about", "please", "give", "show",
        "university", "college", "which", "how"
    }

    question_words = set(
        re.findall(r"\w+", question_lower)
    )

    question_words = {
        word for word in question_words
        if word not in stop_words and len(word) > 1
    }

    results = []

    # ------------------------------------------------
    # PRIORITY PAGE SELECTION
    # ------------------------------------------------

    priority_pages = []

    if category == "fee" and programme == "cse":
        priority_pages = [91]

    elif category == "eligibility":

        if programme == "cse":
            priority_pages = [37, 38]

        elif programme == "food_technology":
            priority_pages = [45]

        elif programme == "mechanical":
            priority_pages = [21, 22, 23, 24, 25, 26]

        elif programme == "marine":
            priority_pages = [21, 22, 23, 24, 25, 26]

        elif programme is None:
            # General B.Tech question requires clarification.
            return []

    elif category == "intake" and programme == "cse":
        priority_pages = [13]

    elif category == "hostel":
        priority_pages = [119]

    elif category == "hostel_fee":
        priority_pages = [120, 123]

    elif category == "scholarship":
        priority_pages = [126, 127, 128, 129]

    # ------------------------------------------------
    # SCORE PDF PAGES
    # ------------------------------------------------

    for page_number, page in pages:

        page_lower = page.lower()

        page_words = set(
            re.findall(r"\w+", page_lower)
        )

        score = len(
            question_words.intersection(page_words)
        )

        # Priority pages
        if page_number in priority_pages:
            score += 1000

        # --------------------------------------------
        # FEE
        # --------------------------------------------

        if category == "fee" and programme == "cse":

            if page_number == 91:
                if "school of computing" in page_lower:
                    score += 100

                if "computer science" in page_lower:
                    score += 100

        # --------------------------------------------
        # ELIGIBILITY
        # --------------------------------------------

        elif category == "eligibility":

            if programme == "cse" and page_number in [37, 38]:

                if "school of computing" in page_lower:
                    score += 100

                if "minimum eligibility criteria" in page_lower:
                    score += 50

            elif programme == "food_technology" and page_number == 45:

                if "food technology" in page_lower:
                    score += 100

            elif programme in ["mechanical", "marine"]:

                if "bachelor of technology" in page_lower:
                    score += 30

        # --------------------------------------------
        # INTAKE
        # --------------------------------------------

        elif category == "intake" and programme == "cse":

            if page_number == 13:

                if "school of computing" in page_lower:
                    score += 100

                if "2175" in page_lower:
                    score += 50

        # --------------------------------------------
        # HOSTEL FACILITIES
        # --------------------------------------------

        elif category == "hostel":

            if page_number == 119:

                if "security" in page_lower:
                    score += 10

                if "recreational" in page_lower:
                    score += 10

        # --------------------------------------------
        # HOSTEL FEES
        # --------------------------------------------

        elif category == "hostel_fee":

            if page_number in [120, 123]:

                if "hostel fee" in page_lower:
                    score += 50

                if "annual charges" in page_lower:
                    score += 30

        # --------------------------------------------
        # SCHOLARSHIPS
        # --------------------------------------------

        elif category == "scholarship":

            if page_number == 126:

                if "various scholarships" in page_lower:
                    score += 100

                if "merit scholarships" in page_lower:
                    score += 50

            elif page_number in [127, 128]:

                if "economically weaker section" in page_lower:
                    score += 50

            elif page_number == 129:

                if "education loan" in page_lower:
                    score += 50

        if score > 0:
            results.append(
                (score, page_number, page)
            )

    # ------------------------------------------------
    # SORT RESULTS
    # ------------------------------------------------

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    # Return all scholarship pages together
    if category == "scholarship":

        selected = [
            result for result in results
            if result[1] in priority_pages
        ]

        return selected

    return results[:top_k]


# ==================================================
# 7. PREPARE CONTEXT FOR GEMINI
# ==================================================

def get_relevant_context(question, pages, top_k=3):

    category = identify_question_category(question)

    programme = identify_programme(question)

    # Ask for clarification for general B.Tech eligibility
    if category == "eligibility" and programme is None:

        return (
            "The student asked for general B.Tech eligibility "
            "without specifying the programme. "
            "Ask which B.Tech specialization they mean. "
            "Do not provide combined or assumed eligibility criteria."
        )

    results = search_college_info(
        question,
        pages,
        top_k
    )

    if not results:

        return (
            "No relevant information found "
            "in the university handbook."
        )

    context_parts = []

    for score, page_number, page in results:

        context_parts.append(
            f"--- PDF Page {page_number} ---\n{page}"
        )

    return "\n\n".join(context_parts)


# ==================================================
# 8. MAIN PROGRAM - RETRIEVAL TESTING
# ==================================================

if __name__ == "__main__":

    college_text = load_college_data()

    pages = split_into_pages(college_text)

    print("University knowledge base loaded!")
    print("Total PDF pages:", len(pages))

    while True:

        question = input("\nEnter your question: ")

        if question.lower() in ["exit", "quit"]:
            print("Search completed.")
            break

        category = identify_question_category(question)
        programme = identify_programme(question)

        print("\nQuestion category:", category)
        print("Identified programme:", programme)

        context = get_relevant_context(
            question,
            pages,
            top_k=3
        )

        print("\nRetrieved Context:\n")
        print(context)

        print("\nRetrieval testing completed!")
