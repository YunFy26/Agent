import os
import dashscope
from dashscope.api_entities.dashscope_response import Message
from logger import logger
import json
from prompt import user_split_task_prompt, user_action_task_prompt


class QwenSplitTask:
    def __init__(self):
        self.api_key = os.environ.get('DASHSCOPE_API_KEY')
        self.model_name = os.environ.get('MODEL_NAME_1')
        self.client = dashscope.Generation()

    def chat(self, prompt):
        try:
            # 构造messages
            messages = [Message(role="system", content=prompt)]
            messages.append(Message(role="user", content=user_split_task_prompt))
            # 请求llm
            response = self.client.call(
                model=self.model_name,
                api_key=self.api_key,
                messages=messages)
            content = json.loads(response["output"]["text"])
            return content
        except Exception as e:
            logger.info("call llm exception:{}".format(e))
        return {}


class QwenAction:
    def __init__(self):
        self.api_key = os.environ.get('DASHSCOPE_API_KEY')
        self.model_name = os.environ.get('MODEL_NAME_1')
        self.client = dashscope.Generation()

    def chat(self, prompt):
        try:
            # 构造messages
            messages = [Message(role="system", content=prompt)]
            messages.append(Message(role="user", content=user_action_task_prompt))

            # 请求llm
            response = self.client.call(
                model=self.model_name,
                api_key=self.api_key,
                messages=messages)

            content = json.loads(response["output"]["text"])
            return content
        except Exception as e:
            logger.info("call llm exception:{}".format(e))
        return {}
