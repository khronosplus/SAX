import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from scipy import fftpack
from normalize import normalize

class fftGUI:
    def __init__(self, master, data=None):
        self.nDataPoints = 100
        self.nModes = 5
        self.data = data
        self.layout(master)

    def layout(self, master):
        # generate tkinter scales and widgets
        frame = tkinter.Frame(master)
        self.nModeScale = tkinter.Scale(frame, label="# fft modes", orient=tkinter.HORIZONTAL,
                                        from_=1, to=50, length=500,
                                        command=self.set_n_modes)
        self.nModeScale.set(self.nModes)
        self.nModeScale.pack(side="bottom")

        self.dataScale = tkinter.Scale(frame, label="data seed", orient=tkinter.HORIZONTAL,
                                       from_=1, to=100, length=500,
                                       command=self.set_data)
        self.dataScale.set(1)
        self.dataScale.pack(side="bottom")

        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.draw()
        self.canvas = FigureCanvasTkAgg(fig, master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()

    def draw(self):
        # (re-)calculate and draw the main plot
        self.ax.cla()
        self.ax.plot(self.data, 'b-')
        k = self.nModes
        fft = fftpack.fft(self.data)
        fft[k+1:-k] = 0
        fft_fit = fftpack.ifft(fft).real
        self.ax.plot(fft_fit, 'r-')
        amplitudes = 2. / self.nDataPoints * np.abs(fft[1:k + 1])
        wavelengths = self.nDataPoints / np.arange(1, k + 1)
        self.ax.bar(wavelengths, amplitudes, color='g', alpha=0.2, width=1.5)

    def refresh(self):
        self.draw()
        self.canvas.draw()

    def set_data(self, seed):
        np.random.seed(int(seed))
        npoints = self.nDataPoints
        data = np.random.randn(npoints)
        data = data.cumsum()
        self.data = normalize(data).calculate().data
        self.refresh()

    def set_n_modes(self, n):
        # callback for the PAA width scale
        self.nModes = int(n)
        self.refresh()


# generate random time series
if __name__ == '__main__':
    #freeze_support()
    np.random.seed(1)
    npoints = 100
    data = np.random.randn(npoints)
    data = data.cumsum()

    root = tkinter.Tk()
    app = fftGUI(root, data=normalize(data).calculate().data)
    root.mainloop()