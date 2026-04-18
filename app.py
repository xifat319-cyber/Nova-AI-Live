from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure API Key
genai.configure(api_key="AIzaSyA7oFMOQo7nPSsXgMFRa8yqG7jiKShDQdI")

# Dynamic Model Fetching (Error theke bachte)
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
        # Asol Magic: Hallucination bondho kora ebong limitation shikar kora
        enhanced_prompt = f"""Act as Nova AI, an advanced academic scholar assistant.
        CRITICAL RULE: You are an offline AI. Your training data only goes up to early 2024. The user is asking from the year 2026.
        DO NOT guess, predict, or hallucinate current events, current leaders, or current news.
        If the user asks about present-day facts, politics, or leaders in 2026, you MUST reply with: 'I apologize, but as an AI, my knowledge is limited to my last training update. I do not have real-time internet access to provide current 2026 news or political updates. Please verify this with a reliable news source.'
        User query: {user_message}"""

        response = chat.send_message(enhanced_prompt)
        return jsonify({'answer': response.text})
    except Exception as e:
        return jsonify({'answer': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
