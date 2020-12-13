def bleep():
	banned_words = ['fuck', 'cock', 'dick', 'niga']#file banned.txt
	
	message = str(input("Enter a message: "))
	censor_message = ""
	
	if message.isalpha() or " " in message:
	
		#message = message.lower()
	
		message = message.split(" ")
	
		for word in message:
			if word == word.upper():
				word = word.lower()
				if word in banned_words:
					#message[message.index(word)] = "*" * len(word)
					censor_message += ("*" * len(word)) + " "
				else:
					censor_message += word.upper() + " "
					
			elif word == word.title():
				word = word.lower()
				if word in banned_words:
					censor_message += ("*" * len(word)) + " "
				else:
					censor_message += word.title() + " "
			
			else:
				if word in banned_words:
					censor_message += ("*" * len(word)) + " "
				else:
					censor_message += word + " "
	
		#message = " ".join(message)
	
		#print(message)
		print(censor_message)
	
	else:
		print("False")
			
bleep()
