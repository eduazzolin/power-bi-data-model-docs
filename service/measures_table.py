import pandas as pd

from model.data_model import DataModel


class MeasuresTable:
    """
    Class to generate a table file with the measures from the model.
    """

    def __init__(self, model: DataModel):
        """
        Constructor of the class.
        :param model: DataModel
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
                row_description = measure.description
                row_expression = measure.get_expression_cleaned()
                row_format_string = measure.format_string
                rows.append(
                    [row_table, row_display_folder, row_measure, row_description, row_expression, row_format_string])
        df = pd.DataFrame(rows,
                          columns=['Table', 'Display Folder', 'Measure', 'Description', 'Expression', 'Format String'])
        sorted_df = df.sort_values(by=['Table', 'Display Folder', 'Measure'], ascending=[True, True, True])
        return sorted_df
