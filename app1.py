import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re
from fpdf import FPDF

load_dotenv()  # load all our environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    print(f"Response text: {response.text}")  # Add this line
    return response.text

def clean_json_string(json_string):
    # Remove any trailing commas
    json_string = re.sub(r',\s*}', '}', json_string)

    # Remove any leading/trailing whitespace characters
    json_string = json_string.strip()

    return json_string

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """ Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding of tech field,software engineering,data science ,data analyst and big data engineer. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide best assistance for improving the resumes. Assign the percentage Matching based on JD and the missing keywords with high accuracy resume:{text} description:{jd} I want the response in one single string having the structure {{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}} """

def review_resume(response_dict):
    jd_match = float(response_dict["JD Match"].strip("%"))
    missing_keywords = response_dict["MissingKeywords"]
    profile_summary = response_dict["Profile Summary"]

    if jd_match >= 80:
        review = f"This resume is a strong match for the job description with a {jd_match}% match score."
    elif jd_match >= 60:
        review = f"This resume is a decent match for the job description with a {jd_match}% match score."
    else:
        review = f"This resume is a weak match for the job description with a {jd_match}% match score."

    if missing_keywords:
        review += f"\nMissing keywords: {', '.join(missing_keywords)}"

    review += f"\n\nProfile Summary: {profile_summary}"

    return review

def extract_details_from_resume(resume_text):
    name_pattern = r"(?:Name|CANDIDATE NAME)[\s:]*(.+?)\n"
    email_pattern = r"(?:Email|E-mail|EMAIL)[\s:]*(.+?)\n"
    phone_pattern = r"(?:Phone|PHONE|Mobile)[\s:]*(.+?)\n"

    name = None
    email = None
    phone = None

    name_match = re.search(name_pattern, resume_text, re.IGNORECASE)
    if name_match:
        name = name_match.group(1).strip()

    email_match = re.search(email_pattern, resume_text, re.IGNORECASE)
    if email_match:
        email = email_match.group(1).strip()

    phone_match = re.search(phone_pattern, resume_text, re.IGNORECASE)
    if phone_match:
        phone = phone_match.group(1).strip()

    return name, email, phone

def suggest_jobs(missing_keywords):
    suggested_jobs = []
    keywords_patterns = {
        "Software Engineer": r"(python|java|c\+\+|algorithms|data structures)",
        "Data Scientist": r"(python|machine learning|statistics|data analysis|sql)",
        "Web Developer": r"(html|css|javascript|react|angular)"
    }

    for job, pattern in keywords_patterns.items():
        for keyword in missing_keywords:
            if re.search(pattern, keyword, re.IGNORECASE):
                suggested_jobs.append(job)
                break

    if suggested_jobs:
        suggestions = f"Based on the missing keywords, you may want to consider applying for the following positions: {', '.join(suggested_jobs)}"
    else:
        suggestions = "No specific job suggestions based on the missing keywords."

    return suggestions

def generate_offer_letter(candidate_name, job_title, experience):
    salary_range = get_average_salary(job_title, experience)
    offer_letter = f"""
Dear {candidate_name},

We are pleased to offer you the position of {job_title} at [Company Name]. This offer is based on your qualifications, experience, and the positive impression you made during the interview process.

Position: {job_title}
Experience: {experience}
Annual Salary: {salary_range}

[Additional details about benefits, start date, etc.]

We are confident that your skills and expertise will be a valuable addition to our team, and we look forward to your contributions to our company's success. Please review the attached documents, which outline the terms and conditions of your employment.

This offer is contingent upon successful completion of background checks and verification of your employment eligibility.

Please indicate your acceptance of this offer by signing and returning a copy of the attached documents.

Sincerely,
[Company Name]
"""
    return offer_letter

def generate_pdf_offer_letter(candidate_name, job_title, experience):
    offer_letter_text = generate_offer_letter(candidate_name, job_title, experience)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=offer_letter_text)
    pdf_filename = f"{candidate_name}_offer_letter.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

def generate_offer_letter(candidate_name, job_title, jd):
    # Extract the role and experience from the job description
    role, experience = get_role_and_experience(jd)

    # Generate the offer letter text
    offer_letter_text = f"Dear {candidate_name},\n\nWe are pleased to offer you the position of {job_title} at our company. The role requires {experience} of experience in the field of {role}.\n\nPlease find the details of the offer in the attached document.\n\nBest regards,\n[Your Name]"

    # Generate the PDF offer letter
    pdf_filename = generate_pdf_offer_letter(candidate_name, job_title, offer_letter_text)

    return pdf_filename


def get_average_salary(role, experience):
    salary_data = {
        "Software Engineer": {
            "0-1 years": "₹ 4.0 Lakhs - ₹ 6.0 Lakhs",
            "1-3 years": "₹ 6.0 Lakhs - ₹ 9.0 Lakhs",
            "3-5 years": "₹ 9.0 Lakhs - ₹ 15.0 Lakhs"
        },
        "Data Scientist": {
            "0-1 years": "₹ 5.0 Lakhs - ₹ 8.0 Lakhs",
            "1-3 years": "₹ 8.0 Lakhs - ₹ 12.0 Lakhs",
            "3-5 years": "₹ 12.0 Lakhs - ₹ 20.0 Lakhs"
        },
        "Web Developer": {
            "0-1 years": "₹ 3.0 Lakhs - ₹ 5.0 Lakhs",
            "1-3 years": "₹ 5.0 Lakhs - ₹ 8.0 Lakhs",
            "3-5 years": "₹ 8.0 Lakhs - ₹ 12.0 Lakhs"
        }
    }

    if role in salary_data and experience in salary_data[role]:
        return salary_data[role][experience]
    else:
        return "Salary range not available"
def get_role_and_experience(jd):
    # Extract the role and experience from the job description
    # This is just a placeholder implementation, you may need to adjust it based on your specific requirements
    role = "Software Engineer"  # Replace with code to extract the role from the job description
    experience = "2-4 years"  # Replace with code to extract the experience from the job description
    return role, experience

role, experience = get_role_and_experience(jd)


def select_top_candidates(percentage_matches, jd, threshold=80):
    top_candidates = []
    rejected_candidates = []
    selected_candidates_list = []
    unselected_candidates_list = []

    for file_name, match_percentage in percentage_matches:
        text = input_pdf_text(uploaded_file)
        candidate_name, candidate_email, candidate_phone = extract_details_from_resume(text)
        role, experience = get_role_and_experience(jd)

        if match_percentage >= threshold:
            top_candidates.append((file_name, match_percentage))
            selected_candidates_list.append((candidate_name, candidate_email))
            job_title = "Software Engineer"  # Replace with the actual job title
            offer_letter_pdf = generate_pdf_offer_letter(candidate_name, job_title)
            st.success(f"Offer letter generated for {candidate_name}: {offer_letter_pdf}")
        else:
            rejected_candidates.append((file_name, match_percentage))
            unselected_candidates_list.append((candidate_name, candidate_email))

    if top_candidates:
        st.success("Congratulations to the following candidates for their outstanding resumes!")
        st.write("Selected Candidates:")
        st.table(selected_candidates_list)
    else:
        st.warning("No candidates met the selection threshold.")

    st.write("Unselected Candidates:")
    st.table(unselected_candidates_list)

    st.write(f"Total resumes selected: {len(top_candidates)}")
    st.write(f"Total resumes rejected: {len(rejected_candidates)}")
## Streamlit app
st.title("Resume buddy")
st.text("FInd your best Candidate here!!")
jd = st.text_area("Paste the Job Description")
uploaded_files = st.file_uploader("Upload Your Resumes", type="pdf", accept_multiple_files=True, help="Please upload the pdf resumes")
submit = st.button("Submit")

if submit:
    if uploaded_files is not None:
        percentage_matches = []
        for uploaded_file in uploaded_files:
            text = input_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt.format(text=text, jd=jd))
            cleaned_response = clean_json_string(response)  # Clean the JSON string
            try:
                response_dict = json.loads(cleaned_response)
                jd_match = float(response_dict["JD Match"].strip("%"))
                percentage_matches.append((uploaded_file.name, jd_match))

                resume_review = review_resume(response_dict)
                st.subheader(f"Resume Review for {uploaded_file.name}")
                st.write(resume_review)

                job_suggestions = suggest_jobs(response_dict["MissingKeywords"])
                st.write(job_suggestions)

            except (ValueError, KeyError) as e:
                st.subheader(f"Error processing {uploaded_file.name}: {e}")

        select_top_candidates(percentage_matches, jd)  # Pass 'jd' as the second argument
    else:
        st.subheader("No resumes uploaded.")