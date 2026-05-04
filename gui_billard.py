import tkinter as tk
 
TABLE_W  = 900
TABLE_H  = 500
PAD      = 60
CUSHION  = 22
POCKET_R = 22
WIN_W    = TABLE_W + PAD * 2
WIN_H    = TABLE_H + PAD * 2
 
POCKETS = [
    (PAD, PAD),
    (PAD + TABLE_W // 2, PAD - 4),
    (PAD + TABLE_W, PAD),
    (PAD, PAD + TABLE_H),
    (PAD + TABLE_W // 2, PAD + TABLE_H + 4),
    (PAD + TABLE_W, PAD + TABLE_H),
]
 
def draw(root):
    c = tk.Canvas(root, width=WIN_W, height=WIN_H, bg="black", highlightthickness=0)
    c.pack(padx=12, pady=12)
 
    # Cadre
    c.create_rectangle(2, 2, WIN_W - 2, WIN_H - 2, fill="", outline="white", width=3)
 
    # Coussins
    c.create_rectangle(PAD - CUSHION, PAD - CUSHION,
                        PAD + TABLE_W + CUSHION, PAD + TABLE_H + CUSHION,
                        fill="#1a1a1a", outline="white", width=1)
 
    # Surface
    c.create_rectangle(PAD, PAD, PAD + TABLE_W, PAD + TABLE_H,
                        fill="#0d0d0d", outline="white", width=2)
 
    # Poches
    for (px, py) in POCKETS:
        c.create_oval(px - POCKET_R, py - POCKET_R,
                      px + POCKET_R, py + POCKET_R,
                      fill="black", outline="white", width=2)
 
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Table de Billard")
    root.resizable(False, False)
    root.configure(bg="black")
    draw(root)
    root.mainloop()