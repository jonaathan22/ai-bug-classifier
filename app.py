from flask import Flask, request, render_template
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Safety check
if not api_key:
    raise ValueError(" GEMINI_API_KEY is missing. Please add it to your .env file.")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-pro")

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    severity = None

    if request.method == "POST":
        bug_description = request.form.get("description", "")
        prompt = f"Classify the severity of this software bug (low, medium, high, critical) and explain why: {bug_description}"

        try:
            response = model.generate_content(prompt)
            severity = response.text.strip()
        except Exception as e:
            severity = f"❌ AI Error: {str(e)}"

    return render_template("index.html", severity=severity)

if __name__ == "__main__":
    app.run(debug=True)
