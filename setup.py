from setuptools import setup, find_packages

import mydealutil

long_desc = """
mydealutil
===============

* 封装一些通用的函数

Installation
--------------

pip install mydelutil

Upgrade
---------------

    pip install easytrader --upgrade

Quick Start
--------------

::

    import easytrader

    user = easytrader.use('ht')

    user.prepare('account.json')

    user.balance

return::

    [{ 'asset_balance': '资产总值',
       'current_balance': '当前余额',
       'enable_balance': '可用金额',
       'market_value': '证券市值',
       'money_type': '币种',
       'pre_interest': '预计利息' ]}

    user.position

return::

    [{'cost_price': '摊薄成本价',
       'current_amount': '当前数量',
       'enable_amount': '可卖数量',
       'income_balance': '摊薄浮动盈亏',
       'keep_cost_price': '保本价',
       'last_price': '最新价',
       'market_value': '证券市值',
       'position_str': '定位串',
       'stock_code': '证券代码',
       'stock_name': '证券名称'}]

    user.entrust

return::

    [{'business_amount': '成交数量',
      'business_price': '成交价格',
      'entrust_amount': '委托数量',
      'entrust_bs': '买卖方向',
      'entrust_no': '委托编号',
      'entrust_price': '委托价格',
      'entrust_status': '委托状态',  # 废单 / 已报
      'report_time': '申报时间',
      'stock_code': '证券代码',
      'stock_name': '证券名称'}]

    user.buy('162411', price=5.55)

    user.sell('16411', price=5.65)

"""
with open('requirements.txt', 'r') as f:
    install_requires = [l for l in f.readlines() if l]

setup(name='mydealutil',
      version=mydealutil.__version__,
      keywords='dealutil',
      description='封装一些通用的函数',
      long_description=long_desc,
      license='MIT',

      url='https://github.com/lamter/mydealutil',
      author='lamter',
      author_email='lamter.fu@gmail.com',

      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,

      )