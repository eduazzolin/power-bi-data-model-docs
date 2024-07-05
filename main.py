import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import requests

from model.data_model import DataModel
from service.comparison import Comparison
from service.fields_table import FieldsTable
from service.html import HTML
from service.measures_table import MeasuresTable
from service.simplified_markdown import SimplifiedMarkdown
from service.ssas import list_running_ssas
from service.system import save, save_xlsx, save_csv


class MainApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Power BI Data Model Documentation Tool")
        self.geometry("500x400")
        self.version = 1.0  # Defina a versão atual do seu aplicativo aqui
        self.create_widgets()

    def create_widgets(self):
        # Create and place widgets in the main window
        self.label = tk.Label(self, text="Escolha a função:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.function_var = tk.StringVar()
        self.function_combobox = ttk.Combobox(self, textvariable=self.function_var, font=("Arial", 12), width=40, state="readonly")
        self.function_combobox['values'] = ('Exportar documentação de modelo de dados em HTML',
                                            'Exportar documentação simplificada em markdown',
                                            'Exportar tabela com medidas',
                                            'Exportar tabela com campos e uso',
                                            'Comparar dois modelos de dados')
        self.function_combobox.pack(pady=10)

        self.run_button = tk.Button(self, text="Executar", command=self.run_function, font=("Arial", 14), width=15, bg="lightgray")
        self.run_button.pack(pady=20)

        self.update_button = tk.Button(self, text="Verificar atualização", command=self.check_update, font=("Arial", 10))
        self.update_button.pack(side=tk.BOTTOM, pady=10)

    def ask_model(self):
        model = None
        while model is None:
            try:
                instances = list_running_ssas()
                escolha = messagebox.askquestion('Modelo', 'Buscar arquivo model.bim?')

                if escolha == 'yes':
                    file_path = filedialog.askopenfilename(filetypes=[("BIM files", "*.bim")])
                    if file_path:
                        model = DataModel(path=file_path)
                else:
                    # Create a new window for selecting running instances
                    select_window = tk.Toplevel(self)
                    select_window.title("Selecione o modelo rodando")

                    label = tk.Label(select_window, text="Escolha o modelo rodando:")
                    label.pack(pady=10)

                    instance_var = tk.StringVar()
                    instance_combobox = ttk.Combobox(select_window, textvariable=instance_var, state="readonly")
                    instance_combobox['values'] = instances
                    instance_combobox.pack(pady=10)

                    def confirm_selection():
                        nonlocal model
                        selected_instance = instance_var.get()
                        if selected_instance:
                            model = DataModel(selected_instance)
                        select_window.destroy()

                    confirm_button = tk.Button(select_window, text="Confirmar", command=confirm_selection)
                    confirm_button.pack(pady=20)

                    self.wait_window(select_window)

            except Exception as e:
                messagebox.showerror('Erro', f'ERRO: {e}')
                return None
        
        return model

    def ask_export_type(self):
        export_type = None
        export_window = tk.Toplevel(self)
        export_window.title("Escolha o formato de exportação")

        label = tk.Label(export_window, text="Escolha o formato de exportação:")
        label.pack(pady=10)

        export_var = tk.StringVar()
        xlsx_button = tk.Radiobutton(export_window, text="Arquivo xlsx", variable=export_var, value="xlsx")
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

    def run_function(self):
        function = self.function_var.get()
        
        if function:
            try:
                function_index = self.function_combobox['values'].index(function) + 1
                if function_index == 5:
                    model1 = self.ask_model()
                    if not model1:
                        return
                    model2 = self.ask_model()
                    if not model2:
                        return
                    service = Comparison(model1, model2)
                    service.compare()
                else:
                    model = self.ask_model()
                    if not model:
                        return
                    
                    if function_index == 1:
                        service = HTML(model)
                        html = service.gerar_html()
                        save(html, model.path, format='html', prefix='data_model_doc', open_folder=True)
                    elif function_index == 2:
                        service = SimplifiedMarkdown(model)
                        md = service.generate_md()
                        save(md, model.path, 'data_model_simpl_doc', open_folder=True)
                    elif function_index == 3:
                        service = MeasuresTable(model)
                        data_frame = service.generate_data_frame()
                        export_type = self.ask_export_type()
                        if not export_type:
                            return
                        if export_type == 'xlsx':
                            save_xlsx(data_frame, model.path, 'measures_table', True)
                        elif export_type == 'csv':
                            save_csv(data_frame, model.path, 'measures_table', True)
                    elif function_index == 4:
                        service = FieldsTable(model)
                        data_frame = service.generate_data_frame()
                        export_type = self.ask_export_type()
                        if not export_type:
                            return
                        if export_type == 'xlsx':
                            save_xlsx(data_frame, model.path, 'fields_table', True)
                        elif export_type == 'csv':
                            save_csv(data_frame, model.path, 'fields_table', True)
            except Exception as e:
                messagebox.showerror('Erro', f'ERRO: {e}')

    def check_update(self):
        try:
            version = self.version
            url = f"https://api.github.com/repos/eduazzolin/power-bi-data-model-docs/releases/latest"
            response = requests.get(url)
            if response.status_code == 200:
                latest_release = response.json()
                latest_release = float(latest_release['tag_name'])
                if latest_release > version:
                    messagebox.showinfo('Atualização disponível', f'Nova versão disponível: {latest_release}\nVeja em: {url}')
                else:
                    messagebox.showinfo('Atualização', 'Você já está utilizando a versão mais recente.')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao verificar atualização: {e}')


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
