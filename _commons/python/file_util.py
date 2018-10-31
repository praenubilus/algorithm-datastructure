import os
import shutil


def copy_files(src_dir, dst_dir, ext='java'):
    file_list = [f for f in os.listdir(src_dir) if f.endswith('.' + ext)]
    for file in file_list:
        shutil.copy(os.path.join(src_dir, file), os.path.join(dst_dir, file))


def copy_file(src, dst):
    shutil.copy(src, dst)


def copy_folder(src, dst):
    shutil.copytree(src, dst)


def del_file(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass


def del_files(from_folder, ext='class'):
    file_list = [f for f in os.listdir(from_folder) if f.endswith('.' + ext)]
    for f in file_list:
        os.remove(os.path.join(from_folder, f))


def delete_folder(target_dir):
    # clean up all files in folder
    shutil.rmtree(target_dir, ignore_errors=True)
    # print('temp files cleaned up.')


def empty_folder(target_dir):
    for f in os.listdir(target_dir):
        target = os.path.join(target_dir, f)
        if os.path.isdir(target):
            delete_folder(target)
        else:
            del_file(target)


def move_folder(src, dst):
    shutil.move(src, dst)
