def algorithm_luna(num_card):
	num_card_l = list(num_card)
	int_num_card = []
	int_num_card_1 = []
	int_num_card_2 = []
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
		print("Valid card")
	else:
		print("Invalid card")


def credit_card():
	print("Payment card validity check\n")
	master_card = ['51', '52', '53', '54', '55']
	while True:
		user_num_card = input("Enter a num card: ")
		if len(user_num_card) == 15:
			if user_num_card[:2] == '34' or user_num_card[:2] == '37':
				print("AMEX\n")
				algorithm_luna(user_num_card)
			else:
				print ("Looks like you're trying to enter the American Express card number. We remind you that the numbers of these cards start with 34 or 37.\n")
				continue
		if len(user_num_card) == 16:
			if user_num_card[:2] in master_card:
				print("MASTERCARD\n")
				algorithm_luna(user_num_card)
			elif user_num_card[:1] == '4':
				print("VISA\n")
				algorithm_luna(user_num_card)
			else:
				print ("Looks like you're trying to enter the MasterCard or Visa card number. We remind you that the numbers of these cards start with 51/52/53/54/55(MasterCard) and with 4(Visa).\n")
				continue
		if len(user_num_card) == 13:
			if user_num_card[:1] == '4':
				print("VISA\n")
				algorithm_luna(user_num_card)
			else:
				print ("Looks like you're trying to enter the Visa card number. We remind you that the number of this card start with 4.\n")
				continue
		if len(user_num_card) < 13 or len(user_num_card) > 16:
			print("Looks like you're trying to enter less or more digits than the one on the payment card.")
			continue
credit_card()
