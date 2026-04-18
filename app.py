import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Render-e amra GEMINI_API_KEY namer je variable set korlam, oita ekhane kaj korbe
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

working_model = "gemini-pro"
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        working_model = m.name
        break

model = genai.GenerativeModel(working_model)
chat = model.start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_ai():
    user_message = request.form['message']
    try:
        # 2026 Context Injection
        enhanced_prompt = f"Act as Nova AI, an advanced academic scholar assistant. The current year is 2026. If asked about current 2026 events, state that you don't have real-time internet access. User query: {user_message}"
        response = chat.send_message(enhanced_prompt)
        return jsonify({'answer': response.text})
    except Exception as e:
        return jsonify({'answer': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
