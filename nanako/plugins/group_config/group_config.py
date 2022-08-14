import json
import logging
import re
from pathlib import Path
from sys import stdout

GroupConfigLogger = logging.getLogger('GroupConfig')
GroupConfigLogger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(stream=stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
GroupConfigLogger.addHandler(console_handler)

file_handler = logging.FileHandler(filename=str(Path('log/').absolute()) + '/' + 'all.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s, %(levelname)s, %(module)s: %(message)s'))
GroupConfigLogger.addHandler(file_handler)

GROUP_CONFIG = {}
DEFAULT_CONFIG = {
    'faq': True,  # 是否开启faq（True/False）
    'faq_db_name': None,  # 数据库名称，如果`faq`为False则该项无效（None/Str）
    # 如果为`None`则使用默认数据库`questions.json`
    # 如果为`'123'`则数据库名称为`questions_123.json`
    'admin_id': ['879157739'],  # 群功能管理员，有权修改config参数，需要手动赋权（List）
    'poke': True,  # 戳某人 戳@某人（True/False）
    'what_to_drink': True,  # 今晚吃啥
}
TRANSLATE_KEY = {
    'admin': '管理员模式',
    'chinese': '中文模式',
    'cai': '卖弱',
    'loving': '表白',
    'answer_book': '答案之书',
    'picture': '懂的都懂',
    'luck': '运气王检测',
    'couplet': '对联',
    'eat': '今晚吃啥'
}
CONFIG_PATH = 'config/'


# CHANGE_FLAG = False  # 优化IO次数：True:变化了，False:没有变化


def load_group_config():
    global GROUP_CONFIG
    if not Path(f'{CONFIG_PATH}group_config.json').is_file():
        Path(f'{CONFIG_PATH}group_config.json').write_text(r'{}')
    GROUP_CONFIG = json.loads(Path(f'{CONFIG_PATH}group_config.json').read_text('utf-8'))
    for group in GROUP_CONFIG:
        for item in DEFAULT_CONFIG.keys():
            if not GROUP_CONFIG[group].__contains__(item):
                GROUP_CONFIG[group][item] = DEFAULT_CONFIG[item]
    Path(f'{CONFIG_PATH}group_config.json').write_text(
        json.dumps(
            GROUP_CONFIG,
            ensure_ascii=False,
            indent=2
        ),
        'utf-8'
    )
    GroupConfigLogger.debug(f'加载完成')


def save_group_config():
    Path(f'{CONFIG_PATH}group_config.json').write_text(
        json.dumps(
            GROUP_CONFIG,
            ensure_ascii=False,
            indent=2
        ),
        'utf-8'
    )
    GroupConfigLogger.debug(f'写入完成')
    load_group_config()


# 原始msg为`group config <QQ_Group_ID> <Option> <Parameter>`
# <QQ_Group_ID>缺省为evnet所在群，可选
# 1. 把群聊加入群功能列表（必须由1299946476操作）
# add（在那个群说）
# 912296291 add（任意群聊）
# 2. 修改群功能（Enable/Disable）
# enable/disable faq（在那个群说）
# 912296291 enable/disable faq（任意群聊）
# <Parameter> = faq admin voice latex
# 3. 添加本群管理员
# enable/disable <QQ_ID>（在那个群说）
# 912296291 enable/disable <QQ_ID>（任意群聊）
# 4. 查询配置
# query（在那个群说）
# 912296291 query（任意群聊）
# 5. 帮助
# help

# 传入的msg必然是没有<QQ_Group_ID>的形式，即msg=<Option> <Parameter>
# <QQ_Group_ID>在`qq_group`参数里


def change_group_config(operator_id, qq_group, msg):
    qq_group = str(qq_group)
    operator_id = operator_id
    # TODO: 把这一大段逻辑拆成鉴权和执行两块
    # def jianquan(peopleId, groupId, opType) -> bool:
    #     pass
    #
    # def exec() -> None:
    #     pass
    # if not jianquan():
    #     return
    # 检查操作正确性
    # exec()
    if qq_group not in list(GROUP_CONFIG.keys()):
        if str(operator_id) != '1299946476':
            return f'用户【{operator_id}】无权操作'
        else:
            if msg in ['add']:
                GROUP_CONFIG[qq_group] = DEFAULT_CONFIG
                save_group_config()
                return f'群聊【{qq_group}】添加完成，启动默认配置'
            else:
                return f'群聊【{qq_group}】尚未添加'
    else:
        if str(operator_id) not in GROUP_CONFIG[qq_group]['admin_id']:
            if msg.strip() == 'help':
                return str('命令模板：group config <群号> <操作> <参数>\n'
                           '<群号>缺省为所在群，可选\n'
                           '<操作>内容如下\n'
                           'add：把群聊加入群功能列表，无参数'
                           'enable/disable：开启/关闭功能，参数为功能代号，如'
                           # msg_help += f"{'、'.join(x + ':' + TRANSLATE_KEY[x] for x in TRANSLATE_KEY)}"
                           f"{'、'.join(x for x in TRANSLATE_KEY)}\n"
                           'enable/disable：添加/删除本群管理员，参数为QQ号\n'
                           'query：查询配置信息\n'
                           'help：打开帮助\n')
            return f'用户【{operator_id}】无权操作'
        else:
            id_list = []
            if msg == '':
                return f'参数错误'
            elif len(msg.split(' ')) == 1:
                option = msg.split(' ')[0].strip()
                parameter = None
            else:
                option = msg.split(' ')[0].strip()
                parameter = msg.split(' ')[1].strip()
                id_list = re.findall(r"\d+\.?\d*", parameter)
            # print('Parameter', parameter)
            if option in ['Enable', 'enable']:
                if parameter in (['faq'] + (list(TRANSLATE_KEY.keys()))):
                    GROUP_CONFIG[qq_group][parameter] = True
                    save_group_config()
                    return f'已修改\n' + get_config_text(qq_group)
                if id_list:
                    if id_list[0] not in GROUP_CONFIG[qq_group]['admin_id']:
                        GROUP_CONFIG[qq_group]['admin_id'].append(id_list[0])
                        save_group_config()
                    return f'已修改\n' + get_config_text(qq_group)
            if option in ['Disable', 'disable']:
                if parameter in (['faq'] + (list(TRANSLATE_KEY.keys()))):
                    GROUP_CONFIG[qq_group][parameter] = False
                    save_group_config()
                    return f'已修改\n' + get_config_text(qq_group)
                if id_list:
                    if id_list[0] == '1299946476':
                        return f'无法移除主人哦'
                    if id_list[0] in GROUP_CONFIG[qq_group]['admin_id']:
                        GROUP_CONFIG[qq_group]['admin_id'].remove(id_list[0])
                        save_group_config()
                        return f'已修改\n' + get_config_text(qq_group)
                    else:
                        return f'用户【{id_list[0]}】不在列表内'
            if option in ['query', 'Query']:
                return get_config_text(qq_group)
            if option in ['change', 'Change']:
                if parameter in ['None', 'NONE', 'none']:
                    GROUP_CONFIG[qq_group]['faq_db_name'] = None
                else:
                    GROUP_CONFIG[qq_group]['faq_db_name'] = parameter
                save_group_config()
                return f'已修改\n' + get_config_text(qq_group)
            if option in ['help', '--h', '帮助']:
                msg_help = str('命令模板：group config <群号> <操作> <参数>\n'
                               '<群号>缺省为所在群，可选\n'
                               '<操作>内容如下\n'
                               'add：把群聊加入群功能列表，无参数'
                               'enable/disable：开启/关闭功能，参数为功能代号，如'
                               # msg_help += f"{'、'.join(x + ':' + TRANSLATE_KEY[x] for x in TRANSLATE_KEY)}"
                               f"{'、'.join(x for x in TRANSLATE_KEY)}\n"
                               'enable/disable：添加/删除本群管理员，参数为QQ号\n'
                               'query：查询配置信息\n'
                               'help：打开帮助\n')
                return msg_help
            if msg in ['add']:
                GROUP_CONFIG[qq_group] = DEFAULT_CONFIG
                save_group_config()
                return f'群聊【{qq_group}】添加完成，启动默认配置'
            return f'参数错误'


def get_config_text(qq_group):
    msg = ""
    msg += get_icon(GROUP_CONFIG[qq_group]['faq']) + '自助答疑\n'
    if GROUP_CONFIG[qq_group]['faq']:
        msg += '     问答库：' + (GROUP_CONFIG[qq_group]
                                 ['faq_db_name'] or 'Default') + '\n'
    for item in TRANSLATE_KEY:
        msg += get_icon(GROUP_CONFIG[qq_group][item]
                        ) + TRANSLATE_KEY[item] + '\n'
    msg += '     本群管理员列表：'
    msg += f"{'、'.join(x for x in GROUP_CONFIG[qq_group]['admin_id'])}"
    return msg


# TODO: 添加光栅化
def get_icon(flag):
    if flag:
        return ' √ '
    else:
        return '     '

# print(change_group_config(1299946476, 1111, 'enable loving'))