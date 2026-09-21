#!/usr/bin/env python3
"""task0 热身题自动判题：对每个 problems/pN-*，运行 solutions/pN.py，
逐个测试点比对 stdout（按行去除行尾空白后比较）。
通过输出 0；存在未通过或未提交输出 1。"""
import glob
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def norm(text: str) -> list[str]:
    return [line.rstrip() for line in text.splitlines()]

def main() -> int:
    problem_dirs = sorted(glob.glob(os.path.join(ROOT, "problems", "p*-*")))
    if not problem_dirs:
        print("未找到题目目录")
        return 1
    any_fail = False
    print(f"{'题目':<22}{'结果':<10}说明")
    print("-" * 60)
    for prob in problem_dirs:
        name = os.path.basename(prob)
        pid = name.split("-", 1)[0]
        sol = os.path.join(ROOT, "solutions", f"{pid}.py")
        if not os.path.isfile(sol):
            print(f"{name:<22}{'未提交':<10}缺少 solutions/{pid}.py")
            any_fail = True
            continue
        cases = sorted(glob.glob(os.path.join(prob, "tests", "*.in")))
        ok = 0
        detail = ""
        for cin in cases:
            ans_file = cin[:-3] + ".ans"
            with open(cin, encoding="utf-8") as f:
                stdin_data = f.read()
            with open(ans_file, encoding="utf-8") as f:
                expect = norm(f.read())
            try:
                r = subprocess.run([sys.executable, sol], input=stdin_data,
                                   capture_output=True, text=True, timeout=10)
            except subprocess.TimeoutExpired:
                detail = f"{os.path.basename(cin)} 超时"
                break
            got = norm(r.stdout)
            if got == expect:
                ok += 1
            else:
                detail = f"{os.path.basename(cin)} 输出不符"
                break
        if ok == len(cases) and not detail:
            print(f"{name:<22}{'通过':<10}{len(cases)}/{len(cases)} 测试点")
        else:
            print(f"{name:<22}{'未通过':<10}{ok}/{len(cases)} 测试点；{detail}")
            any_fail = True
    print("-" * 60)
    print("全部通过" if not any_fail else "存在未通过题目")
    return 0 if not any_fail else 1

if __name__ == "__main__":
    sys.exit(main())
