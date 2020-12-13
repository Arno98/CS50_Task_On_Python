def ceasar():
	key = int(input("Enter a key: "))
	alphavite = 'abcdefghijklmnopqrstuvwxyz'
	open_text = str(input("Enter a text: "))
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
							
			if char not in alphavite:
				closed_text += char
			
	
	print(open_text)
	print(closed_text)
	
ceasar()
