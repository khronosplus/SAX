import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sax import *

class SaxGUI:
    def __init__(self, master, data=None):
        self.sax = SAX( PAA(data, width=5).calculate())
        self.layout(master)

    def layout(self, master):
        # generate tkinter scales and widgets
        frame = tkinter.Frame(master)
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
        # (re-)calculate PAA and SAX and draw the main plot
        self.ax.cla()
        self.sax.paa.calculate()
        self.sax.calculate()
        l = len(self.sax.paa.data)
        x = list(range(l))
        w = self.sax.paa.width

        # plot the time series itself
        self.ax.plot(x, self.sax.paa.data, 'b-')

        # plot paa bars and points and sax letters
        mids = []
        for i, d in enumerate(self.sax.paa.result):
            low = i * w
            high = min(l - 1, (i + 1) * w)
            self.ax.plot([x[low], x[high]], [d, d], 'r-')
            binmid = (x[low]+x[high])/2
            self.ax.text(binmid, -2, self.sax.result[i], fontsize=12)
            mids.append(binmid)
        self.ax.plot(mids, self.sax.paa.result, 'ro')

        # plot sax breakpoints vertical lines
        card = self.sax.card
        for c in range(card - 1):
            y = self.sax.breakpointLookup[card-2][c]
            self.ax.plot([x[0], x[-1]], [y, y], 'k--', alpha=0.5)


    def set_paa_width(self, width):
        # callback for the PAA width scale
        self.sax.paa.setWidth(int(width))
        self.draw()
        self.canvas.draw()

    def set_sax_card(self, card):
        # callback for the SAX cardinality scale
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
app = SaxGUI(root, data=data)
root.mainloop()