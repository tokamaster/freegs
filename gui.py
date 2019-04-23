import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

class Game(tk.Tk):
    def  __init__(self):
        super().__init__()

        self.title("Plasma Shaper")
        self.geometry("900x800")
        self.resizable(False, False)

        self.screen = tk.Canvas(self, bg="white", width=600, height=900)
        self.screen.pack(expand=1, fill=tk.BOTH)

        self.right_frame = tk.Frame(self, width=400, height=900)
        self.right_frame.pack_propagate(0)

        self.config_text = tk.StringVar(self.right_frame)
        self.config_text.set("Current configuration (A):")
        self.config_title = tk.Label(self.right_frame, textvar=self.config_text, background="black", foreground="white" )
        self.config_title.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.controlcurrents = ['','','','','','']
        self.cur1 = tk.StringVar()
        self.cur2 = tk.StringVar()
        self.cur3 = tk.StringVar()
        self.cur4 = tk.StringVar()
        self.cur5 = tk.StringVar()
        self.cur6 = tk.StringVar()
        self.cur1.set('PF Coil 1: ' +str(self.controlcurrents[0]))
        self.cur2.set('PF Coil 2: ' +str(self.controlcurrents[1]))
        self.cur3.set('PF Coil 3: ' +str(self.controlcurrents[2]))
        self.cur4.set('PF Coil 4: ' +str(self.controlcurrents[3]))
        self.cur5.set('PF Coil 5: ' +str(self.controlcurrents[4]))
        self.cur6.set('Central Sol.: ' +str(self.controlcurrents[5]))
        self.var1 = tk.Label(self.right_frame, textvariable=self.cur1)
        self.var1.pack(fill=tk.BOTH, expand=1)
        var2 = tk.Label(self.right_frame, textvariable=self.cur2)
        var2.pack(fill=tk.BOTH, expand=1)
        var3 = tk.Label(self.right_frame, textvariable=self.cur3)
        var3.pack(fill=tk.BOTH, expand=1)
        var4 = tk.Label(self.right_frame, textvariable=self.cur4)
        var4.pack(fill=tk.BOTH, expand=1)
        var5 = tk.Label(self.right_frame, textvariable=self.cur5)
        var5.pack(fill=tk.BOTH, expand=1)
        var6 = tk.Label(self.right_frame, textvariable=self.cur6)
        var6.pack(fill=tk.BOTH, expand=1)

        config_title = tk.Label(self.right_frame, text="Set currents (A):", background="black", foreground="white")
        config_space = tk.Frame(self.right_frame, background="lightgrey", width=300, height=320)
        config_space.pack_propagate(0)

        config_space.pack(side=tk.BOTTOM)
        config_title.pack(side=tk.BOTTOM, fill=tk.X)

        text1 = tk.Label(config_space, text="PF Coil 1")
        text2 = tk.Label(config_space, text="PF Coil 2")
        text3 = tk.Label(config_space, text="PF Coil 3")
        text4 = tk.Label(config_space, text="PF Coil 4")
        text5 = tk.Label(config_space, text="PF Coil 5")
        text6 = tk.Label(config_space, text="Central Solenoid")

        self.coil1 = tk.Entry(config_space, bg="white", fg="black")
        self.coil2 = tk.Entry(config_space, bg="white", fg="black")
        self.coil3 = tk.Entry(config_space, bg="white", fg="black")
        self.coil4 = tk.Entry(config_space, bg="white", fg="black")
        self.coil5 = tk.Entry(config_space, bg="white", fg="black")
        self.coilsol = tk.Entry(config_space, bg="white", fg="black")
        #self.plot_button = tk.Button(config_space, text="Plot", command=self.plot)
        self.update_button = tk.Button(config_space, text="Update", command=self.update)
        self.optimise_button = tk.Button(config_space, text="Start", command=self.optimise)

        text1.pack(fill=tk.BOTH, expand=1)
        self.coil1.pack(fill=tk.BOTH, expand=1)
        text2.pack(fill=tk.BOTH, expand=1)
        self.coil2.pack(fill=tk.BOTH, expand=1)
        text3.pack(fill=tk.BOTH, expand=1)
        self.coil3.pack(fill=tk.BOTH, expand=1)
        text4.pack(fill=tk.BOTH, expand=1)
        self.coil4.pack(fill=tk.BOTH, expand=1)
        text5.pack(fill=tk.BOTH, expand=1)
        self.coil5.pack(fill=tk.BOTH, expand=1)
        text6.pack(fill=tk.BOTH, expand=1)
        self.coilsol.pack(fill=tk.BOTH, expand=1)
        #self.plot_button.pack(fill=tk.X, side=tk.LEFT)
        self.update_button.pack(fill=tk.X, side=tk.LEFT)
        self.optimise_button.pack(fill=tk.X, side=tk.RIGHT)

        self.right_frame.pack(side=tk.RIGHT)
        self.screen.pack(side=tk.LEFT)

    def first_opti(self):

        from freegs import machine
        from freegs.equilibrium import Equilibrium

        self.tokamak = machine.MAST_sym()
        self.eq = Equilibrium(tokamak=self.tokamak, Rmin=0.1, Rmax=2.0, Zmin=-2.0, Zmax=2.0, nx=65, ny=65)
        from freegs.jtor import ConstrainPaxisIp

        self.profiles = ConstrainPaxisIp(3e3, 7e5, 0.4)

        from freegs import control

        self.xpoints = [(0.7, -1.1),(0.7, 1.1)]
        self.isoflux = [(0.7, -1.1, 1.45, 0.0),(0.7, 1.1, 1.45, 0.0)]
        self.constrain = control.constrain(xpoints=self.xpoints, gamma=1e-12, isoflux=self.isoflux)

        return self.tokamak, self.eq, self.profiles, self.constrain

    def optimise(self):

        from freegs import picard
        ## TODO: add 'Optimising...' screen before picard begins
        self.tokamak, self.eq, self.profiles, self.constrain = self.first_opti()
        picard.solve(self.eq, self.profiles, self.constrain, show=True)

        self.controlcurrents = self.tokamak.controlCurrents()

        self.showcurrents()
        self.tokamak_xs = tk.PhotoImage(file='/home/enmidol/Documents/freegs/assets/toka.png', width=500,height=800)
        self.screen.create_image(-20,-65,image=self.tokamak_xs,anchor='nw')
        self.screen.pack(expand=1, fill=tk.BOTH)

    def update(self):

        self.controlcurrents[0] = self.coil1.get()
        self.controlcurrents[0] = float(self.controlcurrents[0])
        self.coil1.pack(fill=tk.BOTH, expand=1)
        self.controlcurrents[1] = self.coil2.get()
        self.controlcurrents[1] = float(self.controlcurrents[1])
        self.coil2.pack(fill=tk.BOTH, expand=1)
        self.controlcurrents[2] = self.coil3.get()
        self.controlcurrents[2] = float(self.controlcurrents[2])
        self.coil3.pack(fill=tk.BOTH, expand=1)
        self.controlcurrents[3] = self.coil4.get()
        self.controlcurrents[3] = float(self.controlcurrents[3])
        self.coil4.pack(fill=tk.BOTH, expand=1)
        self.controlcurrents[4] = self.coil5.get()
        self.controlcurrents[4] = float(self.controlcurrents[4])
        self.coil5.pack(fill=tk.BOTH, expand=1)
        self.controlcurrents[5] = self.coilsol.get()
        self.controlcurrents[5] = float(self.controlcurrents[5])
        self.coilsol.pack(fill=tk.BOTH, expand=1)
        self.cur1.set('PF Coil 1: ' +str(self.controlcurrents[0]))
        self.cur2.set('PF Coil 2: ' +str(self.controlcurrents[1]))
        self.cur3.set('PF Coil 3: ' +str(self.controlcurrents[2]))
        self.cur4.set('PF Coil 4: ' +str(self.controlcurrents[3]))
        self.cur5.set('PF Coil 5: ' +str(self.controlcurrents[4]))
        self.cur6.set('Central Sol.: ' +str(self.controlcurrents[5]))
        self.run_freegs()
        self.tokamak_xs = tk.PhotoImage(file='/home/enmidol/Documents/freegs/assets/toka.png')
        self.screen.create_image(-20,-65,image=self.tokamak_xs,anchor='nw')
        self.screen.pack(expand=1, fill=tk.BOTH)

    def showcurrents(self):

        self.cur1.set('PF Coil 1: ' +str(self.controlcurrents[0]))
        self.cur2.set('PF Coil 2: ' +str(self.controlcurrents[1]))
        self.cur3.set('PF Coil 3: ' +str(self.controlcurrents[2]))
        self.cur4.set('PF Coil 4: ' +str(self.controlcurrents[3]))
        self.cur5.set('PF Coil 5: ' +str(self.controlcurrents[4]))
        self.cur6.set('Central Sol.: ' +str(self.controlcurrents[5]))

    def run_freegs(self):
        from freegs.plotting import plotEquilibrium
        self.tokamak.setControlCurrents(self.controlcurrents)
        plotEquilibrium(self.eq,show=False)

    #def plot(self):
        #self.tokamak_xs = tk.PhotoImage(file='/home/enmidol/Documents/plasma-shaper/assets/toka.png')
        #self.screen.create_image(1,1,image=self.tokamak_xs,anchor='nw')
        #self.screen.pack(expand=1, fill=tk.BOTH)


if __name__ == "__main__":
    game = Game()
    game.mainloop()
