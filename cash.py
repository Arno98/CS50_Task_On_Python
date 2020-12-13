#owed = float(input("Change owed: "))
#coins = [0.25, 0.10, 0.05, 0.01]

"""
a = owed % coins[0]
if a < coins[0]:
	b = a % coins[1]
	if b < coins[1]:
		c = b % coins[2]
		if c < coins[2]:
			d = c % coins[3]
			if d < coins[3]:
				pass
"""

"""
coin = 0

while True:
	for coin in coins:
		mod = owed % coin
		countout = owed / coin
	
		if mod == 0:
			#не присваиваем остаток(mod) переменной здача(owed) (нам не дато отдавать то чего нет)
			#coin += contount
			#print(coin)
			#break
		
		else:#mod != 0
			#присваиваем остаток(mod) переменной здача(owed) (нам надо отдать здачу поттому что что она в остатке)
			#coin += int(countount)
			#continue

print(f'{mod:.3f}')
print(f"The number of coins: {countout}")
print("\n")
"""

#!!! -- 	Если здача больше 0.25 нам нет никакого смысла запрашивать что-то меньше 25, ведь мы можем разделить это число на 0.25 (мы это делаем пока остача(остаток здачи) не быль меньше 0.25 если это и она больше 0.10 значит остачу делим на 0.10 пока она не будет меньше 0.10 и если она меньше 0.10 но больше 0.05 делим ее 0.05 если она меньше 0.05 но больше 0.01 делим все остальное на 0.01 и заканчиваем цыкл 
#Также можно использовать функцию рекурсивную если чесло больше чем переданый аргумент делать что-то или вызывать рекурсию с параметром остатка от деления на число больше

#Ключ ко всему - функция с 4 условиями if arg > 25 if arg < 25 and arg >= 0.10 и т.д.

#если больше 25 мы должны предоставить полный спектр, если между 0.25 и 0.10 мы должны предоставить спектр без 0.25...если спектр между 0.05 и 0.01 все делим на 0.01 !
#можна подвигать список после каждой остачи чтобы первый элемент был отработан 
#уменьшаем период например надо дать 45 копеек здачи = 25 (0.25) если остача != 0 (значит есть что делить!) и записываем +=1 к coins остача будет 0.2 которую мы также делим    или     если mod > coins[1] мы присваиваем этот mod и потом записываем owed = mod b дальше так же
def owed_coin(owed, coins):
	
	if owed > 0.25:
		mod = owed % 0.25
		if mod == 0.00:
			coins += owed // 0.25
			print(coins)
		else:
			coins += owed // 0.25
			owed = mod
			owed_coin(owed, coins)
			
	elif owed < 0.25 and owed >=0.10:
		mod = owed % 0.10
		if mod == 0.00:
			coins += owed // 0.10
			print(coins)
		else:
			coins += owed // 0.10
			owed = mod
			owed_coin(owed, coins)
			
	elif owed < 0.10 and owed >= 0.05:
		mod = owed % 0.05
		if mod == 0.00:
			coins += owed // 0.05
			print(coins)
		else:
			coins += owed // 0.05
			owed = mod
			owed_coin(owed, coins)
			
	elif owed < 0.05 and owed >= 0.01:
		coins += owed // 0.01
		print(coins)
		
	else:
		coins += 1
		print(coins)
		
def __main__():
	while True:
		owed = input("Change owed: ")
		if owed.isalpha():
			continue
		else:
			owed = float(owed)
			if owed > 0:
				owed_coin(owed, 0)
				break
			else:
				continue
	
__main__()
print(0.15 % 0.05)
print(0.15 / 0.05)
