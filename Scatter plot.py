import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 加载数据
data_path = 'Data.csv'  # 请根据实际情况修改文件路径
data = pd.read_csv(data_path)

# 定义顺序和标签
source_order = ['H', 'K', 'L', 'N', 'T', 'S']
sedenvs_order = [1, 2, 3, 4, 5, 6, 0]
source_labels = {'H': '呼伦贝尔', 'K': '科尔沁', 'L': '拉林河及第二松花江', 'N': '嫩江及其支流', 'T': '洮儿河及大兴安岭山前', 'S': '风沙堆积'}
sedenvs_labels = {1: '风沙相', 2: '漫滩相', 3: '冲积相', 4: '湖沼相', 5: '河床相', 6: '残坡积相', 0: '风沙堆积'}

# 映射标签
data['Source_label'] = data['Source'].map(source_labels)
data['SedEnvs_label'] = data['SedEnvs'].map(sedenvs_labels)

# 设置绘图风格
sns.set(style="ticks")
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 10

# 创建一个 2x2 的子图布局
fig, axs = plt.subplots(2, 2, figsize=(28/2.54, 20/2.54), dpi=600)

# 定义坐标对和子图标题
coords = [('X1', 'Y1'), ('X2', 'Y2'), ('X3', 'Y3'), ('X4', 'Y4')]
titles = ['(a)', '(b)', '(c)', '(d)']
x_labels = ['Hf/Nb', '(La:Sm)$_{N}$', '(La:Yb)$_{N}$', 'Th/Nb']
y_labels = ['Zr/Nb', '(Gd:Yb)$_{N}$', 'δEu', 'La/Nb']

i = 0
for ax, coord, title in zip(axs.flat, coords, titles):
    # 绘制散点图，自定义顺序和标签
    sns.scatterplot(data=data, x=coord[0], y=coord[1], 
                    hue='Source', hue_order=source_order,
                    style='SedEnvs', style_order=sedenvs_order,
                    ax=ax, palette='tab10')
    ax.set_title(title, fontdict={'fontsize': 11, 'fontweight': 'bold', 'fontname': 'Times New Roman'}, loc='left')
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
    i = i+1

# 调整布局
plt.subplots_adjust(left=0.08, right=0.8, bottom=0.1, top=0.95, wspace=1.2, hspace=0.3)

# 显示图形
plt.savefig('Scatterplot.png')
plt.show()