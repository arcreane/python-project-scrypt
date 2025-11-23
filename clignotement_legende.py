from PySide6.QtCore import QTimer

def clignoter_avions_urgence(game_widget, duree=4000, intervalle=200):
    """
    Clignotement des avions en Urgence (fuel < 10%)
    """
    temps_ecoule = 0
    timer = QTimer()

    def toggle_blink():
        nonlocal temps_ecoule
        temps_ecoule += intervalle
        for plane in game_widget.planes:
            if plane.avion.fuel < 10:
                plane.blink_urgence = not plane.blink_urgence
        game_widget.update()
        if temps_ecoule >= duree:
            for plane in game_widget.planes:
                plane.blink_urgence = False
            timer.stop()

    timer.timeout.connect(toggle_blink)
    timer.start(intervalle)


def clignoter_avions_attente(game_widget, duree=3000, intervalle=200):
    """
    Clignotement des avions en Attente (fuel >= 10% et non sélectionnés)
    """
    temps_ecoule = 0
    timer = QTimer()

    def toggle_blink():
        nonlocal temps_ecoule
        temps_ecoule += intervalle
        for plane in game_widget.planes:
            if plane.avion.fuel >= 10 and plane is not game_widget.selected_plane:
                plane.blink_attente = not plane.blink_attente
        game_widget.update()
        if temps_ecoule >= duree:
            for plane in game_widget.planes:
                plane.blink_attente = False
            timer.stop()

    timer.timeout.connect(toggle_blink)
    timer.start(intervalle)

