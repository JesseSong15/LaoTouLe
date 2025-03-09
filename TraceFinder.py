import tkinter as tk
from tkinter import Canvas, Scrollbar, Toplevel, Checkbutton, IntVar, Button, filedialog, messagebox
import pandas as pd
import numpy as np
from scipy.optimize import minimize

def select_file(file_type):
    filepath = filedialog.askopenfilename()
    if file_type == 'source':
        entry_source_file.delete(0, tk.END)
        entry_source_file.insert(0, filepath)
        display_source_areas(filepath)
        global source_file_path
        source_file_path = filepath
    elif file_type == 'sand':
        entry_sand_file.delete(0, tk.END)
        entry_sand_file.insert(0, filepath)
        global sand_file_path
        sand_file_path = filepath

def display_source_areas(filepath_source):
    try:
        source_data = pd.read_csv(filepath_source)
        source_areas = source_data['Source'].unique()
        text_source_areas.delete('1.0', tk.END)
        text_source_areas.insert(tk.END, ', '.join(source_areas))
    except Exception as e:
        messagebox.showerror("错误", "读取物源样品文件失败: {}".format(e))

def open_element_selection_window():
    selection_window = Toplevel(root)
    selection_window.title("最佳指纹因子选择")
    selection_window.iconbitmap('ProvenanceTracer.ico')
    
    # 创建横向滚动条
    canvas = Canvas(selection_window)
    scrollbar = Scrollbar(selection_window, orient="horizontal", command=canvas.xview)
    scrollable_frame = tk.Frame(canvas)

    # 配置横向滚动区域
    canvas.configure(xscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # 添加滚动条到窗口
    canvas.pack(side="top", fill="x", expand=True)
    scrollbar.pack(side="bottom", fill="x")

    try:
        data = pd.read_csv(source_file_path)
        columns = data.columns[2:]  # 从C列开始读取元素列
    except Exception as e:
        messagebox.showerror("错误", f"读取物源样品文件失败: {e}")
        return

    # 创建每个元素的Checkbutton
    global selected_factors
    selected_factors = []
    for i, column in enumerate(columns):
        var = IntVar(value=0)  # 默认不选中
        chk = Checkbutton(scrollable_frame, text=column, variable=var)
        chk.grid(row=i % 8, column=i // 8, sticky='w')
        selected_factors.append((column, var))

    # 在scrollable_frame的下方添加“下一步”按钮
    next_button = Button(selection_window, text="下一步", command=open_output_dialog)
    next_button.pack(pady=10)


def open_output_dialog():
    output_window = Toplevel(root)
    output_window.title("结果输出")
    output_window.iconbitmap('ProvenanceTracer.ico')

    tk.Label(output_window, text="输出文件位置:").grid(row=0, column=0, padx=10, pady=5)
    entry_output_file = tk.Entry(output_window, width=50)
    entry_output_file.grid(row=0, column=1, padx=10, pady=5)
    button_select_output = tk.Button(output_window, text="选择位置", 
                                     command=lambda: select_output_file(entry_output_file))
    button_select_output.grid(row=0, column=2, padx=10, pady=5)

    Button(output_window, text="开始计算", 
           command=lambda: start_calculation(entry_output_file.get())).grid(row=1, column=1, padx=10, pady=20)

def select_output_file(entry):
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    entry.delete(0, tk.END)
    entry.insert(0, filepath)

def calculate_contributions(filepath_source, filepath_sand, factors, output_path):
    messagebox.showinfo("指纹因子确认", "使用的指纹因子：\n" + "\n".join(factors))
    
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
    try:
        results_df.to_csv(output_path, index=False)
        print(f'结果已保存到{output_path}')
        return True  # 表示成功完成计算和保存
    except Exception as e:
        print(f'保存结果时出现错误: {e}')
        return False  # 表示在保存时遇到问题

def start_calculation(output_path):
    if not output_path:
        messagebox.showerror("错误", "请选择输出文件位置")
        return
    factors = [factor[0] for factor in selected_factors if factor[1].get() == 1]
    if not factors:
        messagebox.showerror("错误", "未选择任何指纹因子")
        return
    # 从GUI获取的变量值
    filepath_source = entry_source_file.get()
    filepath_sand = entry_sand_file.get()
    factors = [factor for factor, var in selected_factors if var.get() == 1]

    # 调用 calculate_contributions 函数，传入用户选择的输出路径
    success = calculate_contributions(filepath_source, filepath_sand, factors, output_path)

    if success:
        # 如果计算和保存成功，显示消息并关闭所有窗口
        messagebox.showinfo("完成", "结果输出完毕")
        root.destroy()  # 关闭主窗口
    else:
        messagebox.showerror("错误", "计算或保存过程中发生错误")

root = tk.Tk()
root.title("ProvenanceTracer")
root.iconbitmap('ProvenanceTracer.ico')

source_file_path = ""
sand_file_path = ""

tk.Label(root, text="物源样品文件:").grid(row=0, column=0, padx=10, pady=10)
entry_source_file = tk.Entry(root, width=50)
entry_source_file.grid(row=0, column=1, padx=10, pady=10)
button_source_file = tk.Button(root, text="选择文件", command=lambda: select_file('source'))
button_source_file.grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="风沙样品文件:").grid(row=1, column=0, padx=10, pady=10)
entry_sand_file = tk.Entry(root, width=50)
entry_sand_file.grid(row=1, column=1, padx=10, pady=10)
button_sand_file = tk.Button(root, text="选择文件", command=lambda: select_file('sand'))
button_sand_file.grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="物源区列表:").grid(row=2, column=0, padx=10, pady=10, sticky='nw')
text_source_areas = tk.Text(root, height=4, width=37)
text_source_areas.grid(row=2, column=1, padx=10, pady=10)

button_next_step = tk.Button(root, text="下一步", command=open_element_selection_window)
button_next_step.grid(row=3, column=1, padx=10, pady=10, sticky='e')

root.mainloop()