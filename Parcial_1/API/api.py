import pandas as pd
from sodapy import Socrata
from math import ceil

class SoilAPI:
    def __init__(self):
        
        self.soil_variables = [
            'ph_agua_suelo_2_5_1_0',
            'potasio_k_intercambiable_cmol_kg',
            'f_sforo_p_bray_ii_mg_kg'
        ]
    
        self.client = self._create_client()

    def _create_client(self):
        return Socrata("www.datos.gov.co", None)


    def get_data(self, dataset_identifier, **kwargs):
        return self.client.get(dataset_identifier, **kwargs)


    def convert_dataset_to_dataframe(self, data):

        dataframe = pd.DataFrame.from_records(data)
        number_of_columns = dataframe.shape[1]  # Número de columnas en el DataFrame
        
        if number_of_columns == 0:  # Verificar si no hay columnas
            raise ValueError("No se encontraron valores con estos parámetros. Verifique que haya escrito todo de manera correcta.")
        
        return dataframe


    def _data_normalize(self, dataset_values):
        # Normaliza los valores de las variables eliminando aquellos que no son números.
        dataset_position = 0
        while dataset_position < len(dataset_values):
            try:
                # Intentar convertir cada valor a tipo float
                dataset_values[dataset_position] = float(dataset_values[dataset_position])
                dataset_position += 1
            except ValueError:
                # Si el valor no es convertible a float, se elimina
                dataset_values.pop(dataset_position)


    def calculate_median(self, data):
        # Calcula la mediana de las variables del suelo.
        medians = {}
        for variable in self.soil_variables:
            # Obtener los valores de la variable actual, removiendo valores NaN
            values = list(data[variable].dropna())
            self._data_normalize(values)  # Normalizar los valores
            values.sort()  # Ordenar los valores para calcular la mediana
            length = len(values)

            if length == 0:
                # Si no hay datos, la mediana es "No Disponible"
                medians[variable] = "No Disponible"
            elif length % 2 == 0:
                # Si hay un número par de valores, se promedian los dos centrales
                median = (values[length // 2] + values[(length // 2) - 1]) / 2
            else:
                # Si hay un número impar de valores, la mediana es el valor central
                median = values[length // 2]

            medians[variable] = median
        return medians


    def get_relevant_info(self, data):
        # Selecciona las columnas más relevantes para el análisis.
        columns = ["departamento", "municipio", "cultivo", "topografia"] + self.soil_variables
        return data[columns].copy()

    def normalize_params(self, params):
        # Normalizar los parámetros de entrada para consistencia (mayúsculas y capitalización)
        params["departamento"] = params["departamento"].upper()
        params["municipio"] = params["municipio"].upper()
        params["cultivo"] = params["cultivo"].title()
