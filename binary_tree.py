#-*-coding:utf-8-*-
import random
import math

"""
ALL CREDIT TO 
https://github.com/marehr/binary-tree
"""

class NodeKey:
    def __init__(self, value, name=None):
        self.name = name
        self.value = value

    def __lt__(self, other):
        return self.value < other.value or \
               (self.value == other.value and self.name is not None and self.name < other.name)

    def __le__(self, other):
        return self < other or self == other

    def __eq__(self, other):
        return self.value == other.value and self.name == other.name

    def __ne__(self, other):
        return self.value != other.value or self.name != other.name

    def __gt__(self, other):
        return self.value > other.value or \
               (self.value == other.value and self.name is not None and self.name > other.name)

    def __ge__(self, other):
        return self > other or self == other

    def __str__(self):
        if self.name is None:
            return str(self.value)
        else:
            return str(self.value) + "," + str(self.name)


class Node:
    def __init__(self, value, name=None):
        self.key = NodeKey(value, name)
        # print('created node with key ' + str(self.key.value) + ":" + str(self.key.name))
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.height = 0

    def __str__(self):
        return str(self.key)

    def next(self):
        """ Returns the next Node (next key value larger)
        """
        # If has right child, select, then traverse left all the way down
        if self.right_child is not None:
            node = self.right_child
            while node.left_child is not None:
                node = node.left_child
            return node

        node = self
        # Try to find an ancestor that is a left child, return parent of that
        while node.parent is not None:
            if node.parent.left_child == node:
                return node.parent
            node = node.parent

        # Nothing greater than this
        return None

    def previous(self):
        """ Returns the previous Node (next key value smaller)
        """
        # If has left child, select, then traverse right all the way down
        if self.left_child is not None:
            node = self.left_child
            while node.right_child is not None:
                node = node.right_child
            return node

        node = self
        # Try to find an ancestor that is a right child, return parent of that
        while node.parent is not None:
            if node.parent.right_child == node:
                return node.parent
            node = node.parent

        #  Nothing smaller than this
        return None

    def is_leaf(self):
        """ Return True if Leaf, False Otherwise
        """
        return self.height == 0

    def max_child_height(self):
        """ Return Height Of Tallest Child or -1 if No Children
        """
        if self.left_child and self.right_child:
            # two children
            return max(self.left_child.height, self.right_child.height)
        elif self.left_child is not None and self.right_child is None:
            # one child, on left
            return self.left_child.height
        elif self.left_child is None and self.right_child is not None:
            # one child, on right
            return self.right_child.height
        else:
            # no Children
            return -1

    def weigh(self):
        """ Return How Left or Right Sided the Tree Is
        Positive Number Means Left Side Heavy, Negative Number Means Right Side Heavy
        """
        if self.left_child is None:
            left_height = -1
        else:
            left_height = self.left_child.height

        if self.right_child is None:
            right_height = -1
        else:
            right_height = self.right_child.height

        balance = left_height - right_height
        return balance

    def update_height(self):
        """ Updates Height of This Node and All Ancestor Nodes, As Necessary
        """
        # TODO: should stop iterating when reaches correct height
        node = self
        while node is not None:
            node.height = node.max_child_height() + 1
            node = node.parent

    def root(self):
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def balance(self, tree):
        """ Balances node, sets new tree root if appropriate
        Note: If balancing does occur, this node will move to a lower position on the tree
        """
        while self.weigh() < -1 or self.weigh() > 1:
            if self.weigh() < 0:
                # right side heavy
                if self.right_child.weigh() > 0:
                    # right-side left-side heavy
                    self.right_child.rotate_left()
                # right-side right-side heavy
                new_top = self.rotate_right()
            else:
                # left side heavy
                if self.left_child.weigh() < 0:
                    # left-side right-side heavy
                    self.left_child.rotate_right()
                # left-side left-side heavy
                new_top = self.rotate_left()

            if new_top.parent is None:
                tree.root = new_top

    def out(self):
        """ Return String Representing Tree From Current Node Down
        Only Works for Small Trees
        """
        start_node = self
        space_symbol = "*"
        spaces_count = 250
        out_string = ""
        initial_spaces_string = space_symbol * spaces_count + "\n"
        if start_node is None:
            return "AVLTree is empty"
        else:
            level = [start_node]
            while len([i for i in level if (not i is None)]) > 0:
                level_string = initial_spaces_string
                for i in range(len(level)):
                    j = (i + 1) * spaces_count / (len(level) + 1)
                    level_string = level_string[:j] + (str(level[i]) if level[i] else space_symbol) + level_string[j + 1:]
                level_next = []
                for i in level:
                    level_next += ([i.left_child, i.right_child] if i else [None, None])
                level = level_next
                out_string += level_string
        return out_string

    def rotate_right(self):
        assert(self.right_child is not None)
        to_promote = self.right_child
        swapper = to_promote.left_child

        # swap children
        self.right_child = swapper
        to_promote.left_child = self
        new_top = self._swap_parents(to_promote, swapper)
        if swapper is not None:
            swapper.update_height()
        self.update_height()
        return new_top

    def rotate_left(self):
        assert(self.left_child is not None)
        to_promote = self.left_child
        swapper = to_promote.right_child

        # swap children
        self.left_child = swapper
        to_promote.right_child = self
        new_top = self._swap_parents(to_promote, swapper)
        if swapper is not None:
            swapper.update_height()
        self.update_height()
        return new_top

    def _swap_parents(self, promote, swapper):
        """ re-assign parents, returns new top
        """
        promote.parent = self.parent
        self.parent = promote
        if swapper is not None:
            swapper.parent = self

        if promote.parent is not None:
            if promote.parent.right_child == self:
                promote.parent.right_child = promote
            elif promote.parent.left_child == self:
                promote.parent.left_child = promote
        return promote


class BinaryTree:
    """ Binary Search Tree
    Uses AVL Tree
    """
    def __init__(self, *args):
        self.root = None  # root Node
        self.element_count = 0
        if len(args) == 1:
            for i in args[0]:
                self.insert(i)

    def __len__(self):
        return self.element_count

    def __str__(self):
        return self.out()

    def height(self):
        """ Return Max Height Of Tree
        """
        if self.root is not None:
            return self.root.height
        else:
            return 0

    def balance(self):
        """ Perform balancing Operation
        """
        if self.root is not None:
            self.root.balance(self)

    def insert(self, value, name=None):
        #print('Insert {}, {}'.format(name, value))
        if self.root is None:
            # If nothing in tree
            self.root = Node(value, name)
        else:
            if self.find(NodeKey(value, name)) is None:
                # If key/name pair doesn't exist in tree
                self.element_count += 1
                self.add_as_child(self.root, Node(value, name))

    def add_as_child(self, parent_node, child_node):
        if child_node.key < parent_node.key:
            # should go on left
            if parent_node.left_child is None:
                # can add to this node
                parent_node.left_child = child_node
                child_node.parent = parent_node
                child_node.update_height()
            else:
                self.add_as_child(parent_node.left_child, child_node)
        else:
            # should go on right
            if parent_node.right_child is None:
                # can add to this node
                parent_node.right_child = child_node
                child_node.parent = parent_node
                child_node.update_height()
            else:
                self.add_as_child(parent_node.right_child, child_node)

        if parent_node.weigh() not in [-1, 0, 1]:
            parent_node.balance(self)

    def inorder_non_recursive(self):
        node = self.root
        retlst = []
        while node.left_child:
            node = node.left_child
        while node:
            if node.key.name is not None:
                retlst.append([node.key.value, node.key.name])
            else:
                retlst.append(node.key.value)
            if node.right_child:
                node = node.right_child
                while node.left_child:
                    node = node.left_child
            else:
                while node.parent and (node == node.parent.right_child):
                    node = node.parent
                node = node.parent
        return retlst

    def preorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.key.name is not None:
            retlst.append([node.key.value, node.key.name])
        else:
            retlst.append(node.key.value)
        if node.left_child:
            retlst = self.preorder(node.left_child, retlst)
        if node.right_child:
            retlst = self.preorder(node.right_child, retlst)
        return retlst

    def inorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.left_child:
            retlst = self.inorder(node.left_child, retlst)
        if node.key.name is not None:
            retlst.append([node.key.value, node.key.name])
        else:
            retlst.append(node.key.value)
        if node.right_child:
            retlst = self.inorder(node.right_child, retlst)
        return retlst

    def postorder(self, node, retlst=None):
        if retlst is None:
            retlst = []
        if node.left_child:
            retlst = self.postorder(node.left_child, retlst)
        if node.right_child:
            retlst = self.postorder(node.right_child, retlst)
        if node.key.name is not None:
            retlst.append([node.key.value, node.key.name])
        else:
            retlst.append(node.key.value)
        return retlst

    def as_list(self, pre_in_post):
        if not self.root:
            return []
        if pre_in_post == 0:
            return self.preorder(self.root)
        elif pre_in_post == 1:
            return self.inorder(self.root)
        elif pre_in_post == 2:
            return self.postorder(self.root)
        elif pre_in_post == 3:
            return self.inorder_non_recursive()

    def find_value(self, value):
        return self.find_in_subtree(self.root, NodeKey(value))

    def find(self, key):
        return self.find_in_subtree(self.root, key)

    def find_largest_lessthan(self, value):
        return self._find_largest_lessthan(self.root, value, None)

    def _find_largest_lessthan(self, node, value, best):
        if node is None:    # Bottom of tree
            return best

        diff = value - node.key.value
        if diff > 0 and (best is None or diff < value - best.value):
            # Found a closer value
            best = node

        if value < node.key.value:
            return self._find_largest_lessthan(node.left_child, value, best)
        if value > node.key.value:
            return self._find_largest_lessthan(node.right_child, value, best)
        else:       # Equal
            return node

    def find_in_subtree(self, node, node_key):
        if node is None:
            return None  # key not found
        if node_key < node.key:
            return self.find_in_subtree(node.left_child, node_key)
        elif node_key > node.key:
            return self.find_in_subtree(node.right_child, node_key)
        else:  # key is equal to node key
            return node

    def remove(self, key):
        #print('Removing {}, {}'.format(key.name, key.value))
        # first find
        node = self.find(key)

        if node is not None:
            self.element_count -= 1

            if node.is_leaf():
                # The node is a leaf.  Remove it and return.
                #print('leaf')
                self.remove_leaf(node)
            elif (node.left_child is not None and node.right_child is None) or \
                    (node.left_child is None and node.right_child is not None):
                # The node has only 1 child. Make the pointer to this node point to the child of this node.
                #print('branch')
                #fei: there is something wrong
                #self.remove_branch(node)
                #node is the root
                if node.parent is None:
                    #node.parent = None
                    if node.left_child is None:
                        self.root = node.right_child
                    else:
                        self.root = node.left_child
                    self.root.parent = None
                else:
                    self.remove_branch(node)

            else:
                # The node has 2 children. Swap items with the successor (the smallest item in its right subtree) and
                # delete the successor from the right subtree of the node.
                #print('2 childs')
                assert node.left_child and node.right_child
                self.swap_with_successor_and_remove(node)
        else:
            raise Exception('Tried to remove nonexistent key ' + str(key))
        return None

    def remove_leaf(self, node):
        parent = node.parent
        if parent:
            if parent.left_child == node:
                parent.left_child = None
            else:
                assert (parent.right_child == node)
                parent.right_child = None
            parent.update_height()
        else:
            self.root = None

        # rebalance
        node = parent
        while node:
            if not node.weigh() in [-1, 0, 1]:
                node.balance(self)
            node = node.parent

    def remove_branch(self, node):
        parent = node.parent
        if parent is not None:
            if parent.left_child == node:
                parent.left_child = node.right_child
                if parent.left_child is None:
                    parent.left_child = node.left_child
            else:
                assert (parent.right_child == node)
                parent.right_child = node.right_child
                if parent.right_child is None:
                    parent.right_child = node.left_child

            if node.left_child is not None:
                node.left_child.parent = parent
            else:
                assert node.right_child
                node.right_child.parent = parent
            parent.update_height()

        # rebalance
        node = parent
        while node is not None:
            if not node.weigh() in [-1, 0, 1]:
                node.balance(self)
            node = node.parent

    def swap_with_successor_and_remove(self, node):
        successor = node.right_child
        while successor.left_child:
            successor = successor.left_child
        self.swap_nodes(node, successor)
        assert (node.left_child is None)
        if node.height == 0:
            self.remove_leaf(node)
        else:
            self.remove_branch(node)

    def swap_nodes(self, node_1, node_2):
        assert (node_1.height > node_2.height)
        parent_1 = node_1.parent
        left_child_1 = node_1.left_child
        right_child_1 = node_1.right_child
        parent_2 = node_2.parent
        assert (not parent_2 is None)
        assert (parent_2.left_child == node_2 or parent_2 == node_1)
        left_child_2 = node_2.left_child
        assert (left_child_2 is None)
        right_child_2 = node_2.right_child

        # swap heights
        tmp = node_1.height
        node_1.height = node_2.height
        node_2.height = tmp

        if parent_1:
            if parent_1.left_child == node_1:
                parent_1.left_child = node_2
            else:
                assert (parent_1.right_child == node_1)
                parent_1.right_child = node_2
            node_2.parent = parent_1
        else:
            self.root = node_2
            node_2.parent = None

        node_2.left_child = left_child_1
        left_child_1.parent = node_2
        node_1.left_child = left_child_2  # None
        node_1.right_child = right_child_2
        if right_child_2:
            right_child_2.parent = node_1
        if not (parent_2 == node_1):
            node_2.right_child = right_child_1
            right_child_1.parent = node_2

            parent_2.left_child = node_1
            node_1.parent = parent_2
        else:
            node_2.right_child = node_1
            node_1.parent = node_2

            # use for debug only and only with small trees

    def out(self, start_node=None):
        if start_node is None:
            start_node = self.root

        if start_node is None:
            return None
        else:
            return start_node.out()

    def min(self):
        current = self.root
        if current is None:
            return None

        while current.left_child is not None:
            current = current.left_child
        return current

    def second_min(self):
        min = self.min()
        if min is None:
            return None
        elif min == self.root:
            if min.left_child is None and min.right_child is None:
                return None

        parent = None
        child = self.root

        while child.left_child is not None:
            parent = child
            child = child.left_child

        if child.right_child is None:
            return parent

        child = child.right_child
        while child.left_child is not None:
            child = child.left_child

        return child

def test():
    def random_data_generator(count, max_val):
        for n in range(count):
            yield random.randint(0, max_val)

    def sanity_check(tree=None, node=None):
        if node is None and tree is not None:
            node = tree.root
        if (node is None) or (node.is_leaf() and node.parent is None):
            # trivial - no sanity check needed, as either the tree is empty or there is only one node in the tree
            pass
        else:
            if node.height != node.max_child_height() + 1:
                raise Exception("Invalid height for node " + str(node) + ": " + str(node.height) + " instead of " + str(node.max_child_height() + 1) + "!")

            bal_factor = node.weigh()
            #Test the balance factor
            if not (-1 <= bal_factor <= 1):
                raise Exception("Balance factor for node " + str(node) + " is " + str(bal_factor) + "!")
                #Make sure we have no circular references
            if not (node.left_child != node):
                raise Exception("Circular reference for node " + str(node) + ": node.left_child is node!")
            if not (node.right_child != node):
                raise Exception("Circular reference for node " + str(node) + ": node.right_child is node!")

            if node.left_child:
                if not (node.left_child.parent == node):
                    raise Exception("Left child of node " + str(node) + " doesn't know who his father is!")
                if not (node.left_child.key <= node.key):
                    raise Exception("Key of left child of node " + str(node) + " is greater than key of his parent!")
                sanity_check(node=node.left_child)

            if node.right_child:
                if not (node.right_child.parent == node):
                    raise Exception("Right child of node " + str(node) + " doesn't know who his father is!")
                if not (node.right_child.key >= node.key):
                    raise Exception("Key of right child of node " + str(node) + " is less than key of his parent!")
                sanity_check(node=node.right_child)

    print("check empty tree creation")
    a = BinaryTree()
    print("about to do sanity check 1")
    sanity_check(tree=a)

    print("check not empty tree creation")
    seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    seq_copy = list(seq)
    #random.shuffle(seq)
    b = BinaryTree(seq)
    print("about to do sanity check 2")
    sanity_check(tree=b)

    print("check that inorder traversal on an AVL tree (and on a binary search tree in the whole) will return values from the underlying set in order")
    assert (b.as_list(3) == b.as_list(1) == seq_copy)

    random.shuffle(seq)
    for x in seq:
        b.remove(x)

    print("check that node deletion works")
    c = BinaryTree(random_data_generator(20000, 25000))
    before_deletion = c.element_count
    for i in random_data_generator(5000, 25000):
        c.remove(i)
    after_deletion = c.element_count
    sanity_check(tree=c)
    assert (before_deletion >= after_deletion)

    print("check that an AVL tree's height is strictly less than 1.44*log2(N+2)-1 (there N is number of elements)")
    assert (c.height() < 1.44 * math.log(after_deletion + 2, 2) - 1)