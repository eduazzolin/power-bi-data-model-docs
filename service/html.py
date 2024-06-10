import datetime as dt

from model.data_model import DataModel


class HTML:
    """
    Service class to generate the documentation in HTML format using Bootstrap.
    """

    def __init__(self, model: DataModel):
        """
        Constructor of the class.
        :param model: DataModel
        """
        self.model = model

    def gerar_html(self) -> str:
        """
        Gera a documentação em formato HTML com Bootstrap.
        :return: string com a documentação.
        """

        def gerar_html_cabecalho(self) -> str:
            retorno = f'''
<div class="row pt-4">
    <div class="col-12">
        <h2>Documentação de modelo de dados</h2>
        <p>{dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
    </div>
    <div class="col-lg-6">
        <p>Quantidade de tabelas: {len(self.model.tables)} <br>
            Quantidade de relacionamentos: {len(self.model.relationships)} <br>
            Quantidade de colunas: {sum([len([c for c in table.table_itens if c.table_item_type == "column"]) for table in self.model.tables])} <br>
            Quantidade de colunas calculadas: {sum([len([c for c in table.table_itens if c.table_item_type == "calculated"]) for table in self.model.tables])}<br>
            Quantidade de medidas: {sum([len([m for m in table.table_itens if m.table_item_type == "measure"]) for table in self.model.tables])} </p>
    </div>
</div>
            '''
            return retorno

        def gerar_html_detalhamento_tabelas(self) -> str:
            count = 1
            retorno = '''
<div class="row pt-4">
    <div class="col-12">
        <h3>Tabelas</h3>
        <div class="accordion" id="accordionExample">
            '''

            for t in self.model.tables:
                query = '\n'.join(t.power_query_steps)
                query = (query.replace("&", "&amp;")
                         .replace("<", "&lt;")
                         .replace(">", "&gt;")
                         .replace('"', "&quot;")
                         .replace("'", "&#39;"))
                relations = [r for r in self.model.relationships if
                             r.origin_table == t.name or r.target_table == t.name]
                columns = [c for c in t.table_itens if c.table_item_type == 'column']
                measures = [m for m in t.table_itens if m.table_item_type == 'measure']
                calculated_columns = [cc for cc in t.table_itens if cc.table_item_type == 'calculated']

                retorno += f'''
            <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed type="button" data-bs-toggle="collapse" 
                        data-bs-target="#collapse{count}" aria-expanded="false" aria-controls="collapse{count}">
                        {t.name}
                    </button>
                </h2>
                <div id="collapse{count}" class="accordion-collapse collapse">
                    <div class="accordion-body">
                        <h5>Descrição</h5>
                        <ul>
                            <li><strong>Nome:</strong> {t.name}</li>
                            <li><strong>Tipo:</strong> <code>{t.table_type}</code></li>
                            <li><strong>Modo de importação:</strong> <code>{t.import_mode}</code></li>
                        </ul>
                '''
                if query:
                    retorno += f'''    
                        <h5>Power Query</h5>
                        <pre class="border rounded ps-3 m-3">
                            <code>
{query}
                            </code>
                        </pre>
                    '''

                if relations:
                    retorno += f'''
                        <h5>Relacionamentos</h5>
                            <table class="table table-bordered table-hover table-striped small">
                                <thead>
                                    <tr>
                                        <th></th>
                                        <th></th>
                                        <th></th>
                                        <th></th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                        '''
                    for r in relations:
                        origin = f'{r.origin_table}[{r.origin_column}]'
                        target = f'{r.target_table}[{r.target_column}]'
                        direction = f'{" <--> " if r.is_both_directions else " ---> "}'
                        if r.is_active:
                            retorno += f'''
                                    <tr><td>{origin}</td><td>{r.origin_cardinality}</td><td>{direction}</td><td>{r.target_cardinality}</td><td>{target}</td></tr>
                            '''
                        else:
                            retorno += f'''
                                    <tr><td><em>(Desativado) {origin}</em></td><td><em>{r.origin_cardinality}</em></td><td>{direction}</td><td><em>{r.target_cardinality}</em></td><td><em>{target}</em></td></tr>
                            '''
                    retorno += f'''
                                </tbody>
                            </table>
                    '''

                if columns or measures or calculated_columns:
                    retorno += '''
                        <div class="row">
                            <div class="col-12">
                                <h5>Itens</h5>
                            </div>
                        '''
                    if columns:
                        retorno += '''
                            <div class="col-md-4">
                                <table class="table table-bordered table-hover table-striped small">
                                    <thead>
                                        <tr>
                                            <th>Coluna</th>
                                            <th>Tipo</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                            '''
                        for c in columns:
                            retorno += f'''
                                        <tr><td>{c.name}</td><td>{c.data_type}</td></tr>
                            '''
                        retorno += f'''
                                    </tbody>
                                </table>
                            </div>
                        '''
                    if measures:
                        retorno += '''
                            <div class="col-md-4">
                                <table class="table table-bordered table-hover table-striped small">
                                    <thead>
                                        <tr>
                                            <th>Medida</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                            '''
                        for m in measures:
                            retorno += f'''
                                        <tr><td><a href="#{m.table_item_id}">{m.name}</a></td></tr>
                            '''
                        retorno += f'''
                                    </tbody>
                                </table>
                            </div>
                        '''
                    if calculated_columns:
                        retorno += '''
                            <div class="col-md-4">
                                <table class="table table-bordered table-hover table-striped small">
                                    <thead>
                                        <tr>
                                            <th>Coluna Calculada</th>
                                            <th>Tipo</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                            '''
                        for cc in calculated_columns:
                            retorno += f'''
                                        <tr><td><a href="#{cc.table_item_id}">{cc.name}</a></td><td>{cc.data_type}</td></tr>
                            '''
                        retorno += f'''
                                    </tbody>
                                </table>
                            </div>
                        '''
                    retorno += '''
                        </div>
                    '''

                retorno += """
                    </div>
                </div>
            </div>
            """
                count += 1
            retorno += """
        </div>
    </div>
</div>
"""
            return retorno

        def gerar_html_resumo_modelo_relacionamentos(self) -> str:
            retorno = '''
<div class="row pt-4">
    <div class="col-12">
        <h3>Relacionamentos</h3>
        <table class="table table-bordered table-hover table-striped small">
            <thead>
                <tr>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
            '''
            for r in self.model.relationships:
                origin = f'{r.origin_table}[{r.origin_column}]'
                target = f'{r.target_table}[{r.target_column}]'
                direction = f'{" <--> " if r.is_both_directions else " ---> "}'
                if r.is_active:
                    retorno += f'''
                <tr><td>{origin}</td><td>{r.origin_cardinality}</td><td>{direction}</td><td>{r.target_cardinality}</td><td>{target}</td></tr>
                    '''
                else:
                    retorno += f'''
                <tr><td><em>(Desativado) {origin}</em></td><td><em>{r.origin_cardinality}</em></td><td>{direction}</td><td><em>{r.target_cardinality}</em></td><td><em>{target}</em></td></tr>
                    '''
            retorno += f'''
            </tbody>
        </table>
    </div>
</div>
            '''
            return retorno

        def gerar_html_resumo_modelo_medidas(self) -> str:
            """
            Gera uma lista com as medidas do modelo de dados.
            A lista contém também o link para a descrição detalhada de cada medida.
            :return: str
            """
            retorno = '''
<div class="row pt-4">
    <div class="col-12">
        <h3>Medidas</h3>
    </div>
            '''
            for m in self.model.get_all_measures():
                retorno += f'''
    <div class="row border rounded p-2 ms-2 my-2">
        <div class="col-md-4 ">
            <a id="{m.table_item_id}"></a>  
            <h5 class="mb-2">{m.name}</h5>
            <strong>Tabela:</strong> {m.table}
            <br><strong>Pasta:</strong> {m.display_folder if m.display_folder else "Nenhuma"}
            <br><strong>Formato:</strong> <code>{m.format_string}</code>
        </div>
        <div class="col-md-8">
            <pre class="border rounded p-2">
                <code>
{m.get_expression_cleaned(html=True)}
                </code>
            </pre>
        </div>
    </div>
                '''
            retorno += '''
</div>
            '''

            return retorno

        def gerar_html_detalhamento_colunas_calculadas(self) -> str:
            retorno = '''
<div class="row pt-4">
    <div class="col-12">
        <h3>Colunas Calculadas</h3>
    </div>
                        '''
            for m in self.model.get_all_calculated_columns():
                retorno += f'''
    <div class="row border rounded p-2 ms-2 my-2">
        <div class="col-md-4">
            <a id="{m.table_item_id}"></a>  
            <h5 class="mb-2">{m.name}</h5>
            <strong>Tabela:</strong> {m.table}
            <br><strong>Pasta:</strong> {m.display_folder if m.display_folder else "Nenhuma"}
            <br><strong>Tipo:</strong> {m.data_type}
            <br><strong>Formato:</strong> <code>{m.format_string}</code>
        </div>
        <div class="col-md-8">
            <pre class="border rounded p-2">
                <code>
    {m.get_expression_cleaned(html=True)}
                </code>
            </pre>
        </div>
    </div>
                            '''
            retorno += '''
</div>
            '''

            return retorno

        def envelopar_html(html: str) -> str:
            return f'''
<html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
            crossorigin="anonymous"></script>
    </head>
    <body>
        <div class="container pb-5">
        
        
{html}


        </container>
    </body>
</html>'
'''

        html = ''
        html += gerar_html_cabecalho(self)
        html += gerar_html_detalhamento_tabelas(self)
        html += gerar_html_resumo_modelo_relacionamentos(self)
        html += gerar_html_resumo_modelo_medidas(self)
        html += gerar_html_detalhamento_colunas_calculadas(self)

        return envelopar_html(html)
