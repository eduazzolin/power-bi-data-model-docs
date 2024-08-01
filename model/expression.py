class Expression:
    """
    Expression class to represent a expression in a model.
    """

    def __init__(self,
                 expression_id: str,
                 name: str,
                 description: list,
                 annotations: list,
                 kind: str,
                 expression: list,
                 query_group: str,
                 ):

        """
        Constructor of the class
        :param expression_id: the expression id
        :param name: the expression name
        :param description: the expression description
        :param annotations: annotations associated with the expression
        :param kind: the expression type, can be 'm' or '?'
        :param expression: list of expression (PQ) steps
        :query_group: the query group where this expression can be found
        """
        self.expression_id: str = expression_id
        self.name: str = name
        if isinstance(description,str) and description:
            description = [description,]
        self.description: list = description
        self.annotations : dict = {a.get('name',None): a.get('value',None) for a in annotations}
        self.result_type : str = self.annotations.pop('PBI_ResultType',None)
        self.navigation_step_name : str = self.annotations.pop('PBI_NavigationStepName',None)
        self.kind: str = kind
        if isinstance(expression,str):
            expression = [expression,]
        self.expression: list = expression
        self.query_group: str = query_group

    def __str__(self):
        """
        Method to return a string representation of the expression
        :return: string
        """
        result = ''
        result += f'Name: {self.name}\n'
        result += f'Description: {" ".join(self.description)}\n'
        result += f'Type: {self.expression_type}\n'
        result += f"Result Type: {self.result_type}\n"
        result += f"Navigation Step Name: {self.navigation_step_name}\n"
        result += f"Expression Kind: {self.kind}"
        result += f"Query Group: {self.query_group}"
        result += "Annotations: "
        if not self.annotations:
            result += "None\n"
        else:
            result += "\n"
            for k,v in self.annotations.items():
                result += f"   {k} : {v}\n"
        result += "Expression:\n"
        result += '\n'.join(self.expression)

        return result
