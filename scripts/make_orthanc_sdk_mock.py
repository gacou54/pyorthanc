def make_function(function: str) -> str:
    function = function.replace('Function ', '')
    name = function.split('\n')[0].strip()
    documentation = function.split('\n')[1].replace('Documentation: ', '').strip()

    return f'''
def {name.replace('()', '(*args)')}
    """{documentation}"""
    pass
'''


def make_class(class_str: str) -> str:
    class_str = class_str.replace('Class ', '')
    elements = class_str.split('\n')
    name = elements[0].strip()
    documentation = elements[1].replace('Documentation: ', '').strip()

    if _is_enum(class_str):
        enum_elements = [e.replace('- Enumeration value ', '  ') for e in elements[2:]]
        enum_elements = [e.replace(':', ' =') for e in enum_elements]

        elements_as_str = '\n'.join(enum_elements)
        return f'''
class {name.replace(':', '(Enum):')}
    """{documentation}"""
{elements_as_str} 
'''

    methods = elements[2:]
    methods = [m.replace('- Method ', '  def ') for m in methods]
    methods = [m.replace('()', '(self, *args)', 1) for m in methods]
    methods = [m.replace(': ', ':\n') for m in methods]
    methods = [m.replace('\n', '\n        """') + '"""' for m in methods]

    methods = [m + '\n        pass' for m in methods]

    methods_as_str = '\n\n'.join(methods)

    return f'''
class {name}
    """{documentation}"""

{methods_as_str}
'''


def _is_enum(class_str: str) -> bool:
    return 'enumeration' in class_str.split('\n')[1].lower()


with open('./scripts/data/python-sdk.txt') as file:
    content = file.read()

sections = content.split('\n\n')

functions = [s for s in sections if s[:8] == 'Function']
classes = [s for s in sections if s[:5] == 'Class']

functions_code = '\n'.join([make_function(f) for f in functions])
classes_code = '\n'.join([make_class(c) for c in classes])

python_code = f'''
"""{sections[0].replace('-', '')}"""
from enum import Enum

{functions_code}
{classes_code}
'''

with open('pyorthanc/orthanc_sdk.py', 'w') as file:
    file.write(python_code)
