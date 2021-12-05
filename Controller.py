import pymysql
import PyQt5


class Controller:
    def __init__(self):
        self.model = None

    def connect(self, username, password):
        try:
            cnx = pymysql.connect(host='localhost', user=username,
                                  password=password,
                                  db='kitchen', charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
            self.model = cnx
            return True
        except Exception:
            return False

    # select all the recipe names
    def select_recipes_names(self):
        cursor = self.model.cursor()
        cursor.callproc('select_recipes')
        recipes = []
        for row in cursor.fetchall():
            recipes.append(row)

        return recipes
