class Relationship:
    """
    Class to represent a relationship between two tables
    """

    def __init__(self, relationship_id: str, origin_column: str, origin_table: str, origin_cardinality: str,
                 target_column: str,
                 target_table: str, target_cardinality: str, is_active: bool, is_both_directions: bool):
        """
        Constructor of the class
        :param relationship_id: id of the relationship
        :param origin_column: column that filters the target table
        :param origin_table: table that filters the target table
        :param origin_cardinality: cardinality of the origin table, can be 'one' or 'many'
        :param target_column: column that is filtered by the origin table
        :param target_table: table that is filtered by the origin table
        :param target_cardinality: cardinality of the target table, can be 'one' or 'many'
        :param is_active: if the relationship is active
        :param is_both_directions:
        """
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
        """
        Method to return a string representation of the relationship
        :return: str
        """
        origin = f'{self.origin_table}[{self.origin_column}]'
        target = f'{self.target_table}[{self.target_column}]'
        cardinality = f'{self.origin_cardinality:4} {" <--> " if self.is_both_directions else " ---> "} {self.target_cardinality:4}'
        return f'{origin[:50]:50}     {cardinality}     {target}'
