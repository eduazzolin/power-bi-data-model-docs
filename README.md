# Power BI data model documentation tool
It's a simple tool to generate documentation of a Power BI data model. It uses Python to extract the data model information and can generate various types of documentations, such as [these examples](https://github.com/eduazzolin/power-bi-data-model-documentor/blob/main/examples).

## Features
- Generates a HTML file documentations for a data model.
- Generates a simplified markdown file with the data model information.
- Generates a CSV or Excel file with all the measures of the data model.
- Generates a CSV or Excel file with all the columns and an indicator of its usage in the data model. (beta)
- Can compare two data models.
- Can connect to running Power BI Desktop instances or use a model.bim file.

## How to use
1. Download the [latest executable release](https://github.com/eduazzolin/power-bi-data-model-documentation-tool/releases/download/V1/Power-BI-Data-Model-Docs.exe).
2. Run the executable file and follow the instructions. No installation is required.

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
