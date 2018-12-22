from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag: ", tag)

    def handle_endtag(self, tag):
        print("Encountered a end tag: ", tag)

    def handle_data(self, data):
        print("Encountered some data:", data)


parser = MyHTMLParser()
# parser.feed('<html><head><title>Test</title></head><body><h1>Parse me!</h1></body></html>')
parser.feed(
    "<!DOCTYPE html><html><head><title>My Templet</title><?php include '../Template/Bootstrap/bootstrap.php'; ?><link "
    "rel='stylesheet' type='text/css' href='http://localhost/project/Blog/Templet/CSS/frontend.css'></head><body"
    "><?php include '../Template/Navigation/frontend_navigation.php'; ?><div class='jumbotron'><?php include "
    "'vedio.php'; ?><div class='container text-center'><br><img "
    "src='http://localhost/project/Blog/Images/katapath_pawra.png' style='width: 500px;'><p style='color: "
    "black;'>write your heart...</p></div></div>")
