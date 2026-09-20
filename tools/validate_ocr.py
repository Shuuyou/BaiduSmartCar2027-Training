#!/usr/bin/env python3
"""任务二自动校验。"""
import json
import os
import sys

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

def main():
    msgs: list[str] = []
    data = "data"
    if not os.path.isdir(data):
        msgs.append("  ✗ 缺少 data/ 目录")
    else:
        n = sum(1 for f in os.listdir(data) if os.path.splitext(f)[1].lower() in IMAGE_EXTS)
        if n != 10:
            msgs.append(f"  ✗ data/ 应有 10 张图片，实际 {n} 张")

    rj = "results.json"
    if not os.path.isfile(rj):
        msgs.append("  ✗ 缺少 results.json")
    else:
        try:
            r = json.load(open(rj, encoding="utf-8"))
            if not isinstance(r, dict) or "images" not in r:
                msgs.append("  ✗ results.json 顶层应为 {\"images\": [...]}")
            else:
                for i, it in enumerate(r["images"]):
                    if "file" not in it or "texts" not in it:
                        msgs.append(f"  ✗ images[{i}] 缺少 file/texts 字段")
            if not isinstance(r.get("postprocess"), dict) or not r["postprocess"].get("description"):
                msgs.append("  ✗ 缺少 postprocess.description：请说明你的后处理实验")
        except json.JSONDecodeError as e:
            msgs.append(f"  ✗ results.json 不是合法 JSON: {e}")

    notes = "notes.md"
    if not os.path.isfile(notes):
        msgs.append("  ✗ 缺少 notes.md")
    elif len(open(notes, encoding="utf-8").read().strip()) < 150:
        msgs.append("  ✗ notes.md 内容过少，需记录实验前后对比")

    if msgs:
        print("自动校验未通过，共 %d 个问题：" % len(msgs))
        print("\n".join(msgs))
        sys.exit(1)
    print("✓ 自动校验通过！验收日将现场换 3 张新图测试鲁棒性。")

if __name__ == "__main__":
    main()
