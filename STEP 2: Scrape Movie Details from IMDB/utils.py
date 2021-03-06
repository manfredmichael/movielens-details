import functools

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        try:
            value = func(*args, **kwargs)
            return value
        except Exception as e:
            print(f"Error caught on {func.__name__}: {e}")           # 4
    return wrapper_debug
