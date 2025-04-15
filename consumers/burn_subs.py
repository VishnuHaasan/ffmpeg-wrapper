import json
import logging
import subprocess

def burn_subs_into_video(
    ch,
    method,
    properties,
    body
):
    json_body = json.loads(body.decode())
    logging.info(f"Consuming message : {json_body}")
    in_path = json_body["input_path"]
    sub_path = json_body["sub_path"]
    out_path = json_body["output_path"]

    cmd1 = f"ffmpeg -i {in_path} -vf 'subtitles={sub_path}' {out_path}"
    process = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error burning subtitles: {process.stderr}")
    else:
        logging.info(f"Subtitles burned successfully: {out_path}")