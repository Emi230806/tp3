import numpy as np
import json

dt  = 0.1
epsilon = 0.01

class ValeurConfigInvalide(Exception):
    pass

class ChampManquant(Exception):
    pass

def lire_config(chemin):
    with open(chemin, "r") as f:
        config = json.load(f)

    champs_requis = ["largeur", "hauteur", "rayon", "mu", "balles"]
    for champ in champs_requis:
        if champ not in config:
            raise ChampManquant(f"Champ manquant : {champ}")

    if config["largeur"] <= 0 or config["hauteur"] <= 0:
        raise ValeurConfigInvalide("Les dimensions doivent être positives")
    if config["rayon"] <= 0:
        raise ValeurConfigInvalide("Le rayon doit être positif")
    if not (0 <= config["mu"] <= 1):
        raise ValeurConfigInvalide("mu doit être entre 0 et 1")
    if len(config["balles"]) == 0:
        raise ValeurConfigInvalide("Il doit y avoir au moins une balle")

    for i, balle in enumerate(config["balles"]):
        if "position" not in balle:
            raise ChampManquant(f"Champ manquant pour la balle {i}")

    return config

class Noeud :
    def __init__(self, position, vitesse) :
        self.position = position
        self.vitesse = vitesse
        self.droite = None
        self.gauche = None
        self.parent = None

class Balle:
    def __init__(self, position, theta, v0):

        theta_rad = np.radians(theta)

        self.p = np.array(position, dtype=float)
        self.v = v0 * np.array([np.cos(theta_rad), np.sin(theta_rad)])

    def mise_a_jour(self, dt):
        self.p = self.p + self.v * dt

    def get_position(self):
        return self.p.copy()
    
    def get_vitesse(self) :
        return self.v.copy()


class Simulation:
    def __init__(self, largeur, hauteur, rayon, dt, mu, epsilon):
        self.largeur = largeur
        self.hauteur = hauteur
        self.r = rayon
        self.dt = dt
        self.mu = mu
        self.epsilon = epsilon

        self.p_min = np.array([rayon, rayon])
        self.p_max = np.array([largeur - rayon, hauteur - rayon])


    def calculer_trajectoire(self, balle):

        if np.allclose(balle.v, [0, 0]) :
            return Noeud(balle.get_position(), balle.get_vitesse())
        
        racine = Noeud(balle.get_position(), balle.get_vitesse()) #racine position initiale
        pointeur = racine

        while True:
            #friction
            balle.v = balle.v * (1 - (self.mu * self.dt))

            #rebonds
            self.appliquer_rebond(balle)

            #nouvelle position
            balle.mise_a_jour(self.dt)

            nouveau_noeud = Noeud(balle.get_position(), balle.get_vitesse())
            #on avance, nouv.position/nouv.noeud

            pointeur.droite = nouveau_noeud
            nouveau_noeud.gauche = pointeur
            nouveau_noeud.parent = pointeur
            pointeur = nouveau_noeud

            if np.linalg.norm(balle.v) <= self.epsilon :
                break

        return racine
    
    def appliquer_rebond(self, balle) :
        p = balle.get_position()
        v = balle.get_vitesse()

        #rebond gauche
        if p[0] < self.p_min[0] :
            p[0] = self.p_min[0]
            n = np.array([1, 0])
            v = v - 2 * np.dot(v, n) * n
        
        #rebond droit 
        if p[0] > self.p_max[0] :
            p[0] = self.p_max[0]
            n = np.array([-1, 0])
            v = v - 2 * np.dot(v, n) * n
        
        #rebond bas 
        if p[1] < self.p_min[1] :
            p[1] = self.p_min[1]
            n = np.array([0, 1])
            v = v - 2 * np.dot(v, n) * n

        #rebond haut 
        if p[1] > self.p_max[1] :
            p[1] = self.p_max[1]
            n = np.array([0, -1])
            v = v - 2 * np.dot(v, n) * n

        balle.p = p
        balle.v = v


##Test, retourne juste positions et finale sans rebonds
if __name__ == "__main__":
    import os

    try:
        chemin = os.path.join(os.path.dirname(__file__), "configurer.json")
        config = lire_config(chemin)
    except (ValeurConfigInvalide, ChampManquant) as e:
        print(f"Erreur de configuration : {e}")
        exit()

    sim = Simulation(config["largeur"], config["hauteur"], config["rayon"], dt, config["mu"], epsilon)
    b = config["balles"][0]
    balle = Balle(b["position"], b["theta"], b["v0"])

    trajectoire = sim.calculer_trajectoire(balle)
    noeud_courant = trajectoire
    i = 0
    while noeud_courant is not None:
        if i % 10 == 0:
            print(f"position: {noeud_courant.position}, vitesse: {noeud_courant.vitesse}")
        noeud_courant = noeud_courant.droite
        i += 1


