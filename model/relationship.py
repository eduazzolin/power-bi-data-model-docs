class Relationship:
    def __init__(self, id: str, origin_column: str, origin_table: str, origin_cardinality: str, target_column: str,
                 target_table: str, target_cardinality: str, is_active: bool, is_both_directions: bool):
        self.id = id
        self.originColumn = origin_column
        self.originTable = origin_table
        self.targetColumn = target_column
        self.targetTable = target_table
        self.isActive = is_active
        self.originCardinality = origin_cardinality
        self.targetCardinality = target_cardinality
        self.isBothDirections = is_both_directions
        
    def __str__(self):
        origin = f'{self.originTable}[{self.originColumn}]'
        target = f'{self.targetTable}[{self.targetColumn}]'
        cardinality = f'{self.originCardinality:4} {" <--> " if self.isBothDirections else " ---> "} {self.targetCardinality:4}'
        return f'{origin[:35]:35}     {cardinality}     {target[:35]:35}'