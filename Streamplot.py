"""
以下是宝可能要修改的代码部分：
    1. 第52-55行：输入文件的名字（这里已经采用了相对路径），需要注意使用右斜杠“/”
    2. 第142行：输出文件的路径，同样需要使用右斜杠“/”
其余参数已经给宝进行了尽可能详细的注释，可以根据实际效果来进行相应的调整
"""

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.interpolate import griddata
import pandas as pd

# 封装一个函数streamplot_data用于计算绘制流线图所需的数据，传入该函数的参数是nc文件路径
def streamplot_data(data_path):
    nc_data = Dataset(data_path, mode='r')  # 读取nc文件

    # 读取风速数据
    u_wind = nc_data.variables['u10'][:]
    v_wind = nc_data.variables['v10'][:]

    # 计算时间维的平均值
    u_mean = np.mean(u_wind, axis=0)
    v_mean = np.mean(v_wind, axis=0)

    # 读取经纬度坐标
    lat = nc_data.variables['latitude'][:]
    lon = nc_data.variables['longitude'][:]

    nc_data.close()  # 数据读取完毕，关闭nc文件

    # 创建新的等间距经纬网
    lon_new = np.linspace(lon.min(), lon.max(), len(lon))  # 保持原始点数
    lat_new = np.linspace(lat.min(), lat.max(), len(lat))  # 保持原始点数
    Lon_new, Lat_new = np.meshgrid(lon_new, lat_new)

    # 使用原始经纬网格作为插值源点
    Lon, Lat = np.meshgrid(lon, lat)

    # 对u_mean和v_mean进行插值，确保与新的Lon_new和Lat_new网格匹配
    u_mean_new = griddata((Lon.flatten(), Lat.flatten()), u_mean.flatten(), (Lon_new, Lat_new), method='cubic')
    v_mean_new = griddata((Lon.flatten(), Lat.flatten()), v_mean.flatten(), (Lon_new, Lat_new), method='cubic')

    # 计算风速大小
    speed_new = np.sqrt(u_mean_new**2 + v_mean_new**2)
    
    # 绘制流线图所需要的数据是等间距经纬网lon_new、lat_new，以及插值所得的风速数据u_mean_new、v_mean_new，还有风速speed_new
    # 因此，在这里我们将这五个变量构成一个元组，作为函数的返回值（也就是函数要输出给我们的结果）
    return lon_new, lat_new, u_mean_new, v_mean_new, speed_new

# 首先，在这个列表中输入我们所需可视化的所有nc文件
file_path = ['1-MAM.nc',
             '2-JJA.nc',
             '3-SON.nc',
             '4-DJF.nc']
print(f"待绘制{len(file_path)}个文件\n")

# 接着，读取主要城市的坐标
df = pd.read_csv('Cities.csv', encoding='ISO-8859-1')  # 不要更改encoding参数，避免读取文件时编码报错

# 设置图片尺寸
# 创建图片时，传入figsize参数的默认长度单位是英寸，因此在第66行进行了单位转换，即除以2.54
width_cm = 25  # 宽度为25cm
height_cm = 12  # 高度为12cm
dpi_value = 600  # 分辨率为600dpi
fig, axs = plt.subplots(2, 2, figsize=(width_cm/2.54, height_cm/2.54), dpi=dpi_value)  # 创建2x2布局的子图

# 统一设置子图的显示范围
xrange = [115, 130]  # 经度为115°E-130°E
yrange = [43, 50]  # 纬度为43°N-50°N

# 设置各个子图的小标题
plot_labels = ['(a) MAM', '(b) JJA', '(c) SON', '(d) DJF']

# 逐一绘制流线图
i = 0  # 变量i的实际作用在于标记一个顺序，这个序号既表示了子图绘制的顺序、也表示了nc文件读取的顺序、还表示了小标题的顺序
for ax in axs.flat:
    data_path = file_path[i]  # 逐个读取file_path列表中的nc文件
    
    # 绘图
    lon_new, lat_new, u_mean_new, v_mean_new, speed_new = streamplot_data(data_path)  # 通过streamplot_data函数获取插值所需的数据
    strm = ax.streamplot(lon_new, lat_new, u_mean_new, v_mean_new,  # 绘图所需的数据
                         color=speed_new,  # 表示按风速大小为流线上色
                         cmap='Blues',  # 表示色阶的样式，这是一个从白色过渡到深蓝色的色阶
                         # 更多色阶样式可以访问https://zhuanlan.zhihu.com/p/158871093
                         linewidth=1,  # 表示流线的宽度
                         minlength=0.4,  # 表示流线长度的最小值（默认0.1），适当加大这个值可以减少图中不连贯的流线
                         density=1.25  # 表示流线的密度
                         )
    
    # 添加主要的城市
    for index, row in df.iterrows():
        ax.scatter(row['Lon'], row['Lat'], s=10, color='#dd62ab')  # 添加点
        
        # 添加标签
        if row['Name_Short'] == 'MD' or row['Name_Short'] == 'WL' or row['Name_Short'] == 'CC':
            ax.text(row['Lon']-1.15, row['Lat'], row['Name_Short'], ha='left', va='center', fontsize=10, family='Times New Roman')
        else:
            ax.text(row['Lon']+0.2, row['Lat'], row['Name_Short'], ha='left', va='center', fontsize=10, family='Times New Roman')
    
    # 固定显示的范围
    ax.set_xlim(xrange)
    ax.set_ylim(yrange)
    
    # 添加网格
    ax.grid(color='gray', linestyle='--', linewidth=0.25)
    
    # 设置刻度标签与字体
    ax.set_xticks([115, 118, 121, 124, 127, 130])
    ax.set_xticklabels(['115°E', '118°E', '121°E', '124°E', '127°E', '130°E'], fontname='Times New Roman', fontsize=10)
    ax.set_yticks([44, 46, 48, 50])
    ax.set_yticklabels(['44°N', '46°N', '48°N', '50°N'], fontname='Times New Roman', fontsize=10)
    
    # 设置坐标轴标题与字体（暂略去）
    # ax.set_xlabel("经度", fontname='SimSun', fontsize=10)
    # ax.set_ylabel("纬度", fontname='SimSun', fontsize=10)
    
    # 为当前绘制的子图添加标题
    title = plot_labels[i]
    ax.set_title(title, loc='left', fontdict={'family':'Times New Roman', 'weight':'bold', 'size':11})
    
    i = i + 1  # 序号+1
    
    print(f'第{i}/{len(file_path)}个子图（{title}）绘制完成')  # 输出提示
    
    if i >= len(file_path): break  # 检查下一个序号是否超过file_path列表中的文件个数，超过则跳出循环

# 调节页边距，数字代表色阶距图片边缘的比例
plt.subplots_adjust(left=0.05, right=0.85, top=0.95, bottom=0.05, wspace=0.2, hspace=0.35)

# 添加色阶，调整其位置
cbar_ax = fig.add_axes([0.9, 0.15, 0.03, 0.7])  # 数字代表色阶距图片边缘的比例
cbar = fig.colorbar(strm.lines, cax=cbar_ax)
cbar.set_label('风速（m/s）', fontsize=12, fontname='SimSun')  # 设置色阶标题和字体
cbar.ax.tick_params(labelsize=11)  # 设置色阶数字标签的字体大小
for l in cbar.ax.get_yticklabels():
    l.set_family('Times New Roman')
    
print("\n色阶绘制完成")  # 输出提示

# 保存生成的图片
output_path = 'F:/Windspeed streamplot/Streamplot.png'
plt.savefig(output_path)

# 输出提示
print(f'\n文件已经保存到{output_path} \n大小：{width_cm}×{height_cm} cm \n分辨率：{dpi_value} dpi')

plt.show()