from model.model import Model


class GeradorDeDocumentacaoPBI:
    def __init__(self):
        pass


def main():
    model = Model('..\\exemplo')
    for t in model.tables:
        print(f'{t.name[:30]:30} - {t.table_type}')

if __name__ == '__main__':
    main()
