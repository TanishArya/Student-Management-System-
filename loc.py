from PIL import ImageTk
import PIL
n = open('test.txt', 'w')
n.write(PIL.ImageTk.__file__)
print((PIL.ImageTk.__file__))
n.close
