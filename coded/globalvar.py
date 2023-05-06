import telebot
from pysondb import db 
from coded.token import apikey
from enum import Enum

data_base = db.getDb("data/storage.json")

temporary_list = []

bot = telebot.TeleBot(apikey)

class Buttons:
    start_russian_ = "Начать"
    help_russian_ = "Помощь"
    add_recipe_russian_ = "Добавить рецепт"
    recipes_russian_ = "Покажи рецепты"
    recipe_concrete_russian_ = "Покажи конкретный рецепт"
    clear_russian_ = "Очистить хранилище рецептов"
    
    add_ingredient_ = "Добавить ингредиент"
    enough_ingredients_ = "Достаточно ингредиентов"
    
    volume_ = "Объём"
    weight_ = "Вес"
    other_ = "Другой"
    
    add_instruction_ = "Добавь инструкцию"
    enough_instructions_ = "Достаточно инструкций"
    
    yes_ = "Да"
    no_ = "Нет"

class Messages:
    help_message_ = """ Основные команды:
    Начать — /start
    Помощь — /help
    Добавить рецепт — /add_recipe
    Покажи рецепты — /recipes
    Покажи конкретный рецепт — /recipe
    Очистить хранилище рецетов — /clear_storage
    """
    
class VolumeMeasure(Enum):
    milliliters = 0
    litres = 1

class Volume:
    measure = VolumeMeasure.milliliters
    amount = 0
    def __init__(self, measure_, amount_):
        self.amount = amount_
        if measure_ == "milliliters":
            self.measure = VolumeMeasure.milliliters
        else:
            self.measure = VolumeMeasure.litres
    
    def to_str(self):
        result = str(self.amount)
        if self.measure == VolumeMeasure.milliliters:
            result += " мл"
        else:
            result += " л"
        return result

class WeightMeasure(Enum):
    milligramm = 0
    gramm = 1
    kilogramm = 2

class Weight:
    measure = WeightMeasure.milligramm
    amount = 0
    def __init__(self, measure_, amount_):
        self.amount = amount_
        if measure_ == "milligramm":
            self.measure = WeightMeasure.milligramm
        elif measure_ == "gramm":
            self.measure = WeightMeasure.gramm
        else:
            self.measure = WeightMeasure.kilogramm
    
    def to_str(self):
        result = str(self.amount)
        if self.measure == VolumeMeasure.milligramm:
            result += " мг"
        elif self.measure == WeightMeasure.gramm:
            result += " г"
        else:
            result += " кг"
        return result

class OtherMeasurement:
    amount = ""
    def __init__(self, amount):
        self.amount = amount
    
    def to_str(self):
        return self.amount
    
    def to_list(self):
        return [2, self.amount]