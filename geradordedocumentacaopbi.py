from model.model import Model


class GeradorDeDocumentacaoPBI:
    def __init__(self):
        pass


def main():
    model = Model('..\\exemplo')
    for t in model.tables:
        print(t, '\n\n\n')


if __name__ == '__main__':
    main()
