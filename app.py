import json
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load your personal data
with open("mumbere_darius_profile.json", "r") as file:
    personal_data = json.load(file)

# Directly set your API key here
api_key = "AIzaSyAzPgqwBm4HvUOWMlaSJwF-0s3liPaSeeA"

# Configure Gemini API
genai.configure(api_key=api_key)

# Convert JSON data into a text format for AI context
knowledge_base = "\n".join([f"{k}: {v}" for k, v in personal_data.items()])

# Function to generate AI responses
def ask_gemini(question):
    model = genai.GenerativeModel("gemini-pro")  # Use free-tier model if available
    response = model.generate_content(f"Based on this information: {knowledge_base}\n\nQuestion: {question}")
    return response.text if response else "I don't know the answer."

# Flask API
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route("/ask", methods=["POST"])
def ask_question():
    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    answer = ask_gemini(user_question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
