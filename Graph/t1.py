# encoding: utf-8
import json, re


def read_json(path):
    try:
        with open(path, encoding='utf-8') as file:
            content = json.load(file)
        return content
    except Exception as e:
        # ExceptionInfo(e)
        print(e)
        return {}


js = read_json('D:\SYR\\20200301_public\demo2.json')
pass


def is_person_name(name):
    """
    判断一个名称是人名还是公司名称，输入不能为其他类别
    :param name:
    :return:
    """
    _ = [1 if x in name else 0 for x in ['公司', '']]
    pass


class QccRequest:

    def __init__(self, ReturnString):
        if isinstance(ReturnString, dict):
            pass
        else:
            try:
                ReturnString = eval(ReturnString)
            except Exception:
                raise TypeError('')
        self.name = ReturnString['name']
        self.metaModel = ReturnString['metaModel']
        self.url = ReturnString['url']
        self.headers = ReturnString['headers']
        self.get = ReturnString['get']
        self.update_date = ReturnString['date']
        self.id = ReturnString['url']
        self.content = ReturnString['content']
        pass

    def content_keys(self):
        pass


class BaseInfo(QccRequest):

    def __init__(self, ReturnString):
        QccRequest.__init__(ReturnString)
        if self.metaModel != '基本信息':
            raise TypeError('')

        self.BaseAttributes = {}
        pass

    def certifications(self):
        """
        处理->认证信息
        :return:
        """
        ctf = self.content['认证信息']
        ctf_keys = ctf.keys()
        ks = ['电话', '官网', '邮箱', '地址', '简介']
        tel = re.search('\d+[-]\d+', ctf['电话'])
        tel = tel.group(0) if tel is not None else None
        for k in ks:
            self.BaseAttributes[k] = ctf[k] if k in ctf_keys else None
        pass

    def business(self):
        """

        :return:
        """
        bs = self.content['工商信息']
        # 法人代表特殊处理
        legal_rep = bs['法人代表']

        pass


pass
