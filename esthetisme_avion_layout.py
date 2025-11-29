# esthetisme_avion_layout.py
from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QListWidget, QLabel
from PySide6.QtCore import Qt


def style_layout_avions(group_avions: QGroupBox, liste_avions: QListWidget, max_height=400):
    """
    Applique un style esthétique au groupbox et à la liste des avions.

    Args:
        group_avions (QGroupBox): Conteneur du groupe d'avions.
        liste_avions (QListWidget): Liste des avions.
        max_height (int, optional): Hauteur maximale du groupbox. Defaults to 400.
    """
    # Paramètres du groupbox
    group_avions.setMaximumHeight(max_height)
    group_avions.setTitle("")  # Supprime le titre intégré

    group_avions.setStyleSheet("""
        QGroupBox {
            background-color: #FFF8DC;
            border: 2px solid #FFB6C1;
            border-radius: 15px;
            margin-top: 0px;
        }
    """)

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
            color: black;
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

    # Insérer le titre en haut
    layout.insertWidget(0, label_titre)

    # Ajouter la liste des avions si elle n'est pas déjà dans le layout
    if not group_avions.layout():
        layout.addWidget(liste_avions)
        group_avions.setLayout(layout)
