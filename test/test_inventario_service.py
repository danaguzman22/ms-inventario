import unittest
from unittest.mock import patch
from app.services.inventario_service import InventarioService
from app.models.inventario import Stock
import requests

class TestInventarioService(unittest.TestCase):
    inventario_service = InventarioService

    @patch('requests.post')
    @patch.object(Stock, 'retirar_producto')
    def test_actualizar_stock_exitoso(self, mock_retirar_producto, mock_post):
        # Configuración del mock para el servicio externo
        mock_post.return_value.status_code = 200

        # Configuración del mock para retirar producto
        mock_stock = Stock(producto_id=1, cantidad=10, entrada_salida=2)  # 2: salida (TransaccionTipo.SALIDA)
        mock_retirar_producto.return_value = mock_stock

        # Llamada al método que se está probando
        resultado = self.inventario_service.actualizar_stock_despues_de_compra(1, 10)

        # Aserciones para verificar el resultado esperado
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.producto_id, 1)
        self.assertEqual(resultado.cantidad, 10)

    @patch('requests.post')
    def test_actualizar_stock_fallo_actualizacion(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json = lambda: {"error": "Invalid stock update"}

        resultado = self.inventario_service.actualizar_stock_despues_de_compra(1, 10)

        self.assertIsNone(resultado)

    @patch('requests.post')
    def test_actualizar_stock_error_conexion(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Error de conexión")

        resultado = self.inventario_service.actualizar_stock_despues_de_compra(1, 10)

        self.assertIsNone(resultado)

    def test_actualizar_stock_invalid_input(self):
        resultado = self.inventario_service.actualizar_stock_despues_de_compra("invalid_id", "invalid_amount")
        self.assertIsNone(resultado)

if __name__ == "__main__":
    unittest.main()
