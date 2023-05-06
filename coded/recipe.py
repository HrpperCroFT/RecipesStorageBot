from coded.globalvar import *
from coded.ingredient import *
from telebot import types

class Recipe:
    ingredients = []
    def __init__(self, fromlist = False, lst = []):
        self.ingredients = []
        if fromlist:
            self.name = lst[0]
            self.instructions = lst[2]
            for ingr in lst[1]:
                self.ingredients.append(Ingredient(fromlist = True, lst = ingr))
            return
        self.instructions = []
    
    def add_ingredient(self, ingredient_):
        self.ingredients.append(ingredient_)
    
    def add_instruction(self, instruction):
        self.instructions.append(instruction)
        
    def to_list(self):
        result = [self.name]
        result_ingredients = []
        for ingr in self.ingredients:
            result_ingredients.append(ingr.to_list())
        result.append(result_ingredients)
        result.append(self.instructions)
        return result
    
    def to_str(self):
        result = self.name + "\n"
        result += "Требуется: \n"
        for ingr in self.ingredients:
            result += "* " + ingr.to_str() + "\n"
        result += "Приготовление: \n"
        for i in range(len(self.instructions)):
            result += str(i) + ". " + instructions.to_str + "\n"
        return result