import datetime as dt
import os
import time

from model.data_model import DataModel


class SimplifiedMarkdown:
    """
    Service class to generate a simplified markdown file with the model information.
    """

    def __init__(self, model: DataModel):
        """
        Constructor of the class.
        :param model: DataModel
        """
        self.model = model

    def generate_md(self) -> str:
        """
        Method to generate the markdown file.
        :return: str
        """
        result = f'# {self.model.name}\n'
        result += f'- **Hora de execução do arquivo:** {self.model.start_time}\n'
        result += f'\n\n'

        result += f'- **Data do relatório:** {dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n'
        result += f'- **Quantidade de relacionamentos:** {len(self.model.relationships)}\n'
        result += f'- **Quantidade de colunas:** {sum([len([c for c in table.table_itens if c.table_item_type == "column"]) for table in self.model.tables])}\n'
        result += f'- **Quantidade de colunas calculadas:** {sum([len([c for c in table.table_itens if c.table_item_type == "calculated"]) for table in self.model.tables])}\n'
        result += f'- **Quantidade de medidas:** {sum([len([m for m in table.table_itens if m.table_item_type == "measure"]) for table in self.model.tables])}\n'

        result += '\n## relacionamentos\n'
        relacionamentos = [rel for rel in self.model.relationships]
        relacionamentos.sort(key=lambda x: x.origin_column)
        result += f'|  |  |  |  |  |\n'
        result += f'| ---- | ---- | ---- | ---- | ---- |\n'
        for r in relacionamentos:
            origin = f'{r.origin_table}[{r.origin_column}]'
            target = f'{r.target_table}[{r.target_column}]'
            direction = f'{" <--> " if r.is_both_directions else " ---> "}'
            if r.is_active:
                result += f'| {origin} | {r.origin_cardinality} | {direction} | {r.target_cardinality} | {target}\n'
            else:
                result += f'| (Desativado) *{origin}* | *{r.origin_cardinality}* | {direction} | *{r.target_cardinality}* | *{target}*\n'
        result += f'|  |  |  |  |  |\n'

        result += '\n## tabelas\n'
        tables = [table for table in self.model.tables]
        tables.sort(key=lambda x: x.name)
        for t in tables:
            colunas = [c for c in t.table_itens if c.table_item_type == 'column']
            colunas.sort(key=lambda x: x.name)
            result += f'### {t.name}\n'
            result += f'```M\n'
            for step in t.power_query_steps:
                result += f'{step}\n'
            result += f'```\n'
            result += f'- **tipo:** {t.table_type}\n'
            result += f'- **modo de importação:** {t.import_mode}\n'
            result += f'- **descrição:** {" ".join(t.description)}\n' if t.description else ''
            result += f'- **colunas:**\n'
            for c in colunas: result += f'  - **{c.name}** {c.data_type}\n'
            result += '\n---\n'

        result += '\n## medidas\n'
        for m in self.model.get_all_measures():
            result += f'### {m.name}\n'
            result += f'- **tabela:** {m.table}\n'
            result += f'- **Pasta:** {m.display_folder if m.display_folder else "Nenhuma"}\n'
            result += f'- **Formato:** ``{m.format_string if m.format_string else "Automático"}``\n'
            result += f'\n```dax\n'
            result += f'{m.get_expression_cleaned()}\n'
            result += f'```\n'
            result += '\n---\n'

        result += '\n # colunas calculadas\n'
        for c in self.model.get_all_calculated_columns():
            result += f'### {c.name}\n'
            result += f'- **tabela:** {c.table}\n'
            result += f'- **tipo:** {c.data_type}\n'
            result += f'- **formato:** ``{c.format_string if c.format_string else "Automático"}``\n'
            result += f'\n```dax\n'
            result += f'{c.get_expression_cleaned()}\n'
            result += f'```\n'
            result += '\n---\n'

        return result