import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import matplotlib
import os

# 打印可用字体列表
print("Matplotlib 可用字体列表:")
fonts = sorted([f.name for f in fm.fontManager.ttflist])
for i, font in enumerate(fonts[:20]):
    print(f"- {font}")
print(f"总共 {len(fonts)} 种字体")

# 查找特定字体
target_font = "Linux Libertine"
print(f"\n查找 '{target_font}' 字体:")
fonts_with_name = [
    f for f in fm.fontManager.ttflist if target_font.lower() in f.name.lower()
]
if fonts_with_name:
    print(f"找到 {len(fonts_with_name)} 个匹配字体:")
    for font in fonts_with_name:
        print(f"  - 名称: {font.name}")
        print(f"    路径: {font.fname}")
else:
    print(f"未找到任何名称包含 '{target_font}' 的字体")

# 检查系统字体目录
print("\n系统字体目录内容:")
font_dirs = [
    "/Library/Fonts/",
    "/System/Library/Fonts/",
    os.path.expanduser("~/Library/Fonts/"),
]

for font_dir in font_dirs:
    if os.path.exists(font_dir):
        print(f"\n目录: {font_dir}")
        try:
            files = [f for f in os.listdir(font_dir) if "libertine" in f.lower()]
            if files:
                print(f"找到可能的 Libertine 字体文件:")
                for file in files:
                    print(f"  - {file}")
            else:
                print("未找到任何包含 'libertine' 的字体文件")
        except Exception as e:
            print(f"无法读取目录: {str(e)}")

# 手动注册字体
print("\n尝试手动注册字体:")
libertine_paths = []
for font_dir in font_dirs:
    if os.path.exists(font_dir):
        try:
            for file in os.listdir(font_dir):
                if "libertine" in file.lower() and (
                    file.endswith(".ttf") or file.endswith(".otf")
                ):
                    libertine_paths.append(os.path.join(font_dir, file))
        except Exception as e:
            print(f"无法读取目录 {font_dir}: {str(e)}")

if libertine_paths:
    print(f"找到 {len(libertine_paths)} 个 Libertine 字体文件:")
    for path in libertine_paths:
        print(f"  - {path}")
        try:
            font_prop = fm.FontProperties(fname=path)
            print(f"    成功加载字体: {font_prop.get_name()}")
        except Exception as e:
            print(f"    加载失败: {str(e)}")
else:
    print("未找到任何 Libertine 字体文件可手动注册")

# 手动重建字体缓存
print("\n尝试重建字体缓存:")
try:
    fm.findfont("Arial")  # 触发字体缓存重建
    fm._rebuild()
    print("字体缓存已重建")
except Exception as e:
    print(f"重建字体缓存失败: {str(e)}")

# 检查字体是否已正确注册
print("\n检查 Linux Libertine 是否已正确注册:")
libertine_main = "/Users/zihanwu/Library/Fonts/LinLibertine_R.ttf"
if os.path.exists(libertine_main):
    try:
        # 手动注册字体
        fm.fontManager.addfont(libertine_main)
        print(f"已手动注册字体: {libertine_main}")

        # 更新matplotlib配置
        print("\n更新字体配置示例:")
        print("plt.rcParams['font.family'] = 'serif'")
        print(
            "plt.rcParams['font.serif'] = ['Linux Libertine', 'DejaVu Serif', 'serif']"
        )

        # 创建示例使用
        print("\n在main.py中使用Linux Libertine的代码示例:")
        print(
            """
import matplotlib.font_manager as fm

# 手动注册Linux Libertine字体 
libertine_path = '/Users/zihanwu/Library/Fonts/LinLibertine_R.ttf'
fm.fontManager.addfont(libertine_path)

# 使用该字体
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Linux Libertine', 'DejaVu Serif', 'serif']
        """
        )
    except Exception as e:
        print(f"注册字体失败: {str(e)}")
else:
    print(f"找不到主要的Linux Libertine字体文件")
