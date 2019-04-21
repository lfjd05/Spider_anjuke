"""
   数据处理成可以被转可视化的形式
"""
import pandas as pd
import os
import re


# 读取所有文件夹名字
file_name_list = []
for root, _, names in os.walk('D:\python Programme\Spider_anjuke\data'):
    for file_name in names:
        file_name_list.append(os.path.join(root, file_name))

# 逐个打开文件处理
output_data = pd.DataFrame(columns=['name', 'type', 'value', 'date'])
for file_name in file_name_list:
    try:
        file = pd.read_csv(file_name, index_col=None, header=None, encoding='gbk')
    except UnicodeDecodeError:
        file = pd.read_csv(file_name, index_col=None, header=None, encoding='utf-8')
    file.columns = ['索引', '类型', '城市', '月', '价格', '省', '涨幅', '年']

    city_name = []
    type_name = []
    value_price = []
    data_name = []
    # 分组，正常应该一组是76个，如果不是就扔掉
    group = file.groupby('城市')
    drop_city_list = group.count()[group.count()['索引'] != 76].index.tolist()
    print('缺数据的城市', drop_city_list)
    for drop_city in drop_city_list:
        file = file[file['城市'] != drop_city]

    for index, line in file.iterrows():
        city_name.append(line['城市'])
        type_name.append(line['城市'])
        try:
            value_price.append(re.search('\d+', line['价格']).group())
        except AttributeError:
            # 这个城市没用找到价格
            value_price.append('0')
        data_name.append(str(line['年'])+'-'+str(line['月']))

    data = pd.DataFrame({'name': city_name, 'type': type_name, 'value': value_price, 'date': data_name},
                               index=None, columns=['name', 'type', 'value', 'date'])
    output_data = output_data.append(data, ignore_index=True)

output_data.to_csv('D:\python Programme\Historical-ranking-data-visualization-based-on-d3.js-master/全国二手房价格.csv', index=None, encoding='utf-8')

