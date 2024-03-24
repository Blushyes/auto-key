# auto-key

## 介绍

一个简单的自动化按键脚本工具。

## 如何运行

1. 首先安装 Python 环境
1. 安装所需的库
   ```shell
   python.exe -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
1. 打开`main.py`即可运行

识图点击：

![alt text](assets/gui.gif)

识图后依偏移量点击：

![alt text](assets/使用偏移量点击（两个记事本的关闭按钮图形一样）.gif)

- 两个记事本的关闭按钮图形一样，都是“ X ”，单纯识别“ X ”可能会误操作，这是就需要识别标题再根据标题偏移“ offset_x ” “ offiset_y ”位置，再进行点击。

模拟快捷键：

![alt text](assets/模拟快捷键.gif)

- 模拟按下 “Win+R”

## 切换交互

通过更改`config.json`中的`interaction`字段来切换交互

| 选项           | 说明         |
| -------------- | ------------ |
| `command_line` | 命令行交互   |
| `gui`          | GUI 界面交互 |

你也可以在`interaction`包下添加自定义交互，然后在`interaction.factory`中注册你的交互即可。

## 图形界面版全局快捷键

- `F6` 运行脚本

- `F9` 暂停脚本 （鼠标移至屏幕左上角也可暂停）

  可以在 `.\executor\cosmic.py`修改快捷键按键设置

## 目录结构

```python
📁 auto-key/
├─📄LICENSE
├─📜main.py                     # 运行命令行版 auto-key
├─✏️README.md
├─✏️requirements.txt            # 依赖库
├─📁 scripts/                   # 脚本存放处
├─📁 context/
│ ├─📜logging.py
├─📁 executor/                  # 规定了脚本执行器接口
│ ├─📜cosmic.py                 # 需要跨模块访问的变量值，可以在这里 修改快捷键按键设置
│ ├─📜main.py
│ ├─📜simple.py                 # 最简单的脚本执行器
├─📁 interaction/               # 规定了交互接口
│ ├─📄auto_key.ui
│ ├─📜command_line.py           # 命令行交互
│ ├─📜gui.py                    # 图形界面交互
│ ├─📜main.py
│ ├─📜shortcut_handler.py
│ ├─📜Ui_auto_key.py
│ ├─✏️meta.example.json         # meta.json的示例
│ ├─📁 test_calc/
│ ├─📁 test_csv_file_script/
│ └─📁 test_script/
└─📁 script_loader/             # 脚本加载器，规定了一些关于脚本加载有关的接口
  ├─📜excel_loader.py
  ├─📜main.py
```

## 编写脚本

你可以参照`script`目录下面的`test_script`
来实现专属于你的脚本，只要创建一个脚本的文件夹，名字随便定，记得配置好脚本信息`meta.json`。

目前仅支持`Excel`脚本的方式，你可以通过在`script_loader`目录下创建实现了`main.py`中的`ScriptLoader`接口的类的文件来创建属于自己的脚本解析方式。
