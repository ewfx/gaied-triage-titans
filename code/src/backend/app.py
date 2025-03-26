import os
import json
import pdfplumber
import pytesseract
from flask import Flask, jsonify, send_from_directory, request, url_for
from PIL import Image
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

# Set path for Tesseract on Windows (Update accordingly)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
CORS(app)

# Folder containing PDF emails
EMAIL_FOLDER = "emails"  # Update path if necessary
app.config["UPLOAD_FOLDER"] = EMAIL_FOLDER

# Load the pre-trained Flan-T5 model
classifier = pipeline("text2text-generation", model="google/flan-t5-base")

# Define request types for classification
REQUEST_TYPES = [
  "Adjustment", "AU Transfer", "Closing Notice - Reallocation fees",
  "Closing Notice - Amendment fees", "Closing Notice - Reallocation principal",
  "Commitment Charge - Cashless Roll", "Commitment Charge - Decrease",
  "Commitment Charge - Increase", "Fee Payment - Ongoing fee",
  "Fee Payment - Letter of Credit Fee", "Money Movement - Inbound Principal",
  "Money Movement - Inbound Interest", "Money Movement - Inbound Principal + Interest",
  "Money Movement - Outbound Timebound", "Money Movement - Outbound Foreign Currency"
]

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
  text = ""
  with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
      text += page.extract_text() or ""  # Extract text if possible
      # Use OCR if text extraction fails
      if not text.strip():
        image = page.to_image().annotated
        text += pytesseract.image_to_string(image)
  return text.strip()

# Function to classify email content
def classify_email(content):
  prompt = f"Categorize the following email into one of these request types: {', '.join(REQUEST_TYPES)}.\nEmail: {content}\nResponse:"
  response = classifier(prompt, max_length=50, num_return_sequences=1)
  classification = response[0]['generated_text']
  return classification

# Function to compute confidence score
def compute_confidence_score(classification, content):
  words_in_classification = set(classification.lower().split())
  words_in_content = set(content.lower().split())
  common_words = words_in_classification & words_in_content
  return round(len(common_words) / len(words_in_classification), 2)

# Function to detect duplicate emails
def detect_duplicates(email_texts):
  vectorizer = TfidfVectorizer().fit_transform(email_texts)
  similarity_matrix = cosine_similarity(vectorizer)

  duplicates = {}
  for i, row in enumerate(similarity_matrix):
    for j, similarity in enumerate(row):
      if i != j and similarity > 0.85:  # Consider 85% similarity as duplicate
        duplicates[i] = j
  return duplicates

# Flask API endpoint to serve PDFs
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
  return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

# Flask API endpoint
@app.route('/classify_emails', methods=['GET'])
def classify_emails():
  results = []
  email_texts = []
  filenames = []

  # Process all PDFs in the folder
  for filename in os.listdir(EMAIL_FOLDER):
    if filename.endswith(".pdf"):
      pdf_path = os.path.join(EMAIL_FOLDER, filename)
      email_text = extract_text_from_pdf(pdf_path)
      email_texts.append(email_text)
      filenames.append(filename)

  # Detect duplicate emails
  duplicate_indices = detect_duplicates(email_texts)

  for idx, email_text in enumerate(email_texts):
    request_type = classify_email(email_text)
    confidence_score = compute_confidence_score(request_type, email_text)

    download_url = url_for('download_file', filename=filenames[idx], _external=True)

    result = {
      "email": f"{filenames[idx]}",
      "request_type": request_type,
      "confidence_score": confidence_score,
      "reasoning": f"Classified based on LLM response and content analysis.",
      "download_url": download_url
    }
    results.append(result)

  return jsonify(results)

if __name__ == '__main__':
  app.run(debug=True)
