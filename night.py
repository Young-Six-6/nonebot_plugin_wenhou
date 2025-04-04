from nonebot.plugin import PluginMetadata
from nonebot import on_message
from nonebot.rule import Rule
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11 import MessageEvent
import re

__plugin_meta__ = PluginMetadata(
    name="精准晚安插件",
    description="严格匹配晚/晚安问候",
    usage="发送：晚 | 晚安 | 晚上好（允许空格和常见标点）",
)

def check_zao(msg: str) -> bool:
    """严格匹配规则：
    1. 去除首尾空格和标点
    2. 匹配纯问候
    3. 排除命令
    """
    # 去除首尾空格和常见
    cleaned = re.sub(r"^[\s\u3000!?。！？,\.]+|[\s\u3000!?。！？,\.]+$", "", msg)
    
    # 检查是否以符号开头
    if re.match(r"^[/!！]", cleaned):
        return False
    
    # 精确匹配问候形式
    return cleaned in {"晚", "晚安", "晚啊","睡觉去了","去睡觉了"}

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
    await zao_matcher.send("晚安，我亲爱的群友们,晚安，好梦，我们明天见！")