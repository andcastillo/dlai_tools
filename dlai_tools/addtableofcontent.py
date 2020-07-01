import json


def addtoc(input, mark):
    try:
        with open(input) as f:
            notebook = json.load(f)

        # The special marks @ASSIGNMENT, @SOLUTION and @UNIT_TEST
        # must be at the first or second lines
        # For the solution notebook
        cells = notebook['cells']

        head_cell = cells[0]
        '''
         "cell_type": "markdown",
            "metadata": {
                "colab_type": "text",
                "id": "C7oVbe_pLr3C"
            },
            "source": [
                "# Notebook example\n",
                "\n",
                "We start with a full notebook"
            ]
            },
        '''

        for cell in cells[1: len(cells)]:
            if cell['cell_type'] == 'markdown':
                source = ''.join(cell['source'])
                if source.find('# Part [0-9]+:') >= 0:
                    # TODO

                if source.find('## [0-9]+.[0-9]+ ') >= 0:
                    # TODO
                if source.find('### Exercise') >= 0:
                    # TODO

        with open(input.replace('.ipynb', '_toc.ipynb'), 'w') as file:
            file.write(json.dumps(notebook, indent=2))

    except ValueError:
        print("Error during deployment")
        print(ValueError)
