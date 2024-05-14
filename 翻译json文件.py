import json
from pygtrans import Translate

# JSON文件路径
json_file_path = 'en_us.json'
# 输出文件路径
output_file_path = 'zh_cn.json'

# 实例化翻译接口并设置VPN代理端口
client = Translate(proxies={'https': 'http://localhost:8848'})

# 读取JSON文件
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 遍历JSON数据提取所有值
values = [str(value) for value in data.values()]

# 把要翻译的文本交给服务器并接收
translation_results = client.translate(values)
# 处理返回结果并放到一个列表里
translation_results = [text.translatedText for text in translation_results]

# 确保翻译后的键数量与文本文件中的值数量相匹配
if len(data) != len(translation_results):
    print(
        f"警告：JSON中的键数量与翻译结果中的值数量不匹配！源文件中有{len(data)}个元素，而翻译结果却有{len(translation_results)}个元素")
else:
    for key, value in data.items():
        data[key] = translation_results.pop(0)  # 逐个取出值并赋给对应的键
        # 保存到新文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)

print("所有键对应的值已翻译并保存至:", output_file_path)
