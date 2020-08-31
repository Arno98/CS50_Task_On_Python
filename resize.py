from PIL import Image

def resize():
	image = Image.open('d:\python_work\python_project\CS50 on Python\clue.bmp')
	width, height = image.size
	print("Изображение имеет размер " + str(width) + " на " + str(height) + " пикселей.")
	k = input("Вы хотите увеличить или уменьшить изображение ('+' для увеличения, '-' для уменьшения ? ")
	if k == '+':
		k_1 = int(input("Во сколько раз вы хотите увеличить изображение ? "))
		width *= k_1
		height *= k_1
		resize_image = image.resize((width, height), Image.ANTIALIAS)
		resize_image.save("result_1.jpg", "JPEG")
		resize_image.show()
	if k == '-':
		k_1 = int(input("Во сколько раз вы хотите увеличить изображение ? "))
		width //= k_1
		height //= k_1
		resize_image = image.resize((width, height), Image.ANTIALIAS)
		resize_image.save("result_0.jpg", "JPEG")
		resize_image.show()
resize()
 
