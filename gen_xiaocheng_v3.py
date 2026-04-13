#!/usr/bin/env python3
"""萧承 v3 · 以 scene_rain 脸为原型，高保真生成
strength=0.85 只微调表情/场景/服饰，最大限度保持同脸"""

import os, base64, time, requests

API_KEY = "sk-RMFwp3LflfDDQI13puzsrwOelBdZ1ougBYZCUa950F7Wa1A1"
API_URL = "https://api.yunwu.ai/v1/images/generations"
OUT_DIR = "/Users/cherry/.qclaw/workspace-agent-3ce5e1c4/character_refs"
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

NEGATIVE = (
    "ugly, deformed, blurry, low quality, bad anatomy, extra fingers, "
    "fused fingers, bad proportions, watermark, text, logo, different face, "
    "dissimilar face, extra limbs, bad hands, ugly face"
)

# 加载参考图
REF_PATH = os.path.join(OUT_DIR, "xiaocheng_scene_rain.png")
with open(REF_PATH, "rb") as f:
    ref_b64 = base64.b64encode(f.read()).decode()
ref_url = f"data:image/png;base64,{ref_b64}"

def gen(prompt, idx, total, filename, strength=0.85):
    print(f"[{idx}/{total}] {filename}")
    for attempt in range(3):
        try:
            resp = requests.post(API_URL, headers=HEADERS, json={
                "prompt": prompt,
                "negative_prompt": NEGATIVE,
                "model": "flux-schnell",
                "response_format": "b64_json",
                "strength": strength,
                "init_image": ref_url,
                "timeout": 120,
            }, timeout=130)
            data = resp.json()
            if "data" in data and data["data"]:
                img_data = base64.b64decode(data["data"][0]["b64_json"])
                path = os.path.join(OUT_DIR, filename)
                with open(path, "wb") as f:
                    f.write(img_data)
                size = os.path.getsize(path)
                print(f"  ✅ {filename} ({size//1024} KB)")
                return True
            elif "error" in data:
                print(f"  ⚠️ {data['error']}")
            else:
                print(f"  ⚠️ 未知: {str(data)[:200]}")
        except Exception as e:
            print(f"  ❌ {e}")
        time.sleep(3)
    print(f"  ❌ 跳过 {filename}")
    return False

def main():
    # 三视图侧面（3张）
    views = [
        ("full body, side profile facing left, three-quarter turn, gazing into distance, palace corridor, soft lantern light",
         "xiaocheng_v3_side_left.png"),
        ("full body, side profile facing right, slight tilt of head, contemplative expression, misty garden background, ethereal morning mist",
         "xiaocheng_v3_side_right.png"),
        ("full body, three-quarter rear side view, showing black hanfu back detail and long flowing hair, dramatic backlight, clouds parting",
         "xiaocheng_v3_side_back.png"),
    ]

    # 表情各2张（喜/怒/哀/乐）
    expressions = [
        # 喜
        ("gentle happy smile, warm tender eyes, soft joy expression, cherry blossom petals floating, spring courtyard, golden hour light",
         "xiaocheng_v3_happy_1.png"),
        ("subtle content smile, peaceful relaxed expression, slight upward curve of lips, peaceful morning, warm sunlight through window",
         "xiaocheng_v3_happy_2.png"),
        # 怒
        ("intense cold fury, burning dangerous eyes, menacing expression, dark palace interior, dramatic red candlelight, overwhelming pressure",
         "xiaocheng_v3_angry_1.png"),
        ("cold dismissive angry glare, barely contained rage, slight sneer, storm approaching outside window, dramatic shadows",
         "xiaocheng_v3_angry_2.png"),
        # 哀
        ("deeply sad melancholic expression, glistening eyes with restrained tears, slight furrow in brow, rain tapping on window, intimate close-up",
         "xiaocheng_v3_sad_1.png"),
        ("profound grief expression, hollow empty stare, lips slightly parted in quiet pain, night scene, only moonlight illuminating face",
         "xiaocheng_v3_sad_2.png"),
        # 乐
        ("genuine bright joyful laughter, eyes crinkling with happiness, carefree happy expression, flower garden in full bloom, butterflies around",
         "xiaocheng_v3_joy_1.png"),
        ("mischievous playful delighted smirk, eyes sparkling with fun, teasing inviting expression, summer festival lanterns, lively atmosphere",
         "xiaocheng_v3_joy_2.png"),
    ]

    # 服饰各2张
    outfits = [
        ("full body, pristine white silk hanfu with silver embroidery, ethereal pure white theme, standing in snow garden, delicate ice crystals, serene beauty",
         "xiaocheng_v3_outfit_white_1.png"),
        ("full body, flowing white robe with subtle silver cloud pattern, white sash, moonlit night backdrop, mist swirling around feet, celestial immortallike",
         "xiaocheng_v3_outfit_white_2.png"),
        ("full body, deep crimson red hanfu outer robe over black inner layer, dramatic contrasting outfit, grand hall throne room, golden light, imperial grandeur",
         "xiaocheng_v3_outfit_red_1.png"),
        ("full body, rich wine-red silk hanfu with black trim, crimson sash, holding red lantern, night festival, warm dramatic lighting",
         "xiaocheng_v3_outfit_red_2.png"),
        ("full body, dark navy blue hanfu with silver constellation embroidery, mysterious celestial theme, starry night sky, comet visible, ethereal cosmic beauty",
         "xiaocheng_v3_outfit_navy_1.png"),
        ("full body, midnight blue and silver layered hanfu, wind blowing outer garment dramatically, storm clouds above, lightning in distance, epic powerful presence",
         "xiaocheng_v3_outfit_navy_2.png"),
        ("full body, black and gold imperial hanfu, dragon pattern embroidery, majestic dignified outfit, throne room with ministers blurred behind, supreme authority",
         "xiaocheng_v3_outfit_gold_1.png"),
        ("full body, elegant purple violet silk hanfu with silver lotus embroidery, refined aristocratic aesthetic, private garden at dusk, refined beauty",
         "xiaocheng_v3_outfit_purple_1.png"),
    ]

    all_tasks = views + expressions + outfits
    total = len(all_tasks)
    print(f"萧承 v3 · 高保真（strength=0.85）共 {total} 张")
    print("=" * 50)
    success, fail = 0, 0
    for i, (prompt, filename) in enumerate(all_tasks, 1):
        if gen(prompt, i, total, filename, strength=0.85):
            success += 1
        else:
            fail += 1
        time.sleep(1)
    print(f"\n✅ 完成！成功 {success} 张，失败 {fail} 张")

if __name__ == "__main__":
    main()
