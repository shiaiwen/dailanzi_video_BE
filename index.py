# /?spm_id_from=333.337.search-card.all.click&vd_source=3fa8aad56b1e39079241152dbdd9c2a0
# https://www.bilibili.com/video/BV17Y4y1J7Za

import requests
import re
import json
from pprint import pprint
import subprocess
import os
import time

link = 'https://api.bilibili.com/x/web-interface/wbi/search/type?__refresh__=true&_extra=&context=&page=7&page_size=42&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword=%E6%8A%BD%E8%B1%A1%E5%B8%A6%E7%AF%AE%E5%AD%90&qv_id=J38XLwwxIaRfDPV5xct2AYQeZxDJlGyM&ad_resource=5654&source_tag=3&category_id=&search_type=video&dynamic_offset=216&w_rid=27d638084ff6410bb1c5e11e68caafb0&wts=1674030628'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'referer': 'https://www.bilibili.com/video'
}
res = requests.get(url=link, headers=headers)
# pprint(res.json()['data']['result'])
for index in res.json()['data']['result']:
    # print(1234)
    bvid = index['bvid']
    # print(bvid)
    url = f'https://www.bilibili.com/video/{bvid}'
    text = requests.get(url=url, headers=headers).text
    # print(text)
    # 3.解析数据
    t = time.time()
    t = int(t) 
    # title = re.findall('"title":"(.*?)","pubdate"', text)[0].replace(" ", "")
    title = f'带蓝子{bvid}{t}'
    print(title)
    htmlData = re.findall(
        '<script>window.__playinfo__=(.*?)</script>', text)[0]
    jsonData = json.loads(htmlData)
    # print(jsonData)
    # pprint(jsonData)
    audio_url = jsonData['data']['dash']['audio'][0]['baseUrl']
    video_url = jsonData['data']['dash']['video'][0]['baseUrl']
    # print(audio_url)
    audio_content = requests.get(url=audio_url, headers=headers).content
    video_content = requests.get(url=video_url, headers=headers).content
    if audio_content and video_content:
      with open('video\\'+title+'.mp3', mode='wb') as f:
          f.write(audio_content)
      with open('video\\'+title+'.mp4', mode='wb') as f:
          f.write(video_content)
      cmd = f"ffmpeg -i video\\{title}.mp4 -i video\\{title}.mp3 -c:v copy -c:a aac -strict experimental video\\{title}output.mp4"
      subprocess.run(cmd, shell=True)
      # ffmpeg.exe -i audio1.mp4 -i video.mp4 -acodec copy -vcodec copy output.mp4
      os.remove(f'video\\{title}.mp4')
      os.remove(f'video\\{title}.mp3')
