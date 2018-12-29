# --the code at this file will detect files which contains a corresponding substring at the file name
import os


class FileDetector:
    # --method to detect the files
    # --root is the path of the source files and the anchor_str is the corresponding substring to be found in the file
    # --names
    def detect_files(self, root, anchor_str):
        sourceList = open("sourceList.txt", "w")
        for paths, sub_dirs, files in os.walk(root):
            for file_path in files:
                base_name = os.path.basename(file_path)
                file_name = os.path.splitext(base_name)
                if file_name[1] == ".php" or file_name[1] == ".html":
                    # if anchor_str in file_name[0]:
                    #     print(file_name[0])
                    full_path = os.path.join(paths, file_path)
                    sourceList.write(full_path + "\n")
                    print(full_path)
        sourceList.close()
