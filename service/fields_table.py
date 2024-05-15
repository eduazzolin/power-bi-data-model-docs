import os

import pandas as pd

from model.data_model import DataModel


class FieldsTable:
    def __init__(self, model: DataModel):
        """
        Constructor of the class.
        :param model: DataModel
        """
        self.model = model

    def verify_usage(self, table, field):

        name_1 = f'{table}[{field}]'
        name_2 = f'\'{table}\'[{field}]'

        declarations = []
        for table in self.model.tables:
            for measure in [item for item in table.table_itens if item.table_item_type == 'measure']:
                declarations.append(measure.get_expression_cleaned())
            for calculated in [item for item in table.table_itens if item.table_item_type == 'calculated']:
                declarations.append(calculated.get_expression_cleaned())

        for declaration in declarations:
            if name_1 in declaration or name_2 in declaration:
                return True

        return False

    def generate_data_frame(self):
        rows = []
        for table in self.model.tables:
            for column in [item for item in table.table_itens if item.table_item_type == 'column']:
                row_table = table.name
                row_column = column.name
                row_data_type = column.data_type
                row_is_used = self.verify_usage(row_table, row_column)
                rows.append([row_table, row_column, row_data_type, row_is_used])
        df = pd.DataFrame(rows, columns=['Table', 'Column', 'Data Type', 'Is Used'])
        sorted_df = df.sort_values(by=['Table', 'Column'], ascending=[True, True])
        return sorted_df

    def save_csv(self, filename: str = 'fields_table.csv'):
        df = self.generate_data_frame()
        path = os.path.join(self.model.path, filename)
        df.to_csv(path, index=False, encoding='utf-8', lineterminator='\n')
        print(f'\nArquivo {filename} gerado com sucesso!')

    def save_xlsx(self, filename: str = 'fields_table.xlsx'):
        df = self.generate_data_frame()
        path = os.path.join(self.model.path, filename)
        with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            cell_format = workbook.add_format({'text_wrap': True})
            worksheet.set_column('A:Z', cell_format=cell_format)
        print(f'\nArquivo {filename} gerado com sucesso!')