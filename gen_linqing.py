#!/usr/bin/env python3
"""林清角色图生成 - 批量"""
import subprocess
import json
import time
import os
import base64

API_KEY = "sk-RMFwp3LflfDDQI13puzsrwOelBdZ1ougBYZCUa950F7Wa1A1"
BASE_URL = "https://api.yunwu.ai/v1/images/generations"

OUT_DIR = "/Users/cherry/.qclaw/workspace-agent-3ce5e1c4/character_refs/gen"
os.makedirs(OUT_DIR, exist_ok=True)

def gen_image(prompt, filename, retry=3):
    for attempt in range(retry):
        r = subprocess.run([
            "curl", "-s", "-X", "POST", BASE_URL,
            "-H", f"Authorization: Bearer {API_KEY}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({
                "model": "flux-schnell",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024"
            })
        ], capture_output=True, text=True)

        try:
            resp = json.loads(r.stdout)
        except:
            print(f"  JSON解析失败: {r.stdout[:200]}")
            time.sleep(2)
            continue

        if "data" in resp and resp["data"]:
            item = resp["data"][0]
            if "url" in item:
                subprocess.run(["curl", "-s", "-o", f"{OUT_DIR}/{filename}", item["url"]], capture_output=True)
                print(f"  ✅ {filename} (from url)")
                return True
            elif "b64_json" in item:
                img_data = base64.b64decode(item["b64_json"])
                with open(f"{OUT_DIR}/{filename}", "wb") as f:
                    f.write(img_data)
                print(f"  ✅ {filename} (from b64)")
                return True
        print(f"  ❌ {filename} (attempt {attempt+1})")
        time.sleep(2)
    return False

# 林清核心描述（基于linqing_C.png）
BASE_DESC = (
    "A beautiful young Chinese woman, 20s, slender and delicate figure, "
    "fair porcelain skin, clear bright eyes, elegant ancient Chinese hanfu attire, "
    "flowing robes, full body shot, high quality illustration, "
    "Chinese ink painting style, character design for novel, detailed face, soft lighting"
)

tasks = []

# 1. 全身侧面图（多角度）
tasks.append((f"{BASE_DESC}, side profile facing left, standing, wind gently blowing hair, serene expression", "linqing_side_1.png"))
tasks.append((f"{BASE_DESC}, side profile facing right, standing, hands behind back, confident elegant pose", "linqing_side_2.png"))
tasks.append((f"{BASE_DESC}, three-quarter view, full body standing, gentle breeze, graceful posture", "linqing_side_3.png"))

# 2. 表情图 - 喜
tasks.append((f"{BASE_DESC}, happy bright smile, eyes full of joy, full body standing, warm gentle smile", "linqing_happy_1.png"))
tasks.append((f"{BASE_DESC}, joyful laughter, eyes squinted with happiness, dynamic lively pose", "linqing_happy_2.png"))
tasks.append((f"{BASE_DESC}, tender gentle smile, soft expression, full body, blooming flowers background", "linqing_happy_3.png"))

# 3. 表情图 - 怒
tasks.append((f"{BASE_DESC}, angry expression, sharp intense eyes, furrowed brows, full body standing", "linqing_angry_1.png"))
tasks.append((f"{BASE_DESC}, cold icy stare, fury in eyes, dark moody atmosphere", "linqing_angry_2.png"))
tasks.append((f"{BASE_DESC}, furious righteous anger, powerful stance, dramatic lighting", "linqing_angry_3.png"))

# 4. 表情图 - 哀
tasks.append((f"{BASE_DESC}, sad melancholic expression, teary eyes, gazing into distance, full body", "linqing_sad_1.png"))
tasks.append((f"{BASE_DESC}, sorrowful, tears on cheek, emotional, dim lighting", "linqing_sad_2.png"))
tasks.append((f"{BASE_DESC}, lonely desolate mood, looking down, autumn leaves falling, poetic", "linqing_sad_3.png"))

# 5. 表情图 - 乐
tasks.append((f"{BASE_DESC}, cheerful carefree, playful expression, lighthearted, spring scenery background", "linqing_joy_1.png"))
tasks.append((f"{BASE_DESC}, surprised amazed expression, wide eyes, hand on cheek, dramatic moment", "linqing_joy_2.png"))
tasks.append((f"{BASE_DESC}, peaceful serene expression, eyes gently closed, zen atmosphere", "linqing_joy_3.png"))

# 6. 不同服饰
tasks.append((f"{BASE_DESC}, wearing elegant flowing hanfu, palace style, ornate embroidery, full body standing", "linqing_outfit_1.png"))
tasks.append((f"{BASE_DESC}, wearing tactical outdoor jacket, modern ancient fusion, practical warrior outfit", "linqing_outfit_2.png"))
tasks.append((f"{BASE_DESC}, wearing simple servant girl hanfu, plain fabric, humble and graceful", "linqing_outfit_3.png"))
tasks.append((f"{BASE_DESC}, wearing dark assassin outfit, black tight hanfu, hidden weapons, action pose", "linqing_outfit_4.png"))
tasks.append((f"{BASE_DESC}, wearing elegant qipao, traditional Chinese dress, graceful pose", "linqing_outfit_5.png"))
tasks.append((f"{BASE_DESC}, wearing casual simple robe, reading or holding a book, scholar style", "linqing_outfit_6.png"))

print(f"共 {len(tasks)} 张图，开始生成...")
for i, (prompt, filename) in enumerate(tasks):
    print(f"\n[{i+1}/{len(tasks)}] 生成: {filename}")
    success = gen_image(prompt, filename)
    if success:
        time.sleep(2)  # 避免限速

print("\n✅ 全部完成！")
