# qrcode.py

import segno

qrcode = segno.make_qr("https://www.linkedin.com/in/tomas-fryza-0b008753/")
qrcode.save(
    "qrcode.png",
    scale=1,
    border=0
)

from PIL import Image
im = Image.open('qrcode.png', 'r')
width, height = im.size
pixel_values = list(im.getdata())
print(pixel_values)

output_list = [1 if x == 0 else 0 for x in pixel_values]
print(output_list)
print(len(output_list))
