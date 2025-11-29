# InfoWindow.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


# Classe : Fenêtre d'informations
class InfoWindow(QDialog):
    """
    Fenêtre d'informations affichant le projet et les auteurs.
    Fenêtre sans bordure avec image de fond et bouton 'Fermer'.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(600, 400)

        # Retirer la barre de titre et boutons
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Image de fond
        self.background_label = QLabel(self)
        self._set_background("Images/Fond_infos_accueil.png")
        self.background_label.lower()  # Mettre en arrière-plan

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Barre du haut avec bouton Fermer
        self._setup_top_bar(main_layout)

        # Contenu texte
        self._setup_content(main_layout)

        # Étirement final pour centrer le contenu verticalement
        main_layout.addStretch()

    # Méthodes internes
    def _set_background(self, image_path):
        """
        Configure l'image de fond pour le QDialog.
        """
        pixmap = QPixmap(image_path).scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(self.rect())

    def _setup_top_bar(self, layout):
        """
        Configure la barre supérieure contenant le bouton Fermer.
        """
        top_bar = QHBoxLayout()
        top_bar.addStretch()  # pousse le bouton à droite

        self.close_button = QPushButton("Fermer")
        self.close_button.setFixedSize(100, 40)
        self.close_button.clicked.connect(self.accept)
        top_bar.addWidget(self.close_button)

        layout.addLayout(top_bar)

    def _setup_content(self, layout):
        """
        Configure le contenu texte principal du QDialog.
        """
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        self.label_text = QLabel(
            "Projet réalisé par le\n"
            "groupe Scrypt :\n\n"
            "🌸 Mélina LEJEUNE\n"
            "🌸 Lise TUONG\n"
            "🌸 Chloé VINOTTI\n\n"
            "🍃 SkyLink Simulation 🍃\n"
            "            2PH2"
        )
        self.label_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label_text.setStyleSheet("""
            background-color: transparent;
            color: black;
            font-size: 22px;
            font-family: Comic Sans MS;
            font-weight: bold;
        """)

        content_layout.addWidget(self.label_text)
        layout.addLayout(content_layout)
