import json
import logging
import subprocess

def change_video_and_audio_speed(
    ch,
    method,
    properties,
    body
):
    json_body = json.loads(body.decode())
    logging.info(f"Consuming message : {json_body}")
    in_path = json_body["input_path"]
    out_path = json_body["output_path"]
    video_speedup = json_body["vid_speedup"]
    audio_speedup = json_body["audio_speedup"]

    cmd1 = f"ffmpeg -i {in_path} -filter_complex '[0:v]setpts={video_speedup}*PTS[v];[0:a]atempo={audio_speedup}[a]' -map '[v]' -map '[a]' {out_path}"
    process = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        logging.error(f"Error changing video and audio speed: {process.stderr}")
    else:
        logging.info(f"Video and audio speed changed successfully: {out_path}")