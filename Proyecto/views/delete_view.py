import flet as ft
from utils.style import button_style
from services.crud_operations import read_data, delete_data

class DeleteView:
    def __init__(self, page):
        self.page = page

    def build(self):
        self.page.title = "Eliminar"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.update()

        botones_fields = ft.Column(visible=True)
        buscar_fields = ft.Column(visible=False)
        formulario_fields = ft.Column(visible=False)

        def seleccionar_tipo(tipo):
            botones_fields.visible = False
            buscar_fields.visible = True
            formulario_fields.visible = False

            buscar_fields.controls = [
                ft.TextField(
                    label="DNI" if tipo in ["Pacientes", "Medicos"] else "Número de Cita",
                    width=300,
                    on_submit=lambda e: buscar_registro(tipo, e.control.value),
                ),
                ft.ElevatedButton(
                    text="Buscar",
                    style=button_style,
                    width=300,
                    height=50,
                    on_click=lambda e: buscar_registro(tipo, buscar_fields.controls[0].value),
                ),
                ft.ElevatedButton(
                    text="Volver",
                    style=button_style,
                    width=300,
                    height=50,
                    on_click=volver_a_menu_principal,
                ),
            ]
            self.page.update()

        def buscar_registro(tipo, valor):
            """Busca un registro en la base de datos y muestra un mensaje de error si no se encuentra."""
            try:
                if tipo == "Pacientes":
                    filtro = {"DNI": valor}
                elif tipo == "Medicos":
                    filtro = {"DNI": valor}
                elif tipo == "Citas":
                    filtro = {"nro_cita": valor}
                else:
                    raise ValueError("Tipo de búsqueda no válido.")

                resultado = read_data(tipo.lower())
                registro = next((doc for doc in resultado if filtro.items() <= doc.items()), None)

                if not registro:
                    raise Exception("No se encontró ningún registro con el valor proporcionado.")
                
                mostrar_formulario(tipo, registro)

            except Exception as e:
                dialogo = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text(str(e)),
                    actions=[
                        ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialogo))
                    ]
                )
                self.page.dialog = dialogo
                dialogo.open = True
                self.page.update()

        def mostrar_formulario(tipo, registro):
            buscar_fields.visible = False
            formulario_fields.visible = True

            formulario_fields.controls = []
            if tipo == "Citas":
                formulario_fields.controls.extend([
                    ft.TextField(label="Número de Cita", value=str(registro.get("nro_cita", "N/A")), width=300, read_only=True),
                    ft.TextField(label="Fecha", value=str(registro.get("fecha", "N/A")), width=300, read_only=True),
                ])
            else:  # Pacientes o Médicos
                formulario_fields.controls.extend([
                    ft.TextField(label="Nombre", value=registro.get("nombre", "N/A"), width=300, read_only=True),
                    ft.TextField(label="DNI", value=registro.get("DNI", "N/A"), width=300, read_only=True),
                ])
            formulario_fields.controls.extend([
                ft.ElevatedButton(
                    text="Eliminar",
                    style=button_style,
                    width=300,
                    height=50,
                    on_click=lambda e: confirmar_eliminacion(tipo, registro),
                ),
                ft.ElevatedButton(
                    text="Cancelar",
                    style=button_style,
                    width=300,
                    height=50,
                    on_click=volver_a_menu_principal,
                ),
            ])
            self.page.update()

        def confirmar_eliminacion(tipo, registro):
            dialogo = ft.AlertDialog(
                title=ft.Text("Confirmación"),
                content=ft.Text(f"¿Está seguro que desea eliminar el registro?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dialogo)),
                    ft.TextButton("Confirmar", on_click=lambda e: eliminar_registro(tipo, registro, dialogo)),
                ]
            )
            self.page.dialog = dialogo
            dialogo.open = True
            self.page.update()

        def eliminar_registro(tipo, registro, dialogo):
            try:
                collection_name = tipo.lower()
                query_filter = {"DNI": registro["DNI"]} if "DNI" in registro else {"nro_cita": registro["nro_cita"]}

                resultado = delete_data(collection_name, query_filter)
                cerrar_dialogo(dialogo)
                mostrar_exito(resultado["data"])
            except Exception as e:
                cerrar_dialogo(dialogo)
                dialogo_error = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text(str(e)),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(dialogo_error))],
                )
                self.page.dialog = dialogo_error
                dialogo_error.open = True
                self.page.update()

        def mostrar_exito(registro):
            formulario_fields.controls = [
                ft.Text(f"Registro eliminado: {registro.get('nombre', 'N/A')} ({registro.get('DNI', registro.get('nro_cita', 'N/A'))}).", color=ft.colors.GREEN),
                ft.ElevatedButton(
                    text="Volver",
                    style=button_style,
                    width=300,
                    height=50,
                    on_click=volver_a_menu_principal,
                ),
            ]
            self.page.update()

        def cerrar_dialogo(dialogo):
            dialogo.open = False
            self.page.update()

        def volver_a_menu_principal(e=None):
            botones_fields.visible = True
            buscar_fields.visible = False
            formulario_fields.visible = False
            self.page.update()

        botones_fields.controls = [
            ft.ElevatedButton(
                text="Paciente",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: seleccionar_tipo("Pacientes"),
            ),
            ft.ElevatedButton(
                text="Médico",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: seleccionar_tipo("Medicos"),
            ),
            ft.ElevatedButton(
                text="Cita",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: seleccionar_tipo("Citas"),
            ),
            ft.ElevatedButton(
                text="Volver",
                style=button_style,
                width=300,
                height=50,
                on_click=self.ir_a_main,
            )
        ]

        self.page.add(ft.Container(
            content=ft.Column(
                controls=[botones_fields, buscar_fields, formulario_fields],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=20,
        ))

    def ir_a_main(self, e):
        from views import MainView

        self.page.clean()
        main_view = MainView(self.page)
        main_view.build()
