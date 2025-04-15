import json
import logging
import subprocess

def add_color_filters(
    ch,
    method,
    properties,
    body
):
    json_body = json.loads(body.decode())
    logging.info(f"Consuming message : {json_body}")
    in_path = json_body["input_path"]
    out_path = json_body["output_path"]
    color_filter = json_body["color_filter"]

    cmd1 = f"ffmpeg -i {in_path} -vf '{color_filter}' -c:a copy {out_path}"
    process = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error applying color filter: {process.stderr}")
    else:
        logging.info(f"Color filter applied successfully: {out_path}")