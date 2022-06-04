from funcs import Bot
import configs

bot = Bot()
bot.connect(
    configs.server,
    configs.port,
    configs.nickname,
    configs.ident,
    configs.real_name,
    configs.nickserv_pass,
)

while 1:
    logs = bot.response_irc()
    print(logs)
    bot.join(configs.auto_join)
