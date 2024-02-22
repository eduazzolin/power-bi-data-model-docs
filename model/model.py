import json
import os
import sys
import time
from .relationship import Relationship
from .table import Table
from .table_item import TableItem


class Model:
    """
    Class to extract and store information from a Power BI pbip folder.
    """

    def __init__(self, path: str):
        """
        Constructor
        :param path: path of the pbip folder
        :attr model_bim_file: .Dataset/model.bim file
        :attr report_json_file: .Report/report.json file
        :attr tables: list of tables
        :attr relationships: list of relationships
        :attr name: model name
        :attr size: model size in bytes
        """
        self.path = path
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
            table_partitions: dict = table['partitions'][0]
            table_import_mode: str = table_partitions['mode']
            table_power_query_steps: list = [table_partitions['source']['expression']] if isinstance(
                table_partitions['source']['expression'], str) else table_partitions['source']['expression']
            table_type = 'table' if table_partitions['source']['type'] == 'm' else table_partitions['source']['type']

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
            table_measures.append(TableItem(
                name=measure.get('name'),
                table_item_id=measure.get('lineageTag'),
                table_item_type='measure',
                is_hidden=measure.get('isHidden', False),
                display_folder=measure.get('displayFolder'),
                format_string=measure.get('formatString'),
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
            print(f'\033[92mModel.bim loaded!\033[0m')
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
            print(f'\033[92mReport.json loaded!\033[0m')
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
            print(f'\033[92mitem.metadata.json loaded!\033[0m')
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
