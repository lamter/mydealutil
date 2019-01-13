# coding:utf-8
from collections import OrderedDict

try:
    import ConfigParser as configparser
except ImportError:
    import configparser


class MyConfigParser(configparser.SafeConfigParser):
    NONE = ['none', 'null', '']

    def __init__(self, is_origin_optionxform=False, *args, **kwargs):
        self.is_origin_optionxform = is_origin_optionxform
        configparser.SafeConfigParser.__init__(self, *args, **kwargs)

    def autoget(self, section, option):
        """
        从已经自动转化格式的数值结构里面获取数值
        :param section:
        :param option:
        :return:
        """
        data = self.get(section, option)
        if (data.startswith('"') and data.endswith('"')) or (data.startswith("'") and data.endswith("'")):
            # 强制纯文本
            return data[1:-1]

        if data.lower() in self.NONE:
            # None 值
            return None

        # 尝试转换成 bool int float
        for func in [self.getboolean, self.getint, self.getfloat]:
            try:
                return func(section, option)
            except ValueError:
                pass

        # 没有引号的字符串
        return data

    def optionxform(self, optionstr):
        """
        原库中将 option 全部设置为小写，这里设置为不改动
        :param optionstr:
        :return:
        """
        return super(MyConfigParser, self).optionxform(optionstr) if self.is_origin_optionxform else optionstr

    def autoitems(self, section):
        """
        自动获取
        :return:
        """
        return [(option, self.autoget(section, option)) for option in self.options(section)]
