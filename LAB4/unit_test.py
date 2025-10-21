import unittest
from bin_tree import gen_bin_tree

class TestGenBinTree(unittest.TestCase):
    """Unit tests for the gen_bin_tree() function."""

    def test_return_dict(self):
        """Check that the function returns a dictionary."""
        tree = gen_bin_tree()
        self.assertIsInstance(tree, dict)

    def test_struct_keys(self):
        """Verify that the root node contains 'value', 'left', and 'right' keys."""
        tree = gen_bin_tree()
        self.assertIn("value", tree)
        self.assertIn("left", tree)
        self.assertIn("right", tree)

    def test_unit_height(self):
        """Check the case when height equals 1."""
        tree = gen_bin_tree(height=1, root=10)
        self.assertEqual(tree, {"value": 10, "left": None, "right": None})

    def test_zero_height(self):
        """Ensure that height = 0 produces an empty tree (None)."""
        tree = gen_bin_tree(height=0, root=10)
        self.assertIsNone(tree)
    
    def test_leaves_values(self):
        """Verify that left and right children follow the given formulas (root+2, root*3)."""
        tree = gen_bin_tree(height=2, root=3)
        self.assertEqual(tree["left"]["value"], 5)
        self.assertEqual(tree["right"]["value"], 9) 

    def test_float_root(self):
        """Check that the tree is correctly generated when root is a float."""
        tree = gen_bin_tree(height=2, root=1.5)
        self.assertEqual(tree["value"], 1.5)
        self.assertEqual(tree["left"]["value"], 3.5)
        self.assertEqual(tree["right"]["value"], 4.5)

    def test_determined(self):
        """Ensure that repeated calls with the same arguments produce identical but independent trees."""
        t1 = gen_bin_tree(height=4, root=3)
        t2 = gen_bin_tree(height=4, root=3)
        self.assertEqual(t1, t2)
        self.assertIsNot(t1, t2)

    def test_depth(self):
        """Check that the actual depth of the generated tree matches the given height parameter."""
        def depth(t):
            if t is None:
                return 0
            return 1 + max(depth(t["left"]), depth(t["right"]))   

unittest.main(argv=[''], verbosity=2, exit=False)