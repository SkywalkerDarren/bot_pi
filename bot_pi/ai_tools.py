import json
from dataclasses import asdict

import docker
from pydantic import BaseModel, ValidationError

from typing import Type, Optional


class BaseTool:
    def __init__(self, name, description, param_model: Type[BaseModel] = None):
        self.name = name
        self.description = description
        self.param_model = param_model

    def execute(self, parameters: dict = None) -> str:
        if self.param_model and parameters:
            # 使用 pydantic 模型校验参数
            try:
                validated_params = self.param_model(**parameters)
            except ValidationError as e:
                raise ValueError(f"Parameter validation error: {e}")
        else:
            validated_params = None

        return self.run(validated_params)

    def run(self, validated_params: Optional[BaseModel]) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_info(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.param_model.model_json_schema() if self.param_model else None
            }
        }


class RunCodeTool(BaseTool):
    class RunCodeParams(BaseModel):
        """
        可以是多行的python代码块
        """
        code_block: str

    def __init__(self):
        super().__init__("run_code", "运行python代码块，如```print('hello world')```", self.RunCodeParams)

    def run(self, validated_params: Optional[BaseModel]) -> str:
        code_block = validated_params.code_block
        return self.run_code(code_block)

    def run_code(self, code_block: str):
        client = docker.from_env()
        container = client.containers.run("python:3.11.8", command=['python', '-c', code_block], )
        return container.decode('utf-8')
