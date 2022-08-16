import time


def get_account(id_string: str):
    account = ""
    for i in id_string:
        if i.isdigit():
            account += i
    return account


def today():
    time_str = time.strftime("%Y%m%d") + "\n"
    return time_str


def convert_to_ans(data: list[dict]):
    battles = 0
    result = today()  # 时间
    for ship in data:
        battles += ship['shipInfo']['battles']
        result += "\t" + ship['shipInfo']['shipInfo']['nameCn'] + ' :\n'  # 船名
        result += "场数: " + str(ship['shipInfo']['battles']) + '\t\t\t\t\t胜率: ' + str(
            ship['shipInfo']['wins']) + "%\n"
        result += "Pr: " + str(ship['shipInfo']['pr']['value']) + "\t伤害:" + str(ship['shipInfo']['damage']) + '\t' + \
                  str(ship['shipInfo']['pr']['name']) + '\n'

    return result
