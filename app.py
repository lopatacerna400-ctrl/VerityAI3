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

Jsi kluk a jsi přátelský AI kamarád v Roblox hře.
Nejsi jen robot, jsi postava jménem Verity.
Pomáháš hráčům a mluvíš normálně jako člověk.

Hráč se jmenuje {player}.

Rozumíš překlepům, chybám bez háčků a čárek a různým jazykům.
Odpověz vždy jazykem hráče.

Na konci odpovědi vždy napiš jméno hráče: {player}

Zpráva hráče:
{message}

Odpověď Verity:
"""

    try:
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
            },
            timeout=30
        )

        result = response.json()

        if isinstance(result, list):
            answer = result[0].get(
                "generated_text",
                "Promiň, teď nemůžu odpovědět."
            )
        else:
            answer = "Promiň, AI služba teď neodpovídá."

    except Exception as e:
        print("AI ERROR:", e)
        answer = f"Promiň {player}, mám teď problém se spojením."

    return jsonify({
        "text": answer
    })


app.run(host="0.0.0.0", port=10000)
