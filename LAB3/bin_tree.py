import json

def gen_bin_tree(height: int = 4, root: int | float = 3) -> dict | None:
    """
    Recursively generate a binary tree as a nested dictionary.

    Each node of the tree is a dictionary with the keys:
    "value", "left", "right". The values of child nodes are computed
    according to given formulas:
    left child = root + 2
    right child = root * 3

    The recursion terminates when the height is less than or equal to 0
    (returns None) or equals 1 (returns a single-node tree).
    
    Parameters
    ----------
    height : The height of the tree (must be >= 0). Defaults to 4.
    root : The value stored in the root node. Defaults to 3.

    Returns
    -------
    A nested dictionary representing the binary tree,
    or None if the height is 0.
    """
    if height <= 0:
        return None
    if height == 1:
        return {"value": root, "left": None, "right": None}

    return {
        "value": root,
        "left": gen_bin_tree(height-1, root+2),
        "right": gen_bin_tree(height-1, root*3)
    }

print(json.dumps(gen_bin_tree(), indent=4))