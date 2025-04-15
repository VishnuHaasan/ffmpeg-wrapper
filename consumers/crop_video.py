import json
import logging
import subprocess

def crop_video(
    ch,
    method,
    properties,
    body
):
    json_body = json.loads(body.decode())
    logging.info(f"Consuming message : {json_body}")
    in_path = json_body["input_path"]
    out_path = json_body["output_path"]
    from_duration = json_body["from_duration"]
    to_duration = json_body["to_duration"]

    cmd1 = f"ffmpeg -i {in_path} -ss {from_duration} -to {to_duration} -c copy {out_path}"
    process = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error cropping video: {process.stderr}")
    else:
        logging.info(f"Video cropped successfully: {out_path}")