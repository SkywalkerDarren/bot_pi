import json
import sys
import time

import psutil
from openai import OpenAI
from openai._types import NOT_GIVEN
from openai.types.chat import ChatCompletionToolMessageParam, ChatCompletionSystemMessageParam, \
    ChatCompletionUserMessageParam

from chat_service.llm.llm_engine import LLMEngine
from config import CONFIG


class OpenAIEngine(LLMEngine):
    def __init__(self):
        super().__init__()
        self.ai = OpenAI(api_key=CONFIG.openai.key, max_retries=3)
        self.model = CONFIG.openai.chat_model
        self.use_tool_count = 0
        self.max_use_tool_count = 10

    def system_prompt(self):
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
- 每次最多使用1个工具
- 接收来自用户的语音识别的结果
- 语音识别有小概率出错，你在回答问题时需要考虑到这一点
- 语气是聊天的风格，要接地气，不要太书面化
- 回复用户的问题

# Format
- 你有两种输出模式，一种是回答用户模式，一种是使用工具模式
- 使用工具模式
    - 在使用工具的情况下，你应该遵守工具的使用规则
- 回答用户模式
    - 无特殊要求的情况下回答应该尽可能的简短，通常在几个词语到几句话以内
    - 在回复用户问题的情况下，最终会通过TTS语音播报，所以不要输出markdown或代码块等无法听懂的信息，应该输出纯文本的回答
    - 你应该尽可能的使用中文回答用户的问题"""

    def chat(self, message, histories: list):
        """

        :param message:
        :param histories:
        :return: AI的最终回答
        """
        self.use_tool_count = 0
        messages = histories + [
            ChatCompletionUserMessageParam(
                role="user",
                content=message
            )
        ]
        content = self.bootstrap(messages)
        print(f"ai回答: {content}")
        return content, messages

    def bootstrap(self, messages):
        response = self._chat(messages)
        tools = self.try_get_tool(response)
        if tools:
            messages.append(response.choices[0].message)
            for tool in tools:
                assistant = f"使用工具: 名称: {tool.function.name}, 参数: {tool.function.arguments}"  # ai
                print(f"assistant: {assistant}")
                use_tool = next((t for t in self.tools if t.name == tool.function.name), None)
                args = self.try_get_args(tool.function.arguments)
                observer = use_tool.execute(args)
                user = f"观察结果: {observer}"  # user
                print(f"user: {user}")
                messages.append(ChatCompletionToolMessageParam(
                    role="tool",
                    content=observer,
                    tool_call_id=tool.id
                ))
            self.use_tool_count += len(tools)
            return self.bootstrap(messages)
        else:
            return self.get_text(response)

    def try_get_args(self, args: str):
        args = args.strip()
        if args.startswith("'") and args.endswith("'"):
            args = args[1:-1]
        elif args.startswith('"') and args.endswith('"'):
            args = args[1:-1]
        args = args.strip()
        if args:
            return json.loads(args)
        else:
            return None

    def try_get_tool(self, response):
        if response.choices[0].message.tool_calls:
            tools = response.choices[0].message.tool_calls
            return tools
        else:
            return []

    def get_text(self, response):
        return response.choices[0].message.content

    def _chat(self, messages):
        response = self.ai.chat.completions.create(
            model=self.model,
            n=1,
            messages=[
                         ChatCompletionSystemMessageParam(
                             role="system",
                             content=self.system_prompt()
                         )
                     ] + messages,
            tools=NOT_GIVEN if not self.tools else [t.get_info() for t in self.tools]
        )
        return response
