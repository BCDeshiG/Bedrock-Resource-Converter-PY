from PIL import Image
import os

def fixBeds(arg1, arg2): # FIXME Bed Feet
	arg1 += "/textures/entity/bed/"
	arg2 += "/assets/minecraft/textures/entity/bed/"
	beds = []
	try:
		bedNames = os.listdir(arg1)
		for i in range(len(bedNames)):
			beds.append(Image.open(arg1 + bedNames[i]))
	except:
		print("Could not load bed textures")
		return
	q = beds[0].height // 64 # Resize scale
	for i in range(len(beds)):
		temp = beds[i].crop((0, 22*q, 44*q, 50*q))
		bedCopy = beds[i].copy()
		bedCopy.paste(temp, (0, 28*q)) # Shift down 6 pixels
		temp = Image.new("RGBA", (44*q, 6*q))
		bedCopy.paste(temp, (0, 22*q)) # Delete old part

		temp = beds[i].crop((22*q, 0, 38*q, 6*q))
		bedCopy.paste(temp, (22*q, 22*q)) # Shift down into gap
		temp = Image.new("RGBA", (16*q, 6*q))
		bedCopy.paste(temp, (22*q, 0)) # Delete old part
		try:
			bedCopy.save(arg2 + bedNames[i])
		except:
			print("Could not save '" + bedNames[i] + "' file")

def fixChests(arg1, arg2, chest):
	arg1 += "/textures/entity/chest/"
	arg2 += "/assets/minecraft/textures/entity/chest/"
	chestType = chest.replace("double","")
	chestType = chestType.replace("_","")
	chestType = chestType.replace(".png","")
	try:
		im = Image.open(arg1 + chest)
		w,h = im.size
		left = Image.new("RGBA", (w//2, h))
		right = Image.new("RGBA", (w//2, h))
		q = h//64 # Resize scale

		# Right side of chest
		temp = im.crop((0, 0, 29*q, 43*q))
		right.paste(temp, (0, 0))
		temp = right.crop((14*q, 0, 29*q, 14*q))
		right.paste(temp, (29*q, 0))
		temp = right.crop((14*q, 19*q, 29*q, 33*q))
		right.paste(temp, (29*q, 19*q))
		temp = im.crop((44*q, 0, 59*q, 14*q))
		right.paste(temp, (14*q, 0))
		temp = im.crop((44*q, 19*q, 59*q, 33*q))
		right.paste(temp, (14*q, 19*q))
		temp = im.crop((73*q, 14*q, 88*q, 19*q))
		right.paste(temp, (43*q, 14*q))
		temp = im.crop((73*q, 33*q, 88*q, 43*q))
		right.paste(temp, (43*q, 33*q))
		right.save(arg2 + chestType + "_right.png")

		# Left side of chest
		temp = im.crop((0, 0, 6*q, 5*q))
		left.paste(temp, (0, 0))
		temp = im.crop((29*q, 14*q, 73*q, 19*q))
		left.paste(temp.rotate(180), (14*q, 14*q))
		temp = im.crop((29*q, 33*q, 73*q, 43*q))
		left.paste(temp.rotate(180), (14*q, 33*q))
		temp = im.crop((29*q, 19*q, 44*q, 33*q))
		left.paste(temp, (29*q, 19*q))
		temp = im.crop((59*q, 19*q, 74*q, 33*q))
		left.paste(temp, (14*q, 19*q))
		temp = im.crop((59*q, 0, 74*q, 14*q))
		left.paste(temp, (14*q, 0))
		temp = im.crop((29*q, 0, 44*q, 14*q))
		left.paste(temp, (29*q, 0))
		temp = Image.new("RGBA", (15*q, 14*q))
		left.paste(temp, (44*q, 0))
		left.paste(temp, (44*q, 19*q))
		left.save(arg2 + chestType + "_left.png")
	except:
		print("Could not load '" + chest + "' file")

def fixZombies(arg1, arg2, zombie):
	arg1 += "/textures/entity/zombie/"
	arg2 += "/assets/minecraft/textures/entity/zombie/"
	try:
		im = Image.open(arg1 + zombie)
		w,h = im.size
		im.crop((0, 0, w, h*2)).save(arg2 + zombie)
	except FileNotFoundError:
		print("Could not find '" + zombie + "' file")

def fixPiglins(arg1, arg2, inn, out):
	arg1 += "/textures/entity/piglin/"
	arg2 += "/assets/minecraft/textures/entity/piglin/"
	try:
		piglin = Image.open(arg1 + inn)
		w,h = piglin.size
		q = w//128 # Resize scale
		ear1 = piglin.crop((57*q, 22*q, 67*q, 31*q))
		ear2 = piglin.crop((57*q, 38*q, 67*q, 47*q))
		piglin.paste(ear1, (39*q, 6*q))
		piglin.paste(ear2, (51*q, 6*q))
		temp = Image.new("RGBA", (10*q, 9*q)) # Delete old bits
		piglin.paste(temp, (57*q, 22*q))
		piglin.paste(temp, (57*q, 38*q))
		piglin.crop((0, 0, w//2, h//2)).save(arg2 + out)
	except FileNotFoundError:
		print("Could not find '" + inn + "' file")

def fixDrowned(arg1, arg2):
	inn = arg1 + "/textures/entity/zombie/drowned.tga"
	out = arg2 + "/assets/minecraft/textures/entity/zombie/"
	try:
		drowned = Image.open(inn)
		w,h = drowned.size
		q = w//64 # Resize scale
		drowned.save(out + "drowned.png")
		outer = Image.new("RGBA", (w, h))
		temp = drowned.crop((32*q, 0, w, 16*q)) # Drowned head
		outer.paste(temp, (0, 0))
		temp = drowned.crop((0, 32*q, 56*q, 48*q)) # Drowned upper body
		outer.paste(temp, (0, 16*q))
		temp = drowned.crop((0, 48*q, 16*q, w)) # Drowned lower left
		outer.paste(temp, (16*q, 48*q))
		temp = drowned.crop((48*q, 48*q, w, w)) # Drowned lower right
		outer.paste(temp, (32*q, 48*q))
		outer.save(out + "drowned_outer_layer.png")
	except FileNotFoundError:
		print("Could not find drowned texture")

def fixSheep(arg1, arg2):
	inn = arg1 + "/textures/entity/sheep/sheep.tga"
	out = arg2 + "/assets/minecraft/textures/entity/sheep/"
	try:
		im = Image.open(inn)
		w,h = im.size
		im.crop((0, 0, w, h//2)).save(out + "sheep.png")
		im.crop((0, h//2, w, h)).save(out + "sheep_fur.png")
	except FileNotFoundError:
		print("Could not find sheep texture")

def fixes(arg1, arg2):
	fixBeds(arg1, arg2)
	fixChests(arg1, arg2, "double_normal.png")
	fixChests(arg1, arg2, "trapped_double.png")
	fixZombies(arg1, arg2, "zombie.png")
	fixZombies(arg1, arg2, "husk.png")
	fixPiglins(arg1, arg2, "piglin.png", "piglin.png")
	fixPiglins(arg1, arg2, "zombie_piglin.png", "zombified_piglin.png")
	fixDrowned(arg1, arg2)
	fixSheep(arg1, arg2)