from sys import argv

def post_cesear():
	
	if len(argv) != 2 or len(argv) > 2:
		print("You can use 2 arguments not more, not less")
		exit(1)
	if argv[1].isdigit():
		if int(argv[1]) < 0:
			print("You can use only positive number")
			exit(1)
		else:
			alphavite = 'abcdefghijklmnopqrstuvwxyz'
			plaintext = str(input("plaintext: "))
			ciphertext = ""
	
			for char in plaintext:	
				if char in alphavite:
					offset = (alphavite.index(char) + int(argv[1])) % 26
					for charr in alphavite:
						if alphavite.index(charr) == offset:
							ciphertext += charr
				else:
					if char == char.upper():
						char = char.lower()
						if char in alphavite:
							offset = (alphavite.index(char) + int(argv[1])) % 26
							for charr in alphavite:
								if alphavite.index(charr) == offset:
									ciphertext += charr.upper()
					if char not in alphavite:
						ciphertext += char
			
	
			print("ciphertext: " + ciphertext + "\n")
	else:
		print("You can use only integral positive number")
		exit(1)
	
post_cesear()
