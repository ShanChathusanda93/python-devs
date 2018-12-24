import os
import re

# --filePaths in windows
# filePath = "C:\\xampp\\htdocs\\Blog\\Frontend\\frontend.php"
# filePath = "C:\\xampp\\htdocs\\Blog\\Login System\\login_phpcode.php"
# --filePaths in ubuntu
filePath = "/home/shan/Developments/Projects/research-devs/Blog/Frontend/frontend.php"
# filePath = "/home/shan/Developments/Projects/research-devs/Blog/Login System/login_phpcode.php"

with open(filePath, "r", encoding="utf8") as file:
    orig = file.read()
    text = orig.replace('\n', '')

# --develop a for loop for this section for the try block
try:
    # --finding the page title or the file name to create the new file
    uploadedFileTitle = re.findall('<title>(.*?)</title>', text)
    if uploadedFileTitle.__len__() == 0:
        tempBasePath = os.path.basename(filePath)
        fileNameBase = os.path.splitext(tempBasePath)[0].replace(' ', '_')
    else:
        fileNameBase = uploadedFileTitle[0].replace(' ', '_')

    # --iterator
    i = 1
    # --access rights to create directories
    access_rights = 0o755

    # --creating target directory for all php files
    targetPhpDirPath = "/home/shan/Developments/Projects/research-devs/python-devs/fileHandler/phpSnippets"
    if not os.path.exists(targetPhpDirPath):
        os.mkdir(targetPhpDirPath, access_rights)

    # --path for each source files php snippets
    targetFileDirPath = "/home/shan/Developments/Projects/research-devs/python-devs/fileHandler/phpSnippets/" + \
                        fileNameBase

    occurrences = re.findall('<\?php(.*?)\?>', text)
    for occurrence in occurrences:
        # --creating the directory for each source file
        if not os.path.exists(targetFileDirPath):
            os.mkdir(targetFileDirPath, access_rights)

        # --file name of the target php file
        fileName = targetFileDirPath + "/" + fileNameBase + "_php_part_" + str(i) + ".php"

        # --editing the places with the php codes extracted in the source code by putting the references
        alteredPhp = text.replace("<?php" + occurrence + "?>", "<php> include '.." + fileName + "';</php>")
        alteredSrcCode = alteredPhp.replace("\"", "\'")
        with open("alteredSrcFile.txt", "a") as alteredSrc:
            alteredSrc.write(alteredSrcCode)

        with open(fileName, "w") as writingFile:
            # --retouching the extracted php source code
            retouchNew = occurrence.replace(';', ';\n\t')
            retouchBrac = retouchNew.replace('{', '{\n\t')
            retouchReq = retouchBrac.replace('require_once', '\nrequire_once')
            retouchIf = retouchReq.replace('if(', '\t\nif(')

            writingFile.write("<?php\n" + retouchIf + "\n?>")
            writingFile.close()
        i = i + 1
except AttributeError:
    occurrence = 'Not occurrence in the original string'
    print(occurrence)

file.close()
