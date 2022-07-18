#!/bin/env python3

import gi

# Import and use GTK3
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Handle Error Traceback
import traceback
# For Type Hinting
from numbers import Number


class CalcWindow(Gtk.Window):
    # CalcApp is a subclass of GTK Window
    def __init__(self, *args, **kwargs):
        # Create a GTK Window object
        super().__init__(*args, **kwargs)

        # Create a Header for the GTK App
        header = Gtk.HeaderBar(title="Calculator App")
        header.set_subtitle("PyGTK Test App")
        header.props.show_close_button = True
        self.set_titlebar(header)

        # Sets up the icon
        self.set_default_icon_from_file("icon.png")

        # Initializes the UI of app.
        self.init_ui()

        # When the window is destroyed/closed quit the app.
        self.connect("destroy", Gtk.main_quit)
        # Show all windows and start GTK main loop.
        self.show_all()
        # self.create_about_dialog()
        Gtk.main()

    def init_ui(self):
        grid = Gtk.Grid()

        # Row 1
        self.result = Gtk.Entry()
        self.result.set_text("0")
        self.result.set_alignment(1)
        self.result.set_editable(False)
        grid.attach(self.result, 1, 0, 4, 1)
        # Gtk.Grid.attach(child, left, top, width, height)

        # Create the buttons
        btn_num_0 = Gtk.Button(label="0")
        btn_num_1 = Gtk.Button(label="1")
        btn_num_2 = Gtk.Button(label="2")
        btn_num_3 = Gtk.Button(label="3")
        btn_num_4 = Gtk.Button(label="4")
        btn_num_5 = Gtk.Button(label="5")
        btn_num_6 = Gtk.Button(label="6")
        btn_num_7 = Gtk.Button(label="7")
        btn_num_8 = Gtk.Button(label="8")
        btn_num_9 = Gtk.Button(label="9")
        btn_op_add = Gtk.Button(label="+")
        btn_op_subt = Gtk.Button(label="-")
        btn_op_mult = Gtk.Button(label="*")
        btn_op_div = Gtk.Button(label="/")
        btn_op_dot = Gtk.Button(label=".")
        btn_op_perc = Gtk.Button(label="%")
        btn_clear = Gtk.Button(label="C")
        btn_equal = Gtk.Button(label="=")
        btn_delete = Gtk.Button(label="⌫")

        # Add EventListeners
        btn_num_0.connect("clicked", self.num_pressed)
        btn_num_1.connect("clicked", self.num_pressed)
        btn_num_2.connect("clicked", self.num_pressed)
        btn_num_3.connect("clicked", self.num_pressed)
        btn_num_4.connect("clicked", self.num_pressed)
        btn_num_5.connect("clicked", self.num_pressed)
        btn_num_6.connect("clicked", self.num_pressed)
        btn_num_7.connect("clicked", self.num_pressed)
        btn_num_8.connect("clicked", self.num_pressed)
        btn_num_9.connect("clicked", self.num_pressed)

        btn_op_add.connect("clicked", self.op_pressed)
        btn_op_subt.connect("clicked", self.op_pressed)
        btn_op_mult.connect("clicked", self.op_pressed)
        btn_op_div.connect("clicked", self.op_pressed)
        btn_op_dot.connect("clicked", self.op_pressed)
        btn_op_perc.connect("clicked", self.op_pressed)

        btn_clear.connect("clicked", self.clear_calc)
        btn_delete.connect("clicked", self.delete_last)
        btn_equal.connect("clicked", self.get_result)

        # Row 2
        grid.attach(btn_clear, 1, 1, 1, 1)
        grid.attach(btn_op_perc, 2, 1, 1, 1)
        grid.attach(btn_delete, 3, 1, 1, 1)
        grid.attach(btn_op_div, 4, 1, 1, 1)

        # Row 3
        grid.attach(btn_num_7, 1, 2, 1, 1)
        grid.attach(btn_num_8, 2, 2, 1, 1)
        grid.attach(btn_num_9, 3, 2, 1, 1)
        grid.attach(btn_op_mult, 4, 2, 1, 1)

        # Row 4
        grid.attach(btn_num_4, 1, 3, 1, 1)
        grid.attach(btn_num_5, 2, 3, 1, 1)
        grid.attach(btn_num_6, 3, 3, 1, 1)
        grid.attach(btn_op_subt, 4, 3, 1, 1)

        # Row 5
        grid.attach(btn_num_1, 1, 4, 1, 1)
        grid.attach(btn_num_2, 2, 4, 1, 1)
        grid.attach(btn_num_3, 3, 4, 1, 1)
        grid.attach(btn_op_add, 4, 4, 1, 1)

        # Row 6
        grid.attach(btn_num_0, 1, 5, 2, 1)
        grid.attach(btn_op_dot, 3, 5, 1, 1)
        grid.attach(btn_equal, 4, 5, 1, 1)
        # Gtk.Grid.attach(child, left, top, width, height)

        about_btn = Gtk.Button(label="About")
        about_btn.connect("clicked", self.create_about_dialog)

        bar = Gtk.ActionBar()
        bar.pack_start(about_btn)
        grid.attach(bar, 1, 6, 4, 1)

        self.add(grid)

    def num_pressed(self, widget) -> None:
        current = self.result.get_text()
        if current == "0" or current == "Error":
            self.result.set_text(widget.props.label)
        else:
            self.result.set_text(current + widget.props.label)

    def op_pressed(self, widget) -> None:
        current = self.result.get_text()
        if current == "Error":
            current = "0"
        if current == "0" and widget.props.label == "-":
            current = ""
        self.result.set_text(current + widget.props.label)

    def clear_calc(self, widget) -> None:
        self.result.set_text("0")

    def delete_last(self, widget) -> None:
        current = self.result.get_text()
        if current == "Error":
            self.result.set_text("0")
        else:
            new_eq = current[:-1]
            if new_eq == "":
                new_eq = "0"
            self.result.set_text(new_eq)

    def get_result(self, widget) -> None:
        current = self.result.get_text()
        try:
            result = self.eval_eq(self.santize(current))
            result = int(result) if str(result).endswith(".0") else result
            if result is None:
                raise Exception("Error: Couldn't evaluate the equation")
        except:
            traceback.print_exc()
            result = "Error"
        self.result.set_text(str(result))

    def santize(self, equation: str) -> str:
        # if it is just -
        if equation == "-":
            equation = "0"

        # If we have a negative number at beginning
        if equation.startswith("-"):
            equation = "0" + equation

        # if we have % get equivalent arithmetic operation
        if "%" in equation:
            equation = equation.replace("%", "/100")

        return equation

    def eval_eq(self, equation: str) -> Number:
        # If it's an int return
        if equation.isnumeric():
            return int(equation)

        # If it's a float return
        try:
            return float(equation)
        except ValueError:
            pass

        # Else tries to parse equation

        # Case of Addition
        if "+" in equation:
            exp = equation.split("+")
            exp = ["+".join(exp[:-1]), exp[-1]]
            return self.eval_eq(exp[0]) + self.eval_eq(exp[1])

        # Case of Subtraction
        if "-" in equation:
            exp = equation.split("-")
            exp = ["-".join(exp[:-1]), exp[-1]]
            # prevents *- and /- case error
            if exp[0][-1] != "*" and exp[0][-1] != "/":
                return self.eval_eq(exp[0]) - self.eval_eq(exp[1])

        # Case of Multiplication
        if "*" in equation:
            exp = equation.split("*")
            exp = ["*".join(exp[:-1]), exp[-1]]
            # prevents ** case error
            if exp[0][-1] != "*":
                return self.eval_eq(exp[0]) * self.eval_eq(exp[1])

        # Case of Division
        if "/" in equation:
            exp = equation.split("/")
            exp = ["/".join(exp[:-1]), exp[-1]]
            # prevents // case error
            if exp[0][-1] != "/":
                return self.eval_eq(exp[0]) / self.eval_eq(exp[1])

        # Case of Floor Divison
        if "//" in equation:
            exp = equation.split("//")
            exp = ["//".join(exp[:-1]), exp[-1]]
            return self.eval_eq(exp[0]) // self.eval_eq(exp[1])

        # Case of Power
        if "**" in equation:
            exp = equation.split("**")
            exp = ["**".join(exp[:-1]), exp[-1]]
            return self.eval_eq(exp[0]) ** self.eval_eq(exp[1])

    def create_about_dialog(self, widget):
        dialog = Gtk.AboutDialog()
        dialog.set_program_name("Simple PyGTK Calculator App")
        dialog.set_version("0.1.0")
        dialog.set_comments(
            "A simple calculator app made with GTK Python bindings")
        dialog.set_website_label("Source Code")
        dialog.set_website(
            "https://github.com/MrPancakes39/Simple-Calculator-App")
        dialog.set_license_type(Gtk.License.MIT_X11)
        dialog.set_authors(["MrPancakes39"])
        dialog.set_artists(
            ["Math icon by Icons8.", "https://icons8.com/icon/13216/math"])
        dialog.show()


class CalcApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="app.mrpancakes39.CalcGTK")
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = CalcWindow(application=self, title="Calculator App")
        self.window.present()


if __name__ == "__main__":
    app = CalcApp()
    app.run(None)
