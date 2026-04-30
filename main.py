from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os, uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "gizli-acar-123")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("HF_TOKEN")
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    history = data.get("history", [])

    messages = [{"role": "system", "content": "Sən AI-Tech-In köməkçisisən. Həmişə Azərbaycan dilində cavab ver. İstifadəçi ingilis yazsa ingilis cavab ver."}]
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct",
            messages=messages,
            max_tokens=1024,
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"response": f"Xəta: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
