from cs50 import get_string
from sys import argv


def main():

    if len(argv) != 2 or len(argv) > 2:
        print("You can use 2 arguments not more, not less")
        exit(1)
        
    else:
        message = get_string("What message would you like to censor?\n")
        censor_message = ""
        
        if message.isalpha() or " " in message:
            banned_words = []
        
            with open(argv[1]) as file:
                for line in file:
                    banned_words.append(line.strip())
            
            message = message.split(" ")
        
            for word in message:
                if word == word.upper():
                    word = word.lower()
                    if word in banned_words:
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
	    
            print(censor_message)
        
        else:
            print("You can enter only words without punctuation marks")


if __name__ == "__main__":
    main()
