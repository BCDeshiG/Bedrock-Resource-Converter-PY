import sys
import json
import os

def parseArgs():
	if len(sys.argv) == 1: # No arguments supplied
		menu()
	else:
		if sys.argv[1] == "-h" or sys.argv[1] == "--help":
			print("\nUsage: " + sys.argv[0] + " [-h] PACK DEST")
			print("Convert MC Bedrock pack to Java")
			print("\nArguments:")
			print("PACK		Location of Texture folder/mcpack file") # FIXME Implement mcpack support
			print("DEST		Destination folder of converted pack")
			print("-h, --help	Displays this message (ofc)")
			print("\nExample: " + sys.argv[0] + " foo.mcpack 'C:/oofPack'")
		elif len(sys.argv) != 3:
			print("YOU TWONK")
		else:
			#startConversion(sys.argv[1], sys.argv[2])
			parseManifest(sys.argv[1], sys.argv[2])

def menu():
	arg1 = input("Enter location of bedrock texture pack: ")
	arg2 = input("Enter location of destination folder: ")
	#startConversion(sys.argv[1], sys.argv[2])
	parseManifest(arg1, arg2)

def startConversion(arg1, arg2):
	# Placeholder to confirm args
	print("arg1: " + arg1)
	print("arg2: " + arg2)

def parseManifest(arg1, arg2):
	with open(arg1 + "/manifest.json", "r") as file:
		manifest = json.load(file)
		head = manifest["header"]
		desc = head["description"]
	outText = '{"pack": {"description": "'
	outText += desc + '",'
	outText += '"pack_format": 5}}'
	try:
		os.mkdir(arg2)
		file = open(arg2 + "/pack.mcmeta", "x") # Create new file if it donesn't already exist
		file.write(outText)
		file.close()
	except:
		confirm = input("Existing Pack detected, are you sure you want to overwrite it? (Y/N): ")
		if confirm == "Y" or confirm == "y":
			file = open(arg2 + "/pack.mcmeta", "w")
			file.write(outText)
			file.close()


parseArgs()