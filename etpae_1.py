import numpy as np

class Noeud :
    def __init__(self, position) :
        self.position = position
        self.droite = None
        self.gauche = None
        self.parent = None

class Balle:
    def __init__(self, p0, theta, v0):

        theta_rad = np.radians(theta)

        self.p = np.array(p0, dtype=float)
        self.v = v0 * np.array([np.cos(theta_rad), np.sin(theta_rad)])

    def mise_a_jour(self, dt):
       
        self.p = self.p + self.v * dt

    def get_position(self):
        return self.p.copy()


class Simulation:
    def __init__(self, largeur, hauteur, rayon, dt):
        self.largeur = largeur
        self.hauteur = hauteur
        self.r = rayon
        self.dt = dt

        self.p_min = np.array([rayon, rayon])
        self.p_max = np.array([largeur - rayon, hauteur - rayon])

    def touche_bord(self, p):

        return np.any(p <= self.p_min) or np.any(p >= self.p_max)
    # Est-ce que la balle touche un mur ?

    def calculer_trajectoire(self, balle):

        if np.allclose(balle.v, [0, 0]) :
            return Noeud(balle.get_position())
        
        racine = Noeud(balle.get_position())
        pointeur = racine

        while True:
            balle.mise_a_jour(self.dt)
            nouvelle_position = balle.get_position()

            nouveau_noeud = Noeud(nouvelle_position)
            #on avance, nouv.position/nouv.noeud

          
            pointeur.droite = nouveau_noeud
            nouveau_noeud.gauche = pointeur
            nouveau_noeud.parent = pointeur

            pointeur = nouveau_noeud

            if self.touche_bord(nouvelle_position):
                break

        return racine

##Test, retourne juste positions et finale sans rebonds
if __name__ == "__main__" :
    largeur = 200
    hauteur = 100
    rayon = 1
    dt = 0.1

    sim = Simulation(largeur, hauteur, rayon, dt)

    p0 = [10, 10]
    theta = 45
    v0 = 20

    balle = Balle(p0, theta, v0)
    trajectoire = sim.calculer_trajectoire(balle)
    noeud_courant = trajectoire

    while noeud_courant is not None:
        print(noeud_courant.position)
        noeud_courant = noeud_courant.droite
