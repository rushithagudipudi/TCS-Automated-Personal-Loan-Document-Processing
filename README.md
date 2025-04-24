

# 📄 Personal Loan Application OCR Processor

A Streamlit web app that extracts key applicant details from scanned **loan application forms** using **OCR + image preprocessing** and stores them in a bank's loan processing system (structured CSV file).

---

## ⚙️ How It Works

1. **Upload Form** (JPG/PNG)  
2. **Preprocessing** with OpenCV (grayscale → denoise → threshold)  
3. **OCR Extraction** using Tesseract  
4. **Field Parsing** via Regex (Name, DOB, PAN, Aadhaar, Email, etc.)  
5. **Validation** – highlights missing/invalid fields  
6. **Review & Edit** – user can correct fields in-app  
7. **Save to CSV** – clean data stored with timestamp

---

## 🔧 Tech Stack

- **Python + Streamlit**
- **Tesseract OCR**
- **OpenCV** (image processing)
- **Regex** (data extraction)
- **Pandas** (CSV handling)

---

## 🚀 Quick Start

```bash
git clone https://github.com/your-username/loan-ocr-app.git
cd loan-ocr-app
pip install -r requirements.txt
streamlit run app
