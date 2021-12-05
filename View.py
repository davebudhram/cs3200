from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDialog, QLineEdit, QPushButton
import Controller
import sys


# TODO
# 1st create login

class View(QStackedWidget):
    def __init__(self):
        super(View, self).__init__()
        self.controller = Controller.Controller()
        self.initUI()
        self.log_in_view = LogInView(self)
        self.addWidget(self.log_in_view)  # 0
        self.recipes_page_view = None
        self.home_page_view = None
        self.recipe_page_view = None # 3

    def initUI(self):
        self.setGeometry(200, 200, 400, 400)
        self.setWindowTitle("Recipe Book")

    def get_username_password(self, username, password):
        if self.controller.connect(username, password):
            # we now knew the l0gin was succesful, now we can instantialized the remaining pages
            self.home_page_view = HomePageView(self)
            self.addWidget(self.home_page_view)  # 1
            #go to just added homepage
            self.setCurrentIndex(1)

        else:
            print('fail')
            # TODO add message


    def get_recipes(self):

        self.recipes_page_view = RecipesPageView(self)
        self.addWidget(self.recipes_page_view)  # 2
        return self.controller.select_recipes_names()


class LogInView(QDialog):
    def __init__(self, view):
        super(LogInView, self).__init__()
        self.view = view
        # Log in Label
        self.login_label = QtWidgets.QLabel(self)
        self.login_label.setText("Log In")
        self.login_label.move(50, 30)

        # Username label and textbox
        self.username_label = QtWidgets.QLabel(self)
        self.username_label.setText("Username")
        self.username_label.move(50, 50)
        self.username_input = QLineEdit(self)
        self.username_input.move(120, 50)

        # Password label and textbox
        self.password_label = QtWidgets.QLabel(self)
        self.password_label.setText("Password")
        self.password_label.move(50, 70)
        self.password_input = QLineEdit(self)
        self.password_input.move(120, 70)

        # Create a button in the window
        self.login_button = QPushButton('log-in', self)
        self.login_button.move(50, 90)

        # connect button to function log_in_button_clicked
        self.login_button.clicked.connect(self.log_in_button_clicked)

    def log_in_button_clicked(self):
        self.view.get_username_password(self.username_input.text(), self.password_input.text())


class HomePageView(QDialog):
    def __init__(self, view):
        super(HomePageView, self).__init__()
        self.view = view
        # Create a recipe button in the window
        self.recipes_button = QPushButton('Recipe', self)
        self.recipes_button.move(50, 70)
        self.recipes_button.clicked.connect(self.recipes_button_clicked)

        # Create a recipe button in the window
        self.ingredients_button = QPushButton('Ingredients', self)
        self.ingredients_button.move(50, 90)
        self.ingredients_button.clicked.connect(self.ingredients_button_clicked)

        # Create a recipe button in the window
        self.supplies_button = QPushButton('Supplies', self)
        self.supplies_button.move(50, 110)
        self.supplies_button.clicked.connect(self.supplies_button_clicked)

        # Create a button in the window
        self.reviews_button = QPushButton('Reviews', self)
        self.reviews_button.move(50, 130)
        self.reviews_button.clicked.connect(self.reviews_button_clicked)

    def recipes_button_clicked(self):
        self.view.setCurrentIndex(2)

    def ingredients_button_clicked(self):
        self.view.setCurrentIndex(3)

    def supplies_button_clicked(self):
        self.view.setCurrentIndex(4)

    def reviews_button_clicked(self):
        self.view.setCurrentIndex(5)


class RecipesPageView(QDialog):
    def __init__(self, view):
        super(RecipesPageView, self).__init__()
        self.view = view
        self.recipe_label = QtWidgets.QLabel(self)
        self.recipe_label.setText("Recipes")
        self.recipe_label.move(200, 0)
        self.recipe_buttons = []

        # get list of recipe tuples from model
        recipes = self.view.get_recipe_names()

        i = 0
        for recipe in recipes:
            # Create a recipe button in the window
            recipe_pk = recipe.get("recipe_pk")
            self.recipe_pk = QPushButton(recipe.get("name"), self)
            self.recipe_pk.move(50, 20 * i + 20)
            self.recipe_pk.clicked.connect(self.recipe_clicked(self, recipe_pk))
            i += 1

        def recipe_clicked(self, recipe_pk):
            self.view.setCurrentIndex(3)

class RecipePageView(QDialog):
    def __init__(self, view):
        super(RecipePageView, self).__init__()
        self.view = view
        self.recipe_label = QtWidgets.QLabel(self)
        self.recipe_label.setText("Recipes")
        self.recipe_label.move(200, 0)
        self.recipe_buttons = []

        # get list of recipe tuples from model
        recipe = self.view.get_recipe_info()

        def recipe_clicked(self, recipe_pk):
            self.view.setCurrentIndex(2)



def window():
    app = QApplication(sys.argv)
    win = View()
    win.show()
    sys.exit(app.exec_())


window()
