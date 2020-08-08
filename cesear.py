def cesear():
	key = 3
	alphavite = 'abcdefghijklmnopqrstuvwxyz'
	open_text = "Hello, my Cousin! I have a good news. I marry on Elizabeth!"
	closed_text = ""
	
	for char in open_text:	
		if char in alphavite:
			offset = (alphavite.index(char) + key) % 26
			for charr in alphavite:
				if alphavite.index(charr) == offset:
					closed_text += charr
		else:
			if char == char.upper():
				char = char.lower()
				if char in alphavite:
					offset = (alphavite.index(char) + key) % 26
					for charr in alphavite:
						if alphavite.index(charr) == offset:
							closed_text += charr.upper()
			closed_text += char
			
	
	print(open_text)
	print(closed_text)
	
cesear()
