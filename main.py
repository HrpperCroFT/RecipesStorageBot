from coded.globalvar import *
from coded.functionality import *

if __name__ == "__main__":
    " Registering commands in english and starting bot "
    
    bot.message_handler(commands=["start"])(start_command)
    bot.message_handler(commands=["help"])(help_command)
    bot.message_handler(commands=["add_recipe"])(add_recipe)
    bot.message_handler(commands=["recipes"])(look_at_recipes)
    bot.message_handler(commands=["recipe"])(concrete_look)
    bot.message_handler(commands=["clear_storage"])(clear_database)
    
    bot.polling(non_stop = True)