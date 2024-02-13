class TableItem:
    def __init__(self, table_item_id: str, name: str, table_item_type: str = 'column', data_type: str = None, format_string: str = None,
                 display_folder: str = None, is_hidden: bool = False, expression: list = None):
        self.table_item_id = table_item_id
        self.name = name
        self.table_item_type = table_item_type
        self.data_type = data_type
        self.format_string = format_string
        self.display_folder = display_folder
        self.is_hidden = is_hidden
        self.expression = expression

    def __str__(self):
        return f'{self.name} {self.type}'
