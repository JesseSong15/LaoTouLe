# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 09:57:40 2024

@author: Zhang Xinyue & Song Gaoge
"""

import pandas as pd
from scipy.stats import kruskal
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.feature_selection import RFE
from sklearn.preprocessing import LabelEncoder
from scipy.optimize import minimize

def calculate_contributions(filepath_source, filepath_sand, factors):
    # 读取数据
    aeolian_sand_data = pd.read_csv(filepath_sand)
    source_data = pd.read_csv(filepath_source)

    # 自动判断物源区数量 m
    m = len(source_data['Source'].unique())

    # 标准化指纹因子浓度
    max_values = pd.concat([aeolian_sand_data[factors], source_data[factors]]).max()
    aeolian_sand_data_norm = aeolian_sand_data[factors].div(max_values)
    source_data_norm = source_data.pivot_table(index='Source', values=factors, aggfunc='mean').div(max_values)

    # 定义目标函数和约束条件
    def objective_function(P, C_ssi, C_si):
        R_es = np.sum(((C_ssi - np.dot(C_si, P)) / C_ssi) ** 2)
        return R_es
    cons = [{'type': 'eq', 'fun': lambda P: np.sum(P) - 1},  # 确保P_s的和为1
            {'type': 'ineq', 'fun': lambda P: P}]            # 确保P_s的值非负

    # 初始化结果列表
    results_list = []

    # 遍历每个风沙样品进行计算
    for index, row in aeolian_sand_data_norm.iterrows():
        C_ssi = row.values
        C_si = source_data_norm.values.T
        initial_guess = np.ones(m) / m  # 初始猜测，根据物源区数量 m 分配

        # 执行最小化过程
        res = minimize(objective_function, initial_guess, args=(C_ssi, C_si), constraints=cons, method='SLSQP')

        # 创建结果字典并添加到列表中
        result_dict = {
            'Specimen': aeolian_sand_data.loc[index, 'Specimen'],
            **{f'Contribution_{source}': p for source, p in zip(source_data_norm.index, res.x)},
            'GOF': 1 - (1 / len(factors)) * np.sum(np.abs((C_ssi - np.dot(C_si, res.x)) / C_ssi))
        }
        results_list.append(result_dict)

    # 转换结果列表为DataFrame并保存
    results_df = pd.DataFrame(results_list)
    results_path = 'Aeolian_Sand_Contributions_GOF.csv'
    results_df.to_csv(results_path, index=False)
    print(f'结果已保存到{results_path}')


"""
###########################下述代码进行异常值剔除###########################
# 读取Excel文件
file_path = 'Fingerprinting Data.xlsx'  # Excel文件的路径
sheet_name_source = 'Source2'  # 要读取的物源数据工作表名称
sheet_name_aeolian = 'AeolianSand2'  # 要读取的风沙数据工作表名称
df_source = pd.read_excel(file_path, sheet_name=sheet_name_source)  # 物源的DataFrame
df_aeolian = pd.read_excel(file_path, sheet_name=sheet_name_aeolian)  # 风沙的DataFrame

# 提取数据
data_columns_source = df_source.columns[5:49]
data_columns_aeolian = df_aeolian.columns[5:49]

# 初始化两个空的DataFrame来存放没有异常值的数据
cleaned_df_source = df_source.copy()
cleaned_df_aeolian = df_aeolian.copy()

for column in data_columns_source:
    Q1 = cleaned_df_source[column].quantile(0.25)
    Q3 = cleaned_df_source[column].quantile(0.75)
    IQR = Q3 - Q1
    upper_limit = Q3 + 2.2 * IQR  # 计算物源样的最高临界值
    lower_limit = Q1 - 2.2 * IQR  # 计算物源样的最低临界值
    
    # 统一按照物源区的临界值进行异常值剔除
    cleaned_df_source = cleaned_df_source[(cleaned_df_source[column] <= upper_limit) & (cleaned_df_source[column] >= lower_limit)]
    cleaned_df_aeolian = cleaned_df_aeolian[(cleaned_df_aeolian[column] <= upper_limit) & (cleaned_df_aeolian[column] >= lower_limit)]

# 将处理后的数据保存到新的CSV文件中
cleaned_df_source.to_csv('Cleaned Data_Source.csv', index=False, encoding='utf_8_sig')
cleaned_df_aeolian.to_csv('Cleaned Data_AeolianSand.csv', index=False, encoding='utf_8_sig')
print("异常值剔除完成")


###########################下述代码进行物源样的非参数检验###########################
# 提取分类变量和数据
df = pd.read_excel(file_path, sheet_name=sheet_name_source)
source_column = 'Source'  # 分类变量列名
data_columns = df.columns[5:49]  # F至AW列

# 准备存储结果的列表
results_list = []

# 对每个变量进行Kruskal-Wallis H检验
for column in data_columns:
    # 分组数据
    groups = [group.dropna().values for name, group in df.groupby(source_column)[column]]
    # 只有当所有组都有数据时才进行检验
    if all(len(group) > 0 for group in groups):
        stat, p = kruskal(*groups)
        significant = 'Yes' if p < 0.05 else 'No'
        results_list.append({'Variable': column, 'H-Statistic': stat, 'P-Value': p, 'Significant': significant})

# 将结果列表转换为DataFrame
results = pd.DataFrame(results_list)

# 保存结果到CSV文件
results.to_csv('K-W Result_Source.csv', index=False)
print("物源样非参数检验完成，结果储存在K-W Result_Source.csv")


###########################最佳指纹因子提取通过SPSS实现###########################

"""
###########################下述代码基于Walling等简化后的多元混合模型计算贡献率###########################
# 示例调用函数，此处'factors'需要替换为实际的指纹因子名称列表
calculate_contributions('Cleaned Data_Source.csv', 'Cleaned Data_AeolianSand.csv', ['Tb', 'Hf'])