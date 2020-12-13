def vigenere():
	alphavite = 'abcdefghijklmnopqrstuvwxyz'
	alphavite_2 = alphavite.upper()
	word_key = str(input("Word key: "))
	open_text = str(input("Open text: "))
	closed_text = ''
	
	char_open_text = 0
	char_word_key = 0
	
	while char_open_text != len(open_text):
		
		if open_text[char_open_text] not in alphavite and open_text[char_open_text] not in alphavite_2:
			closed_text += open_text[char_open_text]
			char_open_text += 1
			
		else:
			if open_text[char_open_text] in alphavite:
				offset = (alphavite.index(open_text[char_open_text]) + alphavite.index(word_key[char_word_key])) % 26
				for char in alphavite:
					if alphavite.index(char) == offset:
						closed_text += char
				char_open_text += 1
				char_word_key += 1
			
				if char_word_key == len(word_key):
					char_word_key -= len(word_key)
					
			elif open_text[char_open_text] in alphavite_2:
				offset = (alphavite_2.index(open_text[char_open_text]) + alphavite.index(word_key[char_word_key])) % 26
				for char in alphavite_2:
					if alphavite_2.index(char) == offset:
						closed_text += char
				char_open_text += 1
				char_word_key += 1
			
				if char_word_key == len(word_key):
					char_word_key -= len(word_key)
					
	print(open_text)
	print(closed_text)	
		
vigenere()
