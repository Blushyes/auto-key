# auto-key

#### 介绍

一个简单的自动化按键脚本工具。

#### 如何运行？

1. 首先安装 Python 环境
2. 安装所需的库
   ```shell
   python.exe -m pip install --upgrade pip
   pip install -r environment.txt
   ```

3.1 打开`main.py`即可运行

3.2 打开`main_gui.py`运行图形界面版

![alt text](assets/gui.gif)

#### 目录结构

```
.
├── main.py
├── main_gui.py
├── environment.txt
├── scripts # 脚本存放处
│   ├── meta.example.json # meta.json的示例
│   ├── test_script
│   │   ├── meta.json
│   │   └── ...
│   ├── your_script # 你的脚本
│   │   ├── meta.json # 你的脚本的相关信息
│   │   ├── index.xlsx # 你的Excel脚本
│   │   └── ...
└── script_loader # 脚本加载器，规定了一些关于脚本加载有关的接口
│   ├── excel_loader.py # Excel脚本加载器
│   └── ...
└── executor # 规定了脚本执行器接口
│   ├── simple.py # 最简单的脚本执行器
│   └── ...
└── interaction # 规定了交互接口
│   ├── command_line.py # 命令行交互
│   └── ...
└── ...
```

#### 编写脚本

你可以参照`script`目录下面的`test_script`
来实现专属于你的脚本，只要创建一个脚本的文件夹，名字随便定，记得配置好脚本信息`meta.json`。

目前仅支持`Excel`脚本的方式，你可以通过在`script_loader`目录下创建实现了`main.py`中的`ScriptLoader`接口的类的文件来创建属于自己的脚本解析方式。
