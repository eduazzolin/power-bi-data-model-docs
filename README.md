# gerador_de_documentacao_pbi
## lista de arquivos pbip
### .Dataset
1. diagramLayout.json: layouts dos diagramas de relacionamentos do power bi
2. _item.config.json: irrelevante_
3. _item.metadata.json: irrelevante_
4. **model.bim: todos os dados sobre o modelo de dados do power bi**
5. _.pbi/editorSettings.json: irrelevante_
6. _.pbi/localSettings.json: irrelevante_

## model.bin
### itens não muito relevantes:
- annotations: irrelevante
- cultures: acho que é a configuração de idioma e localização
- dataAccessOptions: irrelevante
- expressions: ?
- queryGroups: pastas do power query
### itens relevantes:
#### relationships
lista com todos os relacionamentos entre tabelas:
```json
"relationships": [
      {
        "name": "c2f20cd7-bc3b-4575-b181-9e9b719f3efe",
        "fromColumn": "data",
        "fromTable": "meta_dim_accounts",
        "joinOnDateBehavior": "datePartOnly",
        "toColumn": "Date",
        "toTable": "LocalDateTable_923a44a9-02f7-4826-a9a9-a363fdd0a00a"
      },
      {
        "name": "33b6d5fe-9b70-4466-b6aa-3535b1483e9d",
        "fromColumn": "data",
        "fromTable": "meta_dim_campanhas",
        "joinOnDateBehavior": "datePartOnly",
        "toColumn": "Date",
        "toTable": "LocalDateTable_3cefa55b-7d13-4d7c-8248-f8535575265c"
      },
 ```
Atributos:
o padrão é 1 - *
- 'name': id
- 'toColumn', 'toTable': a que filtra
- 'fromColumn','fromTable': a que é filtrada
- 'toCardinality',  'fromCardinality': podem ser 'one' ou 'many' e quando uma aparece a outra não
- 'crossFilteringBehavior': pode ser 'bothDirections'
- 'name': id
- 'joinOnDateBehavior': irrelevante


 'isActive': 
#### tables
lista com todas as tabelas do modelo de dados:
```json
{
        "name": "DE_PARA_TAGS",
        "annotations": [
          {
            "name": "PBI_ResultType",
            "value": "Table"
          },
          {
            "name": "PBI_NavigationStepName",
            "value": "Navegação"
          }
        ],
        "columns": [
          {
            "name": "ID CLIENTE",
            "annotations": [
              {
                "name": "SummarizationSetBy",
                "value": "Automatic"
              }
            ],
            "dataType": "string",
            "lineageTag": "4d21b5d5-7ea9-4176-99c0-0c311624da52",
            "sourceColumn": "ID CLIENTE",
            "summarizeBy": "none"
          },
          {
            "name": "CANAL",
            "annotations": [
              {
                "name": "SummarizationSetBy",
                "value": "Automatic"
              }
            ],
            "dataType": "string",
            "lineageTag": "aecc44f8-fca9-4454-9fde-fbf9dac5f650",
            "sourceColumn": "CANAL",
            "summarizeBy": "none"
          },
          {
            "name": "TAG",
            "annotations": [
              {
                "name": "SummarizationSetBy",
                "value": "Automatic"
              }
            ],
            "dataType": "string",
            "lineageTag": "b8bbc816-f641-4e14-b7b5-f626dae25af3",
            "sourceColumn": "TAG",
            "summarizeBy": "none"
          },
          {
            "name": "campaign_id",
            "annotations": [
              {
                "name": "SummarizationSetBy",
                "value": "Automatic"
              }
            ],
            "dataType": "string",
            "lineageTag": "accf9b70-4852-42bf-b915-f5997c1c57c8",
            "sourceColumn": "campaign_id",
            "summarizeBy": "none"
          },
          {
            "name": "campaign_name",
            "annotations": [
              {
                "name": "SummarizationSetBy",
                "value": "Automatic"
              }
            ],
            "dataType": "string",
            "expression": [
              "",
              "VAR id_daqui = DE_PARA_TAGS[campaign_id]",
              "RETURN",
              "    CALCULATE(",
              "        MAX('CANAIS UNIFICADOS'[campaign_name]),",
              "        'CANAIS UNIFICADOS'[campaign_id] = id_daqui",
              "    )"
            ],
            "isDataTypeInferred": true,
            "lineageTag": "9a54a875-f01f-47e7-86a6-ac0ede8ed081",
            "summarizeBy": "none",
            "type": "calculated"
          }
        ],
        "lineageTag": "726a9261-f882-4af3-99d7-8fd3b78f77b6",
        "partitions": [
          {
            "name": "DE_PARA_TAGS",
            "mode": "import",
            "queryGroup": "GOOGLE SHEETS",
            "source": {
              "expression": [
                "let",
                "    Fonte = BASE_SHEETS,",
                "    De_Para_TAGs_Table = Fonte{[name=\"De_Para_TAGs\",ItemKind=\"Table\"]}[Data],",
                "    #\"Cabeçalhos Promovidos\" = Table.PromoteHeaders(De_Para_TAGs_Table, [PromoteAllScalars=true]),",
                "    #\"Tipo Alterado\" = Table.TransformColumnTypes(#\"Cabeçalhos Promovidos\",{{\"ID CLIENTE\", type text}, {\"CLIENTE\", type text}, {\"CANAL\", type text}, {\"CAMPANHA\", type text}, {\"TAG\", type any}, {\"\", type any}, {\"MANUAL DA TABELA\", type text}, {\"ID CAMPANHA\", type text}}),",
                "    #\"Colunas Removidas\" = Table.RemoveColumns(#\"Tipo Alterado\",{\"MANUAL DA TABELA\", \"\", \"CLIENTE\"}),",
                "    #\"Linhas Filtradas\" = Table.SelectRows(#\"Colunas Removidas\", each [TAG] <> null and [TAG] <> \"\"),",
                "    #\"Colunas Renomeadas\" = Table.RenameColumns(#\"Linhas Filtradas\",{{\"ID CAMPANHA\", \"campaign_id\"}}),",
                "    #\"Texto Limpo\" = Table.TransformColumns(#\"Colunas Renomeadas\",{{\"TAG\", Text.Clean, type text}}),",
                "    #\"Texto em Maiúscula\" = Table.TransformColumns(#\"Texto Limpo\",{{\"TAG\", Text.Upper, type text}}),",
                "    #\"Colunas Removidas1\" = Table.RemoveColumns(#\"Texto em Maiúscula\",{\"CAMPANHA\"})",
                "in",
                "    #\"Colunas Removidas1\""
              ],
              "type": "m"
            }
          }
        ]
      },
```