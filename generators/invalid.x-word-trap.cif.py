import sys

from num2words import num2words

def plnum(n):
   return num2words(n, lang="pl")

width, height = (1, 256 // 4)

header = f"""CIF: polish
WERSJA jeden
ROZMIAR szerokość: {plnum(width)}, wysokość: {plnum(height)}, bitów_na_piksel: trzydzieści dwa
METADANE test:description Catches decoders that try to use the lazy route of only checking certain letters.
"""

def sus_num(n):
   num = plnum(n)
   words = num.split(' ')
   for i in range(0, len(words)):
      word = words[i]
      if len(word) > 4:
         word = word[0:4] + 'x' * (len(word) - 4)
         words[i] = word
   return " ".join(words)

value = 0
for y in range(0, height):
   r, g, b, a = sus_num(value), sus_num(value + 1), sus_num(value + 2), sus_num(value + 3)
   header += f"{r}; {g}; {b}; {a}\n"
   value += 4

with open(sys.argv[1], "wb") as f:
   f.write(bytes(header, "UTF-8"))
