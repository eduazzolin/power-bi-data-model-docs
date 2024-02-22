from openai import OpenAI
import time


class TableItem:
    """
    TableItem class to represent a column or measure in a table.
    """

    def __init__(self, table_item_id: str, name: str, table_item_type: str = 'column', data_type: str = None,
                 format_string: str = None,
                 display_folder: str = None, is_hidden: bool = False, expression: list = None):
        """
        Constructor of the class
        :param table_item_id: id of the table item
        :param name: name of the table item
        :param table_item_type: type of the table item, can be 'column', 'calculated' or 'measure'
        :param data_type: type of the data, e.g. 'String', 'Integer', 'date', etc.
        :param format_string: the format method for measures
        :param display_folder: the folder where the table item is displayed
        :param is_hidden: if the table item is hidden
        :param expression: the definition of the measure or calculated column. It is a list of string lines.
        """
        self.table_item_id: str = table_item_id
        self.name: str = name
        self.table_item_type: str = table_item_type
        self.data_type: str = data_type
        self.format_string: str = format_string
        self.display_folder: str = display_folder
        self.is_hidden: bool = is_hidden
        self.expression: list = expression

    def __str__(self):
        """
        Method to return a string representation of the table item
        :return: string
        """
        result = ''
        result += f'Name: {self.name}\n'
        result += f'Type: {self.table_item_type}\n'
        result += f'Data Type: {self.data_type}\n'
        result += f'Format String: {self.format_string}\n'
        result += f'Display Folder: {self.display_folder}\n'
        result += f'Is Hidden: {self.is_hidden}\n'
        result += f'Expression: {self.expression}\n'
        return result

    def generate_comment_openai(self):
        """
        Method to generate a comment for the table item using OpenAI's GPT-3.5
        :return: string
        """
        with open('model\\openai-key.txt', 'r') as file:
            client = OpenAI(api_key=file.read())

        expression = '\n'.join(self.expression)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Você responde de forma resumida em texto pleno sobre medidas dax e colunas calculadas do Power BI"},
                {"role": "user",
                 "content": f"Explique resumidamente a medida '{self.name}': `{expression}`"}
            ],
            max_tokens=200
        )

        print(f'Generating AI comment for table item: {self.name}')
        return completion.choices[0].message.content

    def get_expression_cleaned(self) -> str:
        """
        Returns the expression without blank lines at the
        start and end.
        :return: string
        """
        if not self.expression:
            return ''

        result = self.expression.copy()

        i = 0
        while i < len(result) and result[i] == '':
            result.pop(i)
            i += 1

        i = len(result)-1
        while i >= 0 and result[i] == '':
            result.pop(i)
            i -= 1

        return '\n'.join(result)
