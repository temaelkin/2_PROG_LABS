import json

def gen_bin_tree(height: int = 4,
                 root: int | float = 3, 
                 left_branch = lambda x: x + 2, 
                 right_branch = lambda x: x * 3) -> dict | None:
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
    left_branch : Lambda for computing left child's value. Defaults to x + 2.
    right_branch : Lambda for computing right child's value. Defaults to x * 3.

    Returns
    -------
    A nested dictionary representing the binary tree,
    or None if the height is 0.
    """

    if height < 0:
        return None
    elif height == 0:
        return root
    else:
        return {
            "value": root,
            "left": gen_bin_tree(height-1, left_branch(root), left_branch, right_branch),
            "right": gen_bin_tree(height-1, right_branch(root), left_branch, right_branch)
        }

print(json.dumps(gen_bin_tree(), indent=4))