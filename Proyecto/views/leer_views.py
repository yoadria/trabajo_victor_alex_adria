import flet as ft
from services.crud_operations import read_data
from utils.style import button_style, estilo_encabezado, estilo_celda, estilo_tabla

class LeerViews:
    def __init__(self, page):
        '''Constructor de la clase'''
        self.page = page
        self.collection_name = ""  # Nombre de la colección seleccionada

    def build(self):
        '''Método que construye la página Leer'''
        self.page.title = "Leer"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Detectar el tamaño de la pantalla
        def ajustar_vista_por_tamaño():
            if self.page.window_width < 600:  # Pantallas pequeñas (móviles)
                return {
                    "scroll_mode": ft.ScrollMode.AUTO,  # Desplazamiento automatico
                    "tabla_width": "100%",
                    "tabla_height": 700,
                    "fuente_celda": 12,
                    "vista": "tarjetas"
                }
            else:  # Pantallas grandes (escritorio)
                return {
                    "scroll_mode": ft.ScrollMode.AUTO,  # Desplazamiento automático
                    "tabla_width": 1000,
                    "tabla_height": 700,
                    "fuente_celda": 14,
                    "vista": "tabla"
                }

        ajustes = ajustar_vista_por_tamaño()

        botones_fields = ft.Column(visible=True)
        tabla_fields = ft.Column(visible=False)

        def mostrar_campos(tipo):
            '''Método para mostrar los datos dinámicamente según la colección seleccionada'''
            self.collection_name = tipo
            botones_fields.visible = False
            tabla_fields.visible = True

            try:
                # Obtener datos de la colección utilizando crud_operations
                datos = read_data(self.collection_name)
                
                # Si hay datos, filtramos el campo '_id' de las columnas y filas
                if datos:
                    # Obtener las columnas sin incluir '_id' y reemplazar "nro_citas" por "numero citas"

                    # columnas = [("numero citas" if col == "nro_cita" else col) for col in datos[0].keys() if col != "_id"]
                    columnas = [
                        "numero citas" if col == "nro_cita" else 
                        "DNI paciente" if col == "id_paciente" else
                        "DNI medico" if col == "id_medico" else 
                        col 
                        for col in datos[0].keys() if col != "_id"
                    ]

                    # Obtener las filas sin incluir '_id'
                    filas = []
                    for row in datos:
                        fila_filtrada = {}
                        for key, value in row.items():
                            if key != "_id":
                                fila_filtrada[key] = value

                        filas.append(fila_filtrada)
                    
                    # Mostrar los datos en formato de tabla o tarjetas
                    if ajustes["vista"] == "tabla":
                        
                        tabla = estilo_tabla(
                            columns=[estilo_encabezado(col) for col in columnas],
                            rows=[ft.DataRow(cells=[
                                estilo_celda(
                                    str(fila[
                                        "nro_cita" if col == "numero citas" else
                                        "id_paciente" if col == "DNI paciente" else
                                        "id_medico" if col == "DNI medico" else
                                        col
                                    ]), 
                                    ajustes["fuente_celda"]
                                ) for col in columnas
                            ]) for fila in filas]
                        )

                        # Aplicar el estilo de la tabla
                        tabla_fields.controls = [
                            ft.Container(
                                content=ft.Column(
                                    controls=[tabla],
                                    scroll=ajustes["scroll_mode"],  # Desplazamiento automático si es necesario
                                    height=ajustes["tabla_height"],  # Ajustamos la altura de la tabla
                                    width=ajustes["tabla_width"],  # Ancho de la tabla
                                    alignment=ft.MainAxisAlignment.CENTER,  # Centrado de la tabla
                                ),
                            ),
                            ft.ElevatedButton(
                                text="Volver",
                                style=button_style,
                                width=1000,
                                height=50,
                                on_click=volver_a_menu_principal, # Conectar botón "Volver"
                            )
                        ]
                    elif ajustes["vista"] == "tarjetas":
                        # Crear tarjetas con los datos filtrados y aplicar el color de fondo azul gris
                        
                        # tarjetas = [
                        #     ft.Card(
                        #         content=ft.Container(
                        #             content=ft.Column(
                        #                 controls=[ft.Text(f"{'numero citas' if key == 'nro_cita' else key}: {value}", size=ajustes["fuente_celda"], color=ft.colors.BLACK) for key, value in fila.items()],
                        #                 spacing=5
                        #             ),
                        #             bgcolor=ft.colors.BLUE_GREY_200,  # Color de fondo de las tarjetas
                        #             width=300,  # Ancho fijo para todas las tarjetas

                        #             height=200,  # Altura fija para todas las tarjetas
                        #             border_radius=15,  # Bordes redondeados
                        #             padding=10  # Espaciado interno para contenido
                        #         ),
                        #         elevation=2
                        #     ) for fila in filas
                        # ]


                        tarjetas = [
                            ft.Card(
                                content=ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text(
                                                f"{
                                                    'numero citas' if key == 'nro_cita' else
                                                    'DNI paciente' if key == 'id_paciente' else
                                                    'DNI medico' if key == 'id_medico' else
                                                    key
                                                }: {value}", 
                                                size=ajustes["fuente_celda"], 
                                                color=ft.colors.BLACK
                                            ) for key, value in fila.items()
                                        ],
                                        spacing=5
                                    ),
                                    bgcolor=ft.colors.BLUE_GREY_200,
                                    width=300,
                                    height=200,
                                    border_radius=15,
                                    padding=10
                                ),
                                elevation=2
                            ) for fila in filas
                        ]

                        tabla_fields.controls = [
                            ft.Container(
                                content=ft.Column(
                                    controls=tarjetas,
                                    scroll=ajustes["scroll_mode"],
                                    spacing=10
                                ),
                                width="100%",
                                height=ajustes["tabla_height"]
                            ),
                            ft.ElevatedButton(
                                text="Volver",
                                style=button_style,
                                width=300,
                                height=50,
                                on_click=volver_a_menu_principal
                            )
                        ]
                else:
                    tabla_fields.controls = [
                        ft.Text("No hay datos disponibles.", color=ft.colors.RED),
                        ft.ElevatedButton(
                            text="Volver",
                            style=button_style,
                            width=300,
                            height=50,
                            on_click=volver_a_menu_principal
                        )
                    ]
            
            except Exception as e:
                tabla_fields.controls = [
                    ft.Text(f"Error al cargar los datos: {str(e)}", color=ft.colors.RED),
                    ft.ElevatedButton(
                        text="Volver",
                        style=button_style,
                        width=300,
                        height=50,
                        on_click=volver_a_menu_principal
                    )
                ]

            self.page.update()

        def volver_a_menu_principal(e):
            '''Método para volver al menú principal'''
            botones_fields.visible = True
            tabla_fields.visible = False
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
                on_click=lambda e: mostrar_campos("pacientes"),
            ),
            ft.ElevatedButton(
                text="Médico",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: mostrar_campos("medicos"),
            ),
            ft.ElevatedButton(
                text="Cita",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: mostrar_campos("citas"),
            ),
            ft.ElevatedButton(
                text="Volver",
                style=button_style,
                width=300,
                height=50,
                on_click=lambda e: ir_a_main("Volver"),
            )
        ]

        # Agregar los botones y la tabla dinámica a la página
        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[botones_fields, tabla_fields],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centrado vertical
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centrado horizontal
                    spacing=20,
                ),
                padding=20,
            )
        )
