import json
import re


def deploy_assignment(input, keep_unit_tests=True):
    ''' Creates the Assignment and the Solution notebooks from a development notebook.
    The function will create new files in the same folder where the input is located.
    Args:
        'input' (str): The path to the _dev.ipynb notebook.
        'keep_unit_tests' (bool): Keep unit tests in the assignments notebook?
    Examples:
        'deploy_assignment("C1_W1_Assignment_dev.ipynb", True)'
        # Produces: 'C1_W1_Assignment.ipynb'
                    'C1_W1_Assignment_Solution.ipynb'
    '''

    try:
        with open(input) as f:
            nb_solution = json.load(f)

        with open(input) as f:
            nb_assignment = json.load(f)

        # The special marks @ASSIGNMENT, @SOLUTION and @UNIT_TEST
        # must be at the first or second lines
        # For the solution notebook
        cells = nb_solution['cells']
        for cell in cells:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                if source.find('# @ASSIGNMENT') >= 0:
                    cells.remove(cell)

        if (input.find('_Dev')):
            with open(input.replace('_Dev', '_Solution'), 'w') as file:
                file.write(json.dumps(nb_solution, indent=2))
        else:
            with open(input.replace('.ipynb', '_Solution.ipynb'), 'w') as file:
                file.write(json.dumps(nb_solution, indent=2))

        # For the assignment notebook
        cells2 = nb_assignment['cells']
        for cell in cells2:
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                if source.find('# @SOLUTION') >= 0:
                    cells2.remove(cell)
                else:
                    if not keep_unit_tests:
                        if source.find('# @UNIT_TEST') >= 0:
                            cells2.remove(cell)
        if (input.find('_Dev')):
            with open(input.replace('_Dev', '_'), 'w') as file:
                file.write(json.dumps(nb_assignment, indent=2))
        else:
            with open(input.replace('.ipynb', '_Assignment.ipynb'), 'w') as file:
                file.write(json.dumps(nb_assignment, indent=2))

    except ValueError:
        print("Error during deployment")
        print(ValueError)


def add_toc(input):
    """ Function to include a table of content on a jupyter notebook based on its
        markdown. It receives a file path as input, and creates a new notebook
        file that includes the table of content in the same path.
        It performs some style fix during the process. For more information see
        the attached notebook example.

    Args:
        input ([strin]): The notebook file to be formated
    """
    try:
        with open(input) as f:
            notebook = json.load(f)

        cells = notebook['cells']

        head_cell = cells[0]

        part = 0
        section = 0
        exercise = 0

        toc = ['\n', '## Outline\n']

        for cell in cells[1: len(cells)]:
            if cell['cell_type'] == 'markdown':
                source_array = cell['source']
                row = 0
                skip = False
                for source in source_array:
                    if not skip:
                        if re.search('^[#]+ Introduction', source, re.IGNORECASE):
                            source_array.insert(row, '<a name="0"></a>\n')
                            toc.append('- [Introduction](#0)\n')
                            source_array[row + 1] = '# Introduction\n'
                            skip = True

                        if isPart(source):
                            part += 1
                            name = partName(source)
                            source_array.insert(
                                row, '<a name="' + str(part) + '"></a>\n')
                            toc.append('- [Part ' + str(part) + ': ' +
                                       name + '](#' + str(part) + ')\n')
                            # Fix source line if needed
                            source_array[row + 1] = '# Part' + \
                                str(part) + ': ' + name + '\n'

                            section = 1
                            skip = True

                        if re.search('^## [0-9]+.[0-9]+', source, re.IGNORECASE):
                            label = str(part) + '.' + str(section)
                            name = sectionName(source)
                            source_array.insert(
                                row, '<a name="' + label + '"></a>\n')
                            toc.append(
                                '    - [' + label + ' ' + name + '](#' + label + ')\n')

                            # Fix source line if needed
                            source_array[row + 1] = '## ' + \
                                label + ' ' + name + '\n'

                            section += 1
                            skip = True

                        if re.search('^### Exercise', source, re.IGNORECASE):
                            exercise += 1
                            label = "{:02d}".format(exercise)
                            source_array.insert(
                                row, '<a name="ex' + label + '"></a>\n')
                            toc.append(
                                '        - [Exercise ' + label + '](#ex' + label + ')\n')

                            source_array[row +
                                         1] = '### Exercise ' + label + '\n'
                            skip = True
                    else:
                        skip = False
                    row += 1
            # Clear outputs and reset the execution count
            if cell['cell_type'] == 'code':
                cell['execution_count'] = 0
                cell['outputs'] = []

        # Remove the old toc
        toc_line = 0
        for line in head_cell['source']:
            if re.search('^## Outline', line, re.IGNORECASE):
                head_cell['source'] = head_cell['source'][0: toc_line]
                break
            toc_line += 1

        head_cell['source'] = head_cell['source'] + toc

        with open(input.replace('.ipynb', '_toc.ipynb'), 'w') as file:
            file.write(json.dumps(notebook, indent=2))

    except ValueError:
        print("Error during deployment")
        print(ValueError)


def isPart(line):
    if re.search('^# Part [0-9]+:', line, re.IGNORECASE) \
            or re.search('^# [0-9]+', line, re.IGNORECASE):
        return True
    return False


def partName(line):
    title_search = re.search('^# Part [0-9]+:', line, re.IGNORECASE)
    if title_search:
        return re.sub(r'# Part [0-9]+:', '', line).replace('\n', '')

    else:
        title_search = re.search('^# [0-9]+', line, re.IGNORECASE)
        if title_search:
            return re.sub(r'# [0-9]+', '', line).replace('\n', '')


def sectionName(line):
    title_search = re.search('^## [0-9]+.[0-9]+', line, re.IGNORECASE)
    if title_search:
        return re.sub(r'## [0-9]+.[0-9]+', '', line).replace('\n', '')
