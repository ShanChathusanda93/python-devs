from TestFiles.staticdatatest.class_a import ClassA
from TestFiles.staticdatatest.class_b import ClassB


class_a = ClassA()
class_a.set_source_directory_path("/this/is/the/source/path")
class_b = ClassB()
print(class_b.get_source_directory_path())

