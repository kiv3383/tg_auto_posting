from auto_post_gasket import client
from auto_post_target_group import bot, bot_token

if __name__ == "__main__":
    client.start()
    bot.start(bot_token=bot_token)
    client.run_until_disconnected()
    bot.run_until_disconnected()
