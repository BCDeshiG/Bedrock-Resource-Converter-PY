import sys, json, os, zipfile, csv
from PIL import Image
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
	genFolders(arg2)
	parseTexts(arg1, arg2)
	copyBlocks(arg1, arg2)
	copyBreak(arg1, arg2)
	print("\nConversion Complete")
	print("Please see 'fixme.txt' for textures that need attention")
	if os.path.isfile("missing.txt"):
		print("\nSome files were missing from your texture pack and were not included.")
		print("Please see the generated 'missing.txt' file for details.")

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
		file = open(arg2 + "/pack.mcmeta", "x") # Create new file if it doesn't already exist
		file.write(outText)
		file.close()
	except:
		print("Folder already exists or was unable to be created")
		exit()

def genFolders(arg2):
	with open("paths.txt", "r") as file:
		for line in file:
			os.makedirs(arg2 + line.rstrip())

def parseTexts(arg1, arg2):
	try:
		with open(arg1 + "/splashes.json", "r") as file:
			splashes = json.load(file)
	except:
		print("Unable to parse splashes")
		return
	outFile = open(arg2 + "/assets/minecraft/texts/splashes.txt", "w")
	arr = splashes["splashes"]
	for i in range(len(arr)):
		outFile.write(arr[i]+"\n")
	outFile.close()
	try:
		copyfile((arg1 + "/credits/end.txt"), (arg2 + "/assets/minecraft/texts/end.txt"))
	except FileNotFoundError:
		print("Could not find 'end.txt' file")

def copyBlocks(arg1, arg2):
	arg1 = arg1 + "/textures/blocks/"
	arg2 = arg2 + "/assets/minecraft/textures/block/"
	missingFiles = []
	with open("diff.csv", "r") as csv_file: # Files differently named to their java counterpart
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			try:
				if row[0].lower().endswith(".tga"):
					Image.open(arg1 + row[0]).save(arg2 + row[1])
				else:
					copyfile((arg1 + row[0]), (arg2 + row[1]))
			except FileNotFoundError:
				missingFiles.append(row[0] + "\n")
				continue
	with open("same.txt", "r") as text_file: # Files with same name as their java counterpart
		for line in text_file:
			try:
				if row[0].lower().endswith(".tga"):
					Image.open(arg1 + line.rstrip()).save(arg2 + line.rstrip())
				else:
					copyfile((arg1 + line.rstrip()), (arg2 + line.rstrip()))
			except FileNotFoundError:
				missingFiles.append(line)
				continue
	if len(missingFiles) != 0: # Outputs names of missing textures to text file
		with open("missing.txt", "w") as missing:
			missing.writelines(missingFiles)


def copyBreak(arg1, arg2):
	arg1 = arg1 + "/textures/environment/"
	arg2 = arg2 + "/assets/minecraft/textures/block/"
	missingFiles = []
	for i in range(10):
		name = "destroy_stage_" + str(i) + ".png"
		try:
			copyfile((arg1 + name), (arg2 + name))
		except FileNotFoundError:
			missingFiles.append(name + "\n")
			continue
	if len(missingFiles) != 0: # Outputs names of missing textures to text file
		with open("missing.txt", "a") as missing:
			missing.writelines(missingFiles)


parseArgs()