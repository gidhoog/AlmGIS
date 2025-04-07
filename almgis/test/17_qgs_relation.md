<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# create two tables based on a qgsattributetableview where the data is in a parent child relation. selecting a row in the parent table should limit the row in the child table to the only related rows. create a working example in pyqgis standalone application

Here's a PyQGIS standalone implementation using `QgsAttributeTableView` with parent-child table filtering:

```python
from qgis.core import QgsApplication, QgsProject, QgsVectorLayer, QgsRelation, QgsAttributeTableView
from qgis.gui import QgsAttributeTableFilterModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter

# Initialize QGIS Application
qgs = QgsApplication([], False)
qgs.initQgis()

# Create parent and child layers
parent_layer = QgsVectorLayer("None?field=id:integer&amp;field=name:string", "Parent", "memory")
child_layer = QgsVectorLayer("None?field=id:integer&amp;field=parent_id:integer&amp;field=child_data:string", "Child", "memory")

# Add sample data
with edit(parent_layer):
    parent_layer.addFeature(QgsFeature(parent_layer.fields()).setAttributes([1, "Parent 1"]))
    parent_layer.addFeature(QgsFeature(parent_layer.fields()).setAttributes([2, "Parent 2"]))

with edit(child_layer):
    child_layer.addFeature(QgsFeature(child_layer.fields()).setAttributes([1, 1, "Child 1-1"]))
    child_layer.addFeature(QgsFeature(child_layer.fields()).setAttributes([2, 1, "Child 1-2"]))
    child_layer.addFeature(QgsFeature(child_layer.fields()).setAttributes([3, 2, "Child 2-1"]))

# Create relation
relation = QgsRelation()
relation.setId("parent_child")
relation.setName("Parent-Child")
relation.setReferencingLayer(child_layer.id())
relation.setReferencedLayer(parent_layer.id())
relation.addFieldPair("parent_id", "id")
relation.isValid()  # Should return True

# Create main window
widget = QWidget()
layout = QVBoxLayout()
splitter = QSplitter()

# Create attribute table views
parent_view = QgsAttributeTableView()
child_view = QgsAttributeTableView()

# Set models with relation filtering
parent_filter_model = QgsAttributeTableFilterModel(parent_view)
parent_filter_model.setSourceModel(parent_layer)
parent_view.setModel(parent_filter_model)

child_filter_model = QgsAttributeTableFilterModel(child_view)
child_filter_model.setSourceModel(child_layer)
child_view.setModel(child_filter_model)

# Connect selection events
def filter_child_table():
    selected = parent_view.selectionModel().selectedRows()
    if selected:
        parent_id = parent_layer.getFeature(selected[^1_0].row())["id"]
        child_filter_model.setFilterExpression(f'"parent_id" = {parent_id}')
    else:
        child_filter_model.setFilterExpression("")

parent_view.selectionModel().selectionChanged.connect(filter_child_table)

# Layout setup
splitter.addWidget(parent_view)
splitter.addWidget(child_view)
layout.addWidget(splitter)
widget.setLayout(layout)
widget.show()

# Execute application
qgs.exec_()
qgs.exitQgis()
```

**Key components explained:**

1. **Relation Setup**
The parent-child relationship is established using `QgsRelation` with field pairing between `parent_id` (child) and `id` (parent)[^1_8][^1_9].
2. **Dynamic Filtering**
The `filter_child_table` function updates the child table's filter expression based on the selected parent row using `QgsAttributeTableFilterModel`[^1_8].
3. **Standalone Initialization**
QGIS environment is initialized without GUI components (`QgsApplication([], False)`) but still supports Qt widgets[^1_3][^1_10].
4. **Table Views**
`QgsAttributeTableView` provides native QGIS attribute table functionality with built-in filtering capabilities[^1_8].

To run this script:

1. Adjust QGIS prefix path in `setPrefixPath()`
2. Install PyQt5 and pyqgis dependencies
3. Execute in a Python environment with QGIS libraries

The child table will automatically filter to show only records related to the selected parent row. Multiple parent-child relationships can be added by creating additional relations and filter models[^1_6][^1_9].

<div>⁂</div>

[^1_1]: https://community.fabric.microsoft.com/t5/Desktop/How-to-create-parent-child-data-structure-to-build-a-ragged/td-p/3529146

[^1_2]: https://github.com/opengisch/QField/discussions/5745

[^1_3]: https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/intro.html

[^1_4]: https://community.qlik.com/t5/QlikView-App-Dev/create-2-tables-from-one/td-p/1778464

[^1_5]: https://stackoverflow.com/questions/71647032/creating-a-qtreewidget-from-a-parent-child-table-in-python

[^1_6]: https://www.opengis.ch/de/2022/11/29/qgis-relations-their-widgets-and-the-plugins-of-them/

[^1_7]: https://blocks.roadtolarissa.com/thomasg77/f711853e5fb81c746d2a1af0b2a9ecf5

[^1_8]: https://qgis.org/pyqgis/3.40/gui/QgsAttributeTableView.html

[^1_9]: https://docs.qgis.org/latest/en/docs/user_manual/working_with_vector/joins_relations.html

[^1_10]: https://github.com/MarByteBeep/pyqgis-standalone

