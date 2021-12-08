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
    if try_to_connect(u, p) is None:
        return enter()
    else:
        return Controller(u, p)


class Controller:
    def __init__(self, username, password):

        self.connection = try_to_connect(username, password)
        self.homepage_section()

    def exit(self):
        self.connection.commit()
        self.connection.close()

    def homepage_section(self):
        print("Welcome to your recipe book: Enter what you want to see\n"
              + "Commands:\nTo exit: exit\nTo view your recipes: recipes\nTo view your ingredienta: ingredients"
                "\nTo view your supplies: supplies\nTo view your reviews: reviews"
                "\nTo view your cuisines: cuisines\nTo view your types : types")
        command = input()

        if command.lower() == "recipes":
            self.recipes_section()
        elif command.lower() == "cuisines":
            self.cuisines_section()
        elif command.lower() == "types":
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
            print("Invalid command")
            self.homepage_section()

    # Recipes
    def recipes_section(self):
        self.recipes_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add recipe: add\n"
              "To view: [recipe name]")
        command = input()
        if command.lower() == "home":
            self.homepage_section()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.recipe_add()
        elif command.lower() == "delete":
            self.recipe_delete()
        else:
            self.recipe_display(command)

    # displays all the recipe names
    def recipes_display_all(self):
        print("Your recipes:")
        cursor_for_recipe_names = self.connection.cursor()
        cursor_for_recipe_names.callproc("select_recipes")
        i = 1
        for row in cursor_for_recipe_names.fetchall():
            name = row.get('recipe_pk')
            print(i.__str__() + ".", name)
            i =+1
        cursor_for_recipe_names.close()

    def recipe_add(self):
        print("Enter recipe name:")
        recipe_name = input().__str__()
        print("Enter serving size (ex: five people):")
        serving_size = input().__str__()
        print("Enter recipe cook/bake time as an integer:")
        time = input()
        print("Enter your recipe difficulty (ex: intermediate)")
        level = input().__str__()
        try:
            cursor_add_recipe= self.connection.cursor()
            cursor_add_recipe.callproc("insert_recipe", (recipe_name, serving_size, time, level,))
            cursor_add_recipe.close()
            self.connection.commit()
            self.recipe_add_relationships(recipe_name)
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Invalid Fields")
            self.recipes_section()

    def recipe_add_relationships(self, recipe_pk):
        print("Commands:\nAdd ingredient to recipe: ingredient\n"
              "Add supply to recipe: supply\nAdd cuisine to recipe: cuisine\n"
              "Add direction to recipe: direction\nAdd type to recipe: type\n"
              "When finished with recipe: finish")
        command = input().__str__()
        if command == "ingredient":
            self.recipe_add_ingredient(recipe_pk)
        elif command == "direction":
            self.recipe_add_direction(recipe_pk)
        elif command == "supply":
            self.recipe_add_supply(recipe_pk)
        elif command == "cuisine":
            self.recipe_add_cuisine(recipe_pk)
        elif command == "type":
            self.recipe_add_type(recipe_pk)
        elif command == "finish":
            self.recipe_display(recipe_pk)
        else:
            print("Invalid command")
            self.recipe_add_relationships(recipe_pk)

    def recipe_add_ingredient(self, recipe_pk):
        print("Enter ingredient name, here are the ones you can add")
        self.ingredients_display_all()
        name = input().__str__()
        print("Enter amount of ingredient (ex: five tablespoons)")
        quantity = input().__str__()
        try:
            cursor_add_ingredient= self.connection.cursor()
            cursor_add_ingredient.callproc("insert_ingredient_recipe",(name, recipe_pk, quantity,))
            cursor_add_ingredient.close()
            self.connection.commit()
            self.recipe_add_relationships(recipe_pk)
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Invalid Fields")
            self.recipe_add_relationships(recipe_pk)

    def recipe_add_supply(self, recipe_pk):
        print("Enter supply name, here are the ones you can add:")
        self.supplies_display_all()
        name = input().__str__()
        print("Enter number of this supply needed as integer:")
        quantity = input().__str__()
        try:
            cursor_add_supply= self.connection.cursor()
            cursor_add_supply.callproc("insert_supply_quantity",(name, recipe_pk, quantity,))
            cursor_add_supply.close()
            self.connection.commit()
            self.recipe_add_relationships(recipe_pk)
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Invalid Fields")
            self.recipe_add_relationships(recipe_pk)

    def recipe_add_type(self, recipe_pk):
        print("Enter the type of recipe, here are the ones you can add:")
        self.type_display_all()
        name = input().__str__()
        try:
            cursor_add_type= self.connection.cursor()
            cursor_add_type.callproc("insert_type_recipe",(name, recipe_pk,))
            cursor_add_type.close()
            self.connection.commit()
            self.recipe_add_relationships(recipe_pk)
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Invalid Field")
            self.recipe_add_relationships(recipe_pk)

    def recipe_add_cuisine(self, recipe_pk):
        print("Enter the cuisine of recipe, here are the ones you can add:")
        self.cuisines_display_all()
        name = input().__str__()
        try:
            cursor_add_cuisine = self.connection.cursor()
            cursor_add_cuisine.callproc("insert_cuisine_recipe",(name, recipe_pk,))
            cursor_add_cuisine.close()
            self.connection.commit()
            self.recipe_add_relationships(recipe_pk)
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Invalid Field")
            self.recipe_add_relationships(recipe_pk)

    def recipe_add_direction(self, recipe_pk):
        print("Enter direction")
        direction = input().__str__()
        try:
            cursor_add_ingredient= self.connection.cursor()
            cursor_add_ingredient.callproc("insert_direction", (recipe_pk, direction,))
            cursor_add_ingredient.close()
            self.connection.commit()
            self.recipe_add_relationships(recipe_pk)
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Invalid Fields")
            self.recipe_add_relationships(recipe_pk)

    def recipe_delete(self):
        print("Enter recipe's name to delete:")
        recipe_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_recipe", (recipe_name,))
            cursor.close()
            self.connection.commit()
            self.recipes_section()
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Unable to delete recipe")
            self.recipes_section()

    def recipe_display(self, name):
        try:
            cursor_for_recipe = self.connection.cursor()
            cursor_for_recipe.callproc('select_recipe', (name,))
            recipe = cursor_for_recipe.fetchall()[0]
            print(recipe.get("recipe_pk"))
            print("Serving size:", recipe.get("serving_size"))
            print("Time:", recipe.get("time"), "minutes")
            print("Difficultly:", recipe.get("level"))
            cursor_for_recipe.close()
            self.recipe_cuisines_display(name)
            self.recipe_types_display(name)
            self.recipe_ingredients_display(name)
            self.recipe_supplies_display(name)
        except (IndexError, pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Recipe Not Found")
            self.recipes_section()

    def recipe_ingredients_display(self, recipe_pk):
        print("Ingredients:")
        cursor_for_ingredient = self.connection.cursor()
        cursor_for_ingredient.callproc("select_ingredient_quantity", (recipe_pk,))
        i = 1
        for row in cursor_for_ingredient.fetchall():
            name = row.get('ingredient')
            quantity = row.get('amount')
            print(i.__str__() + ".", quantity, name)
            i += 1
        cursor_for_ingredient.close()

    def recipe_supplies_display(self, recipe_pk):
        print("Supplies:")
        cursor_for_supply = self.connection.cursor()
        cursor_for_supply.callproc("select_supplies_quantity", (recipe_pk,))
        i = 1
        for row in cursor_for_supply.fetchall():
            name = row.get('supply')
            quantity = row.get('amount')
            size = row.get('size')
            print(i.__str__() + ".", quantity, size, name)
            i += 1
        cursor_for_supply.close()

    def recipe_cuisines_display(self, recipe_pk):
        print("Cuisines:")
        cursor_for_cuisine = self.connection.cursor()
        cursor_for_cuisine.callproc("select_cuisine_recipe", (recipe_pk,))
        i = 1
        for row in cursor_for_cuisine.fetchall():
            name = row.get('cuisine')
            print(i.__str__() + ".", name)
            i += 1
        cursor_for_cuisine.close()

    def recipe_types_display(self, recipe_pk):
        print("Types:")
        cursor_for_type = self.connection.cursor()
        cursor_for_type.callproc("select_type_recipe", (recipe_pk,))
        i = 1
        for row in cursor_for_type.fetchall():
            name = row.get('type')
            print(i.__str__() + ".", name)
            i += 1
        cursor_for_type.close()

    # cuisines

    def cuisines_section(self):
        self.cuisines_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add cuisine: add\n"
              "To view, edit, or delete cuisine: [cuisine name]")
        command = input()
        if command.lower() == "home":
            self.homepage_section()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.cuisines_add()
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
            self.connection.commit()
            self.cuisines_section()
        except pymysql.err.IntegrityError:
            print("Invalid Name, Try Again")
            self.cuisines_add()

    def cuisines_delete(self, cuisine_name):
        try:
            cursor_for_cuisines_add = self.connection.cursor()
            cursor_for_cuisines_add.callproc("delete_cuisine", (cuisine_name,))
            cursor_for_cuisines_add.close()
            self.connection.commit()
            self.cuisines_section()
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Invalid Name")
            self.cuisines_section()

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
              "To delete cuisine: delete\n"
              "To update cuisine name: update")
        command = input()
        if command == "home":
            self.homepage_section()
        elif command == "exit":
            self.exit()
        elif command.lower() == "delete":
            self.cuisines_delete(command_new)
        elif command == "update":
            print("Enter new name for cuisine:")
            name = input().__str__()
            try:
                cursor_for_cuisines_add = self.connection.cursor()
                cursor_for_cuisines_add.callproc("update_cuisine", (command_new, name,))
                cursor_for_cuisines_add.close()
                self.connection.commit()
                self.cuisine_display(name)
            except (pymysql.err.IntegrityError, pymysql.err.DataError):
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
              "To view, edit, or delete type: [type name]")
        command = input().__str__()
        if command.lower() == "home":
            self.homepage_section()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.type_add()
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

    def type_add(self):
        print("Enter type name to add:")
        type_name = input().__str__()
        try:
            cursor_for_type_add = self.connection.cursor()
            cursor_for_type_add.callproc("insert_type", (type_name,))
            cursor_for_type_add.close()
            self.connection.commit()
            self.types_section()
        except pymysql.err.IntegrityError:
            print("Invalid Fields")
            self.types_section()

    def type_delete(self, type_name):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_type", (type_name,))
            cursor.close()
            self.connection.commit()
            self.types_section()
        except pymysql.err.IntegrityError:
            print("Cannot delete type, used in recipe")
            self.types_section()


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
              "To delete type name: delete\n"
              "To update type name: update")
        command = input()
        if command.lower() == "home":
            self.homepage_section()
        elif command.lower() == 'exit':
            self.exit()
        elif command.lower() == 'delete':
            self.type_delete(type_pk)
        elif command.lower() == "update":
            self.type_update_name(type_pk)
        else:
            print("Invalid Command")
            self.type_display(type_pk)

    def type_update_name(self, type_pk):
        print("Enter new name for type")
        new_type_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("update_type_name", (type_pk,new_type_name,))
            cursor.close()
            self.connection.commit()
            self.type_display(new_type_name)
        except (pymysql.err.IntegrityError, IndexError):
            print("New type name is invalid, try again")
            self.type_update_name(type_pk)

    # Reviews
    def reviews_section(self):
        self.reviews_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add review: add\n"
              "To view or delete review: [review name]")
        command = input().__str__()
        if command.lower() == "home":
            self.homepage_section()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.review_add()
        else:
            self.review_display(command)

    def reviews_display_all(self):
        print("Reviews:")
        cursor_for_review_names = self.connection.cursor()
        cursor_for_review_names.callproc("select_reviews")
        i = 1
        for row in cursor_for_review_names.fetchall():
            review = row.get('review_pk')
            print(i.__str__() + ".", review)
            i += 1
        cursor_for_review_names.close()

    def review_add(self):
        print("Enter recipe name to add review to:")
        recipe_name = input().__str__()
        print("Enter review title:")
        review_name = input().__str__()
        print("Enter number of starts as an integer:")
        stars = input().__str__()
        print("Enter your review for that recipe:")
        review = input().__str__()
        try:
            cursor_for_type_add = self.connection.cursor()
            cursor_for_type_add.callproc("insert_review", (review_name, recipe_name, stars, review,))
            cursor_for_type_add.close()
            self.connection.commit()
            self.review_display(review_name)
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Unable to add review")
            self.reviews_section()

    def review_delete(self, review_name):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_review", (review_name,))
            cursor.close()
            self.connection.commit()
            self.reviews_section()
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Cannot delete review, does not exist")
            self.reviews_section()

    def review_display(self, review_pk):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("select_review", (review_pk,))
            review_fields = cursor.fetchall()[0]
            print("Review:", review_fields.get("review_pk"))
            print("Recipe:", review_fields.get("recipe_fk"))
            print("Stars:", review_fields.get("stars"))
            print("Review:", review_fields.get("review_text"))
            cursor.close()
            print("Commands:\nGo back to homepage: home\n"
                  "To exit: exit\n"
                  "To delete review: delete"
                  "To go back to reviews: reviews")
            command = input()
            if command.lower() == "home":
                self.homepage_section()
            elif command.lower() == 'exit':
                self.exit()
            elif command.lower() == 'delete':
                self.review_delete(review_pk)
            elif command.lower() == 'reviews':
                self.reviews_section()
            else:
                print("Invalid command")
                self.review_display(review_pk)
        except (pymysql.err.IntegrityError, IndexError, pymysql.err.DataError):
            print("Review not found")
            self.reviews_section()

    # Ingredients
    def ingredient_section(self):
        self.ingredients_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add ingredient: add\n"
              "To view, edit, or delete ingredient: [Ingredient name]")
        command = input().__str__()
        if command.lower() == "home":
            self.homepage_section()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.ingredient_add()
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
            self.connection.commit()
            self.ingredient_section()
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Invalid Fields")
            self.ingredient_section()

    def ingredient_delete(self, ingredient_name):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_ingredient", (ingredient_name,))
            cursor.close()
            self.connection.commit()
            self.ingredient_section()
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Unable to delete ingredient")
            self.ingredient_section()

    def ingredient_display(self, ingredient_pk):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("select_ingredient", (ingredient_pk,))
            ingredient = cursor.fetchall()[0]
            print("Ingredient:", ingredient.get("ingredient_pk"))
            print("Storage:", ingredient.get("storage"))
            cursor.close()
            self.connection.commit()
            self.ingredient_update(ingredient_pk)
        except (pymysql.err.IntegrityError, pymysql.err.DataError, IndexError):
            print("Ingredient not found")
            self.ingredient_section()

    def ingredient_update(self, ingredient_pk):
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To go back to all ingredients: ingredients\n"
              "To delete ingredient: delete\n"
              "To update ingredient: update")
        command = input()
        if command.lower() == "home":
            self.homepage_section()
        elif command.lower() == 'exit':
            self.exit()
        elif command.lower() == 'delete':
            self.ingredient_delete(ingredient_pk)
        elif command.lower() == 'ingredients':
            self.ingredient_section()
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
            self.connection.commit()
            self.ingredient_display(new_ingredient_name)
        except (pymysql.err.IntegrityError, IndexError, pymysql.err.DataError):
            print("New ingredient name is invalid")
            self.ingredient_display(ingredient_pk)

    def ingredient_update_storage(self, ingredient_pk):
        print("Enter new storage for ingredient")
        new_storage_name = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("update_ingredient_storage", (ingredient_pk, new_storage_name,))
            cursor.close()
            self.connection.commit()
            self.ingredient_display(ingredient_pk)
        except (pymysql.err.OperationalError, IndexError, pymysql.err.DataError):
            print("Invalid storage name")
            self.ingredient_display(ingredient_pk)

    #Supplies
    def supply_section(self):
        self.supplies_display_all()
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To add supply: add\n"
              "To view, edit, or delete supply: [supply name]")
        command = input().__str__()
        if command.lower() == "home":
            self.homepage_section()
        elif command.lower() == "exit":
            self.exit()
        elif command.lower() == "add":
            self.supply_add()
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
            self.connection.commit()
            self.supply_section()
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
            print("Invalid Fields")
            self.supply_section()

    def supply_delete(self, supply_name):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("delete_supply", (supply_name,))
            cursor.close()
            self.connection.commit()
            self.supply_section()
        except (pymysql.err.IntegrityError, pymysql.err.DataError):
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
            self.connection.commit()
            self.supply_update(supply_pk)
        except (pymysql.err.IntegrityError, IndexError, pymysql.err.DataError):
            print("Supply not found")
            self.supply_section()

    def supply_update(self, supply_pk):
        print("Commands:\nGo back to homepage: home\n"
              "To exit: exit\n"
              "To go back to all supplies: supplies\n"
              "To delete supply: delete\n"
              "To update supply: update")
        command = input()
        if command.lower() == "home":
            self.homepage_section()
        elif command.lower() == 'exit':
            self.exit()
        elif command.lower() == 'supplies':
            self.supply_section()
        elif command.lower() == 'delete':
            self.supply_delete(supply_pk)
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
            self.connection.commit()
            self.supply_display(new_supply_name)
        except (pymysql.err.IntegrityError, IndexError, pymysql.err.DataError):
            print("New supply name is invalid")
            self.supply_display(supply_pk)

    def supply_update_size(self, supply_pk):
        print("Enter new size for supply")
        new_size = input().__str__()
        try:
            cursor = self.connection.cursor()
            cursor.callproc("update_supply_size", (supply_pk, new_size,))
            cursor.close()
            self.connection.commit()
            self.supply_display(supply_pk)
        except (pymysql.err.OperationalError, IndexError, pymysql.err.DataError):
            print("Invalid storage name")
            self.supply_display(supply_pk)


# test comment for commit
controller = enter()
