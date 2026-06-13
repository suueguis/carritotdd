# carrito.py refactorizado
class Carrito:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, nombre, cantidad, precio):
        self.productos.append({
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio
        })

    def calcular_total(self):
        return sum(prod["precio"] * prod["cantidad"] for prod in self.productos)

    def eliminar_producto(self, nombre_producto):
        self.productos = [p for p in self.productos if p["nombre"] != nombre_producto]

    def aplicar_descuento(self, porcentaje):
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        total = self.calcular_total()
        return total - (total * porcentaje / 100)
