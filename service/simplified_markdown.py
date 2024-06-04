import datetime as dt
import os
import time

from model.data_model import DataModel


class SimplifiedMarkdown:
    def __init__(self, model: DataModel):
        """
        Constructor of the class.
        :param model: DataModel
        """
        self.model = model

    def generate_md(self):
        result = '# Resumo\n'
        result += f'- **Data do relatório:** {dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n'
        result += f'- **Quantidade de relacionamentos:** {len(self.model.relationships)}\n'
        result += f'- **Quantidade de colunas:** {sum([len([c for c in table.table_itens if c.table_item_type == "column"]) for table in self.model.tables])}\n'
        result += f'- **Quantidade de colunas calculadas:** {sum([len([c for c in table.table_itens if c.table_item_type == "calculated"]) for table in self.model.tables])}\n'
        result += f'- **Quantidade de medidas:** {sum([len([m for m in table.table_itens if m.table_item_type == "measure"]) for table in self.model.tables])}\n'

        result += '\n# relacionamentos\n'
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

        result += '\n# tables\n'
        tables = [table for table in self.model.tables]
        tables.sort(key=lambda x: x.name)
        for t in tables:
            colunas = [c for c in t.table_itens if c.table_item_type == 'column']
            colunas.sort(key=lambda x: x.name)
            result += f'#### {t.name}\n'
            result += f'```M\n'
            for step in t.power_query_steps:
                result += f'{step}\n'
            result += f'```\n'
            result += f'- **tipo:** {t.table_type}\n'
            result += f'- **modo de importação:** {t.import_mode}\n'
            result += f'- **descrição:** {" ".join(t.description)}\n' if t.description else ''
            result += f'- **colunas:**\n'
            for c in colunas: result += f'  - **{c.name}** {c.data_type.upper()}\n'
            result += '\n---\n'
        
        result += '\n# medidas\n'
        measures = [measure for table in self.model.tables for measure in table.table_itens if measure.table_item_type == 'measure']
        measures.sort(key=lambda x: x.name)
        for m in measures:
            result += f'#### {m.name}\n'
            result += f'- **tabela:** {m.display_folder}\n'
            result += f'- **Pasta:** {m.display_folder if m.display_folder else "Nenhuma"}\n'
            result += f'- **Formato:** ``{m.format_string if m.format_string else "Automático"}``\n'
            result += f'\n```dax\n'
            result += f'{m.get_expression_cleaned()}\n'
            result += f'```\n'
            result += '\n---\n'
        
        result += '\n # colunas calculadas\n'
        calculated = [calculated for table in self.model.tables for calculated in table.table_itens if calculated.table_item_type == 'calculated']
        calculated.sort(key=lambda x: x.name)
        for c in calculated:
            result += f'#### {c.name}\n'
            result += f'- **tabela:** {c.display_folder}\n'
            result += f'- **formato:** {c.data_type.upper()}\n'
            result += f'\n```dax\n'
            result += f'{c.get_expression_cleaned()}\n'
            result += f'```\n'
            result += '\n---\n'

        return result

    def save_md(self, md):
        timestamp = dt.datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            with open(os.path.join(self.model.path, f'data_model_documentation {timestamp}.md'), 'w',
                      encoding='utf-8') as f:
                f.write(md)
            print('\n\nDocumentação gerada com sucesso!')
        except Exception as e:
            print(f'Erro ao gerar documentação: {e}')
            time.sleep(5)