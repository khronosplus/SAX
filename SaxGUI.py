import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sax import *

class App:
    def __init__(self, master, data=None):
        self.sax = SAX( PAA(data, width=5).calculate())
        self.layout(master)

    def layout(self, master):
        # Create a container
        frame = tkinter.Frame(master)
        # Create 2 buttons
        self.widthScale = tkinter.Scale(frame,  label="PAA width", orient=tkinter.HORIZONTAL,
                                         from_=2, to=100, length=300,
                                         command=self.set_paa_width)
        self.widthScale.set(self.sax.paa.width)
        self.widthScale.pack(side="bottom")
        self.cardScale = tkinter.Scale(frame, label="SAA cardinality", orient=tkinter.HORIZONTAL,
                                       from_=2, to=8, length = 300,
                                           command=self.set_sax_card)
        self.cardScale.set(self.sax.card)
        self.cardScale.pack(side="bottom")

        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.draw()
        self.canvas = FigureCanvasTkAgg(fig, master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()

    def draw(self):
        self.ax.cla()
        self.sax.paa.calculate()
        self.sax.calculate()
        l = len(self.sax.paa.data)
        x = list(range(l))
        w = self.sax.paa.width
        self.ts_plot, = self.ax.plot(x, self.sax.paa.data, 'b-')

        for i, d in enumerate(self.sax.paa.result):
            low = i * w
            high = min(l - 1, (i + 1) * w)
            self.ax.plot([x[low], x[high]], [d, d], 'r-')
            self.ax.text((x[low]+x[high])/2, -2, self.sax.result[i], fontsize=12)

    def set_paa_width(self, width):
        self.sax.paa.setWidth(int(width))
        self.draw()
        self.canvas.draw()

    def set_sax_card(self, card):
        self.sax.setCardinality(int(card))
        self.draw()
        self.canvas.draw()


# generate random time series
np.random.seed(1)
npoints = 100
x = list(range(npoints))
data = np.random.randn(npoints)
data = data.cumsum()

root = tkinter.Tk()
app = App(root, data=data)
root.mainloop()