from flask import Flask, render_template_string, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='static')


def word_tokenizer(text):
    text = text.lower()
    word = ""
    tokens = []


    for ch in text:
        if ('a' <= ch <= 'z') or ('0' <= ch <= '9') or ch == "'":
            word += ch
        else:
            if word != "":
                tokens.append(word)
                word = ""

    if word != "":
        tokens.append(word)

    return tokens


def char_tokenizer(text):
    text = text.lower()
    tokens = []

    for ch in text:
        if ch != " ":
            tokens.append(ch)

    return tokens


def sentence_tokenizer(text):
    sentences = []
    sentence = ""

    for ch in text:
        sentence += ch

        if ch in ".!?":
            cleaned = sentence.strip()
            if cleaned:
                sentences.append(cleaned)
            sentence = ""

    if sentence.strip():
        sentences.append(sentence.strip())

    return sentences


INDEX_HTML = open(
    os.path.join(os.path.dirname(__file__), "index.html"),
    encoding="utf-8"
).read()


@app.route("/")
def index():
    return render_template_string(INDEX_HTML)


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), "static"),
        filename
    )


@app.route("/tokenize", methods=["POST"])
def tokenize_route():
    data = request.get_json() or {}
    mode = data.get("mode", "word")
    text = data.get("text", "") or ""

    if mode == "char":
        tokens = char_tokenizer(text)
    elif mode == "sentence":
        tokens = sentence_tokenizer(text)
    else:
        tokens = word_tokenizer(text)

    return jsonify({
        "mode": mode,
        "tokens": tokens,
        "count": len(tokens),
        "input_preview": text[:200]
    })


if __name__ == "__main__":
    app.run(debug=True)
    
    