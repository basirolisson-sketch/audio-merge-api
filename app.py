from flask import Flask, request, send_file, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "ok"}

@app.route("/merge", methods=["POST"])
def merge_audio():

    if "files" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist("files")

    if len(files) < 2:
        return jsonify({"error": "Upload at least 2 files"}), 400

    temp_id = str(uuid.uuid4())
    paths = []

    for i, file in enumerate(files):
        path = f"/tmp/{temp_id}_{i}.mp3"
        file.save(path)
        paths.append(path)

    list_file = f"/tmp/{temp_id}_list.txt"

    with open(list_file, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")

    output = f"/tmp/{temp_id}_output.mp3"

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        output
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return send_file(
        output,
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name="merged.mp3"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
