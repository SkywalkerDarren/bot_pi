from typing import Optional

import docker
from pydantic import BaseModel

from chat_service.ai_tools import BaseTool
from config import PROJECT_ROOT


def _run_code(code_block: str):
    client = docker.from_env()

    with open(f"{PROJECT_ROOT}/temp_docker/temp.py", "w", encoding='utf-8') as f:
        f.write(code_block)

    docker_id = 'temp_code_run'

    client.images.build(path=f"{PROJECT_ROOT}/temp_docker", tag=docker_id, rm=True, forcerm=True)
    result = client.containers.run(docker_id, remove=True, stderr=True)

    print("Container output:")
    print(result.decode('utf-8'))

    # 步骤 3: 清理资源 - 删除容器和镜像
    print("Cleaning up...")
    client.images.remove(image=docker_id, force=True)

    print("Done.")
    return result.decode('utf-8')


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
        return _run_code(code_block)
