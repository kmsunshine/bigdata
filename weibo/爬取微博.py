import requests
import random
import time
import re
import json
import csv
import os
import requests
print(requests.get("https://m.weibo.cn").status_code)
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

weibo_id = "5178410051044212"
start_url = f"https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id_type=0"

headers = {
    'cookie': '网页获取cookie',
    'user-agent': '网页获取user-agent',
}

save_mode = 'csv'
csv_file = open("weibo_comments.csv", "w", encoding="utf-8-sig", newline='') if save_mode == 'csv' else None
csv_writer = csv.writer(csv_file) if csv_file else None
if csv_writer:
    csv_writer.writerow(["编号", "评论时间", "用户ID", "昵称", "评论楼层", "评论内容"])

txt_file = open("weibo_comments.txt", "w", encoding="utf-8") if save_mode == 'txt' else None

def clean_text(html_text):
    return ''.join(re.findall(r'[\u4e00-\u9fa5，。！？：；、“”‘’（）——]', html_text))

def save_comment(index, create_time, user_id, screen_name, floor_number, text):
    if save_mode == 'csv':
        csv_writer.writerow([index, create_time, user_id, screen_name, floor_number, text])
    elif save_mode == 'txt':
        txt_file.write(f"{index} | {create_time} | {user_id} | {screen_name} | 第{floor_number}楼 | {text}\n")

def get_comments(start_url, max_pages=100):
    url = start_url
    count = 0
    for page in range(max_pages):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                print(f"请求失败：状态码 {resp.status_code}")
                break
            data = resp.json()
        except Exception as e:
            print(f"请求异常：{e}")
            break

        if data.get("ok") != 1:
            print("没有更多数据或接口失败")
            break

        comments = data['data']['data']
        max_id = data['data'].get('max_id')

        for item in comments:
            count += 1
            create_time = item['created_at']
            floor_number = item.get('floor_number', '无')
            text = clean_text(item['text'])
            user_id = item['user']['id']
            screen_name = item['user']['screen_name']

            save_comment(count, create_time, user_id, screen_name, floor_number, text)
            print(f"{count}. {screen_name}：{text}")

        if not max_id:
            break
        url = f"https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id={max_id}&max_id_type=0"
        time.sleep(random.uniform(1, 3))  # 防止被封

    print(f"\n✅ 共抓取 {count} 条评论")

get_comments(start_url, max_pages=50)

if csv_file:
    csv_file.close()
if txt_file:
    txt_file.close()
