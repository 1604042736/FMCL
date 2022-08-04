import platform

system = platform.system()
print(system)
if system == 'Windows':
    from QtFBN.QFBNWindowWindows import QFBNWindowWindows
    QFBNWindow = QFBNWindowWindows
else:
    from QtFBN.QFBNWindowDefault import QFBNWindowDefault
    QFBNWindow = QFBNWindowDefault
