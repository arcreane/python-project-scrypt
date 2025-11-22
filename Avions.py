class Avions:
    nb_avions = 0
    global_id = 1
    def __init__(self, nom=None, altitude=None, vitesse=None, fuel=None, cap=None):
        self.id = Avions.global_id
        Avions.global_id += 1

        self.nom = nom if nom else f"Avion {self.id}"
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
        Avions.nb_avions -= 1