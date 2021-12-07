from PIL import Image
import os

def fixBeds(arg1, arg2): # FIXME Bed Feet
	arg1 += "/textures/entity/bed/"
	arg2 += "/assets/minecraft/textures/entity/bed/"
	try:
		bedNames = os.listdir(arg1)
		for i in range(len(bedNames)):
			bedTex = Image.open(arg1 + bedNames[i])
			q = bedTex.height // 64 # Resize scale

			temp = bedTex.crop((0, 22*q, 44*q, 50*q))
			bedCopy = bedTex.copy()
			bedCopy.paste(temp, (0, 28*q)) # Shift down 6 pixels
			temp = Image.new("RGBA", (44*q, 6*q))
			bedCopy.paste(temp, (0, 22*q)) # Delete old part

			temp = bedTex.crop((22*q, 0, 38*q, 6*q))
			bedCopy.paste(temp, (22*q, 22*q)) # Shift down into gap
			temp = Image.new("RGBA", (16*q, 6*q))
			bedCopy.paste(temp, (22*q, 0)) # Delete old part

			if bedNames[i][:6] == "silver":
				bedNames[i] = "light_gray.png"

			try:
				bedCopy.save(arg2 + bedNames[i])
			except:
				print("Could not save '" + bedNames[i] + "' file")
	except:
		print("Could not load bed textures")
		return

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

def fixHoglins(arg1, arg2, hog):
	arg1 += "/textures/entity/" + os.path.splitext(hog)[0] + "/"
	arg2 += "/assets/minecraft/textures/entity/hoglin/"
	try:
		hoglin = Image.open(arg1 + hog)
		w,h = hoglin.size
		q = w//128 # Resize scale
		tusk = hoglin.crop((1*q, 13*q, 9*q, 26*q))
		hoglin.paste(tusk, (10*q, 13*q))
		hoglin.save(arg2 + hog)
	except FileNotFoundError:
		print("Could not find '" + hog + "' file")

def fixFoxes(arg1, arg2, fox):
	inn = arg1 + "/textures/entity/fox/"
	out = arg2 + "/assets/minecraft/textures/entity/fox/"
	try:
		im = Image.open(inn + fox)
		w,h = im.size
		q = w//64 # Resize scale
		woke = Image.new("RGBA", (48*q, 32*q)) # Awake texture
		temp = im.crop((28*q, 0, 46*q, 14*q)) # Tail
		woke.paste(temp, (30*q, 0))
		temp = im.crop((30*q, 15*q, 54*q, h)) # Body
		woke.paste(temp, (24*q, 15*q))
		temp = im.crop((22*q, 24*q, 30*q, h)) # Foot
		woke.paste(temp, (4*q, 24*q))
		temp = im.crop((14*q, 24*q, 22*q, h)) # Other Foot
		woke.paste(temp, (13*q, 24*q))
		temp = im.crop((0, 24*q, 14*q, 29*q)) # Nose
		woke.paste(temp, (6*q, 18*q))
		temp = im.crop((0, 0, 6*q, 3*q)) # Ear
		woke.paste(temp, (8*q, q))
		temp = im.crop((22*q, 0, 28*q, 3*q)) # Other Ear
		woke.paste(temp, (15*q, q))
		slep = woke.copy() # Asleep texture
		temp = im.crop((0, 0, 28*q, 12*q)) # Awake Head
		woke.paste(temp, (q, 5*q))
		temp = im.crop((0, 12*q, 28*q, 24*q)) # Asleep Head
		slep.paste(temp, (q, 5*q))
		# Fix extra ears from pasting head
		temp = Image.new("RGBA", (6*q, 3*q))
		woke.paste(temp, (q, 5*q))
		woke.paste(temp, (23*q, 5*q))
		slep.paste(temp, (q, 5*q))
		slep.paste(temp, (23*q, 5*q))
		# Save images
		if fox == "arctic_fox.png":
			fox = "snow_fox.png"
		woke.save(out + fox)
		fox = os.path.splitext(fox)[0] + "_sleep.png"
		slep.save(out + fox)
	except FileNotFoundError:
		print("Could not find '" + fox + "' file")

def fixDog(arg1, arg2):
	inn = arg1 + "/textures/entity/wolf/"
	out = arg2 + "/assets/minecraft/textures/entity/wolf/"
	try:
		dog = Image.open(inn + "wolf_tame.tga")
		w,h = dog.size
		q = w//64 # Resize scale
		mask = Image.open(inn + "wolf.png").getchannel("A")
		dog.putalpha(mask)
		dog.save(out + "wolf_tame.png")
		collar = dog.crop((28*q, 0, 36*q, 7*q))
		temp = Image.new("RGBA", (6*q, 5*q)) # Delete middle
		collar.paste(temp, (q, q))
		temp = Image.new("RGBA", (w,h))
		temp.paste(collar, (28*q, 0))
		temp.save(out + "wolf_collar.png")
	except FileNotFoundError:
		print("Could not find wolf texture")
	except ValueError:
		print("Please ensure that the wolf texture is in 'RGBA' format")

def fixCat(arg1, arg2):
	inn = arg1 + "/textures/entity/cat/"
	out = arg2 + "/assets/minecraft/textures/entity/cat/cat_collar.png"
	try:
		catArr = os.listdir(inn) # List of cat textures
		tameArr = [] # List of tamed cat textures
		for i in range(len(catArr)):
			if "tame" in catArr[i]:
				tameArr.append(catArr[i])
		tame = Image.open(inn + tameArr[0]) # Doesn't need to be specific
		w,h = tame.size
		q = w//64 # Resize scale
		collar = Image.new("RGBA", (w,h))
		part1 = (20*q, 6*q, 24*q, 7*q)
		collar.paste(tame.crop(part1), part1)
		part2 = (26*q, 3*q, 30*q, 4*q)
		collar.paste(tame.crop(part2), part2)
		part3 = (32*q, 6*q, 40*q, 7*q)
		collar.paste(tame.crop(part3), part3)
		collar.save(out)
	except FileNotFoundError:
		print("Could not find cat texture")

def fixAzalea(arg1, arg2, bush):
	inn = arg1 + "/textures/blocks/"
	out = arg2 + "/assets/minecraft/textures/block/"
	tup = (1,0,0,0,1,-1) # Translate 0 across and 1 pixels down (elements 2 and 5)
	try:
		im = Image.open(inn + bush)
		im = im.transform(im.size, Image.AFFINE, tup)
		im.save(out + bush)
	except FileNotFoundError:
		print("Could not find " + bush + " file")

def fixes(arg1, arg2):
	fixBeds(arg1, arg2)
	fixChests(arg1, arg2, "double_normal.png")
	fixChests(arg1, arg2, "trapped_double.png")
	fixZombies(arg1, arg2, "zombie.png")
	fixZombies(arg1, arg2, "husk.png")
	fixDrowned(arg1, arg2)
	fixSheep(arg1, arg2)
	fixHoglins(arg1, arg2, "hoglin.png")
	fixHoglins(arg1, arg2, "zoglin.png")
	fixFoxes(arg1, arg2, "fox.png")
	fixFoxes(arg1, arg2, "arctic_fox.png")
	fixDog(arg1, arg2)
	fixCat(arg1, arg2)
	fixAzalea(arg1, arg2, "potted_azalea_bush_side.png")
	fixAzalea(arg1, arg2, "potted_flowering_azalea_bush_side.png")