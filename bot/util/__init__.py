class Hook:
    """Functions to register functions with commands
    and execute them at will"""

    def _command(func, *args):
      self.commands[func.func_name] = func(*args)
      return func

    def __init__(self):
      self.commands = dict()
