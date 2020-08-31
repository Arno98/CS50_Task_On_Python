from PIL import Image, ImageDraw
img = Image.open('d:\python_work\python_project\CS50 on Python\clue.bmp')
draw = ImageDraw.Draw(img)
height = img.size[1]
width = img.size[0]
pix = img.load()
pix_avg_list = []

for x in range(width):
	for y in range(height):
		r, g, b = pix[x, y]
		if r < 255:
			draw.point((x, y), (0, 0, 0))
img.save("result.jpg", "JPEG")
