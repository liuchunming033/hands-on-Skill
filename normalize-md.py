"""
Markdown 列表预处理：在列表项前插入空行，确保 pandoc 正确解析 <ul>/<ol>。
用法: python3 normalize-md.py < input.md | pandoc ...
"""
import sys
import re

text = sys.stdin.read()
lines = text.split('\n')
result = []
in_code_block = False

for line in lines:
    stripped = line.strip()

    # 跟踪代码块状态
    if stripped.startswith('```'):
        in_code_block = not in_code_block

    # 判断当前行是否为列表项（- item、* item、1. item 等）
    is_list_item = bool(re.match(r'^(- |\* |\d+\. )', stripped))

    # 不在代码块内 + 是列表项 + 前一行非空且非列表项 → 插入空行
    if not in_code_block and is_list_item and result:
        prev = result[-1].strip()
        prev_is_list = bool(re.match(r'^(- |\* |\d+\. )', prev))
        if prev != '' and not prev_is_list:
            result.append('')

    result.append(line)

sys.stdout.write('\n'.join(result))
