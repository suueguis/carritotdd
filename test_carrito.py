# test_carrito.py
import unittest
from carrito import Carrito

class TestCarritoCompras(unittest.TestCase):
    
    def test_calcular_total_carrito(self):
        # Preparar el escenario (Arrange)
        carrito = Carrito()
        carrito.productos = [
            {"nombre": "Camisa", "cantidad": 2, "precio": 50000}, # 100,000
            {"nombre": "Zapatos", "cantidad": 1, "precio": 120000} # 120,000
        ]
        
        # Actuar (Act)
        total = carrito.calcular_total()
        
        # Verificar (Assert)
        self.assertEqual(total, 220000)

    def test_eliminar_producto_por_nombre(self):
        carrito = Carrito()
        carrito.productos = [
            {"nombre": "Camisa", "cantidad": 2, "precio": 50000},
            {"nombre": "Zapatos", "cantidad": 1, "precio": 120000}
        ]
        
        # Intentamos eliminar las Camisas
        carrito.eliminar_producto("Camisa")
        
        # Verificamos que solo quede 1 tipo de producto y que NO sea Camisa
        self.assertEqual(len(carrito.productos), 1)
        self.assertEqual(carrito.productos[0]["nombre"], "Zapatos")

if __name__ == '__main__':
    unittest.main()