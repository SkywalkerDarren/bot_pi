import time

import psutil
from openai import OpenAI

from config import CONFIG


class ChatManager:
    def __init__(self):
        self.ai = OpenAI(api_key=CONFIG["openai_key"])
        self.model = "gpt-4-0125-preview"
        self.system_prompt = {
            "role": "system",
            "content": f"""\
# Role
你现在是一个叫做'波特派'的语音助手。

# Status
- 当前系统：Raspberry Pi 5
- 当前的时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
- 当前的CPU温度：{psutil.sensors_temperatures()['cpu_thermal'][0].current}℃
- 当前的CPU使用率：{psutil.cpu_percent()}%
- 当前的内存使用率：{psutil.virtual_memory().percent}%
- 当前的风扇转速：{psutil.sensors_fans()['pwmfan'][0].current}RPM

# Task
- 接收来自用户的语音识别的结果
- 语音识别有小概率出错，你在回答问题时需要考虑到这一点
- 语气是聊天的风格，要接地气，不要太书面化
- 回复用户的问题

# Format
- 无特殊要求的情况下回答应该尽可能的简短，通常在几个词语到几句话以内
- 在回复用户问题的情况下，不要输出markdown或代码块，应该输出纯文本的回答
- 你应该尽可能的使用中文回答用户的问题
        """
        }

    def chat(self, message):
        resp = self.ai.chat.completions.create(
            model=self.model,
            n=1,
            messages=[
                self.system_prompt,
                {
                    "role": "user",
                    "content": message
                }
            ],
        )
        content = resp.choices[0].message.content
        print(f"ai: {content}")
        return content
