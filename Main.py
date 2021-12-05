import pymysql
import re


def try_to_connect(username, password):
    try:
        cnx = pymysql.connect(host='localhost', user=username, password=password,
                              db='kitchen', charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)
        return cnx
    except Exception:
        return None


def enter():
    print("Enter username")
    u = input()
    print("Enter password")
    p = input()
    if try_to_connect(u, p) == None:
        return enter()
    else:
        return Controller(u, p)


class Controller:
    def __init__(self, username, password):

        self.connection = try_to_connect(username, password)
        self.doStuff()

    def exit(self):
        self.connection.commit()
        self.connection.close()
    def doStuff(self):
        print("Welcome to your recipe book: Enter what you want to see\n"
              + "Recipes\nIngredients\nSupplies\nReviews\nCuisines\nType")
        command = input()

        if command.lower() == "recipes":
            self.recipes_section()
        elif command.lower() == "cuisines":
            self.cuisines_section()
        elif command.lower() == "type":
            self.cuisines_section()
        elif command.lower() == "ingredients":
            self.recipes_section()

        elif command.lower() == "supplies":
            self.recipes_section()

        elif command.lower() == "reviews":
            self.recipes_section()

        elif command.lower() == "exit":
            self.exit()
        else:
            print("Not supported, try again")
            self.doStuff()

    # recipe homepage
    def recipes_section(self):
        self.view_all_recipes()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add recipe: add\n"
              "To view, edit, or delete recipe: [recipe name]")
        command = input()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.doStuff()
        else:
            self.display_recipe(command)

    # displays all the recipe names
    def view_all_recipes(self):
        print("Your recipes:")
        cursor_for_recipe_names = self.connection.cursor()
        cursor_for_recipe_names.callproc("select_recipes")
        for row in cursor_for_recipe_names.fetchall():
            name = row.get('recipe_pk')
            print("1.", name)
        cursor_for_recipe_names.close()

    # displays recipe
    def display_recipe(self, name):
        try:
            cursor_for_recipe = self.connection.cursor()
            cursor_for_recipe.callproc('select_recipe', (name,))
            recipe = cursor_for_recipe.fetchall()[0]
            print(recipe.get("recipe_pk"))
            print(recipe.get("serving_size"))
            print(recipe.get("time"), "minutes")
            print("Difficultly:", recipe.get("level"))
            cursor_for_recipe.close()
        except IndexError:
            print("Recipe Not Found :(")
            self.recipes_section()

    def cuisines_section(self):
        self.cuisines_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add cuisine: add\n"
              "To delete cuisine: delete\n"
              "To view, edit, or delete cuisine: [cuisine name]")
        command = input()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.cuisines_add()
        elif command.lower() == "delete":
            self.cuisines_delete()
        else:
            self.cuisine_display(command)

    def cuisines_display_all(self):
        print("Your cuisines:")
        cursor_for_cuisines_names = self.connection.cursor()
        cursor_for_cuisines_names.callproc("select_cuisines")
        i = 1
        for row in cursor_for_cuisines_names.fetchall():
            name = row.get('cuisine_pk')
            print(i.__str__() + ".", name)
            i += 1
        cursor_for_cuisines_names.close()

    def cuisines_add(self):
        print("Enter cuisine name to add:")
        cuisine_name = input().__str__()
        try:
            cursor_for_cuisines_add = self.connection.cursor()
            cursor_for_cuisines_add.callproc("insert_cuisine", (cuisine_name,))
            cursor_for_cuisines_add.close()
            self.cuisines_section()
        except pymysql.err.IntegrityError:
            print("Invalid Name, Try Again")
            self.cuisines_add()

    def cuisines_delete(self):
        print("Enter cuisine name To delete:")
        cuisine_name = input().__str__()
        try:
            cursor_for_cuisines_add = self.connection.cursor()
            cursor_for_cuisines_add.callproc("delete_cuisine", (cuisine_name,))
            cursor_for_cuisines_add.close()
            self.cuisines_section()
        except pymysql.err.IntegrityError:
            print("Invalid Name, Try Again")
            self.cuisines_delete()

    def cuisine_display(self, command):
        new_command = command.__str__()
        try:
            cursor_for_cuisines_add = self.connection.cursor()
            cursor_for_cuisines_add.callproc("select_cuisine", (new_command,))
            print(cursor_for_cuisines_add.fetchall()[0].get("cuisine_pk"))
            cursor_for_cuisines_add.close()
            self.cuisines_update(new_command)
        except (pymysql.err.IntegrityError, IndexError):
            print("Cuisine not found")
            self.cuisines_section()

    def cuisines_update(self, command_new):
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To update cuisine name: update")
        command = input()
        if command == "home":
            self.doStuff()
        elif command == "exit":
            self.exit()
        elif command == "update":
            print("Enter new name for cuisine:")
            name = input().__str__()
            try:
                cursor_for_cuisines_add = self.connection.cursor()
                cursor_for_cuisines_add.callproc("update_cuisine", (command_new, name,))
                cursor_for_cuisines_add.close()
                self.cuisine_display(name)
            except pymysql.err.IntegrityError:
                print("Invalid name")
                self.cuisine_display(name)
        else:
            print("Invalid command")
            self.cuisine_display(command_new)

    def ingredient_section(self):
        self.ingredients_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add ingredient: add\n"
              "To delete ingredient: delete\n"
              "To view, edit, or delete ingredient: [cuisine name]")

    def ingredients_display_all(self):
        print("Ingredients:")
        cursor_for_ingredient_names = self.connection.cursor()
        cursor_for_ingredient_names.callproc("select_ingredients")
        i = 1
        for row in cursor_for_ingredient_names.fetchall():
            name = row.get('ingredient_pk')
            print(i.__str__() + ".", name)
            i += 1
        cursor_for_ingredient_names.close()

    def ingredient_add(self):
        print("Enter ingredient name to add:")
        ingredient_name = input().__str__()
        ingredient_storage = input().__str__()
        try:
            cursor_for_ingredient_add = self.connection.cursor()
            cursor_for_ingredient_add.callproc("insert_ingredient", (ingredient_name, ingredient_storage))
            cursor_for_ingredient_add.close()
            self.ingredient_section()
        except pymysql.err.IntegrityError:
            print("Invalid Fields, Try Again")
            self.ingredient_add()

    def ingredient_delete(self):
        print("Enter ingredient name To delete:")
        ingredient_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_cuisine", (ingredient_name,))
            cursor.close()
            self.ingredient_section()
        except pymysql.err.IntegrityError:
            print("Invalid Name, Try Again")
            self.ingredient_delete()

    def ingredient_display(self, ingredient_pk):
        ingredient_pk_str = str(ingredient_pk)
        try:
            cursor = self.connection.cursor()
            cursor.callproc("select_ingredient", (ingredient_pk_str,))
            print(cursor.fetchall()[0].get("ingredient_pk"),
                  cursor.fetchall()[0].get("storage"))
            cursor.close()
        except (pymysql.err.IntegrityError, IndexError):
            print("Cuisine not found")
            self.cuisines_section()



controller = enter()
