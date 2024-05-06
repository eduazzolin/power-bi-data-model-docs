import json
import os
import time


class Model:
    """
    Class to extract and store information from a Power BI pbip folder.
    """

    def __init__(self, path: str, model_type: int, skip_loading: bool = False, ):
        """
        Constructor
        :param path: path of the pbip folder
        :param skip_loading: if True, it will not print the loading messages
        :param model_type: 1 = PBIP FOLDER, 2 = MODEL.BIM FOLDER
        :attr model_bim_file: .Dataset/model.bim file
        :attr report_json_file: .Report/report.json file
        :attr item_metadata_json_file: .Dataset/item.metadata.json file
        :attr tables: list of tables
        :attr relationships: list of relationships
        :attr name: model name
        :attr size: model size in bytes
        """
        self.path = path
        self.skip_loading = skip_loading
        self.model_type = model_type

        if self.model_type == 2:
            self.model_bim_file = self.open_model_bim_file_specifc()
            self.name = self.extract_model_name_from_model_bim()
            self.tables = self.extract_tables()
            self.relationships = self.extract_relationships()
            self.size = 0
        elif self.model_type == 1:
            self.model_bim_file = self.open_model_bim_file()
            self.report_json_file = self.open_report_json_file()
            self.item_metadata_json_file = self.open_item_metadata_json_file()
            self.tables = self.extract_tables()
            self.relationships = self.extract_relationships()
            self.name = self.extract_model_name()
            self.size = self.extract_model_size()

    def extract_tables(self) -> list:
        """
        Extract tables from model.bim file
        :return: list of tables
        """
        tables = []
        for table in self.model_bim_file['model']['tables']:

            # table name
            table_name: str = table['name']
            if table_name.startswith('LocalDateTable_') or table_name.startswith('DateTableTemplate_'):
                continue

            if not self.skip_loading:
                print(f'Extracting table: {table_name}')
                time.sleep(0.01)

            # table id
            table_id = table.get('lineageTag', None)

            # table description
            table_description = table.get('description', [])
            table_description = [table_description] if isinstance(table_description, str) else table_description

            # table import mode
            # table power query steps
            # table type
            try:
                if table.get('refreshPolicy'):
                    table_import_mode = 'atualização incremental'
                    table_power_query_steps = [table.get('refreshPolicy').get('sourceExpression')] if isinstance(
                        table.get('refreshPolicy').get('sourceExpression'), str) else table.get('refreshPolicy').get(
                        'sourceExpression')
                    table_type = 'table'
                elif table.get('partitions'):
                    table_partitions: dict = table.get('partitions')[0]
                    table_import_mode = table_partitions.get('mode')
                    table_type = 'table' if table_partitions.get('source').get('type') == 'm' else table_partitions.get(
                        'source').get('type')
                    table_power_query_steps = [table_partitions['source']['expression']] if isinstance(
                        table_partitions['source']['expression'], str) else table_partitions['source']['expression']
            except Exception as e:
                print(f'Error extracting table: {table_name}')
                print(e)
                table_import_mode = '-------'
                table_power_query_steps = ['-------']
                table_type = '-------'

            # table items
            table_columns: list = []
            if 'columns' in table:
                self.extract_columns(table, table_columns)
            table_measures: list = []
            if 'measures' in table:
                self.extract_measures(table, table_measures)
            table_itens = table_columns + table_measures
            if table_itens:
                table_itens = sorted(table_itens, key=lambda x: (x.name, x.table_item_type))

            # table object
            tables.append(Table(
                table_id=table_id,
                name=table_name,
                description=table_description,
                table_itens=table_itens,
                table_type=table_type,
                import_mode=table_import_mode,
                power_query_steps=table_power_query_steps,
            ))

        return sorted(tables, key=lambda x: x.name)

    def extract_measures(self, table, table_measures):
        """
        Extract measures from table
        :param table: table dictionary
        :param table_measures: list to hold measures
        """
        for measure in table['measures']:
            string_description = measure.get('description', '')
            if string_description:
                string_description = ' '.join(string_description) if isinstance(string_description,
                                                                                list) else string_description

            table_measures.append(TableItem(
                name=measure.get('name'),
                table_item_id=measure.get('lineageTag'),
                table_item_type='measure',
                is_hidden=measure.get('isHidden', False),
                display_folder=measure.get('displayFolder'),
                format_string=measure.get('formatString'),
                description=string_description,
                expression=[measure.get('expression')] if isinstance(measure.get('expression'),
                                                                     str) else measure.get('expression')
            ))

    def extract_columns(self, table, table_columns):
        """
        Extract columns from table
        :param table: table dictionary
        :param table_columns: list to hold columns
        """
        for column in table['columns']:
            table_columns.append(TableItem(
                table_item_id=column.get('lineageTag'),
                name=column.get('name'),
                data_type=column.get('dataType'),
                table_item_type=column.get('type', 'column'),
                expression=[column.get('expression')] if isinstance(column.get('expression'),
                                                                    str) else column.get('expression'),
                format_string=column.get('formatString'),
                is_hidden=column.get('isHidden', False)
            ))

    def extract_relationships(self):
        """
        Extract relationships from model.bim file
        :return: list of relationships objects
        """
        relationships = []
        if 'relationships' in self.model_bim_file['model']:
            for relation in self.model_bim_file['model']['relationships']:
                if relation.get('toTable', None).startswith('LocalDateTable_'):
                    continue
                if relation.get('fromTable', None).startswith('DateTableTemplate_'):
                    continue

                if not self.skip_loading:
                    print(f'Extracting relationship: {relation.get("fromTable", "")} -> {relation.get("toTable", "")}')
                    time.sleep(0.01)

                relationships.append(Relationship(
                    relationship_id=relation.get('name', None),
                    origin_table=relation.get('toTable', None),
                    origin_column=relation.get('toColumn', None),
                    target_table=relation.get('fromTable', None),
                    target_column=relation.get('fromColumn', None),
                    is_active=relation.get('isActive', True),
                    is_both_directions=True if 'crossFilteringBehavior' in relation else False,
                    origin_cardinality=relation.get('toCardinality', 'one'),
                    target_cardinality=relation.get('fromCardinality', 'many')
                ))
        return sorted(relationships, key=lambda x: x.origin_table)

    def open_model_bim_file(self) -> dict:
        """
        Open model.bim file
        :return: the file in dict format
        """
        try:
            model_folder = [os.path.join(self.path, f, 'model.bim') for f in os.listdir(self.path) if
                            os.path.isdir(os.path.join(self.path, f)) if f.endswith('.Dataset')]
            with open(model_folder[0], 'r', encoding='utf-8') as file:
                model = json.load(file)
            print(f'\033[92mModel.bim loaded!\033[0m' if not self.skip_loading else '')
            return model
        except Exception as e:
            print(f'\033[93mModel.bim not found!\033[0m')
            raise e
        return None

    def open_report_json_file(self) -> dict:
        """
        Open report.json file
        :return: the file in dict format
        """
        try:
            report_folder = [os.path.join(self.path, f, 'report.json') for f in os.listdir(self.path) if
                             os.path.isdir(os.path.join(self.path, f)) if f.endswith('.Report')]
            with open(report_folder[0], 'r', encoding='utf-8') as file:
                file = json.load(file)
            print(f'\033[92mReport.json loaded!\033[0m' if not self.skip_loading else '')
            return file
        except Exception as e:
            print(f'\033[93mReport file not found!\033[0m')
            raise e
        return None

    def open_item_metadata_json_file(self) -> dict:
        """
        Open item.metadata.json file
        :return: the file in dict format
        """
        try:
            model_folder = [os.path.join(self.path, f, 'item.metadata.json') for f in os.listdir(self.path) if
                            os.path.isdir(os.path.join(self.path, f)) if f.endswith('.Dataset')]
            with open(model_folder[0], 'r', encoding='utf-8') as file:
                model = json.load(file)
            print(f'\033[92mitem.metadata.json loaded!\033[0m' if not self.skip_loading else '')
            return model
        except Exception as e:
            print(f'\033[93mitem.metadata.json not found!\033[0m')
            raise e
        return None

    def extract_model_name(self) -> str:
        """
        Extract model name from item.metadata.json file
        :return: string name
        """

        if self.item_metadata_json_file:
            if not self.skip_loading:
                print(f'Extracting model name: {self.item_metadata_json_file.get("displayName", "Model")}')
                time.sleep(0.01)
            return self.item_metadata_json_file.get('displayName', 'Model')
        pass

    def extract_model_size(self) -> int:
        """
        Calculate model size in bytes
        :return: int size
        """
        total = 0
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(root, file)
                total += os.path.getsize(file_path)
        return total

    def open_model_bim_file_specifc(self):
        try:
            with open(os.path.join(self.path, 'model.bim'), 'r', encoding='utf-8') as file:
                model = json.load(file)
            print(f'\033[92mModel.bim loaded!\033[0m' if not self.skip_loading else '')
            return model
        except Exception as e:
            print(f'\033[93mModel.bim not found!\033[0m')
            raise e
        return None

    def extract_model_name_from_model_bim(self):
        """
        Extract model name from model.bim file
        :return: str
        """
        if self.model_bim_file.get('name'):
            return self.model_bim_file.get('name')
        else:
            return 'Data model'


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
                self.power_query_steps[i] = f'{prefix}  _CUSTOM_QUERY_  {postfix}'
                return query

            # Oracle DB
            if 'Oracle.Database(' in self.power_query_steps[i] and 'Query="' in self.power_query_steps[i]:
                line = self.power_query_steps[i]
                prefix: str = line[:line.find('Query=') + 7]
                postfix: str = line[len(line) - 3:]
                query: str = line[line.find('Query=') + 7:len(line) - 3]
                query = query.replace('#(lf)', '\n').replace('#(tab)', '    ')
                self.power_query_steps[i] = f'{prefix}  _CUSTOM_QUERY_  {postfix}'
                return query


class Relationship:
    """
    Class to represent a relationship between two tables
    """

    def __init__(self, relationship_id: str, origin_column: str, origin_table: str, origin_cardinality: str,
                 target_column: str,
                 target_table: str, target_cardinality: str, is_active: bool, is_both_directions: bool):
        """
        Constructor of the class
        :param relationship_id: id of the relationship
        :param origin_column: column that filters the target table
        :param origin_table: table that filters the target table
        :param origin_cardinality: cardinality of the origin table, can be 'one' or 'many'
        :param target_column: column that is filtered by the origin table
        :param target_table: table that is filtered by the origin table
        :param target_cardinality: cardinality of the target table, can be 'one' or 'many'
        :param is_active: if the relationship is active
        :param is_both_directions:
        """
        self.relationship_id = relationship_id
        self.origin_column = origin_column
        self.origin_table = origin_table
        self.target_column = target_column
        self.target_table = target_table
        self.is_active = is_active
        self.origin_cardinality = origin_cardinality
        self.target_cardinality = target_cardinality
        self.is_both_directions = is_both_directions

    def __str__(self):
        """
        Method to return a string representation of the relationship
        :return: str
        """
        origin = f'{self.origin_table}[{self.origin_column}]'
        target = f'{self.target_table}[{self.target_column}]'
        cardinality = f'{self.origin_cardinality:4} {" <--> " if self.is_both_directions else " ---> "} {self.target_cardinality:4}'
        return f'{origin[:50]:50}     {cardinality}     {target}'


class TableItem:
    """
    TableItem class to represent a column or measure in a table.
    """

    def __init__(self, table_item_id: str, name: str, table_item_type: str = 'column', data_type: str = None,
                 format_string: str = None,
                 display_folder: str = None, is_hidden: bool = False, expression: list = None, description: str = ''):
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

    def generate_comment_openai(self, openai_key: str) -> str:
        """
        Method to generate a comment for the table item using OpenAI's GPT-3.5
        :return: string
        """
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)

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

        i = len(result) - 1
        while i >= 0 and result[i] == '':
            result.pop(i)
            i -= 1

        return '\n'.join(result)
