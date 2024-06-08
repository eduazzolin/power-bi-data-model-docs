from service.simplified_markdown import SimplifiedMarkdown
from model.data_model import DataModel
from service.system import save_md
import os
import time

class Comparison:
    def __init__(self, model1: DataModel, model2: DataModel):
        self.model1 = model1
        self.model2 = model2

    def compare(self):
        md1 = SimplifiedMarkdown(self.model1).generate_md()
        md2 = SimplifiedMarkdown(self.model2).generate_md()

        # criar uma pasta temporária oculta
        path_hidden_folder = os.path.dirname(os.path.abspath(__file__))
        path_hidden_folder = os.path.join(path_hidden_folder, '.temp')
        os.makedirs(path_hidden_folder, exist_ok=True)

        # salvar os arquivos markdown
        save_md(md1, path_hidden_folder, 'model1', open_folder=False, silent=True)
        save_md(md2, path_hidden_folder, 'model2', open_folder=False, silent=True)

        print('\nAbrindo Visual Studio Code')
        time.sleep(1)

        # abrir o vscode para comparar os arquivos
        os.system(f'code --diff {path_hidden_folder}/model1.md {path_hidden_folder}/model2.md')
