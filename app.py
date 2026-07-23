from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

@app.route("/verity", methods=["POST"])
def verity():

    data = request.json

    player = data.get("player")
    message = data.get("text")

    prompt = f"""
Jsi Verity.
Jsi kluk a jsi přátelský AI kamarád v Roblox hře.

Mluvíš přirozeně.
Rozumíš chybám v psaní a různým jazykům.
Vždy odpovídej správným jazykem hráče.

Hráč se jmenuje {player}.

Na konci každé odpovědi napiš jeho jméno.

Hráč napsal:
{message}
"""

    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers={
            "Authorization": f"Bearer {HF_TOKEN}"
        },
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150
            }
        }
    )

    result = response.json()

    answer = result[0]["generated_text"]

    return jsonify({
        "text": answer
    })


app.run(host="0.0.0.0", port=10000)
