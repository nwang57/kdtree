from collections import namedtuple
from operator import itemgetter
import pprint

class Node(object):
    def __init__(self, point, left_child = None, right_child = None):
        self.point = point
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self, level=0):
        ret = "\t"*level + repr(self.point) + "\n"
        ret += self.left_child.__str__(level+1) if self.left_child else "\t"*(level+1)+'None'+"\n"
        ret += self.right_child.__str__(level+1) if self.right_child else "\t"*(level+1)+'None'+"\n"
        return ret

class Kdtree(object):
    def __init__(self, point_list=[]):
        self.tree = self.build(point_list)

    def get_height(self):
        return self._get_height(self.tree)

    def _get_height(self, tree):
        if not tree:
            return 0
        return max(self._get_height(tree.left_child), self._get_height(tree.right_child)) + 1

    def search(self, point):
        return self._search(self.tree, point)

    def _search(self, tree, point, depth=0):
        if not tree:
            return False
        if all([point[i] == tree.point[i] for i in xrange(len(point))]):
            return True
        else:
            axis = depth % len(point)
            if point[axis] < tree.point[axis]:
                return self._search(tree.left_child, point, depth+1)
            else:
                return self._search(tree.right_child, point, depth+1)

    def add_point(self, point):
        if self.search(point):
            print("point: %s already in the tree" % point)
        else:
            self._add_point(self.tree, point)

    def _add_point(self, tree, point, depth=0):
        if not tree:
            new_node = Node(point=point, left_child=None, right_child=None)
            tree = new_node
        else:
            axis = depth % len(point)
            if point[axis] < tree.point[axis]:
                if not tree.left_child:
                    new_node = Node(point=point, left_child=None, right_child=None)
                    tree.left_child = new_node
                else:
                    self._add_point(tree.left_child, point, depth+1)
            else:
                if not tree.right_child:
                    new_node = Node(point=point, left_child=None, right_child=None)
                    tree.right_child = new_node
                else:
                    self._add_point(tree.right_child, point, depth+1)

    def delete(self, point):
        if not self.search(point):
            print("Point not found")
        # Check if the root node will be deleted
        if all([point[i] == self.tree.point[i] for i in xrange(len(point))]):
            self.tree = self.build(self.to_list(self.tree.left_child)+self.to_list(self.tree.right_child))
        else:
            self._delete(self.tree, point)

    def _delete(self, tree, point, level=0):
        axis = level % len(point)
        if point[axis] < tree.point[axis]:
            if all([point[i] == tree.left_child.point[i] for i in xrange(len(point))]):
                tree.left_child = self.build(self.to_list(tree.left_child.left_child)+self.to_list(tree.left_child.right_child))
            else:
                self._delete(tree.left_child, point, level+1)
        else:
            if all([point[i] == tree.right_child.point[i] for i in xrange(len(point))]):
                tree.right_child = self.build(self.to_list(tree.right_child.left_child)+self.to_list(tree.right_child.right_child))
            else:
                self._delete(tree.right_child, point, level+1)

    def to_list(self, tree):
        if tree is None:
            return []
        return self.to_list(tree.left_child) + [tree.point] + self.to_list(tree.right_child)

    def build(self, point_list, depth=0):
        try:
            k = len(point_list[0])
        except IndexError as e:
            return None
        axis = depth % k
        point_list.sort(key=itemgetter(axis))
        median = len(point_list) // 2
        return Node(
                point=point_list[median],
                left_child=self.build(point_list[:median], depth+1),
                right_child=self.build(point_list[median+1:], depth+1)
                )
