import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.font_manager import FontProperties

# 由于无法直接访问外部文件路径，以下代码块假设数据已正确加载到data DataFrame中
data_path = 'Data2.csv'  # 请根据实际情况修改文件路径
data = pd.read_csv(data_path)

# 定义顺序和标签，这些设置假定已正确定义
loc_order = ['W', 'M', 'E']
sedenvs_order = [1, 2, 3, 4, 6, 0]
loc_labels = {'W': '西部沙区', 'M': '中部沙区', 'E': '东部沙区'}
sedenvs_labels = {1: '风沙相', 2: '洪流相', 3: '河床相', 4: '湖沼相', 6: '残坡积相', 0: '风沙堆积'}

# 假设data是已经加载的DataFrame
data['loc_label'] = data['loc'].map(loc_labels)

# 设置绘图风格
sns.set(style="ticks")
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10

# 定义坐标对和子图标题，坐标轴标签
coords = [('X1', 'Y1'), ('X2', 'Y2')]
titles = ['(a)', '(c)']
x_labels = ['Hf/Nb', '(La:Sm)$_{N}$']
y_labels = ['Zr/Nb', '(Gd:Yb)$_{N}$']
filenames = ['subplot_a.png', 'subplot_c.png']

# 分别导出4张子图
for i in range(2):
    plt.figure(figsize=(7, 5), dpi=600)  # 单独设置每张图的大小
    X = coords[i][0]
    Y = coords[i][1]
    ax = sns.scatterplot(data=data, x=X, y=Y, s=100,
                         hue='loc', hue_order=loc_order,
                         style='SedEnvs', style_order=sedenvs_order,
                         palette='tab10')
    ax.set_title(titles[i], fontdict={'fontsize': 11, 'fontweight': 'bold', 'fontname': 'Times New Roman'}, loc='left')
    ax.set_xlabel(x_labels[i], fontsize=11, fontname='Times New Roman')
    ax.set_ylabel(y_labels[i], fontsize=11, fontname='Times New Roman')
    annotations = ['DSZ-1', 'DSZ-2', 'DSZ-3', 'HDM-1', 'HDM-2', 'DLHT', 'XPA-1', 'XPA-2', 'YS-1', 'YS-2', 'ZY-1', 'SJZ-1', 'SJZ-2', 'SJZ-3']
    """
    for j, label in enumerate(annotations):
        plt.annotate(label, (X[j], Y[j]))
    """
    # 生成自定义图例
    # loc图例
    loc_handles_labels = [(handle, label) for handle, label in zip(*ax.get_legend_handles_labels()) if label in loc_labels]
    loc_handles, loc_labels_ordered = zip(*[(handle, loc_labels[label]) for handle, label in loc_handles_labels])
    # 清除当前图例
    ax.legend_.remove()
    # 添加新图例
    loc_legend = ax.legend(loc_handles, loc_labels_ordered, title='', bbox_to_anchor=(1.05, 1), loc='upper left', prop={'family': 'SimSun', 'size': 10})
    ax.add_artist(loc_legend)
    plt.subplots_adjust(left=0.1, right=0.75, bottom=0.1, top=0.95)
    plt.savefig(filenames[i])  # 保存每张图
    plt.close()  # 关闭图形，以便开始下一个