import cv2
import numpy as np 
import math
import subprocess

def convert_to_vr(input_file, output_file):
    # Set up FFmpeg command
    command = ['ffmpeg', '-i', input_file, '-filter_complex', '[0:v]split[vl][vr];[vl]pad=iw*2:ih[vl];[vl][vr]overlay=w', output_file]
    
    # Run FFmpeg command
    subprocess.run(command)

convert_to_vr("phone_video.mp4","phone.mp4")


