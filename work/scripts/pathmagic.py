"""
    Path hack to make everything work
"""
import os
import sys


class Context:
    """
        Class to make imports work
    """
    def __enter__(self):
        """
            Initialize context manager
        """
        module_path = os.path.abspath(os.getcwd() + '\\..\\..')
        if module_path not in sys.path:
            sys.path.append(module_path)

    def __exit__(self, *args):
        """
            Turn down context manager
        """
        pass
