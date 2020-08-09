def vigenere():
	alphavite = 'abcdefghijklmnopqrstuvwxyz'
	word_key = 'abc'
	open_text = 'hello!'
	closed_text = ''
	
	char_open_text = 0
	char_word_key = 0
	
	while char_open_text != len(open_text):
		for c in open_text:
			if c in alphavite:
				offset = (alphavite.index(open_text[char_open_text]) + alphavite.index(word_key[char_word_key])) % 26
				for char in alphavite:
					if alphavite.index(char) == offset:
						closed_text += char
				char_open_text += 1
				char_word_key += 1
				if char_word_key == len(word_key):
					char_word_key -= len(word_key)
			
	print(open_text)
	print(closed_text)	
		
vigenere()
