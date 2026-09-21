import sys
lines = sys.stdin.read().splitlines()
words = sum(len(l.split()) for l in lines)
chars = sum(len(l) for l in lines)
print(f"lines={len(lines)} words={words} chars={chars}")
