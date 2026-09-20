#!/usr/bin/env python3
"""任务一自动校验：检查产出结构是否完整。通过输出 0，失败输出 1 并列出问题。"""
import json
import os
import sys

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

def fail(msgs, m):
    msgs.append("  ✗ " + m)

def main():
    msgs: list[str] = []
    # data/
    data = "data"
    if not os.path.isdir(data):
        fail(msgs, "缺少 data/ 目录")
    else:
        n = sum(1 for f in os.listdir(data) if os.path.splitext(f)[1].lower() in IMAGE_EXTS)
        if n != 5:
            fail(msgs, f"data/ 应有 5 张图片，实际 {n} 张")

    # output/
    out = "output"
    missing = [f"vis_{i}.jpg" for i in range(1, 6)
               if not os.path.isfile(os.path.join(out, f"vis_{i}.jpg"))] if os.path.isdir(out) else [f"vis_{i}.jpg" for i in range(1, 6)]
    if missing:
        fail(msgs, "output/ 缺少可视化结果: " + ", ".join(missing))

    # results.json
    rj = "results.json"
    if not os.path.isfile(rj):
        fail(msgs, "缺少 results.json")
    else:
        try:
            r = json.load(open(rj, encoding="utf-8"))
            if not isinstance(r, dict) or "images" not in r or not isinstance(r["images"], list):
                fail(msgs, "results.json 顶层应为 {\"images\": [...]}（见 results.example.json）")
            else:
                for i, item in enumerate(r["images"]):
                    if "file" not in item or "detections" not in item:
                        fail(msgs, f"results.json images[{i}] 缺少 file/detections 字段")
                files = [it.get("file") for it in r["images"]]
                if len(set(files)) != len(files):
                    fail(msgs, "results.json 中图片 file 重复")
        except json.JSONDecodeError as e:
            fail(msgs, f"results.json 不是合法 JSON: {e}")

    # notes.md
    notes = "notes.md"
    if not os.path.isfile(notes):
        fail(msgs, "缺少 notes.md")
    else:
        body = open(notes, encoding="utf-8").read().strip()
        if len(body) < 100:
            fail(msgs, f"notes.md 内容过少（{len(body)} 字符），至少要记录你的尝试过程")

    if msgs:
        print("自动校验未通过，共 %d 个问题：" % len(msgs))
        print("\n".join(msgs))
        sys.exit(1)
    print("✓ 自动校验通过！请在验收日前准备现场演示与追问。")

if __name__ == "__main__":
    main()
