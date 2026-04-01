def find_largest_square(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    cols_count = len(matrix[0])
    prev_row = [0] * (cols_count + 1)
    max_side = 0

    for row in matrix:
        current_row = [0] * (cols_count + 1)

        for col_index in range(1, cols_count + 1):
            if row[col_index - 1] == 1:
                current_row[col_index] = min(
                    prev_row[col_index],
                    current_row[col_index - 1],
                    prev_row[col_index - 1],
                ) + 1

                if current_row[col_index] > max_side:
                    max_side = current_row[col_index]

        prev_row = current_row

    return max_side


def main() -> None:
    rows_count, cols_count = map(int, input().split())

    matrix = [
        list(map(int, input().split()))
        for _ in range(rows_count)
    ]

    if len(matrix) != rows_count:
        raise ValueError(
            f"Ожидалось {rows_count} строк матрицы, получено {len(matrix)}"
        )

    for row in matrix:
        if len(row) != cols_count:
            raise ValueError(
                f"Ожидалось {cols_count} значений в строке, получено {len(row)}"
            )

    print(find_largest_square(matrix))


if __name__ == "__main__":
    main()
