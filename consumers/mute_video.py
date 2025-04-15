import json
import logging
import subprocess

def mute_video(
    ch,
    method,
    properties,
    body
):
    json_body = json.loads(body.decode())
    logging.info(f"Consuming message : {json_body}")
    in_path = json_body["input_path"]
    out_path = json_body["output_path"]

    cmd1 = f"ffmpeg -i {in_path} -c:v copy -an {out_path}"
    process = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error muting video: {process.stderr}")
    else:
        logging.info(f"Video muted successfully: {out_path}"
)