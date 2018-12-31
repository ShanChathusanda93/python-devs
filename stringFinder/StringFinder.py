import re

# text = 'Allowed Hello Hollow'
text = '<?php include "../Template/Navigation/frontend_navigation.php"; ?><?php echo ?>'
for i in re.finditer('<\?php', text):
    for j in re.finditer('\?>', text):
        print('<?php found in ', i.start(), i.end(), j.start(), j.end())
