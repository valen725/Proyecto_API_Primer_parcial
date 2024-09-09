import os
from tabulate import tabulate

class UserInterface:
    def __init__(self, soil_variables):
        self.soil_variables = soil_variables  # Inicializa las variables de suelo que serán usadas en las tablas.

    def menu(self):
        print("¿Qué desea hacer?")
        print("1. Buscar")
        print("2. Salir")
    

    def get_option(self):
        while True:
            opcion = int(input("Ingrese un valor: "))
            if opcion != 1 and opcion != 2:
                print("\n\tOpción no válida\n")
                continue
            return opcion
        

    def get_params(self):
        params = {}
        params_name = ("departamento", "municipio", "cultivo", "limit") 
        
        print("\n\tIngrese los valores correspondientes\n")

        # Recoge valores para cada parámetro con validación de entrada
        for param in params_name:
            while True:
                value = input(f"Ingrese el valor de {param}: ")
                if len(value) == 0:
                    print("\t\n#######  Debe ingresar un valor #######\n")  # Verifica que no haya campos vacíos
                else:
                    break

            # Si el parámetro es el límite, verifica que no supere 1000
            if param == "limit":
                while True:
                    try:
                        if int(value) > 1000:
                            print("Se tomará como límite 1000 porque el ingresado lo sobrepasa") 
                            value = "1000"
                        break
                    except ValueError as error:
                        print(f"Error: {error}\n\t\tIntenta de nuevo")

            params[param] = value  # Almacena el valor ingresado para cada parámetro
        return params
    
    def print_table(self, data, medians):
    
        basic_info_columns = ["departamento", "municipio", "cultivo", "topografia"]
        soil_variable_table = [" pH ", " Potasio ", "Fósforo "]

        # Extrae los datos de información básica de la primera fila del DataFrame
        basic_info = [data.iloc[0][column] for column in basic_info_columns]

        # Crea una tabla para mostrar la información básica de la primera fila
        basic_table_data = [[" Información Básica "] + basic_info]
        print(tabulate(basic_table_data, headers=["", *basic_info_columns], tablefmt = "fancy_grid"))
        
        # Extrae los valores de la mediana para cada variable de suelo
        median_values = [medians.get(var, "No Disponible") for var in self.soil_variables]
        median_table_data = [[" Medianas "] + median_values]

        # Muestra la tabla de medianas
        print(tabulate(median_table_data, headers=["", *soil_variable_table], tablefmt = "fancy_grid"))

        
    def clean_terminal(self):
        os.system("cls" if os.name == "nt" else "clear")
