from directoryTree import DirectoryTree

if __name__ == '__main__':
    ignore_list = ('.git', '$RECYCLE.BIN', '.svn', 'System Volume Information', '.sync', '.idea')
    tree = DirectoryTree(ignore_list=ignore_list, directory_path=r'E:\CloudMusic\Aimer')
    print('==================FileTree==================')
    print(tree.tree)
    print('==================DirTree==================')
    print(tree.dir_tree)
