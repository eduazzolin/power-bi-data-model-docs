class TableItem:
    def __init__(self, id: str, name: str, type: str = 'column', data_type: str = None, format_string: str = None,
                 display_folder: str = None, is_hidden: bool = False, expression: list = None):
        self.id = id
        self.name = name
        self.type = type
        self.dataType = data_type
        self.formatString = format_string
        self.displayFolder = display_folder
        self.isHidden = is_hidden
        self.expression = expression

    def __str__(self):
        return f'{self.name} {self.type}'
