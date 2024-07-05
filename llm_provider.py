import os
import dashscope
from dashscope.api_entities.dashscope_response import Message
from logger import logger
import json
from prompt import user_prompt

class BaseLLM(object):
    def __init__(self):
        pass

    def chat(self, prompt: str, chat_history: list):
        pass


class Qwen(BaseLLM):
    def __init__(self):
        super().__init__()
        self.api_key = os.environ.get('DASHSCOPE_API_KEY')
        self.model_name = os.environ.get('MODEL_NAME')
        self.client = dashscope.Generation()

    def chat(self, prompt, chat_history):
        try:
            # 构造messages
            messages = [Message(role="system", content=prompt)]
            for his in chat_history:
                messages.append(Message(role="user", content=his[0]))
                messages.append(Message(role="system", content=his[1]))
            messages.append(Message(role="user", content=user_prompt))

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