from html.entities import name2codepoint
from html.parser import HTMLParser

f = open("codeHierarchy.txt", "a")


class MyHTMLParser02(HTMLParser):

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        print("Start tag", tag)
        f.write("Start tag: " + tag + "\n")
        for attr in attrs:
            print("     attr:", attr)
            f.write("   attr: " + str(attr) + "\n")

    def handle_endtag(self, tag):
        print("End tag", tag)
        f.write("End tag: " + tag + "\n")

    def handle_data(self, data):
        print("     Data:", data)
        f.write("       Data:" + data + "\n")

    def handle_comment(self, data):
        print("Comment  :", data)
        f.write("Comment: " + data + "\n")

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)
        f.write("Named ent: " + c + "\n")

    def handle_charref(self, name):
        if name.startwith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent:", c)
        f.write("Num ent: " + c + "\n")

    def handle_decl(self, data):
        print("Decl     :", data)
        f.write("Decl: " + data + "\n")


parser = MyHTMLParser02()
filePath = "/home/shan/Developments/Projects/research-devs/Blog/Template/Navigation/frontend_navigation.php"
access_rights = 0o777
file = open(filePath, "r", access_rights, encoding="utf8")
orig = file.read()
text = orig.replace('\n', '')
file.close()
parser.feed(text)

# file.close()
# parser.feed(
#     "<!DOCTYPE html><html><head><title>My Templet</title><?php include '../Template/Bootstrap/bootstrap.php';
#     ?><link "
#     "rel='stylesheet' type='text/css' href='http://localhost/project/Blog/Templet/CSS/frontend.css'></head><body"
#     "><php> include '../Template/Navigation/frontend_navigation.php';</php><div class='jumbotron'><php> include "
#     "'vedio.php'; </php><div class='container text-center'><br><img "
#     "src='http://localhost/project/Blog/Images/katapath_pawra.png' style='width: 500px;'><p style='color: "
#     "black;'>write your heart...</p></div></div>")
# parser.feed(
#     "<footer style='background-color: brown;'><div class='container'><div class='row'><br><br><div class='col-md-4' "
#     "style='color: white;'><p>'Shamali',<br> Colombo Road,<br> Pokunuwita,<br> Sri Lanka.</p><p>077- _ _ _ _ _</p><a "
#     "href='mailto:mail@example.com'>mail@example.com</a></div><div class='col-md-4'><p>')")
f.close()
