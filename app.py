import os
from flask import Flask, render_template, request, redirect, url_for, flash
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "demo_key"

# Load Gemini API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# System instructions for explaining code
SYSTEM_PROMPT = (
    "You are CodeBuddy, an assistant that explains code to beginners. "
    "1) Give a simple summary. "
    "2) Explain the code line-by-line. "
    "3) Give beginner-friendly suggestions."
)

def explain_code(code_text):
    """Uses Gemini to generate an explanation of the code."""
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(
        SYSTEM_PROMPT + "\n\nUser code:\n" + code_text
    )
    return response.text


@app.route("/", methods=["GET", "POST"])
def index():
    explanation = None

    if request.method == "POST":
        code_text = request.form.get("code_input", "").strip()

        if not code_text:
            flash("Please paste some code first.")
            return redirect(url_for("index"))

        try:
            explanation = explain_code(code_text)
        except Exception as e:
            # Show the error directly (no demo mode)
            explanation = f"Error contacting Gemini: {str(e)}"

    return render_template("index.html", explanation=explanation)


if __name__ == "__main__":
    app.run(debug=True)