import os
import shutil


def generate_path(*paths)->str:
    path = os.path.join(*paths)
    return path


def make_pythonic_name(fname_with_spaces: str)->str:
    names = fname_with_spaces.strip().split(' ')
    py_fname = '_'.join([n.lower() for n in names])
    return py_fname


def make_java_class_name(pythonic_fname: str)->str:
    names = pythonic_fname.split('_')
    java_fname = ''.join([n.capitalize() for n in names])
    return java_fname


def make_title_name(pythonic_fname: str)->str:
    names = pythonic_fname.split('_')
    title_name = ' '.join([n.capitalize() for n in names])
    return title_name


def copy_files(src_dir, dst_dir, ext='java'):
    file_list = [f for f in os.listdir(src_dir) if f.endswith('.' + ext)]
    for file in file_list:
        shutil.copy(os.path.join(src_dir, file), os.path.join(dst_dir, file))


def copy_file(src, dst):
    shutil.copy(src, dst)


def copy_dir(src, dst):
    shutil.copytree(src, dst)


def del_file(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass


def del_files(from_dir, ext='class'):
    file_list = [f for f in os.listdir(from_dir) if f.endswith('.' + ext)]
    for f in file_list:
        os.remove(os.path.join(from_dir, f))


def delete_dir(target):
    # clean up all files in directory
    shutil.rmtree(target, ignore_errors=True)
    # print('temp files cleaned up.')


def empty_dir(target):
    for f in os.listdir(target):
        target = os.path.join(target, f)
        if os.path.isdir(target):
            delete_dir(target)
        else:
            del_file(target)


def move_dir(src, dst):
    shutil.move(src, dst)
