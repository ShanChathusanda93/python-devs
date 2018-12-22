import re
from  bs4 import BeautifulSoup

# s = 'asdf=5;iwantthis123jasd -aaaaa asdf=5;hhhhhhhh123jasd'
# result = re.search('asdf=5;(.*)123jasd', s)
# print(result.group(1))

string = "<?php session_start();" \
         "include 'login_phpcode.php'
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <title>LMS Login</title>
  <?php include '../Template/Bootstrap/bootstrap.php'; ?>
  <link rel="stylesheet" type="text/css" href="login.css">
  <link rel="stylesheet" type="text/css" href="http://localhost/project/Blog/Templet/CSS/frontend.css">
</head>

<body>
<?php include '../Template/Navigation/frontend_navigation.php'; ?>
<div class="container-home" style="background-image:url(http://localhost/project/Blog/Images/img2.png);
background-positon:50% 50%; background-attachment:fixed; background-repeat:no-repeat; background-size:cover;">
        <div class="container">
        <div class="row">
            <div class="col-md-4 text-center">
                <br><br><br><br>
                <hr>
            </div>
            <div class="col-md-4 text-center">
                <br><br>
                <?php include 'login_form.php'; ?>
            </div>
            <div class="col-md-4 text-center">
                <br><br><br><br>
                <hr>
            </div>
        </div>
        </div>


    </div>
<!-- Footer -->
<?php include '../Template/Footer/footer.php'; ?>
</body>
</html>"
result = re.findall('<\?php([A-Za-z0-9.*\\\/+\"_=,;()\'$&!\[\]\n{\}<>%\-:#\s\n{\};\u00A9])+\?>',
                    string)
for r in result:
    print(r)
# print(result)

# s = 'foohellobargggggfoobellowbar'
# substring1 = 'foo'
# substring2 = 'bar'
# my_string = s[(s.index(substring1) + len(substring1)):s.index(substring2)]
# print(my_string)
