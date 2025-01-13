import flet as ft

class AlertView:
    def __init__(self, titulo: str, mensaje: str, page: ft.Page):
        """
        Args:
            titulo (str): Título del diálogo.
            mensaje (str): Mensaje del diálogo.
            page (ft.Page): Página donde se mostrará el diálogo.
        """
        self.page = page
        self.titulo = titulo
        self.mensaje = mensaje

        # Crear el diálogo al inicializar
        self.dialog = ft.AlertDialog(
            title=ft.Text(self.titulo, text_align=ft.TextAlign.CENTER),  # Título centrado
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            self.mensaje,
                            text_align=ft.TextAlign.CENTER,  # Texto centrado
                        ),
                        ft.Row(
                            controls=[ 
                                ft.ElevatedButton(
                                    "Cerrar",
                                    on_click=lambda e: self.close_dialog()
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,  # Botón alineado a la derecha
                        ),
                    ],
                    spacing=20,  # Espacio entre el texto y el botón
                ),
                width=400,
                height=80,
            )
        )
        self.page.dialog = self.dialog  # Asociar el diálogo a la página

    def open_dialog(self):
        """
        Abre el diálogo.
        """
        self.dialog.open = True
        self.page.update()

    def close_dialog(self):
        """
        Cierra el diálogo.
        """
        self.dialog.open = False
        self.page.update()


# Clase hija para manejar un cuadro de texto con una pregunta y dos posibles respuestas
class QuestionDialog(AlertView):
    def __init__(self, titulo: str, pregunta: str, respuesta_1: str, respuesta_2: str, page: ft.Page, respuesta_1_action, respuesta_2_action):
        """
        Clase que extiende de AlertView para mostrar una pregunta con dos posibles respuestas.
        
        Args:
            titulo (str): Título del diálogo.
            pregunta (str): La pregunta que se hará.
            respuesta_1 (str): Texto de la primera respuesta.
            respuesta_2 (str): Texto de la segunda respuesta.
            page (ft.Page): Página donde se mostrará el diálogo.
            respuesta_1_action (function): Acción que se ejecutará cuando se seleccione la primera respuesta.
            respuesta_2_action (function): Acción que se ejecutará cuando se seleccione la segunda respuesta.
        """
        # Inicializar la clase base (AlertView)
        super().__init__(titulo, pregunta, page)

        # Guardar las acciones de las respuestas
        self.respuesta_1_action = respuesta_1_action
        self.respuesta_2_action = respuesta_2_action

        # Crear el contenido del diálogo con las dos respuestas
        self.dialog.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        self.mensaje,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                respuesta_1, 
                                on_click=self.respuesta_1_action
                            ),
                            ft.ElevatedButton(
                                respuesta_2, 
                                on_click=self.respuesta_2_action
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Botones centrados
                        spacing=20,
                    ),
                ],
                spacing=20,
            ),
            width=400,
            height=150,
        )

    def open_dialog(self):
        """Abre el diálogo con las opciones de respuestas"""
        self.dialog.open = True
        self.page.update()

    def close_dialog(self):
        """Cierra el diálogo"""
        self.dialog.open = False
        self.page.update()
