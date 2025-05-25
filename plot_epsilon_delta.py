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
plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"


def plot_param_sensitivity_heatmap(
    data_dict,
    title="Parameter Sensitivity Heatmap",
    x_label="step",
    y_label="min",
    use_latex=False,
):
    # 构造 DataFrame
    df = pd.DataFrame(
        [
            {"min": float(k[0]), "step": float(k[1]), "mean": sum(v) / len(v)}
            for k, v in data_dict.items()
        ]
    )
    pivot_df = df.pivot(index="min", columns="step", values="mean")

    # 设置大字体样式
    sns.set_context("notebook", font_scale=4.0)  # 字体放大约4倍

    # 使用学术字体
    with plt.style.context({"font.family": "serif", "font.serif": [chosen_font]}):
        # 绘图
        plt.figure(figsize=(16, 12))
        ax = sns.heatmap(
            pivot_df, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={"shrink": 0.5}
        )
        # plt.title(title, fontsize=48)
        plt.xlabel(x_label, fontsize=36)
        plt.ylabel(y_label, fontsize=36)
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=28)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=28)
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
    delta_pattern = r"delta_min=(\d+), delta_step=(\d+): 平均值=([\d\.]+), 标准差=([\d\.]+), 值=\[([\d\., ]+)\]"
    for match in re.finditer(delta_pattern, delta_section):
        delta_min = float(match.group(1))
        delta_step = float(match.group(2))
        mean_value = float(match.group(3))
        std_dev = float(match.group(4))
        values = [float(v) for v in match.group(5).split(", ")]
        delta_data[(delta_min, delta_step)] = values

    # 解析Epsilon数据
    epsilon_data = {}
    epsilon_pattern = r"eps_min=([\d\.]+), eps_step=([\d\.]+): 平均值=([\d\.]+), 标准差=([\d\.]+), 值=\[([\d\., ]+)\]"
    for match in re.finditer(epsilon_pattern, epsilon_section):
        eps_min = float(match.group(1))
        eps_step = float(match.group(2))
        mean_value = float(match.group(3))
        std_dev = float(match.group(4))
        values = [float(v) for v in match.group(5).split(", ")]
        epsilon_data[(eps_min, eps_step)] = values

    return delta_data, epsilon_data


def mannually_delta_epsilon_data():
    delta_data = {
        (1, 1): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (1, 2): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (1, 3): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (1, 4): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (1, 5): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (2, 1): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (2, 2): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (2, 3): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (2, 4): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (2, 5): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (3, 1): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (3, 2): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (3, 3): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (3, 4): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (3, 5): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (4, 1): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (4, 2): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (4, 3): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (4, 4): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (4, 5): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (5, 1): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (5, 2): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (5, 3): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (5, 4): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (5, 5): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (6, 1): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (6, 2): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (6, 3): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (6, 4): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        (6, 5): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    }
    epsilon_data = {}

    return delta_data, epsilon_data


def main():
    # 解析数据
    delta_data, epsilon_data = parse_results_file("summary_results.txt")

    # 绘制Delta热力图
    plot_param_sensitivity_heatmap(
        delta_data,
        title="Delta Parameter Sensitivity",
        x_label=r"$\Delta \delta$",
        y_label=r"$\delta_{min}$",
    )

    # 绘制Epsilon热力图
    # plot_param_sensitivity_heatmap(
    #     epsilon_data,
    #     title="Epsilon Parameter Sensitivity",
    #     x_label=r"$\varepsilon_{step}$",
    #     y_label=r"$\varepsilon_{min}$",
    # )

    print("热力图已生成并保存。")


if __name__ == "__main__":
    main()
