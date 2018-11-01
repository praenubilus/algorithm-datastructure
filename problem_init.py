import argparse as ap
import os
import shutil
import _commons.python.file_util as fu


##################################
# Input Arguments for the script
##################################

parser = ap.ArgumentParser(description='Problem infrastructure generator.')
parser.add_argument('-d', '--directory', required=True, dest='problem_directory',
                    help="the target directory where the generated problem directory will be")
parser.add_argument('-n', '--name', required=True, dest='problem_name', default="",
                    help="the name of the problem")
parser.add_argument('-ln', '--lintcode-id', dest='lintcode_id', default="",
                    help="the id number of question on lintcode")
parser.add_argument('-lc', '--leetcode-id', dest='leetcode_id', default="",
                    help="the id number of question on leetcode")
parser.add_argument('-t', '--tag', dest='problem_tags', nargs='+',
                    help="the tags for the problem")
parser.add_argument('-c', '--company', dest='problem_company', nargs='+',
                    help="the company names who use this question")
parser.add_argument('-lcl', '--leetcode-link', dest='leetcode_link', default="",
                    help="the problem link on leetcode")
parser.add_argument('-lnl', '--lintcode-link', dest='lintcode_link', default="",
                    help="the problem link on lintcode")


PROBLEM_TEMPLATE_DIR = fu.generate_path(
    '_commons', '_templates', 'problem_template')
PYTHON_INIT_FILE_NAME = '__init__.py'
PYTHON_INIT_TEMPLATE_PATH = fu.generate_path(
    '_commons', 'python', PYTHON_INIT_FILE_NAME)
PYTHON_SOLUTION_TEMPLATE = 'solution_template'
PYTHON_TEST_TEMPLATE = 'test_solution_template'
PYTHON_LINE_COMMENT_INITIAL = '# '
JAVA_SOLUTION_TEMPLATE = 'SolutionTemplate'
JAVA_TEST_TEMPLATE = 'TestSolutionTemplate'


args = parser.parse_args()

##################################
# Input Arguments for the script
##################################


def main():
    problem_parent_dir = args.problem_directory
    problem_name = fu.make_pythonic_name(args.problem_name)
    ln_id = args.lintcode_id
    lc_id = args.leetcode_id
    problem_tags = args.problem_tags
    problem_companies = args.problem_company
    problem_link = args.leetcode_link

    # create target directory
    problem_dir = create_dir_from_template(
        target_dir=problem_parent_dir, problem_name=problem_name)
    # cleanup for cache files and initialization
    directory_init(problem_dir)

    # Python template update
    update_python_template(problem_dir, problem_name)
    # Java template update
    update_java_template(problem_dir, fu.make_java_class_name(problem_name))

    # README template update


def update_java_template(target_dir: str, name: str):
    sol_file_dir = fu.generate_path(target_dir, 'java')
    # write contents to new solution file with name based on problem name
    # the format is CamelCase(Egyptian Style) for name, then preppend to the 'Solution'
    new_sol_name = name+'Solution'

    # 1. processing solution file
    sol_file_path = fu.generate_path(
        sol_file_dir, JAVA_SOLUTION_TEMPLATE+'.java')
    with open(sol_file_path, 'r') as file:
        data = file.readlines()

    # create new list in case delete on iterating
    output = []
    for idx, content in enumerate(list(data)):
        # java public class name must match the file name, rename the solution class
        if JAVA_SOLUTION_TEMPLATE in content:
            content = content.replace(JAVA_SOLUTION_TEMPLATE, new_sol_name)
        output.append(content)
    # rename the solution file name
    new_sol_fpath = fu.generate_path(sol_file_dir, new_sol_name+'.java')
    with open(new_sol_fpath, 'w') as file:
        file.writelines(output)

    # 2. processing unit test file
    test_file_dir = sol_file_dir
    test_file_path = fu.generate_path(
        test_file_dir, JAVA_TEST_TEMPLATE+'.java')
    with open(test_file_path, 'r') as file:
        data = file.readlines()

    # write contents to new solution file with name based on problem name
    # the format is CamelCase(Egyptian Style) for name, then append to the 'Test'
    new_test_name = 'Test'+new_sol_name

    # create new list in case delete on iterating
    output = []
    for idx, content in enumerate(list(data)):
        # java public class name must match the file name, rename the solution class
        if JAVA_SOLUTION_TEMPLATE in content:
            content = content.replace(JAVA_SOLUTION_TEMPLATE, new_sol_name)
        if JAVA_TEST_TEMPLATE in content:
            content = content.replace(JAVA_TEST_TEMPLATE, new_test_name)
        output.append(content)

    new_test_fpath = fu.generate_path(test_file_dir, new_test_name+'.java')
    with open(new_test_fpath, 'w') as file:
        file.writelines(output)

    # 3. clean up, delete the old template files
    fu.del_file(sol_file_path)
    fu.del_file(test_file_path)


def update_python_template(target_dir: str, name: str):
    sol_file_dir = fu.generate_path(target_dir, 'python')

    # 1. processing solution file
    sol_file_path = fu.generate_path(
        sol_file_dir, PYTHON_SOLUTION_TEMPLATE+'.py')
    with open(sol_file_path, 'r') as file:
        data = file.readlines()

    # create new list in case delete on iterating
    output = []
    line_starts = len(PYTHON_LINE_COMMENT_INITIAL)
    for idx, content in enumerate(list(data)):
        # python template is commented out by default, comment it back for each line
        if content.lower().startswith(PYTHON_LINE_COMMENT_INITIAL):
            content = content[line_starts:]
        output.append(content)

    # write contents to new solution file with name based on problem name
    # the format is get the initial of each problem word name, then append to the 'solution_'
    new_sol_name = 'solution_'+''.join(w[0] for w in name.split('_'))
    new_sol_fpath = fu.generate_path(sol_file_dir, new_sol_name+'.py')
    with open(new_sol_fpath, 'w') as file:
        file.writelines(output)

    # 2. processing unit test file
    test_file_dir = sol_file_dir
    test_file_path = fu.generate_path(
        test_file_dir, PYTHON_TEST_TEMPLATE+'.py')
    with open(test_file_path, 'r') as file:
        data = file.readlines()

    # create new list in case delete on iterating
    output = []
    line_starts = len(PYTHON_LINE_COMMENT_INITIAL)
    for idx, content in enumerate(list(data)):
        # python template is commented out by default, comment it back for each line
        if content.lower().startswith(PYTHON_LINE_COMMENT_INITIAL):
            content = content[line_starts:]
        if PYTHON_SOLUTION_TEMPLATE in content:
            content = content.replace(PYTHON_SOLUTION_TEMPLATE, new_sol_name)
        output.append(content)

    # write contents to new solution file with name based on problem name
    # the format is get the initial of each problem word name, then append to the 'test_solution_'
    new_test_name = 'test_'+new_sol_name
    new_test_fpath = fu.generate_path(test_file_dir, new_test_name+'.py')
    with open(new_test_fpath, 'w') as file:
        file.writelines(output)

    # 3. clean up, delete the old template files
    fu.del_file(sol_file_path)
    fu.del_file(test_file_path)


def update_readme_template():
    # edit content
    with open(readme_file_path, 'r') as file:
        data = file.readlines()

    line_num = 0
    for line in list(data):  # create new list in case delete on iterating
        if line.lower().startswith('tags:'):  # this line contains all tags
            if problem_tags is not None:  # add all tags
                line = 'Tags:'
                for tag in problem_tags:
                    line += ' __' + tag + '__,'
            if problem_companies is not None:  # add company tags
                for company in problem_companies:
                    line += ' __' + company + '__,'

            data[line_num] = line[:-1]

        if line.lower().startswith('# brief intro'):
            if problem_id is not None:
                # edit File Title to problem name
                data[line_num] = '# ' + problem_id + '. ' + problem_name + '\n'
            else:
                data[2] = '# ' + problem_name + '\n'

        if 'leetcode qxxx' in line:
            if problem_link is not None:
                line = line.replace('https://www.google.com', problem_link)
            if problem_id is not None:
                line = line.replace('qxxx', ('' + problem_id).zfill(3))

            data[line_num] = line
            # delete the 'from CCI page xxx' line, all following lines will reduce number by 1
            del data[line_num - 1]

        line_num += 1

    # and write everything back
    with open(readme_file_path, 'w') as file:
        file.writelines(data)


def directory_init(target_dir: str, init_python: bool = True, init_java: bool = False):
    """ At every level from bottom to top of the target directory, cleanup cache directory and
    do initialization work. In current implementation, only python related cache directory, '__pycache__'
    will be cleaned up and python module related '__init__.py' file will be injected.
    """
    if init_java:
        # currently there is no java initialization and cleanup requirements
        pass
    if init_python:
        tmp_target_path = fu.generate_path(target_dir, 'python')
        cache_dir_name = '__pycache__'
        while tmp_target_path:
            cache_path = fu.generate_path(tmp_target_path, cache_dir_name)
            # delete cache directory if exists
            if os.path.isdir(cache_path):
                fu.delete_dir(cache_path)
            init_path = fu.generate_path(
                tmp_target_path, PYTHON_INIT_FILE_NAME)
            # inject init file if not exists
            if not os.path.isfile(init_path):
                fu.copy_file(PYTHON_INIT_TEMPLATE_PATH, init_path)

            # move directory being worked on to upper level
            tmp_target_path = os.path.split(tmp_target_path)[0]


def create_dir_from_template(target_dir: str, problem_name: str)->str:
    """ Create a directory based on given problem name and target directory. A copy of
    the preset template will be generated inside the target directory with a pythonic
    directory name. e.g. <dir_name_for_problem>

    """
    problem_target_dir = fu.generate_path(target_dir, problem_name)
    # copy the template to target directory
    fu.copy_dir(PROBLEM_TEMPLATE_DIR, problem_target_dir)

    return problem_target_dir


if __name__ == '__main__':
    main()
