import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

import requests
import winsound

from model.data_model import DataModel
from service.comparison import Comparison
from service.fields_table import FieldsTable
from service.html import HTML
from service.measures_table import MeasuresTable
from service.simplified_markdown import SimplifiedMarkdown
from service.ssas import list_formatted_instances
from service.system import save, save_xlsx, save_csv


class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Power BI Data Model Documentation Tool")
        self.geometry("550x500")
        self.version = 1.1
        try:
            self.iconbitmap('docs/ico.ico')
        except:
            self.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ico.ico'))
        self.create_widgets()

    def open_file_dialog(self):
        """
        Method to open the file dialog to select a file
        """
        file_path = filedialog.askopenfilename(filetypes=[("BIM files", "*.bim")])
        if file_path:
            print(f"File selected: {file_path}")
            self.file_path_var.set(file_path)

    def create_widgets(self):
        self.label = tk.Label(self, text="Escolha a função:", font=("Arial", 14))
        self.label.pack(pady=10, padx=5)

        self.function_var = tk.StringVar()
        self.function_combobox = ttk.Combobox(self, textvariable=self.function_var, font=("Arial", 12), width=50,
                                              state="readonly")
        self.function_combobox['values'] = ('Exportar documentação de modelo de dados em HTML',
                                            'Exportar documentação simplificada em markdown',
                                            'Exportar tabela com medidas',
                                            'Exportar tabela com campos e uso',
                                            'Comparar dois modelos de dados')
        self.function_combobox.current(0)
        self.function_combobox.pack(pady=10)
        self.function_combobox.bind('<<ComboboxSelected>>', self.on_function_select)

        self.model1_label = tk.Label(self, text="Selecione um modelo semântico:", font=("Arial", 14))
        self.model1_label.pack(pady=10)

        self.model1_var = tk.StringVar()
        self.model1_combobox = ttk.Combobox(self, textvariable=self.model1_var, font=("Arial", 12), width=50,
                                            state="readonly")
        self.model1_combobox['values'] = list_formatted_instances() + ['Arquivo model.bim']
        self.model1_combobox.current(0)
        self.model1_combobox.pack(pady=10)
        self.file_path_var = tk.StringVar()

        self.model2_label = tk.Label(self, text="Selecione o segundo modelo semântico:", font=("Arial", 14))
        self.model2_var = tk.StringVar()
        self.model2_combobox = ttk.Combobox(self, textvariable=self.model2_var, font=("Arial", 12), width=50,
                                            state="readonly")
        self.model2_combobox['values'] = list_formatted_instances() + ['Arquivo model.bim']

        self.run_button = tk.Button(self, text="Executar", command=self.run_function, font=("Arial", 14), width=15,
                                    bg="lightgray")
        self.run_button.pack(pady=20)

        self.update_button = tk.Button(self, text="Verificar atualização", command=self.check_update,
                                       font=("Arial", 10))
        self.update_button.pack(side=tk.BOTTOM, pady=10)

    def refresh_list(self):
        """
        Method to refresh the list of running valid SSAS instances
        """
        self.model1_combobox['values'] = list_formatted_instances() + ['Arquivo model.bim']
        self.model2_combobox['values'] = list_formatted_instances() + ['Arquivo model.bim']

    def on_function_select(self, event):
        """
        Method to handle the event when the user selects a function
        """
        if self.function_var.get() == 'Comparar dois modelos de dados':
            self.model2_label.pack(pady=10)
            self.model2_combobox.pack(pady=10)
            self.run_button.pack_forget()
            self.run_button.pack(pady=20)
        else:
            self.model2_label.pack_forget()
            self.model2_combobox.pack_forget()
            self.run_button.pack_forget()
            self.run_button.pack(pady=20)

    def ask_export_type(self):
        """
        Method to ask the user the export type
        :return: str with the export type
        """
        export_type = None
        export_window = tk.Toplevel(self)
        export_window.title("Escolha o formato de exportação")

        label = tk.Label(export_window, text="Escolha o formato de exportação:")
        label.pack(pady=10)

        export_var = tk.StringVar()
        xlsx_button = tk.Radiobutton(export_window, text="Arquivo xlsx", variable=export_var, value="xlsx")
        xlsx_button.select()
        xlsx_button.pack(pady=5)
        csv_button = tk.Radiobutton(export_window, text="Arquivo csv", variable=export_var, value="csv")
        csv_button.pack(pady=5)

        def confirm_export_type():
            nonlocal export_type
            export_type = export_var.get()
            export_window.destroy()

        confirm_button = tk.Button(export_window, text="Confirmar", command=confirm_export_type)
        confirm_button.pack(pady=20)

        self.wait_window(export_window)

        return export_type

    def get_models(self):
        """
        Method to get the models selected by the user
        :return: list with the models
        """
        models = []
        try:
            if self.model1_var.get() == 'Arquivo model.bim':
                self.open_file_dialog()
                models.append(DataModel(self.file_path_var.get(), skip_loading=True))
            else:
                models.append(DataModel(self.model1_var.get(), skip_loading=True))
        except Exception as e:
            raise Exception("Não foi possível conectar ao modelo semântico")

        if self.model2_var.get():
            try:
                if self.model2_var.get() == 'Arquivo model.bim':
                    self.open_file_dialog()
                    models.append(DataModel(self.file_path_var.get(), skip_loading=True))
                else:
                    models.append(DataModel(self.model2_var.get(), skip_loading=True))
            except Exception as e:
                raise Exception("Não foi possível conectar ao modelo semântico")
        else:
            models.append(None)
        return models

    def run_function(self):
        function = self.function_var.get()

        try:
            model, model2 = self.get_models()
        except Exception as e:
            messagebox.showerror('Erro', str(e))
            return

        path = model.path
        if path.startswith('localhost'):
            path = os.getcwd() + '\\'
        else:
            path = os.path.dirname(path) + '\\'

        if function:
            try:
                function_index = self.function_combobox['values'].index(function) + 1

                # Export HTML documentation
                if function_index == 1:
                    service = HTML(model)
                    html = service.gerar_html()
                    save(html, model.path, format='html', prefix='data_model_doc')
                    os.startfile(path)

                # Export simplified markdown documentation
                elif function_index == 2:
                    service = SimplifiedMarkdown(model)
                    md = service.generate_md()
                    save(md, model.path, 'data_model_simpl_doc')
                    os.startfile(path)

                # Export measures table
                elif function_index == 3:
                    service = MeasuresTable(model)
                    data_frame = service.generate_data_frame()
                    export_type = self.ask_export_type()
                    if not export_type:
                        return
                    if export_type == 'xlsx':
                        save_xlsx(data_frame, model.path, 'measures_table')
                    elif export_type == 'csv':
                        save_csv(data_frame, model.path, 'measures_table')
                    os.startfile(path)

                # Export fields table
                elif function_index == 4:
                    service = FieldsTable(model)
                    data_frame = service.generate_data_frame()
                    export_type = self.ask_export_type()
                    if not export_type:
                        return
                    if export_type == 'xlsx':
                        save_xlsx(data_frame, model.path, 'fields_table')
                    elif export_type == 'csv':
                        save_csv(data_frame, model.path, 'fields_table')
                    os.startfile(path)

                # Compare two data models
                elif function_index == 5:
                    service = Comparison(model, model2)
                    service.compare()


                # Tocar o som do Windows de sucesso (SystemAsterisk)
                winsound.MessageBeep(winsound.MB_ICONASTERISK)

            except Exception as e:
                messagebox.showerror('Erro', f'ERRO: {e}')

    def check_update(self):
        """
        Method to check if there is a new version available
        It compares the current version with the latest release on GitHub
        """
        try:
            version = self.version
            url = f"https://api.github.com/repos/eduazzolin/power-bi-data-model-docs/releases/latest"
            response = requests.get(url)
            if response.status_code == 200:
                latest_release = response.json()
                latest_release = float(latest_release['tag_name'])
                if latest_release > version:
                    messagebox.showinfo('Atualização disponível',
                                        f'Nova versão disponível: {latest_release}\nClique em OK para abrir no navegador.')
                    # oppens the browser with the release page
                    os.system('start https://github.com/eduazzolin/power-bi-data-model-docs/releases')
                else:
                    messagebox.showinfo('Atualização', 'Você já está utilizando a versão mais recente.')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao verificar atualização: {e}')


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
