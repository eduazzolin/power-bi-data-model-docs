import datetime as dt
import os
import subprocess
import time

from model import Model


class Markdown:
    """
    Class to generate the documentation in markdown format.
    """

    def __init__(self, model: Model, gerar_interpretacao_ia: bool = False, openai_key: str = None):
        """
        Constructor of the class.
        :param model: Model
        :param gerar_interpretacao_ia: bool
        :param openai_key: str
        """
        self.model = model
        self.gerar_interpretacao_ia = gerar_interpretacao_ia
        self.openai_key = openai_key

    def gerar_md(self):
        """
        Gera a documentação em formato markdown.
        :return: string com a documentação.
        """

        def gerar_md_cabecalho(self) -> str:
            """
            Gera o cabeçalho do markdown, com o nome do modelo e a data do relatório.
            :return: str
            """
            retorno = f'# {self.model.name}\n'
            retorno += f'- Data do relatório: {dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n'
            return retorno

        def gerar_md_resumo_modelo_caracteristicas(self) -> str:
            """
            Gera o resumo do modelo de dados, com as características do modelo, como quantidade de tabelas,
            de colunas, de medidas, e relacionamentos.
            :return: str
            """
            retorno = f'\n# Resumo do modelo de dados\n'
            retorno += f'- **Tamanho do modelo:** {((self.model.size / 1024) / 1024):.2f} MB\n'
            retorno += f'- **Quantidade de tabelas:** {len(self.model.tables)}\n'
            retorno += f'- **Quantidade de relacionamentos:** {len(self.model.relationships)}\n'
            retorno += f'- **Quantidade de colunas:** {sum([len([c for c in table.table_itens if c.table_item_type == "column"]) for table in self.model.tables])}\n'
            retorno += f'- **Quantidade de colunas calculadas:** {sum([len([c for c in table.table_itens if c.table_item_type == "calculated"]) for table in self.model.tables])}\n'
            retorno += f'- **Quantidade de medidas:** {sum([len([m for m in table.table_itens if m.table_item_type == "measure"]) for table in self.model.tables])}\n'
            return retorno

        def gerar_md_resumo_modelo_tabelas(self) -> str:
            """
            Gera uma lista com as tabelas do modelo de dados.
            A lista contém também o link para a descrição detalhada de cada tabela.
            :return: srt
            """
            retorno = f'\n## Tabelas\n'
            count = 1
            for t in self.model.tables:
                retorno += f'{str(count)}. [{t.name}](#{t.table_id})\n'
                count += 1
            return retorno

        def gerar_md_resumo_modelo_relacionamentos(self) -> str:
            """
            Gera uma tabela com todos os relacionamentos do modelo de dados.
            :return: str
            """
            retorno = f'\n## Relacionamentos\n\n'
            retorno += f'|  |  |  |  |  |\n'
            retorno += f'| ---- | ---- | ---- | ---- | ---- |\n'
            for r in self.model.relationships:
                origin = f'{r.origin_table}[{r.origin_column}]'
                target = f'{r.target_table}[{r.target_column}]'
                direction = f'{" <--> " if r.is_both_directions else " ---> "}'
                if r.is_active:
                    retorno += f'| {origin} | {r.origin_cardinality} | {direction} | {r.target_cardinality} | {target}\n'
                else:
                    retorno += f'| (Desativado) *{origin}* | *{r.origin_cardinality}* | {direction} | *{r.target_cardinality}* | *{target}*\n'
            retorno += f'|  |  |  |  |  |\n'
            return retorno

        def gerar_md_resumo_modelo_medidas(self) -> str:
            """
            Gera uma lista com as medidas do modelo de dados.
            A lista contém também o link para a descrição detalhada de cada medida.
            :return: srt
            """
            retorno = f'\n## Medidas\n'
            count = 1
            for t in self.model.tables:
                for m in [item for item in t.table_itens if item.table_item_type == 'measure']:
                    retorno += f'{str(count)}. [{m.name}](#{m.table_item_id})\n'
                    count += 1
            return retorno

        def gerar_md_detalhamento_tabelas(self) -> str:
            """
            Gera a descrição detalhada de cada tabela do modelo de dados.
            Inclui descrição, colunas, medidas, colunas calculadas, relacionamentos, query e definição no PowerQuery.
            Inclui também âncoras para cada tabela ficar relacionada com um link.
            Este método é composto por outros métodos que geram a descrição de cada item.
            :return: str
            """

            def gerar_md_detalhamento_tabelas_descricao(t) -> str:
                retorno = f'\n<a id="{t.table_id}"></a>\n'
                retorno += f'\n## {t.name}\n'
                retorno += f'- **Nome:** {t.name}\n'
                retorno += f'- **Tipo:** {t.table_type}\n'
                retorno += f'- **Modo de importação:** {t.import_mode}\n'
                retorno += f'- **Descrição:** {" ".join(t.description)}\n' if t.description else ''
                return retorno

            def verificar_tabela(t):
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
                return is_in_relationship, has_columns, has_measures, has_calculated_columns

            def gerar_md_detalhamento_tabelas_colunas(t) -> str:
                retorno = f'\n### Colunas\n'
                count = 0
                for c in [item for item in t.table_itens if item.table_item_type == 'column']:
                    count += 1
                    retorno += f'{str(count)}. {c.name}:  _{c.data_type}_\n'
                return retorno

            def gerar_md_detalhamento_tabelas_colunas_calculadas(t) -> str:
                retorno = f'\n### Colunas calculadas\n'
                count = 0
                for c in [item for item in t.table_itens if item.table_item_type == 'calculated']:
                    count += 1
                    retorno += f'{str(count)}. [{c.name}](#{c.table_item_id}):  _{c.data_type}_\n'
                return retorno

            def gerar_md_detalhamento_tabelas_medidas(t) -> str:
                retorno = f'\n### Medidas\n'
                count = 0
                for m in [item for item in t.table_itens if item.table_item_type == 'measure']:
                    count += 1
                    retorno += f'{str(count)}. [{m.name}](#{m.table_item_id})\n'
                return retorno

            def gerar_md_detalhamento_tabelas_definicao_colunas_calculadas(t) -> str:
                retorno = f'\n### Definições das colunas calculadas\n'
                for c in [item for item in t.table_itens if item.table_item_type == 'calculated']:
                    retorno += f'\n<a id="{c.table_item_id}"></a>\n'
                    retorno += f'\n**{c.name}**\n'
                    retorno += f'- **Interpretação IA:** {c.generate_comment_openai(self.openai_key)}\n' if self.gerar_interpretacao_ia in (
                        2, 3) else ''
                    retorno += f'```dax\n'
                    retorno += f'{c.get_expression_cleaned()}\n'
                    retorno += f'```\n'
                return retorno

            def gerar_md_detalhamento_tabelas_relacionamentos(t) -> str:
                when_both = [r for r in self.model.relationships if r.is_both_directions if
                             r.origin_table == t.name or r.target_table == t.name]
                when_target = [r for r in self.model.relationships if r.target_table == t.name if
                               r.relationship_id not in [r.relationship_id for r in when_both]]
                when_origin = [r for r in self.model.relationships if r.origin_table == t.name if
                               r.relationship_id not in [r.relationship_id for r in when_both]]

                retorno = f'\n### Relacionamentos\n'
                retorno += f'|  |  |  |  |  |\n'
                retorno += f'| ---- | ---- | ---- | ---- | ---- |\n'

                for r in when_origin:
                    origin = f'{r.origin_table}[{r.origin_column}]'
                    target = f'{r.target_table}[{r.target_column}]'
                    if r.is_active:
                        retorno += f'| {origin} | {r.origin_cardinality} |   -->   | {r.target_cardinality} | {target} |\n'
                    else:
                        retorno += f'| (Desativado) *{origin}* | *{r.origin_cardinality}* |   -->   | *{r.target_cardinality}* | *{target}*\n'
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
                    if r.is_active:
                        retorno += f'| {origin} | {origin_cardinality} |   <->   | {target_cardinality} | {target} |\n'
                    else:
                        retorno += f'| (Desativado) *{origin}* | *{origin_cardinality}* |   <->   | *{target_cardinality}* | *{target}*\n'
                for r in when_target:
                    target = f'{r.origin_table}[{r.origin_column}]'
                    origin = f'{r.target_table}[{r.target_column}]'
                    target_cardinality = r.origin_cardinality
                    origin_cardinality = r.target_cardinality
                    if r.is_active:
                        retorno += f'| {origin} | {origin_cardinality} |   <--   | {target_cardinality} | {target} |\n'
                    else:
                        retorno += f'| (Desativado) *{origin}* | *{origin_cardinality}* |   <--   | *{target_cardinality}* | *{target}*\n'

                retorno += f'|  |  |  |  |  |\n'
                return retorno

            def gerar_md_detalhamento_tabelas_query(t) -> str:
                retorno = f'\n### Query:\n'
                retorno += f'```sql\n'
                retorno += f'{t.query}\n'
                retorno += f'```\n'
                return retorno

            def gerar_md_detalhamento_tabelas_power_query(t) -> str:
                retorno = f'\n### Definição no PowerQuery:\n'
                retorno += f'```M\n'
                for step in t.power_query_steps:
                    retorno += f'{step}\n'
                retorno += f'```\n'
                return retorno

            retorno = f'\n# Detalhamento das tabelas\n'
            for t in self.model.tables:
                is_in_relationship, has_columns, has_measures, has_calculated_columns = verificar_tabela(t)
                retorno += gerar_md_detalhamento_tabelas_descricao(t)
                retorno += gerar_md_detalhamento_tabelas_colunas(t) if has_columns else ''
                retorno += gerar_md_detalhamento_tabelas_colunas_calculadas(t) if has_calculated_columns else ''
                retorno += gerar_md_detalhamento_tabelas_medidas(t) if has_measures else ''
                retorno += gerar_md_detalhamento_tabelas_relacionamentos(t) if is_in_relationship else ''
                retorno += gerar_md_detalhamento_tabelas_query(t) if t.query else ''
                retorno += gerar_md_detalhamento_tabelas_power_query(t) if t.power_query_steps else ''
                retorno += gerar_md_detalhamento_tabelas_definicao_colunas_calculadas(
                    t) if has_calculated_columns else ''
            return retorno

        def gerar_md_detalhamento_medidas(self) -> str:
            """
            Gera a descrição detalhada de cada medida do modelo de dados.
            Inclui a tabela a qual a medida pertence, a pasta onde a medida está, o formato, e a expressão.
            Possui também uma âncora para cada medida ficar relacionada com um link.
            :param self:
            :return:
            """
            retorno = f'\n# Detalhamento das medidas\n'
            for t in self.model.tables:
                for m in [item for item in t.table_itens if item.table_item_type == 'measure']:
                    retorno += f'\n<a id="{m.table_item_id}"></a>\n'
                    retorno += f'\n## {m.name}\n'
                    retorno += f'- **Nome:** {m.name}\n'
                    retorno += f'- **Tabela:** [{t.name}](#{t.table_id})\n'
                    retorno += f'- **Pasta:** {m.display_folder if m.display_folder else "Nenhuma"}\n'
                    retorno += f'- **Formato:** ``{m.format_string if m.format_string else "Automático"}``\n'
                    retorno += f'- **Interpretação IA:** {m.generate_comment_openai(self.openai_key)}\n' if self.gerar_interpretacao_ia in (
                        1, 3) else ''
                    retorno += f'\n```dax\n'
                    retorno += f'{m.get_expression_cleaned()}\n'
                    retorno += f'```\n'
            return retorno

        md = ''
        md += gerar_md_cabecalho(self)
        md += gerar_md_resumo_modelo_caracteristicas(self)
        md += gerar_md_resumo_modelo_tabelas(self)
        md += gerar_md_resumo_modelo_relacionamentos(self)
        md += gerar_md_resumo_modelo_medidas(self)
        md += gerar_md_detalhamento_tabelas(self)
        md += gerar_md_detalhamento_medidas(self)
        return md

    def salvar_md(self, md: str):
        """
        Salva a documentação em formato markdown em um arquivo.
        :param md: str
        :return: None
        """
        timestamp = dt.datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            with open(os.path.join(self.model.path, f'Documentação {timestamp}.md'), 'w', encoding='utf-8') as f:
                f.write(md)
            try:
                subprocess.Popen(f'explorer "{self.model.path}"')
            except:
                pass
            print('\n\nDocumentação.md gerada com sucesso!')
        except Exception as e:
            print(f'Erro ao gerar documentação: {e}')
            time.sleep(5)
