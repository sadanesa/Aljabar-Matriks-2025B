from typing import List

def minor(matrix: List[List[float]], i: int, j: int) -> List[List[float]]:
    return [ [row[col] for col in range(len(row)) if col != j] 
             for idx,row in enumerate(matrix) if idx != i ]

def determinant(matrix: List[List[float]]) -> float:
    n = len(matrix)
    if n == 0:
        return 1.0
    if any(len(row) != n for row in matrix):
        raise ValueError("Matrix harus bujur sangkar atau matriks nxn")
    
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    det = 0.0
    for j, a in enumerate(matrix[0]):
        sign = (-1) ** (0 + j)
        m = minor(matrix, 0, j)
        det_j = determinant(m)
        det += a * sign * det_j
    return det

if __name__ == "__main__":
    A = [
        [8, 8, 3, 5],
        [3, 9, 6, 0],
        [4, 6, 4, 1], 
        [3, 0, 1, 0]
    ]
    print("Matrix A:")
    for row in A:
        print(row)
    print("Determinant (kofaktor) =", determinant(A))