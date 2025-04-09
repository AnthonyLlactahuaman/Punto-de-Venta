from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from config.config import (
    ICON_LOGO, ICON_TIENDA, ICON_INVENTARIO, ICON_VENTAS,
    ICON_COMPRAS, ICON_SUNAT, ICON_GRAFICOS
)
from utils.supabase_client import supabase


class InventarioView(QMainWindow):
    def __init__(self, user_role: str = "vendedor"):
        """
        :param user_role: Rol del usuario logeado ("admin" o "vendedor").
        """
        super().__init__()
        self.user_role = user_role
        self.setWindowTitle("Inventario - LlactaSoft")
        # Se define un tamaño inicial, pero la ventana será redimensionable.
        self.resize(1200, 750)

        # Almacenar datos completos para filtrar
        self.full_data = []

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal horizontal: menú lateral + contenido
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Se crea el menú lateral (ancho fijo de 75px)
        self.create_side_menu()

        # Crear el área de contenido principal y agregarla con factor de estiramiento 1
        self.create_content_area()

        # Cargar datos de inventario desde Supabase
        self.load_inventory_data()

    # ==================== MENÚ LATERAL ====================
    def create_side_menu(self):
        menu_widget = QWidget()
        # Limitar el ancho del menú a 75px
        menu_widget.setMinimumWidth(75)
        menu_widget.setMaximumWidth(75)
        menu_layout = QVBoxLayout(menu_widget)
        menu_widget.setStyleSheet("background-color: #2F3A56;")
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)

        # Espacio fijo de 20px en la parte superior (opcional)
        spacer1 = QWidget()
        spacer1.setFixedHeight(20)
        menu_layout.addWidget(spacer1)

        # Logo del menú, pegado en la parte superior
        logo_label = QLabel()
        logo_label.setPixmap(QIcon(ICON_LOGO).pixmap(QSize(64, 64)))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(logo_label)

        # Espacio fijo de 60px entre el logo y los iconos
        spacer2 = QWidget()
        spacer2.setFixedHeight(60)
        menu_layout.addWidget(spacer2)

        # Contenedor para los botones (iconos)
        icons_container = QWidget()
        icons_layout = QVBoxLayout(icons_container)
        icons_layout.setContentsMargins(0, 0, 0, 80)
        icons_layout.setSpacing(0)

        # Primer botón: Tienda (pegado a la parte superior del contenedor)
        self.btn_tienda = QPushButton()
        self.btn_tienda.setIcon(QIcon(ICON_TIENDA))
        self.btn_tienda.setIconSize(QSize(32, 32))
        self.btn_tienda.setStyleSheet("border: none;")
        self.btn_tienda.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_tienda.setVisible(True)
        icons_layout.addWidget(self.btn_tienda)

        # Agregar el resto de botones, distribuidos equitativamente
        self.btn_inventario = QPushButton()
        self.btn_inventario.setIcon(QIcon(ICON_INVENTARIO))
        self.btn_inventario.setIconSize(QSize(32, 32))
        self.btn_inventario.setStyleSheet("border: none;")
        self.btn_inventario.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_inventario.setVisible(True)
        icons_layout.addStretch(1)
        icons_layout.addWidget(self.btn_inventario)

        self.btn_ventas = QPushButton()
        self.btn_ventas.setIcon(QIcon(ICON_VENTAS))
        self.btn_ventas.setIconSize(QSize(32, 32))
        self.btn_ventas.setStyleSheet("border: none;")
        self.btn_ventas.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ventas.setVisible(self.user_role == "admin")
        icons_layout.addStretch(1)
        icons_layout.addWidget(self.btn_ventas)

        self.btn_compras = QPushButton()
        self.btn_compras.setIcon(QIcon(ICON_COMPRAS))
        self.btn_compras.setIconSize(QSize(32, 32))
        self.btn_compras.setStyleSheet("border: none;")
        self.btn_compras.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_compras.setVisible(self.user_role == "admin")
        icons_layout.addStretch(1)
        icons_layout.addWidget(self.btn_compras)

        self.btn_sunat = QPushButton()
        self.btn_sunat.setIcon(QIcon(ICON_SUNAT))
        self.btn_sunat.setIconSize(QSize(32, 32))
        self.btn_sunat.setStyleSheet("border: none;")
        self.btn_sunat.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_sunat.setVisible(self.user_role == "admin")
        icons_layout.addStretch(1)
        icons_layout.addWidget(self.btn_sunat)

        self.btn_graficos = QPushButton()
        self.btn_graficos.setIcon(QIcon(ICON_GRAFICOS))
        self.btn_graficos.setIconSize(QSize(32, 32))
        self.btn_graficos.setStyleSheet("border: none;")
        self.btn_graficos.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_graficos.setVisible(self.user_role == "admin")
        icons_layout.addStretch(1)
        icons_layout.addWidget(self.btn_graficos)
        # No se añade stretch después del último botón, para que quede pegado al fondo

        menu_layout.addWidget(icons_container)
        # Agregar el menú lateral al layout principal sin factor de estiramiento
        self.main_layout.addWidget(menu_widget)

    # ==================== ÁREA DE CONTENIDO ====================
    def create_content_area(self):
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Sección 1: Barra superior con el título "Inventario"
        top_bar = self.create_top_bar()
        content_layout.addWidget(top_bar)

        # Sección 2: Filtros y tabla
        filters_table = self.create_filters_and_table()
        content_layout.addWidget(filters_table)

        # Sección 3: Botones (Agregar producto, Editar producto, Eliminar producto, Cargar Excel)
        buttons_bar = self.create_buttons_bar()
        content_layout.addWidget(buttons_bar)

        # Agregar el área de contenido al layout principal con factor de estiramiento 1
        self.main_layout.addWidget(content_widget, 1)

    def create_top_bar(self):
        """Crea la barra superior con el título 'Inventario'."""
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(10, 0, 0, 0)
        top_bar.setMinimumHeight(60)
        top_bar.setStyleSheet("background-color: #406D96;")
        inventario_label = QLabel("Inventario")
        inventario_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        top_bar_layout.addWidget(inventario_label)
        top_bar_layout.addStretch()
        return top_bar

    def create_filters_and_table(self):
        """
        Crea el área de filtros y la tabla.
        Los filtros (por nombre, código y marca) actualizan la tabla automáticamente al escribir.
        La tabla tiene barra de desplazamiento horizontal y vertical cuando es necesario.
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Filtros: Se crean 3 QLineEdit
        filter_bar = QWidget()
        filter_bar_layout = QHBoxLayout(filter_bar)
        filter_bar_layout.setContentsMargins(0, 5, 0, 5)

        self.filter_nombre = QLineEdit()
        self.filter_nombre.setPlaceholderText("Filtro por nombre")
        self.filter_codigo = QLineEdit()
        self.filter_codigo.setPlaceholderText("Filtro por código")
        self.filter_marca = QLineEdit()
        self.filter_marca.setPlaceholderText("Filtro por marca")

        filter_bar_layout.addWidget(self.filter_nombre)
        filter_bar_layout.addWidget(self.filter_codigo)
        filter_bar_layout.addWidget(self.filter_marca)

        layout.addWidget(filter_bar)

        # Conectar la señal textChanged de cada filtro para actualizar la tabla
        self.filter_nombre.textChanged.connect(self.filter_table)
        self.filter_codigo.textChanged.connect(self.filter_table)
        self.filter_marca.textChanged.connect(self.filter_table)

        # Tabla para mostrar datos
        self.table = QTableWidget()
        # Actualizamos el número de columnas y encabezados para mostrar todos los campos
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Código",
            "Nombre",
            "Marca",
            "Desc.",
            "Prec/Desc",
            "Ubicación",
            "Stock",
            "PrecioCompra",
            "PrecioVenta"
        ])

        # Permitir el desplazamiento horizontal si el contenido excede el ancho
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # Para que el usuario pueda ajustar manualmente el tamaño de cada columna
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        layout.addWidget(self.table)
        return widget

    def create_buttons_bar(self):
        """
        Crea la barra con los botones:
        - Agregar producto
        - Editar producto
        - Eliminar producto
        - Cargar Excel
        Cada botón llama a su función respectiva.
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Definir tamaño fijo para los botones
        button_width = 200
        button_height = 50

        self.btn_add_product = QPushButton("Agregar producto")
        self.btn_add_product.setStyleSheet("background-color: #406D96; color: white; font-weight: bold;")
        self.btn_add_product.clicked.connect(self.add_product)
        self.btn_add_product.setFixedSize(button_width, button_height)

        self.btn_edit_product = QPushButton("Editar producto")
        self.btn_edit_product.setStyleSheet("background-color: #406D96; color: white; font-weight: bold;")
        self.btn_edit_product.clicked.connect(self.edit_product)
        self.btn_edit_product.setFixedSize(button_width, button_height)

        self.btn_delete_product = QPushButton("Eliminar producto")
        self.btn_delete_product.setStyleSheet("background-color: #406D96; color: white; font-weight: bold;")
        self.btn_delete_product.clicked.connect(self.delete_product)
        self.btn_delete_product.setFixedSize(button_width, button_height)

        self.btn_load_excel = QPushButton("Cargar Excel")
        self.btn_load_excel.setStyleSheet("background-color: #406D96; color: white; font-weight: bold;")
        self.btn_load_excel.clicked.connect(self.load_excel)
        self.btn_load_excel.setFixedSize(button_width, button_height)

        layout.addWidget(self.btn_add_product)
        layout.addWidget(self.btn_edit_product)
        layout.addWidget(self.btn_delete_product)
        layout.addWidget(self.btn_load_excel)
        layout.addStretch()

        return widget

    # ==================== FUNCIONES DE FILTRADO Y POBLADO DE TABLA ====================
    def load_inventory_data(self):
        """
        Carga los datos de la tabla "Inventario" de Supabase,
        almacena la información completa en self.full_data y
        los muestra en la tabla.
        """
        try:
            response = supabase.table("Inventario").select("*").execute()
            data = response.data  # Lista de diccionarios
            if not data:
                return
            self.full_data = data  # Guardamos todos los datos para poder filtrar
            self.populate_table(data)
        except Exception as e:
            print("Error cargando datos de inventario:", e)

    def populate_table(self, data):
        """Puebla la tabla con la lista de diccionarios 'data'."""
        self.table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            # Ajusta las claves según tus columnas en Supabase:
            codigo = row_data.get("Codigo", "")
            nombre = row_data.get("Nombre", "")
            marca = row_data.get("Marca", "")
            desc_ = row_data.get("Descuento", "")
            prec_desc = row_data.get("PrexDesc", "")
            ubicacion = row_data.get("Ubicacion", "")
            stock = row_data.get("Stock", "")
            precio_compra = row_data.get("Precio_Compra", "")
            precio_venta = row_data.get("Precio_Venta", "")

            self.table.setItem(row_index, 0, QTableWidgetItem(str(codigo)))
            self.table.setItem(row_index, 1, QTableWidgetItem(str(nombre)))
            self.table.setItem(row_index, 2, QTableWidgetItem(str(marca)))
            self.table.setItem(row_index, 3, QTableWidgetItem(str(desc_)))
            self.table.setItem(row_index, 4, QTableWidgetItem(str(prec_desc)))
            self.table.setItem(row_index, 5, QTableWidgetItem(str(ubicacion)))
            self.table.setItem(row_index, 6, QTableWidgetItem(str(stock)))
            self.table.setItem(row_index, 7, QTableWidgetItem(str(precio_compra)))
            self.table.setItem(row_index, 8, QTableWidgetItem(str(precio_venta)))

    def filter_table(self):
        """
        Filtra los datos de la tabla según los textos ingresados en los filtros
        (por nombre, código y marca) y actualiza la tabla.

        NOTA: Todos los valores en la BD están en mayúscula, así que convertimos
        el texto ingresado en el filtro a mayúscula antes de comparar.
        """
        # Convertimos el texto de los filtros a mayúscula
        nombre_filter = self.filter_nombre.text().upper()
        codigo_filter = self.filter_codigo.text().upper()
        marca_filter = self.filter_marca.text().upper()

        filtered_data = []
        for row in self.full_data:
            # Convertimos a mayúscula el valor en la BD para compararlo
            row_codigo = str(row.get("Codigo", "")).upper()
            row_nombre = str(row.get("Nombre", "")).upper()
            row_marca = str(row.get("Marca", "")).upper()

            if (codigo_filter in row_codigo and
                    nombre_filter in row_nombre and
                    marca_filter in row_marca):
                filtered_data.append(row)

        self.populate_table(filtered_data)

    # ==================== FUNCIONES DE LOS BOTONES ====================
    def add_product(self):
        """
        Abre un formulario emergente para agregar un nuevo producto.
        Si se aprueba, verifica que no exista un producto con el mismo Código y Marca,
        y si no existe, inserta el producto en la base de datos y recarga la tabla.
        """
        from PyQt6.QtWidgets import QDialog, QMessageBox
        from views.add_product_dialog import AddProductDialog
        from models.inventory import insert_product, check_product_exists

        dialog = AddProductDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            product_data = dialog.get_data()
            codigo = product_data["Codigo"]
            marca = product_data["Marca"]

            # Verificar si ya existe un producto con el mismo Código y Marca
            if check_product_exists(codigo, marca):
                QMessageBox.warning(self, "Producto existente",
                                    "Ya existe un producto con el mismo Código y Marca.")
            else:
                result = insert_product(product_data)
                if result is not None:
                    QMessageBox.information(self, "Producto agregado", "Producto agregado exitosamente.")
                    # Recargar los datos de inventario
                    self.load_inventory_data()
                else:
                    QMessageBox.warning(self, "Error", "Error al agregar el producto.")

    def edit_product(self):
        """Función para editar un producto de forma individual (a implementar)."""
        print("boton ejecutado (Editar producto)")

    def delete_product(self):
        """Función para eliminar un producto de forma individual (a implementar)."""
        print("boton ejecutado (Eliminar producto)")

    def load_excel(self):
        """Función para cargar productos mediante Excel (a implementar)."""
        print("boton ejecutado (Cargar Excel)")
