import requests
from model import UserData


def send_post_request(name, score, callback):
    # url = 'http://127.0.0.1:6600/api/score'
    url = 'http://101.200.131.69:80/api/score'
    data = {'name': name, 'score': score}

    response = requests.post(url, data)

    if response.status_code == 200:
        print("POST request successful")

        # text_data = response.text  # 获取文本内容
        # print(text_data)

        json_data = response.json()  # 解析 JSON 数据
        print(json_data)

        # user_objects = []
        # for item in json_data['data']:
        #     user_object = UserData(item['id'], item['user_name'], item['score'])
        #     user_objects.append(user_object)

        callback(json_data['data'])

    else:
        print(f"POST request failed with status code: {response.status_code}")



# 调用函数发送 POST 请求
# name = 'John'
# score = 95
# send_post_request(name, score)
