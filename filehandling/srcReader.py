import re

# filePath = "C:\\xampp\\htdocs\\Blog\\Frontend\\frontend.php"
filePath = "C:\\xampp\\htdocs\\Blog\\Login System\\login_phpcode.php"
with open(filePath, "r", encoding="utf8") as file:
    orig = file.read()
    text = orig.replace('\n', '')
    stringLength = len(text)

# develop a for loop for this section for the try block
try:
    # found = re.search('<?php(.+?)?>', text).group(1)
    found = re.findall('<\?php(.*?)\?>', text)
    for f in found:
        retouchNew = f.replace(';', ';\n\t')
        retouchBrac = retouchNew.replace('{', '{\n\t')
        retouchReq = retouchBrac.replace('require_once', '\nrequire_once')
        retouchIf = retouchReq.replace('if(', '\t\nif(')
        print(retouchIf)
except AttributeError:
    found = 'Not found in the original string'
    print(found)

file.close()

# counter = text.index("?>")
# print(str(counter) + "\n")
# print(found + "\n")
# f = open("D:\\Academics\\Year_4_Individual_Research\\Research Sample Codes\\Blog\\Frontend\\frontend.php", "r",
#          encoding="utf8")
# file = f.read()
# print(file)
# found = re.findall('<?php(.+?)?>', file).group(1)
# for find in found:
#     counter = find.index("?>")
#     print(str(counter) + "\n")
#     print(find + "\n")
