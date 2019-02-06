from PySide2 import QtWidgets
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from .dialogs.add_hall_dialog import AddHallDialog
from .dialogs.item_dialog import ItemDialog
from .dialogs.items_dialog import ItemsDialog
from ..hall.hall import Hall

class Magacin(QtWidgets.QMainWindow):
    """
    Klasa koja predstavlja glavni prozor plagina za magacin.

    """
    def __init__(self, hall_service, parent: QtWidgets.QWidget=None):
        """
        Inicijalizator za prozor - za magacin.

        :param halls: hall servis koji nam obezbedjuje operacije nad halama.
        :type halls: HallService
        :param parent: roditeljski widget (default: None).
        :type parent: QWidget
        """
        # pozivanje super inicijalizatora(super - predstavlja konstruktor)
        super().__init__(parent) 
        
        # cuvan se atribut za hall servise
        self.hall_service = hall_service

        # centralni widget predstavlja deo glavnog prozora u koji treba da se smesti glavni widget aplikacije
        self.centralwidget = QtWidgets.QWidget(self)

        # layout sluzi za namestanje i stilizovanje table-a       
        self.halls_dialog_layout = QtWidgets.QGridLayout(self.centralwidget)
        # table widget
        self.halls_table = QtWidgets.QTableWidget(self.centralwidget)
        self.halls_table.verticalHeader().setVisible(False)
        self.halls_table.horizontalHeader().setVisible(True)
        self.halls_table.horizontalHeader().setSortIndicatorShown(True)
        self.halls_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.halls_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # u trenutku mozemo samo jedan red da selektujemo
        self.halls_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.halls_table.setGridStyle(Qt.SolidLine)
        self.halls_table.setAlternatingRowColors(True)

        # tabela se popunjava sa podacima
        self._populate_table()
        self.halls_table.horizontalHeader().setStretchLastSection(True)

        self.halls_dialog_layout.addWidget(self.halls_table, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.halls_table.setSortingEnabled(True)

        # popunjava se toolbar
        self._set_toolbar()
        # pozivaju se sopstvene privatne metode
        self._bind_actions()
        self.halls_table.setFocusPolicy(Qt.ClickFocus)

    def _set_toolbar(self):
        """
        Populiše toolbar sa korisnim funkcijama.
        """
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.add_hall = QtWidgets.QAction(self)
        self.add_hall.setIcon(QIcon("resources/icons/application-plus.png"))
        self.delete_hall = QtWidgets.QAction(self)
        self.delete_hall.setIcon(QIcon("resources/icons/minus-circle.png"))
        self.item_hall = QtWidgets.QAction(self)
        self.item_hall.setIcon(QIcon("resources/icons/category-item.png"))
        self.item_all = QtWidgets.QAction(self)
        self.item_all.setIcon(QIcon("resources/icons/application-block.png"))
        self.toolBar.addAction(self.add_hall)
        self.toolBar.addAction(self.delete_hall)
        self.toolBar.addAction(self.item_hall)
        self.toolBar.addAction(self.item_all)
        self.add_hall.setText("Dodaj Halu")
        self.add_hall.setToolTip("Dodaj Halu")
        self.delete_hall.setText("Obriši Halu")
        self.delete_hall.setToolTip("Obriši Halu")
        self.item_hall.setText("Otvori listu proizvoda u hali")
        self.item_hall.setToolTip("Otvori listu proizvoda u hali")
        self.item_all.setText("Otvori listu proizvoda")
        self.item_all.setToolTip("Otvori listu proizvoda")

    def _populate_table(self):
        """
        Populiše tabelu sa podacima za halu.
        """
        self.halls_table.clear()
        self.halls_table.setColumnCount(4)
        self.halls_table.setHorizontalHeaderLabels(
               ["Ime hale", "Popunjena Mesta", "Kapacitet hale", "Tip hale"])
        self.halls_table.setColumnWidth(1, 150)
        self.halls_table.setColumnWidth(2, 150)
        self.halls_table.setRowCount(len(self.hall_service.halls))
        for i, hall in enumerate(self.hall_service.halls):
            name = QtWidgets.QTableWidgetItem(hall.name)
            places_total = QtWidgets.QTableWidgetItem(str(hall.places_total))
            places_filled = QtWidgets.QTableWidgetItem(str(hall.places_filled))
            hall_type =  self._hall_type(hall.hall_type)
            hall_type = QtWidgets.QTableWidgetItem(hall_type)

            self.halls_table.setItem(i, 0, name)
            self.halls_table.setItem(i, 1, places_filled)
            self.halls_table.setItem(i, 2, places_total)
            self.halls_table.setItem(i, 3, hall_type)

    def _bind_actions(self):
        """
        Uvezuje akcije sa funkcijama koje se izvršavaju na njihovo pokretanje.
        """
        self.add_hall.triggered.connect(self._on_add)
        self.delete_hall.triggered.connect(self._on_delete)
        self.item_hall.triggered.connect(self._on_item)
        self.item_all.triggered.connect(self._on_items)

    def _on_add(self):
        """
        Dodaje novu halu u Magacin.
        """
        self.halls_table.setSortingEnabled(False)
        dialog = AddHallDialog()
        answer = dialog.exec_()
        if answer != 0:
            provera = self.hall_service.create(dialog.new_hall)
            if provera:
                self._populate_table()
                self.hall_service.add_hall(dialog.new_hall)
                QtWidgets.QMessageBox.information(self, "Obaveštenje", "Hala je uspešno uneta", QtWidgets.QMessageBox.Ok)
            else:
                QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Hala nije uspešno uneta", QtWidgets.QMessageBox.Ok)            
        self.halls_table.setSortingEnabled(True)    
        
    def _on_item(self):
        """
        Metoda koja poziva odgovarajucu listu proizvoda u odnosu na izabranu halu.
        """
        self.halls_table.setSortingEnabled(False)   
        selected_hall = self.halls_table.selectedItems()
        if len(selected_hall) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Molimo Vas odaberite halu", QtWidgets.QMessageBox.Ok)
        hall = self.get_hall(selected_hall)
        index = self.hall_service.halls.index(hall)
        selected_hall = self.hall_service.halls[index]
        dialog = ItemDialog(self.hall_service,selected_hall)
        dialog.exec_()
        
        self._populate_table()
        self.halls_table.setSortingEnabled(True)   

    def _on_items(self):
        """
        Metoda koja poziva odgovarajucu listu proizvoda koji se nalaze u svim halama.
        """
        self.halls_table.setSortingEnabled(False)   
        dialog = ItemsDialog()
        dialog.exec_()
        self.halls_table.setSortingEnabled(True)   


    def _on_delete(self):
        """
        Metoda koja briše-uklanja halu koja je odabrana iz tabele hala.
        """
        self.halls_table.setSortingEnabled(False)
        selected_hall = self.halls_table.selectedItems()
        if len(selected_hall) == 0:
            return QtWidgets.QMessageBox.warning(self, "Obaveštenje", "Odaberite halu koju zelite da obrisete.", QtWidgets.QMessageBox.Ok)
        hall = self.get_hall(selected_hall)
        provera = self.hall_service.delete(hall)
        if provera:
            self._populate_table()
            self.hall_service.delete_hall(hall)
            QtWidgets.QMessageBox.information(self, "Obaveštenje", "Hala je uspešno obrisana", QtWidgets.QMessageBox.Ok)
        self.halls_table.setSortingEnabled(True)    
        

    def _hall_type(self, type):
        """
        Metoda koja vraća tačan tip hale u tabelu.

        :returns: str -- tip hale u celom nazivu.
        """
        if type == 1:
            return "sobna temperatura (19°C do 25°C)" 
        elif type == 2:
            return "rashladna hala (1°C do 18°C)"
        else:
            return "hala za zamrzavanje (-10°C do 0°C)"

    def get_hall(self, hall):
        """
        Metoda koja dobavlja podatke iz tabele.

        :returns: Hall -- inicializuje halu.
        """ 
        return Hall(hall[0].text(), int(hall[1].text()), int(hall[2].text()), hall[3].text())
        



