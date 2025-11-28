#esthetisme_avion_layout.py
from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QListWidget, QLabel
from PySide6.QtCore import Qt

def style_layout_avions(group_avions: QGroupBox, liste_avions: QListWidget, max_height=400):
    group_avions.setMaximumHeight(max_height)
    group_avions.setTitle("")  # Supprimer le titre intégré

    # Nouveau bandeau titre
    label_titre = QLabel("Avion")
    label_titre.setAlignment(Qt.AlignCenter)
    label_titre.setStyleSheet("""
        QLabel {
            background-color: #FFB6C1;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            padding: 6px;
        }
    """)

    # Style du groupbox
    group_avions.setStyleSheet("""
        QGroupBox {
            background-color: #FFF8DC;
            border: 2px solid #FFB6C1;
            border-radius: 15px;
            margin-top: 0px;
        }
    """)

    # Style de la liste
    liste_avions.setStyleSheet("""
        QListWidget {
            background-color: #FFFAF0;
            border: none;
            border-radius: 10px;
            padding: 5px;
        }
        QListWidget::item {
            padding: 8px;
            margin: 2px;
            border-radius: 10px;
            color: black;  /* texte toujours noir */
        }
        QListWidget::item:selected {
            background-color: #FFB6C1;
            color: black;
        }
        QListWidget::item:hover {
            background-color: #FFD1DC;
        }
    """)

    # Layout
    layout = group_avions.layout() or QVBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(5)

    layout.insertWidget(0, label_titre)  # titre en haut
    if not group_avions.layout():
        layout.addWidget(liste_avions)
        group_avions.setLayout(layout)
