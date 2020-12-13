while True:
	height = input("Height: ")
	if height.isdigit():
		height = int(height)
		if height > 0 and height <= 8:
			for x in range(height):
				print((" " * (height - (x+1))) + ("#" * (x+1)))
			break
