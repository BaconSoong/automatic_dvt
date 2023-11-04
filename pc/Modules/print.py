import inspect


class Print:
    @staticmethod
    def custom_print(*args, **kwargs):
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename
        line_no = frame.f_lineno
        func_name = frame.f_code.co_name
        print(f"\n[{filename}:{line_no} {func_name}] ", end="")
        print(*args, **kwargs)
