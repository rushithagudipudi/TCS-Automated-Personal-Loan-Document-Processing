

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

## 📸 Screenshots

### Main Page
![Screenshot 2025-04-24 205524](https://github.com/user-attachments/assets/5819c5ab-2083-4089-913c-1d9351e2123b)


### OCR Text Preview
![Screenshot 2025-04-24 205539](https://github.com/user-attachments/assets/1d319c75-42d4-461c-bcc1-a2f8157ac7bd)

### OCR Corrections Page
![Screenshot 2025-04-24 205603](https://github.com/user-attachments/assets/bfa7c2e2-ed7d-4da1-bb7d-df866a75b1fc)

### Extracted Data Saved
![Screenshot 2025-04-24 205619](https://github.com/user-attachments/assets/4840befe-0e0e-4d48-b77a-fc93b8236109)
![Screenshot 2025-04-24 210104](https://github.com/user-attachments/assets/d9811e3f-cb49-4a9a-b54a-c6ae333605f7)


