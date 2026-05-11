import tkinter as tk
from etpae_1 import Simulation, Balle

largeur = 800
hauteur = 600
epaisseur_bande = 15
rayon = 10
delai_ms = 16
mu = 0.05
epsilon = 0.01
dt = 0.1
p0 = [10, 10]
theta = 45
v0 = 200

fenetre = tk.Tk()
fenetre.resizable(False, False) # Empêche le redimensionnement de la fenêtre.
canvas = tk.Canvas(fenetre, width=largeur + 2 * epaisseur_bande,height=hauteur + 2 * epaisseur_bande, bg="white")
canvas.pack()

lbl_pos = tk.Label(fenetre, text="Position finale : –")
lbl_pos.pack(pady=4)

cadre_boutons = tk.Frame(fenetre)
cadre_boutons.pack(pady=4)
bouton_tirer = tk.Button(cadre_boutons, text="Tirer")
bouton_tirer.pack(side="left", padx=4)
bouton_recommencer = tk.Button(cadre_boutons, text="Recommencer")
bouton_recommencer.pack(side="left", padx=4)

def dessiner_terrain():
    canvas.delete("all")
    e_b = epaisseur_bande
    canvas.create_rectangle(0, 0, largeur + 2*e_b, hauteur + 2*e_b, fill="dark green", outline="")
    canvas.create_rectangle(e_b, e_b, e_b + largeur, e_b + hauteur, fill="green", outline="")

def sim_vers_canvas(px, py):
    cx = epaisseur_bande + px
    cy = epaisseur_bande + (hauteur - py)
    return cx, cy

noeud_courant = None
after_id      = None

def dessiner_balle(px, py):
    canvas.delete("balle")
    cx, cy = sim_vers_canvas(px, py)
    r = rayon
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="white", outline="black", tags="balle")

def animer():
    global noeud_courant, after_id
    if noeud_courant is None:
        return
    dessiner_balle(*noeud_courant.position)
    noeud_courant = noeud_courant.droite
    if noeud_courant is not None:
        after_id = fenetre.after(delai_ms, animer)
        
def simuler():
    global noeud_courant, after_id
    if after_id is not None:
        fenetre.after_cancel(after_id)
        after_id = None

    dessiner_terrain()
    balle = Balle(p0, theta, v0)
    sim = Simulation(largeur, hauteur, rayon, dt, mu, epsilon)
    trajectoire = sim.calculer_trajectoire(balle)
    dernier = trajectoire
    while dernier.droite is not None:
        dernier = dernier.droite
    px, py = dernier.position
    lbl_pos.config(text=f"Position finale : ({px:.1f}, {py:.1f})")

    noeud_courant = trajectoire
    animer()

def reset():
    global noeud_courant, after_id

    if after_id is not None:
        fenetre.after_cancel(after_id)
        after_id = None

    noeud_courant = None
    lbl_pos.config(text="Position finale : –")
    dessiner_terrain()

bouton_tirer.config(command=simuler)
bouton_recommencer.config(command=reset)

dessiner_terrain()
fenetre.mainloop()
