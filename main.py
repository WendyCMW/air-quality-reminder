import requests
import os
import sys

# --- 配置区域 ---
# 这里从 GitHub 的保险箱读取 Token，你不需要动这里
waqi_token = os.environ.get('WAQI_TOKEN')
push_token = os.environ.get('PUSH_TOKEN')

# 请修改这里为你所在的城市拼音 (例如: beijing, shanghai, chengdu)
CITY = 'shanghai' 

def get_air_quality():
    """获取空气质量数据"""
    url = f"https://api.waqi.info/feed/{CITY}/?token={waqi_token}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == 'ok':
            aqi = data['data']['aqi']
            return aqi
        else:
            print("数据获取失败:", data)
            return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

def send_wechat_push(title, content):
    """发送微信推送"""
    url = "http://www.pushplus.plus/send"
    data = {
        "token": push_token,
        "title": title,
        "content": content
    }
    requests.post(url, json=data)

def main():
    print(f"开始检查 {CITY} 的空气质量...")
    aqi = get_air_quality()
    
    if aqi is None:
        send_wechat_push("空气助手出错了", "无法获取空气质量数据，请检查代码或网络。")
        return

    # --- 判断逻辑 ---
    # AQI > 100 属于不健康，> 150 属于中度污染
    msg_title = ""
    msg_content = f"今日 {CITY} 空气指数 (AQI): {aqi}。"
    
    if aqi <= 50:
        msg_title = "空气超棒！🌿"
        msg_content += " 空气非常清新，尽情深呼吸吧！"
    elif aqi <= 100:
        msg_title = "空气良好 🍃"
        msg_content += " 空气质量不错，可以正常活动。"
    elif aqi <= 150:
        msg_title = "⚠️ 轻度污染提醒"
        msg_content += " 敏感人群建议佩戴口罩，减少户外运动。"
    else:
        msg_title = "🔴 严重污染警告！"
        msg_content += " **请务必佩戴口罩！** 尽量避免出门！😷"

    # 只有当污染严重时才推送？还是每天都推送？
    # 这里设置为每天都推送，让你安心。
    print(f"检测结果: {msg_title}")
    send_wechat_push(msg_title, msg_content)

if __name__ == "__main__":
    main()
