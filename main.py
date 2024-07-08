import json
import time
from input import initial_input
from prompt import gen_split_task_prompt, gen_action_task_prompt
from llm_provider import QwenSplitTask, QwenAction
from dotenv import load_dotenv

from tools import tools_map

load_dotenv()

llm_split_task = QwenSplitTask()
llm_action_task = QwenAction()


def split_task(task) -> json:
    """
    :param task:
    :return: {'task': '检查106.14.218.41的22,80,443端口是否开放，结果写入data/task/task.json',
              'subtask_list': [{'task_number': '1', 'description': '扫描106.14.218.41的22,80,443端口状态'},
              {'task_number': '2', 'description': '将扫描结果写入data/task/task.json'}]}
    """
    prompt = gen_split_task_prompt(task)
    return llm_split_task.chat(prompt=prompt)


def agent_execute(task_list, max_request_time):
    task_num = len(task_list.get("subtask_list"))
    cur_request_time = 0
    # 历史对话，存储上次执行的任务id，调用的工具名称，工具的参数，工具的执行结果
    chat_history = {}
    task_id = "0"
    action_name = ""
    action_args = {}
    action_result = ""
    # agent的自我反思
    agent_reflection = ""
    while cur_request_time < max_request_time:
        cur_request_time += 1
        # 生成prompt
        prompt = gen_action_task_prompt(task_list, task_id, action_name, action_args, action_result)
        star_time = time.time()
        # call llm
        # TODO:增加chat history
        response = llm_action_task.chat(prompt=prompt)
        # print(response)
        # action = response.get("action")
        # print(action)
        task_id = response.get("action").get("action_subtask_id")
        task_description = response.get("action").get("subtask_description")
        print("准备执行子任务{}:{}".format(task_id, task_description))
        reasoning = response.get("action").get("reasoning")
        print("任务分析:{}".format(reasoning))
        action_name = response.get("action").get("tool_name")
        action_args = response.get("action").get("tool_args")
        print("准备调用工具:{}".format(action_name) + "\t" + "参数:{}".format(action_args))
        # action_result = response.get("action").get("tool_output")
        # 调用工具
        try:
            # TODO:子任务不需要调用任何工具时的处理逻辑
            if action_name == '':
                print("子任务{}不需要调用任何工具".format(task_id))
                break
            else:
                func = tools_map.get(action_name)
                action_result = func(**action_args)
                print("工具执行结果:{}".format(action_result))
                # TODO：把子任务id，调用的工具，工具的参数，工具的执行结果存入向量数据库，作为long memory？
        except Exception as e:
            print("调用工具异常:{}".format(e))
            action_result = "{}".format(e)

        chat_history[int(task_id)] = {
            "task_id:{}".format(task_id): {
                "调用工具名": action_name,
                "参数": action_args,
                "工具输出结果": action_result
            }
        }
        # 完成任务退出
        if task_id == str(task_num):
            # TODO:执行完最后一个任务后，查询向量数据库，把执行过的所有信息反馈给大模型进行总结
            #
            print("任务执行完成")
            break
        # print(response)
        end_time = time.time()


def main():
    # 支持多轮输入，需要循环调用llm
    # 设置最大请求次数
    max_request_time = 5
    # while True:
    # task = initial_input("请输入您的任务: ")
    # if task == "exit":
    # return
    # task_list = split_task(task)
    task_list = {
        'task': '检查106.14.218.41的22,80,443端口是否开放，扫描127.0.0.1的22,80,443端口状态,没有root权限，把分析后的结果写入task1.txt',
        'subtask_list': [{'task_number': '1', 'description': '扫描106.14.218.41的22,80,443端口状态,没有root权限'},
                         {'task_number': '2', 'description': '扫描127.0.0.1的22,80,443端口状态,没有root权限'},
                         {'task_number': '3',
                          'description': '详细分析任务执行的整个过程以及任务的完成状况，形成一个中文报告，把报告写入文件task1.txt'}]}

    agent_execute(task_list, max_request_time=5)


if __name__ == '__main__':
    # 探测106.14.218.41的22，80，443端口是否开放，你没有root权限
    # '检查106.14.218.41的22,80,443端口是否开放，你没有root权限，我需要你把任务的执行情况写入文件data/task/task.json中'
    main()
