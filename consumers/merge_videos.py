import os
import json
import time
import logging
import subprocess

def merge_vids(
    ch,
    method,
    properties,
    body
):
    json_body = json.loads(body.decode())
    logging.info(f"Consuming message : {json_body}")
    out_path = json_body["output_path"]
    video_list = json_body["video_list"]

    int_path = os.getcwd() + f"/{int(time.time())}_intermediate.txt"

    with open(int_path, "w") as file:
        for video in video_list:
            file.write(f"file '{video}'\n")

    cmd1 = f"ffmpeg -f concat -safe 0 -i {int_path} -c copy {out_path}"
    process = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error merging videos: {process.stderr}")
        return
    else:
        logging.info(f"Videos merged successfully: {out_path}")

    cmd2 = f"rm {int_path}"
    process = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error deleting intermediate file: {process.stderr}")
    else:
        logging.info(f"Intermediate file deleted successfully: {int_path}")

