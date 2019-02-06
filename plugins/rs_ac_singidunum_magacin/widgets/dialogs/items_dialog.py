from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from ...item.item_service import ItemService
from ...item.item import Item

class ItemsDialog(QtWidgets.QDialog):
    """ 
    Klasa koja predstavlja dialog u kojoj se prikazuje lista proizvoda
    """
    def __init__(self, parent=None):
        """
        Inicijalizator dijaloga za podesavanje i prikaz proizvoda.

        :param selected_hall: selektovana hala
        :type hall: Hall
        :param parent: roditeljski widget dijaloga.
        :type parent: QWidget
        """
        # podesavanje dijaloga
        super().__init__(parent)
        self.setWindowTitle("Proizvodi")
        # prosiriv ekran velicina
        self.resize(800,750)
        # postavljanje ikonice prozora
        self.setWindowIcon(QIcon("resources/icons/address-book-blue.png")) 

        items = ItemService()
        items.load_items('all')
        self.item_service = items
        self.item_dialog_layout = QtWidgets.QVBoxLayout()

        self.items_table = QtWidgets.QTableWidget(self)
        self.items_table.verticalHeader().setVisible(False)
        self.items_table.horizontalHeader().setVisible(True)
        self.items_table.horizontalHeader().setSortIndicatorShown(True)
        self.items_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.items_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.items_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.items_table.setGridStyle(Qt.SolidLine)
        self.items_table.setAlternatingRowColors(True)

         # popunjavamo toolbar
        self._set_toolbar()

        self._populate_table()

        self.items_table.horizontalHeader().setStretchLastSection(True)
        
        self.item_dialog_layout.addLayout(self.item_options_layout)
        self.item_dialog_layout.addWidget(self.items_table)
        
        
        self.setLayout(self.item_dialog_layout)

        self.items_table.setSortingEnabled(True)

    def _set_toolbar(self):
        """
        Populise toolbar sa korisnim funkcijama.
        """
        self.item_options_layout = QtWidgets.QHBoxLayout()
        self.plugin_dialog_layout = QtWidgets.QVBoxLayout()


    def _populate_table(self):
        """
        Populiše tabelu sa podacima za proivod.
        """
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels(
            ["Ime proizvoda", "Rok upotrebe", "Temperatura za cuvanje", "Kolicina", "Hala"])
        self.items_table.setRowCount(len(self.item_service.items))
        self.items_table.setColumnWidth(0, 200)
        self.items_table.setColumnWidth(2, 220)
        for i, item in enumerate(self.item_service.items):
            name = QtWidgets.QTableWidgetItem(item.name)
            expiration_date = QtWidgets.QTableWidgetItem(item.expiration_date)
            item_count = QtWidgets.QTableWidgetItem(str(item.item_count))
            temperature = QtWidgets.QTableWidgetItem(str(item.temperature))
            hall_id = QtWidgets.QTableWidgetItem(str(item.hall_id))

            self.items_table.setItem(i, 0, name)
            self.items_table.setItem(i, 1, expiration_date)
            self.items_table.setItem(i, 2, temperature)
            self.items_table.setItem(i, 3, item_count)
            self.items_table.setItem(i, 4, hall_id)

    
    def get_item(self, item):
        """
        Dobavlja podatke iz tabele.
        
        :param item: selektovan red, proizvod
        :type item: QItem
        :returns: Item -- inicializuje proizvod.
        """   
        name = item[0].text()
        expiration_date = item[1].text()
        temperature = int(item[2].text())
        item_count = int(item[3].text())
        hall_id = int(item[4].text())

        return Item(name, expiration_date, temperature, item_count, hall_id)
    