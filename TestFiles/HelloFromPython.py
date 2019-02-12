import os


# print("Hello World from python...!!!")
#
# for i in range(1, 10):
#     print(i)
#     print("\n")


def detect_files():
    file_paths = []
    for paths, sub_dirs, files in os.walk("/home/shan/Developments/Projects/research-devs/Blog"):
        for file_path in files:
            base_name = os.path.basename(file_path)
            file_name = os.path.splitext(base_name)
            if file_name[1] == ".php" or file_name[1] == ".html":
                full_path = os.path.join(paths, file_path)
                file_paths.append(full_path)
                # print(full_path)
    return file_paths


def get_hello_with_name(name_str):
    hello = "Hello Mr. " + name_str
    return hello
    # print(hello)


def square(value):
    return value * value
# detect_files("/home/shan/Developments/Projects/research-devs/Blog")
