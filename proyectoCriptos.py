from tkinter import *
from tkinter import ttk
import krakenex
from pykrakenapi import KrakenAPI
import pandas as pd
import plotly.graph_objects as go



def funcion_1(cripto, col, name):
    cripto_media_movil = cripto.rolling(14).mean()
    cripto_media_movil.dropna(inplace=True)

    delta = cripto['close'].diff()
    delta.dropna(inplace=True)
    window_rsi = 14
    up = delta.clip(lower=0)
    up_df = pd.DataFrame(up)
    up_df_avg = up_df.rolling(window=window_rsi, min_periods=window_rsi).mean()

    down = -1 * delta.clip(upper=0)
    down_df = pd.DataFrame(down)
    down_df_avg = down_df.rolling(window=window_rsi, min_periods=window_rsi).mean()

    RS = up_df_avg / down_df_avg
    RSI = 100 - (100 / (1 + RS))
    # RSI_actual = RSI.iloc[-1]

    columna1 = cripto_media_movil[col]

    fig = go.Figure(data=[go.Candlestick(x=cripto.index,
                                         open=cripto['open'],
                                         high=cripto['high'],
                                         low=cripto['low'],
                                         close=cripto['close']),
                          go.Scatter(x=cripto.index, y=cripto['close'],
                                     line=dict(color='purple', width=2), name=name),
                          go.Scatter(x=cripto_media_movil.index, y=columna1,
                                     line=dict(color='yellow', width=2), name='media movil'),
                          go.Scatter(x=RSI.index, y=columna1,
                                     line=dict(color='blue', width=2), name='RSI')
                          ])

    fig.show()


class Cripto:
    def __init__(self, master):
        self.col = None
        self.etiquetatiempo = None
        self.etiquetafc = None
        self.otra_ventana = None
        self.boton_interval = None
        self.botonentermedia = None
        self.cripto = None
        self.comboExample = None
        self.labelTop = None
        self.master = master
        self.ventanamedia = None
        self.interval = None

        menu = Menu(self.master)
        self.master.config(menu=menu)

        filemenu = Menu(menu)
        filemenu.add_command(label="Exit", command=root.destroy)
        menu.add_cascade(label="Tools", menu=filemenu)

        self.api = krakenex.API()
        self.k = KrakenAPI(self.api)

        self.etiqueta = Label(master, text="Cripto Analysis")
        self.etiqueta.pack()

        self.labelTop = Label(master, text="Seleccionar criptomoneda")
        self.labelTop.place(x=10, y=20)
        lista_criptos = []
        pairs = self.k.get_tradable_asset_pairs()
        for i in pairs['wsname']:
            lista_criptos.append(i)
        self.comboExample = ttk.Combobox(master, values=lista_criptos)
        self.comboExample.place(x=10, y=50)
        self.comboExample.current(0)

        self.etiquetatiempo = Label(master, text="Intervalo de tiempo")
        self.etiquetatiempo.place(x=10, y=80)

        self.interval = ttk.Combobox(master, values=['1', '5', '15', '30', '60', '240', '1440', '10080'])
        self.interval.place(x=10, y=100)
        self.interval.current(0)

        self.etiquetatiempo = Label(master, text="Seleccionar columna para calcular la media y el RSI")
        self.etiquetatiempo.place(x=10, y=130)

        self.colum = ttk.Combobox(master, values=['open', 'high', 'low', 'close'])
        self.colum.place(x=10, y=150)
        self.colum.current(0)

        self.botonentermedia = Button(master, text="Enter", command=self.seleccionardatos)
        self.botonentermedia.place(x=200, y=100)

    def seleccionardatos(self):
        self.cripto = self.comboExample.get()
        self.boton_interval = self.interval.get()
        self.col = self.colum.get()

        datos, _ = self.k.get_ohlc_data(self.cripto, interval=int(self.boton_interval))
        funcion_1(datos, self.col, self.cripto)


if __name__ == '__main__':
    root = Tk()
    miVentana = Cripto(root)
    root.wm_title("Cripto Analysis")
    root.geometry("350x250")
    root.config()
    root.mainloop()
