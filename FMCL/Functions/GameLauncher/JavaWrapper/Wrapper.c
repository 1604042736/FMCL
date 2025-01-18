#include <jni.h>
#include <windows.h>

JNIEXPORT jstring JNICALL
Java_fmcl_javawrapper_Wrapper_getCommandLine(JNIEnv *env, jclass clazz)
{
    // 获取命令行
    LPWSTR cmdLine = GetCommandLineW();
    if (cmdLine == NULL)
    {
        return NULL;
    }

    // 计算长度
    int len = lstrlenW(cmdLine);

    // 将宽字符转换为 UTF-8 字符串
    int utf8Len =
        WideCharToMultiByte(CP_UTF8, 0, cmdLine, len, NULL, 0, NULL, NULL);
    char *utf8Str = (char *)malloc(utf8Len + 1);
    WideCharToMultiByte(CP_UTF8, 0, cmdLine, len, utf8Str, utf8Len, NULL, NULL);
    utf8Str[utf8Len] = '\0';

    // 创建 Java 字符串
    jstring result = (*env)->NewStringUTF(env, utf8Str);

    // 释放资源
    free(utf8Str);

    return result;
}