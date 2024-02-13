class Relationship:
    def __init__(self, relationship_id: str, origin_column: str, origin_table: str, origin_cardinality: str, target_column: str,
                 target_table: str, target_cardinality: str, is_active: bool, is_both_directions: bool):
        self.relationship_id = relationship_id
        self.origin_column = origin_column
        self.origin_table = origin_table
        self.target_column = target_column
        self.target_table = target_table
        self.is_active = is_active
        self.origin_cardinality = origin_cardinality
        self.target_cardinality = target_cardinality
        self.is_both_directions = is_both_directions
        
    def __str__(self):
        origin = f'{self.origin_table}[{self.origin_column}]'
        target = f'{self.target_table}[{self.target_column}]'
        cardinality = f'{self.origin_cardinality:4} {" <--> " if self.is_both_directions else " ---> "} {self.target_cardinality:4}'
        return f'{origin[:50]:50}     {cardinality}     {target}'