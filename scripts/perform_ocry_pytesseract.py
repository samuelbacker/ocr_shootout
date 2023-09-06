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



parser = argparse.ArgumentParser()
parser.add_argument("--input_file", dest='input_file', help="input_file_folder")
parser.add_argument("--output_file", dest= "output_file", help = "output_ocr_text")


args = parser.parse_args()


def make_ocr(the_file):
    text_file = []
    for i in range(len(the_file)):
        page = the_file[i]
        pixmap = page.get_pixmap()
        png_bytes = pixmap.tobytes()
        image = Image.open(io.BytesIO(png_bytes))
        #there are also definitely modes to further test/explore here, including page/column segmentation mode                                                                                                       
        text = pytesseract.image_to_string(image)
        text = text.replace('\n', ' ')
        text_file.append(text)
    return text_file


text_list = {}


pathway = args.input_file
with open (pathway, 'r') as zip_file:
    doc = fitz.open(zip_file)
    out_text = make_ocr(doc)
    text_list[pathway] = out_text

with open (args.output_file, "w") as out_file:
    out_file.write(json.dumps(text_list, indent = 4))
