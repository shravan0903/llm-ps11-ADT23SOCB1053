
import time
import streamlit as st

from utils.retriever import (
    load_college_data,
    split_into_pages,
    get_relevant_context
)

from utils.gemini_client import generate_response_stream


# =====================================================
# LOAD UNIVERSITY KNOWLEDGE BASE
# =====================================================

@st.cache_resource
def load_knowledge_base():
    college_text = load_college_data()
    return split_into_pages(college_text)


pages = load_knowledge_base()


# =====================================================
# COURSE IDENTIFICATION
# =====================================================

def find_course_reference(question, conversation_history):

    course_names = {
        "computer science & engineering": "Computer Science & Engineering",
        "computer science and engineering": "Computer Science & Engineering",
        "computer science": "Computer Science & Engineering",
        "cse": "Computer Science & Engineering",
        "food technology": "Food Technology",
        "mechanical engineering": "Mechanical Engineering",
        "marine engineering": "Marine Engineering",
        "electrical engineering": "Electrical Engineering",
        "civil engineering": "Civil Engineering",
        "electronics engineering": "Electronics Engineering",
        "electronics and communication": "Electronics and Communication Engineering"
    }

    question_lower = question.lower()

    for keyword, course in course_names.items():
        if keyword in question_lower:
            return course

    for message in reversed(conversation_history):

        if message.get("role") == "user":

            previous_question = message.get("content", "").lower()

            for keyword, course in course_names.items():
                if keyword in previous_question:
                    return course

    return None


# =====================================================
# SCHOLARSHIP INFORMATION
# =====================================================

def get_scholarship_answer(question):

    q = question.lower()

    scholarship_keywords = [
        "scholarship",
        "scholarships",
        "financial aid",
        "financial support",
        "fee concession",
        "fee waiver",
        "earn and learn",
        "merit scholarship",
        "education loan",
        "pm vidyalaxmi",
        "e-kalyan"
    ]

    if not any(word in q for word in scholarship_keywords):
        return None

    return """
### Scholarships and Financial Assistance at MIT ADT University

According to the Admission Handbook 2026–27 (PDF Pages 126–129):

**1. University-Funded Merit Scholarships**
- Merit Excellence
- Merit Achiever
- Merit Performer
- Merit-Based Support
- Tuition fee waivers from 3% to 20%, depending on admission merit
  or academic performance and applicable scholarship rules.

**2. Need-Based Tuition Support**
- Generally provides tuition fee concessions up to 10%.
- Higher support may be considered in exceptional verified cases,
  subject to approval.

**3. Achievement-Based Tuition Credit**
- Fixed 10% tuition fee waiver for eligible verified achievements.
- Includes national or international innovation competitions
  such as Smart India Hackathon.
- Also covers recognized State, National and Inter-University sports.

**4. Government Scholarships**
- Eligible students can apply through the National Scholarship Portal,
  according to applicable government guidelines.

**5. Programme-Specific Scholarships**
- Marine Engineering: entry-level merit and gender-based support.
- Bioengineering: merit-linked tuition discounts.
- Design: need-cum-merit scholarships.
- Ph.D.: tuition fee concessions through the Research and Development Cell.

**6. Earn and Learn Scheme**
- Provides part-time, non-hazardous work opportunities within
  the university.
- Remuneration is provided according to university norms.

**7. Staff Ward / Spouse Fee Concession**
- Available to eligible wards and spouses of MAEER's MIT Group
  employees, subject to prescribed conditions.

### EWS Scholarship / Fee Concession

According to PDF Pages 127–128:

- 50% concession / scholarship in total fees.
- Available to 10% of students, selected according to merit
  and EWS eligibility.
- Maharashtra students with annual family income below ₹8 lakh
  may be eligible, subject to applicable requirements.
- Income and EWS documents must be verified.

### Education Loan and State Schemes

According to PDF Page 129:

- PM Vidyalaxmi: education loan facility through participating banks.
- Bihar Student Credit Card: for Bihar-domiciled students.
- Jharkhand E-Kalyan: post-matric scholarship for eligible
  SC/ST/Backward Class students domiciled in Jharkhand.

**Important:** Scholarship policies and eligibility conditions
are subject to university and government rules.

Source: MIT ADT Admission Handbook 2026–27, PDF Pages 126–129.
"""


# =====================================================
# HOSTEL INFORMATION
# =====================================================

def get_hostel_answer(question):

    q = question.lower()

    hostel_keywords = [
        "hostel",
        "hostels",
        "accommodation",
        "hostel room"
    ]

    if not any(word in q for word in hostel_keywords):
        return None

    # HOSTEL FEES
    if any(word in q for word in [
        "fee", "fees", "cost", "charges", "price",
        "single occupancy", "double occupancy"
    ]):

        return """
### MIT ADT University – Hostel Fee Structure

According to the Admission Handbook 2026–27:

**1. Institute of Design Hostels**
(PDF Page 120)

| Fee Head | Annual Charges |
|---|---:|
| Hostel | ₹1,03,000 |
| Mess | ₹98,000 |
| Laundry | ₹13,500 |
| **Total** | **₹2,14,500** |

**2. Non-Design Hostels**
(PDF Page 123)

| Hostel Category | Annual Charges |
|---|---:|
| Boys and Girls – All hostels | ₹1,75,000 |
| Vishwashanti Sangeet Kala Academy | ₹1,07,500 |
| Single Occupancy | ₹2,60,000 |
| Double Occupancy | ₹2,10,000 |

**Important:**
- Fees cover 10 months of the academic year.
- Additional monthly charges apply for stays beyond 10 months.
- Hostel fees are subject to annual review.
- These fee structures apply to different hostel categories.

Source: Admission Handbook 2026–27, PDF Pages 120 and 123.
"""

    # HOSTEL FACILITIES
    if any(word in q for word in [
        "facilities", "facility", "available",
        "amenities", "features", "provide"
    ]):

        return """
### MIT ADT University – Hostel Facilities

According to the Admission Handbook 2026–27 (PDF Page 119),
the university hostel provides:

1. Recreational rooms.
2. Mess and transportation facilities.
3. 24-hour security and attendants.
4. Centralized solar water systems and electric geysers.
5. Water dispensers and RO water coolers.
6. Indoor games such as carrom, chess and table tennis.
7. Wi-Fi facilities.
8. Well-furnished rooms.
9. Uninterrupted power supply.
10. Laundry services.
11. Parking facilities.
12. Sanitary pad vending machines in the girls' hostel.

**Safety and Security:**
- CCTV cameras monitor hostel premises and main corridors.
- Students must carry their university identity cards.

Source: Admission Handbook 2026–27, PDF Page 119.
"""

    return None


# =====================================================
# REQUIRED DOCUMENTS
# =====================================================

def get_documents_answer(question):

    q = question.lower()

    document_keywords = [
        "document",
        "documents",
        "required documents",
        "certificate",
        "certificates",
        "paperwork",
        "what should i submit",
        "what do i need to submit"
    ]

    if not any(word in q for word in document_keywords):
        return None

    # DIRECT SECOND YEAR AFTER DIPLOMA
    if "diploma" in q and any(word in q for word in [
        "direct second year", "second year", "documents"
    ]):

        return """
### Documents Required – Direct Second Year After Diploma

According to the MIT ADT Admission Handbook 2026–27
(PDF Pages 79–80):

1. 10th or equivalent mark sheet / passing certificate.
2. Diploma final-year mark sheet and provisional passing certificate.
3. Leaving / Transfer Certificate.
4. Migration Certificate for candidates other than Maharashtra State.
5. Equivalence Certificate from MSBTE, Mumbai, for diplomas completed
   outside Maharashtra State Board of Technical Education.
6. Birth / Domicile / Nationality Certificate.
7. Caste Certificate, if applicable.
8. Non-Creamy Layer Certificate, if applicable.
9. Gap Certificate, if the gap is at least one year.
10. Photocopy of Aadhaar card.

Source: Admission Handbook 2026–27, PDF Pages 79–80.
"""

    # POSTGRADUATE DOCUMENTS
    if any(word in q for word in [
        "postgraduate", "post graduate", "pg",
        "masters", "master's"
    ]):

        return """
### Documents Required – Postgraduate Programme

According to the MIT ADT Admission Handbook 2026–27
(PDF Pages 80–81):

1. Final-year undergraduate mark sheet and passing certificate.
2. Leaving / Transfer Certificate.
3. Migration Certificate, where applicable.
4. Birth / Domicile / Nationality Certificate.
5. Caste Certificate, if applicable.
6. Caste Validity Certificate, if applicable.
7. Non-Creamy Layer Certificate, if applicable.
8. Gap / Work Experience Certificate, if the gap is at least one year.
9. Valid entrance exam scorecard for professional programmes.
10. Photocopy of Aadhaar card.

Note:
- If the Migration Certificate mentions the Leaving Certificate,
  a separate Leaving Certificate is not required.
- If the previous institution does not issue a Migration Certificate,
  its letter confirming this may be accepted.

Source: Admission Handbook 2026–27, PDF Pages 80–81.
"""

    # UNDERGRADUATE FIRST YEAR DOCUMENTS
    if any(word in q for word in [
        "undergraduate", "ug", "first year",
        "12th", "10+2", "btech"
    ]):

        return """
### Documents Required – Undergraduate First Year

According to the MIT ADT Admission Handbook 2026–27
(PDF Page 79):

1. 10th or equivalent mark sheet / passing certificate.
2. 10+2 or equivalent mark sheet / passing certificate.
3. Leaving / Transfer Certificate.
4. Migration Certificate for candidates other than Maharashtra State Board.
5. Birth / Domicile / Nationality Certificate.
6. Caste Certificate, if applicable.
7. Caste Validity Certificate, if applicable.
8. Non-Creamy Layer Certificate, if applicable.
9. Gap Certificate, if the gap is at least one year.
10. Valid entrance exam scorecard for professional programmes.
11. Passport is mandatory for B.Tech Marine Engineering and
    B.Sc Nautical Science.
12. Photocopy of Aadhaar card.

Note:
The Leaving Certificate may be accepted as nationality, birth or
domicile proof if it mentions nationality and place of birth.

Source: Admission Handbook 2026–27, PDF Page 79.
"""

    # DIRECT SECOND YEAR FROM ANOTHER INSTITUTE
    if any(word in q for word in [
        "another university",
        "another institute",
        "transfer admission",
        "direct second year from"
    ]):

        return """
### Documents Required – Direct Second Year from Another Institute

According to the MIT ADT Admission Handbook 2026–27
(PDF Page 80):

1. First-year marksheets (First and Second Semester).
2. Leaving / Transfer Certificate.
3. Migration Certificate.
4. No Objection Certificate from the concerned Institute / University.
5. Equivalence Certificate from DUGC of MIT-ADT University.
6. Nationality / Domicile / Birth Certificate.
7. Caste Certificate, if applicable.
8. Caste Validity Certificate, if applicable.
9. Non-Creamy Layer Certificate, if applicable.
10. Gap Certificate, if the gap is at least one year.
11. Photocopy of Aadhaar card.

Source: Admission Handbook 2026–27, PDF Page 80.
"""

    return """
The required documents depend on your programme level and admission category.

Please specify which category applies to you:

1. Undergraduate – First Year
2. Direct Second Year after Diploma
3. Direct Second Year from another Institute / University
4. Postgraduate
5. NRI / OCI / PIO category

Source: MIT ADT Admission Handbook 2026–27, PDF Pages 79–82.
"""


# =====================================================
# ADMISSION GUIDANCE
# =====================================================

def get_admission_answer(question):

    q = question.lower()

    admission_keywords = [
        "admission process",
        "admission procedure",
        "how to apply",
        "how can i apply",
        "application process",
        "apply for admission",
        "admission steps",
        "online admission",
        "admission guidelines",
        "how to get admission",
        "how do i get admission"
    ]

    if not any(word in q for word in admission_keywords):
        return None

    # LATERAL ENTRY
    if any(word in q for word in [
        "lateral entry",
        "direct second year",
        "second year admission"
    ]):

        return """
### Direct Second Year / Lateral Entry Admission

According to the MIT ADT Admission Handbook 2026–27
(PDF Pages 22–23):

- Lateral entry to the second year of undergraduate degree
  programmes is permitted.
- It can be up to a maximum of 10% of the approved intake,
  over and above the approved intake.
- Unfilled first-year seats and vacancies arising from withdrawals
  may also be considered.
- Candidates must meet the eligibility criteria for their programme.

**Important:** Contact the relevant school for programme-specific
eligibility and current seat availability.

Source: Admission Handbook 2026–27, PDF Pages 22–23.
"""

    # EWS ADMISSION
    if "ews" in q:

        return """
### EWS Admission Guidelines

According to the MIT ADT Admission Handbook 2026–27
(PDF Page 21):

- 10% seats are reserved for EWS candidates.
- These seats are over and above the sanctioned intake
  for the respective course.
- Admission is based on qualifying examination marks or grades,
  eligibility and seat availability.
- EWS vacant seats may be considered for lateral entry
  to the second year under the applicable reservation policy.

The handbook also mentions a 50% programme-fee concession /
scholarship for 10% of admitted EWS students, based on merit
and applicable rules.

Source: Admission Handbook 2026–27, PDF Page 21.
"""

    # INTERNATIONAL ADMISSION
    if any(word in q for word in [
        "international student",
        "foreign student",
        "foreign national",
        "nri",
        "oci",
        "pio",
        "ciwgc",
        "ciwsea"
    ]):

        return """
### International / NRI / OCI Admission

According to the MIT ADT Admission Handbook 2026–27
(PDF Pages 21–23):

The handbook describes these admission categories:

1. Foreign Nationals (FN): Citizens of countries other than India
   holding a foreign passport.
2. CIWGC / CIWSEA: Children of Indians working in Gulf countries
   and Southeast Asian countries.
3. OCI: Applicants holding an Overseas Citizenship of India card.
4. NRI: Applicants eligible under the handbook's NRI definition.

**Documents may include:**
- Academic mark sheets and certificates.
- Leaving / Transfer Certificate.
- Migration Certificate.
- Birth Certificate.
- Passport copies of student and parent.
- OCI / PIO card, where applicable.
- Parent's work permit and employer certificate,
  where applicable.
- Sponsorship letter, where applicable.
- NRI certificate, where applicable.
- Visa / residence permit copies of parents.

Additional documents depend on the admission category.

Source: Admission Handbook 2026–27, PDF Pages 21–23.
"""

    # GENERAL ADMISSION PROCEDURE
    return """
### MIT ADT University – Admission Guidance 2026–27

According to the Admission Handbook 2026–27:

**1. Visit the official website**

Apply online at:
https://www.mituniversity.ac.in

**2. Select your programme**

Choose the undergraduate, postgraduate or other programme
you wish to apply for.

**3. Check eligibility**

- UG applicants must have passed 10+2 or equivalent
  from a recognized institution.
- PG applicants must hold a bachelor's degree or equivalent
  from a recognized university.
- Programme-specific eligibility requirements must also be checked.

**4. Understand the selection basis**

Admission is based on:
- Marks or grades obtained in the qualifying examination.
- Programme eligibility criteria.
- Availability of seats.

The handbook states that admissions are on a first-come,
first-served basis.

**5. Check required documents**

Prepare the documents applicable to your programme and category.

**Important:**
The handbook does not provide a complete click-by-click
application or payment procedure. Check the official website
or contact the relevant school admission coordinator for
current application instructions.

Source: Admission Handbook 2026–27, PDF Pages 8 and 21–24.
"""


# =====================================================
# LOCAL FAQ FALLBACK
# =====================================================

def get_local_fallback_answer(question, course_reference):

    q = question.lower()

    # SCHOLARSHIP
    scholarship_answer = get_scholarship_answer(question)

    if scholarship_answer:
        return scholarship_answer

    # HOSTEL
    hostel_answer = get_hostel_answer(question)

    if hostel_answer:
        return hostel_answer

    # REQUIRED DOCUMENTS
    documents_answer = get_documents_answer(question)

    if documents_answer:
        return documents_answer

    # ADMISSION GUIDANCE
    admission_answer = get_admission_answer(question)

    if admission_answer:
        return admission_answer

    # CSE-SPECIFIC ANSWERS
    if course_reference != "Computer Science & Engineering":
        return None

    # CSE ELIGIBILITY
    if any(word in q for word in [
        "eligibility", "eligible", "qualification"
    ]):

        return """
### B.Tech Computer Science & Engineering – Eligibility

According to the MIT ADT Admission Handbook 2026–27:

**Option 1: 10+2 Qualification**
- Passed 10+2 or equivalent from a recognized board.
- Minimum 45% marks for General / Open category.
- Physics and Mathematics are mandatory.
- One additional subject must be selected from the subjects
  listed in Table A of the handbook.

**Option 2: Diploma Qualification**
- Passed a minimum three-year Diploma from a recognized board.
- Minimum 45% marks for General / Open category.

**Relaxation:** 5% relaxation in minimum qualifying marks applies
to Reserved Categories, EWS and PwD candidates from Maharashtra.

**Entrance Exams:** MHT-CET / JEE / PERA CET 2026.

Source: Admission Handbook 2026–27, PDF Pages 37–38.
"""

    # CSE FEES
    if any(word in q for word in [
        "fee", "fees", "cost", "tuition"
    ]):

        return """
### B.Tech Computer Science & Engineering – Fee Structure

According to the MIT ADT Admission Handbook 2026–27:

| Academic Year | Indian Resident |
|---|---:|
| 2026–27 | ₹2,87,000 |
| 2027–28 | ₹3,15,000 |
| 2028–29 | ₹3,35,000 |
| 2029–30 | ₹3,35,000 |
| **Total** | **₹12,72,000** |

**Other categories:**
- EWS: ₹7,32,500 total.
- NRI / PIO / OCI / CIWGC / CIWSE A / FN: ₹19,08,000 total.

Source: Admission Handbook 2026–27, PDF Page 91.

Note: Fees are subject to university rules and revision.
"""

    # CSE INTAKE
    if any(word in q for word in [
        "intake", "capacity", "seats"
    ]):

        return """
### B.Tech Computer Science & Engineering – Intake

According to the MIT ADT Admission Handbook 2026–27:

- Approved intake: 1,740
- EWS: 174
- NRI / PIO / OCI / CIWSEA / FN: 261
- **Total intake capacity: 2,175**

Source: Admission Handbook 2026–27, PDF Page 13.
"""

    return None


# =====================================================
# MAIN CHATBOT FUNCTION
# =====================================================

def ask_college_chatbot(question, conversation_history=None):

    if conversation_history is None:
        conversation_history = []

    start_time = time.perf_counter()

    course_reference = find_course_reference(
        question,
        conversation_history
    )

    # Try local answers first
    local_answer = get_local_fallback_answer(
        question,
        course_reference
    )

    if local_answer:
        return iter([local_answer]), 0.0

    # Retrieve handbook information for other questions
    retrieval_question = question

    if course_reference:
        retrieval_question += f" Course: {course_reference}"

    context = get_relevant_context(
        retrieval_question,
        pages,
        top_k=2
    )

    retrieval_time = time.perf_counter() - start_time

    if not context or context.startswith(
        "No relevant information found"
    ):

        return iter([
            "I could not find relevant information in the university handbook. "
            "Please try asking your question in a different way."
        ]), retrieval_time

    # Recent conversation history
    recent_messages = conversation_history[-4:]

    history_text = ""

    for message in recent_messages:

        role = message.get("role", "").upper()
        content = message.get("content", "")

        history_text += f"\n{role}: {content}\n"

    # Gemini prompt
    prompt = f"""
You are a helpful college enquiry assistant for
MIT Art, Design and Technology University, Pune.

Answer the student's latest question using ONLY
the university information provided below.

CONVERSATION HISTORY:
{history_text}

CURRENT QUESTION:
{question}

IDENTIFIED COURSE:
{course_reference if course_reference else "Not identified"}

UNIVERSITY INFORMATION:
{context}

INSTRUCTIONS:
1. Give simple, clear and accurate answers.
2. Do not invent facts, figures, fees or eligibility criteria.
3. If information is missing, clearly say so.
4. Mention handbook PDF page numbers whenever possible.
5. Understand follow-up questions using conversation history.
6. Answer only the latest question.
7. Never combine eligibility criteria from different programmes.
8. Do not assume that all programmes have the same entrance exam.
9. If a programme is not identified, ask the student to specify it
   when programme-specific information is needed.
10. Do not claim that an admission process or deadline is confirmed
    unless it is present in the supplied information.

ANSWER:
"""

    response_stream = generate_response_stream(prompt)

    return response_stream, retrieval_time
