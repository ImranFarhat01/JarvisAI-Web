from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from config import apikey

client = OpenAI(api_key=apikey)
app = Flask(__name__)
CORS(app)

# Store conversation history
conversation_history = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("message", "")

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})

        # Keep only last 10 messages to avoid token limits
        recent_history = conversation_history[-10:]

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fixed model name (was "gpt-4.1-mini")
            messages=recent_history,
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content

        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/reset", methods=["POST"])
def reset():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({"message": "Conversation reset"})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)