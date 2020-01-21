import sys
import json
import os
import zipfile
from shutil import copyfile

def parseArgs():
	if len(sys.argv) == 1: # No arguments supplied
		arg1 = input("Enter location of bedrock texture pack: ")
		arg2 = input("Enter location of destination folder: ")
		startConversion(arg1, arg2)
	else:
		if sys.argv[1] == "-h" or sys.argv[1] == "--help":
			print("\nUsage: " + sys.argv[0] + " [-h] PACK DEST")
			print("Convert MC Bedrock pack to Java")
			print("\nArguments:")
			print("PACK		Location of Texture folder/zip/mcpack file")
			print("DEST		Destination folder of converted pack")
			print("-h, --help	Displays this message (ofc)")
			print("\nExample: " + sys.argv[0] + " foo.mcpack 'C:/oofPack'")
		elif len(sys.argv) != 3:
			print("YOU TWONK")
		else:
			startConversion(sys.argv[1], sys.argv[2])

def startConversion(arg1, arg2):
	arg1 = parseZip(arg1)
	parseManifest(arg1, arg2)
	#parseSplashes(arg1, arg2)
	#copyfile((arg1 + "/end.txt"), (arg2 + "/assets/minecraft/texts/end.txt")) # FIXME add to main copy function

def parseZip(arg1):
	if arg1.lower().endswith(".zip"):
		fileExt = ".zip"
	elif arg1.lower().endswith(".mcpack"):
		fileExt = ".mcpack"
	else:
		return arg1
	arg1 = os.path.splitext(arg1)[0]
	with zipfile.ZipFile(arg1 + fileExt,"r") as pack:
		pack.extractall(arg1)
	try:
		file = open(arg1 + "/manifest.json") # Checks if manifest in root folder
		file.close()
	except:
		for root, dirs, files in os.walk(arg1):
			if "manifest.json" in files: # Find manifest
				arg1 = root + "\\" # Navigate to where manifest is
	return arg1

def parseManifest(arg1, arg2):
	try:
		with open(arg1 + "/manifest.json", "r") as file:
			manifest = json.load(file)
			head = manifest["header"]
			desc = head["description"]
	except:
		print("Pack does not exist or is invalid")
		exit()
	outText = '{"pack": {"description": "'
	outText += desc + '",'
	outText += '"pack_format": 5}}'
	try:
		os.mkdir(arg2)
		file = open(arg2 + "/pack.mcmeta", "x") # Create new file if it donesn't already exist
		file.write(outText)
		file.close()
	except:
		print("Folder already exists or was unable to be created")
		exit()

def parseSplashes(arg1, arg2):
	with open(arg1 + "/splashes.json", "r") as file:
		splashes = json.load(file)
	outFile = open(arg2 + "/assets/minecraft/texts/splashes.txt", "w") # FIXME Make directories 1st 
	arr = splashes["splashes"]
	for i in range(len(arr)):
		outFile.write(arr[i]+"\n")
	outFile.close()

parseArgs()