from nonebot.plugin import PluginMetadata
from nonebot import on_message
from nonebot.rule import Rule
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11 import MessageEvent
import re

__plugin_meta__ = PluginMetadata(
    name="精准早安插件",
    description="严格匹配早/早安/早上好三种问候",
    usage="发送：早 | 早安 | 早上好（允许空格和常见标点）",
)

def check_zao(msg: str) -> bool:
    """严格匹配规则：
    1. 去除首尾空格和标点
    2. 匹配纯「早」「早安」「早上好」
    3. 排除命令格式
    """
    # 去除标点
    cleaned = re.sub(r"^[\s\u3000!?。！？,\.]+|[\s\u3000!?。！？,\.]+$", "", msg)
    
    # 排除特殊符号
    if re.match(r"^[/!！]", cleaned):
        return False
    
    # 收到问候形式触发
    return cleaned in {"早", "早安", "早上好","早早早"}

async def message_checker(event: MessageEvent) -> bool:
    text = event.get_message().extract_plain_text()
    return check_zao(text)

zao_matcher = on_message(
    rule=Rule(message_checker),
    priority=10,
    block=True
)

@zao_matcher.handle()
async def handle_zao():
    await zao_matcher.send("早呀~小机器人祝你早安")