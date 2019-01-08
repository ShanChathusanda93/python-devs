import re
from stringFinder.ReferenceFinder import ReferenceFinder


def conversion_format_detector(file_name):
    with open(file_name, "r") as altered_source:
        source = altered_source.read()
        source = source.replace("\n", " ")

    # php_occurrences = php_detector_1(source)
    ref = ReferenceFinder()
    php_occurrences = ref.php_detector(source)

    # --if there is a html header, get the count of the header part of the file
    if re.findall('<!DOCTYPE html>', source).__len__() > 0:
        header = re.findall('<!DOCTYPE html>(.*?)</head>', source)
        header_length = len('<!DOCTYPE html></head>') + len(header[0])
    elif re.findall('<html>', source).__len__() > 0:
        header = re.findall('(<html>(.*?)</head>)', source)
        header_length = len('<html></head>') + len(header[0])
    else:
        header_length = 0

    file_length = source.__len__()

    # --get the total length of php codes
    total_php_length = 0
    for occurrence in php_occurrences:
        total_php_length = total_php_length + len(occurrence) + len("<?php?>")

    # --check whether the file contains a html header
    if header_length > 0:
        total_php_length = total_php_length + len("<body></body></html>")

    # --check whether the file contains more than php codes
    print(file_length - header_length)
    print(total_php_length)
    if file_length - header_length > total_php_length:
        print("article file")
    else:
        print("separate file")


def php_detector_1(source_code):
    occurrences = re.findall('<php>(.*?)<\/php>', source_code)
    return occurrences

# --not completed yet
conversion_format_detector(
    "/home/shan/Developments/Projects/research-devs/Blog/Login System/config.php")
