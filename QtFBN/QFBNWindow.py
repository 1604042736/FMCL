import platform

system = platform.system()
if system == 'Windows':
    from QtFBN.QFBNWindowWindows import QFBNWindowWindows
    QFBNWindow = QFBNWindowWindows
else:
    raise Exception(f"暂不兼容的系统:{system}")
