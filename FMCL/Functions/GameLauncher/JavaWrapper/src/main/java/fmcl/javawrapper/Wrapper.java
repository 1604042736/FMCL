//参考https://github.com/00ll00/java_launch_wrapper
package fmcl.javawrapper;

import static java.lang.System.arraycopy;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

import com.google.gson.*;

class ClassPathInjector {

    private static final int JAVA_VER;

    static {
        String ver = System.getProperty("java.specification.version");
        int pos = ver.indexOf('.');
        if (pos == -1) {
            JAVA_VER = Integer.parseInt(ver);
        } else {
            JAVA_VER = Integer.parseInt(ver.substring(pos + 1));
        }
    }

    public static void appendClassPath(String path) throws MalformedURLException, InvocationTargetException,
            NoSuchMethodException, IllegalAccessException, ClassNotFoundException, NoSuchFieldException {
        if (JAVA_VER <= 8) {
            appendClassPath8(path);
        } else {
            appendClassPath9(path);
        }
    }

    private static void appendClassPath8(String path)
            throws NoSuchMethodException, MalformedURLException, InvocationTargetException, IllegalAccessException {
        URLClassLoader classLoader = (URLClassLoader) ClassLoader.getSystemClassLoader();
        Method add = URLClassLoader.class.getDeclaredMethod("addURL", URL.class);
        add.setAccessible(true);
        add.invoke(classLoader, new File(path).toURI().toURL());
    }

    private static void appendClassPath9(String path) throws ClassNotFoundException, NoSuchFieldException,
            NoSuchMethodException, IllegalAccessException, MalformedURLException, InvocationTargetException {
        ClassLoader classLoader = ClassLoader.getSystemClassLoader();
        Class<?> clazz = classLoader.loadClass("jdk.internal.loader.BuiltinClassLoader");
        Class<?> ucpCls = classLoader.loadClass("jdk.internal.loader.URLClassPath");
        Field ucp = clazz.getDeclaredField("ucp");
        ucp.setAccessible(true);
        Method add = ucpCls.getDeclaredMethod("addURL", URL.class);
        add.setAccessible(true);
        add.invoke(ucp.get(classLoader), new File(path).toURI().toURL());
    }
}

class ArgParser {

    static String[] parse(String commandLine) {
        int pos = 0;
        int length = commandLine.length();

        StringBuilder sb = new StringBuilder();

        char[] chars = commandLine.toCharArray();
        ArrayList<String> res = new ArrayList<String>();

        boolean inStr = false;

        while (pos < length) {
            char c = chars[pos++];
            switch (c) {
                case ' ':
                case '\t':
                    if (inStr) {
                        sb.append(c);
                    } else if (sb.length() > 0) {
                        res.add(sb.toString());
                        sb = new StringBuilder();
                    }
                    break;
                case '\\':
                    if (pos < length && (chars[pos] == '"' || chars[pos] == '\\')) {
                        sb.append(chars[pos]);
                        pos++;
                    } else {
                        sb.append(c);
                    }
                    break;
                case '"':
                    inStr = !inStr;
                    break;
                default:
                    sb.append(c);
            }
        }
        if (sb.length() > 0) {
            res.add(sb.toString());
        }
        return res.toArray(new String[0]);
    }
}

public class Wrapper {
    public static native String getCommandLine();

    public static void main(String[] originArgs) throws Throwable {
        File jar_file = new File(Wrapper.class.getProtectionDomain().getCodeSource().getLocation().getPath());
        System.load(jar_file.getParent() + "\\JavaWrapper.dll");

        String commandLine = getCommandLine();

        String[] args = ArgParser.parse(commandLine);

        int pos = 1;
        final int len = args.length;
        String clazzMain = null;
        String[] argsOut = null;
        String version_jar_path = null;
        do {
            String flag = args[pos++];
            String arg = "";
            if (flag.charAt(0) == '-') {
                int eqPos = flag.indexOf('=');
                if (eqPos > -1) {
                    arg = flag.substring(eqPos + 1);
                    flag = flag.substring(0, eqPos);
                } else if (args[pos].charAt(0) != '-') {
                    arg = args[pos];
                }
                if (flag.startsWith("-D")) {
                    System.setProperty(flag.substring(2), arg);
                } else if ("-cp".equals(flag) || "--classpath".equals(flag) || "--class-path".equals(flag)) {
                    System.setProperty("java.class.path", arg);
                    String[] arg_split = arg.split(File.pathSeparator);
                    version_jar_path = arg_split[arg_split.length - 1];
                    for (String path : arg_split)
                        ClassPathInjector.appendClassPath(path);
                } else if ("-jar".equals(flag)) {
                    pos++;
                    clazzMain = args[pos++];
                    int lenOut = len - pos;
                    argsOut = new String[lenOut];
                    arraycopy(args, pos, argsOut, 0, lenOut);
                    pos = len;
                }
            }
        } while (pos < len);

        File version_jar = new File(version_jar_path);
        String version_path = version_jar.getParent();
        String timerecord_path = version_path + "/FMCL/timerecord.json";
        File timerecord_file = new File(timerecord_path);
        if (!timerecord_file.exists()) {
            Files.createDirectories(Paths.get(timerecord_file.getParent()));
            timerecord_file.createNewFile();
            FileWriter writer = new FileWriter(timerecord_file);
            writer.write("{}");
            writer.close();
        }
        JsonObject json_object = getJsonObject(timerecord_path);

        JsonObject new_record = new JsonObject();
        Number start = Long.valueOf(System.currentTimeMillis() / 1000);
        new_record.addProperty("start", start);
        new_record.addProperty("end", start);

        String index = Integer.toString(json_object.size());
        json_object.add(index, new_record);
        writeJson(timerecord_path, json_object);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            try {
                JsonObject json_object2 = getJsonObject(timerecord_path);
                JsonObject cur_record = json_object2.getAsJsonObject(index);
                Number end = Long.valueOf(System.currentTimeMillis() / 1000);
                cur_record.addProperty("end", end);
                writeJson(timerecord_path, json_object2);
            } catch (Throwable e) {
                e.printStackTrace();
            }
        }));

        invokeMain(clazzMain, argsOut);
    }

    private static void invokeMain(String mainClass, String[] args)
            throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        Class<?> clazz = ClassLoader.getSystemClassLoader().loadClass(mainClass);
        Method main = clazz.getDeclaredMethod("main", String[].class);
        main.setAccessible(true);
        main.invoke(null, (Object) args);
    }

    private static void writeJson(String json_path, JsonObject json_object) throws IOException {
        File json_file = new File(json_path);
        FileWriter writer = new FileWriter(json_file);
        writer.write((new Gson()).toJson(json_object));
        writer.close();
    }

    private static JsonObject getJsonObject(String json_path) throws IOException {
        String json_string = Files.readString(Paths.get(json_path));
        JsonObject json_object = JsonParser.parseString(json_string).getAsJsonObject();
        return json_object;
    }
}