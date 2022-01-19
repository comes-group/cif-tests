import sys

from PIL import Image

width, height = 8, 8

image = Image.new("RGBA", (8, 8))
image_data = image.getdata()

value = 0
for y in range(0, height):
   for x in range(0, width):
      image.putpixel((x, y), (value, value + 1, value + 2, value + 3))
      value += 4

image.save(sys.argv[1], format="PNG")
