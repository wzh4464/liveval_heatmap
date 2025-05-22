import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
import matplotlib as mpl
import matplotlib.font_manager as fm
import os

# 手动注册Linux Libertine字体
libertine_path = "/Users/zihanwu/Library/Fonts/LinLibertine_R.ttf"
if os.path.exists(libertine_path):
    fm.fontManager.addfont(libertine_path)
    print(f"已注册Linux Libertine字体: {libertine_path}")
else:
    print(f"未找到Linux Libertine字体文件: {libertine_path}")

# 获取可用字体列表
available_fonts = sorted([f.name for f in fm.fontManager.ttflist])
print("系统可用字体:")
for font in available_fonts[:10]:  # 只打印前10个作为示例
    print(f"- {font}")
print(f"总共 {len(available_fonts)} 种字体")

# 搜索学术风格字体
academic_keywords = [
    "libertine",
    "times",
    "palatino",
    "charter",
    "bookman",
    "georgia",
    "garamond",
    "cambria",
]
academic_fonts = []
for keyword in academic_keywords:
    matches = [f for f in available_fonts if keyword.lower() in f.lower()]
    if matches:
        academic_fonts.extend(matches)
        print(f"找到{keyword}相关字体: {matches}")

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
plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath} \usepackage{bm}"

# 全局设置字体加粗
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['figure.titleweight'] = 'bold'


def plot_param_sensitivity_heatmap(
    data_dict,
    title="Parameter Sensitivity Heatmap",
    x_label="max",
    y_label="min",
    use_latex=False,
):
    # 构造 DataFrame
    df = pd.DataFrame(
        [
            {"min": float(k[0]), "max": float(k[1]), "mean": sum(v) / len(v)}
            for k, v in data_dict.items()
        ]
    )
    pivot_df = df.pivot(index="min", columns="max", values="mean")

    # 设置大字体样式
    sns.set_context("notebook", font_scale=4.0)  # 字体放大约4倍
    
    # 使用学术字体
    with plt.style.context({"font.family": "serif", "font.serif": [chosen_font]}):
        # 绘图
        plt.figure(figsize=(18, 14))  # 适配大字体所需更大图像尺寸
        ax = sns.heatmap(
            pivot_df, 
            annot=True, 
            fmt=".2f", 
            cmap="YlGnBu", 
            cbar_kws={"shrink": 0.5},
            annot_kws={"weight": "bold", "size": 72},  # 热力图数值标签加粗并增大字号（从28增加到42）
        )
        
        # 添加标题并加粗
        plt.title(title, fontsize=72, fontweight="bold")  # 标题字体从48增加到72
        
        # 坐标轴标签加粗
        plt.xlabel(x_label, fontsize=72, fontweight="bold")  # 坐标轴标签从36增加到54
        plt.ylabel(y_label, fontsize=72, fontweight="bold")  # 坐标轴标签从36增加到54

        # 设置刻度标签加粗
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=42, fontweight="bold")  # 刻度标签从28增加到42
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=42, fontweight="bold")  # 刻度标签从28增加到42

        # 设置颜色条标签加粗
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=42)  # 颜色条标签从28增加到42
        ticks = cbar.get_ticks()
        cbar.set_ticks(ticks)  # 先设置刻度位置
        cbar.ax.set_yticklabels([f"{tick:.2f}" for tick in ticks], fontweight="bold", fontsize=42)  # 再设置标签
        
        # 确保坐标轴线和刻度线也加粗
        plt.setp(ax.spines.values(), linewidth=3)  # 坐标轴线加粗（从2增加到3）
        ax.tick_params(width=3, length=10)  # 刻度线加粗并延长
        
        plt.tight_layout()
        plt.savefig(f"{title.lower().replace(' ', '_')}.png", dpi=300)
        plt.close()

def parse_results_file(file_path):
    """解析实验结果文件，提取Delta和Epsilon的数据"""
    with open(file_path, "r") as f:
        content = f.read()

    # 分离Delta和Epsilon部分
    delta_section = (
        content.split("Delta实验结果:")[1].split("Epsilon实验结果:")[0].strip()
    )
    epsilon_section = content.split("Epsilon实验结果:")[1].strip()

    # 解析Delta数据
    delta_data = {}
    delta_pattern = r"delta_min=(\d+), delta_max=(\d+): 平均值=([\d\.]+), 标准差=([\d\.]+), 值=\[([\d\., ]+)\]"
    for match in re.finditer(delta_pattern, delta_section):
        delta_min = float(match.group(1))
        delta_max = float(match.group(2))
        mean_value = float(match.group(3))
        std_dev = float(match.group(4))
        values = [float(v) for v in match.group(5).split(", ")]
        delta_data[(delta_min, delta_max)] = values

    # 解析Epsilon数据
    epsilon_data = {}
    epsilon_pattern = r"eps_min=([\d\.]+), eps_max=([\d\.]+): 平均值=([\d\.]+), 标准差=([\d\.]+), 值=\[([\d\., ]+)\]"
    for match in re.finditer(epsilon_pattern, epsilon_section):
        eps_min = float(match.group(1))
        eps_max = float(match.group(2))
        mean_value = float(match.group(3))
        std_dev = float(match.group(4))
        values = [float(v) for v in match.group(5).split(", ")]
        epsilon_data[(eps_min, eps_max)] = values

    return delta_data, epsilon_data

def main():
    # 解析数据
    delta_data, epsilon_data = parse_results_file("summary_results.txt")
    
    # 绘制Delta热力图
    plot_param_sensitivity_heatmap(
        delta_data, 
        title="Delta Parameter Sensitivity", 
        x_label=r"$\boldsymbol{\delta_{max}}$",  # LaTeX加粗
        y_label=r"$\boldsymbol{\delta_{min}}$",  # LaTeX加粗
    )
    
    # 绘制Epsilon热力图
    plot_param_sensitivity_heatmap(
        epsilon_data, 
        title="Epsilon Parameter Sensitivity", 
        x_label=r"$\boldsymbol{\varepsilon_{max}}$",  # LaTeX加粗
        y_label=r"$\boldsymbol{\varepsilon_{min}}$",  # LaTeX加粗
    )
    
    print("热力图已生成并保存。")

if __name__ == "__main__":
    main()
