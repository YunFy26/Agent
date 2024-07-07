import json
import os
from typing import Optional
import nmap


def _get_workdir_root():
    workdir_root = os.environ.get('WORKDIR_ROOT', "data/tasks/")
    return workdir_root


WORKDIR_ROOT = _get_workdir_root()


def write_to_file(filename, content):
    filename = os.path.join(WORKDIR_ROOT, filename)
    with open(filename, 'a') as f:
        f.write(content)
    return f"Successfully written to {filename}."


nm = nmap.PortScanner()


def port_scan_syn(ip: Optional[str], port: Optional[str]):
    nm.scan(ip, port, '-Pn -sV -T4 -sS')
    json_data = nm.analyse_nmap_xml_scan()
    scan_result = json_data["scan"]
    return scan_result


def port_scan_conn(ip: Optional[str], port: Optional[str]):
    nm.scan(ip, port, '-Pn -sV -T4 -sT')
    json_data = nm.analyse_nmap_xml_scan()
    scan_result = json_data["scan"]
    return scan_result


def host_discover(ip: Optional[str]):
    nm.scan(ip, '-sP -T4')
    # print("调用了host_discover")
    json_data = nm.analyse_nmap_xml_scan()
    scan_result = json_data["scan"]
    return scan_result


tools_info = [
    {
        "name": "write_to_file",
        "description": "write content to file",
        "args": [
            {
                "name": "filename",
                "type": "string",
                "description": "file name"
            },
            {
                "name": "content",
                "type": "string",
                "description": "append to file content"
            }
        ]
    },
    {
        "name": "port_scan_syn",
        "description": "Use tcp_syn to scan whether the port is open, select this if you have root permissions",
        "args": [
            {
                "name": "ip",
                "type": "Optional[str]",
                "description": "target ip"
            },
            {
                "name": "port",
                "type": "Optional[str]",
                "description": "target port"
            }
        ]
    },
    {
        "name": "port_scan_conn",
        "description": "Use connect() to scan whether the port is open, select this if you do not have root permissions",
        "args": [
            {
                "name": "ip",
                "type": "Optional[str]",
                "description": "target ip"
            },
            {
                "name": "port",
                "type": "Optional[str]",
                "description": "target port"
            }
        ]
    },
    {
        "name": "host_discover",
        "description": "Check whether the host is alive",
        "args": [
            {
                "name": "ip",
                "type": "Optional[str]",
                "description": "target ip"
            }
        ]
    }

]

tools_map = {
    "write_to_file": write_to_file,
    "port_scan_syn": port_scan_syn,
    "port_scan_conn": port_scan_conn,
    "host_discover": host_discover
}


def gen_tools_desc():
    """
    生成工具描述
    """
    tools_desc = []
    for index, tool in enumerate(tools_info):
        args_desc = []
        for info in tool["args"]:
            args_desc.append({
                "name": info["name"],
                "description": info["description"],
                "type": info["type"]
            })
        args_desc = json.dumps(args_desc, ensure_ascii=False)
        tool_desc = f"{index+1}.{tool['name']}:{tool['description']}, args: {args_desc}"
        tools_desc.append(tool_desc)
    tools_prompt = "\n".join(tools_desc)
    # print(tools_prompt)
    return tools_prompt

# gen_tools_desc()

