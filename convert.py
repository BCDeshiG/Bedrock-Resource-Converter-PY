import sys, json, os, zipfile, csv
from PIL import Image
from shutil import copyfile, copytree
import fixTextures

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

def checkMissing(missingFiles):
	if len(missingFiles) != 0: # Outputs names of missing textures to text file
		with open("missing.txt", "a") as missing:
			missing.writelines(missingFiles)

def startConversion(arg1, arg2):
	arg1 = parseZip(arg1)
	parseManifest(arg1, arg2)
	genFolders(arg2)
	parseTexts(arg1, arg2)
	if os.path.isfile("missing.txt"):
		os.remove("missing.txt")
	copyTextures(arg1, arg2)
	splitCompass(arg1, arg2, "watch_atlas.png")
	splitCompass(arg1, arg2, "compass_atlas.png")
	splitPaintings(arg1, arg2)
	fixTextures.fixes(arg1, arg2) # Fixes texture differences
	copyAnimations(arg2) # Copy over animation mcmeta files
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
	with zipfile.ZipFile(arg1 + fileExt, "r") as pack:
		pack.extractall(arg1)
	try:
		file = open(arg1 + "/manifest.json") # Checks if manifest in root folder
		file.close()
	except:
		for root, dirs, files in os.walk(arg1):
			if "manifest.json" in files: # Find manifest
				arg1 = root # Navigate to where manifest is
				return arg1
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
	outText = '{"pack": {"description": "' + desc + '",' + '"pack_format": 8}}'
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
		copyfile((arg1 + "/credits/end.txt"), (arg2 + "/assets/minecraft/texts/end.txt"))
	except FileNotFoundError:
		print("Could not find 'end.txt' file")
	try:
		with open(arg1 + "/splashes.json", "r", encoding="utf-8") as file:
			splashes = json.load(file)
	except:
		print("Unable to parse splashes")
		return
	outFile = open(arg2 + "/assets/minecraft/texts/splashes.txt", "w", encoding="utf-8")
	arr = splashes["splashes"]
	for i in range(len(arr)):
		outFile.write(arr[i]+"\n")
	outFile.close()

def copyTextures(arg1, arg2):
	missingFiles = []
	with open("textures.csv", "r") as csv_file: # Table of bedrock and java file names
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
	checkMissing(missingFiles)

def splitCompass(arg1, arg2, atlas):
	arg2 += "/assets/minecraft/textures/item/"
	try:
		im = Image.open(arg1 + "/textures/items/" + atlas)
		w,h = im.size
		for i in range(h//w):
			frame = im.crop((0, i*16, w, (i+1)*16))
			if i < 10:
				frame.save(arg2 + atlas.split("_")[0] + "_0" + str(i) + ".png")
			else:
				frame.save(arg2 + atlas.split("_")[0] + "_" + str(i) + ".png")
	except FileNotFoundError:
		print("Could not find '" + atlas + "' file")

def splitPaintings(arg1, arg2):
	arg1 += "/textures/painting/"
	arg2 += "/assets/minecraft/textures/painting/"
	# yh yh hardcoded paintings ik
	x16P = [
		"kebab.png", "aztec.png", "alban.png", "aztec2.png",
		"bomb.png", "plant.png", "wasteland.png"
	] 
	xWide = [
		"pool.png", "courbet.png", "sea.png",
		"sunset.png", "creebet.png"
	]
	xTall = ["wanderer.png", "graham.png"]
	x32P = [
		"match.png", "bust.png", "stage.png",
		"void.png", "skull_and_roses.png", "wither.png"
	]
	x64P = ["pointer.png", "pigscene.png", "burning_skull.png"]
	try:
		kz = Image.open(arg1 + "kz.png")
		splitPaintingsAux(kz, x16P, 0, 1, 1, arg2)
		splitPaintingsAux(kz, xWide, 2, 2, 1, arg2)
		splitPaintingsAux(kz, xTall, 4, 1, 2, arg2)
		splitPaintingsAux(kz, x32P, 8, 2, 2, arg2)
		splitPaintingsAux(kz, x64P, 12, 4, 4, arg2)
		w,h = kz.size
		kz.crop((0, (h//16)*6, (w//16)*4, (h//16)*8)).save(arg2 + "fighters.png")
		kz.crop(((w//16)*12, (h//16)*4, w, (h//16)*7)).save(arg2 + "skeleton.png")
		kz.crop(((w//16)*12, (h//16)*7, w, (h//16)*10)).save(arg2 + "donkey_kong.png")
	except FileNotFoundError:
		print("Could not find paintings texture")

def splitPaintingsAux(kz, arr, qtop, qw, qh, arg2): # uses quantum sizes
	q = kz.height//16 # quantum cell size
	# qtop is the starting y coord of the images
	# qw and qh are the width and height of each image
	top = q * qtop
	right = q * qw
	bottom = top + (qh * q)
	for i in range(len(arr)):
		im = kz.crop((qw*i*q, top, right+(qw*i*q), bottom))
		im.save(arg2 + arr[i])

def copyAnimations(arg2):
	arg2 += "/assets/minecraft/textures/"
	copytree("./mcmeta/block/", arg2 + "block/", dirs_exist_ok=True)
	copytree("./mcmeta/entity/", arg2 + "entity/", dirs_exist_ok=True)
	copytree("./mcmeta/misc/", arg2 + "misc/", dirs_exist_ok=True)

parseArgs()