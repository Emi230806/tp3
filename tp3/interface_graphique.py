import tkinter as tk
from etpae_1 import Simulation, Balle

largeur  = 800
hauteur  = 600
epaisseur_bande = 15

fenetre = tk.Tk()
fenetre.resizable(False, False) # Empêche le redimensionnement de la fenêtre.
canvas = tk.Canvas(fenetre, width=largeur + 2 * epaisseur_bande,height=hauteur + 2 * epaisseur_bande, bg="white")
canvas.pack()

lbl_pos = tk.Label(fenetre, text="Position finale : –")
lbl_pos.pack(pady=4)

cadre_boutons = tk.Frame(fenetre)
cadre_boutons.pack(pady=4)
bouton_simuler = tk.Button(cadre_boutons, text="Tirer")
bouton_simuler.pack(side="left", padx=4)
bouton_reset = tk.Button(cadre_boutons, text="Recommencer")
bouton_reset.pack(side="left", padx=4)

def dessiner_terrain():
    canvas.delete("all")
    e_b = epaisseur_bande
    canvas.create_rectangle(0, 0, largeur + 2*e_b, hauteur + 2*e_b, fill="dark green", outline="")
    canvas.create_rectangle(e_b, e_b, e_b + largeur, e_b + hauteur, fill="green", outline="")

dessiner_terrain()
fenetre.mainloop()
