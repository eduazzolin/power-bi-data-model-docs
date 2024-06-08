import datetime as dt
import os
import time

import pandas as pd


def save_md(md: str, path: str, prefix: str, open_folder: bool = False):
    """
    Method to save the markdown file.
    :param md: str
    :param path: str
    :param prefix: str
    """
    full_path, path = generate_final_path(path, prefix, 'md')

    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(md)
        print('\n\nDocumentação gerada com sucesso!\nCaminho: ' + full_path)
        if open_folder:
            try:
                os.startfile(path)
            except:
                pass
    except Exception as e:
        print(f'Erro ao gerar documentação: {e}')
        time.sleep(5)


def generate_final_path(path, prefix, format):
    if path.startswith('localhost'):
        path = os.getcwd()
    if path.upper().endswith('MODEL.BIM'):
        path = path[:-9]
    timestamp = dt.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'{prefix} {timestamp}.{format}'
    full_path = os.path.join(path, file_name)
    return full_path, path


def save_csv(df: pd.DataFrame, path: str, prefix: str, open_folder: bool = False):
    full_path, path = generate_final_path(path, prefix, 'csv')
    try:
        df.to_csv(full_path, index=False, encoding='utf-8', lineterminator='\n')
        print(f'\nTabela gerada com sucesso!\nCaminho: {full_path}')
        if open_folder:
            try:
                os.startfile(path)
            except:
                pass
    except Exception as e:
        print(f'Erro ao gerar tabela: {e}')
        time.sleep(5)


def save_xlsx(df: pd.DataFrame, path: str, prefix: str, open_folder: bool = False):
    full_path, path = generate_final_path(path, prefix, 'xlsx')
    try:
        with pd.ExcelWriter(full_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            cell_format = workbook.add_format({'text_wrap': False})
            worksheet.set_column('A:Z', cell_format=cell_format)
        print(f'\nTabela gerada com sucesso!\nCaminho: {full_path}')
        if open_folder:
            try:
                os.startfile(path)
            except:
                pass
    except Exception as e:
        print(f'Erro ao gerar tabela: {e}')
        time.sleep(5)
