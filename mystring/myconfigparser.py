# coding:utf-8
from collections import OrderedDict

try:
    import ConfigParser as configparser
except ImportError:
    import configparser


class MyConfigParser(configparser.SafeConfigParser):
    def __init__(self, auto=True, is_origin_optionxform=False, *args, **kwargs):
        self.auto = auto  # 是否自动转换格式
        self.is_origin_optionxform = is_origin_optionxform
        configparser.SafeConfigParser.__init__(self, *args, **kwargs)

        self.autoData = OrderedDict()

    def _read(self, fp, fpname):
        r = super(MyConfigParser, self)._read(fp, fpname)
        for section in self.sections():
            if section not in self.autoData:
                self.autoData[section] = OrderedDict()
            for option in self.options(section):
                data = self.get(section, option)
                if data.startswith('"') and data.endswith('"'):
                    data = data[1:-1]
                elif data.startswith("'") and data.endswith("'"):
                    data = data[1:-1]
                else:
                    for func in [self.getboolean, self.getint, self.getfloat]:
                        try:
                            data = func(section, option)
                            break
                        except ValueError:
                            pass
                self.autoData[section][option] = data
        return r
    def optionxform(self, optionstr):
        """
        原库中将 option 全部设置为小写，这里设置为不改动
        :param optionstr:
        :return:
        """
        return super(MyConfigParser, self).optionxform(optionstr) if self.is_origin_optionxform else optionstr

    def autoget(self, section, option):
        """
        尝试自动获得数据类型
        :param section:
        :param option:
        :return:
        """
        o = self.get(section, option)
        try:
            return int(o)
        except ValueError:
            pass
        try:
            return float(o)
        except ValueError:
            pass

        if o.startswith('"') and o.endswith('"'):
            o = o[1:-1]
        elif o.startswith("'") and o.endswith("'"):
            o = o[1:-1]
        return o

    def autoitems(self, section):
        """
        自动获取
        :return:
        """
        self.items()
        # return ((s, turn(o)) for s, o in super(MyConfigParser, self).items(section))


if __name__ == '__main__':
    config = MyConfigParser(auto=True)
    with open('../tmp/test.ini', 'r') as f:
        config.readfp(f)
    section = u'中文section'
    print(config.autoData)
