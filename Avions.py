class Avions:
    nb_avions = 0
    def __init__(self, nom, altitude, vitesse, fuel, cap):
        self.nom = nom
        self.altitude = altitude
        self.vitesse = vitesse
        self.fuel = fuel
        self.cap = cap
        Avions.nb_avions += 1

    def monter(self):
        self.altitude += 100
    def descendre(self):
        self.altitude -= 100
    def gauche(self):
        self.cap -= 45
    def droite(self):
        self.cap += 45
    def __del__(self):
        self.accepted = True
        Avions.nb_avions -= 1