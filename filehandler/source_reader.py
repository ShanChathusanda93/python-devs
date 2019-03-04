class SourceReader:
    @staticmethod
    def get_source(file_path):
        with open(file_path, "r") as source_file:
            source_code = source_file.read()
        source_code = source_code.replace("\n", " ")
        source_code = source_code.replace("require_once", "include")
        source_code = source_code.replace("require", "include")
        return source_code
