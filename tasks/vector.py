from typing import List, Optional

def scalar_product(a: Optional[List[float]], b: Optional[List[float]]) -> float:
    """Вычисляет скалярное произведение двух векторов произвольной размерности."""
    # Проверяем, что векторы не равны None
    if a is None or b is None:
        raise ValueError("Один из векторов пуст или None")
    
    # Проверяем, что векторы одной размерности
    if len(a) != len(b):
        raise ValueError("Векторы должны быть одной размерности")
    
    # Возвращаем сумму произведений соответствующих элементов
    return sum(a[i] * b[i] for i in range(len(a)))

def length_vec(a: Optional[List[float]], b: Optional[List[float]]) -> float:
    """Вычисляет длину вектора между двумя точками a и b произвольной размерности."""
    # Проверяем, что обе точки не равны None
    if a is None or b is None:
        raise ValueError("Одна из точек пуста или None")
    
    # Проверяем, что точки одной размерности
    if len(a) != len(b):
        raise ValueError("Точки должны быть одной размерности")
    
    # Вычисляем длину вектора, используя формулу расстояния между двумя точками
    return (sum((b[i] - a[i]) ** 2 for i in range(len(a)))) ** 0.5

def cos_ab(a: Optional[List[float]], b: Optional[List[float]]) -> float:
    """Вычисляет косинус угла между векторами a и b произвольной размерности."""
    # Проверяем, что векторы не равны None
    if a is None or b is None:
        raise ValueError("Один из векторов пуст или None")
    
    # Проверяем, что векторы одной размерности
    if len(a) != len(b):
        raise ValueError("Векторы должны быть одной размерности")
    
    # Вычисляем скалярное произведение векторов
    dot_product = scalar_product(a, b)
    
    # Вычисляем длины векторов a и b
    magnitude_a = (sum(coord ** 2 for coord in a)) ** 0.5
    magnitude_b = (sum(coord ** 2 for coord in b)) ** 0.5
    
    # Проверяем, что длины векторов не равны нулю
    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Длина одного из векторов равна нулю, невозможно вычислить косинус угла")
    
    # Вычисляем и возвращаем косинус угла между векторами
    return dot_product / (magnitude_a * magnitude_b)
