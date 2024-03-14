import json
import time

import psutil
from openai import OpenAI

from chat_service.run_code_tool import RunCodeTool
from chat_service.search_engine_tool import SearchEngineTool
from config import CONFIG


class ChatManager:
    def __init__(self, search_service, voice_assistant_controller):
        self.ai = OpenAI(api_key=CONFIG.openai.key)
        self.model = CONFIG.openai.chat_model
        self.tool_list = [
            RunCodeTool(),
            SearchEngineTool(search_service),
        ]
        self.tool_use_limit = 5
        self.tool_use_count = 0
        self.system_prompt = {
            "role": "system",
            "content": f"""\
# Role
你现在是一个叫做'波特派'的语音助手。

# Status
- 当前系统：Raspberry Pi 5
- 当前的地区：中国，深圳
- 当前的时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
- 当前的CPU温度：{psutil.sensors_temperatures()['cpu_thermal'][0].current}℃
- 当前的CPU使用率：{psutil.cpu_percent()}%
- 当前的内存使用率：{psutil.virtual_memory().percent}%
- 当前的风扇转速：{psutil.sensors_fans()['pwmfan'][0].current}RPM
- 一共可使用的工具次数：{self.tool_use_limit}，剩余可使用的工具次数：{self.tool_use_limit - self.tool_use_count}

# Task
- 你可以使用工具来帮助用户解决问题，但连续使用工具的次数有限
- 你一次可以使用多种工具
- 接收来自用户的语音识别的结果
- 语音识别有小概率出错，你在回答问题时需要考虑到这一点
- 语气是聊天的风格，要接地气，不要太书面化
- 回复用户的问题

# Format
- 在使用工具的情况下，你应该遵守工具的使用规则
- 无特殊要求的情况下回答应该尽可能的简短，通常在几个词语到几句话以内
- 在回复用户问题的情况下，最终会通过TTS语音播报，所以不要输出markdown或代码块等无法听懂的信息，应该输出纯文本的回答
- 你应该尽可能的使用中文回答用户的问题"""
        }

    def chat(self, message):
        messages = [
            {
                "role": "user",
                "content": message
            }
        ]
        response = self.ai.chat.completions.create(
            model=self.model,
            n=1,
            messages=[
                         self.system_prompt,
                     ] + messages,
            tools=[t.get_info() for t in self.tool_list]
        )
        if response.choices[0].message.tool_calls:
            msg = ""
            tools = response.choices[0].message.tool_calls
            for tool in tools:
                msg += f"使用工具: {tool.function.name} {tool.function.arguments}\n"
                use_tool = next((t for t in self.tool_list if t.name == tool.function.name), None)
                observer = use_tool.execute(json.loads(tool.function.arguments))
                msg += f"观察结果: {observer}\n"
            print(f'ai: {msg}')
            messages.append({
                'role': 'assistant',
                'content': msg
            })
            messages.append({
                'role': 'user',
                'content': '请根据观察结果进行人性化的回复。'
            })
            response = self.ai.chat.completions.create(
                n=1,
                model=self.model,
                messages=[
                             self.system_prompt,
                         ] + messages,
            )
        content = response.choices[0].message.content
        print(f"ai回答: {content}")
        return content
