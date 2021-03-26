# pip install Pillow
from PIL import Image, ImageDraw, ImageFont

image_size_xy = (200, 200)
string = 'stun32165'

image = Image.new("RGB", image_size_xy, 'white')
font = ImageFont.truetype("arial.ttf", 37)
drawer = ImageDraw.Draw(image)

center_image_xy = (image_size_xy[0] // 2, image_size_xy[1] // 2)
drawer.multiline_text(center_image_xy, string, font=font, fill='black', anchor='mm')

image.save('temp_img.png')
