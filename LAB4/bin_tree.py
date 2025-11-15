import json
from collections import deque

def gen_bin_tree(height: int = 4, 
                 root: int | float = 3, 
                 left_branch = lambda x: x + 2, 
                 right_branch = lambda x: x * 3) -> dict:
    """
    Generate a binary tree as a nested dictionary NON-recusively.

    Each node of the tree is a dictionary with the keys:
    "value", "left", "right". The values of child nodes are computed
    according to given formulas as lambdas:
    left child = root + 2
    right child = root * 3

    The tree is built iteratively using a queue (FIFO structure),
    implemented via collections.deque for O(1) pops from the left,
    ensuring efficient level-by-level expansion without recursion.

    Parameters
    ----------
    height : The height of the tree (must be >= 1). Defaults to 4.
    root : The value stored in the root node. Defaults to 3.
    left_branch : Lambda for computing left child's value. Defaults to x + 2.
    right_branch : Lambda for computing right child's value. Defaults to x * 3.

    Returns
    -------
    A nested dictionary representing the binary tree,
    or Root value if the height is 0 and None if the height is less than 0.
    """

    if height < 0:
        return None
    elif height == 0:
        return root

    root_node = {
        "value": root, 
        "left": None, 
        "right": None
    }
    
    queue = deque([root_node])

    for _ in range(height):
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()

            if height == 0:
                continue

            left_value = left_branch(node["value"])
            right_value = right_branch(node["value"])

            left_child = {"value": left_value, "left": None, "right": None}
            right_child = {"value": right_value, "left": None, "right": None}

            node["left"] = left_child
            node["right"] = right_child

            queue.append(left_child)
            queue.append(right_child)

        height -= 1

    return root_node

print(json.dumps(gen_bin_tree(), indent=4))