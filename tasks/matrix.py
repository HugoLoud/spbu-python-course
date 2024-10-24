from typing import List, Optional


def get_row_matrix(matrix: Optional[List[List[int]]]) -> int:
    ## Возвращает количество строк в матрице.
    ## Если матрица пуста или равна None, вызывает ошибку.

    if matrix is None or not matrix:
        raise ValueError("Матрица пуста или равна None")
    return len(matrix)


def get_cols_matrix(matrix: Optional[List[List[int]]]) -> int:
    ## Возвращает количество столбцов в матрице.
    ## Если матрица пуста или равна None, вызывает ошибку.

    if matrix is None or not matrix:
        raise ValueError("Матрица пуста или равна None")
    return len(matrix[0]) if len(matrix) > 0 else 0


def sum_matrix(
    a: Optional[List[List[int]]], b: Optional[List[List[int]]]
) -> List[List[int]]:
    ## Складывает две матрицы и возвращает результат.
    ## Проверяет, что обе матрицы не равны None и имеют одинаковые размеры.

    if a is None or b is None:
        raise ValueError("Одна из матриц пуста или равна None")

    if get_row_matrix(a) != get_row_matrix(b) or get_cols_matrix(a) != get_cols_matrix(
        b
    ):
        raise ValueError("Размеры матриц не совпадают")

    # Суммируем соответствующие элементы обеих матриц
    return [
        [a[i][j] + b[i][j] for j in range(get_cols_matrix(a))]
        for i in range(get_row_matrix(a))
    ]


def product_matrix(
    a: Optional[List[List[int]]], b: Optional[List[List[int]]]
) -> List[List[int]]:
    ## Перемножает две матрицы и возвращает результат.
    ## Проверяет, что обе матрицы не равны None и что количество столбцов
    ## первой матрицы совпадает с количеством строк второй матрицы.

    if a is None or b is None:
        raise ValueError("Одна из матриц пуста или равна None")

    if get_cols_matrix(a) != get_row_matrix(b):
        raise ValueError(
            "Количество столбцов первой матрицы должно быть равно количеству строк второй матрицы"
        )

    # Инициализируем результирующую матрицу нулями
    result = [[0 for _ in range(get_cols_matrix(b))] for _ in range(get_row_matrix(a))]

    # Умножаем матрицы, используя стандартный алгоритм умножения матриц
    for i in range(get_row_matrix(a)):
        for j in range(get_cols_matrix(b)):
            for k in range(get_cols_matrix(a)):
                result[i][j] += a[i][k] * b[k][j]

    return result


def transponiruem_matrix(matrix: Optional[List[List[int]]]) -> List[List[int]]:
    ## Транспонирует матрицу (меняет строки и столбцы местами).
    ## Если матрица пуста или равна None, возвращает пустой список.

    if matrix is None or len(matrix) == 0 or len(matrix[0]) == 0:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    # Создаем новую матрицу, в которой строки и столбцы поменяны местами
    return [[matrix[j][i] for j in range(rows)] for i in range(cols)]
