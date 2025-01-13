# from views import MainView

# def app(page):
#     # Cargar la vista principal
#     main_view = MainView(page)
#     main_view.build()


'''
para windos se elimina el fichero main.py 
y se ejecuta el programa con el codigo de abajo
'''

from views import MainView  # Importar la vista principal

def main(page):
    # Crear la instancia de la vista principal
    main_view = MainView(page)
    main_view.build()

# Esto es típico en Flet para correr la app
if __name__ == "__main__":
    import flet
    flet.app(target=main)
