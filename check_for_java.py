import re

def check_for_java(text):
  return bool(re.search("((.|\n)*)[(].*\.java.*[)]((.|\n)*)", text))
  
  
testString = 'Exception in thread "main" java.lang.ClassNotFoundException: com.mysql.jdbc.Driver\nat java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:581)\nat java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:17)\nat java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:521)\nat java.base/java.lang.Class.forName0(Native Method)\nat java.base/java.lang.Class.forName(Class.java:315)'

print(check_for_java(testString))

testString = 'at java.base/java.java.lang.Class.forName(Class.jsva:315)'

print(check_for_java(testString))