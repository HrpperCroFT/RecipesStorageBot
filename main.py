from coded.globalvar import *
from coded.functionality import *

if __name__ == "__main__":
    #bot.message_handler(start_command, commands=["start"])
    #bot.message_handler(help_command, commands=["help"])
    #bot.message_handler(add_recipe, commands=["add_recipe"])
    #bot.message_handler(look_at_recipes, commands=["recipes"])
    #bot.message_handler(concrete_look, commands=["recipe"])
    #bot.message_handler(clear_database, commands=["clear_storage"])
    bot.polling(non_stop = True)