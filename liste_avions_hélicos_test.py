# liste_avions_helis.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout
from PySide6.QtCore import Qt

class ListeAvionsHelis(QWidget):
    def __init__(self, avions=[], helis=[]):
        super().__init__()

        #Scroll Avions
        scroll_avions = QScrollArea()
        scroll_avions.setWidgetResizable(True)
        scroll_avions.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_avions.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        widget_avions = QWidget()
        layout_avions = QVBoxLayout(widget_avions)

        for avion in avions:
            label = QLabel(f"{avion['nom']} - ALT:{avion['alt']} - VIT:{avion['vit']} - FUEL:{avion['fuel']}")
            label.setWordWrap(True)
            layout_avions.addWidget(label)

        layout_avions.addStretch()
        scroll_avions.setWidget(widget_avions)

        #Titre fixe Avions
        label_titre_avion = QLabel("Avions")
        label_titre_avion.setAlignment(Qt.AlignCenter)
        label_titre_avion.setStyleSheet("font-weight: bold; font-size: 16px;")

        #Layout complet Avions
        layout_avion_complet = QVBoxLayout()
        layout_avion_complet.addWidget(label_titre_avion)
        layout_avion_complet.addWidget(scroll_avions)

        #Scroll Hélicoptères
        scroll_helis = QScrollArea()
        scroll_helis.setWidgetResizable(True)
        scroll_helis.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_helis.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        widget_helis = QWidget()
        layout_helis = QVBoxLayout(widget_helis)

        for heli in helis:
            label = QLabel(f"{heli['nom']} - ALT:{heli['alt']} - VIT:{heli['vit']} - FUEL:{heli['fuel']}")
            label.setWordWrap(True)
            layout_helis.addWidget(label)

        layout_helis.addStretch()
        scroll_helis.setWidget(widget_helis)

        #Titre fixe Hélicoptères
        label_titre_heli = QLabel("Hélicoptères")
        label_titre_heli.setAlignment(Qt.AlignCenter)
        label_titre_heli.setStyleSheet("font-weight: bold; font-size: 16px;")

        #Layout complet Hélicoptères
        layout_heli_complet = QVBoxLayout()
        layout_heli_complet.addWidget(label_titre_heli)
        layout_heli_complet.addWidget(scroll_helis)

        #Layout horizontal final
        layout_h = QHBoxLayout()
        layout_h.addLayout(layout_avion_complet)
        layout_h.addLayout(layout_heli_complet)

        self.setLayout(layout_h)
