from PySide6.QtWidgets import QApplication, QWidget
# Only needed for access to command line arguments
import sys
# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = QWidget()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()
# Your application won't reach here until you exit and the event
# loop has stopped.







from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")

        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(button)


app = QApplication(sys.argv)

window = MainWindow()
window.show()





from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Slot

# Fonction appelée lors du clic sur le bouton
@Slot()
def on_button_clicked():
    print("Bouton cliqué !")

# Création de l'application
app = QApplication([])

# Création de la fenêtre principale
window = QWidget()
window.setWindowTitle("Exemple de bouton avec PySide6")

# Création du bouton
button = QPushButton("Cliquez-moi")
button.clicked.connect(on_button_clicked)  # Connexion du signal au slot

# Mise en page
layout = QVBoxLayout()
layout.addWidget(button)
window.setLayout(layout)

# Affichage de la fenêtre
window.show()

# Lancement de l'application
app.exec()




from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Créer le QStackedWidget pour gérer les pages
        self.stacked_widget = QStackedWidget()

        # Créer les pages
        self.page1 = QWidget()
        self.page2 = QWidget()

        # Configurer les pages
        self.setup_page1()
        self.setup_page2()

        # Ajouter les pages au QStackedWidget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)

        # Définir le QStackedWidget comme widget central
        self.setCentralWidget(self.stacked_widget)

    def setup_page1(self):
        layout = QVBoxLayout()
        button = QPushButton("Aller à la page 2")
        button.clicked.connect(self.go_to_page2)  # Connecter le bouton à la méthode
        layout.addWidget(button)
        self.page1.setLayout(layout)

    def setup_page2(self):
        layout = QVBoxLayout()
        button = QPushButton("Retour à la page 1")
        button.clicked.connect(self.go_to_page1)  # Connecter le bouton à la méthode
        layout.addWidget(button)
        self.page2.setLayout(layout)

    def go_to_page2(self):
        self.stacked_widget.setCurrentWidget(self.page2)  # Changer vers la page 2

    def go_to_page1(self):
        self.stacked_widget.setCurrentWidget(self.page1)  # Changer vers la page 1


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.setWindowTitle("Changer de page avec PySide6")
    window.resize(400, 300)
    window.show()

    app.exec()
