# Power BI data model documentation tool
It's a simple tool to generate documentation of a Power BI data model. It uses Python to extract the data model information and can generate a markdown doc as [this example](https://github.com/eduazzolin/power-bi-data-model-documentor/blob/main/docs/example.md) and other spreadsheets.

## Features
- Generates a markdown file with the data model documentation.
- Exports a CSV or Excel file with all the measures of the data model.
- Exports a CSV or Excel file with all the columns and an indicator of its usage in the data model. (beta)
- Can connect to running Power BI Desktop instances or use a model.bim file.

## How to use
1. Install the required packages by running the command `pip install -r requirements.txt`.
2. Run the script `main.py` with the command ``python main.py`` and follow the instructions.

## Contributing
Feel free to contribute to this project by opening an issue or a pull request. I'm open to suggestions and improvements. To create new forms of exporting the data model documentation, you just need to use the following classes and methods:
```python
from model.data_model import DataModel

# Create a model object:
model = DataModel('./model.bim', skip_loading=True)

# Your data model object is now ready to be used:
for table in model.tables:
    print(f'The table {table.name} has the following columns:')
    for column in table.table_itens:
        print(f'  - {column.name}')
    print('\n')
```
