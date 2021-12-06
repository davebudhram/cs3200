import pymysql


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
            self.types_section()
        elif command.lower() == "ingredients":
            self.ingredient_section()
        elif command.lower() == "supplies":
            self.supply_section()
        elif command.lower() == "reviews":
            self.reviews_section()
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

    # Types

    def types_section(self):
        self.types_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add types: add\n"
              "To delete types: delete\n"
              "To view, edit, or delete type: [type name]")
        command = input().__str__()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.type_add()
        elif command.lower() == "delete":
            self.type_delete()
        else:
            self.type_display(command)

    def types_display_all(self):
        print("Types:")
        cursor_for_type_names = self.connection.cursor()
        cursor_for_type_names.callproc("select_types")
        i = 1
        for row in cursor_for_type_names.fetchall():
            name = row.get('type_pk')
            print(i.__str__() + ".", name)
            i += 1
        cursor_for_type_names.close()

    # TODO add insert procedure to database
    def type_add(self):
        print("Enter type name to add:")
        type_name = input().__str__()
        try:
            cursor_for_type_add = self.connection.cursor()
            cursor_for_type_add.callproc("insert_type", (type_name,))
            cursor_for_type_add.close()
            self.types_section()
        except pymysql.err.IntegrityError:
            print("Invalid Fields")
            self.ingredient_section()

    # TODO fix delete procedure to take in a varchar
    def type_delete(self):
        print("Enter type name To delete:")
        type_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_type", (type_name,))
            cursor.close()
            self.types_section()
        except pymysql.err.IntegrityError:
            print("Cannot delete type, used in recipe")
            self.types_section()

    # TODO add select type function to database
    def type_display(self, type_pk):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("select_type", (type_pk,))
            type_curs = cursor.fetchall()[0]
            print("Type:", type_curs.get("type_pk"))
            cursor.close()
            self.type_update(type_pk)
        except (pymysql.err.IntegrityError, IndexError):
            print("Type not found")
            self.types_section()

    def type_update(self, type_pk):
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To update type name: update")
        command = input()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == 'exit':
            self.exit()
        elif command.lower() == "update":
            self.type_update_name(type_pk)
        else:
            print("Invalid Command")
            self.type_display(type_pk)

    # TODO fix update_type_name procedure to use tpk
    def type_update_name(self, type_pk):
        print("Enter new name for type")
        new_type_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("update_type_name", (type_pk,new_type_name,))
            cursor.close()
            self.type_display(new_type_name)
        except (pymysql.err.IntegrityError, IndexError):
            print("New type name is invalid, try again")
            self.type_update_name(type_pk)

    # Reviews

    def reviews_section(self):
        self.reviews_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add reviews: add\n"
              "To delete reviews: delete\n"
              "To view, edit, or delete reviews: [reviews name]")
        command = input().__str__()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.review_add()
        elif command.lower() == "delete":
            self.review_delete()
        else:
            self.review_display(command)

    # TODO add select reviews procedure to database
    def reviews_display_all(self):
        print("Reviews:")
        cursor_for_review_names = self.connection.cursor()
        cursor_for_review_names.callproc("select_reviews")
        i = 1
        for row in cursor_for_review_names.fetchall():
            recipe_name = row.get('recipe_fk')
            review = row.get('review_pk')
            print(i.__str__() + ".", recipe_name)
            print(i.__str__() + ".", review)
            i += 1
        cursor_for_review_names.close()

    # TODO add insert review to database
    def review_add(self):
        print("Enter recipe name to add review to:")
        recipe_name = input().__str__()
        review = input('Enter your review for that recipe:')
        try:
            cursor_for_type_add = self.connection.cursor()
            cursor_for_type_add.callproc("insert_review", (recipe_name,review,))
            cursor_for_type_add.close()
            self.types_section()
        except pymysql.err.IntegrityError:
            print("Invalid Fields")
            self.ingredient_section()

    # TODO add delete review into database
    def review_delete(self):
        print("Enter review's recipe name To delete:")
        recipe_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_review", (recipe_name,))
            cursor.close()
            self.reviews_section()
        except pymysql.err.IntegrityError:
            print("Cannot delete review, does not exist")
            self.reviews_section()

    # TODO add select review function to database
    # TODO finish this method
    def review_display(self, recipe_fk):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("select_review", (recipe_fk,))
            type_curs = cursor.fetchall()[0]
            print("Type:", type_curs.get("type_pk"))
            cursor.close()
            self.type_update(recipe_fk)
        except (pymysql.err.IntegrityError, IndexError):
            print("Type not found")
            self.types_section()

    # TODO finish this method
    def review_update(self, type_pk):
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To update type name: update")
        command = input()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == 'exit':
            self.exit()
        elif command.lower() == "update":
            self.type_update_name(type_pk)
        else:
            print("Invalid Command")
            self.type_display(type_pk)

    # TODO finish method if we want to implemetn updates
    def review_update_name(self, type_pk):
        print("Enter new name for type")
        new_type_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("update_type_name", (type_pk,new_type_name,))
            cursor.close()
            self.type_display(new_type_name)
        except (pymysql.err.IntegrityError, IndexError):
            print("New type name is invalid, try again")
            self.type_update_name(type_pk)

    # Ingredients

    def ingredient_section(self):
        self.ingredients_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add ingredient: add\n"
              "To delete ingredient: delete\n"
              "To view, edit, or delete ingredient: [Ingredient name]")
        command = input().__str__()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.ingredient_add()
        elif command.lower() == "delete":
            self.ingredient_delete()
        else:
            self.ingredient_display(command)

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
        print("Enter ingredient storage to add:")
        ingredient_storage = input().__str__()
        try:
            cursor_for_ingredient_add = self.connection.cursor()
            cursor_for_ingredient_add.callproc("insert_ingredient", (ingredient_name, ingredient_storage))
            cursor_for_ingredient_add.close()
            self.ingredient_section()
        except pymysql.err.IntegrityError:
            print("Invalid Fields")
            self.ingredient_section()

    def ingredient_delete(self):
        print("Enter ingredient name To delete:")
        ingredient_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_ingredient", (ingredient_name,))
            cursor.close()
            self.ingredient_section()
        except pymysql.err.IntegrityError:
            print("Cannot delete ingredient, used in recipe")
            self.ingredient_section()

    def ingredient_display(self, ingredient_pk):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("select_ingredient", (ingredient_pk,))
            ingredient = cursor.fetchall()[0]
            print("Ingredient:", ingredient.get("ingredient_pk"))
            print("Storage:", ingredient.get("storage"))
            cursor.close()
            self.ingredient_update(ingredient_pk)
        except (pymysql.err.IntegrityError, IndexError):
            print("Ingredient not found")
            self.ingredient_section()

    def ingredient_update(self, ingredient_pk):
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To update ingredient: update")
        command = input()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == 'exit':
            self.exit()
        elif command.lower() == "update":
            print("Commands:\nTo update ingredient name: name\nTo update ingredient storage: storage")
            ingredient_update = input()
            if ingredient_update.lower() == "name":
                self.ingredient_update_name(ingredient_pk)
            elif ingredient_update.lower() == "storage":
                self.ingredient_update_storage(ingredient_pk)
            else:
                print("Invalid update type")
                self.ingredient_display(ingredient_pk)
        else:
            print("Invalid Command")
            self.ingredient_display(ingredient_pk)

    def ingredient_update_name(self, ingredient_pk):
        print("Enter new name for ingredient")
        new_ingredient_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("update_ingredient_name", (ingredient_pk, new_ingredient_name,))
            cursor.close()
            self.ingredient_display(new_ingredient_name)
        except (pymysql.err.IntegrityError, IndexError):
            print("New ingredient name is invalid, try again")
            self.ingredient_update_name(ingredient_pk)

    def ingredient_update_storage(self, ingredient_pk):
        print("Enter new storage for ingredient")
        new_storage_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("update_ingredient_storage", (ingredient_pk, new_storage_name,))
            cursor.close()
            self.ingredient_display(ingredient_pk)
        except (pymysql.err.OperationalError, IndexError):
            print("Invalid storage name")
            self.ingredient_update_storage(ingredient_pk)

    def supply_section(self):
        self.supplies_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add supply: add\n"
              "To delete supply: delete\n"
              "To view, edit, or delete supply: [supply name]")
        command = input().__str__()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.supply_add()
        elif command.lower() == "delete":
            self.supply_delete()
        else:
            self.supply_display(command)

    def supplies_display_all(self):
        print("Supplies:")
        cursor = self.connection.cursor()
        cursor.callproc("select_supplies")
        i = 1
        for row in cursor.fetchall():
            name = row.get('supply_pk')
            print(i.__str__() + ".", name)
            i += 1
        cursor.close()

    def supply_add(self):
        print("Enter supply name to add:")
        supply_name = input().__str__()
        print("Enter supply size to add:")
        supply_size = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("insert_supply", (supply_name, supply_size))
            cursor.close()
            self.supply_section()
        except pymysql.err.IntegrityError:
            print("Invalid Fields")
            self.supply_section()

    def supply_delete(self):
        print("Enter supply name To delete:")
        supply_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_supply", (supply_name,))
            cursor.close()
            self.supply_section()
        except pymysql.err.IntegrityError:
            print("Cannot delete supply, used in recipe")
            self.supply_section()

    def supply_display(self, supply_pk):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("select_supply", (supply_pk,))
            ingredient = cursor.fetchall()[0]
            print("Supply:", ingredient.get("supply_pk"))
            print("Size:", ingredient.get("size"))
            cursor.close()
            self.supply_update(supply_pk)
        except (pymysql.err.IntegrityError, IndexError):
            print("Supply not found")
            self.supply_section()

    def supply_update(self, supply_pk):
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To update supply: update")
        command = input()
        if command.lower() == "home":
            self.doStuff()
        elif command.lower() == 'exit':
            self.exit()
        elif command.lower() == "update":
            print("Commands:\nTo update supply name: name\nTo update supply size: size")
            supply_update = input()
            if supply_update.lower() == "name":
                self.supply_update_name(supply_pk)
            elif supply_update.lower() == "size":
                self.supply_update_size(supply_pk)
            else:
                print("Invalid update type")
                self.supply_display(supply_pk)
        else:
            print("Invalid Command")
            self.supply_display(supply_pk)

    def supply_update_name(self, supply_pk):
        print("Enter new name for supply")
        new_supply_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("update_supply_name", (supply_pk, new_supply_name,))
            cursor.close()
            self.supply_display(new_supply_name)
        except (pymysql.err.IntegrityError, IndexError):
            print("New supply name is invalid, try again")
            self.supply_update_name(supply_pk)

    def supply_update_size(self, supply_pk):
        print("Enter new size for supply")
        new_size = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("update_supply_size", (supply_pk, new_size,))
            cursor.close()
            self.supply_display(supply_pk)
        except (pymysql.err.OperationalError, IndexError):
            print("Invalid storage name")
            self.supply_update_size(supply_pk)


# test comment for commit
controller = enter()
