def algorithm_luna(num_card):
	num_card_l = list(num_card)
	int_num_card = []
	int_num_card_1 = []
	int_num_card_2 = []
	master_card = ['51', '52', '53', '54', '55']
	for x in num_card_l:
		int_num_card.append(int(x))
	int_num_card.reverse()
	for x in int_num_card[1:len(int_num_card):2]:
		x = x * 2
		if x > 9:
			x = list(str(x))
			for y in x:
				int_num_card_1.append(int(y))
		else:
			int_num_card_1.append(x)
	for x in int_num_card[0:len(int_num_card):2]:
		int_num_card_2.append(x)
	add = sum(int_num_card_1) + sum(int_num_card_2)
	if add % 10 == 0:
		if len(num_card) == 15:
			if num_card[:2] == '34' or num_card[:2] == '37':
				print("AMEX\n")
		if len(num_card) == 16:
			if num_card[:2] in master_card:
				print("MASTERCARD\n")
			elif num_card[:1] == '4':
				print("VISA\n")
		if len(num_card) == 13:
			if num_card[:1] == '4':
				print("VISA\n")
	elif add % 10 != 0:
		print("INVALID\n")

def credit_card():
	while True:
		user_num_card = input("Number: ")
		if user_num_card.isdigit():
				algorithm_luna(user_num_card)
		else:
			continue
		
credit_card()
