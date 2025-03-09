import os
import base64
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from groq import Groq
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Missing GROQ_API_KEY in environment variables.")

# Analyze image using Groq API
def analyze_image(base64_image):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "List all visible ingredients in the food with their estimated weight in grams and total weight. Format: 'ingredient - weight'. Example: 'strawberry - 20g'"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            model="llama-3.2-11b-vision-preview",
        )

        response_text = chat_completion.choices[0].message.content
        return response_text.strip()
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']
    image_data = base64.b64encode(image.read()).decode('utf-8')
    result = analyze_image(image_data)

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
