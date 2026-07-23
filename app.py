from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

HF_TOKEN = os.environ.get("HF_TOKEN")

MODEL = "mistralai/Mistral-7B-Instruct-v0.2"


@app.route("/verity", methods=["POST"])
def verity():

    data = request.json

    player = data.get("player", "hráč")
    message = data.get("text", "")

    prompt = f"""
Jsi Verity.

Jsi kluk a jsi AI kamarád v Roblox hře.
Jmenuješ se Verity.
Pomáháš hráčům a chováš se jako normální kamarád.

Hráč se jmenuje {player}.

Rozumíš:
- chybám v psaní
- textu bez háčků a čárek
- různým jazykům

Odpověz jazykem hráče.

Na konci odpovědi napiš jméno hráče {player}.

Hráč:
{message}

Verity:
"""

    try:

        response = requests.post(
            "https://api-inference.huggingface.co/models/" + MODEL,
            headers={
                "Authorization": "Bearer " + HF_TOKEN
            },
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200
                }
            },
            timeout=30
        )

        result = response.json()

        print("HUGGING FACE ODPOVED:", result)

        if isinstance(result, list):
            answer = result[0]["generated_text"]
        else:
            answer = "AI chyba: " + str(result)

    except Exception as e:

        print("AI ERROR:", e)

        answer = "Promiň " + player + ", Verity má problém se spojením."


    return jsonify({
        "text": answer
    })


app.run(
    host="0.0.0.0",
    port=10000
)
