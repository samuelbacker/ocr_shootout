import json
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", dest='input_file', help="input_file_folder", nargs = "+")
parser.add_argument("--output_file", dest= "output_file", help = "output_ocr_text")

args = parser.parse_args()
out_dict = {}
pathway = args.input_file
#print(pathway)
for path in pathway:
    print("this is the way")
    print(path)
    with open(path, 'r') as zip_file:
        path = path.split("from")
        path = path[1]
        path = path.split(".")
        path = path[0]
        print(path)
        thing = zip_file.read()
        dictionary = json.loads(thing)
        keys = dictionary.keys()
        for key in keys:
            if out_dict.get(key):
                temp_list = out_dict[key]
                temp_list.append([path, dictionary[key]])
                out_dict[key] = temp_list
            else:
                temp_list = []
                temp_list.append([path,dictionary[key]])
                out_dict[key] = temp_list
with open(args.output_file, "w") as out_file:
    out_file.write(json.dumps(out_dict, indent = 4))
            
