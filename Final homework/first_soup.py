# 1.拿到页面源代码
# 2.使用re进行解析，拿到数据
# 3.解析后的数据存入excel中

import requests
from bs4 import BeautifulSoup
import re
import pandas
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 初始化要存入信息的容器
name = []  # 品名
cat = []  # 分类
lowPrice = []  # 最低价
highPrice = []  # 最高价
avgPrice = []  # 平均价
specInfo = []  # 规格
date = []  # 发布日期

# 1.使用requests拿到页面源代码
for cur in range(1, 8):
    url = "http://www.xinfadi.com.cn/getPriceData.html"
    dat = {
        "limit": "20",
        "current": f"{cur}"
    }
    resp = requests.post(url, data=dat)
# print(resp.text)
# with open("beauti.html", mode="w", encoding="utf-8") as f:  # windows默认 txt创建编码方式为gbk
#     f.write(resp.text)
    print(f"over!, {cur}")


# 2.使用re进行解析，拿到数据
# result = re.finditer("\"prodName\":\"(?P<name>.*?)\"", resp.text)  # 使用finditer出错
# for it in re.finditer("\"prodName\":\"(?P<name>.*?)\"", resp.text):
#     print(it.group("name"))
#     bf = it.group("name").string
#     name.append(str(bf))
# print(name)
    for it in re.findall("\"prodName\":\"(.*?)\".*?\"prodCat\":\"蔬菜\".*?\"prodPcat\":\"(.*?)\".*?\"lowPrice\":\"(.*?)\".*?\"highPrice\":\"(.*?)\".*?\"avgPrice\":\"(.*?)\".*?\"specInfo\":\"(.*?)\".*?\"pubDate\":\"(\d\d\d\d-\d\d-\d\d).*?\"", resp.text):
        # print(it)
        name_f = it[0]  # 品名
        cat_f = it[1]  # 分类
        lowPrice_f = it[2]  # 最低价
        highPrice_f = it[3]  # 最高价
        avgPrice_f = it[4]  # 平均价
        specInfo_f = it[5]  # 规格
        date_f = it[6]  # 发布日期
        if(cat_f == ""):
            if(specInfo_f == "") :
                name.append(str(name_f))
            else:
                name.append(str(name_f + '(' + specInfo_f + ')'))
            lowPrice.append(float(lowPrice_f))
            highPrice.append(float(highPrice_f))
            avgPrice.append(float(avgPrice_f))
            specInfo.append(str(specInfo_f))
            date.append(str(date_f))
resp.close()

# print(name, "\n")
# print(lowPrice, "\n")
# print(highPrice, "\n")
# print(avgPrice, "\n")
# print(specInfo, "\n")
# print(data, "\n")


# 3.使用pandas将解析后的数据存入excel中
info = {'品名': name, '最低价': lowPrice, '最高价': highPrice,'平均价': avgPrice, '规格': specInfo, '日期': date}
dm_file = pandas.DataFrame(info)
dm_file.to_excel('Vegetable.xlsx', sheet_name="蔬菜价格分析")


# 4.使用matplotlib绘制可视化分析图
my_font = font_manager.FontProperties(fname='./FZGuoMeiJinDaoTi.TTF')  # 设置中文字体（图标中能显示中文）
# 为了坐标轴上能显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


# *****************最高价和最低价对比
# *******最高价条形图
fig, ax1 = plt.subplots()
plt.bar(name, highPrice, color='red', width=1)  # 设置柱状图
plt.title('最高价和最低价数据分析', fontproperties=my_font)  # 表标题
ax1.tick_params(axis='x', labelsize=3.8)
ax1.tick_params(axis='y', labelsize='medium')
plt.axis(ymin=0, ymax=16)
plt.xlabel('蔬菜名')  # 横轴名
plt.ylabel('最高价')  # 纵轴名
plt.xticks(rotation=90, color='green')  # 设置横坐标变量名旋转度数和颜色

# *******最低价折线图
ax2 = ax1.twinx()  # 组合图必须加这个
ax2.plot(lowPrice, color='yellow')  # 设置线粗细，节点样式
plt.axis(ymin=0, ymax=16)
plt.ylabel('最低价')  # y轴

plt.plot(1, label='最高价', color="red", linewidth=5.0)  # 图例
plt.plot(1, label='最低价', color="yellow", linewidth=1.0, linestyle="-")  # 图例
plt.legend()

plt.savefig(r'high_low.png', dpi=1000, bbox_inches='tight')  # 保存至本地


# *****************平均价和最低价对比
# *******平均价条形图
fig, ax1 = plt.subplots()
plt.bar(name, avgPrice, color='red', width=1)  # 设置柱状图
plt.title('平均价和最低价数据分析', fontproperties=my_font)  # 表标题
ax1.tick_params(axis='x', labelsize=3.8)
ax1.tick_params(axis='y', labelsize='medium')
plt.axis(ymin=0, ymax=16)
plt.xlabel('蔬菜名')  # 横轴名
plt.ylabel('平均价')  # 纵轴名
plt.xticks(rotation=90, color='green')  # 设置横坐标变量名旋转度数和颜色

# *******最低价折线图
ax2 = ax1.twinx()  # 组合图必须加这个
ax2.plot(lowPrice, color='yellow')  # 设置线粗细，节点样式
plt.axis(ymin=0, ymax=16)
plt.ylabel('最低价')  # y轴

plt.plot(1, label='平均价', color="red", linewidth=5.0)  # 图例
plt.plot(1, label='最低价', color="yellow", linewidth=1.0, linestyle="-")  # 图例
plt.legend()

plt.savefig(r'avg_low.png', dpi=1000, bbox_inches='tight')  # 保存至本地


# *****************平均价和最高价对比
# *******平均价条形图
fig, ax1 = plt.subplots()
plt.bar(name, avgPrice, color='red', width=1)  # 设置柱状图
plt.title('最高价和最低价数据分析', fontproperties=my_font)  # 表标题
ax1.tick_params(axis='x', labelsize=3.8)
ax1.tick_params(axis='y', labelsize='medium')
plt.axis(ymin=0, ymax=16)
plt.xlabel('蔬菜名')  # 横轴名
plt.ylabel('平均价')  # 纵轴名
plt.xticks(rotation=90, color='green')  # 设置横坐标变量名旋转度数和颜色

# *******最高价折线图
ax2 = ax1.twinx()  # 组合图必须加这个
ax2.plot(highPrice, color='yellow')  # 设置线粗细，节点样式
plt.axis(ymin=0, ymax=16)
plt.ylabel('最高价')  # y轴

plt.plot(1, label='平均价', color="red", linewidth=5.0)  # 图例
plt.plot(1, label='最高价', color="yellow", linewidth=1.0, linestyle="-")  # 图例
plt.legend()

plt.savefig(r'avg_high.png', dpi=1000, bbox_inches='tight')  # 保存至本地

# plt.show()