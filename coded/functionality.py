from coded.globalvar import *
import telebot
from telebot import types
from coded.recipe import Recipe
from coded.ingredient import Ingredient 
import random

@bot.message_handler(content_types=['text'])
def main_handler(message):
    match message.text:
        case Buttons.start_russian_:
            start_command(message)
        case Buttons.help_russian_:
            help_command(message)
        case Buttons.add_recipe_russian_:
            add_recipe(message)
        case Buttons.recipes_russian_:
            look_at_recipes(message)
        case Buttons.recipe_concrete_russian_:
            concrete_look(message)
        case Buttons.clear_russian_:
            clear_database(message)
        case _:
            bot.send_message(message.chat.id, "Не знаю такой команды")
        
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
    
    help_button = types.KeyboardButton(Buttons.help_russian_)
    add_recipe_button = types.KeyboardButton(Buttons.add_recipe_russian_)
    recipes_button = types.KeyboardButton(Buttons.recipes_russian_)
    recipe_concrete_button = types.KeyboardButton(Buttons.recipe_concrete_russian_)
    
    markup.add(help_button, add_recipe_button, recipes_button, recipe_concrete_button)
    
    bot.send_message(message.chat.id, 'Данный бот предназначен для хранения и просмотра рецептов, что вы хотите сделать?', reply_markup=markup)
    
def help_command(message):
    bot.send_message(message.chat.id, Messages.help_message_)

def add_recipe(message):
    new_recipe = Recipe()
    
    temporary_list.append(new_recipe)
    
    bot.send_message(message.chat.id, "Введите название рецепта")
    
    bot.register_next_step_handler(message, get_name, len(temporary_list) - 1)
    
def get_name(message, index):
    temporary_list[index].name = message.text
    menu_recipe_ingredients(message, index)
    
def menu_recipe_ingredients(message, index):
    markup = types.InlineKeyboardMarkup(row_width = 2)
    
    add_ingredient_button = types.InlineKeyboardButton(Buttons.add_ingredient_, callback_data="add_ingredient|" + str(index))
    enough_ingredients_button = types.InlineKeyboardButton(Buttons.enough_ingredients_, callback_data="enough_ingredients|" + str(index))
    
    markup.add(add_ingredient_button, enough_ingredients_button)
    
    bot.send_message(message.chat.id, "Вы хотите добавить ингредиент? Их сейчас " + str(len(temporary_list[index].ingredients)), reply_markup = markup)

@bot.callback_query_handler(func = lambda call: call.data.startswith("add_ingredient"))
def add_ingredient(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split('|')[1])
    bot.send_message(call.message.chat.id, "Введите название ингредиента (не используйте символ |)")
    bot.register_next_step_handler(call.message, add_ingredient_name, index)

@bot.callback_query_handler(func = lambda call: call.data.startswith("enough_ingredients"))    
def enough_ingredients(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split("|")[1])
    menu_recipe_instructions(call.message, index)
    
def add_ingredient_name(message, index):
    if '|' in message.text:
        bot.send_message(message.chat.id, "Нельзя использовать символ |, попробуйте ещё раз")
        bot.register_next_step_handler(message, add_ingredient_name, index)
        return
    stored = message.text + "|" + str(index)
    
    markup = types.InlineKeyboardMarkup(row_width = 3)
    
    volume_button = types.InlineKeyboardButton(Buttons.volume_, callback_data="measure|volume|"+stored)
    weight_button = types.InlineKeyboardButton(Buttons.weight_, callback_data="measure|weight|"+stored)
    other_button = types.InlineKeyboardButton(Buttons.other_, callback_data="measure|other|"+stored)
    
    markup.add(volume_button, weight_button, other_button)
    
    bot.send_message(message.chat.id, "Способ измерения количества?", reply_markup = markup)

@bot.callback_query_handler(func = lambda call: call.data.startswith("measure"))
def add_ingredient_measure(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    parsed = call.data.split('|')
    
    match parsed[1]:
        case "volume":
            bot.send_message(call.message.chat.id, "Введите количество в формате: число-единица измерения, последнее либо мг, либо г, либо кг.")
        case "weight":
            bot.send_message(call.message.chat.id, "Введите количество в формате: число-единица измерения, последнее либо мл, либо л")
        case "other":
            bot.send_message(call.message.chat.id, "Введите количество (не используйте знак |)")
    
    bot.register_next_step_handler(call.message, last_step_ingredient, parsed)
    
def last_step_ingredient(message, parsed):
    if "|" in message.text:
        bot.send_message(message.chat.id, "Неверный формат, попробуйте ещё раз")
        bot.register_next_step_handler(message, last_step_ingredient, parsed)
        return
    index = int(parsed[-1])
    match parsed[1]:
        case "volume":
             parsed_amount = message.text.split("-")
             if len(parsed_amount) != 2 or not parsed_amount[0].isdigit() or not parsed_amount[1] in ['мг', 'г', 'кг']:
                 bot.send_message(message.chat.id, "Неверный формат, попробуйте ещё раз")
                 bot.register_next_step_handler(message, last_step_ingredient, parsed)
                 return
             match parsed_amount[1]:
                 case 'мг':
                     temporary_list[index].add_ingredient(Ingredient(parsed[-2], parsed_amount[0], "volume", "milligramm"))
                 case 'г':
                     temporary_list[index].add_ingredient(Ingredient(parsed[-2], parsed_amount[0], "volume", "gramm"))
                 case 'кг':
                     temporary_list[index].add_ingredient(Ingredient(parsed[-2], parsed_amount[0], "volume", "kilogramm"))
        case "weight":
            parsed_amount = message.text.split("-")
            if len(parsed_amount) != 2 or not parsed_amount[0].isdigit() or not parsed_amount[1] in ['мл', 'л']:
                bot.send_message(message.chat.id, "Неверный формат, попробуйте ещё раз")
                bot.register_next_step_handler(message, last_step_ingredient, parsed)
                return
            match parsed_amount[1]:
                case 'мл':
                    temporary_list[index].add_ingredient(Ingredient(parsed[-2], parsed_amount[0], "volume", "milliliters"))
                case 'л':
                    temporary_list[index].add_ingredient(Ingredient(parsed[-2], parsed_amount[0], "volume", "liters"))
        case "other":
            temporary_list[index].add_ingredient(Ingredient(parsed[-2], message.text, "other"))
    menu_recipe_ingredients(message, index)

def menu_recipe_instructions(message, index):
    markup = types.InlineKeyboardMarkup(row_width = 2)
    
    add_instruction_button = types.InlineKeyboardButton(Buttons.add_instruction_, callback_data = "add_instruction|" + str(index))
    enough_instructions_button = types.InlineKeyboardButton(Buttons.enough_instructions_, callback_data = "enough_instructions|" + str(index))
    
    markup.add(add_instruction_button, enough_instructions_button)
    
    bot.send_message(message.chat.id, "Какие инструкции к приготовлению?", reply_markup = markup)
    
@bot.callback_query_handler(func = lambda call: call.data.startswith("add_instruction"))
def add_instruction(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split('|')[1])
    bot.send_message(call.message.chat.id, "Введите инструкцию")
    get_instruction(call.message, index)

def get_instruction(message, index):
    temporary_list[index].add_instruction(message.text)
    bot.register_next_step_handler(message, menu_recipe_instructions, index)

@bot.callback_query_handler(func = lambda call: call.data.startswith("enough_instructions"))
def enough_instruction(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split('|')[1])
    bot.send_message(call.message.chat.id, "Ваш рецепт записан")
    lst = temporary_list[index].to_list()
    print(lst)
    data_base.add({ "recipe_listed" : lst })
    
def look_at_recipes(message):
    to_message = ""
    for recipe in data_base.getAll():
        to_message += (recipe[recipe_listed][0] + ": id " + str(recipe["id"])) + "\n"
    if to_message == "":
        bot.send_message(message.chat.id, "У ва сещё нет рецептов")
        return
    bot.send_message(message.chat.id, to_message)

def concrete_look(message):
    bot.send_message(message.chat.id, "Введите id рецепта")
    bot.register_next_step_handler(message, get_id_recipe)

def get_id_recipe(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Неправильный формат id, попробуйте ещё раз")
        bot.register_next_step_handler(message, get_id_recipe)
        return
    got = data_base.getByQuerry(querry = {"id" : int(message.text)})
    if len(got) == 0:
        bot.send_message(message.chat.id, "Рецепта с таким id не существует")
        return
    bot.send_message(message.chat.id, Recipe(fromlist = True, lst = got[0]["recipe_listed"]).to_str())
        
        
def clear_database(message):
    markup = types.InlineKeyboardMarkup(row_width = 2)
    
    yes_button = types.InlineKeyboardButton(Buttons.yes_, callback_data="clear_all")
    no_button = types.InlineKeyboardButton(Buttons.no_)
    
    bot.send_message(message.chat.id, "Вы хотите стереть все рецепты?", reply_markup = markup)

@bot.callback_query_handler(func = lambda call: call.data == "clear_all")
def clear_all(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.id, "Всё очищено")
    data_base.deleteAll()