from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# === Setup DeepSeek API ===
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # set in environment
API_URL = "https://api.deepseek.com/v1/chat/completions"

# === Webpage route ===
@app.route("/")
def index():
    return render_template("index.html")

# === Chat route ===
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    # System instruction (forces Nepali)
    messages = [
        {"role": "system", "content": "तपाईं एक उपयोगी र विनम्र नेपाली भाषा बोल्ने सहायक हुनुहुन्छ। सबै जवाफ नेपालीमा मात्र दिनुहोस्।"},
        {"role": "user", "content": user_message}
    ]

    payload = {"model": "deepseek-chat", "messages": messages, "stream": False}
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"माफ गर्नुहोस्, कुनै त्रुटि भयो: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
