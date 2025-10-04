# Height = 4, root = 3
# left_leaf = root+2, right_leaf = root*3

import json

def gen_bin_tree(height=4, root=3):
    if height <= 1:
        return {"value": root, "left": None, "right": None}

    return {
        "value": root,
        "left": gen_bin_tree(height-1, root+2),
        "right": gen_bin_tree(height-1, root*3)
    }

print(json.dumps(gen_bin_tree(), indent=4))