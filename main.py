import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import openai

app = Flask(__name__)
openai.api_key = ""

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

        chat_history[session_id].append({"message": prompt, "sender": "user"})

        messages = [
            {"role": "system", "content": "You are a helpful assistant named GPT-4."},
            {"role": "user", "content": prompt},
        ]

        chat_messages = chat_history[session_id]
        for message in chat_messages:
            messages.append(
                {"role": "user" if message["sender"] == "user" else "assistant", "content": message["message"]})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
        )
        answer = completion.choices[0].message["content"]
        chat_history[session_id].append({"message": answer, "sender": "assistant"})

        server_response = answer
    elif key == "reset":
        print(chat_history)
        chat_history[session_id] = []
        server_response = "Chat history reset"

    else:
        return jsonify({"message": "Invalid key"})

    return jsonify({"message": server_response})


app.run()
