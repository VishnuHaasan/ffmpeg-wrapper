import json
import logging
import subprocess

def convert_video_format(
    ch,
    method,
    properties,
    body
):
    json_body = json.loads(body.decode())
    logging.info(f"Consuming message : {json_body}")
    in_path = json_body["input_path"]
    out_path = json_body["output_path"]

    cmd1 = f"ffmpeg -i {in_path} -codec copy {out_path}"
    process = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error converting video format: {process.stderr}")
    else:
        logging.info(f"Video format converted successfully: {out_path}")
