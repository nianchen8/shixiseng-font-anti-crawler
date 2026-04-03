# shixiseng-font-anti-crawler
实习僧招聘网站字体反爬破解，自动翻页并导出Excel

# 实习僧字体反爬数据采集

破解实习僧招聘网站的字体反爬，自动翻页采集岗位信息并导出 Excel。

## 功能特点

- 自动翻页，支持全站采集
- 动态下载每次请求变化的字体文件（woff）
- 使用 OCR（easyocr）识别加密字符，建立映射
- 自动清理临时字体文件
- 导出结构化 Excel 报表（职位、公司、薪资、城市、每周天数、持续月数、标签等）

## 技术栈

- Python 3.x
- requests / lxml
- fontTools / Pillow / easyocr
- openpyxl

## 安装与使用

### 1. 安装依赖

```bash
pip install requests lxml fontTools Pillow numpy easyocr openpyxl
首次运行 easyocr 会自动下载识别模型（约 300MB），耐心等待。

2. 运行脚本
bash
python 字体加密：每次请求变化（全页大规模单线程数据提取）.py
3. 配置说明
脚本中的 cookies 和 headers 可能需要根据实际情况更新。

默认采集关键词为“产品”，城市为“全国”，类型为“实习”，可在 params 中修改。

如需修改采集页数，可在 run() 方法的循环中调整 range(1, self.pages + 1)。

输出结果
运行成功后，会在当前目录生成 实习岗位.xlsx 文件，包含以下字段：

职位、公司、薪资、城市

每周天数、持续月数

标签（3个）、行业、企业规模、企业描述

注意事项
本脚本仅用于学习和研究，请勿对目标网站造成压力。

建议适当增加延时，降低请求频率。

字体文件每次请求会变化，脚本每次都会重新下载并建立映射，确保准确性。
