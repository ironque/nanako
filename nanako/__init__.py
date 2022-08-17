import nonebot


def load_plugins():
    nonebot.load_builtin_plugins("echo")
    nonebot.load_plugin("nanako.plugins.roll_luck")
    # nonebot.load_plugin("nanako.plugins.group")
    nonebot.load_plugin("nanako.plugins.tietie")
    nonebot.load_plugin("nanako.plugins.what_to_drink")
    nonebot.load_plugin("nonebot_plugin_heisi")
    nonebot.load_plugin("nanako.plugins.recent")
    # nonebot.load_plugin("nanako.plugins.just_for_test")
    nonebot.load_plugin("nonebot_plugin_atri")
    nonebot.load_plugin("nanako.plugins.answerbook")
