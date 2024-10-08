import requests
import logging
from app.models.inventario import Stock

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InventarioService:
    BASE_URL_COMPRAS = "http://localhost:5000/procesar_pago_y_guardar_compra"  # Cambia el puerto según corresponda

    @staticmethod
    def agregar_stock(producto_id, cantidad):
        try:
            nuevo_stock = Stock.agregar_stock(producto_id, cantidad)
            logger.info(f"Producto {producto_id} añadido al inventario. Cantidad: {cantidad}.")
            return nuevo_stock
        except Exception as e:
            logger.error(f"Error al añadir producto {producto_id} al inventario: {str(e)}")
            return None

    @staticmethod
    def retirar_producto(producto_id, cantidad):
        try:
            nuevo_stock = Stock.retirar_producto(producto_id, cantidad)
            logger.info(f"Producto {producto_id} retirado del inventario. Cantidad: {cantidad}.")
            return nuevo_stock
        except Exception as e:
            logger.error(f"Error al retirar producto {producto_id} del inventario: {str(e)}")
            return None

    @staticmethod
    def actualizar_stock(producto_id, cantidad, entrada_salida):
        """
        Actualiza el stock del producto, ya sea agregando (entrada_salida = 1) o retirando (entrada_salida = -1).
        """
        # Validar entradas
        if not isinstance(producto_id, int) or not isinstance(cantidad, int):
            logger.error(f"Datos de entrada no válidos: producto_id={producto_id}, cantidad={cantidad}")
            return None

        # Determinar si se agrega o se retira el stock
        if entrada_salida == 1:
            return InventarioService.agregar_stock(producto_id, cantidad)
        elif entrada_salida == -1:
            return InventarioService.retirar_producto(producto_id, cantidad)
        else:
            logger.error(f"Valor de entrada_salida no válido: {entrada_salida}")
            return None

    @staticmethod
    def actualizar_stock_despues_de_compra(producto_id, cantidad):
        """
        Actualiza el stock después de una compra llamando al microservicio de compras.
        """
        try:
            # Llamar al microservicio de compras para procesar la compra y luego actualizar el stock
            respuesta = requests.post(InventarioService.BASE_URL_COMPRAS, json={"producto_id": producto_id, "cantidad": cantidad})

            if respuesta.status_code == 200:
                return InventarioService.retirar_producto(producto_id, cantidad)
            else:
                logger.error("Error al actualizar el stock después de la compra: %s", respuesta.json())
                return None

        except requests.exceptions.RequestException as e:
            logger.error("Error al conectar con el microservicio de compras: %s", str(e))
            return None
