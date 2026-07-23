from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/verity", methods=["POST"])
def verity():
    data = request.json

    player = data.get("player")
    message = data.get("text")

    answer = f"Ahoj {player}, slyším tě. Napsal jsi: {message}"

    return jsonify({
        "text": answer
    })

app.run(host="0.0.0.0", port=10000)
