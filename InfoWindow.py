from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class InfoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(600, 400)

        # --- Retirer la barre de titre et les boutons ---
        self.setWindowFlags(Qt.FramelessWindowHint)

        # --- Image en fond via QLabel ---
        self.background_label = QLabel(self)
        self.background_label.setPixmap(
            QPixmap("Images/fond_infos_accueil.png").scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
        )
        self.background_label.setGeometry(self.rect())
        self.background_label.lower()  # Met en arrière-plan

        # --- Layout principal ---
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # --- Barre du haut avec bouton Fermer ---
        top_bar = QHBoxLayout()
        top_bar.addStretch()  # pousse le bouton à droite
        self.close_button = QPushButton("Fermer")
        self.close_button.setFixedSize(100, 40)
        self.close_button.clicked.connect(self.accept)
        top_bar.addWidget(self.close_button)
        main_layout.addLayout(top_bar)

        # --- Layout horizontal texte ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Texte à gauche avec saut de ligne avant "Projet réalisé par"
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

        main_layout.addLayout(content_layout)
        main_layout.addStretch()
