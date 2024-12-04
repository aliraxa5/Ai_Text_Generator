from flask import Flask, render_template, request, jsonify
import openai
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Set API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_API_URL = "https://api.anthropic.com/v1/complete"

# Initialize Flask app
app = Flask(__name__)

# Function to call OpenAI API
def generate_with_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

# Function to call Claude API
def generate_with_claude(prompt):
    try:
        headers = {"Authorization": f"Bearer {CLAUDE_API_KEY}"}
        payload = {
            "prompt": prompt,
            "max_tokens_to_sample": 150
        }
        response = requests.post(CLAUDE_API_URL, headers=headers, json=payload)
        response_data = response.json()
        return response_data.get("completion", "No response received.")
    except Exception as e:
        return f"Error: {e}"

# Route for the frontend
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle text generation
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    api_choice = data.get('api_choice')

    if not prompt or not api_choice:
        return jsonify({"error": "Missing 'prompt' or 'api_choice'"}), 400

    if api_choice == "openai":
        result = generate_with_openai(prompt)
    elif api_choice == "claude":
        result = generate_with_claude(prompt)
    else:
        return jsonify({"error": "Invalid 'api_choice'. Use 'openai' or 'claude'"}), 400

    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True)
