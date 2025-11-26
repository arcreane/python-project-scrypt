from PySide6.QtWidgets import QVBoxLayout, QGroupBox, QLabel, QPushButton, QSizePolicy, QSpacerItem
from PySide6.QtCore import Qt

def style_layout_instructions(group_instructions: QGroupBox, max_height=600):
    """
    Applique un style mignon (Animal Crossing) au layout des instructions
    et limite sa hauteur maximale.
    """
    group_instructions.setMaximumHeight(max_height)
    group_instructions.setTitle("")  # Supprimer le titre intégré

    # Nouveau bandeau titre
    label_titre = QLabel("Instructions")
    label_titre.setAlignment(Qt.AlignCenter)
    label_titre.setStyleSheet("""
        QLabel {
            background-color: #C5A6F0;  /* violet clair */
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            padding: 6px;
        }
    """)

    # Style du groupbox et des boutons
    group_instructions.setStyleSheet("""
        QGroupBox {
            background-color: #F5E6FF;  /* violet très clair */
            border: 2px solid #C5A6F0;
            border-radius: 15px;
            margin-top: 0px;
        }
        QPushButton {
            background-color: #DCC3F0;  /* violet clair pour les boutons */
            color: black;
            border-radius: 10px;
            padding: 8px 16px;
            font-size: 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #FFB6C1;  /* rose pastel au survol */
            color: black;
        }
        QPushButton:pressed {
            background-color: #FF69B4;  /* rose un peu plus foncé quand appuyé */
            color: black;
        }
    """)

    # Layout
    layout = group_instructions.layout() or QVBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(5)

    # On insère le bandeau titre en haut
    layout.insertWidget(0, label_titre)

    # Ajouter un spacer pour que le dernier bouton ne soit pas collé au bas
    spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout.addItem(spacer)

    if not group_instructions.layout():
        group_instructions.setLayout(layout)
