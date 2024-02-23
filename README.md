# Power BI data model documentation tool
It's a simple tool to generate a markdown documentation of a Power BI data model. It uses Python to extract the data model information from the Power BI pbip files and generate a markdown file as [this example](https://github.com/eduazzolin/power-bi-data-model-documentor/blob/main/example.md).

## How to use
1. Locate the folder where the Power BI pbip file is stored.
2. Run the script `main.py` and paste the path of the folder.
3. The script will generate a markdown file with the data model documentation in the same folder.

## Power BI pbip format
- The Power BI pbip format is currently a preview feature in Power BI Desktop that can be activated in the preview options. Instead of saving the report in a single .pbix file, it saves it in a folder with the .pbip extension. The folder contains all the information of the report in the form of .json and .bim files. For more information about the pbip format, visit the [official documentation](https://learn.microsoft.com/pt-br/power-bi/developer/projects/projects-overview).
- If your report is in the .pbix format, you can save a copy of the report in the .pbip format by going to `File > Save As > Power BI project (.pbip)`, after activating the preview feature.

## Contributing
Feel free to contribute to this project by opening an issue or a pull request. I'm open to suggestions and improvements. To create new forms of exporting the data model documentation, you just need to use the following classes and methods:
```python
from model.model import Model

# Create a model object:
model = Model('path/to/folder', skip_loading=True)

# Your data model object is now ready to be used:
for table in model.tables:
    print(f'The table {table.name} has the following columns:')
    for column in table.table_itens:
        print(f'  - {column.name}')
    print('\n')
```