from API.api import SoilAPI
from UI.ui import UserInterface

dataset_identifier = "ch4u-f3i5"  # Identificador del conjunto de datos que se utilizará

class MainProgram:
    def __init__(self):
        self.api = SoilAPI()  # Inicializa la API para acceder a los datos del suelo
        self.ui = UserInterface(self.api.soil_variables)  

    def manage_data(self):
        params = self.ui.get_params() 
        self.api.normalize_params(params)  
        result = self.api.get_data(dataset_identifier = dataset_identifier, **params) 

        try:
            result_dataframe = self.api.convert_dataset_to_dataframe(result)  
        except ValueError as error:
            print(f"\n\tError: {error}\n") 
            return
        
        relevant_info = self.api.get_relevant_info(result_dataframe)  
        medians = self.api.calculate_median(relevant_info) 
        self.ui.print_table(relevant_info, medians) 

    def main(self):
        while True:
            self.ui.menu()  # Muestra el menú de opciones
            opcion = self.ui.get_option()  

            if opcion == 1:
                self.manage_data()  
            elif opcion == 2:
                return  # Sale del programa si la opción es salir
                
            input("\n\tOprima enter para volver al menú...")  
            self.ui.clean_terminal()  


if __name__ == "__main__":
    program = MainProgram()  # Inicializa el programa principal
    program.main()  # Llama al método principal para iniciar la ejecución
