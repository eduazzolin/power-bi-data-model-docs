from markdown import Markdown
from measures_table import MeasuresTable
from model import Model


def ask_function():
    return int(input(f'\nEscolha a função:'
                     f'\n1. Gerar documentação de modelo de dados'
                     f'\n2. Exportar tabela com medidas'
                     f'\nEscolha: '))


def ask_model_type():
    return int(input(f'\nEscolha o tipo de modelo de dados:'
                     f'\n1. Modelo de dados pbip'
                     f'\n2. Arquivo model.bim'
                     f'\nEscolha: '))


def ask_ia_description():
    return int(input('\nDeseja gerar interpretações com IA (beta)?'
                     '\n0. Não'
                     '\n1. Somente medidas'
                     '\n2. Somente colunas calculadas'
                     '\n3. Tudo'
                     '\nEscolha: '))


def ask_openai_key():
    return input('\nDigite a chave da API do OpenAI: ')


def ask_measures_table_type():
    return int(input('\nEscolha o tipo de tabela de medidas:'
                     '\n1. Arquivo xlsx'
                     '\n2. Arquivo csv'
                     '\nEscolha: '))


print(f'\nGeração de documentação de modelo de dados\n{"-" * 40}')

function = ask_function()
model_type = ask_model_type()

if model_type == 1:
    path = input('\nDigite o caminho da pasta raiz do modelo de dados: ')
    model = Model(path, model_type=1)
elif model_type == 2:
    path = input('\nDigite o caminho da pasta em que está o arquivo model.bim: ')
    model = Model(path, model_type=2)

if function == 1:
    ia_description = ask_ia_description()
    openai_key = ask_openai_key() if ia_description != 0 else None
    markdown = Markdown(model, ia_description, openai_key)
    documentacao_md = markdown.gerar_md()
    markdown.salvar_md(documentacao_md)
elif function == 2:
    measures_table_type = ask_measures_table_type()
    if measures_table_type == 1:
        measures_table = MeasuresTable(model)
        measures_table.save_xlsx()
    elif measures_table_type == 2:
        measures_table = MeasuresTable(model)
        measures_table.save_csv()
