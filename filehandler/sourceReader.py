import os

from stringfinder.reference_finder import ReferenceFinder

# --filePaths in windows
# filePath = "C:\\xampp\\htdocs\\Blog\\Frontend\\frontend.php"
# filePath = "C:\\xampp\\htdocs\\Blog\\Login System\\login_phpcode.php"
# --filePaths in ubuntu
# filePath = "/home/shan/Developments/Projects/research-devs/Blog/Frontend/frontend.php"
# filePath = "/home/shan/Developments/Projects/research-devs/Blog/Login System/login_phpcode.php"
filePath = "/home/shan/Developments/Projects/research-devs/Blog/Login System/config.php"
# filePath = "/home/shan/Developments/Projects/research-devs/Blog/Template/Navigation/frontend_navigation.php"

with open(filePath, "r", encoding="utf8") as file:
    orig = file.read()
    text = orig.replace('\n', '')

# --develop a for loop for this section for the try block
try:
    tempBasePath = os.path.basename(filePath)
    fileNameBase = os.path.splitext(tempBasePath)[0].replace(' ', '_')

    # --iterator
    i = 1
    # --access rights to create directories
    access_rights = 0o755

    # --creating target directory for all php files
    targetPhpDirPath = "/home/shan/Developments/Projects/research-devs/python-devs/filehandler/phpSnippets"
    if not os.path.exists(targetPhpDirPath):
        os.mkdir(targetPhpDirPath, access_rights)

    # --creating the target directory for the altered source code
    targetAlteredSrcDirPath = "/home/shan/Developments/Projects/research-devs/python-devs/filehandler/alteredSrc"
    if not os.path.exists(targetAlteredSrcDirPath):
        os.mkdir(targetAlteredSrcDirPath, access_rights)

    # --path for each source files php snippets
    targetFileDirPath = "/home/shan/Developments/Projects/research-devs/python-devs/filehandler/phpSnippets/" + \
                        fileNameBase

    # occurrences = re.findall('<\?php(.*?)\?>', text)
    php_occurrences = ReferenceFinder.get_php_occurrences(ReferenceFinder, text)
    included_files = ReferenceFinder.get_included_php_file_paths(ReferenceFinder, php_occurrences,
                                                                 need_compl_path=False)
    required_files = ReferenceFinder.get_required_php_file_paths(ReferenceFinder, php_occurrences,
                                                                 need_compl_path=False)

    if php_occurrences.__len__() > 0:
        # --creating the directory for each php source file
        if not os.path.exists(targetFileDirPath):
            os.mkdir(targetFileDirPath, access_rights)
        if included_files.__len__() == 0 and required_files.__len__() == 0:
            alteredPhp = text
            for occurrence in php_occurrences:
                # --file name of the target php file
                fileName = targetFileDirPath + "/" + fileNameBase + "_php_part_" + str(i) + ".php"

                # --editing the places with the php codes extracted in the source code by putting the references
                text = text.replace("<?php" + occurrence + "?>", "<php> include '.." + fileName + "';</php>")
                text = text.replace("\"", "\'")

                with open(fileName, "w") as writingFile:
                    # --retouching the extracted php source code
                    retouchNew = occurrence.replace(';', ';\n\t')
                    retouchBrac = retouchNew.replace('{', '{\n\t')
                    retouchReq = retouchBrac.replace('require_once', '\nrequire_once')
                    retouchIf = retouchReq.replace('if(', '\t\nif(')

                    writingFile.write("<?php\n" + retouchIf + "\n?>")
                    writingFile.close()
                i = i + 1
            with open(targetAlteredSrcDirPath + "/altered_" + fileNameBase + ".txt", "w") as alteredSrc:
                alteredSrc.write(text)
except AttributeError:
    occurrence = 'Not occurrence in the original string'
    print(occurrence)

file.close()

# --finding the page title or the file name to create the new file
# uploadedFileTitle = re.findall('<title>(.*?)</title>', text)
# if uploadedFileTitle.__len__() == 0:

# else:
#     fileNameBase = uploadedFileTitle[0].replace(' ', '_')

# # --searching for includes and requires in the occurrence
# includeFiles = re.findall('include \'(.*?)\';', occurrence)
# baseSourcePath = "/home/shan/Developments/Projects/research-devs/Blog"
# for includeFile in includeFiles:
#     if "../" in includeFile:
#         includeFilePath = includeFile.replace('..', baseSourcePath)
#     else:
#         includeFilePath = baseSourcePath + "/Frontend/" + includeFile
#
#     with open(includeFilePath, "r") as inclFile:
#         incl = inclFile.read()
#         # print(includeFilePath)
#         # print(incl)
#         inclFile.close()
