from typing import Type, Optional

from pydantic import BaseModel, ValidationError


class BaseTool:
    def __init__(self, name, description, param_model: Type[BaseModel] = None):
        self.name = name
        self.description = description
        self.param_model = param_model

    def execute(self, parameters: dict = None) -> str:
        try:
            if self.param_model and parameters:
                # 使用 pydantic 模型校验参数
                try:
                    validated_params = self.param_model(**parameters)
                except ValidationError as e:
                    raise ValueError(f"Parameter validation error: {e}")
            else:
                validated_params = None

            return self.run(validated_params)
        except Exception as e:
            return f"使用工具异常: {e}"

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
