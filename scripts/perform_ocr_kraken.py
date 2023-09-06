
from PIL import Image
import glob
from PyPDF2 import PdfReader
import argparse
import json
import fitz
from kraken import binarization, pageseg, blla, serialization 
from kraken.lib import vgsl, models




parser = argparse.ArgumentParser()
parser.add_argument("--input_file", dest='input_folder', help="input_file_folder")
parser.add_argument("--output_file", dest= "output_file", help = "output_ocr_text")

args = parser.parse_args()

seg_model_path = "/home/sbacker2/ocr_shootout/ocr_comparison/kraken/blla_ft_lectaurep_logical_structure.mlmodel"
seg_model =  vgsl.TorchVGSLModel.load_model(seg_model_path)
rec_model_path = "/home/sbacker2/ocr_shootout/ocr_comparison/kraken/en_best.mlmodel"
rec_model = models.load_any(rec_model_path) 
output_dict = {}

pathway = args.input_folder
for x in glob.glob("{}*".format(pathway)):
    print(x)
    print("did it")
    with open (x, 'r') as zip_file:
        doc = fitz.open(zip_file)
        bw_im = binarization.nlbin(im)
        seg = pageseg.segment(bw_im)
        baseline_seg = blla.segment(im, model=seg_model)
        print(baseline_seg)
        #alto = serialization.serialize_segmentation(baseline_seg, image_name=im.filename, image_size=im.size, template='alto')
        pred_it = kraken.rpred.rpred(rec_model, im, baseline_seg)
        out_list = []
        for record in pred_it:
            letter = record.prediction
            out_list.append(letter)
        output_dict[x] = out_list

with open(args.output_file, "w") as json_out:
    json_out.write(json.dumps(output_dict, indent = 4))
