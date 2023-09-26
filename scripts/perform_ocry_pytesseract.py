import os
import subprocess
from PIL import Image
import glob
import io
import pytesseract
from PyPDF2 import PdfReader
import argparse
import json
import fitz
import cv2
import numpy as np

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", dest='input_file', help="input_file_folder")
parser.add_argument("--output_file", dest= "output_file", help = "output_ocr_text")
parser.add_argument("--grayscale", dest = "grayscale", type =str2bool, help="Convert image to grayscale")
parser.add_argument("--denoise", dest = "denoise", type = str2bool,help="Remove noise from image")
parser.add_argument("--binary_threshold", dest = "binary_threshold", type = str2bool, help="Apply binary thresholding")
parser.add_argument("--preprocess", dest = "pre_process", type = str2bool, help = "is preprocess on?") 
parser.add_argument("--test_segmentation", dest = "seg_test", type = str2bool, help = "test segmentation methods?") 
args = parser.parse_args()
settings = {
        "grayscale": args.grayscale,
        "denoise": args.denoise,
        "binary_threshold": args.binary_threshold 
    }

seg_types = ["--psm 1", "--psm 4", "--psm 11","--psm 12"]
seg_result = args.seg_test
#print("initial seg result")
#print(seg_result)


def make_ocr(the_file, seg_no = ""):
    text_file = []
 #   print("in the make ocr function")
  #  print(seg_result)
    for i in range(len(the_file)):
        page = the_file[i]
        pixmap = page.get_pixmap()
        png_bytes = pixmap.tobytes()
        image = Image.open(io.BytesIO(png_bytes))
        #there are also definitely modes to further test/explore here, including page/column segmentation mode
        
        if args.pre_process == True:
      #      print("preprocessed!")
            text = preprocess_image(image, settings)
            text = pytesseract.image_to_string(text)
            text = text.replace('\n', ' ')
            text_file.append(text)
        elif seg_result == True:
       #     print("segmented!")
            text = pytesseract.image_to_string(image,config = seg_no)
            text = text.replace('\n', ' ')
            text_file.append(text)
        else:
        #    print("done normally")
            text = pytesseract.image_to_string(image)
            text = text.replace('\n', ' ')
            text_file.append(text)
    return text_file


def preprocess_image(page, settings):
    
    image_np = np.array(page)

    if settings.get("grayscale", True):
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    if settings.get("denoise", True):
        image_np = cv2.medianBlur(image_np, 3)

    if settings.get("binary_threshold", True):
        _, image_np = cv2.threshold(image_np, 128, 255, cv2.THRESH_BINARY)

    processed_image = Image.fromarray(image_np)

    return processed_image

#the dictionary wrapper gives names to the ocr-ed files. 
text_list = {}


pathway = args.input_file

with open (pathway, 'r') as zip_file:
    doc = fitz.open(zip_file)
    #print("in the basic open ")
    #print(seg_result)
    #print(type(seg_result))
    if seg_result == True:
        for seg_name in seg_types:
            name = pathway + seg_name
            out_text = make_ocr(doc,seg_no = seg_name) 
            text_list[name] = out_text
            #print(out_text)
    else:
     #   print("segment_test_false")
        out_text = make_ocr(doc)
        text_list[pathway] = out_text
        #print(out_text)

with open (args.output_file, "w") as out_file:
    out_file.write(json.dumps(text_list, indent = 4))
 
