import streamlit as st
import pytesseract
import pandas as pd
import cv2
import re
import tempfile
from PIL import Image
from datetime import datetime
import numpy as np

# --- Page Config (must be first Streamlit call) ---
st.set_page_config(page_title="Loan Document OCR", layout="wide")

# --- Apply Custom CSS ---
def apply_custom_css():
    st.markdown("""
        <style>
        /* Make all buttons green */
        div.stButton > button {
            background-color: #28a745 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            border: none;
        }

        div.stButton > button:hover {
            background-color: #218838 !important;
            color: white !important;
            transition: background-color 0.3s ease;
        }

        /* File uploader area */
        section[data-testid="stFileUploader"] > div {
            border: 2px dashed #28a745 !important;
            border-radius: 10px;
            background-color: #f0fff4 !important;
            padding: 1rem;
        }

        section[data-testid="stFileUploader"] > div:hover {
            border-color: #218838 !important;
        }

        /* Padding for the app */
        .block-container {
            padding: 2rem 2rem 3rem 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

def normalize_text(text):
    text = text.replace(' @', '@').replace('@ ', '@')  # Fix space near @
    text = re.sub(r'\s+com', '.com', text)  # Fix "example com" -> "example.com"
    text = text.replace(' dot ', '.').replace(' DOT ', '.')
    return text


# --- Preprocessing Function ---
def preprocess_image(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    image = cv2.imread(tmp_path)
    if image is None:
        st.error("Failed to load image.")
        return None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(thresh)

# --- OCR Function ---
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# --- Field Extraction Function ---
def extract_fields(text):
    fields = {
        "full_name": re.search(r"Name[:\-]?\s*(.+)", text, re.IGNORECASE),
        "dob": re.search(r"Date of Birth[:\-]?\s*(\d{2}[\/\-]\d{2}[\/\-]\d{4})", text, re.IGNORECASE),
        "gender": re.search(r"Gender[:\-]?\s*(Male|Female|Other)", text, re.IGNORECASE),
        "pan_number": re.search(r"PAN[:\-]?\s*([A-Z]{5}\d{4}[A-Z])", text, re.IGNORECASE),
        "aadhaar_number": re.search(r"Aadhaar?\s*(\d{4}\s\d{4}\s\d{4})", text, re.IGNORECASE),
        "mobile_number": re.search(r"Mobile[:\-]?\s*(\d{10})", text, re.IGNORECASE),
        "email": re.search(r"Email[:\-]?\s*([\w\.-]+@[\w\.-]+)", text, re.IGNORECASE),
        "address": re.search(r"Address[:\-]?\s*(.+)", text, re.IGNORECASE),
        "employment_type": re.search(r"Employment Type[:\-]?\s*(Salaried|Self-Employed|Business)", text, re.IGNORECASE),
        "monthly_income": re.search(r"Income[:\-]?\s*₹?([\d,]+)", text, re.IGNORECASE),
        "organization": re.search(r"Employer[:\-]?\s*(.+)", text, re.IGNORECASE),
        "loan_amount": re.search(r"Loan Amount[:\-]?\s*₹?([\d,]+)", text, re.IGNORECASE),
        "loan_tenure": re.search(r"Tenure[:\-]?\s*(\d+)\s*(months|years)?", text, re.IGNORECASE),
    }
    return {k: (v.group(1).strip() if v else "") for k, v in fields.items()}

# --- Validation Function ---
def validate_fields(fields):
    required = ["full_name", "dob", "mobile_number", "pan_number", "monthly_income", "loan_amount"]
    errors = []
    for field in required:
        if not fields[field]:
            errors.append(f"Missing or invalid value for: {field.replace('_', ' ').title()}")
    return errors

# --- Save to CSV Function ---
def save_to_csv(data, filename="loan_applications.csv"):
    data["submitted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = pd.DataFrame([data])
    try:
        existing = pd.read_csv(filename)
        combined = pd.concat([existing, new_entry], ignore_index=True)
    except FileNotFoundError:
        combined = new_entry
    combined.to_csv(filename, index=False)

# --- Page 1: Upload and Validate ---
def page_upload():
    st.title("🏦 Automated Personal Loan Document Processing")
    st.markdown("""
<div style='
    background-color: #e6f4ea;
    padding: 1.2rem;
    border-left: 6px solid #28a745;
    border-radius: 8px;
    margin-bottom: 1.5rem;
'>
    <h4 style='color: #1a3c2e; margin-top: 0;'>📌 <u>Project Objective</u></h4>
    <p style='color: #333; font-size: 16px; line-height: 1.6;'>
        Develop an OCR-based solution to automatically extract and process information from personal loan application documents.
        The system should identify key fields such as applicant name, address, income details, and loan amount. 
        Additionally, the solution should validate the extracted data and integrate with the bank's loan processing system.
    </p>
</div>
""", unsafe_allow_html=True)

    
    uploaded_file = st.file_uploader("Upload Loan Application Form to extract and validate applicant data automatically. (Image Only)", type=["png", "jpg", "jpeg"])

    if uploaded_file and st.button("🔍 Extract Data"):
        preprocessed_img = preprocess_image(uploaded_file)
        if preprocessed_img:
            text = extract_text_from_image(preprocessed_img)
            text = normalize_text(text)
            fields = extract_fields(text)
            errors = validate_fields(fields)

            st.session_state["extracted_text"] = text
            st.session_state["extracted_data"] = fields

            if errors:
                st.warning("⚠️ Please correct the following issues:")
                for error in errors:
                    st.write(f"- {error}")
                st.text_area("Extracted Text", st.session_state.get("extracted_text", ""), height=300)
            else:
                st.session_state["page"] = "ocr_review"
                st.rerun()

# --- Page 2: Review OCR Output ---
def page_ocr_review():
    st.markdown("### 🔍 OCR Output (Raw Text)")
    st.success("✅ All required fields were extracted successfully!")
    st.text_area("Extracted Text", st.session_state.get("extracted_text", ""), height=300)
    if st.button("➡️ Next"):
        st.session_state["page"] = "review_and_edit"
        st.rerun()

# --- Page 3: Review & Edit ---
def page_review_and_edit():
    st.markdown("""
    <style>
        .stTextInput label {
            font-weight: 600 !important;
            font-size: 13px !important;
            margin-bottom: 0px !important;
        }
        .stTextInput>div>div {
            margin-bottom: 8px !important; /* Reduce spacing between input fields */
        }
        .stTextInput>div>div>input {
            padding: 6px 10px !important;
            font-size: 13px !important;
        }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        .element-container:has(.stTextInput) {
            margin-bottom: 4px !important; /* Reduce gap between input components */
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Review & Edit Extracted Information")

    fields = st.session_state.get("extracted_data", {})
    corrected_fields = {}

    col1, col2 = st.columns(2)

    for i, (key, value) in enumerate(fields.items()):
        label = key.replace("_", " ").title()

        if i % 2 == 0:
            with col1:
                corrected_fields[key] = st.text_input(label, value=value, key=key)
        else:
            with col2:
                corrected_fields[key] = st.text_input(label, value=value, key=key)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✅ Submit Final Data"):
        save_to_csv(corrected_fields)
        st.session_state["page"] = "success"
        st.rerun()



# --- Page 4: Success ---
def page_success():
    st.write(".")
    st.success("🎉 Application data saved successfully!")
    if st.button("🔄 Go back to Home"):
        st.session_state.clear()
        st.session_state["page"] = "upload"
        st.rerun()

# --- Main ---
def main():
    apply_custom_css()
    if "page" not in st.session_state:
        st.session_state["page"] = "upload"

    if st.session_state["page"] == "upload":
        page_upload()
    elif st.session_state["page"] == "ocr_review":
        page_ocr_review()
    elif st.session_state["page"] == "review_and_edit":
        page_review_and_edit()
    elif st.session_state["page"] == "success":
        page_success()

if __name__ == "__main__":
    main()
