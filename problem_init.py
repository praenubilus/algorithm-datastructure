import argparse as ap
import os
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
parser.add_argument('-tt', '--template-type', dest='template_type', default="pythonjava",
                    help="the types of template script will generate")


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
README_TEMPLATE = 'README.md'
README_TEMPLATE_TITLE = "Problem Name"
README_TEMPLATE_SOURCE = "Source"
README_TEMPLATE_TAG = "Tags"
README_TEMPLATE_COMPANY = "Company"
README_TEMPLATE_DESCRIPTION = "Description"
QUESTION_NUMBER_ZEROS = 4

args = parser.parse_args()

##################################
# Input Arguments for the script
##################################


def main():
    problem_parent_dir = args.problem_directory
    problem_name = fu.make_pythonic_name(args.problem_name)
    ln_id: str = args.lintcode_id
    lc_id: str = args.leetcode_id
    problem_tags = args.problem_tags
    problem_companies = args.problem_company
    leetcode_link = args.leetcode_link
    lintcode_link = args.lintcode_link
    template_type = args.template_type

    # format the problem number with unified format which have leading zeros
    if ln_id:
        ln_id = lc_id.zfill(QUESTION_NUMBER_ZEROS)
    if lc_id:
        lc_id = lc_id.zfill(QUESTION_NUMBER_ZEROS)

    # create target directory
    problem_dir = create_dir_from_template(
        target_dir=problem_parent_dir, problem_name=problem_name)
    # cleanup for cache files and initialization
    directory_init(problem_dir)

    # Python template update, by default, python will always generate
    update_python_template(problem_dir, problem_name)
    # Java template update
    # java can be omitted if it's not in template type
    if 'java' in template_type:
        update_java_template(
            problem_dir, fu.make_java_class_name(problem_name))
    else:
        fu.delete_dir(fu.generate_path(problem_dir, 'java'))

    # README template update
    update_readme_template(problem_dir,
                           fu.make_title_name(problem_name),
                           ln_id=ln_id,
                           lc_id=lc_id,
                           leetcode_link=leetcode_link,
                           lintcode_link=lintcode_link,
                           problem_tags=problem_tags,
                           problem_companies=problem_companies)


def update_readme_template(target_dir: str, name: str, **args):

    # 1. processing solution file
    readme_file_path = fu.generate_path(
        target_dir, README_TEMPLATE)
    with open(readme_file_path, 'r') as file:
        data = file.readlines()

    # create new list in case delete on iterating
    output = []
    valid_id_lc = True if args.get('ln_id', False) else False
    valid_source_lc = True if args.get('leetcode_link', False) else False
    valid_id_lin = True if args.get('lc_id', False) else False
    valid_source_lin = True if args.get('lintcode_link', False) else False
    valid_tags = True if args.get('problem_tags', False) else False
    valid_companies = True if args.get('problem_companies', False) else False

    for idx, content in enumerate(list(data)):

        # update Template Title name with Capitalized String
        if README_TEMPLATE_TITLE in content:
            content = content.replace(README_TEMPLATE_TITLE, name)

        if README_TEMPLATE_SOURCE in content:
            if valid_id_lin:
                if valid_source_lin:
                    content += "["
                content += "Lintcode "+args.get('ln_id')+". "+name
                if valid_source_lin:
                    content += "]({link})".format(link=args.get('lintcode_link'))
                content += '\n'
            if valid_id_lc:
                if valid_source_lc:
                    content += "["
                content += "Leetcode "+args.get('lc_id')+". "+name
                if valid_source_lc:
                    content += "]({link})".format(link=args.get('leetcode_link'))
                content += '\n'

        if README_TEMPLATE_TAG in content and valid_tags:
            content += ','.join([' **{tag}**'.format(tag=t)
                                 for t in args.get('problem_tags')])
            content += '\n'

        if README_TEMPLATE_COMPANY in content and valid_companies:
            content += ','.join([' **{comp}**'.format(comp=c)
                                 for c in args.get('problem_companies')])
            content += '\n'

        output.append(content)

    # and write everything back
    with open(readme_file_path, 'w') as file:
        file.writelines(output)


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
