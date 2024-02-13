import datetime as dt

from model.model import Model


class GeradorDeDocumentacaoPBI:

    def __init__(self, path):
        self.model = Model(path)

    def exportar_md(self):
        md = ''
        md += f'# {self.model.name}\n'
        md += f'Data do relatório: {dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n'

        md += f'## Resumo do modelo de dados\n'
        md += f'Tamanho do modelo: {((self.model.size / 1024) / 1024):.2f} MB\n'
        md += f'Quantidade de tabelas: {len(self.model.tables)}\n'
        md += f'Quantidade de relacionamentos: {len(self.model.relationships)}\n'
        md += f'Quantidade de colunas: {sum([len([c for c in table.table_itens if c.table_item_type == "column"]) for table in self.model.tables])}\n'
        md += f'Quantidade de colunas calculadas: {sum([len([c for c in table.table_itens if c.table_item_type == "calculated"]) for table in self.model.tables])}\n'
        md += f'Quantidade de medidas: {sum([len([m for m in table.table_itens if m.table_item_type == "measure"]) for table in self.model.tables])}\n'

        md += f'### Tabelas\n'
        for t in self.model.tables:
            md += f'{t.name}\n'

        md += f'### Relacionamentos\n'
        for r in self.model.relationships:
            origin = f'{r.origin_table}[{r.origin_column}]'
            target = f'{r.target_table}[{r.target_column}]'
            direction = f'{" <--> " if r.is_both_directions else " ---> "}'
            md += f'|  |  |  |  |  |\n'
            md += f'| ---- | ---- | ---- | ---- | ---- |\n'
            md += f'| {origin} | {r.origin_cardinality} | {direction} | {r.target_cardinality} |\n'
        md += f'|  |  |  |  |  |\n'
        md += f'### Medidas\n'
        for t in self.model.tables:
            for m in t.table_itens:
                if m.table_item_type == 'measure':
                    md += f'[{m.name}]\n'

        md += f'## Detalhamento das tabelas\n'
        for t in self.model.tables:
            is_in_relationship = False
            has_columns = False
            has_measures = False
            has_calculated_columns = False

            for r in self.model.relationships:
                if r.origin_table == t.name or r.target_table == t.name:
                    is_in_relationship = True
                    break

            for i in t.table_itens:
                if i.table_item_type == 'column':
                    has_columns = True
                if i.table_item_type == 'measure':
                    has_measures = True
                if i.table_item_type == 'calculated':
                    has_calculated_columns = True


            md += f'### {t.name}\n'
            md += f'Nome: {t.name}\n'
            md += f'Tipo: {t.table_type}\n'
            md += f'Modo de importação: {t.import_mode}\n'

            if t.query:
                md += f'#### Query:\n'
                md += f'```sql\n'
                md += f'{t.query}\n'
                md += f'```\n'

            if t.power_query_steps:
                md += f'#### Definição no PowerQuery:\n'
                md += f'```M\n'
                for step in t.power_query_steps:
                    md += f'{step}\n'
                md += f'```\n'

            if is_in_relationship:
                md += f'#### Relacionamentos\n'
                md += f'|  |  |  |  |  |\n'
                md += f'| ---- | ---- | ---- | ---- | ---- |\n'
                when_both = [r for r in self.model.relationships if r.is_both_directions if r.origin_table == t.name or r.target_table == t.name]
                when_target = [r for r in self.model.relationships if r.target_table == t.name if r.relationship_id not in [r.relationship_id for r in when_both]]
                when_origin = [r for r in self.model.relationships if r.origin_table == t.name if r.relationship_id not in [r.relationship_id for r in when_both]]
                for r in when_origin:
                    origin = f'{r.origin_table}[{r.origin_column}]'
                    target = f'{r.target_table}[{r.target_column}]'
                    md += f'| {origin} | {r.origin_cardinality} |   -->   | {r.target_cardinality} | {target} |\n'
                for r in when_both:
                    origin = f'{r.origin_table}[{r.origin_column}]'
                    target = f'{r.target_table}[{r.target_column}]'
                    origin_cardinality = r.origin_cardinality
                    target_cardinality = r.target_cardinality
                    if r.target_table == t.name:
                        target = f'{r.origin_table}[{r.origin_column}]'
                        origin = f'{r.target_table}[{r.target_column}]'
                        target_cardinality = r.origin_cardinality
                        origin_cardinality = r.target_cardinality
                    md += f'| {origin} | {r.origin_cardinality} |   <->   | {r.target_cardinality} | {target} |\n'
                for r in when_target:
                    target = f'{r.origin_table}[{r.origin_column}]'
                    origin = f'{r.target_table}[{r.target_column}]'
                    target_cardinality = r.origin_cardinality
                    origin_cardinality = r.target_cardinality
                    md += f'| {origin} | {r.origin_cardinality} |   <--   | {r.target_cardinality} | {target} |\n'

                md += f'|  |  |  |  |  |\n'

            md += f'#### Colunas\n' if has_columns else ''
            count = 0
            for c in t.table_itens:
                if c.table_item_type == 'column':
                    count += 1
                    md += f'{str(count)}. {c.name}\n'

            md += f'#### Colunas calculadas\n' if has_calculated_columns else ''
            for c in t.table_itens:
                if c.table_item_type == 'calculated':
                    c_expression = '\n'.join(c.expression)
                    md += f'##### {c.name}\n'
                    md += f'```dax\n'
                    md += f'{c_expression}\n'
                    md += f'```\n'

            md += f'#### Medidas\n' if has_measures else ''
            for m in t.table_itens:
                if m.table_item_type == 'measure':
                    if m.expression:
                        m_expression = '\n'.join(m.expression)
                    else:
                        m_expression = 'Vazio'
                    md += f'##### {m.name}\n'
                    md += f'Nome: {m.name}\n'
                    md += f'Pasta: {m.display_folder if m.display_folder else "Nenhuma"}\n'
                    md += f'Formato: ``{m.format_string if m.format_string else "Automático"}``\n'
                    md += f'```dax\n'
                    md += f'{m_expression}\n'
                    md += f'```\n'
        return md


if __name__ == '__main__':
    gerador = GeradorDeDocumentacaoPBI('..\\exemplo')
    md = gerador.exportar_md()
    print(md)
    with open('..\\exemplo\\documentacao.md', 'w', encoding='utf-8') as f:
        f.write(md)
