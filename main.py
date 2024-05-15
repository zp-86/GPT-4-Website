import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from openai import OpenAI

client = OpenAI()
app = Flask(__name__) # defaults to getting the key using os.environ.get("OPENAI_API_KEY")

chat_history = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    prompt = data["prompt"]
    key = data["key"]
    session_id = data["session_id"]

    if key == "gpt4":
        if session_id not in chat_history:
            chat_history[session_id] = []

        chat_history[session_id].append({"role": "user", "content": prompt})

        messages = [{"role": "system", "content": "You are a helpful assistant named GPT-4."}]
        chat_messages = chat_history[session_id]

        for message in chat_messages:
            role = "user" if message.get("sender") == "user" else "assistant"
            messages.append({"role": role, "content": message.get("message", "")})

        messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        answer = completion.choices[0].message.content
        chat_history[session_id].append({"role": "assistant", "content": answer})

        server_response = answer
    elif key == "reset":
        print(chat_history)
        chat_history[session_id] = []
        server_response = "Chat history reset"

    else:
        return jsonify({"message": "Invalid key"})

    return jsonify({"message": server_response})


app.run()
