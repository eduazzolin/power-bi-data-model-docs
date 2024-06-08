import subprocess

from model.data_model import DataModel
from service.fields_table import FieldsTable
from service.markdown import Markdown
from service.measures_table import MeasuresTable
from service.simplified_markdown import SimplifiedMarkdown
from service.ssas import list_running_ssas
from service.system import save_md, save_xlsx, save_csv


class Main:

    @staticmethod
    def ask_function():
        return int(input(f'\nEscolha a função:'
                         f'\n1. Gerar documentação de modelo de dados'
                         f'\n2. Exportar documentação simpificada'
                         f'\n3. Exportar tabela com medidas'
                         f'\n4. Exportar tabela com campos e uso'
                         f'\nEscolha: '))

    @staticmethod
    def ask_path():
        instances = list_running_ssas()
        print(f'\nA qual modelo deseja conectar?'
              f'\n1. Buscar arquivo model.bim')
        for i, instance in enumerate(instances):
            print(f'{i + 2}. MODELO RODANDO: {instance}')

        escolha = int(input('\nEscolha: '))

        if escolha == 1:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(filetypes=[("BIM files", "*.bim")])
            return file_path
        else:
            return instances[escolha - 2]

    @staticmethod
    def ask_export_type():
        return int(input('\nEscolha o formato de exportação:'
                         '\n1. Arquivo xlsx'
                         '\n2. Arquivo csv'
                         '\nEscolha: '))

    @staticmethod
    def print_title():
        print('-' * 40)
        print('Power BI Data Model Documentation Tool')
        print('-' * 40)

    def run(self):
        '''
        Main function to generate the documentation of the data model.
        It is executed when the script is called without arguments.
        '''

        # Asking wich function the user wants to execute
        function = self.ask_function()

        model = None
        while model is None:
            try:
                path = self.ask_path()
                model = DataModel(path=path)
            except Exception as e:
                print(f'\nERRO: {e}')

        if function == 1:
            # Generate full documentation
            service = Markdown(model)
            md = service.gerar_md()
            save_md(md, model.path, 'data_model_doc', open_folder=True)
        elif function == 2:
            # Export simplified documentation
            service = SimplifiedMarkdown(model)
            md = service.generate_md()
            save_md(md, model.path, 'data_model_simpl_doc', open_folder=True)
        elif function == 3:
            # Export measures table
            service = MeasuresTable(model)
            data_frame = service.generate_data_frame()
            export_type = self.ask_export_type()
            if export_type == 1:
                save_xlsx(data_frame, model.path, 'measures_table', True)
            elif export_type == 2:
                save_csv(data_frame, model.path, 'measures_table', True)
        elif function == 4:
            # Export fields table
            service = FieldsTable(model)
            data_frame = service.generate_data_frame()
            export_type = self.ask_export_type()
            if export_type == 1:
                save_xlsx(data_frame, model.path, 'fields_table', True)
            elif export_type == 2:
                save_csv(data_frame, model.path, 'fields_table', True)


if __name__ == '__main__':
    executable = Main()
    executable.print_title()
    while True:
        executable.run()
