import re
import os
from pathlib import Path
from pathlib import WindowsPath
from typing import Optional, List


class DirectoryTree:
    """export pretty and readable directory or file tree list."""

    def __init__(self,
                 directory_name: str = None,
                 directory_path: str = '.',
                 ignore_list: Optional[List[str]] = None):
        self.owner: WindowsPath = Path(directory_path)
        self.owner_path: str = directory_path.replace('\\', '/')
        if directory_name is None:
            directory_name = self.owner_path
        self.tree: str = directory_name + '/\n'
        self.dir_tree: str = directory_name + '/\n'
        self.ignore_list = ignore_list
        if ignore_list is None:
            self.ignore_list = []
        self.directory_ergodic(path_object=self.owner_path, n=0)

    def structure_tree(self, path_object: WindowsPath, depth=0, last=False, last_dir=False):
        if depth > 0:
            if last:
                self.tree += '│' + ('    │' * (depth - 1)) + '    └────' + path_object
            else:
                self.tree += '│' + ('    │' * (depth - 1)) + '    ├────' + path_object
        else:
            if last:
                self.tree += '└' + ('──' * 2) + path_object
            else:
                self.tree += '├' + ('──' * 2) + path_object
        if os.path.isfile(path_object):
            self.tree += '\n'
            return False
        elif os.path.isdir(path_object):
            self.tree += '/\n'

            if depth > 0:
                if last_dir:
                    self.dir_tree += '│' + ('    │' * (depth - 1)) + '    └────' + path_object
                else:
                    self.dir_tree += '│' + ('    │' * (depth - 1)) + '    ├────' + path_object
            else:
                if last_dir:
                    self.dir_tree += '└' + ('──' * 2) + path_object
                else:
                    self.dir_tree += '├' + ('──' * 2) + path_object

            self.dir_tree += '/\n'
            return True

    def filter_file(self, file):
        for item in self.ignore_list:
            if re.fullmatch(item, file):
                return False
        return True

    def directory_ergodic(self, path_object: WindowsPath, n=0):
        children: list = []
        for child in os.listdir(path_object):
            try:
                combine_path = path_object + '/' + child
                children.append(combine_path)
            except PermissionError:
                pass

        dir_file: list = children
        dir_count: int = 0
        counter: int = 0

        for path in dir_file:
            if os.path.isdir(path):
                dir_count += 1

        dir_file.sort(key=lambda x: x.lower())
        dir_file = [f for f in filter(self.filter_file, dir_file)]
        for i, item in enumerate(dir_file):
            if os.path.isdir(item):
                counter += 1

            if i + 1 == len(dir_file):
                if self.structure_tree(item, n, last=True, last_dir=counter == dir_count):
                    self.directory_ergodic(item, n + 1)
            else:
                if self.structure_tree(item, n, last=False, last_dir=counter == dir_count):
                    self.directory_ergodic(item, n + 1)
