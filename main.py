import time
from input import initial_input
from prompt import gen_prompt, user_prompt
from llm_provider import Qwen
from dotenv import load_dotenv

from tools import tools_map

load_dotenv()

llm = Qwen()


def parse_response(response):
    try:
        thoughts = response.get("thoughts")
        observation = thoughts.get("observation")
        plan = thoughts.get("plan")
        reasoning = thoughts.get("reasoning")
        revision = thoughts.get("revision")
        prompt = f"plan: {plan}\nreasoning: {reasoning}\nobservation: {observation}\nrevision: {revision}"
        return prompt
    except Exception as e:
        print("parse_response error:{}".format(e))
        return "".format(e)


def agent_execute(query, max_request_time):
    cur_request_time = 0
    # 历史对话
    chat_history = []
    # agent的自我反思
    agent_reflection = ""
    while cur_request_time < max_request_time:
        cur_request_time += 1
        # 生成prompt
        prompt = gen_prompt(query, revision=agent_reflection)
        star_time = time.time()
        # call llm
        response = llm.chat(prompt=prompt, chat_history=chat_history)
        print(response)
        end_time = time.time()
        if not response or not isinstance(response, dict):
            print("call llm exception, response is :{}".format(response))
            continue

        action_info = response.get("action")
        action_name = action_info.get("name")
        action_args = action_info.get("args")
        print("当前action_name:{}||action_参数:{}".format(action_name, action_args))

        thoughts = response.get("thoughts")
        reasoning = thoughts.get("reasoning")
        plan = thoughts.get("plan")
        observation = thoughts.get("observation")
        # criticism = thoughts.get("criticism")
        print("reasoning:{}".format(reasoning))
        print("plan:{}".format(plan))
        print("observation:{}".format(observation))
        # print("criticism:{}".format(criticism))

        try:
            func = tools_map.get(action_name)
            call_function_result = func(**action_args)
        except Exception as e:
            print("调用工具异常:{}".format(e))
            call_function_result = "{}".format(e)

        agent_reflection = agent_reflection + "\n: observation:{}\n execute action result: {}".format(observation,
                                                                                                      call_function_result)

        chat_history.append([user_prompt, observation])


def main():
    # 支持多轮输入，需要循环调用llm
    # 设置最大请求次数
    # max_request_time = 3
    # while True:
    query = initial_input("请输入您的目标: ")
    if query == "exit":
        return
    agent_execute(query, max_request_time=3)


if __name__ == '__main__':
    # 探测106.14.218.41的22，80，443端口是否开放，你没有root权限
    # '检查106.14.218.41的22,80,443端口是否开放，你没有root权限，我需要你把任务的执行情况写入文件'
    main()
