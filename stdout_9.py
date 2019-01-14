import sys
import io


class MyBuffer:
    def __init__(self):
        self.original_stdout = sys.stdout

    def __enter__(self):
        self.open_buffer = io.StringIO()
        sys.stdout = self.open_buffer
        return self.open_buffer

    def __exit__(self, *args):
        self.open_buffer.close()
        sys.stdout = self.original_stdout


def main():
    with MyBuffer() as buffer_output:
        print('test output')  # Does not print to screen - the output goes to buffer.
        output_inside_context_manager = buffer_output.getvalue()
    # Print 'test output' outside the context manager.
    print(f'Printing the buffer output outside the context manager: {output_inside_context_manager}')


if __name__ == '__main__':
    main()
