import os
"""
import os 是 Python 的内置模块导入语句，用于提供与操作系统交互的功能，主要包括：
文件和目录操作（创建、删除、重命名等）
路径管理（拼接、分割、获取绝对路径等）
环境变量访问
执行系统命令
这是 Python 中最常用的基础模块之一。
"""
import re
"""
import re 是导入 Python 的正则表达式模块，用于：
模式匹配：通过正则表达式搜索、匹配特定格式的文本
字符串处理：替换、分割、提取符合规则的字符串内容
数据验证：检查字符串是否符合特定格式（如邮箱、电话等）
这是文本处理和爬虫开发中常用的核心模块。
"""
import time
"""
import time 是导入 Python 的时间处理模块，主要功能包括：
时间获取：获取当前时间戳、日期时间
延时控制：使用 sleep() 让程序暂停执行
时间格式化：时间戳与字符串之间的转换
性能测试：计算代码执行时间
在爬虫脚本中常用于控制请求频率，避免被封禁。
"""
import shutil
"""
import shutil 是导入 Python 的高级文件操作模块，主要功能包括：
文件复制：拷贝文件和文件夹
文件移动/重命名：移动或重命名文件
文件删除：删除整个目录树
压缩解压：处理 zip、tar 等归档文件
相比 os 模块，shutil 提供更便捷的文件批量操作功能。
"""
import requests
"""
import requests 是导入 Python 的 HTTP 请求库，主要功能包括：
发送网络请求：支持 GET、POST 等各种 HTTP 方法
获取网页内容：下载 HTML、JSON、文件等资源
参数传递：轻松添加 URL 参数、请求头、表单数据
会话管理：保持 Cookie 和连接复用
这是 Python 爬虫开发中最常用的 HTTP 库，使用简单且功能强大。
"""
import numpy as np
"""
import numpy as np 是导入 Python 的数值计算库 NumPy，主要功能包括：
数组操作：提供高性能的多维数组对象
数学运算：支持大规模矩阵和数值计算
数据处理：用于数据分析和科学计算
在爬虫项目中可能用于处理批量数据、统计分析或加密算法相关的数值运算。
"""
from lxml import etree
"""
from lxml import etree 是从 lxml 库导入 XML/HTML 解析模块，主要功能包括：
HTML/XML 解析：快速解析网页结构，提取 DOM 树
XPath 查询：使用 XPath 表达式精准定位和提取元素内容
数据抓取：爬虫中用于从网页中提取所需数据
相比 BeautifulSoup，lxml 基于 C 库实现，解析速度更快，是爬虫开发中的主流选择。
"""
from openpyxl import Workbook
"""
from openpyxl import Workbook 是导入 Excel 文件操作类，主要功能包括：
创建工作簿：新建 Excel 文件（.xlsx 格式）
数据写入：向单元格写入数据、设置样式
表格管理：创建/删除工作表、调整行列属性
在该脚本中用于将爬取或处理的数据导出保存为 Excel 文件，便于后续分析和查看。
"""
# ========== 字体反爬专用模块 ==========
from fontTools.ttLib import TTFont   # 用于解析 .woff 字体文件，获取字符映射表
"""
作用：读取字体文件（.woff）的内部结构，获取字体里包含的所有“加密字符”的 unicode 编码。

为什么需要：因为网页里那些奇怪的符号（比如 ）其实是一个特殊的 unicode 字符，我们必须知道这个字符在字体文件里的编码，才能把它映射回真实数字。
"""
import easyocr   # 通用 OCR 库，支持中文/英文/数字等，用来识别图片上的字符
"""

作用：识别图片中的文字（可以是数字、字母、汉字等）。

为什么需要：我们生成了每个加密字符的图片，但不知道它对应什么真实字符。EasyOCR 会告诉我们图片里画的是“8”还是“薪”，这样我们就知道加密字符对应哪个真实字符，从而建立映射。

"""
from PIL import Image, ImageDraw, ImageFont   # 用于将字符渲染成图片（供 OCR 识别）
"""
作用：用我们下载的字体文件，把每个加密字符画成图片。

为什么需要：OCR 模型（EasyOCR）只能识别图片，不能直接识别字符的 unicode 编码。所以我们要先生成图片，再让 EasyOCR 去“看”这张图片里是什么数字/汉字。
"""
# ====================================

class Font:
    def __init__(self):
        self.html = ''
        self.mapping = {}   # 存储 {加密字符: 真实字符} 的映射关系，例如 {'\ue123': '8', '\ue456': '薪'}
        self.reader = easyocr.Reader(['ch_sim', 'en'])
        # 初始化 EasyOCR 识别器
        # 参数说明：
        #   ['ch_sim', 'en']  → 加载简体中文模型和英文模型，能够识别中文、数字、英文
        #   gpu=True          → 启用独立显卡（NVIDIA RTX 5060）加速，识别速度比 CPU 快很多,如果不写它会自动检测 .但是写了的话 会提速
        # 首次运行会自动下载模型（约 300 MB），耐心等待即可。之后不会重复下载。
        self.decrypted = []
        self.pages = ''

    #从网页链接获取html
    def get_html(self):
        url = 'https://www.shixiseng.com/interns'
        cookies = {
            '__jsluid_s': '8184c27a40831f5ffadd94d88296798e',
            'utm_source_first': 'PC',
            'utm_source': 'PC',
            'utm_campaign': 'PC',
            'position': 'pc_default',
            'Hm_lvt_03465902f492a43ee3eb3543d81eba55': '1774730140,1774954052',
            'Hm_lpvt_03465902f492a43ee3eb3543d81eba55': '1774954052',
            'HMACCOUNT': '85B371DDC9AC8F11',
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
            # 'cookie': '__jsluid_s=8184c27a40831f5ffadd94d88296798e; utm_source_first=PC; utm_source=PC; utm_campaign=PC; position=pc_default; Hm_lvt_03465902f492a43ee3eb3543d81eba55=1774730140,1774954052; Hm_lpvt_03465902f492a43ee3eb3543d81eba55=1774954052; HMACCOUNT=85B371DDC9AC8F11',
        }
        params = {
            'keyword': '产品',
            'city': '全国',
            'type': 'intern',
            'from': 'menu',
        }
        response = requests.get(url, cookies=cookies, headers=headers, params=params)
        self.html = response.text
        # print(response.status_code)
        # print(self.html)

    #获取网页总页数链接
    def get_page_num(self):
        HTML = etree.HTML(self.html)
        pages = HTML.xpath('//ul[@class="el-pager"]/li/text()')
        self.pages = int(pages[-1])

    #从html之中获取字体
    def get_font(self):
        p = re.compile(r'\((/interns/iconfonts/file\?rand=.+?)\)')#匹配字体文件
        font_url = 'https://www.shixiseng.com' + p.findall(self.html)[0]#获取字体文件链接
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0'}
        font_response =requests.get(font_url, headers=headers)

        with open ('./cache.woff','wb') as f:#
            f.write(font_response.content)
        # 功能：将下载的字体文件保存到本地
        # 分步说明：
        # open('./cache.woff', 'wb') - 以二进制写入模式打开（或创建）名为cache.woff的文件
        # font_response.content - 获取HTTP响应中的字体文件二进制数据
        # f.write() - 将二进制数据写入文件，完成字体文件下载
        # 作用：临时保存网页中的加密字体文件，供后续OCR识别使用。

    #构建映射关系
    def build_map(self):
        #1.  加载字体文件
        font = TTFont('./cache.woff')
        # 2. 获取字符映射表 (cmap)
        #    cmap 是字典，键是字符的 Unicode 码点（整数），值是对应的字形名称（如 'uniE123'）
        cmap = font.getBestCmap()
        try:
            pil_font = ImageFont.truetype('./cache.woff', size=100)#是 Pillow 库中用来加载字体文件的函数。第一个参数是字体文件的路径：'./cache.woff'（当前目录下的 cache.woff 文件）。第二个参数是字体大小（单位是像素），这里设为100
            """
            try 和 except 是 Python 的异常处理结构。

            程序先执行 try 块里的代码。如果执行过程中发生任何错误（比如文件不存在、格式不对、Pillow 无法识别等），Python 会立即跳到 except 块执行，而不会让程序崩溃。

            这里 except Exception 表示捕获任何类型的异常。因为无论什么原因导致加载失败，我们都希望采用备用方案。
            """
        except Exception :
            shutil.copy('./cache.woff', './cache.ttf')#将当前目录下的 cache.woff 文件复制一份，新文件名为 cache.ttf。注意：这只是简单改名，并没有真正解压，所以不一定总是有效，但经常能解决一部分问题。
            pil_font = ImageFont.truetype('./cache.ttf', size=100)#是 Pillow 库中用来加载字体文件的函数。第一个参数是字体文件的路径：'./cache.ttf'（当前目录下的 cache.ttf 文件）。第二个参数是字体大小（单位是像素），这里设为 100
            os.remove('./cache.ttf')

        for code_point in cmap.keys():#遍历字体文件中的字符，cmap 是一部字典（dictionary），它存储了字体文件中所有字符的信息。.keys() 是字典的一个方法，作用是取出字典中所有的键。
            img = Image.new('RGB', (200, 200), "white")
            # 功能：创建一张空白图片用于字符渲染
            # 参数说明：
            # 'RGB' - 图片颜色模式为红绿蓝三原色
            # (200, 200) - 图片尺寸为200×200像素
            #  "white" - 背景颜色为白色
            # 作用：生成一张纯白色的正方形画布，后续会在上面绘制加密字符（黑色），形成"白底黑字"的图片供OCR识别

            draw = ImageDraw.Draw(img)
            # 代码解释
            # 功能：创建绘图工具，准备在图片上画画
            # 详细说明：
            # ImageDraw.Draw(img) - 创建一个"画笔"对象
            # 这个画笔绑定到刚才创建的白色图片img上
            # 之后可以用这支"笔"在图片上绘制文字、图形等
            # 类比理解：
            # 如果img是一张白纸
            # draw就是一支可以在这张纸上写字画画的笔
            # 作用：为下一步在图片上绘制加密字符做准备。
            draw.text((20, 20), chr(code_point), font=pil_font, fill="black")
            # 功能：在白色图片上绘制加密字符
            # 参数说明：
            # (20, 20) - 文字起始坐标（距左上角各20像素）
            # chr(code_point) - 要绘制的字符（将Unicode编码转为字符，如 ）
            # font = pil_font - 使用下载的加密字体文件渲染
            # fill = "black" - 文字颜色为黑色
            # 作用：用特殊字体把加密字符画成"白底黑字"的图片，让OCR能识别出它真实是什么数字 / 文字。
            result = self.reader.readtext(np.array(img), detail=0)
            # 使用EasyOCR识别图片中的文字，返回识别结果列表
            if result:# 判断是否识别成功
                self.mapping[chr(code_point)] = result[0]# 如果结果不为空，将字符映射到对应的识别结果

    #获取源码数据
    def get_data(self):
        HTML = etree.HTML(self.html)#使用 lxml 库解析 HTML
        items = HTML.xpath('//div[@class="intern-wrap interns-point intern-item"]')#获取所有职位信息
        result = []#创建一个空列表，用于存储结果
        for item in items:#遍历每一项
            # 职位
            position = item.xpath('.//div[@class="f-l intern-detail__job"]/p[1]/a/text()')
            position = position[0] if position else ''# 判断职位是否为空，如果为空则赋值为空字符串，否则取第一个元素
            # 薪资
            salary = item.xpath('.//span[@class="day font"]/text()')
            salary = salary[0] if salary else ''
            # 城市
            city = item.xpath('.//p[@class="tip"]/span[1]/text()')
            city = city[0] if city else ''
            # 每周天数
            week = item.xpath('.//p[@class="tip"]/span[3]/text()')
            week = week[0] if week else ''
            # 月数
            month = item.xpath('.//p[@class="tip"]/span[5]/text()')
            month = month[0] if month else ''
            # 企业名称
            company = item.xpath('.//div[@class="f-r intern-detail__company"]/p[1]/a/text()')
            company = company[0] if company else ''
            # 行业
            industry = item.xpath('.//div[@class="f-r intern-detail__company"]/p[2]/span[1]/text()')
            industry = industry[0] if industry else ''
            # 企业规模
            company_scale = item.xpath('.//div[@class="f-r intern-detail__company"]/p[2]/span[3]/text()')
            company_scale = company_scale[0] if company_scale else ''
            # 职位标签
            job_labels = item.xpath('.//div[@class="f-l"]/span/text()')
            # 企业描述
            company_desc = item.xpath('.//div[@class="f-r ellipsis"]/span/text()')
            company_desc = company_desc[0] if company_desc else ''

            row = [
                position,
                company,
                salary,
                city,
                week,
                month,
                job_labels[0] if len(job_labels) > 0 else '',# 安全提取，防止越界
                job_labels[1] if len(job_labels) > 1 else '',
                job_labels[2] if len(job_labels) > 2 else '',
                industry,
                company_scale,
                company_desc
            ]#创建一个列表，用于存储处理后的数据
            result.append(row)# 将处理后的数据append添加到result = []结果列表中
        return result #return返回处理后的数据result

    #解密函数
    def decrypt(self,text):
        r = ''#创建空字符串用于存储解密结果
        for ch in text:#遍历加密后的文本text
            if ch in self.mapping:#如果该字符在映射表中（是加密字符）
                r += self.mapping[ch]#映射成真实文字后拼接
            else:
                r += ch #如果不在映射表中（普通字符），保持原样
        return r #返回解密后的完整文本

    #清除下载的字体文件
    def clear(self):
        os.remove('./cache.woff')

    #保存为excel文件
    def save_to_excel(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "实习岗位"  # 可自定义工作表名称

        # 写入列标题
        headers = ['职位', '公司', '薪资', '城市', '每周天数', '持续月数',
                   '标签1', '标签2', '标签3', '行业', '企业规模', '企业描述']
        ws.append(headers)

        # 写入数据
        for row in self.decrypted:
            ws.append(row)

        wb.save("实习岗位.xlsx")
        print("数据已保存到 实习岗位.xlsx")

    def run(self):
        self.get_html()
        self.get_page_num()
        for page_num in range(1, self.pages + 1):
            time.sleep(1)
            print(f"正在爬取第 {page_num} 页...")
            url = f'https://www.shixiseng.com/interns?page={page_num}'
            cookies = {
                '__jsluid_s': '8184c27a40831f5ffadd94d88296798e',
                'utm_source_first': 'PC',
                'utm_source': 'PC',
                'utm_campaign': 'PC',
                'position': 'pc_default',
                'Hm_lvt_03465902f492a43ee3eb3543d81eba55': '1774730140,1774954052',
                'Hm_lpvt_03465902f492a43ee3eb3543d81eba55': '1774954052',
                'HMACCOUNT': '85B371DDC9AC8F11',
            }
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Microsoft Edge";v="146"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0',
                # 'cookie': '__jsluid_s=8184c27a40831f5ffadd94d88296798e; utm_source_first=PC; utm_source=PC; utm_campaign=PC; position=pc_default; Hm_lvt_03465902f492a43ee3eb3543d81eba55=1774730140,1774954052; Hm_lpvt_03465902f492a43ee3eb3543d81eba55=1774954052; HMACCOUNT=85B371DDC9AC8F11',
            }
            params = {
                'keyword': '产品',
                'city': '全国',
                'type': 'intern',
                'from': 'menu',
            }
            response = requests.get(url, cookies=cookies, headers=headers, params=params)
            self.html = response.text
            self.get_font()
            self.build_map()
            self.clear()
            data_list = self.get_data()#接收源码数据return result
            decrypted = []
            for row in data_list:
                decrypted_row = [self.decrypt(item) for item in row]#self.decrypt(item)创造临时变量item接收return r
                self.decrypted.append(decrypted_row)
            print(f'第 {page_num} 页爬取完成')

        self.save_to_excel()

if __name__ == '__main__':
    font = Font()
    font.run()