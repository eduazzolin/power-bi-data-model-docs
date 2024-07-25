import datetime as dt
import os
import time

import pandas as pd


def save(md: str, path: str, prefix: str, format='md', open_folder: bool = False, silent: bool = False):
    """
    Method to save the markdown file.
    :param md: str
    :param path: str
    :param prefix: str
    :param format: str
    :param open_folder: bool
    :param silent: bool
    """
    full_path, path = generate_final_path(path, prefix, format, silent)

    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(md)
        if not silent:
            print('\n\nDocumentação gerada com sucesso!\nCaminho: ' + full_path)
        if open_folder:
            try:
                os.startfile(path)
            except:
                pass
    except Exception as e:
        print(f'Erro ao gerar documentação: {e}')
        time.sleep(5)


def generate_final_path(path, prefix, format, silent=False):
    """
    Method to generate the final path of the file.
    :param path: location of the file
    :param prefix: name like 'documentation'
    :param format: ending of the file like 'md'
    :param silent: bool, if True, won't include the timestamp in the file name and won't print the success message
    :return: str with the path and name of the file and str with the path of the file
    """
    if path.startswith('localhost'):
        path = os.getcwd()
    if os.path.isfile(path):
        path = os.path.dirname(path)
    timestamp = dt.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'{prefix}{(" " + timestamp) if not silent else ""}.{format}'
    full_path = os.path.join(path, file_name)
    return full_path, path


def save_csv(df: pd.DataFrame, path: str, prefix: str, open_folder: bool = False):
    """
    save a DataFrame as a csv file
    :param df: Pandas.DataFrame
    :param path: path to save the file
    :param prefix: name of the file
    :param open_folder: if True, open the folder after saving the file
    :return: None
    """
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
    """
    Save a DataFrame as a xlsx file
    :param df: Pandas.DataFrame
    :param path: path to save the file
    :param prefix: name of the file
    :param open_folder: if True, open the folder after saving the file
    :return: None
    """
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
