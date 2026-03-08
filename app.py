from flask import Flask, request, send_file
import subprocess
import os

app = Flask(_name_)

@app.route("/")
def home():
    return {"status": "ok"}

@app.route("/merge", methods=["POST"])
def merge_audio():
    files = request.files.getlist("files")

    paths = []

    for i, file in enumerate(files):
        path = f"/tmp/input{i}.mp3"
        file.save(path)
        paths.append(path)

    list_file = "/tmp/list.txt"

    with open(list_file, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")

    output = "/tmp/output.mp3"

    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output
    ])

    return send_file(output, mimetype="audio/mpeg", as_attachment=True, download_name="merged.mp3")

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)
