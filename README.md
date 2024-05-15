# Power BI data model documentation tool
It's a simple tool to generate documentation of a Power BI data model. It uses Python to extract the data model information from a pbip project or a model.bim file and can generate a markdown doc as [this example](https://github.com/eduazzolin/power-bi-data-model-documentor/blob/main/docs/example.md) and other spreadsheets.

## Features
- Generates a markdown file with the data model documentation.
- Exports a CSV or Excel file with all the measures of the data model.
- Exports a CSV or Excel file with all the columns and an indicator of its usage in the data model. (beta)
- Supports pbip projects and model.bim files.

## How to use
1. Install the required packages by running the command `pip install -r ./docs/requirements.txt`.
2. Run the script `main.py` with the command ``python main.py`` and follow the instructions.
3. The script will generate the chosen document in the same folder.

![how-to-use](https://github.com/eduazzolin/power-bi-data-model-documentation-tool/assets/114076084/4c27e92c-1146-409c-926a-8112e35a6942)


### Autorun option
1. You can also run the script without the need to paste the path, by putting the `Model.bim` file in the same folder as the script and running the ``autorun.cmd`` file.
2. The autorun option will generate the documentation in the same folder as the script.

![autorun](https://github.com/eduazzolin/power-bi-data-model-documentation-tool/assets/114076084/67d44d99-ec46-4619-aac7-2f5010b529e9)


## Power BI pbip format
- The Power BI pbip format is currently a preview feature in Power BI Desktop that can be activated in the preview options. Instead of saving the report in a single .pbix file, it saves it in a folder with the .pbip extension. The folder contains all the information of the report in the form of .json and .bim files. For more information about the pbip format, visit the [official documentation](https://learn.microsoft.com/pt-br/power-bi/developer/projects/projects-overview).
- If your report is in the .pbix format, you can save a copy of the report in the .pbip format by going to `File > Save As > Power BI project (.pbip)`, after activating the preview feature.

## Model.bim file
- The model.bim file is a JSON file that contains the data model information of a Power BI report. It can be exported by opening the data model in [Tabular Editor](https://github.com/TabularEditor/TabularEditor) and going to `File > Save As > Model.bim`.

## Contributing
Feel free to contribute to this project by opening an issue or a pull request. I'm open to suggestions and improvements. To create new forms of exporting the data model documentation, you just need to use the following classes and methods:
```python
from model.data_model import DataModel

# Create a model object:
model = DataModel('path/to/folder', skip_loading=True)

# Your data model object is now ready to be used:
for table in model.tables:
    print(f'The table {table.name} has the following columns:')
    for column in table.table_itens:
        print(f'  - {column.name}')
    print('\n')
```
