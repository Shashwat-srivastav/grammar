# app.py
from flask import Flask, request, jsonify, render_template
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

# Get your Groq API key from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY is not set in your .env file.")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route("/")
def index():
    # Serve the index.html template
    return render_template("index.html")

@app.route("/correct", methods=["POST"])
def correct():
    data = request.get_json()
    text = data.get("text", "")
    print("Received transcript for correction:", text)  # Log transcript to terminal

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Prepare the prompt for the Groq API
    message_content = f'Please correct the grammar, articulation and English usage of the following text: "{text}"'
    request_data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{
            "role": "user",
            "content": message_content
        }]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + GROQ_API_KEY
    }

    # Call the Groq API
    response = requests.post(GROQ_API_URL, json=request_data, headers=headers)
    print("Groq API response:", response.text)  # Log API response

    if response.status_code != 200:
        return jsonify({"error": "Groq API error: " + response.text}), response.status_code

    api_response = response.json()
    # Assuming the corrected text is in the following structure:
    corrected_text = api_response["choices"][0]["message"]["content"]
    print("Corrected text:", corrected_text)  # Log corrected text
    return jsonify({"corrected_text": corrected_text})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
