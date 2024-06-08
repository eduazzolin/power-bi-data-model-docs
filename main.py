import subprocess

from model.data_model import DataModel
from service.fields_table import FieldsTable
from service.markdown import Markdown
from service.measures_table import MeasuresTable
from service.simplified_markdown import SimplifiedMarkdown
from service.ssas import list_running_ssas
from service.system import save_md, save_xlsx, save_csv
from service.comparison import Comparison
from service.html import HTML


class Main:

    @staticmethod
    def ask_function():
        return int(input(f'\nEscolha a função:'
                         f'\n1. Exportar documentação de modelo de dados em HTML'
                         f'\n2. Exportar documentação simpificada em markdown'
                         f'\n3. Exportar tabela com medidas'
                         f'\n4. Exportar tabela com campos e uso'
                         f'\n5. Comparar dois modelos de dados'
                         f'\n\nEscolha: '))

    @staticmethod
    def ask_model():
        model = None
        while model is None:
            try:
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
                    model = DataModel(path=file_path)
                else:
                    model = DataModel(instances[escolha - 2])
            except Exception as e:
                print(f'\nERRO: {e}')

        return model

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

        if function == 5:
            print('-' * 40)
            print("\nEscolha o primeiro modelo de dados:")

        # Asking for the path of the data model
        model = self.ask_model()

        if function == 1:
            # Generate full documentation
            service = HTML(model)
            md = service.gerar_html()
            save_md(md, model.path, 'data_model_doc.HTML', open_folder=True, silent=True)

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

        elif function == 5:
            print('-' * 40)
            print("\nEscolha o segundo modelo de dados:")
            model1 = model
            model2 = self.ask_model()
            service = Comparison(model1, model2).compare()




if __name__ == '__main__':
    executable = Main()
    executable.print_title()
    while True:
        executable.run()
