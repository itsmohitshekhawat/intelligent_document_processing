# import requests
# from flask import Flask, render_template, url_for
# from flask import request as req


# app = Flask(__name__)


# @app.route("/", methods=["GET", "POST"])
# def Index():
#     return render_template("index.html")


# @app.route("/Summarize", methods=["GET", "POST"])
# def Summarize():
#     if req.method == "POST":
#         API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
#         headers = {
#             "Authorization": "Bearer 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"
#         }  # Replace with your actual API token

#         data = req.form["data"]
#         maxL = int(req.form["maxL"])
#         minL = maxL // 4

#         def query(payload):
#             response = requests.post(API_URL, headers=headers, json=payload)
#             return response.json()

#         output = query(
#             {
#                 "inputs": data,
#                 "parameters": {"min_length": minL, "max_length": maxL},
#             }
#         )

#         # Check if response is a list and get the first element
#         if isinstance(output, list) and output:
#             summary_text = output[0].get("summary_text")
#         else:
#             summary_text = "Summary not available"

#         return render_template("index.html", result=summary_text)
#     else:
#         return render_template("index.html")


# if __name__ == "__main__":
#     app.debug = True
#     app.run()


import requests
from flask import Flask, render_template, request
import fitz  # PyMuPDF

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarize", methods=["POST"])
def Summarize():
    if request.method == "POST":
        # Extract text from uploaded PDF file
        pdf_file = request.files['pdf_file']
        if pdf_file:
            pdf_data = pdf_file.read()
            pdf_text = extract_text_from_pdf(pdf_data)

            # Summarize the text
            if pdf_text:
                summary_text = summarize_text(pdf_text)
                return render_template("index.html", result=summary_text)
            else:
                return render_template("index.html", result="Failed to extract text from PDF")
        else:
            return render_template("index.html", result="No PDF file uploaded")

def extract_text_from_pdf(pdf_data):
    try:
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print("Error extracting text from PDF:", e)
        return None

def summarize_text(text):
    # Implement your summarization logic here
    # For now, simply return the first 1000 characters as a summary
    return text[:1000]

if __name__ == "__main__":
    app.run(debug=True)



