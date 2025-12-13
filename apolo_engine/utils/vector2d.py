# -*- coding: utf-8 -*-
"""
Módulo Vector2D: Fornece uma classe para manipulação de vetores bidimensionais,
essencial para os sistemas de física e posicionamento.
"""
import math

class Vector2D:
    """
    Representa um vetor em um espaço 2D com operações matemáticas básicas.
    """
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Soma de vetores."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtração de vetores."""
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float):
        """Multiplicação por um escalar."""
        return Vector2D(self.x * scalar, self.y * scalar)

    @property
    def magnitude(self) -> float:
        """Calcula a magnitude (comprimento) do vetor."""
        return math.sqrt(self.x**2 + self.y**2)

    def normalizar(self):
        """Retorna o vetor unitário (magnitude 1)."""
        mag = self.magnitude
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)

    def __repr__(self):
        return f"Vector2D({self.x:.2f}, {self.y:.2f})"
