import unittest
from kdtree import Kdtree

class KdtreeTest(unittest.TestCase):
    def setUp(self):
        self.point_list = [(2,3), (4,5), (3,8), (1,6), (7, 2)]
        self.tree = Kdtree(self.point_list)

    def test_empty_tree(self):
        tree = Kdtree()
        self.assertIsNone(tree.tree)
        self.assertEqual(tree.n_nodes, 0)

    def test_build_tree(self):
        point_list = [(2,3), (4,5), (3,8), (1,6), (7, 2)]
        tree = Kdtree(point_list)
        self.assertEqual(tree.get_height(), 3)
        self.assertEqual(tree.n_nodes, 5)

    def test_search(self):
        self.assertTrue(self.tree.search((1,6)))
        self.assertFalse(self.tree.search((3,3)))

    def test_add_point(self):
        self.assertFalse(self.tree.search((5,3)))
        self.tree.add_point((5,3))
        self.assertTrue(self.tree.search((5,3)))
        self.assertEqual(self.tree.n_nodes, 6)

    def test_to_list(self):
        test_point_list = self.tree.to_list(self.tree.tree)
        a = set(test_point_list)
        b = set(self.point_list)
        self.assertEqual(a, b)

    def test_delete(self):
        self.assertTrue(self.tree.search((1,6)))
        self.tree.delete((1,6))
        self.assertFalse(self.tree.search((1,6)))
        self.assertEqual(self.tree.n_nodes, 4)

    def test_failed_delete(self):
        with self.assertRaises(IndexError):
            self.tree.delete((6,5))

    def test_nearest_neighbor(self):
        point = self.tree.get_nearest_neighbor((1,5))
        self.assertEqual(point, (1,6))

    def test_k_nearest_neighbor(self):
        knn = self.tree.get_k_nearest_neighbor((1,5), 3)
        self.assertTrue((1,6) in knn)
        self.assertTrue((2,3) in knn)
        self.assertTrue((4,5) in knn)

    def test_k_nearest_neighbor_large_k(self):
        knn = self.tree.get_k_nearest_neighbor((1,5), 6)
        for point in self.point_list:
            self.assertTrue(point in knn)
