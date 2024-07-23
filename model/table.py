class Table:
    """
    Table class to represent a table in a model.
    """

    def __init__(self,
                 table_id: str,
                 name: str,
                 description: list,
                 table_type: str,
                 table_itens: list,
                 import_mode: str,
                 power_query_steps: list):
        """
        Constructor of the class
        :param table_id: the table id
        :param name: the table name
        :param description: the table description
        :param table_type: the table type, can be 'table' or 'calculated'
        :param table_itens: list of objects of type TableItem
        :param import_mode: the import mode of the table, can be 'import' or 'directquery'
        :param power_query_steps: list of power query steps
        """
        self.table_id: str = table_id
        self.name: str = name
        self.description: list = description
        self.table_type: str = table_type
        self.table_itens: list = table_itens
        self.import_mode: str = import_mode
        self.power_query_steps: list = power_query_steps
        self.query: str = self.format_query()

    def __str__(self):
        """
        Method to return a string representation of the table
        :return: string
        """
        result = ''
        result += f'Name: {self.name}\n'
        result += f'Description: {" ".join(self.description)}\n'
        result += f'Type: {self.table_type}\n'
        result += f'Import Mode: {self.import_mode}\n'
        result += f'Power Query Steps: {self.power_query_steps}\n'
        result += f'Query: {self.query}\n'
        result += f'Items:\n'
        for item in self.table_itens:
            result += f'{item}\n'
        return result

    def format_query(self) -> str:
        """
        Method to format the query in the power query steps
        the query is replaced by a token _CUSTOM_QUERY_ in the steps
        and the query is returned
        :return: query string
        """
        for i in range(len(self.power_query_steps)):
            # Google BigQuery
            if 'NativeQuery' in self.power_query_steps[i]:
                line = self.power_query_steps[i]
                prefix: str = line[:line.find('[Data],') + 9]
                postfix: str = line[line.rfind(', null') - 1:]
                query: str = line[line.find('[Data],') + 9:line.rfind(', null') - 1]
                query = query.replace('#(lf)', '\n').replace('#(tab)', '    ')
                return query

            # Oracle DB
            if 'Oracle.Database(' in self.power_query_steps[i] and 'Query="' in self.power_query_steps[i]:
                line = self.power_query_steps[i]
                prefix: str = line[:line.find('Query=') + 7]
                postfix: str = line[len(line) - 3:]
                query: str = line[line.find('Query=') + 7:len(line) - 3]
                query = query.replace('#(lf)', '\n').replace('#(tab)', '    ')
                return query
