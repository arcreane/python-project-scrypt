# Game_over.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class GameOverWidget(QWidget):
    """
    Widget affiché lors de la fin de partie.
    Permet de redémarrer ou quitter le jeu et affiche le score final.
    """

    def __init__(self, parent=None, restart_callback=None, quit_callback=None):
        super().__init__(parent)

        # Callbacks pour les actions
        self.restart_callback = restart_callback
        self.quit_callback = quit_callback

        # Fenêtre sans bordure et transparente
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Layout principal centré
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)

        # Sections du widget
        self._init_title()
        self._init_buttons()
        self._init_info_label()

    # Titre "GAME OVER"
    def _init_title(self):
        self.label = QLabel("GAME OVER")
        font = self.label.font()
        font.setPointSize(60)  # très grand
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: red;")
        self.main_layout.addWidget(self.label)

    # Boutons "Recommencer" et "Quitter"
    def _init_buttons(self):
        self.btn_restart = QPushButton("Recommencer")
        self.btn_quit = QPushButton("Quitter")

        # Ne pas prendre le focus clavier
        for b in [self.btn_restart, self.btn_quit]:
            b.setFocusPolicy(Qt.NoFocus)
            b.setFixedSize(240, 70)

        # Styles CSS
        self.btn_restart.setStyleSheet("""
            QPushButton {
                background-color: #5BC074;
                border: 3px solid #4caf50;
                border-radius: 24px;
                padding: 10px 20px;
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
            }
            QPushButton:hover { background-color: #7cd88b; }
            QPushButton:pressed { background-color: #44994f; }
        """)

        self.btn_quit.setStyleSheet("""
            QPushButton {
                background-color: #E85757;
                border: 3px solid #e06684;
                border-radius: 24px;
                padding: 10px 20px;
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;                 
            }
            QPushButton:hover { background-color: #ff9999; }
            QPushButton:pressed { background-color: #ffc6d5; }
        """)

        # Layout horizontal pour les boutons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(30)
        btn_row.setAlignment(Qt.AlignHCenter)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_restart)
        btn_row.addWidget(self.btn_quit)
        btn_row.addStretch()

        self.main_layout.addLayout(btn_row)

        # Connexion des actions
        self.btn_restart.clicked.connect(self.on_restart)
        self.btn_quit.clicked.connect(self.on_quit)

    # Label d'information sur le score
    def _init_info_label(self):
        self.info_label = QLabel("Ton score a atteint 0 — la partie est terminée.")
        font = self.info_label.font()
        font.setPointSize(14)
        self.info_label.setFont(font)

        self.info_label.setStyleSheet("""
            color: black;
            background-color: rgba(80, 150, 255, 140);
            padding: 5px 15px;            
            border-radius: 8px;
        """)

        self.info_label.setMaximumWidth(self.info_label.sizeHint().width())

        info_layout = QHBoxLayout()
        info_layout.addStretch()
        info_layout.addWidget(self.info_label)
        info_layout.addStretch()

        self.main_layout.addLayout(info_layout)

    # Callbacks des boutons
    def on_restart(self):
        """Relance la partie via le callback si défini."""
        if self.restart_callback:
            self.restart_callback()
        self.close()

    def on_quit(self):
        """Quitte le jeu via le callback si défini."""
        if self.quit_callback:
            self.quit_callback()
        self.close()
