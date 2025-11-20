"""
file = open('data1.txt', 'r')
print(file)
lineas = file.readlines()
print(lineas)
file.close()"""

"""with open('data2.txt', 'r') as archivo:
    lineas = archivo.readlines()
    #print(lineas)
#print(lineas)
for l in lineas:
    print(l)"""
"""with open('data2.txt', 'r') as archivo:
    contenido = archivo.read()
    lineas = contenido.split('\n')
    print(lineas)"""
"""with open('data2.txt', 'r') as archivo:
    contenido = archivo.read()
    lineas = contenido.split('\n')
    poss = archivo.tell()
    print(poss)
    print('el archivo tiene {0} caracteres de longitud'.format(poss))"""
"""with open('data2.txt', 'r') as archivo:
    archivo.seek(7)
    poss = archivo.tell()
    print(poss)
    contenido = archivo.read()
    lineas = contenido.split('\n')
    print(lineas)"""
"""with open('data2.txt', 'r') as archivo:
    siguientes4 = archivo.read(4)
    print(siguientes4)    """
with open('data2.txt', 'r') as archivo:
    print(type(archivo.read()))

with open('data2.txt', 'rb') as archivo:
    print(type(archivo.read()))