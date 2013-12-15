from PySide import QtCore
from PySide import QtGui
from qtodotxt.lib.filters import *
from qtodotxt.ui.resource_manager import getIcon

class FiltersTreeView(QtGui.QWidget):
    
    filterSelectionChanged = QtCore.Signal(list)
    
    def __init__(self, parent=None):
        super(FiltersTreeView, self).__init__(parent)
        self._filterItemByFilterType = dict()
        self._filterIconByFilterType = dict()
        self._treeItemByFilterType = dict()
        self._initUI()

    def getSelectedFilters(self):
        items = self._tree.selectedItems()
        filters = [item.filter for item in items]
        return filters

    def clear(self):
        self._tree.clear()
        self._addDefaultTreeItems(self._tree)
        self._initFilterTypeMappings()

    def clearSelection(self):
        self._tree.clearSelection()

    def addFilter(self, filter):
        parentItem = self._filterItemByFilterType[type(filter)]
        icon = self._filterIconByFilterType[type(filter)]
        FilterTreeWidgetItem(parentItem, [filter.text], filter=filter, icon=icon)
        parentItem.setExpanded(True)
        parentItem.sortChildren(0,QtCore.Qt.AscendingOrder)
            
    def selectAllTasksFilter(self):
        self._incompleteTasksItem.setSelected(True)

    def _selectItem(self, item):
        if item:
            item.setSelected(True)
            self._tree.setCurrentItem(item)        

    def _selectContext(self, context):
        item = self._findItem(context, self._contextsItem)
        self._selectItem(item)
              
    def _selectProject(self, project):
        item = self._findItem(project, self._projectsItem)
        self._selectItem(item)

    def _findItem(self, text, parentItem):
        for index in range(parentItem.childCount()):
            child = parentItem.child(index)
            if child.text(0) == text:
                return child
        return None

    def _initUI(self):
        layout = QtGui.QGridLayout()
        self.setLayout(layout)
        self._tree = self._createTreeWidget()
        layout.addWidget(self._tree)

    def _createTreeWidget(self):
        tree = QtGui.QTreeWidget()
        tree.header().hide()
        tree.setSelectionMode(
            QtGui.QAbstractItemView.SelectionMode.ExtendedSelection)
        tree.itemSelectionChanged.connect(self._tree_itemSelectionChanged)
        self._addDefaultTreeItems(tree)
        self._initFilterTypeMappings()
        return tree
        
    def _addDefaultTreeItems(self, tree):
        self._incompleteTasksItem = \
            FilterTreeWidgetItem(None, ['Pending'], IncompleteTasksFilter(), getIcon('time.png'))
        self._uncategorizedTasksItem = \
            FilterTreeWidgetItem(None, ['Uncategorized'], UncategorizedTasksFilter(), getIcon('help.png'))
        self._contextsItem = \
            FilterTreeWidgetItem(None, ['Contexts'], HasContextsFilter(), getIcon('at.png'))
        self._projectsItem = \
            FilterTreeWidgetItem(None, ['Projects'], HasProjectsFilter(), getIcon('plus.png'))
        self._completeTasksItem = \
            FilterTreeWidgetItem(None, ['Complete'], CompleteTasksFilter(), getIcon('x.png'))
        tree.addTopLevelItems([
            self._incompleteTasksItem,
            self._uncategorizedTasksItem,
            self._contextsItem,
            self._projectsItem,
            self._completeTasksItem])
        
    def _initFilterTypeMappings(self):
        self._filterItemByFilterType[ContextFilter] = self._contextsItem
        self._filterItemByFilterType[ProjectFilter] = self._projectsItem
        self._filterIconByFilterType[ContextFilter] = getIcon('at.png')
        self._filterIconByFilterType[ProjectFilter] = getIcon('plus.png')
        self._treeItemByFilterType[IncompleteTasksFilter] = self._incompleteTasksItem
        self._treeItemByFilterType[UncategorizedTasksFilter] = self._uncategorizedTasksItem
        self._treeItemByFilterType[CompleteTasksFilter] = self._completeTasksItem
        self._treeItemByFilterType[HasProjectsFilter] = self._projectsItem
        self._treeItemByFilterType[HasContextsFilter] = self._contextsItem

    def _tree_itemSelectionChanged(self):
        self.filterSelectionChanged.emit(self.getSelectedFilters())

    def selectFilter(self, filter):
        if isinstance(filter, ContextFilter):
            self._selectContext(filter.text)
        elif isinstance(filter, ProjectFilter):
            self._selectProject(filter.text)
        else:
            item = self._treeItemByFilterType[type(filter)]
            self._selectItem(item)
            
class FilterTreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent, strings, filter=None, icon=None):
        QtGui.QTreeWidgetItem.__init__(self, parent, strings)
        self.filter = filter
        if icon:
            self.setIcon(0, icon)
