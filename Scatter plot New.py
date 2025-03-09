import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.font_manager import FontProperties

# 由于无法直接访问外部文件路径，以下代码块假设数据已正确加载到data DataFrame中
data_path = 'Data_New.csv'  # 请根据实际情况修改文件路径
data = pd.read_csv(data_path)

# 定义顺序和标签，这些设置假定已正确定义
source_order = ['H', 'K', 'L', 'N', 'T', 'S']
sedenvs_order = [1, 2, 3, 4, 6, 0]
source_labels = {'H': '呼伦贝尔', 'K': '科尔沁', 'L': '拉林河及第二松花江', 'N': '嫩江及其支流', 'T': '洮儿河及大兴安岭山前', 'S': '风沙堆积'}
sedenvs_labels = {1: '风沙相', 2: '洪流相', 3: '河床相', 4: '湖沼相', 6: '残坡积相', 0: '风沙堆积'}

# 假设data是已经加载的DataFrame
data['Source_label'] = data['Source'].map(source_labels)
data['SedEnvs_label'] = data['SedEnvs'].map(sedenvs_labels)

# 设置绘图风格
sns.set(style="ticks")
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10

# 定义坐标对和子图标题，坐标轴标签
coords = [('X1', 'Y1'), ('X2', 'Y2')]
titles = ['(b)', '(d)']
x_labels = ['Hf/Nb', '(La:Sm)$_{N}$']
y_labels = ['Zr/Nb', '(Gd:Yb)$_{N}$']
filenames = ['subplot_b.png', 'subplot_d.png']

# 分别导出4张子图
for i in range(2):
    plt.figure(figsize=(7, 5), dpi=600)  # 单独设置每张图的大小
    ax = sns.scatterplot(data=data, x=coords[i][0], y=coords[i][1], 
                         hue='Source', hue_order=source_order,
                         style='SedEnvs', style_order=sedenvs_order,
                         palette='tab10')
    ax.set_title(titles[i], fontdict={'fontsize': 11, 'fontweight': 'bold', 'fontname': 'Times New Roman'}, loc='left')
    ax.set_xlabel(x_labels[i], fontsize=11, fontname='Times New Roman')
    ax.set_ylabel(y_labels[i], fontsize=11, fontname='Times New Roman')
    # 生成自定义图例
    # Source图例
    source_handles_labels = [(handle, label) for handle, label in zip(*ax.get_legend_handles_labels()) if label in source_labels]
    source_handles, source_labels_ordered = zip(*[(handle, source_labels[label]) for handle, label in source_handles_labels])
    # SedEnvs图例
    sedenvs_handles_labels = [(handle, label) for handle, label in zip(*ax.get_legend_handles_labels()) if label.isdigit()]
    sedenvs_handles, sedenvs_labels_ordered = zip(*[(handle, sedenvs_labels[int(label)]) for handle, label in sedenvs_handles_labels])
    # 清除当前图例
    ax.legend_.remove()
    # 添加新图例
    source_legend = ax.legend(source_handles, source_labels_ordered, title='', bbox_to_anchor=(1.05, 1), loc='upper left', prop={'family': 'SimSun', 'size': 10})
    ax.add_artist(source_legend)
    ax.legend(sedenvs_handles, sedenvs_labels_ordered, title='', bbox_to_anchor=(1.05, 0.5), loc='upper left', prop={'family': 'SimSun', 'size': 10})
    plt.subplots_adjust(left=0.08, right=0.68, bottom=0.1, top=0.95)
    plt.savefig(filenames[i])  # 保存每张图
    plt.close()  # 关闭图形，以便开始下一个



"""
# 设置样式
sns.set(style="ticks")

# 定义source_labels字典，用于表示物源符号与名称之间的对应关系
source_labels = {'H': '呼伦贝尔',
                 'K': '科尔沁',
                 'L': '拉林河及第二松花江',
                 'N': '嫩江及支流',
                 'S': '风沙堆积',
                 'T': '洮儿河及大兴安岭山前'}

# 定义sedEnvs_labels字典，用于表示沉积环境符号与名称之间的对应关系
sedEnvs_labels = {0: '风沙堆积',
                 1: '风沙相',
                 2: '洪流相',
                 3: '河床相',
                 4: '湖沼相',
                 6: '残坡积相'}

# 定义markers字典，用于标示不同物源区的符号
markers = {'H': '^',  # 呼伦贝尔为三角形
           'K': 'H',  # 科尔沁为六边形
           'L': 's',  # 拉林河及第二松花江为正方形
           'N': 'D',  # 嫩江及支流为菱形
           'S': 'o',  # 风沙为圆形
           'T': 'X'}  # 洮儿河及大兴安岭山前为星形

# 定义colors字典，用于标示不同沉积环境的颜色
colors = {0: 'black',
          1: 'blue',
          2: 'cyan',
          3: 'green',
          4: 'red',
          5: 'purple',
          6: 'orange'}

# 创建12×8cm的画布
plt.figure(figsize=(24/2.54, 12/2.54), dpi=600)
frame_font_properties = FontProperties(size=11, family='SimSun')  # 坐标轴标题为11磅宋体
ticks_font_properties = FontProperties(size=11, family='Times New Roman')  # 刻度为11磅Times New Roman

# 绘制实际的散点图数据
for (source, sedenv), group_data in data.groupby(['Source', 'SedEnvs']):
    plt.scatter(group_data['X3'], group_data['Y3'], 
                s=40, alpha=0.7, 
                marker=markers[source], 
                color=colors[sedenv])

# 设置字体属性为SimSun
legend_title_font_prop = FontProperties(size=10, family='SimSun', weight='bold')

# 分别为物源区和沉积环境创建图例
# 创建物源区图例的句柄列表，确保“风沙堆积”在最后
source_order = ['H', 'K', 'L', 'N', 'T', 'S']  # 最后放置'S'
source_handles = [plt.Line2D([0], [0], marker=markers[s], color='w', markerfacecolor='black', markersize=10, label=source_labels[s]) for s in source_order]
# 添加物源区图例
leg_source = plt.legend(handles=source_handles, bbox_to_anchor=(1.05, 1), loc='upper left', title="物源区", title_fontproperties=legend_title_font_prop, prop=FontProperties(size=10, family='SimSun'))
plt.gca().add_artist(leg_source)  # 将物源区图例添加到图上

# 创建沉积环境图例的句柄列表，确保“风沙堆积”在最后
sedenv_order = [1, 2, 3, 4, 6, 0]  # 最后放置0，表示风沙堆积
sedenv_handles = [plt.Line2D([0], [0], marker='s', color=colors[se], label=sedEnvs_labels[se], markersize=10) for se in sedenv_order]
# 添加沉积环境图例
plt.legend(handles=sedenv_handles, bbox_to_anchor=(1.05, 0.5), loc='upper left', title="沉积环境", title_fontproperties=legend_title_font_prop, prop=FontProperties(size=10, family='SimSun'))

# 设置坐标轴标题
plt.xlabel('维度1', fontproperties=frame_font_properties)
plt.ylabel('维度2', fontproperties=frame_font_properties)

# 获取当前图表的坐标轴
ax = plt.gca()

# 添加透明度为60%的刻度线
ax.grid(True, which='both', color='gray', linestyle='-', linewidth=0.5, alpha=0.6)

# 设置x轴和y轴的刻度标签字体
for label in ax.get_xticklabels():
    label.set_fontproperties(ticks_font_properties)
for label in ax.get_yticklabels():
    label.set_fontproperties(ticks_font_properties)

# 保存图片
# plt.tight_layout(rect=[0, 0, 0.85, 1]) # 这里调整了tight_layout的rect参数以留出空间给图例
plt.subplots_adjust(left=0.1, right=0.7, bottom=0.15, top=0.95)
plt.savefig('Scatter plot_NewNew.png')
plt.show()
"""