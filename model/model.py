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
        self.tables = self.get_tables()
        self.relationships = self.get_relationships()

    # ANSI escape codes for text color #TODO remove this
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

    def get_tables(self):
        tables = []
        for table in self.model_bim_file['model']['tables']:

            # table name
            table_name: str = table['name']
            if table_name.startswith('LocalDateTable_'):
                continue
            if table_name.startswith('DateTableTemplate_'):
                continue

            # table id
            table_id = table['lineageTag']

            # table import mode
            # table power query steps
            table_partitions: dict = table['partitions'][0]
            table_import_mode: str = table_partitions['mode']
            table_power_query_steps: list = [table_partitions['source']['expression']] if isinstance(
                table_partitions['source']['expression'], str) else table_partitions['source']['expression']

            # table columns
            table_columns: list = []
            if 'columns' in table:
                for column in table['columns']:
                    table_columns.append(TableItem(
                        id=column.get('lineageTag'),
                        name=column.get('name'),
                        data_type=column.get('dataType'),
                        type=column.get('type', 'column'),
                        expression=column.get('expression'),
                        format_string=column.get('formatString'),
                        is_hidden=column.get('isHidden', False)
                    ))

            # table measures
            table_measures: list = []
            if 'measures' in table:
                for measure in table['measures']:
                    table_measures.append(TableItem(
                        name=measure.get('name'),
                        id=measure.get('lineageTag'),
                        is_hidden=measure.get('isHidden', False),
                        display_folder=measure.get('displayFolder'),
                        format_string=measure.get('formatString'),
                        expression=[measure.get('expression')] if isinstance(measure.get('expression'),
                                                                             str) else measure.get('expression')
                    ))

            tables.append(Table(
                id=table_id,
                name=table_name,
                columns=table_columns,
                import_mode=table_import_mode,
                power_query_steps=table_power_query_steps,
                measures=table_measures
            ))

        return tables

    def get_relationships(self):
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
                    id=relation.get('name', None),
                    origin_table=relation.get('toTable', None),
                    origin_column=relation.get('toColumn', None),
                    target_table=relation.get('fromTable', None),
                    target_column=relation.get('fromColumn', None),
                    is_active=relation.get('isActive', True),
                    is_both_directions=True if 'crossFilteringBehavior' in relation else False,
                    origin_cardinality=relation.get('toCardinality', 'one'),
                    target_cardinality=relation.get('fromCardinality', 'many')
                ))
        return sorted(relationships, key=lambda x: x.originTable)

    def open_model_bim_file(self):
        model_folder = [os.path.join(self.path, f, 'model.bim') for f in os.listdir(self.path) if
                        os.path.isdir(os.path.join(self.path, f)) if f.endswith('.Dataset')]
        try:
            with open(model_folder[0], 'r', encoding='utf-8') as file:
                model = json.load(file)
            print(f'{Model.GREEN}Model file loaded!{Model.RESET}')
            return model
        except Exception:
            print(f'{Model.YELLOW}Model file not found!{Model.RESET}')
        return None

    def open_report_json_file(self):
        report_folder = [os.path.join(self.path, f, 'report.json') for f in os.listdir(self.path) if
                         os.path.isdir(os.path.join(self.path, f)) if f.endswith('.Report')]
        try:
            with open(report_folder[0], 'r', encoding='utf-8') as file:
                file = json.load(file)
            print(f'{Model.GREEN}Report.json loaded!{Model.RESET}')
            return file
        except Exception:
            print(f'{Model.YELLOW}Report file not found!{Model.RESET}')
        return None


if __name__ == '__main__':
    controller = Model('..\\..\\exemplo')
    for t in controller.tables:
        print(t, '\n\n')
    for r in controller.relationships:
        print(r)
    #     print(f'{origin[:30]:30}     {cardinality}     {target}')
    # for table in controller.tables:
    #     print(f'{table.name}')
    #     for column in table.columns:
    #         print(f'    {column.name} - {column.type} - {column.dataType}')
    #         if column.expression:
    #             print(f'        {column.expression}')
