# views/add_product_dialog.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox,
    QMessageBox
)


class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar nuevo producto")
        self.setModal(True)
        # Fija un tamaño específico (opcional)
        self.setFixedSize(500, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        # Campos obligatorios
        self.codigo_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.marca_input = QLineEdit()
        self.ubicacion_input = QLineEdit()
        self.stock_input = QLineEdit()
        self.precio_compra_input = QLineEdit()
        self.precio_venta_input = QLineEdit()

        # Campo para Descuento (entero)
        self.descuento_input = QLineEdit()

        # NOTA: PrexDesc no se ingresa manualmente, se calculará automáticamente
        #       así que no lo incluimos en el formulario.

        # Agregamos al formulario (marcando con asterisco los obligatorios)
        form_layout.addRow("Código*:", self.codigo_input)
        form_layout.addRow("Nombre*:", self.nombre_input)
        form_layout.addRow("Marca*:", self.marca_input)
        form_layout.addRow("Descuento* (entero):", self.descuento_input)
        form_layout.addRow("Ubicación*:", self.ubicacion_input)
        form_layout.addRow("Stock* (entero):", self.stock_input)
        form_layout.addRow("Precio Compra* (float):", self.precio_compra_input)
        form_layout.addRow("Precio Venta* (float):", self.precio_venta_input)

        layout.addLayout(form_layout)

        # Botones OK y Cancel
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def accept(self):
        """
        Valida que los campos obligatorios no estén vacíos y que los numéricos sean válidos.
        El campo 'Descuento' es opcional.
        """
        if (not self.codigo_input.text().strip() or
                not self.nombre_input.text().strip() or
                not self.marca_input.text().strip() or
                not self.ubicacion_input.text().strip() or
                not self.stock_input.text().strip() or
                not self.precio_compra_input.text().strip() or
                not self.precio_venta_input.text().strip()):
            QMessageBox.warning(self, "Campos obligatorios", "Por favor, complete todos los campos obligatorios.")
            return

        try:
            int(self.stock_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "El campo 'Stock' debe ser un número entero.")
            return

        # El campo 'Descuento' es opcional; si se ingresa, debe ser entero
        discount_text = self.descuento_input.text().strip()
        if discount_text:
            try:
                int(discount_text)
            except ValueError:
                QMessageBox.warning(self, "Valor inválido",
                                    "El campo 'Descuento' debe ser un número entero si se proporciona.")
                return

        try:
            float(self.precio_compra_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "El campo 'Precio Compra' debe ser un número flotante.")
            return

        try:
            float(self.precio_venta_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Valor inválido", "El campo 'Precio Venta' debe ser un número flotante.")
            return

        super().accept()

    def get_data(self):
        """
        Retorna un diccionario con los datos ingresados,
        convirtiendo a mayúsculas los campos de texto.
        Calcula PrexDesc = Precio_Venta * (100 - Descuento) / 100.
        Si el campo 'Descuento' está vacío, se toma como 0.
        """
        codigo = self.codigo_input.text().strip().upper()
        nombre = self.nombre_input.text().strip().upper()
        marca = self.marca_input.text().strip().upper()
        ubicacion = self.ubicacion_input.text().strip().upper()

        # Si el campo 'Descuento' está vacío, se asigna 0; sino, se convierte a entero
        discount_text = self.descuento_input.text().strip()
        descuento = int(discount_text) if discount_text else 0

        stock = int(self.stock_input.text().strip())
        precio_compra = float(self.precio_compra_input.text().strip())
        precio_venta = float(self.precio_venta_input.text().strip())

        # Calcular PrexDesc aplicando el descuento porcentual
        prexdesc = precio_venta * (100 - descuento) / 100.0

        return {
            "Codigo": codigo,
            "Nombre": nombre,
            "Marca": marca,
            "Descuento": descuento,
            "PrexDesc": prexdesc,
            "Ubicacion": ubicacion,
            "Stock": stock,
            "Precio_Compra": precio_compra,
            "Precio_Venta": precio_venta
        }
