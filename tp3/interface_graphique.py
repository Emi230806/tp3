import tkinter as tk
from etpae_1 import Simulation, Balle, lire_config, dt, epsilon
import os

chemin = os.path.join(os.path.dirname(__file__), "configurer.json")
config = lire_config(chemin)

fenetre = tk.Tk()
fenetre.resizable(False, False) # Empêche le redimensionnement de la fenêtre.
canvas = tk.Canvas(fenetre, width=config["largeur"] + 2 * config["epaisseur_bande"], height=config["hauteur"] + 2 * config["epaisseur_bande"], bg="white")
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
    e_b = config["epaisseur_bande"]
    canvas.create_rectangle(0, 0, config["largeur"] + 2*e_b, config["hauteur"] + 2*e_b, fill="dark green", outline="")
    canvas.create_rectangle(e_b, e_b, e_b + config["largeur"], e_b + config["hauteur"], fill="green", outline="")

def sim_vers_canvas(px, py):
    cx = config["epaisseur_bande"] + px
    cy = config["epaisseur_bande"] + (config["hauteur"] - py)
    return cx, cy

noeud_courant = None
after_id      = None

def dessiner_balle(px, py):
    canvas.delete("balle")
    cx, cy = sim_vers_canvas(px, py)
    r = config["rayon"]
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="white", outline="black", tags="balle")

def animer():
    global noeud_courant, after_id
    if noeud_courant is None:
        return
    dessiner_balle(*noeud_courant.position)
    noeud_courant = noeud_courant.droite
    if noeud_courant is not None:
        after_id = fenetre.after(config["delai_ms"], animer)
        
def simuler():
    global noeud_courant, after_id
    if after_id is not None:
        fenetre.after_cancel(after_id)
        after_id = None

    dessiner_terrain()
    balle = Balle(config["balles"][0]["position"], config["balles"][0]["theta"], config["balles"][0]["v0"])
    sim = Simulation(config["largeur"], config["hauteur"], config["rayon"], dt, config["mu"], epsilon)
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
