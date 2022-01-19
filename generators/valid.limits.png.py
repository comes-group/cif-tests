import os
import sys

from PIL import Image

for width in [300, 400, 500, 600, 700, 800, 900, 1000, 1255, 2000, 255000, 999999]:
   image = Image.new("RGB", (width, 1))

   for x in range(0, width):
      image.putpixel((x, 0), (3, 0, 3))

   name = f"limits{width}.png"
   path = os.path.join(sys.argv[1], name)
   image.save(path, format="PNG")
