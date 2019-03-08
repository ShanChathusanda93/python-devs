import re


def remove_html_header(source):
    edited_source = " "
    if re.findall('<!DOCTYPE html>', source).__len__() > 0:
        header = re.findall('<!DOCTYPE html>(.*?)<body>', source)
        edited_source = source.replace("<!DOCTYPE html>" + header[0] + "<body>", " ")
    elif re.findall('<html>', source).__len__() > 0:
        header = re.findall('(<html>(.*?)<body>)', source)
        edited_source = source.replace("<html>" + header[0] + "<body>", " ")
    edited_source = edited_source.replace("</body>", " ")
    edited_source = edited_source.replace("</html>", " ")
    return edited_source
