from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from flask_cors import CORS
from openai import OpenAI
from config import apikey
import json

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

        def generate():
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=recent_history,
                temperature=0.7,
                max_tokens=500,
                stream=True
            )

            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield f"data: {json.dumps({'content': content})}\n\n"

            # Add complete response to history
            conversation_history.append({"role": "assistant", "content": full_response})
            yield f"data: {json.dumps({'done': True})}\n\n"

        return Response(stream_with_context(generate()), mimetype='text/event-stream')

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