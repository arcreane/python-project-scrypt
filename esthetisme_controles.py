# -*- coding: utf-8 -*-
"""
Esthetisme_Control.py
Style "Animal Crossing" pour le Layout des contrôles (Groupe "Contrôles", boutons, progress bars, labels).
Conserver les connexions/signaux : ce module ne modifie QUE l'apparence.
"""
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtCore import Qt

def style_layout_control(group_controles: QWidget,
                         all_buttons: list,
                         btn_atterrir=None,
                         btn_urgence=None,
                         btn_attente=None,
                         progress_bars: list | None = None,
                         label_nom_avion=None,
                         compass=None):

    # Palette générale
    pastel_purple = "#C8A2FF"   # boutons génériques
    pastel_blue = "#CDEEFF"      # hover bouton
    pastel_pink = "#FFD6E0"      # pressed bouton
    cream = "#FFF8EE"
    wood = "#8B5E3C"
    soft_border = "rgba(139,94,60,0.12)"

    # Couleurs spécifiques
    urgence_color = "#FF6B6B"    # rouge/orangé
    atterrir_color = "#6BCB77"   # vert pastel foncé
    attente_color = "#4D96FF"    # bleu pastel

    # --- Style du QGroupBox (groupe Contrôles) ---
    group_style = f"""
    QGroupBox {{
        background: qlineargradient(x1:0,y1:0, x2:1,y2:1,
                    stop:0 {cream}, stop:1 {pastel_purple});
        border: 2px solid rgba(139,94,60,0.08);
        border-radius: 14px;
        margin-top: 8px;
        padding: 10px;
        font-weight: bold;
        color: {wood};
        font-size: 16px;
    }}
    QGroupBox::title {{
        subcontrol-origin: none;
        height: 0px;
    }}
    """
    try:
        group_controles.setStyleSheet(group_style)
    except Exception:
        pass

    # --- Police globale ---
    default_font = QFont()
    default_font.setPointSize(14)
    default_font.setBold(True)

    # --- Style générique des boutons ---
    button_base = f"""
    QPushButton {{
        background-color: {pastel_purple};
        border: 2px solid {soft_border};
        border-radius: 12px;
        padding: 10px 14px;
        min-height: 48px;
        font-size: 15px;
        font-weight: bold;
        color: {wood};
    }}
    QPushButton:hover {{
        background-color: {pastel_blue};
        transform: translateY(-1px);
    }}
    QPushButton:pressed {{
        background-color: {pastel_pink};
        padding-top: 11px;
        padding-bottom: 9px;
    }}
    QPushButton:disabled {{
        background: rgba(200,200,200,0.35);
        color: #7a6b5a;
        border-style: dashed;
    }}
    """
    for b in all_buttons:
        try:
            b.setStyleSheet(button_base)
            b.setFont(default_font)
        except Exception:
            pass

    # --- Bouton urgence ---
    if btn_urgence:
        urgence_style = f"""
        QPushButton {{
            background-color: {urgence_color};
            border: 2px solid rgba(255,100,80,0.18);
            color: white;
        }}
        QPushButton:hover {{ background-color: #FF8C7E; }}
        QPushButton:pressed {{ background-color: #FF4C4C; }}
        """
        try:
            btn_urgence.setStyleSheet(urgence_style)
        except Exception:
            pass

    # --- Bouton attente ---
    if btn_attente:
        attente_style = f"""
        QPushButton {{
            background-color: {attente_color};
            border: 2px solid rgba(80,150,255,0.18);
            color: white;
        }}
        QPushButton:hover {{ background-color: #6EA0FF; }}
        QPushButton:pressed {{ background-color: #3B7BFF; }}
        """
        try:
            btn_attente.setStyleSheet(attente_style)
        except Exception:
            pass

    # --- Bouton atterrir ---
    if btn_atterrir:
        atterrir_style = f"""
        QPushButton {{
            background-color: {atterrir_color};
            border: 2px solid rgba(100,180,120,0.18);
            color: white;
        }}
        QPushButton:hover {{ background-color: #81D99B; }}
        QPushButton:pressed {{ background-color: #4FB86A; }}
        """
        try:
            btn_atterrir.setStyleSheet(atterrir_style)
        except Exception:
            pass

    # --- Progress bars ---
    if progress_bars:
        for pb in progress_bars:
            try:
                prog_style = f"""
                QProgressBar {{
                    border: 2px solid rgba(139,94,60,0.06);
                    border-radius: 10px;
                    background: {cream};
                    text-align: center;
                    min-height: 28px;
                    font-weight: bold;
                    color: {wood};
                }}
                QProgressBar::chunk {{
                    border-radius: 8px;
                    margin: 2px;
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                        stop:0 #D4B3FF, stop:0.6 #FFEE88, stop:1 #FFB88A);
                }}
                """
                pb.setStyleSheet(prog_style)
                try:
                    f = pb.font()
                    f.setPointSize(12)
                    f.setBold(True)
                    pb.setFont(f)
                except Exception:
                    pass
            except Exception:
                pass

    # --- Label nom avion ---
    if label_nom_avion:
        try:
            # Largeur minimale pour éviter que le layout bouge
            label_nom_avion.setMinimumWidth(label_nom_avion.sizeHint().width())
            # S'adapte horizontalement à l'espace disponible
            label_nom_avion.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            # Texte tronqué si trop long
            label_nom_avion.setWordWrap(False)
            label_nom_avion.setTextInteractionFlags(Qt.TextSelectableByMouse)
            label_nom_avion.setElideMode(Qt.ElideRight)
            # Style
            label_nom_avion.setStyleSheet(f"""
                QLabel {{
                    color: {wood};
                    background: transparent;
                }}
            """)
            f = label_nom_avion.font()
            f.setPointSize(18)
            f.setBold(True)
            label_nom_avion.setFont(f)
        except Exception:
            pass

    # --- Compass ---
    if compass:
        try:
            compass.setStyleSheet(f"""
                QWidget {{
                    border: 2px solid rgba(139,94,60,0.06);
                    border-radius: 10px;
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 {pastel_blue}, stop:1 {cream});
                }}
            """)
        except Exception:
            pass

    return True
