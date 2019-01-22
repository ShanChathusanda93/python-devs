import re

from utils.Stack import Stack


# --this class contains the methods to detect the extended while and for loops in the source code
# --need further implementations
class LoopDetector:

    def detect_extended_while_loops(self):
        indices = []
        while_stack = Stack()
        with open("/opt/lampp/htdocs/Blog/post views/view_post_image_phpcode.php", "r") as source_file:
            code = source_file.read()
        source = code.replace("\n", " ")
        # for_start_indices = [(w.start(0), w.end(0)) for w in re.finditer("while\s*\((.*?)\s*:", source)]
        while_start_indices = [w.start(0) for w in re.finditer("while\s*\((.*?)\s*:", source)]
        end_start_indices = [e.start(0) for e in re.finditer("endwhile;", source)]
        for w_index in while_start_indices:
            indices.append(w_index)
        for e_index in end_start_indices:
            indices.append(e_index)

        indices.sort(reverse=False)
        for idx in indices:
            if idx in while_start_indices:
                while_stack.push(idx)
            elif idx in end_start_indices:
                if while_stack.size() == 1:
                    while_start = while_stack.pop()
                    file = source[while_start:idx]
                    print(file)
                else:
                    while_stack.pop()

    def detect_extended_for_loops(self):
        for_indices = []
        for_stack = Stack()
        with open("/opt/lampp/htdocs/Blog/post views/view_post_image_phpcode.php", "r") as source_file:
            code = source_file.read()
        source = code.replace("\n", " ")
        # for_start_indices = [(w.start(0), w.end(0)) for w in re.finditer("while\s*\((.*?)\s*:", source)]
        for_start_indices = [f.start(0) for f in re.finditer("for\s*\((.*?)\s*:", source)]
        end_start_indices = [e.start(0) for e in re.finditer("endfor;", source)]
        for f_index in for_start_indices:
            for_indices.append(f_index)
        for e_index in end_start_indices:
            for_indices.append(e_index)

        for_indices.sort(reverse=False)
        for idx in for_indices:
            if idx in for_start_indices:
                for_stack.push(idx)
            elif idx in end_start_indices:
                if for_stack.size() == 1:
                    while_start = for_stack.pop()
                    file = source[while_start:idx]
                    print(file)
                else:
                    for_stack.pop()
