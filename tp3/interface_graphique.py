import tkinter as tk
import tkinter
from etpae_1 import Simulation, Balle, dt, epsilon
import os
import json
from tkinter import filedialog

class ValeurConfigInvalide(Exception):
    pass

class ChampManquant(Exception):
    pass

def lire_config(chemin):
    with open(chemin, "r") as f:
        config = json.load(f)

    champs_requis = ["largeur", "hauteur", "rayon", "balles"]
    for champ in champs_requis:
        if champ not in config:
            raise ChampManquant(f"Champ manquant : {champ}")

    if config["largeur"] <= 0 or config["hauteur"] <= 0:
        raise ValeurConfigInvalide("Les dimensions doivent être positives")
    if config["rayon"] <= 0:
        raise ValeurConfigInvalide("Le rayon doit être positif")
    if len(config["balles"]) == 0:
        raise ValeurConfigInvalide("Il doit y avoir au moins une balle")

    for i, balle in enumerate(config["balles"]):
        if "position" not in balle:
            raise ChampManquant(f"Champ manquant pour la balle {i}")

    return config

root_temp = tk.Tk()
root_temp.withdraw()

chemin = tkinter.filedialog.askopenfilename(title="Choisir un fichier JSON", filetypes=[("Fichiers JSON", "*.json")])

if not chemin:
    exit()

try:
    config = lire_config(chemin)

except (ValeurConfigInvalide, ChampManquant) as e:
    import tkinter.messagebox as mb
    mb.showerror("Erreur de configuration", str(e))
    exit()


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

label_vitesse_0 = tk.Label(cadre_boutons, text = "Vitesse initale : ")
label_vitesse_0.pack(side = "left", padx = 4)
champ_vitesse_0  = tk.Entry(cadre_boutons, width = 10)
champ_vitesse_0.pack(side="left", padx=4)

label_theta_0 = tk.Label(cadre_boutons, text = "Angle initial : ")
label_theta_0.pack(side = "left", padx = 4)
champ_theta_0  = tk.Entry(cadre_boutons, width = 10)
champ_theta_0.pack(side="left", padx=4)

label_mu = tk.Label(cadre_boutons, text = "Coeffcient de frottement : ")
label_mu.pack(side = "left", padx = 4)
champ_mu  = tk.Entry(cadre_boutons, width = 10)
champ_mu.pack(side="left", padx=4)
champ_mu.insert(0, str(config["mu"]))

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
after_id = None

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

    try:
        v0 = float(champ_vitesse_0.get())
    except ValueError:
        lbl_pos.config(text="Vitesse invalide ou manquante")
        return

    try:
        theta = float(champ_theta_0.get())
    except ValueError:
        lbl_pos.config(text="Angle invalide ou manquant")
        return
    
    try :
        mu = float(champ_mu.get())
        if not (0 <= mu < 1) :
            lbl_pos.config(text="le mu doit être entre 0 et 1")
            return
    except ValueError :
        lbl_pos.config(text = "mu invalide ou manquant")

    dessiner_terrain()
    balle = Balle(config["balles"][0]["position"], theta, v0)
    sim = Simulation(config["largeur"], config["hauteur"], config["rayon"], dt, mu, epsilon)
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

bouton_tirer.config(command = simuler)
bouton_recommencer.config(command = reset)

dessiner_terrain()
fenetre.mainloop()
