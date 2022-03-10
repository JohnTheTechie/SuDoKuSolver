from enum import Enum

import interfaces
from interfaces import Model, View, Controller
import logging


class CellType(Enum):
    CELL_PRESET = 1
    CELL_EMPTY = 2


class Cell:

    def __init__(self, column_index, row_index, cell_type):
        self._flag = True
        self.type = cell_type
        self.column = column_index
        self.row = row_index
        self.potential_candidates_list = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.value = 0x0
        self.review_flag = False
        logging.debug(f"cell created for position c={self.column} r={self.row} type={self.type}")

    def __setattr__(self, key, value):
        if (key == "value" or key == "potential_candidates_list") and (self.type == CellType.CELL_EMPTY or self._flag):
            self._flag = False
            self.__dict__[key] = value
            logging.debug(f"cell[{self.row}][{self.column}] value updated attrib={key} value={value}")
        elif key == "column" or key == "row" or key == "type" or key == "review_flag":
            self.__dict__[key] = value
        elif key == "_flag":
            self.__dict__[key] = value

    def __str__(self):
        string = f"cell[{self.row}][{self.row} of value={self.value} and pot list={self.potential_candidates_list}]"


class MatrixBuilder:

    @staticmethod
    def build_matrix(length=9, height=9):
        matrix: list[list[Cell]] = []
        for row_i in range(height):
            matrix.append([])
            for col in range(length):
                matrix[row_i].append(Cell(col, row_i, CellType.CELL_EMPTY))
        return matrix


class MatrixAnalyser:

    def __init__(self, container: interfaces.Model = None):
        self.model = container

    def set_container(self, container):
        self.model = container

    def review_column_n_row(self, matrix: list[list[Cell]], value, column_i, row_i):
        for col in range(9):
            logging.debug(f"reviewing cell[{row_i}][{col}] with potential_list=({matrix[row_i][col].potential_candidates_list})")
            if value in matrix[row_i][col].potential_candidates_list:
                matrix[row_i][col].potential_candidates_list.remove(value)
                logging.debug(
                    f"reviewing cell[{row_i}][{col}] with potential_list=({matrix[row_i][col].potential_candidates_list})")
            if len(matrix[row_i][col].potential_candidates_list) == 1:
                logging.debug(
                    f"reviewing cell[{row_i}][{col}] | {value} removed from potential list = {matrix[row_i][col].potential_candidates_list}")
                self.model.set_value(matrix[row_i][col].potential_candidates_list.pop(), row_i, col)
                self.model.review_column_n_row(matrix[row_i][col].value, col, row_i)
                self.model.review_subcell(matrix[row_i][col].value, col, row_i)
        for r in range(9):
            logging.debug(f"reviewing cell[{r}][{column_i}] with potential_list=({matrix[r][column_i].potential_candidates_list})")
            if value in matrix[r][column_i].potential_candidates_list:
                matrix[r][column_i].potential_candidates_list.remove(value)
                logging.debug(
                    f"reviewing cell[{r}][{column_i}] with potential_list=({matrix[r][column_i].potential_candidates_list})")
            if len(matrix[r][column_i].potential_candidates_list) == 1:
                logging.debug(
                    f"reviewing cell[{r}][{column_i}] | {value} removed from potential list = {matrix[r][column_i].potential_candidates_list}")
                self.model.set_value(matrix[r][column_i].potential_candidates_list.pop(), r, column_i)
                self.model.review_column_n_row(matrix[r][column_i].value, column_i, r)
                self.model.review_subcell(matrix[r][column_i].value, column_i, r)

    def review_subcell(self, matrix: list[list[Cell]], value, column_i, row_i):
        r_l, r_u = row_i // 3 * 3, (row_i // 3 * 3) + 3
        c_l, c_u = column_i // 3 * 3, (column_i // 3 * 3) + 3
        for r_i in range(r_l, r_u):
            for c_i in range(c_l, c_u):
                logging.debug(f"reviewing cell[{r_i}][{c_i}] with potential_list=({matrix[r_i][c_i].potential_candidates_list})")
                if value in matrix[r_i][c_i].potential_candidates_list:
                    matrix[r_i][c_i].potential_candidates_list.remove(value)
                    logging.debug(
                        f"reviewing cell[{r_i}][{c_i}] | {value} removed from potential list = {matrix[r_i][c_i].potential_candidates_list}")
                if len(matrix[r_i][c_i].potential_candidates_list) == 1:
                    logging.debug(
                        f"reviewing cell[{r_i}][{c_i}] with 1 potential value = {matrix[r_i][c_i].potential_candidates_list}")
                    self.model.set_value(matrix[r_i][c_i].potential_candidates_list.pop(), r_i, c_i)
                    self.model.review_column_n_row(matrix[r_i][c_i].value, c_i, r_i)
                    self.model.review_subcell(matrix[r_i][c_i].value, c_i, r_i)

    def review_matrix(self, matrix: list[list[Cell]]):
        logging.info("matrix review initiated")
        for r_i in range(0, 9):
            for c_i in range(0, 9):
                logging.debug(f"reviewing cell[{r_i}][{c_i}] with potential_list=({matrix[r_i][c_i].potential_candidates_list})")
                if len(matrix[r_i][c_i].potential_candidates_list) == 1:
                    logging.debug(f"reviewing cell[{r_i}][{c_i}] with 1 potential value = {matrix[r_i][c_i].potential_candidates_list}")
                    self.model.set_value(matrix[r_i][c_i].potential_candidates_list.pop(), r_i, c_i)
                    self.model.review_column_n_row(matrix[r_i][c_i].value, c_i, r_i)
                    self.model.review_subcell(matrix[r_i][c_i].value, c_i, r_i)
                if matrix[r_i][c_i].review_flag & 0x1 != 0x01:
                    self.model.review_column_n_row(matrix[r_i][c_i].value, c_i, r_i)
                if matrix[r_i][c_i].review_flag & 0x2 != 0x02:
                    self.model.review_subcell(matrix[r_i][c_i].value, c_i, r_i)
        self.review_sub_matrix(matrix)

    def review_sub_matrix(self, matrix: list[list[Cell]]):
        print("submatrix review initiated")
        for x in range(0, 3):
            for y in range(0, 3):
                row_lower, row_upper = x*3, x*3+3
                column_lower, column_upper = y*3, y*3+3
                hashmap = {z:[] for z in range(1, 10)}
                for ri in range(row_lower, row_upper):
                    for ci in range(column_lower, column_upper):
                        logging.debug(f"reviewing cell[{ri}][{ci}] with potential_list=({matrix[ri][ci].potential_candidates_list})")
                        for val in range(1, 10):
                            if matrix[ri][ci].value == 0 and val in matrix[ri][ci].potential_candidates_list:
                                logging.debug(f"cell[{ri}][{ci}] is considered for value=[{val}]")
                                hashmap[val].append(matrix[ri][ci])
                for val, cells in hashmap.items():
                    logging.debug(f"hashmap entry value={val} for items={cells}")
                    if len(cells) == 1:
                        self.model.set_value(val, cells[0].column, cells[0].row)


class MatrixConverter:

    @staticmethod
    def generate_matrix_in_strings(matrix) -> list[str]:
        output_string = []
        index = 0
        for row_l in matrix:
            output_string.append("")
            for cell in row_l:
                output_string[index] += str(cell.value) + " "
            index += 1
        return output_string

    @staticmethod
    def generate_matrix_in_lists(matrix) -> list:
        output_string = []
        index = 0
        for row_l in matrix:
            output_string.append([])
            for cell in row_l:
                output_string[index].append(cell.value)
            index += 1
        return output_string


class BasicContainer(Model):
    __instances = {}

    def __init__(self, controller=None,
                 view=None,
                 solver=None,
                 matrix_analyser: MatrixAnalyser = None,
                 converter: MatrixConverter = None):
        self.matrix: list[list[Cell]] = MatrixBuilder.build_matrix(height=9, length=9)
        self.controller = controller
        self.view = view
        self.solver = solver
        self.analyser = matrix_analyser
        self.converter = converter

    def __new__(cls, *args, **kwargs):
        if cls not in BasicContainer.__instances:
            cls.__instances[cls] = super(Model, cls).__new__(cls)
        return cls.__instances[cls]

    def set_base_puzzle(self, matrix):
        if type(matrix[0][0]) is str:
            matrix: list[str]
            for row_i in range(9):
                values = list(map(int, matrix[row_i].split()))
                for col in range(9):
                    self.matrix[row_i][col].value = values[col]
                    if values[col] > 0:
                        self.matrix[row_i][col].potential_candidates_list.clear()
                        self.review_column_n_row(values[col], col, row_i)
                        self.review_subcell(values[col], col, row_i)
                        self.matrix[row_i][col].type = CellType.CELL_PRESET

    def set_value(self, value, column_i, row_i):
        self.matrix[row_i][column_i].value = value
        self.matrix[row_i][column_i].potential_candidates_list.clear()

    def clear_value(self, column_i: int, row_i: int):
        self.matrix[row_i][column_i].value = 0

    def get_value(self, column_i, row_i):
        return self.matrix[row_i][column_i].value

    def add_potential_value(self, value, column_i, row_i):
        self.matrix[row_i][column_i].potential_candidates_list.add(value)

    def remove_potential_value(self, value, column_i, row_i):
        self.matrix[row_i][column_i].potential_candidates_list.remove(value)

    def clear_potential_value(self, column_i, row_i):
        self.matrix[row_i][column_i].potential_candidates_list.clear()

    def get_potential_value(self, column_i, row_i):
        return self.matrix[row_i][column_i].potential_candidates_list

    def review_column_n_row(self, value, column_i, row_i):
        logging.info(f"review initiation with cell[{row_i}][{column_i}] with value={self.matrix[row_i][column_i].value} and pot. list={self.matrix[row_i][column_i].potential_candidates_list}")
        if self.matrix[row_i][column_i].review_flag & 0x1 != 0x01:
            self.analyser.review_column_n_row(self.matrix, value, column_i, row_i)
        if self.matrix[row_i][column_i].value > 0:
            self.matrix[row_i][column_i].review_flag |= 0x1

    def review_subcell(self, value, column_i, row_i):
        logging.info(
            f"review initiation with cell[{row_i}][{column_i}] with value={self.matrix[row_i][column_i].value} and pot. list={self.matrix[row_i][column_i].potential_candidates_list}")
        if self.matrix[row_i][column_i].review_flag & 0x2 != 0x02:
            self.analyser.review_subcell(self.matrix, value, column_i, row_i)
        if self.matrix[row_i][column_i].value > 0:
            self.matrix[row_i][column_i].review_flag |= 0x2

    def review_matrix(self):
        self.analyser.review_matrix(self.matrix)

    def set_controller(self, controller: Controller):
        self.controller = controller

    def set_view(self, view: View):
        self.view = view

    def set_analyser(self, analyser):
        self.analyser = analyser

    def set_converter(self, converter):
        self.converter = converter

    def generate_matrix_in_strings(self) -> list[str]:
        return self.converter.generate_matrix_in_strings(self.matrix)

    def generate_matrix_in_lists(self) -> list:
        return self.converter.generate_matrix_in_lists(self.matrix)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename=r"d:\logs.txt", filemode="w+")
    c = BasicContainer()
    c.set_analyser(MatrixAnalyser(c))
    c.set_converter(MatrixConverter())
    mat = ["0 0 0 0 0 0 2 0 0",
           "5 9 2 0 0 1 0 8 0",
           "0 0 0 8 0 5 0 9 0",
           "0 0 0 0 6 3 8 4 0",
           "7 8 0 0 5 0 0 3 5",
           "0 3 4 5 1 0 0 0 0",
           "0 4 0 6 0 9 0 0 0",
           "0 1 6 2 0 0 9 7 3",
           "0 0 5 0 0 0 0 0 0"]
    c.set_base_puzzle(mat)
    for i in range(0, 9):
        c.review_matrix()
    for row in c.generate_matrix_in_lists():
        print(row)
