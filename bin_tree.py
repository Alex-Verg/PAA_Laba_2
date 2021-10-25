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

    def __len__(self):
        return self.size

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


class Heap:

    def __init__(self, arr):
        self.n = len(arr)
        self.list = arr
        for i in range(self.n // 2, -1, -1):
            self.max_heapify(i)

    def max_heapify(self, ind):
        l = 2 * ind + 1
        r = 2 * ind + 2
        if l < self.n and self.list[l] > self.list[ind]:
            largest = l
        else:
            largest = ind
        if r < self.n and self.list[r] > self.list[largest]:
            largest = r
        if largest != ind:
            self.list[ind], self.list[largest] = self.list[largest], self.list[ind]
            self.max_heapify(largest)

    def heapsort(self):
        for i in range(self.n-1, 0, -1):
            self.list[0], self.list[i] = self.list[i], self.list[0]
            self.n -= 1
            self.max_heapify(0)

    def print(self):
        print(*self.list)

COUNT = [5]


def print2DUtil(root, space=0):
    if not root:
        return
    space += COUNT[0]
    print2DUtil(root.right, space)
    print()
    for i in range(COUNT[0], space):
        print(end = " ")
    print(root.value)
    print2DUtil(root.left, space)


if __name__ == "__main__":
    tree = BTree()
    nodes = [15, 28, 27, 9, 19, 6, 26, 29, 8, 18, 2, 20, 23, 21, 4, 17]
    for i in range(16):
        data = nodes[i]
        tree.insert(data)
    print2DUtil(tree.head)
    heap = Heap(nodes)
    heap.heapsort()
    heap.print()
