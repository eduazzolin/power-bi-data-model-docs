import json
import os

from .table_item import TableItem
from .relationship import Relationship
from .table import Table


class Model:

    def __init__(self, path: str):
        self.path = path
        self.model_bim_file = self.open_model_bim_file()
        self.report_json_file = self.open_report_json_file()
        self.tables = self.extract_tables()
        self.relationships = self.extract_relationships()


    def extract_tables(self):
        tables = []
        for table in self.model_bim_file['model']['tables']:

            # table name
            table_name: str = table['name']
            if table_name.startswith('LocalDateTable_') or table_name.startswith('DateTableTemplate_'):
                continue

            # table id
            table_id = table['lineageTag']

            # table import mode
            # table power query steps
            # table type
            table_partitions: dict = table['partitions'][0]
            table_import_mode: str = table_partitions['mode']
            table_power_query_steps: list = [table_partitions['source']['expression']] if isinstance(
                table_partitions['source']['expression'], str) else table_partitions['source']['expression']
            table_type = 'table' if table_partitions['source']['type'] == 'm' else table_partitions['source']['type']

            # table columns
            table_columns: list = []
            if 'columns' in table:
                self.extract_columns(table, table_columns)

            # table measures
            table_measures: list = []
            if 'measures' in table:
                self.extract_measures(table, table_measures)

            table_itens = table_columns + table_measures
            if table_itens:
                table_itens = sorted(table_itens, key=lambda x: (x.name, x.table_item_type))

            tables.append(Table(
                table_id=table_id,
                name=table_name,
                table_itens=table_itens,
                table_type=table_type,
                import_mode=table_import_mode,
                power_query_steps=table_power_query_steps,
                measures=table_measures
            ))

        return sorted(tables, key=lambda x: x.name)

    def extract_measures(self, table, table_measures):
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
        for column in table['columns']:
            table_columns.append(TableItem(
                table_item_id=column.get('lineageTag'),
                name=column.get('name'),
                data_type=column.get('dataType'),
                table_item_type=column.get('type', 'column'),
                expression=column.get('expression'),
                format_string=column.get('formatString'),
                is_hidden=column.get('isHidden', False)
            ))

    def extract_relationships(self):
        """
        Atributos:
        o padrão é 1 - *
        - 'name': id
        - 'toColumn', 'toTable': a que filtra ORIGIN
        - 'fromColumn','fromTable': a que é filtrada TARGET
        - 'toCardinality',  'fromCardinality': podem ser 'one' ou 'many' e quando uma aparece a outra não
        - 'crossFilteringBehavior': pode ser 'bothDirections'
        - 'name': id
        - 'joinOnDateBehavior': irrelevante
        """
        relationships = []
        if 'relationships' in self.model_bim_file['model']:
            for relation in self.model_bim_file['model']['relationships']:
                if relation.get('toTable', None).startswith('LocalDateTable_'):
                    continue
                if relation.get('fromTable', None).startswith('DateTableTemplate_'):
                    continue

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

    def open_model_bim_file(self):
        model_folder = [os.path.join(self.path, f, 'model.bim') for f in os.listdir(self.path) if
                        os.path.isdir(os.path.join(self.path, f)) if f.endswith('.Dataset')]
        try:
            with open(model_folder[0], 'r', encoding='utf-8') as file:
                model = json.load(file)
            print(f'\033[92mModel.bim loaded!\033[0m')
            return model
        except Exception:
            print(f'\033[93mModel.bim not found!\033[0m')
        return None

    def open_report_json_file(self):
        report_folder = [os.path.join(self.path, f, 'report.json') for f in os.listdir(self.path) if
                         os.path.isdir(os.path.join(self.path, f)) if f.endswith('.Report')]
        try:
            with open(report_folder[0], 'r', encoding='utf-8') as file:
                file = json.load(file)
            print(f'\033[92mReport.json loaded!\033[0m')
            return file
        except Exception:
            print(f'\033[93mReport file not found!\033[0m')
        return None


