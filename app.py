from flask import Flask, request
from flask_cors import CORS
from textblob import TextBlob
from random import choice

app = Flask(__name__)
CORS(app)

positive_phrases = [
    "Que bueno, sigue así!",
    "Me da mucho gusto :D",
    "Es todo prro!"
]

negative_phrases = [
    "Echale ganas mijo",
    "Ta canijo pero tu puedes",
    "Animo, todo va a mejorar"
]

def analyse():
    polarity = 0
    subjectivity = 0

    text = request.get_json()['message']

    blob = TextBlob(text)
    blob = blob.translate(to="en")

    for sentence in blob.sentences:
        polarity = polarity + sentence.sentiment.polarity
        subjectivity = subjectivity + sentence.sentiment.subjectivity

    return (polarity, subjectivity)


@app.route("/", methods=["POST"])
def index():
    if request.method == "POST":
        polarity, subjectivity = analyse()

        if polarity < 0:
            return ("Tuviste un mal dia basado en tu polaridad de {0}, estoy seguro en un {1}, {2}").format(polarity, subjectivity, choice(negative_phrases))
        else:
            return ("Tuviste un buen dia basado en tu polaridad de {0}, estoy seguro en un {1}, {2}").format(polarity, subjectivity, choice(positive_phrases))


if __name__ == "__main__":
    app.run()
