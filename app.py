import os
import base64
from groq import Groq
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Analyze image using Groq API
def analyze_image(base64_image):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Can you tell me as precise as possible calorie count of the image?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
    )
    
    response_text = chat_completion.choices[0].message.content
    
    if isinstance(response_text, str):
        return response_text
    
    formatted_response = "\n".join(
        [f"* {item.capitalize()}: {cal} calories" for item, cal in response_text.items() if item != "total"]
    )
    
    return f"{formatted_response}\n\nTotal estimated calorie count: {response_text.get('total', 'N/A')} calories."


# Serve HTML form
@app.route('/')
def index():
    return render_template('index.html')

# API to analyze image
@app.route('/analyze', methods=['POST'])
def analyze():
    image = request.files['image']
    image_data = base64.b64encode(image.read()).decode('utf-8')
    result = analyze_image(image_data)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
