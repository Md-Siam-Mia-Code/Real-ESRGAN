import os
import uuid
import subprocess
import threading
import zipfile
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    jsonify,
    send_file,
)
from io import BytesIO
import shutil

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "Input"
app.config["PROCESSED_FOLDER"] = "Output"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "webp"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["PROCESSED_FOLDER"], exist_ok=True)

progress_lock = threading.Lock()
progress_dict = {}
batch_files = {}
processes = {}


def clean_filename(filename):
    return "".join(c if c.isalnum() or c in (" ", "_") else "_" for c in filename)


def get_gpu_name():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        gpu_name = result.stdout.strip()
        return [{"name": gpu_name}]
    except Exception as e:
        print(f"Error getting GPU name: {str(e)}")
        return [{"name": "Default GPU"}]


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/")
def index():
    gpus = get_gpu_name()
    return render_template("index.html", gpus=gpus)


@app.route("/process", methods=["POST"])
def process_image():
    if "files" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist("files")
    if len(files) == 0:
        return jsonify({"error": "No selected files"}), 400

    batch_id = uuid.uuid4().hex
    processed_files = []

    for file in files:
        if file.filename == "" or not allowed_file(file.filename):
            continue

        original_filename = clean_filename(file.filename.rsplit(".", 1)[0])
        unique_id = uuid.uuid4().hex
        ext = file.filename.rsplit(".", 1)[1].lower()
        input_path = os.path.join(
            app.config["UPLOAD_FOLDER"], f"{unique_id}_{original_filename}.{ext}"
        )
        output_filename = f"Enhanced_{original_filename}.png"
        output_path = os.path.join(app.config["PROCESSED_FOLDER"], output_filename)
        file.save(input_path)

        cmd = [
            "./realesrgan/Real-ESRGAN.exe",
            "-i",
            input_path,
            "-o",
            output_path,
            "-s",
            request.form.get("scale", "4"),
            "-n",
            request.form.get("model", "4xHFA2k"),
            "-f",
            "png",
            "-v",
        ]

        if "tta" in request.form:
            cmd.append("-x")

        with progress_lock:
            progress_dict[unique_id] = {
                "progress": 0,
                "status": "processing",
                "output_url": None,
                "error": None,
                "output_path": output_path,
                "original_name": file.filename,
                "output_filename": output_filename,
            }

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        processes[unique_id] = process
        thread = threading.Thread(
            target=run_processing, args=(unique_id, cmd, input_path, output_path)
        )
        thread.start()
        processed_files.append(unique_id)

    with progress_lock:
        batch_files[batch_id] = processed_files

    return jsonify({"batch_id": batch_id, "task_ids": processed_files})


def run_processing(task_id, cmd, input_path, output_path):
    try:
        process = processes.get(task_id)
        for line in process.stdout:
            if "%" in line:
                try:
                    percent = int(line.split("%")[0].strip().split()[-1])
                    with progress_lock:
                        progress_dict[task_id]["progress"] = percent
                except:
                    pass

        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, cmd)

        with progress_lock:
            progress_dict[task_id]["status"] = "completed"
            progress_dict[task_id][
                "output_url"
            ] = f"/processed/{os.path.basename(output_path)}"

    except Exception as e:
        with progress_lock:
            progress_dict[task_id]["status"] = "error"
            progress_dict[task_id]["error"] = str(e)
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if task_id in processes:
            del processes[task_id]


@app.route("/progress/<task_id>")
def get_progress(task_id):
    with progress_lock:
        task_data = progress_dict.get(task_id, {"error": "Invalid task ID"})
    return jsonify(task_data)


# --- New route for batch progress ---
@app.route("/batch_progress/<batch_id>")
def get_batch_progress(batch_id):
    with progress_lock:
        file_ids = batch_files.get(batch_id, [])
        if not file_ids:
            return (
                jsonify(
                    {
                        "status": "error",
                        "error": "Invalid batch ID or no files in batch",
                    }
                ),
                404,
            )

        total_progress = 0
        completed_tasks = 0
        error_tasks = 0

        for task_id in file_ids:
            task_data = progress_dict.get(task_id)
            if task_data:
                if task_data["status"] == "completed":
                    total_progress += 100
                    completed_tasks += 1
                elif task_data["status"] == "processing":
                    total_progress += task_data["progress"]
                elif (
                    task_data["status"] == "error" or task_data["status"] == "cancelled"
                ):
                    error_tasks += 1

        if not file_ids:  # Avoid division by zero if no files
            average_progress = 0
        else:
            average_progress = total_progress / len(file_ids)

        batch_status = "processing"  # Default status
        if completed_tasks == len(file_ids):
            batch_status = "completed"
        elif error_tasks == len(file_ids):  # All tasks resulted in error or cancelled
            batch_status = "error"
        elif (completed_tasks + error_tasks) == len(
            file_ids
        ) and completed_tasks > 0:  # Some completed, some error/cancelled, but at least one completed
            batch_status = (
                "completed_with_errors"  # Or a more descriptive status if needed
            )

        return jsonify({"progress": average_progress, "status": batch_status})


@app.route("/processed/<filename>")
def processed_file(filename):
    return send_from_directory(
        app.config["PROCESSED_FOLDER"], filename, as_attachment=True
    )


@app.route("/cancel_processing", methods=["POST"])
def cancel_processing():
    data = request.json
    task_id = data.get("task_id")
    process = processes.get(task_id)
    if process:
        process.terminate()
        with progress_lock:
            progress_dict[task_id]["status"] = "cancelled"
        return jsonify({"status": "cancelled"})
    return jsonify({"error": "Process not found"}), 404


@app.route("/clear_history", methods=["POST"])
def clear_history():
    try:
        for folder in [app.config["UPLOAD_FOLDER"], app.config["PROCESSED_FOLDER"]]:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
        with progress_lock:
            progress_dict.clear()
            batch_files.clear()
            processes.clear()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download_all/<batch_id>")
def download_all(batch_id):
    with progress_lock:
        file_ids = batch_files.get(batch_id, [])

    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_id in file_ids:
            file_data = progress_dict.get(file_id)
            if file_data and file_data["status"] == "completed":
                zf.write(file_data["output_path"], file_data["output_filename"])

    memory_file.seek(0)
    return send_file(
        memory_file,
        mimetype="application/zip",
        as_attachment=True,
        download_name="Enhanced_Output.zip",
    )


if __name__ == "__main__":
    app.run(debug=True, port=1000)
