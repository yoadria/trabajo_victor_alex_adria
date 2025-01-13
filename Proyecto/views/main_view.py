import flet as ft

from views.alert_view import AlertView, QuestionDialog
from services.GeneracionDatos import generar_datos

class MainView:
    def __init__(self, page):
        self.page = page

    def build(self):
        from utils.style import button_style
        '''Método que construye la página principal'''

        self.page.title = "Página Principal"

        # Centrar los elementos de la página
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


        self.page.bgcolor = ft.colors.WHITE

        # Botones principales (Aplicación de estilo general)
        botones = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ElevatedButton(
                        text="Leer Datos",
                        width=300,
                        height=50,
                        style=button_style,
                        on_click=self.ir_a_leer,
                    ),
                    ft.ElevatedButton(
                        text="Insertar Datos",
                        width=300,
                        height=50,
                        style=button_style,
                        on_click=self.ir_a_insersiones,
                    ),
                    ft.ElevatedButton(
                        text="Actualizar Datos",
                        width=300,
                        height=50,
                        style=button_style,
                        on_click=self.ir_a_modificaciones,
                    ),
                    ft.ElevatedButton(
                        text="Eliminar Datos",
                        width=300,
                        height=50,
                        style=button_style,
                        on_click=self.ir_a_eliminar,
                    ),
                    ft.ElevatedButton(
                        text="Generar Datos",
                        width=300,
                        height=50,
                        style=button_style,
                        on_click=self.ir_a_generacion_datos,
                    ),
                    ft.ElevatedButton(
                        text="Salir",
                        width=300,
                        height=50,
                        style=button_style,
                        on_click=self.cerrar,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=15,  # Espacio entre los botones
            ),
            padding=10,
        )

        # Agregar los botones y título a la parte superior de la página
        self.page.add(
            ft.Container(
                content=ft.Text(
                    "Menú Principal",
                    size=28,
                    weight="bold",
                    color="Black"
                ),
                alignment=ft.alignment.center,
                margin=ft.Margin(0, 20, 0, 20)  # Margen superior e inferior
            )
        )

        self.page.add(botones)
        self.page.update()

    def cerrar(self, e):
        '''Función que se llama al presionar el botón "Salir" y cierra la ventana.'''
        self.page.window_close()

    def ir_a_insersiones(self, e):
        '''Función que se llama al presionar el botón "Insertar Datos" y abre la página "InsercionesView".'''
        from views import InsercionesView
        self.page.clean()  # Limpiar la página actual
        insersiones_view = InsercionesView(self.page)
        insersiones_view.build()

    def ir_a_leer(self, e):
        '''Función que se llama al presionar el botón "Leer Datos" y abre la página "LeerViews".'''
        from views import LeerViews
        self.page.clean()  # Limpiar la página actual
        submenu_view = LeerViews(self.page)
        submenu_view.build()

    def ir_a_modificaciones(self, e):
        '''Función que se llama al presionar el botón "Actualizar Datos" y abre la página "ModificarViews".'''
        from views import ModificarViews
        self.page.clean()  # Limpiar la página actual
        modificar_view = ModificarViews(self.page)
        modificar_view.build()

    def ir_a_eliminar(self, e):
        '''Función que se llama al presionar el botón "Eliminar Datos" y abre la página "EliminarViews".'''
        from views import DeleteView
        self.page.clean()  # Limpiar la página actual
        eliminar_view = DeleteView(self.page)
        eliminar_view.build()

    def ir_a_generacion_datos(self, e):
        '''Función que se llama al presionar el botón "Generar Datos" y muestra un cuadro de diálogo con dos respuestas.'''

        def opcion_si(e):
            #logica para la generación de datos:
            generar_datos()
            # Cerrar el diálogo
            question_dialog.close_dialog()

        def opcion_no(e):
            # Cerrar el diálogo
            question_dialog.close_dialog()

        # Crear el cuadro de diálogo de pregunta con dos respuestas
        question_dialog = QuestionDialog(
            titulo="Generar Datos",
            pregunta="¿Está seguro de que desea generar los datos?",
            respuesta_1="Sí",
            respuesta_2="No",
            page=self.page,
            respuesta_1_action=opcion_si,
            respuesta_2_action=opcion_no,
        )

        # Abrir el diálogo
        question_dialog.open_dialog()
