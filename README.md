# FMCW App

This GUI was developed to assist the development and test of the FMCW Radar Project. Using the Qt Designer available in the PySide6 package.

## GUI developement

To launch the Qt Designer, open the terminal and run:

```bash
pyside6-designer
```

This will open the graphical interface where you can wmodify the applica your application's GUI. For example:

![Qt Designer Screenshot](images/img.png)

After designing your interface, save your work as a `.ui` file. This file can be loaded directly in `main.py` using PySide6. For more information on working with `.ui` files in PySide6, see the [official tutorial](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html#tutorial-uifiles).

The `.ui` constains solely a skeleton of the GUI. The look and feel of the GUI  is defined in the `stylesheet.qss` file. This file is loaded in the `main.py` file.

## Creating the executable

To create the executable, run the following command in your terminal:

```bash
python build_executable.py
```

This script will package the application and its dependencies into a standalone executable.

## Generating the dependencies file

After adding new dependencies to the project, update the `requirements.txt` file by running:

```bash
pip freeze > requirements.txt
```

This command will capture all installed Python packages and their versions, ensuring other collaborators have the same versions of the packages.
