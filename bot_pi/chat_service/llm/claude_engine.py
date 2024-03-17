import json
import sys
import time

import psutil
from anthropic import Anthropic

from chat_service.llm.llm_engine import LLMEngine
from config import CONFIG


class ClaudeEngine(LLMEngine):
    def __init__(self):
        super().__init__()
        self.client = Anthropic(api_key=CONFIG.anthropic.key)
        self.model_name = CONFIG.anthropic.model
        self.use_tool_count = 0
        self.max_use_tool_count = 10

    def system_prompt(self):
        tools_json = '\n'.join(json.dumps(t.get_info()['function'], ensure_ascii=False) for t in self.tools)
        if sys.platform == 'win32':
            status_msg = f"""\
- 当前系统：windows 11
- 当前的地区：中国，深圳
- 当前的时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
- 当前剩余使用工具的次数：{self.max_use_tool_count - self.use_tool_count}"""
        else:
            status_msg = f"""\
- 当前系统：Raspberry Pi 5
- 当前的地区：中国，深圳
- 当前的时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
- 当前的CPU温度：{psutil.sensors_temperatures()['cpu_thermal'][0].current}℃
- 当前的CPU使用率：{psutil.cpu_percent()}%
- 当前的内存使用率：{psutil.virtual_memory().percent}%
- 当前的风扇转速：{psutil.sensors_fans()['pwmfan'][0].current}RPM
- 当前剩余使用工具的次数：{self.max_use_tool_count - self.use_tool_count}"""
        return f"""\
# Role
你现在是一个叫做'波特派'的语音助手。

# Status
{status_msg}

# Task
- 你可以使用工具来帮助用户解决问题
- 接收来自用户的语音识别的结果
- 语音识别有小概率出错，你在回答问题时需要考虑到这一点
- 语气是聊天的风格，要接地气，不要太书面化
- 回复用户的问题

# Function tool
这里有一些工具可以帮助你解决问题，使用工具时你需要知道工具的使用规则，工具有自己的名称和描述，工具参数的输入使用的是json schema进行约束，以下是一些例子：

## Function Example
以下是一个示例工具的表示：
{{
    "name": "foo_tool",
    "description": "这是一个示例工具",
    "parameters": {{
        "type": "object",
        "properties": {{
            "foo": {{
                "type": "string",
                "description": "foo参数"
            }}
        }},
        "required": ["foo"]
    }}
}}

以下是一个示例工具的使用方式，使用工具时你应该按照如下格式的json进行返回：
{{
    "name": "foo_tool",
    "parameters": {{
        "foo": "bar"
    }}
}}

以下是一个调用链路的展示
user: 测试使用实例工具
assistant: {{"name": "foo_tool", "parameters": {{"foo": "bar"}}}}

## Tool list
{tools_json}

# Format
- 你的回答模式有两种，一种是普通的回答，一种是使用工具的回答
— 工具模式：
    - 你应该遵守工具的使用规则
    - 你只能返回一个json格式来调用工具，不能有其他的输出，你的回答应该只有一行才对
    - 对于回答我将使用json.loads进行检测，检测失败会被视为文本模式
    - 不要回答任何不符合工具规则的内容，包括json的前导文本和后续文本等
- 文本模式：
    - 无特殊要求的情况下回答应该尽可能的简短，通常在几个词语到几句话以内
    - 在回复用户问题的情况下，最终会通过TTS语音播报，所以不要输出markdown或代码块等无法听懂的信息，应该输出纯文本的回答
    - 你应该尽可能的使用中文回答用户的问题"""

    def chat(self, message):
        messages = [
            {
                "role": "user",
                "content": message
            }
        ]
        text = self.bootstrap(messages)

        return text

    def bootstrap(self, messages):
        text = self._chat(messages)
        print(f"ai回答: ->{text}<-")
        tool = self.try_get_tool(text)
        if tool:
            msg = ""
            for t in self.tools:
                if t.name == tool['name']:
                    print(f"使用工具: {t.name} {tool['parameters']}")
                    msg += f"使用工具: {t.name} {tool['parameters']}\n"
                    result = t.execute(tool['parameters'])
                    print(f"观察结果: {result}")
                    msg += f"观察结果: {result}"
            messages.append({
                'role': 'assistant',
                'content': text
            })
            messages.append({
                'role': 'user',
                'content': msg
            })
            return self.bootstrap(messages)
        else:
            return text

    def try_get_tool(self, text):
        for t in text.split('\n'):
            try:
                return json.loads(t)
            except json.JSONDecodeError:
                continue
        return {}

    def _chat(self, messages):
        response = self.client.messages.create(
            system=self.system_prompt(),
            messages=messages,
            model=self.model_name,
            max_tokens=4096
        )
        text = response.content[0].text
        return text.strip()
