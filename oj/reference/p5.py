a = list(map(int, input().split()))
cnt = {"low": 0, "ok": 0, "full": 0}
for i, x in enumerate(a, 1):
    lv = "low" if x < 30 else ("full" if x > 70 else "ok")
    cnt[lv] += 1
    print(f"tower_{i}: {lv}")
print("low={} ok={} full={}".format(cnt["low"], cnt["ok"], cnt["full"]))
