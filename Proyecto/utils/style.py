import flet as ft

# Estilo de los botones (color, bordes redondeados y tamaño)
button_style = ft.ButtonStyle(
    bgcolor="#FFA07A",
    color="black",
    overlay_color="#D35400",  # Color al hacer clic
    shape=ft.RoundedRectangleBorder(radius=10)  # Bordes redondeados
)

# Estilo del encabezado de las tablas
def estilo_encabezado(texto):
    """Crea un DataColumn con estilo de encabezado en negrita."""
    return ft.DataColumn(
        ft.Text(texto, weight="bold", color="black", size=16) # Encabezados en negrita
    )

# Estilo de las celdas de las tablas
def estilo_celda(texto, fuente_celda=14):
    """Crea un contenedor con estilo para una celda de la tabla."""
    return ft.DataCell(
        ft.Container(
            content=ft.Text(texto, color="black", size=fuente_celda),  # Se agrega el tamaño de la fuente
            alignment=ft.alignment.center  # Centra el texto
        )
    )


# Estilo para la tabla
def estilo_tabla(columns, rows):
    return ft.Container(
        content=ft.DataTable(
            columns=columns,
            rows=rows,
            vertical_lines=ft.BorderSide(3, "black"),  # Líneas verticales negras
            horizontal_lines=ft.BorderSide(3, "black"),  # Líneas horizontales negras
            divider_thickness=1,  # Grosor de las líneas divisorias
            heading_row_color=ft.colors.BLUE_GREY_200,  # Fondo azul para la fila de encabezado
            # data_row_color={"even": "#E8F6F3", "odd": "#D1F2EB"},  # Colores alternos en filas
            border=ft.border.all(1, "black"),  # Borde negro alrededor de la tabla
        ),
        border=ft.border.all(2, "black"),
        border_radius=8,  # Aplica el border_radius a toda la tabla
        padding=0  # Para evitar espacio adicional en el contenedor
    )

