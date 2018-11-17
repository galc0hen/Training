class Number(int):

    def __init__(self, num):
        super().__init__()
        self.num = num

    # Utility Function.
    def find_divider_by_index(self, index, current_index, current_divider):
        while current_index < index:
            current_divider += 1
            if current_divider > self.num:
                return None, None
            if self.num % current_divider == 0:
                current_index += 1
        return current_index, current_divider

    # Utility Function.
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
            return self.find_divider_by_index(index, 0, 1)[1]
        if type(index) == slice:
            return self.find_dividers_by_slice(index.start, index.stop)

    def __contains__(self, divider):
        if divider == 0:
            return False
        if self.num % divider == 0:
            return True
        return False


def main():
    example_number = Number(15)  # Example number is 15.
    print(example_number[0])  # Return the first divider of 15 (1).
    print(example_number[1])  # Return the second divider of 15 (3).
    print(example_number[3])  # Return the forth divider of 15 (15).
    print(example_number[4])  # Return the fifth divider of 15 (None).
    print(4 in example_number)  # True if 4 is a divider of 15 (False).
    print(3 in example_number)  # True if 3 is a divider of 15 (True).
    print(example_number[1:3])  # Return the 2nd to 4th dividers of 15 (3, 5 are the 2nd and 3rd dividers).


if __name__ == '__main__':
    main()
