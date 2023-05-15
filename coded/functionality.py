from coded.globalvar import *
import telebot
from telebot import types
from coded.recipe import Recipe
from coded.ingredient import Ingredient 
import random
import os
            
@bot.message_handler(commands=["start"])
def start_command(message):
    """ Shows start menu """
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
    
    help_button = types.KeyboardButton(Buttons.help_russian_)
    add_recipe_button = types.KeyboardButton(Buttons.add_recipe_russian_)
    recipes_button = types.KeyboardButton(Buttons.recipes_russian_)
    recipe_concrete_button = types.KeyboardButton(Buttons.recipe_concrete_russian_)
    
    markup.add(help_button, add_recipe_button, recipes_button, recipe_concrete_button)
    
    bot.send_message(message.chat.id, 'Данный бот предназначен для хранения и просмотра рецептов, что вы хотите сделать?', reply_markup=markup)

@bot.message_handler(commands=["help"])    
def help_command(message):
    """ Shows help message """
    
    bot.send_message(message.chat.id, Messages.help_message_)

@bot.message_handler(commands=["add_recipe"])
def add_recipe(message):
    """ Starts adding new recipe """
    
    new_recipe = Recipe()
    
    temporary_list.append(new_recipe)
    
    bot.send_message(message.chat.id, "Введите название рецепта")
    
    bot.register_next_step_handler(message, get_name, len(temporary_list) - 1)
    
def get_name(message, index):
    """ Gets name of new recipe """
    
    temporary_list[index].name = message.text
    menu_recipe_ingredients(message, index)
    
def menu_recipe_ingredients(message, index):
    """ Shows menu of adding new ingredients to this recipe """
    
    markup = types.InlineKeyboardMarkup(row_width = 2)
    
    add_ingredient_button = types.InlineKeyboardButton(Buttons.add_ingredient_, callback_data="add_ingredient|" + str(index))
    enough_ingredients_button = types.InlineKeyboardButton(Buttons.enough_ingredients_, callback_data="enough_ingredients|" + str(index))
    
    markup.add(add_ingredient_button, enough_ingredients_button)
    
    bot.send_message(message.chat.id, "Вы хотите добавить ингредиент? Их сейчас " + str(len(temporary_list[index].ingredients)), reply_markup = markup)

@bot.callback_query_handler(func = lambda call: call.data.startswith("add_ingredient"))
def add_ingredient(call):
    """ Starts ading new ingredient to recipe """
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split('|')[1])
    bot.send_message(call.message.chat.id, "Введите название ингредиента (не используйте символ |)")
    bot.register_next_step_handler(call.message, add_ingredient_name, index)

@bot.callback_query_handler(func = lambda call: call.data.startswith("enough_ingredients"))    
def enough_ingredients(call):
    """ Ends adding ingredients to recipe """
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split("|")[1])
    menu_recipe_instructions(call.message, index)
    
def add_ingredient_name(message, index):
    """ Gets name of new ingredient and shows menu of getting way of measuring """
    
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
    """ Adds measurement of new ingredient """
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    parsed = call.data.split('|')
    
    match parsed[1]:
        case "weight":
            bot.send_message(call.message.chat.id, "Введите количество в формате: число-единица измерения, последнее либо мг, либо г, либо кг.")
        case "volume":
            bot.send_message(call.message.chat.id, "Введите количество в формате: число-единица измерения, последнее либо мл, либо л")
        case "other":
            bot.send_message(call.message.chat.id, "Введите количество (не используйте знак |)")
    
    bot.register_next_step_handler(call.message, last_step_ingredient, parsed)
    
def last_step_ingredient(message, parsed):
    """ Finally adds new ingredient """
    
    if "|" in message.text:
        bot.send_message(message.chat.id, "Неверный формат, попробуйте ещё раз")
        bot.register_next_step_handler(message, last_step_ingredient, parsed)
        return
    
    index = int(parsed[-1])
    match parsed[1]:
        case "weight":
             parsed_amount = message.text.split("-")
             if len(parsed_amount) != 2 or not parsed_amount[0].isdigit() or not parsed_amount[1] in ['мг', 'г', 'кг']:
                 bot.send_message(message.chat.id, "Неверный формат, попробуйте ещё раз")
                 bot.register_next_step_handler(message, last_step_ingredient, parsed)
                 return
             match parsed_amount[1]:
                 case 'мг':
                     temporary_list[index].add_ingredient(Ingredient(parsed[-2], parsed_amount[0], "weight", "milligramm"))
                 case 'г':
                     temporary_list[index].add_ingredient(Ingredient(parsed[-2], parsed_amount[0], "weight", "gramm"))
                 case 'кг':
                     temporary_list[index].add_ingredient(Ingredient(parsed[-2], parsed_amount[0], "weight", "kilogramm"))
        case "volume":
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
    """ Shows menu of adding instructions to this recipe """
    
    markup = types.InlineKeyboardMarkup(row_width = 2)
    
    add_instruction_button = types.InlineKeyboardButton(Buttons.add_instruction_, callback_data = "add_instruction|" + str(index))
    enough_instructions_button = types.InlineKeyboardButton(Buttons.enough_instructions_, callback_data = "enough_instructions|" + str(index))
    
    markup.add(add_instruction_button, enough_instructions_button)
    
    bot.send_message(message.chat.id, "Какие инструкции к приготовлению?", reply_markup = markup)
    
@bot.callback_query_handler(func = lambda call: call.data.startswith("add_instruction"))
def add_instruction(call):
    """ Starts adding current instruction to recipe """
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split('|')[1])
    bot.send_message(call.message.chat.id, "Введите инструкцию")
    bot.register_next_step_handler(call.message, get_instruction, index)

def get_instruction(message, index):
    """ Gets full instruction text and adds it to recipe """
    
    temporary_list[index].add_instruction(message.text)
    menu_recipe_instructions(message, index)

@bot.callback_query_handler(func = lambda call: call.data.startswith("enough_instructions"))
def enough_instruction(call):
    """ Ends adding instruction and finally adds new recipe """
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split('|')[1])
    
    markup = types.InlineKeyboardMarkup(row_width = 2)
    
    add_instruction_button = types.InlineKeyboardButton(Buttons.yes_, callback_data = "add_image|" + str(index))
    enough_instructions_button = types.InlineKeyboardButton(Buttons.no_, callback_data = "no_image|" + str(index))
    
    markup.add(add_instruction_button, enough_instructions_button)
    
    bot.send_message(call.message.chat.id, "Хотите прикрепить изобржение?", reply_markup = markup)

@bot.callback_query_handler(func = lambda call: call.data.startswith("add_image"))
def add_image(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split('|')[1])
    
    bot.send_message(call.message.chat.id, "Отправьте фото. Если передумали, напишите 'Не надо фото'")
    bot.register_next_step_handler(call.message, end_adding_recipe_with_image, index)

def end_adding_recipe_with_image(message, index):
    adding_image = False
    if message.content_type != "photo":
        if not message.content_type == "text" or message.data != "Не надо фото":
            bot.send_message(message.chat.id, "Это не фото. Если передумали, напишите 'Не надо фото'")
            bot.register_next_step_handler(message, end_adding_recipe_with_image, index)
            return;
    else:
        adding_image = True
    bot.send_message(message.chat.id, "Ваш рецепт записан")
    lst = temporary_list[index].to_list()
    id_got = data_base.add({ "recipe_listed" : lst })
    if adding_image:
        if not os.path.isdir("./data/" + str(id_got)):
            os.mkdir("./data/" + str(id_got))
        raw = message.photo[2].file_id
        name = raw+".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("./data/" + str(id_got) + "/image.jpg",'wb') as new_file:
            new_file.write(downloaded_file)
     
@bot.callback_query_handler(func = lambda call: call.data.startswith("no_image"))
def no_image(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    index = int(call.data.split('|')[1])
    
    bot.send_message(call.message.chat.id, "Ваш рецепт записан")
    lst = temporary_list[index].to_list()
    data_base.add({ "recipe_listed" : lst })

@bot.message_handler(commands=["recipes"])
def look_at_recipes(message):
    """ Shows list of names of recipes with id """
    
    to_message = ""
    for recipe in data_base.getAll():
        to_message += (recipe["recipe_listed"][0] + ": id " + str(recipe["id"])) + "\n"
    if to_message == "":
        bot.send_message(message.chat.id, "У вас ещё нет рецептов")
        return
    bot.send_message(message.chat.id, to_message)

@bot.message_handler(commands=["recipe"])
def concrete_look(message):
    """ Shows concrete recipe by id """
    
    bot.send_message(message.chat.id, "Введите id рецепта")
    bot.register_next_step_handler(message, get_id_recipe)

def get_id_recipe(message):
    """ Gets id of recipe and shows it """
    
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Неправильный формат id, попробуйте ещё раз")
        bot.register_next_step_handler(message, get_id_recipe)
        return
    
    got_id = int(message.text)
    
    got = data_base.getByQuery(query = {"id" : got_id})
    
    if len(got) == 0:
        bot.send_message(message.chat.id, "Рецепта с таким id не существует")
        return
    
    if os.path.isfile("./data/" + str(got_id) + "/image.jpg"):
        img = open("./data/" + str(got_id) + "/image.jpg", 'rb')
        bot.send_photo(message.chat.id, img)
        
    bot.send_message(message.chat.id, got[0]["recipe_listed"][1])
        
@bot.message_handler(commands=["clear_storage"])
def clear_database(message):
    """ Shows menu of clearing database """
    
    markup = types.InlineKeyboardMarkup(row_width = 2)
    
    yes_button = types.InlineKeyboardButton(Buttons.yes_, callback_data="clear_all")
    no_button = types.InlineKeyboardButton(Buttons.no_, callback_data="not_clear")
    
    markup.add(yes_button, no_button)
    
    bot.send_message(message.chat.id, "Вы хотите стереть все рецепты?", reply_markup = markup)

@bot.callback_query_handler(func = lambda call: call.data == "clear_all")
def clear_all(call):
    """ Clears database """
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Всё очищено")
    data_base.deleteAll()

@bot.callback_query_handler(func = lambda call: call.data == "not_clear")
def not_clear(call):
    """ Doesn't clear database """
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Ладно")
    

@bot.message_handler(content_types=['text'])
def main_handler(message):
    """ Main comannd's handler """
    
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