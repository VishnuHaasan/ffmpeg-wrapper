import json
import logging
import subprocess

def extract_subs_into_ass(
    ch,
    method,
    properties,
    body
):
    json_body = json.loads(body.decode())
    logging.info(f"Consuming message : {json_body}")
    in_path = json_body["input_path"]
    sub_index = json_body["sub_index"]
    out_path = json_body["output_path"]

    f_name, ext = in_path.split("/")[-1].split(".")
    f_name_int = f"{f_name}_intermediate.srt"
    int_path = f"{'/'.join(in_path.split("/")[:-1])}/{f_name_int}"

    cmd1 = f"ffmpeg -i {in_path} -map 0:s:{sub_index} {int_path}"
    process = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error occurred while extracting subtitles: {process.stderr}")
        return
    else:
        logging.info(f"Subtitles extracted successfully to intermediate file: {int_path}")

    cmd2 = f"ffmpeg -sub_charenc ISO-8859-1 -i {int_path} {out_path}"
    process = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error occurred while converting .srt to .ass : {process.stderr}")
        return
    else:
        logging.info(f"Successfully converted .srt to .ass")

    cmd3 = f"rm {int_path}"
    process = subprocess.run(cmd3, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error occurred while removing the intermediate file : {process.stderr}")
        return
    else:
        logging.info(f"Successfully removed intermediate file : {int_path}")

