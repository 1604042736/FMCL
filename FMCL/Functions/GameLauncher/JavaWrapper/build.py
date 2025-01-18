import os
import shutil

os.system(
    'gcc -shared -o ../JavaWrapper.dll -I"%JAVA_HOME%\include" -I"%JAVA_HOME%\include\win32" Wrapper.c'
)
os.system("gradle build")
os.system("gradle shadowJar")
shutil.copy("build/libs/JavaWrapper-all.jar", "..")
if os.path.exists("../JavaWrapper.jar"):
    os.remove("../JavaWrapper.jar")
os.rename("../JavaWrapper-all.jar", "../JavaWrapper.jar")
