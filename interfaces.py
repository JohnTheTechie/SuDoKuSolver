

class Controller:
    def set_model(self, model):
        raise NotImplementedError

    def set_solver(self, solver):
        raise NotImplementedError

    def set_view(self, view):
        raise NotImplementedError

    def button_pressed(self, press_event):
        raise NotImplementedError

    def number_selected(self, value):
        raise NotImplementedError

    def cell_clicked(self, column, row):
        raise NotImplementedError


class View:
    pass


class Model:
    """
    base interface for matrix to contain the SuDoKu data
    """
    def set_base_puzzle(self, matrix: list[list]):
        """
        function to set the predefined values in predefined cells
        The inputs could be either a list of strings read from the cmdline\
            or list of list of values provided by a GUI
        :param matrix: list data
        :return:
        """
        raise NotImplementedError

    def set_value(self, value, column, row):
        raise NotImplementedError

    def clear_value(self, column, row):
        raise NotImplementedError

    def get_value(self, column, row):
        raise NotImplementedError

    def add_potential_value(self, value, column, row):
        raise NotImplementedError

    def remove_potential_value(self, value, column, row):
        raise NotImplementedError

    def clear_potential_value(self, column, row):
        raise NotImplementedError

    def get_potential_value(self, column, row):
        raise NotImplementedError

    def review_column_n_row(self, value, column, row):
        raise NotImplementedError

    def review_subcell(self, value, column, row):
        raise NotImplementedError

    def review_matrix(self):
        raise NotImplementedError

    def set_controller(self, controller: Controller):
        raise NotImplementedError

    def set_view(self, view: View):
        raise NotImplementedError

    def set_analyser(self, analyser):
        raise NotImplementedError

    def set_converter(self, converter):
        raise NotImplementedError

    def generate_matrix_in_strings(self) -> list[str]:
        raise NotImplementedError

    def generate_matrix_in_lists(self) -> list:
        raise NotImplementedError


class Solver:
    def set_model(self, model: Model):
        raise NotImplementedError

    def set_controller(self, controller: Controller):
        raise NotImplementedError

    def set_view(self, view: View):
        raise NotImplementedError

    def solve(self):
        raise NotImplementedError
