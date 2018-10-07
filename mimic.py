from sys import stdout


class Node:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


class MyList:
    def __init__(self):
        self.start = Node('start', None, None)
        self.end = Node('end', self.start, None)
        self.start.next = self.end
        self.list_len = 0

    def append(self, val):
        new_node = Node(val, self.end.prev, self.end)
        self.end.prev.next = new_node
        self.end.prev = new_node
        self.list_len += 1

    def print(self):
        stdout.write('[')
        node = self.start.next
        while node != self.end:
            stdout.write('{},'.format(node.value))
            node = node.next
        stdout.write('\b]\n')

    def find_index(self, position):  # Utility function
        if (position > self.list_len - 1) or (position < 0):
            print('invalid index')
            return None
        current_position = 0
        node = self.start.next
        while current_position < position:
            node = node.next
            current_position += 1
        return node

    def return_value(self, position):
        node = self.find_index(position)
        if node is None:
            return
        return node.value

    def remove(self, position):
        node = self.find_index(position)
        if node is None:
            return
        node.prev.next = node.next
        node.next.prev = node.prev
        self.list_len -= 1

    def return_length(self):
        return self.list_len


lst = MyList()
lst.append(5)
lst.append('a')
lst.append(7)
lst.print()
print(lst.return_value(3))
lst.remove(1)
print(lst.return_length())
lst.print()