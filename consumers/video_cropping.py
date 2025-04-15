import os
import json
import logging
import subprocess

def compress_and_crop(
    ch,
    method,
    properties,
    body
):
    json_body = json.loads(body.decode())
    logging.info(f"Consuming message : {json_body}")
    in_path = json_body["in_path"]
    out_path = json_body["out_path"]
    intermediate_scale = json_body["intermediate_scale"]
    crop_to = json_body["crop_to"]
    scale_out = json_body["scale_out"]
    out_sar = json_body["out_sar"]

    f_name, ext = in_path.split("/")[-1].split(".")
    f_name_int = f"{f_name}_intermediate.{ext}"
    int_path = f"{'/'.join(in_path.split("/")[:-1])}/{f_name_int}"

    cmd1 = f"ffmpeg -i {in_path} -vf 'scale={intermediate_scale},crop={crop_to}' -c:a copy {int_path}"
    process = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error during intermediate processing: {process.stderr}")
        return
    else:   
        logging.info(f"Intermediate processing done successfully: {int_path}")

    cmd2 = f"ffmpeg -i {int_path} -vf 'scale={scale_out},setsar={out_sar}' -c:a copy {out_path}"
    process = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error during final processing: {process.stderr}")
    else:
        logging.info(f"Final processing done successfully: {out_path}")

    cmd3 = f"rm {int_path}"
    process = subprocess.run(cmd3, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error deleting intermediate file: {process.stderr}")
    else:
        logging.info(f"Intermediate file deleted successfully: {int_path}")


    