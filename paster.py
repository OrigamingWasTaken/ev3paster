from ast import arg
import json
import random
import sys
import os
from os import path
from textwrap import indent
import zipfile
from zipfile import ZipFile
import tempfile
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))
args = sys.argv
class colors:
        BLACK = '\u001b[30m'
        RED = '\u001b[31m'
        BRED = '\u001b[41;1m'
        GREEN = '\u001b[32m'
        BGREEN = '\u001b[42;1m'
        YELLOW = '\033[92m'
        BYELLOW = '\u001b[43;1m'
        BLUE = '\u001b[34m'
        MAGENTA = '\u001b[35m'
        BMAGENTA = '\u001b[45;1m'
        CYAN = '\u001b[36;1m'
        WHITE = '\u001b[37m'
        BWHITE = '\u001b[47;1m'
        RESET = '\u001b[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

if not path.isdir(path.join(dir_path,"Projects")):
    os.mkdir(path.join(dir_path,"Projects"))

if not len(args) >= 3:
    print(colors.RED + colors.BOLD + "Please provide 2 files" + colors.RESET)
    exit()

if not path.isfile(args[1]):
    print(colors.RED + colors.BOLD + "Could not paste: file1 is not valid" + colors.RESET)
    exit()

if not path.isfile(args[2]):
    print(colors.RED + colors.BOLD + "Could not paste: file2 is not valid" + colors.RESET)
    exit()

file1 = args[1]
file2 = args[2]

fileFolder1 = tempfile.mktemp()
fileFolder2 = tempfile.mktemp()

ZipFile(file1).extractall(fileFolder1)
ZipFile(file2).extractall(fileFolder2)

ZipFile(path.join(fileFolder1,"scratch.sb3")).extractall(path.join(fileFolder1,"scratch"))
ZipFile(path.join(fileFolder2,"scratch.sb3")).extractall(path.join(fileFolder2,"scratch"))

os.remove(path.join(fileFolder1,"scratch.sb3"))
os.remove(path.join(fileFolder2,"scratch.sb3"))

inJson = json.load(open(path.join(fileFolder2,"scratch/project.json")))

dirname = "Combined Project"
while path.isdir(path.join(dir_path,"Projects",dirname)):
    dirname = dirname + str(random.randrange(1,999))

files = os.listdir(fileFolder1)
shutil.copytree(fileFolder1,path.join(dir_path,"Projects",dirname))

project = path.join(dir_path,"Projects",dirname)

fromJson = json.load(open(path.join(project,"scratch/project.json"),"r+"))

fromJson["targets"][1]["blocks"] = fromJson["targets"][1]["blocks"] | inJson["targets"][1]["blocks"]
fromJson["targets"][1]["variables"] = fromJson["targets"][1]["variables"] | inJson["targets"][1]["variables"]
fromJson["targets"][1]["lists"] = fromJson["targets"][1]["lists"] | inJson["targets"][1]["lists"]
fromJson["targets"][1]["broadcasts"] = fromJson["targets"][1]["broadcasts"] | inJson["targets"][1]["broadcasts"]
fromJson["targets"][1]["comments"] = fromJson["targets"][1]["comments"] | inJson["targets"][1]["comments"]
fromJson["extensions"] = fromJson["extensions"] + inJson["extensions"]

os.remove(path.join(project,"scratch/project.json"))
with open(path.join(project,"scratch/project.json"),"w") as f:
    json.dump(fromJson,f)

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

with ZipFile("scratch.sb3","w",zipfile.ZIP_DEFLATED) as zipe:
    zipdir(path.join(project,"scratch"),zipe)
    shutil.move(path.join(dir_path,"scratch.sb3"),path.join(dir_path,"Projects",dirname))
    shutil.rmtree(path.join(project,"scratch"))

def lmsp():
    pass

zipf = shutil.make_archive(path.join(dir_path,"Projects",dirname),"zip",project)
os.rename(path.join(dir_path,"Projects",dirname + ".zip"),dirname + ".lmsp")
shutil.rmtree(path.join(dir_path,"Projects",dirname))
shutil.move(path.join(dir_path,dirname + ".lmsp"),path.join(dir_path,"Projects"))

# zipf = shutil.make_archive(dirname, "zip", dirname)
# shutil.rmtree(path.join(dir_path,"Projects",dirname))
# os.rename(zipf,path.join(dir_path,"Projects",dirname + ".lmsp"))

# with ZipFile(dirname + ".lmsp", 'w', zipfile.ZIP_DEFLATED) as zipf:
#     zipdir(project + "/", zipf)
#     shutil.move(path.join(dir_path,dirname + ".lmsp"),path.join(dir_path,"Projects"))
#     shutil.rmtree(path.join(dir_path,"Projects",dirname))


print(fileFolder1)