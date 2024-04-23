from coded.globalvar import *
from coded.ingredient import *
from telebot import types

class Recipe:
    """ This class contains full information about recipe """
    
    ingredients = []
    def __init__(self, fromlist = False, lst = []):
        self.ingredients = []
        self.name = ""
        self.instructions = []
    

    def add_ingredient(self, ingredient_):
        """ Adds new ingredient to this recipe """
        
        self.ingredients.append(ingredient_)
    

    def add_instruction(self, instruction):
        """ Adds new instruction to this recipe """
        
        self.instructions.append(instruction)
    
    
    def to_list(self):
        """ Converts information about recipe to string """
        
        result = [self.name]
        result.append(self.to_str())
        return result
    

    def to_str(self):
        """ Converts information about recipe to string """
        
        result = self.name + "\n"
        
        result += "Требуется: \n"
        for ingr in self.ingredients:
            result += "* " + ingr.to_str() + "\n"
        
        result += "Приготовление: \n"
        for i in range(len(self.instructions)):
            result += str(i + 1) + ". " + self.instructions[i] + "\n"
        
        return result