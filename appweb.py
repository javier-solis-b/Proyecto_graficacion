#Proyecto final por:
#Francisco Javier Solis Bamaca
#Paola Jadziry Culebro Ovando
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter as tk
from tkinter import font

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Análisis y Pronóstico de Ventas")
        self.geometry("800x600")
        self.configure(bg='lightblue')
        self.titulo_font = font.Font(family="Helvetica", size=36, weight="bold")
        self.titulo_label = tk.Label(self, text="ROBOT SHOP", font=self.titulo_font, bg='lightblue', fg='green')
        self.titulo_label.pack(pady=10)
        self.boton_cargar = tk.Button(self, text="Cargar Archivo CSV", command=self.cargar_archivo, bg='lightgreen', fg='black')
        self.boton_cargar.pack(pady=50)
        self.boton_visualizar = tk.Button(self, text="Visualizar Ventas", command=self.visualizar_ventas, bg='lightgreen', fg='black')
        self.boton_visualizar.pack(pady=50)
        self.boton_pronostico = tk.Button(self, text="Pronóstico de Ventas", command=self.pronostico_ventas, bg='lightgreen', fg='black')
        self.boton_pronostico.pack(pady=50)
        self.etiqueta_final = tk.Label(self, text="Graficación\nFrancisco Javier Solis Bamaca\ny\nPaola Jadziry Culebro Ovando", justify=tk.CENTER, bg='lightblue', fg='black')
        self.etiqueta_final.place(relx=0.5, rely=1.0, anchor='s')
        self.dataframe = None

    def cargar_archivo(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if ruta_archivo:
            self.dataframe = pd.read_csv(ruta_archivo, index_col='Fecha', parse_dates=True, dayfirst=True)
            self.dataframe.index = pd.to_datetime(self.dataframe.index, dayfirst=True)
            self.dataframe['Año'] = self.dataframe.index.year
            self.dataframe['Mes'] = self.dataframe.index.month
            self.dataframe['Dia'] = self.dataframe.index.day
            print("Archivo cargado exitosamente.")
            self.boton_cargar.config(text="Archivo Cargado")

    def visualizar_ventas(self):
        if self.dataframe is not None:
            ventas_2017 = self.dataframe[self.dataframe['Año'] == 2017]
            ventas_2018 = self.dataframe[self.dataframe['Año'] == 2018]
            promedios_mensuales = self.dataframe.resample('ME').mean()
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(ventas_2017.index.month, ventas_2017['ventas'], color='blue', marker='o', linestyle='-', label='2017')
            ax.plot(ventas_2018.index.month, ventas_2018['ventas'], color='orange', marker='o', linestyle='-', label='2018')
            ax.plot(promedios_mensuales.index.month, promedios_mensuales['ventas'], color='green', marker='o', linestyle='-', label='Promedios Mensuales')
            ax.set_title('Ventas Totales por Mes')
            ax.set_xlabel('Mes')
            ax.set_ylabel('Ventas ($)')
            ax.legend()
            ax.margins(x=0.05, y=0.05)
            plt.show()
        else:
            print("No se ha cargado ningún archivo.")

    def pronostico_ventas(self):
        if self.dataframe is not None:
            X_train = self.dataframe[(self.dataframe['Año'] == 2018) & (self.dataframe['Mes'] < 7)].index.day
            y_train = self.dataframe[(self.dataframe['Año'] == 2018) & (self.dataframe['Mes'] < 7)]['ventas']
            X_test = self.dataframe[(self.dataframe['Año'] == 2018) & (self.dataframe['Mes'] == 7)].index.day
            y_test = self.dataframe[(self.dataframe['Año'] == 2018) & (self.dataframe['Mes'] == 7)]['ventas']

            modelo = LinearRegression()
            modelo.fit(X_train.values.reshape(-1, 1), y_train)

            fechas_pronostico = pd.date_range(start='2019-06-01', end='2019-07-31')
            dias_pronostico = fechas_pronostico.day
            pronostico = modelo.predict(dias_pronostico.values.reshape(-1, 1))

            pronostico_df = pd.DataFrame({'Fecha': fechas_pronostico, 'Pronostico': pronostico})

            # Permitir al usuario seleccionar la ubicación y el nombre del archivo para guardar
            ruta_guardar = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("csv file", ".csv")])
            if ruta_guardar:
                pronostico_df.to_csv(ruta_guardar, index=False)
                print("Pronóstico guardado exitosamente.")

            # Visualizar el DataFrame
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(pronostico_df['Fecha'], pronostico_df['Pronostico'], color='orange', marker='o', linestyle='-', label='Pronóstico')
            ax.set_title('Pronóstico de Ventas para el Verano de 2019')
            ax.set_xlabel('Fecha')
            ax.set_ylabel('Ventas ($)')
            ax.legend()
            ax.margins(x=0.05, y=0.05)
            plt.show()
        else:
            print("No se ha cargado ningún archivo.")

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
