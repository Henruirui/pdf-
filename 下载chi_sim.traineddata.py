import requests

url = 'https://raw.githubusercontent.com/tesseract-ocr/tessdata/main/chi_sim.traineddata'
# 根据实际情况修改保存路径
save_path = r'C:\Program Files\Tesseract-OCR\tessdata\chi_sim.traineddata'

# 设置代理
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

response = requests.get(url, proxies=proxies)
if response.status_code == 200:
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print('文件下载成功！')
else:
    print(f'下载失败，状态码：{response.status_code}')