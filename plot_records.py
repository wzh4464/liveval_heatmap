###
# File: ./liveval_heatmap/plot_records.py
# Created Date: Saturday, May 24th 2025
# Author: Zihan
# -----
# Last Modified: Saturday, 24th May 2025 7:50:42 pm
# Modified By: the developer formerly known as Zihan at <wzh4464@gmail.com>
# -----
# HISTORY:
# Date      		By   	Comments
# ----------		------	---------------------------------------------------------
###

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import seaborn as sns  # Import seaborn for font_scale

# 手动注册Linux Libertine字体
libertine_path = "/Users/zihanwu/Library/Fonts/LinLibertine_R.ttf"
if os.path.exists(libertine_path):
    fm.fontManager.addfont(libertine_path)
    print(f"已注册Linux Libertine字体: {libertine_path}")
else:
    print(f"未找到Linux Libertine字体文件: {libertine_path}")

# 获取可用字体列表
available_fonts = sorted([f.name for f in fm.fontManager.ttflist])

# 选择合适的学术字体
chosen_font = "Linux Libertine" if "Linux Libertine" in available_fonts else "Palatino"
for font in ["Linux Libertine", "Palatino", "Charter", "Georgia", "Garamond"]:
    if font in available_fonts:
        chosen_font = font
        break
print(f"选择使用字体: {chosen_font}")

# 使用选定的学术字体并启用LaTeX支持
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = [chosen_font, "DejaVu Serif", "serif"]
plt.rcParams["mathtext.fontset"] = "dejavuserif"
# 启用LaTeX渲染
plt.rcParams["text.usetex"] = True
plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"

# 指定文件路径
# file_path = 'results/experiment_heatmap_0523/delta_exp/delta_step_1_delta_max_5/seed_3/delta_records.csv'
file_path = "delta_records.csv"

# 读取CSV文件
df = pd.read_csv(file_path)

# 取前400
df = df.iloc[:400]

# 获取除 'epoch' 列以外的所有列名
columns_to_plot = [col for col in df.columns if col != "epoch"]

# 创建图表
plt.figure(figsize=(16, 8))  # 您可以根据需要调整图表大小
sns.set_context("notebook", font_scale=2.0)  # 进一步放大字体

# 遍历选择的列并绘制折线图
# [L_t,dot_L,delta,delta_change]
# 'delta', 'delta_change' 用散点
# 颜色 ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628']
colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628"]

# 定义要绘制的列和对应的LaTeX标签
# 注意：'dot_L' 假设表示 L 上方有一个点 (导数)
columns_to_plot_map = {"L_t": r"$L_t$", "dot_L": r"$\dot{L}$", "delta": r"$\delta$"}
# 保持原始顺序以确保颜色一致性
plot_order = ["L_t", "dot_L", "delta"]

for i, column_name in enumerate(plot_order):
    if column_name in df.columns and column_name in columns_to_plot_map:
        latex_label = columns_to_plot_map[column_name]
        # 原始代码中有散点图的注释，这里我们遵循主要逻辑使用plot
        # 如果特定列需要散点图，可以取消下方注释并调整
        # if column_name in ['delta', 'delta_change']: # 'delta_change' 不在当前绘制列表
        #     plt.scatter(df.index, df[column_name], label=latex_label, color=colors[i])
        # else:
        plt.plot(df.index, df[column_name], label=latex_label, color=colors[i])

# 添加图例
plt.legend()  # LaTeX 标签会在这里生效, 字体大小受 font_scale影响

# 添加标题和标签
# plt.title('Metrics Over Steps (Excluding Epoch)', fontsize=24) # 增大字体
plt.xlabel("Step", fontsize=24)  # 增大字体
# plt.ylabel('Value', fontsize=24) # 增大字体
plt.xticks(fontsize=24)  # 增大字体
plt.yticks(fontsize=24)  # 增大字体

# 显示网格
plt.grid(True)

# 保存图表为图片文件
output_filename = "metrics_plot.png"
plt.savefig(output_filename, dpi=300)  # 增加 dpi 以提高图片质量
print(f"图表已保存为 {output_filename}")

# 如果您希望在运行时直接显示图表，取消下一行的注释
# plt.show()
