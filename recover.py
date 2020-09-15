def check_header(block_of_bytes):
	buffer_4_bytes = []
	for b in block_of_bytes[:4]:
		b = hex(b)
		buffer_4_bytes.append(b)
	if buffer_4_bytes[0] == '0xff' and buffer_4_bytes[1] == '0xd8' and buffer_4_bytes[2] == '0xff':
		return True
		
with open('recover/card.raw', "rb+") as f:
	image_number = 0
	while True:
		block_of_bytes = f.read(512)
		if len(block_of_bytes) < 512:
			break
		while check_header(block_of_bytes):
			image_number += 1
			with open('recover/image_' +  str(image_number) + '.jpg', 'wb+') as pict:
				pict.write(block_of_bytes)
				while True:
					block_of_bytes = f.read(512)
					if check_header(block_of_bytes) or len(block_of_bytes) < 512:
						break
					pict.write(block_of_bytes)
