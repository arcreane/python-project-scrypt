# esthetisme_stats_layout.py
from PySide6.QtGui import QFont

def style_layout_stats(label_stats, score_label, niveau_label, group_avions):
    """
    Applique un style Animal Crossing au panneau de stats.
    Aucun changement de logique : uniquement visuel.
    """

    # Couleurs Animal Crossing
    bg_panel = "#FFF9E8"      # beige crème
    border_color = "#C8B28A"  # marron clair
    title_color = "#8B6F47"   # bois
    text_color = "#4F3B24"    # brun doux
    pastel_blue = "#A3D1FF"
    pastel_green = "#A7D9A9"

    # Label "Stats"
    font_stats = QFont(label_stats.font())
    font_stats.setPointSize(26)
    font_stats.setBold(True)
    label_stats.setFont(font_stats)
    label_stats.setStyleSheet(f"""
        QLabel {{
            background-color: {bg_panel};
            color: {title_color};
            padding: 10px 16px;
            border: 3px solid {border_color};
            border-radius: 15px;
            box-shadow: 2px 2px 8px rgba(0,0,0,40);
        }}
    """)

    # Label "Score"
    font_score = QFont(score_label.font())
    font_score.setPointSize(22)
    font_score.setBold(True)
    score_label.setFont(font_score)
    score_label.setStyleSheet(f"""
        QLabel {{
            background-color: {pastel_green};
            color: {text_color};
            padding: 12px;
            border-radius: 12px;
            border: 2px solid {border_color};
        }}
    """)

    # Label "Niveau"
    font_niveau = QFont(niveau_label.font())
    font_niveau.setPointSize(22)
    font_niveau.setBold(True)
    niveau_label.setFont(font_niveau)
    niveau_label.setStyleSheet(f"""
        QLabel {{
            background-color: {pastel_blue};
            color: {text_color};
            padding: 12px;
            border-radius: 12px;
            border: 2px solid {border_color};
        }}
    """)

    # Groupe avions
    group_avions.setStyleSheet(f"""
        QGroupBox {{
            background-color: {bg_panel};
            border: 3px solid {border_color};
            border-radius: 18px;
            margin-top: 14px;
            padding-top: 18px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            top: 6px;
            left: 12px;
            padding: 0 8px;
            color: {title_color};
            font-size: 20px;
            font-weight: bold;
        }}

        QListWidget {{
            background-color: #FAF3DD;
            border-radius: 10px;
            border: 2px solid {border_color};
        }}

        QListWidget::item:selected {{
            background-color: {pastel_blue};
            color: {text_color};
            border-radius: 6px;
        }}

        QListWidget::item:hover {{
            background-color: {pastel_green};
            color: {text_color};
        }}
    """)
