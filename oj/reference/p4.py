import sys
d = {}
for line in sys.stdin:
    s = line.strip()
    if not s or s.startswith("#"):
        continue
    k, v = s.split("=", 1)
    d[k] = v
for k in sorted(d):
    print(f"{k}: {d[k]}")
