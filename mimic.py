DELIMITER = ', '


class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node


class MyList:
    def __init__(self):
        self.start_pointer = None
        self.end_pointer = None
        self.list_len = 0

    def append(self, val):
        new_node = Node(val, None)
        if self.start_pointer is None:
            self.start_pointer = new_node
        if self.end_pointer is None:
            self.end_pointer = new_node
        else:
            self.end_pointer.next_node = new_node
            self.end_pointer = new_node
        self.list_len += 1

    def __repr__(self):
        if self.start_pointer is None:
            list_to_print = '[]'
            return list_to_print
        list_to_print = '['
        node = self.start_pointer
        while node.next_node is not None:
            list_to_print = list_to_print + str(node.value) + DELIMITER
            node = node.next_node
        list_to_print = list_to_print + str(self.end_pointer.value) + ']'
        return list_to_print

    # Utility function.
    def find_node(self, index):
        if (index > self.list_len - 1) or (index < 0):
            return None
        current_index = 0
        node = self.start_pointer
        while current_index < index:
            node = node.next_node
            current_index += 1
        return node

    def index(self, value):
        curr_index = 0
        curr_node = self.start_pointer
        while curr_node is not None:
            if curr_node.value == value:
                return curr_index
            curr_node = curr_node.next_node
            curr_index += 1
        raise ValueError

    def __getitem__(self, position):
        node = self.find_node(position)
        if node is None:
            return
        return node.value

    def remove(self, index):
        """
        Remove node by index.
        """
        node = self.find_node(index)
        if node is None:
            return
        self.list_len -= 1
        if index == 0:
            self.start_pointer = node.next_node
            return
        previous_node = self.find_node(index - 1)
        previous_node.next_node = node.next_node

    def __len__(self):
        return self.list_len

    def __iter__(self):
        return MyListIterator(self.start_pointer, self.end_pointer)

    def sort(self):
        if self.list_len < 2:
            return
        temp_start_pointer = None
        temp_end_pointer = None
        unsorted_list_len = self.list_len
        while unsorted_list_len > 0:
            curr_node = self.start_pointer
            curr_index = 0
            min_value = self.start_pointer.value
            min_value_index = 0
            while curr_node is not None:  # Search next min value.
                if curr_node.value < min_value:
                    min_value = curr_node.value
                    min_value_index = curr_index
                curr_node = curr_node.next_node
                curr_index += 1
            node_to_append = self.find_node(min_value_index)
            previous_node = self.find_node(min_value_index - 1)
            if temp_start_pointer is None:  # For first node in new list, initialize start pointer.
                temp_start_pointer = node_to_append
            if temp_end_pointer is not None:  # Append current node to last node in new list.
                temp_end_pointer.next_node = node_to_append
            if previous_node is not None:  # Remove current node from original list.
                previous_node.next_node = node_to_append.next_node
            if min_value_index == 0:  # Reinitialize original start pointer if we remove first node from original list.
                self.start_pointer = node_to_append.next_node
            temp_end_pointer = node_to_append
            node_to_append.next_node = None
            unsorted_list_len -= 1
        self.start_pointer = temp_start_pointer
        self.end_pointer = temp_end_pointer


class MyListIterator:
    def __init__(self, start, end):
        self.index = start
        self.end_index = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.index is None:
            raise StopIteration
        node_value = self.index.value
        self.index = self.index.next_node
        return node_value


def main():
    lst = MyList()
    lst.append(7)
    lst.append(9)
    lst.append(2)
    print(f'print list - expecting [7, 9, 2]: {lst}')  # Expected output: [7, 9, 2].
    lst.sort()
    print(f'print list - expecting sorted list [2, 7, 9]: {lst}')  # Expected output: [2, 7, 9] (sorted list).
    print(f'print index of list element 7 - expecting output 1: {lst.index(7)}')  # Expected output: 1.
    print(f'print list element in index 0 - expecting output 2: {lst[0]}')  # Expected output: 2.
    print('print first "for" loop - expecting "2 7 9":')
    for item in lst:
        print(item, end=' ')
    print('\nprint second "for" loop - expecting "7 9":')
    for i in range(1, 3):
        print(lst[i], end=' ')
    print('\n')
    lst.remove(1)
    print(f'print list after removing element - expecting [2, 9]: {lst}')  # Expected output: [2, 9].
    print(f'print list length - expecting 2: {len(lst)}')   # Expected output: 2.


if __name__ == '__main__':
    main()
