import os
path = r'./snake/sounds'
print(path)
tree = os.walk(path)
print(tree)

for _, _, files in tree:
    print(files)
    print(files[0])


