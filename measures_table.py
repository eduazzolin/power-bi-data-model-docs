import os
import subprocess

import pandas as pd

from model import Model


class MeasuresTable:
    """
    Class to generate a table file with the measures from the model.
    """

    def __init__(self, model: Model):
        """
        Constructor of the class.
        :param model: Model
        """
        self.model = model

    def generate_data_frame(self):
        """
        Method to generate the data frame with the measures.
        :return: Pandas.DataFrame
        """

        rows = []
        for table in self.model.tables:
            for measure in [item for item in table.table_itens if item.table_item_type == 'measure']:
                row_table = table.name
                row_display_folder = measure.display_folder
                row_measure = measure.name
                row_expression = measure.get_expression_cleaned()
                row_format_string = measure.format_string
                rows.append([row_table, row_display_folder, row_measure, row_expression, row_format_string])
        df = pd.DataFrame(rows, columns=['Table', 'Display Folder', 'Measure', 'Expression', 'Format String'])
        sorted_df = df.sort_values(by=['Table', 'Display Folder', 'Measure'], ascending=[True, True, True])
        return sorted_df

    def save_xlsx(self, filename: str = 'measures_table.xlsx'):
        """
        Method to save the data frame to a xlsx file.
        :param filename: custom filename
        """
        df = self.generate_data_frame()
        path = os.path.join(self.model.path, filename)
        with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            cell_format = workbook.add_format({'text_wrap': True})
            worksheet.set_column('A:Z', cell_format=cell_format)
        print(f'\nArquivo {filename} gerado com sucesso!')
        try:
            subprocess.Popen(f'explorer "{self.model.path}"')
        except:
            pass

    def save_csv(self, filename: str = 'measures_table.csv'):
        """
        Method to save the data frame to a csv file.
        :param filename: custom filename
        :return:
        """
        df = self.generate_data_frame()
        path = os.path.join(self.model.path, filename)
        df.to_csv(path, index=False, encoding='utf-8', lineterminator='\n')
        print(f'\nArquivo {filename} gerado com sucesso!')
        try:
            subprocess.Popen(f'explorer "{self.model.path}"')
        except:
            pass
