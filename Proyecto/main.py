from app import app
import flet as ft

'''
Este fichero lo he tenido que crear yo al estas usando linux.
cuando se pase el codigo a windows se elimina y en app.py hay 
que hacer cambios
'''

if __name__ == "__main__":
    # Ejecutar la aplicación en modo web
    ft.app(target=app, view=ft.WEB_BROWSER)
    