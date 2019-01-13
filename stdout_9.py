import sys
import io


class MyBuffer:
    def __init__(self):
        self.original_stdout = sys.stdout

    def __enter__(self):
        self.open_buffer = io.StringIO()
        sys.stdout = self.open_buffer
        # self.open_file = open(self.filename, self.mode)
        # return self.open_buffer

    def __exit__(self, *args):
        self.open_buffer.close()
        return self.original_stdout


def main():
    sys.stdout.write('foo')
    with MyBuffer() as outfile:
        sys.stdout.write('foo')
        # outfile.write('foo')
        print(outfile.read())


if __name__ == '__main__':
    main()
