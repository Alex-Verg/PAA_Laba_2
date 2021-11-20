class Node:

    def __init__(self, val):
        self.left = None
        self.right = None
        self.value = val
        self.height = 1

    def _str(self):
        return "%d" % self.value

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.value
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.value
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class BTree:

    def __init__(self):
        self.head = None
        self.size = 0
        self.deep = 0
        self.values_list = []

    def __len__(self):
        return self.size

    def insert(self, data):
        self.values_list.append(data)
        root = self.head
        if not root:
            self.head = Node(data)
            self.size += 1
            self.deep = 0
        d = 0
        while root:
            d += 1
            if data < root.value:
                if not root.left:
                    root.left = Node(data)
                    self.size += 1
                    if d > self.deep:
                        self.deep = d
                    return
                else:
                    root = root.left
            elif data == root.value:
                return
            elif data > root.value:
                if not root.right:
                    root.right = Node(data)
                    self.size += 1
                    if d > self.deep:
                        self.deep = d
                    return
                else:
                    root = root.right

    def height(self, node):
        return node.height if node else 0

    def bfactor(self, node):
        return self.height(node.right) - self.height(node.left)

    def fix_height(self, node):
        hl = self.height(node.left)
        hr = self.height(node.right)
        node.height = (hl if hl > hr else hr) + 1

    def right_rot(self, node):
        q = node.left
        node.left = q.right
        q.right = node
        self.fix_height(node)
        self.fix_height(q)
        return q

    def left_rot(self, node):
        q = node.right
        node.right = q.left
        q.left = node
        self.fix_height(node)
        self.fix_height(q)
        return q

    def balance(self, node):
        self.fix_height(node)
        bf = self.bfactor(node)
        if bf >= 2:
            if self.bfactor(node.right) < 0:
                node.right = self.right_rot(node.right)
            node = self.left_rot(node)
            return node, True
        elif bf <= -2:
            if self.bfactor(node.left) > 0:
                node.left = self.left_rot(node.left)
            node = self.right_rot(node)
            return node, True
        return node, False

    def rebalance(self, node):
        global step
        if node is None:
            return None, False
        else:
            node.left, pr = self.rebalance(node.left)
            if pr:
                print(f"Крок {step}. Балансування вершини {pr}:")
                tree.print_tree()
                step += 1
            node.right, pr = self.rebalance(node.right)
            if pr:
                print(f"Крок {step}. Балансування вершини {pr}:")
                tree.print_tree()
                step += 1
            n, pr = self.balance(node)
            if pr:
                return n, node.value
            else:
                return n, pr

    def print_tree(self):
        self.head.display()
        print("\n\n")


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
        print("\n", *self.list)


if __name__ == "__main__":
    tree = BTree()
    nodes = [15, 28, 27, 9, 19, 6, 26, 29, 8, 18, 2, 20, 23, 21, 4, 17]
    for i in range(16):
        data = nodes[i]
        tree.insert(data)
    print("Утворене двійкове дерево без балансування:\n")
    tree.print_tree()

    step = 1
    print("Балансування раніше створеного дерева:\n")
    tree.head, pr = tree.rebalance(tree.head)
    if pr:
        print(f"Крок {step}. Балансування вершини {pr}:")
        tree.print_tree()
        step += 1
    tree.head, _ = tree.rebalance(tree.head)
    print("Збалансоване за висотою дерево:")
    tree.print_tree()

    print("Вершини дерева після пірамідального сортування:")
    heap = Heap(nodes)
    heap.heapsort()
    heap.print()
