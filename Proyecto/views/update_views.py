import flet as ft
from services.crud_operations import read_data, update_data
from utils.style import button_style  # Importar los estilos

class ModificarViews:
    def __init__(self, page):
        '''Constructor de la clase'''
        self.page = page
        self.collection_name = ""  # Nombre de la colección seleccionada

    def build(self):
        '''Método que construye la página Modificar'''
        self.page.title = "Modificar"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.update()

        botones_fields = ft.Column(visible=True)
        buscar_fields = ft.Column(visible=False)
        formulario_fields = ft.Column(visible=False)

        def seleccionar_tipo(tipo):
            '''Método para seleccionar el tipo de búsqueda y mostrar el formulario de búsqueda'''
            self.collection_name = tipo
            botones_fields.visible = False
            buscar_fields.visible = True
            formulario_fields.visible = False

            buscar_fields.controls = [
                ft.TextField(
                    label="DNI" if tipo in ["pacientes", "medicos"] else "Numero de Cita",
                    width=300,
                    on_submit=lambda e: buscar_registro(e.control.value),
                    color=ft.Colors.BLACK,
                ),
                ft.ElevatedButton(
                    text="Buscar",
                    style=button_style,
                    width=300,
                    height=50,
                    on_click=lambda e: buscar_registro(buscar_fields.controls[0].value),
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

        def buscar_registro(identificador):
            '''Método para buscar un registro específico'''
            try:
                if not identificador:
                    buscar_fields.controls.append(
                        ft.Text("Por favor, ingrese un identificador válido.", color=ft.colors.RED)
                    )
                    self.page.update()
                    return

                datos = read_data(self.collection_name)
                filtro = None
                if self.collection_name in ["pacientes", "medicos"]:
                    filtro = next((fila for fila in datos if str(fila.get("DNI", "")) == identificador), None)
                elif self.collection_name == "citas":
                    filtro = next((fila for fila in datos if str(fila.get("nro_cita", "")) == identificador), None)

                if filtro:
                    mostrar_formulario([filtro], list(filtro.keys()))
                else:
                    buscar_fields.controls.append(
                        ft.Text("No se encontró ningún registro con ese identificador.", color=ft.colors.RED)
                    )
                self.page.update()

            except Exception as e:
                buscar_fields.controls.append(
                    ft.Text(f"Error al buscar el registro: {str(e)}", color=ft.colors.RED)
                )
                self.page.update()

        def mostrar_formulario(filas, columnas):
            '''Método para mostrar el formulario de modificación'''
            buscar_fields.visible = False
            formulario_fields.visible = True

            inputs = {}; id_oculto = {} #Inicializamos listas que se usaran para el guardado

            for col in columnas: #Se crea el formulario obteniendo los datos dinamicamente de la BD. No se muestra ni el nro_cita ni el DNI
                if col not in ["_id", "DNI", "nro_cita"]:
                    value = str(filas[0].get(col, ""))
                    inputs[col] = ft.TextField(label=col, value=value, width=300)
                elif col == "DNI":
                    id_oculto["DNI"] = filas[0].get("DNI", "")
                elif col == "nro_cita":
                    id_oculto["nro_cita"] = filas[0].get("nro_cita", "")

            formulario_fields.controls = [
                *inputs.values(),
                ft.ElevatedButton(
                    text="Guardar Cambios",
                    width=300,
                    height=50,
                    on_click=lambda e: guardar_cambios(inputs, id_oculto),
                    style=button_style
                ),
                ft.ElevatedButton(
                    text="Cancelar",
                    width=300,
                    height=50,
                    on_click=volver_a_menu_principal,
                    style=button_style
                ),
            ]
            self.page.update()

        def guardar_cambios(inputs, filtro):
            from utils import validar_telefono, validar_email, validar_edad
            from views import AlertView
            from services import  get_dni
            '''Método para guardar los cambios realizados'''
            try:
                # Obtener los valores del formulario
                nuevos_datos = {key: field.value for key, field in inputs.items()}
                print (self.collection_name)
                print(filtro)
                print(nuevos_datos)

                if self.collection_name == 'pacientes':
                    if not validar_edad(nuevos_datos['edad']):
                        alerta = AlertView(
                            titulo="Error",
                            mensaje=f"La edad debe ser un número entero.",
                            page=self.page,
                        )
                        alerta.open_dialog()
                        return

                if self.collection_name == 'pacientes' or self.collection_name == 'medicos':
                    # validaciones
                    if not validar_telefono(nuevos_datos["telefono"]):
                        alerta = AlertView(
                            titulo="Error",
                            mensaje=f"El telefono debe contener 9 digitos.",
                            page=self.page,
                        )
                        alerta.open_dialog()
                        return
                    if not validar_email(nuevos_datos["email"]):
                        alerta = AlertView(
                            titulo="Error",
                            mensaje=f"El correo electronico debe tener un formato válido.",
                            page=self.page,
                        )
                        alerta.open_dialog()
                        return
                    
                if self.collection_name == 'citas':
                    if not get_dni('pacientes', nuevos_datos['id_paciente']):
                        alerta = AlertView(
                            titulo="Error",
                            mensaje=f"No se encuentra un paciente con DNI {nuevos_datos['id_paciente']}.",
                            page=self.page,
                        )
                        alerta.open_dialog()
                        return
                    
                    if not get_dni('medicos', nuevos_datos['id_medico']):
                        alerta = AlertView(
                            titulo="Error",
                            mensaje=f"No se encuentra un médico con DNI {nuevos_datos['id_medico']}.",
                            page=self.page,
                        )
                        alerta.open_dialog()
                        return
                            

                
                # Llamar a update_data para realizar la actualización
                update_data(self.collection_name, filtro, nuevos_datos)

                # Mostrar mensaje de éxito
                formulario_fields.controls = [
                    ft.Text("Cambios guardados con éxito.", color=ft.colors.GREEN),
                    ft.ElevatedButton(
                        text="Volver",
                        width=300,
                        height=50,
                        style=button_style,
                        on_click=volver_a_menu_principal,
                    ),
                ]

            except Exception as e:
                # Mostrar mensaje de error
                formulario_fields.controls = [
                    ft.Text(f"Error al guardar cambios: {str(e)}", color=ft.colors.RED),
                    ft.ElevatedButton(
                        text="Volver",
                        width=300,
                        height=50,
                        on_click=volver_a_menu_principal,
                    ),
                ]
            self.page.update()

        def volver_a_menu_principal(e=None):
            '''Método para volver al menú principal'''
            botones_fields.visible = True
            buscar_fields.visible = False
            formulario_fields.visible = False
            self.page.update()

        def ir_a_main(e):
            from views import MainView
            # Limpiar la página actual
            self.page.clean()

            # Crear una instancia de MainView y construirla
            main_view = MainView(self.page)
            main_view.build()
            
        botones_fields.controls = [
            ft.ElevatedButton(
                text="Paciente",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: seleccionar_tipo("pacientes"),
            ),
            ft.ElevatedButton(
                text="Médico",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: seleccionar_tipo("medicos"),
            ),
            ft.ElevatedButton(
                text="Cita",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: seleccionar_tipo("citas"),
            ),
            ft.ElevatedButton(
                text="Volver",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: ir_a_main("Volver"),
            )
        ]

        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[botones_fields, buscar_fields, formulario_fields],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=20,
            )
        )
