import os
import subprocess
import sys
import time

from service.fields_table import FieldsTable
from service.markdown import Markdown
from service.measures_table import MeasuresTable
from model.data_model import DataModel
from service.simplified_markdown import SimplifiedMarkdown

class Main:

    @staticmethod
    def ask_function():
        return int(input(f'\nEscolha a função:'
                         f'\n1. Gerar documentação de modelo de dados'
                         f'\n2. Exportar tabela com medidas'
                         f'\n3. Exportar tabela com campos e uso'
                         f'\n4. Exportar documentação simpificada'
                         f'\nEscolha: '))

    @staticmethod
    def ask_model_type():
        return int(input(f'\nEscolha o tipo de modelo de dados:'
                         f'\n1. Modelo de dados pbip'
                         f'\n2. Arquivo model.bim'
                         f'\nEscolha: '))

    @staticmethod
    def ask_ia_description():
        return int(input('\nDeseja gerar interpretações com IA (beta)?'
                         '\n0. Não'
                         '\n1. Somente medidas'
                         '\n2. Somente colunas calculadas'
                         '\n3. Tudo'
                         '\nEscolha: '))

    @staticmethod
    def ask_openai_key():
        return input('\nDigite a chave da API do OpenAI: ')

    @staticmethod
    def ask_export_type():
        return int(input('\nEscolha o formato de exportação:'
                         '\n1. Arquivo xlsx'
                         '\n2. Arquivo csv'
                         '\nEscolha: '))

    @staticmethod
    def open_result_folder(path):
        try:
            subprocess.Popen(f'explorer "{path}"')
        except:
            pass

    @staticmethod
    def print_title():
        print('-' * 40)
        print('Power BI Data Model Documentation Tool')
        print('-' * 40)

    def main(self):
        '''
        Main function to generate the documentation of the data model.
        It is executed when the script is called without arguments.
        '''


        function = self.ask_function()

        model = None
        while model is None:
            model_type = self.ask_model_type()
            try:
                if model_type == 1:
                    path = input('\nDigite o caminho da pasta raiz do modelo \nde dados: ')
                    model = DataModel(path, model_type=1)
                elif model_type == 2:
                    path = input('\nDigite o caminho da pasta em que está o \narquivo model.bim: ')
                    model = DataModel(path, model_type=2)
            except FileNotFoundError:
                print('\nArquivo não encontrado. Verifique o caminho e tente novamente.')

        if function == 1:
            ia_description = self.ask_ia_description()
            openai_key = self.ask_openai_key() if ia_description != 0 else None
            markdown = Markdown(model, ia_description, openai_key)
            documentacao_md = markdown.gerar_md()
            markdown.salvar_md(documentacao_md)
        elif function == 2:
            export_type = self.ask_export_type()
            if export_type == 1:
                measures_table = MeasuresTable(model)
                measures_table.save_xlsx()
            elif export_type == 2:
                measures_table = MeasuresTable(model)
                measures_table.save_csv()
        elif function == 3:
            export_type = self.ask_export_type()
            if export_type == 1:
                fields_table = FieldsTable(model)
                fields_table.save_xlsx()
            elif export_type == 2:
                fields_table = FieldsTable(model)
                fields_table.save_csv()
        elif function == 4:
            service = SimplifiedMarkdown(model)
            service.save_md(service.generate_md())

        self.open_result_folder(path)

    def autorun(self):
        '''
        Function to be executed when the script is called with the argument 'autorun'.
        '''
        path = os.path.dirname(__file__)
        time.sleep(2)
        try:
            model = DataModel(path, model_type=2)
            service = SimplifiedMarkdown(model)
            service.save_md(service.generate_md())
            time.sleep(3)
            exit()
        except FileNotFoundError:
            print('\nERRO: Nenhum arquivo model.bim foi encontrado na pasta do script.')
            time.sleep(60)


if __name__ == '__main__':
    self = Main()
    self.print_title()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'autorun':
            self.autorun()
    else:
        self.main()
