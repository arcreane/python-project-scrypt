# clignotement_legende.py
from PySide6.QtCore import QTimer


# Clignotement des avions en urgence (fuel < 20%)
def clignoter_avions_urgence(game_widget, duree=4000, intervalle=200):
    """
    Clignotement des avions en Urgence (fuel < 10%)

    Args:
        game_widget: Instance de GameWidget contenant la liste des avions.
        duree: Durée totale du clignotement en millisecondes.
        intervalle: Intervalle entre chaque bascule du clignotement (ms).
    """
    temps_ecoule = 0
    timer = QTimer()

    def toggle_blink():
        nonlocal temps_ecoule
        temps_ecoule += intervalle

        # Bascule du clignotement pour chaque avion en urgence
        for plane in game_widget.planes:
            if plane.avion.fuel < 10:
                plane.blink_urgence = not getattr(plane, 'blink_urgence', False)

        game_widget.update()

        # Arrêt du timer une fois la durée écoulée
        if temps_ecoule >= duree:
            for plane in game_widget.planes:
                plane.blink_urgence = False
            timer.stop()

    timer.timeout.connect(toggle_blink)
    timer.start(intervalle)


# Clignotement des avions en attente (fuel >= 10%)
def clignoter_avions_attente(game_widget, duree=3000, intervalle=200):
    """
    Clignotement des avions en Attente (fuel >= 10% et non sélectionnés)

    Args:
        game_widget: Instance de GameWidget contenant la liste des avions.
        duree: Durée totale du clignotement en millisecondes.
        intervalle: Intervalle entre chaque bascule du clignotement (ms).
    """
    temps_ecoule = 0
    timer = QTimer()

    def toggle_blink():
        nonlocal temps_ecoule
        temps_ecoule += intervalle

        # Bascule du clignotement pour chaque avion en attente
        for plane in game_widget.planes:
            if plane.avion.fuel >= 10 and plane is not game_widget.selected_plane:
                plane.blink_attente = not getattr(plane, 'blink_attente', False)

        game_widget.update()

        # Arrêt du timer une fois la durée écoulée
        if temps_ecoule >= duree:
            for plane in game_widget.planes:
                plane.blink_attente = False
            timer.stop()

    timer.timeout.connect(toggle_blink)
    timer.start(intervalle)
