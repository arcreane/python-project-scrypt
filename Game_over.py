# Game_over.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class GameOverWidget(QWidget):
    def __init__(self, parent=None, restart_callback=None, quit_callback=None):
        super().__init__(parent)
        self.restart_callback = restart_callback
        self.quit_callback = quit_callback
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Layout principal centré
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        layout.setSpacing(20)

        self.label = QLabel("GAME OVER")
        font = self.label.font()
        font.setPointSize(60)   # très grand
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: red;")
        layout.addWidget(self.label)

        self.btn_restart = QPushButton("Recommencer")
        self.btn_quit = QPushButton("Quitter")
        for b in [self.btn_restart, self.btn_quit]:
            b.setFixedSize(240, 70)

        restart_style = """
        QPushButton {
            background-color: #5BC074;      /* couleur de base conservée */
            border: 3px solid #4caf50;      /* contour vert foncé */
            border-radius: 24px;
            padding: 10px 20px;
            font-size: 20px;
            font-weight: bold;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #7cd88b; }
        QPushButton:pressed {
            background-color: #44994f; }
        """

        quit_style = """
            QPushButton {
                background-color: #E85757;      /* rose pastel */
                border: 3px solid #e06684;      /* contour rose foncé */
                border-radius: 24px;
                padding: 10px 20px;
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;                 
            }
            QPushButton:hover {
                background-color: #ff9999;
            }
            QPushButton:pressed {
                background-color: #ffc6d5;
            }
        """
        self.btn_restart.setStyleSheet(restart_style)
        self.btn_quit.setStyleSheet(quit_style)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(30)
        btn_row.setAlignment(Qt.AlignHCenter)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_restart)
        btn_row.addWidget(self.btn_quit)
        btn_row.addStretch()

        layout.addLayout(btn_row)

        # Création du QLabel
        self.info_label = QLabel("Ton score a atteint 0 — la partie est terminée.")
        info_font = self.info_label.font()
        info_font.setPointSize(14)
        self.info_label.setFont(info_font)

        self.info_label.setStyleSheet("""
            color: #black;
            background-color: rgba(80, 150, 255, 140);
            padding: 5px 15px;            
            border-radius: 8px;
        """)

        self.info_label.setMaximumWidth(self.info_label.sizeHint().width())

        info_layout = QHBoxLayout()
        info_layout.addStretch()
        info_layout.addWidget(self.info_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)

        self.btn_restart.clicked.connect(self.on_restart)
        self.btn_quit.clicked.connect(self.on_quit)

        self.setLayout(layout)

    def on_restart(self):
        if self.restart_callback:
            self.restart_callback()
        self.close()

    def on_quit(self):
        if self.quit_callback:
            self.quit_callback()
        self.close()
