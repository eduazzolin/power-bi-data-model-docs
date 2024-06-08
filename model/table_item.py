class TableItem:
    """
    TableItem class to represent a column or measure in a table.
    """

    def __init__(self, table_item_id: str, name: str, table_item_type: str = 'column', data_type: str = None,
                 format_string: str = None,
                 display_folder: str = None, is_hidden: bool = False, expression: list = None, description: str = '',
                 table_name=''):
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
        :param description: the description of the table item
        :param table_name: the name of the table where the table item is located
        """
        self.table_item_id: str = table_item_id
        self.name: str = name
        self.table_item_type: str = table_item_type
        self.data_type: str = data_type
        self.format_string: str = format_string
        self.display_folder: str = display_folder
        self.is_hidden: bool = is_hidden
        self.expression: list = expression
        self.description: str = description
        self.table_name: str = table_name

    def __str__(self):
        """
        Method to return a string representation of the table item
        :return: string
        """
        result = ''
        result += f'Name: {self.name}\n'
        result += f'Description: {self.description}\n'
        result += f'Type: {self.table_item_type}\n'
        result += f'Data Type: {self.data_type}\n'
        result += f'Format String: {self.format_string}\n'
        result += f'Display Folder: {self.display_folder}\n'
        result += f'Is Hidden: {self.is_hidden}\n'
        result += f'Expression: {self.expression}\n'
        return result

    def get_expression_cleaned(self, html=False) -> str:
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

        i = len(result) - 1
        while i >= 0 and result[i] == '':
            result.pop(i)
            i -= 1

        text = '\n'.join(result)
        if html:
           text = (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;"))
        return text
