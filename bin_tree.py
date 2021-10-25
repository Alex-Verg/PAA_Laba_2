class Node:

    def __init__(self, val):
        self.left = None
        self.right = None
        self.parent = None
        self.value = val

    def _str(self):
        return "%d" % self.value


class BTree:

    def __init__(self):
        self.head = None
        self.size = 0

    def insert(self, data):
        root = self.head
        if not root:
            self.head = Node(data)
            self.size += 1
        while root:
            if data < root.value:
                if not root.left:
                    root.left = Node(data)
                    root.left.parent = root
                    self.size += 1
                    return
                else:
                    root = root.left
            elif data == root.value:
                return
            elif data > root.value:
                if not root.right:
                    root.right = Node(data)
                    root.right.parent = root
                    self.size += 1
                    return
                else:
                    root = root.right
