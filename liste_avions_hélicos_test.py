# test liste_avions_helis.py pour code : a supprimer test redim.fenetre.jeu.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout

class ListeAvionsHelis(QWidget):
    def __init__(self, avions=[], helis=[]):
        super().__init__()

        # Scroll Avions
        scroll_avions = QScrollArea()
        scroll_avions.setWidgetResizable(True)
        widget_avions = QWidget()
        layout_avions = QVBoxLayout(widget_avions)
        scroll_avions.setWidget(widget_avions)

        layout_avions.addWidget(QLabel("Avions"))
        for avion in avions:
            layout_avions.addWidget(QLabel(f"{avion['nom']} - ALT:{avion['alt']} - VIT:{avion['vit']} - FUEL:{avion['fuel']}"))
        layout_avions.addStretch()

        # Scroll Hélicoptères
        scroll_helis = QScrollArea()
        scroll_helis.setWidgetResizable(True)
        widget_helis = QWidget()
        layout_helis = QVBoxLayout(widget_helis)
        scroll_helis.setWidget(widget_helis)

        layout_helis.addWidget(QLabel("Hélicoptères"))
        for heli in helis:
            layout_helis.addWidget(QLabel(f"{heli['nom']} - ALT:{heli['alt']} - VIT:{heli['vit']} - FUEL:{heli['fuel']}"))
        layout_helis.addStretch()

        # Layout horizontal
        layout_h = QHBoxLayout()
        layout_h.addWidget(scroll_avions,1)
        layout_h.addWidget(scroll_helis,1)

        self.setLayout(layout_h)
