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

    def verify_usage(self, p_table, p_field):
        """
        Verify if a field is used in the model.
        It's verified both in measures and calculated columns.
        :param p_table: table name
        :param p_field: field name
        :return: bool
        """
        name_standard = f'{p_table}[{p_field}]'
        name_with_quotation = f'\'{p_table}\'[{p_field}]'
        name_only_field = f'[{p_field}]'
        all_table_names = [table.name for table in self.model.tables]
        found = False

        for table in self.model.tables:
            for measure in [item for item in table.table_itens if item.table_item_type == 'measure']:
                if name_standard in measure.get_expression_cleaned() or name_with_quotation in measure.get_expression_cleaned():
                    found = True
                    print(f'{p_table}.{p_field} found at {table.name}.{measure.name}')
            for calculated in [item for item in table.table_itens if item.table_item_type == 'calculated']:
                if name_standard in calculated.get_expression_cleaned() or name_with_quotation in calculated.get_expression_cleaned():
                    found = True
                    print(f'{p_table}.{p_field} found at {table.name}.{calculated.name}')
                if table.name == p_table and name_only_field in calculated.get_expression_cleaned():
                    """
                    In this section we verify if the field appears in a calculated column of the same table.
                    In this case, we need to verify if the field is used without the name of its table.
                    To discard cases of fields with the same name in different tables, we rip off all the cases
                    where the field is used with the name of any table, and then we verify if the field is still present.
                    """
                    expression = calculated.get_expression_cleaned()
                    for table_name in all_table_names:
                        name_standard_temp = f'{table_name}{name_only_field}'
                        name_with_quotation_temp = f'\'{table_name}\'{name_only_field}'
                        expression = expression.replace(name_standard_temp, '')
                        expression = expression.replace(name_with_quotation_temp, '')
                    if name_only_field in expression:
                        found = True
                        print(f'{p_table}.{p_field} found at {table.name}.{calculated.name}')

        for relation in self.model.relationships:
            if p_table == relation.origin_table and p_field == relation.origin_column:
                found = True
                print(f'{p_table}.{p_field} found at RELATIONSHIP {relation.origin_table}|{relation.target_table}')
            if p_table == relation.target_table and p_field == relation.target_column:
                found = True
                print(f'{p_table}.{p_field} found at RELATIONSHIP {relation.origin_table}|{relation.target_table}')

        return found

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