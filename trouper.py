class Number(int):

    def __init__(self, num):
        int.__init__(self)
        self.num = num

    # Utility Function
    def find_divider_by_index(self, index, current_index, current_divider):
        while current_index < index:
            current_divider += 1
            if current_divider > self.num:
                return None, None
            if self.num % current_divider == 0:
                current_index += 1
        return current_index, current_divider

    # Utility Function
    def find_dividers_by_slice(self, start_index, end_index):
        result = []
        current_divider = 1
        current_index = 0
        index = start_index
        while index < end_index:
            current_index, current_divider = self.find_divider_by_index(
                index, current_index, current_divider)
            if current_divider is None:
                return result
            result.append(current_divider)
            index += 1
        return result

    def __getitem__(self, index):
        if type(index) == int:
            index, divider = self.find_divider_by_index(index, 0, 1)
            return divider
        elif type(index) == slice:
            return self.find_dividers_by_slice(index.start, index.stop)

    def __contains__(self, divider):
        if divider == 0:
            return False
        if self.num % divider == 0:
            return True
        else:
            return False


a = Number(15)
print(a[2])
print(4 in a)
print(a[1:3])
