import sys
sys.path.append('/home/cyberp/Documents/PyCharm/Projects/pythonProjects/my_classes')
import vtxconn
from fuzzywuzzy import fuzz, process
import json
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFrame, QTextEdit, QMenu, QMessageBox, QToolBar, QAction, QWidget, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys

from PyQt5.QtGui import QPalette, QColor

class SrbijaMestaGUI(QMainWindow):
	def __init__(self, parent=None):
		super(SrbijaMestaGUI, self).__init__()

		self.conn = None
		self.cursor = None
		self.data_index = 0
		self.all_data = []

		centralni_widget = QWidget()
		self.setCentralWidget(centralni_widget)

		frame = QVBoxLayout()

		toolbar = QToolBar('Moj alatni bar')
		toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)
		toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.addToolBar(Qt.TopToolBarArea, toolbar)

		# Kreiranje padajućeg menija za Settings
		settingsMenu = QMenu("Settings", self)
		darkAction = QAction("Dark Mode", self)
		lightAction = QAction("Light Mode", self)

		darkAction.triggered.connect(lambda: self.switch_theme("Dark"))
		lightAction.triggered.connect(lambda: self.switch_theme("Light"))

		settingsMenu.addAction(darkAction)
		settingsMenu.addAction(lightAction)

		settingsMenu.setToolTip("")

		settingsButton = QAction("Settings", self)
		settingsButton.setMenu(settingsMenu)

		# Dodavanje Settings dugmeta na toolbar
		toolbar.addAction(settingsButton)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		toolbar.addWidget(spacer)

		helpMenu = QMenu("Help", self)
		aboutAction = QAction("About", self)
		helpMenu.addAction(aboutAction)
		aboutAction.triggered.connect(self.showAboutDialog)

		helpButton = QAction("Help", self)
		helpButton.setMenu(helpMenu)
		toolbar.addAction(helpButton)

		ispravka_layout = QGridLayout()

		self.ispravkaLabel = QLabel("Ispravka za:")
		ispravka_layout.addWidget(self.ispravkaLabel, 0, 0, 1, 3)

		self.orgAdresaEdit = QLineEdit()
		self.orgMestoEdit = QLineEdit()
		self.orgTelefonEdit = QLineEdit()
		ispravka_layout.addWidget(self.orgAdresaEdit, 1, 0)
		ispravka_layout.addWidget(self.orgMestoEdit, 1, 1)
		ispravka_layout.addWidget(self.orgTelefonEdit, 1, 2)

		# Postavljanje procentualne širine kolona
		ispravka_layout.setColumnStretch(0, 45)
		ispravka_layout.setColumnStretch(1, 35)
		ispravka_layout.setColumnStretch(2, 20)

		frame.addLayout(ispravka_layout)

		ponudjeno_layout = QGridLayout()

		ponudjenaLabel = QLabel("Ponuđena adresa:")
		ponudjeno_layout.addWidget(ponudjenaLabel, 2, 0, 1, 3)

		self.ponudjenoOpstinaEdit = QLineEdit()
		self.ponudjenoUlicaEdit = QLineEdit()
		self.ponudjenoBrojEdit = QLineEdit()
		self.ponudjenoMestoEdit = QLineEdit()
		self.ponudjenoTelefonEdit = QLineEdit()
		ponudjeno_layout.addWidget(self.ponudjenoOpstinaEdit, 3, 0)
		ponudjeno_layout.addWidget(self.ponudjenoUlicaEdit, 4, 0)
		ponudjeno_layout.addWidget(self.ponudjenoBrojEdit, 4, 1)
		ponudjeno_layout.addWidget(self.ponudjenoMestoEdit, 4, 2)
		ponudjeno_layout.addWidget(self.ponudjenoTelefonEdit, 4, 3)

		# Postavljanje procentualne širine kolona
		ponudjeno_layout.setColumnStretch(0, 36)
		ponudjeno_layout.setColumnStretch(1, 8)
		ponudjeno_layout.setColumnStretch(2, 35)
		ponudjeno_layout.setColumnStretch(3, 20)

		frame.addLayout(ponudjeno_layout)

		napomenaAdresnicaLabel = QLabel("Napomena za dostavu:")
		self.napomenaAdresnicaEdit = QLineEdit()
		self.napomenaAdresnicaEdit.setPlaceholderText('Npr. naziv firme ili lokala...')
		frame.addWidget(napomenaAdresnicaLabel)
		frame.addWidget(self.napomenaAdresnicaEdit)

		self.prihvatiDugme = QPushButton("Sačuvaj")
		self.preskociDugme = QPushButton("Preskoči")

		grupadva_layout = QGridLayout()

		# Dodavanje dugmadi
		grupadva_layout.addWidget(self.prihvatiDugme, 0, 1)
		grupadva_layout.addWidget(self.preskociDugme, 0, 0)

		# Dodavanje labela
		self.internaNapomenaLabel = QLabel("Interna Napomena:")
		self.bexNapomenaLabel = QLabel("Bex Napomena:")
		grupadva_layout.addWidget(self.internaNapomenaLabel, 1, 0)
		grupadva_layout.addWidget(self.bexNapomenaLabel, 1, 1)

		# Dodavanje multiline polja
		self.internaNapomenaMultiline = QTextEdit()
		self.internaNapomenaMultiline.setFixedHeight(80)
		self.bexNapomenaMultiline = QTextEdit()
		self.bexNapomenaMultiline.setFixedHeight(80)
		grupadva_layout.addWidget(self.internaNapomenaMultiline, 2, 0)
		grupadva_layout.addWidget(self.bexNapomenaMultiline, 2, 1)

		# Dodavanje layouta u glavni frame
		frame.addLayout(grupadva_layout)

		separator2 = QFrame()
		separator2.setFrameShape(QFrame.HLine)
		separator2.setFrameShadow(QFrame.Sunken)
		frame.addWidget(separator2)

		status_layout = QGridLayout()

		statusLabel = QLabel("Izmena za 4 / 10 adresnice.")
		status_layout.addWidget(statusLabel, 0, 0)
		self.connectLabel = QLabel("by cyberp.")
		status_layout.addWidget(self.connectLabel, 0, 1)

		font = QFont()
		font.setPointSize(10)
		statusLabel.setFont(font)
		statusLabel.setStyleSheet("color: gray;")

		self.connectLabel.setFont(font)
		self.connectLabel.setStyleSheet("color: gray;")
		self.connectLabel.setAlignment(Qt.AlignRight)

		frame.addLayout(status_layout)

		centralni_widget.setLayout(frame)

		self.setWindowTitle('SrbijaMesta.py 1.0.0')

		self.resize(720, 380)

		self.switch_theme("Dark")

		self.show()
		self.prihvatiDugme.setFocus()
		self.prihvatiDugme.clicked.connect(self.next_data)

	def load_data_from_json(self, data_json):
		self.all_data = data_json
		self.update_gui_with_data(self.all_data[self.data_index])

	def next_data(self):
		self.data_index += 1
		if self.data_index < len(self.all_data):
			self.update_gui_with_data(self.all_data[self.data_index])
		else:
			self.close()  # ili neka druga radnja kada su sve ispravke pregledane

	def update_gui_with_data(self, data):
		order = data.get('order', '')
		ime = data.get('ime', '')
		adresa = data.get('adresa', '')
		zip_code = data.get('zip', '')
		mesto = data.get('mesto', '')
		telefon = data.get('telefon', '')
		napomena = data.get('napomena', '')
		cena = data.get('cena', '')
		datum = data.get('datum', '')
		shop = data.get('shop', '')

		self.ispravkaLabel.setText(f'Ispravka za: <span style="color: grey;">{order} | {ime} | {cena} dinara | {datum} | {shop}.</span>')
		self.orgAdresaEdit.setText(adresa)
		if zip_code:
			self.orgMestoEdit.setText(mesto + " " + zip_code)
		else:
			self.orgMestoEdit.setText(mesto)
		self.orgTelefonEdit.setText(telefon)
		self.internaNapomenaMultiline.setText(napomena)

	def printStatus(self, status):
		self.connectLabel.setText(status)

	def main(self, parametri):

		if parametri:
			order = parametri.get('order', None)
			ime = parametri.get('ime', None)
			adresa = parametri.get('adresa', None)
			zip = parametri.get('zip', None)
			mesto = parametri.get('mesto', None)
			telefon = parametri.get('telefon', None)
			napomena = parametri.get('napomena', None)
			cena = parametri.get('cena', None)
			datum = parametri.get('datum', None)
			shop = parametri.get('shop', None)

			self.ispravkaLabel.setText(f'Ispravka za: <span style="color: grey;">{order} | {ime} | {cena} dinara | {datum} | {shop}.</span>')
			self.orgAdresaEdit.setText(adresa)
			if zip:
				self.orgMestoEdit.setText(mesto + " " + zip)
			else:
				self.orgMestoEdit.setText(mesto)
			self.orgTelefonEdit.setText(telefon)

			if any(char in adresa.lower() for char in 'абвгдђежзијклљмнњопрстћуфхцчџш'):
				adresa = self.cirilica_u_latinicu(adresa)
			if any(char in mesto.lower() for char in 'абвгдђежзијклљмнњопрстћуфхцчџш'):
				mesto = self.cirilica_u_latinicu(mesto)
			telefon = self.normalize_phone(telefon)
			if not telefon.isdigit() or not telefon.startswith('06'):
				self.ponudjenoTelefonEdit.setStyleSheet("background-color: #7b1616;")  # Crvena boja
			self.ponudjenoTelefonEdit.setText(telefon)

			ulica, broj = self.extract_house_number(adresa)

			self.ponudjenoBrojEdit.setText(broj)

			self.napomenaMultiline.setText("Interna : " + napomena + "\n")

			self.conn = vtxconn.DatabaseConnector()
			ulica, mesto_zip = self.get_from_srbija_mesta(ulica, mesto + " " + zip)
			self.ponudjenoMestoEdit.setText(mesto_zip)
			self.ponudjenoUlicaEdit.setText(ulica)

	def get_from_srbija_mesta(self, ulica, mesto):
		mesta = self.conn.execute_query("SELECT DISTINCT LOWER(MestoPlusZip) FROM UlicePlusMesta")
		mesta = [x[0] for x in mesta]
		mesta = [str(m) for m in mesta if m is not None]
    
		# Pronalazenje najboljeg poklapanja
		best_match_mesto, score = process.extractOne(mesto, mesta)

		print(best_match_mesto + " " + str(score))


		if score >= 90:
			mesto = best_match_mesto
			kveri = "SELECT IDulice, LOWER(NazivUlice), LOWER(MestoPlusZip) FROM UlicePlusMesta WHERE LOWER(MestoPlusZip) = '" + mesto + "'"
		else:
			mesto = re.sub(r' \d{5}$', '', mesto)
			kveri = "SELECT IDulice, LOWER(NazivUlice), LOWER(MestoPlusZip) FROM UlicePlusMesta WHERE LOWER(MestoPlusZip) LIKE '%" + mesto + "%'"
		ulice = self.conn.execute_query(kveri)
		if ulice:
			ulica_mesto_map = {}
			for x in ulice:
				if x[1] is not None and x[2] is not None:
					ulica_mesto_map[str(x[1])] = str(x[2])

			# Pravimo listu samo sa nazivima ulica za poređenje
			samo_ulice = list(ulica_mesto_map.keys())

			# Nađemo najbolje podudaranje
			best_match_ulica, score = process.extractOne(ulica, samo_ulice)

			# Koristimo najbolje podudaranje da pronađemo pripadajuće mesto
			best_match_mesto = ulica_mesto_map.get(best_match_ulica, "")

			return best_match_ulica, best_match_mesto
		else:
			return "", mesto

	def extract_house_number(self, adresa):
    	# Uklanjanje nepotrebnih belih prostora sa početka i kraja stringa
		adresa = adresa.lower()
		adresa = adresa.strip()

		broj = ""
		ulica = ""
		
		# Uklanjanje tačke sa kraja stringa, ako postoji
		if adresa.endswith('.'):
			adresa = adresa[:-1]
			
		# Provera za "bb" ili "bez broja" na kraju adrese
		if adresa.endswith('bb'):
			ulica = adresa[:-2].strip()
			broj = '0'
			return ulica, broj
		elif adresa.endswith('bez broja'):
			ulica = adresa[:-9].strip()
			broj = '0'
			return ulica, broj

		if adresa.startswith('selo'):
			adresa = adresa.replace('selo', '', 1).strip()

		adresa = adresa.replace(' br.', ' ').replace(' br ', ' ').strip()
		adresa = adresa.replace('.', ' ').replace(',', ' ').strip()
		adresa = adresa.replace(" stan ", " / ")
		adresa = adresa.replace(" sprat ", " / ")

		# Pronađi poslednji niz od dva slova ili više
		match = re.search('[a-zćčšđž]{2,}', adresa[::-1])
		if match:
			pozicija = len(adresa) - match.start()
			broj = adresa[pozicija:].strip().replace(" ", "")
			ulica = adresa[:pozicija].strip()
			return ulica, broj
		else:
			return adresa, "0"

	def cirilica_u_latinicu(self, text):
		text = text.replace("љ", "lj").replace("Љ", "Lj")
		text = text.replace("њ", "nj").replace("Њ", "Nj")
		text = text.replace("џ", "dž").replace("Џ", "Dž")
		
		cirilicne_slova = 'абвгдђежзијклмнопрстћуфхцчш'
		latinicne_slova = 'abvgdđežzijklmnoprstćufhččš'
		
		prevod = str.maketrans(cirilicne_slova + cirilicne_slova.upper(), latinicne_slova + latinicne_slova.upper())
		prevedeni_tekst = text.translate(prevod)
		
		return prevedeni_tekst

	def normalize_phone(self, broj_telefona):
		broj_telefona = broj_telefona.replace(' ', '').replace('/', '').replace('-', '')			

		if broj_telefona.startswith('+381'):
			broj_telefona = '0' + broj_telefona[4:]

		return broj_telefona
	
	def __del__(self):
		if self.cursor:
			self.cursor.close()
		if self.conn:
			self.conn.close()

	def showAboutDialog(self):
		QMessageBox.information(self, "About", "Created by CyberP with help of GPT-4.")

	def switch_theme(self, mode):
		palette = QPalette()
		
		if mode == "Dark":
			#app.setStyleSheet("QToolTip { background-color: #333; color: #fff; border: 1px solid #555; }")
			palette.setColor(QPalette.Window, QColor(53, 53, 53))
			palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
			palette.setColor(QPalette.Base, QColor(25, 25, 25))
			palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
			palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
			palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
			palette.setColor(QPalette.Text, QColor(255, 255, 255))
			palette.setColor(QPalette.Button, QColor(53, 53, 53))
			palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
			palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
			palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
			palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
		else:
			palette.setColor(QPalette.Window, QColor(255, 255, 255))
			palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
			palette.setColor(QPalette.Base, QColor(255, 255, 255))
			palette.setColor(QPalette.AlternateBase, QColor(242, 242, 242))
			palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
			palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
			palette.setColor(QPalette.Text, QColor(0, 0, 0))
			palette.setColor(QPalette.Button, QColor(255, 255, 255))
			palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
			palette.setColor(QPalette.BrightText, QColor(0, 0, 0))
			palette.setColor(QPalette.Link, QColor(0, 120, 215))
			palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
			palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
		app.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    prozor = SrbijaMestaGUI()

    if len(sys.argv) > 1:
        dodatni_string = sys.argv[1]
        parametri = json.loads(dodatni_string)
        prozor.load_data_from_json(parametri)

    sys.exit(app.exec_())
