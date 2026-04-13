#!/usr/bin/env python3
"""萧承角色图生成 - 绝色古风美男 · 妖孽权谋风"""

import os, base64, time, requests

API_KEY = "sk-RMFwp3LflfDDQI13puzsrwOelBdZ1ougBYZCUa950F7Wa1A1"
API_URL = "https://api.yunwu.ai/v1/images/generations"
OUT_DIR = "/Users/cherry/.qclaw/workspace-agent-3ce5e1c4/character_refs"
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

BASE_PROMPT = (
    "Masterpiece, top-tier illustration, hyperrealistic CG rendering, ancient Chinese male, "
    "tall slender build, full-body shot, idol-level face, extremely gorgeous and alluring features, "
    "fine silky hair with strands falling across face, sword eyebrows, peach blossom eyes with soft affectionate gaze, "
    "delicate small nose, seductive thin lips, translucent porcelain white skin with dramatic chiaroscuro lighting, "
    "subtle elegant makeup, silver accessories, black hanfu with intricate silver ornamentation, "
    "high-end composition, high saturation, rich details, ultra sharp, 8K quality"
)

NEGATIVE = (
    "ugly, deformed, blurry, low quality, bad anatomy, extra fingers, "
    "fused fingers, bad proportions, watermark, text, logo, deformed face"
)

# (prompt, filename) 元组列表
ALL_PROMPTS = [
    # 三视图（3张）
    (f"{BASE_PROMPT}, front view full body, standing pose, confident serious expression, palace courtyard background",
     "xiaocheng_front_1.png"),
    (f"{BASE_PROMPT}, side profile full body, three-quarter turn, gazing into distance, misty mountain background",
     "xiaocheng_side_1.png"),
    (f"{BASE_PROMPT}, back view full body, showing hanfu detail and hair flowing, dramatic backlight silhouette",
     "xiaocheng_back_1.png"),

    # 头部特写（3张）
    (f"{BASE_PROMPT}, extreme close-up headshot, sharp focus on face, intense gaze, hair framing face, cinematic lighting, dark moody atmosphere",
     "xiaocheng_face_1.png"),
    (f"{BASE_PROMPT}, head portrait, side profile face, sword eyebrows, delicate features, soft romantic lighting, bokeh background",
     "xiaocheng_face_2.png"),
    (f"{BASE_PROMPT}, face close-up, both eyes detailed, sensual lips, porcelain skin texture visible, dramatic chiaroscuro, studio lighting",
     "xiaocheng_face_3.png"),

    # 表情特写（4张）
    (f"{BASE_PROMPT}, intense cold stare, barely perceptible slight smile, dominance and authority radiating, dark palace interior",
     "xiaocheng_expr_cold.png"),
    (f"{BASE_PROMPT}, melancholic sad expression, slight furrow in brow, soft vulnerable moment, rain and candlelight",
     "xiaocheng_expr_sad.png"),
    (f"{BASE_PROMPT}, seductive smirk, one eyebrow slightly raised, playful yet dangerous energy, wine cup in hand",
     "xiaocheng_expr_smirk.png"),
    (f"{BASE_PROMPT}, eyes filled with suppressed emotion, lips slightly parted, deeply moved yet restrained, cherry blossoms falling",
     "xiaocheng_expr_emotion.png"),

    # 不同氛围/场景（5张）
    (f"{BASE_PROMPT}, standing in heavy rain, soaked black hanfu clinging to body, wind and storm atmosphere, epic scale",
     "xiaocheng_scene_rain.png"),
    (f"{BASE_PROMPT}, seated on ornate chair, one leg crossed, casual yet commanding posture, luxury study interior, candlelight",
     "xiaocheng_scene_study.png"),
    (f"{BASE_PROMPT}, by moonlit window, moonlight casting silver glow on face, contemplative expression, silk curtains blowing",
     "xiaocheng_scene_moon.png"),
    (f"{BASE_PROMPT}, walking through flower garden, petals swirling, spring scenery, softer warmer mood, ethereal beauty",
     "xiaocheng_scene_garden.png"),
    (f"{BASE_PROMPT}, on ancient battlefield ruins, smoke and mist, battle-worn black armor over hanfu, battle-scarred yet beautiful, epic",
     "xiaocheng_scene_battle.png"),

    # 服装/配饰细节（4张）
    (f"{BASE_PROMPT}, full body, silver crown headdress detail, intricate silver hairpin, elegant headwear, close-up on accessories",
     "xiaocheng_outfit_1.png"),
    (f"{BASE_PROMPT}, upper body close-up, silver necklaces and pendants, silver belt detail, embroidered black sleeve, fine craftsmanship visible",
     "xiaocheng_outfit_2.png"),
    (f"{BASE_PROMPT}, full body, different black hanfu variant with silver embroidery pattern, wide sleeve style, standing in grand hall",
     "xiaocheng_outfit_3.png"),
    (f"{BASE_PROMPT}, full body, black outer robe with silver inner layer, layered hanfu, wind blowing outer garment, dramatic silhouette",
     "xiaocheng_outfit_4.png"),
]

def generate(prompt, idx, total, filename):
    print(f"[{idx}/{total}] 生成: {filename}")
    for attempt in range(3):
        try:
            resp = requests.post(API_URL, headers=HEADERS, json={
                "prompt": prompt,
                "negative_prompt": NEGATIVE,
                "model": "flux-schnell",
                "response_format": "b64_json",
                "timeout": 120,
            }, timeout=130)
            data = resp.json()
            if "data" in data and data["data"]:
                b64 = data["data"][0]["b64_json"]
                img_data = base64.b64decode(b64)
                path = os.path.join(OUT_DIR, filename)
                with open(path, "wb") as f:
                    f.write(img_data)
                size = os.path.getsize(path)
                print(f"  ✅ {filename} ({size//1024} KB)")
                return True
            elif "error" in data:
                print(f"  ⚠️ API错误: {data['error']}")
            else:
                print(f"  ⚠️ 未知响应: {str(data)[:200]}")
        except Exception as e:
            print(f"  ❌ 异常: {e}")
        time.sleep(3)
    print(f"  ❌ 跳过 {filename}")
    return False

def main():
    total = len(ALL_PROMPTS)
    print(f"萧承 · 绝色古风美男，共 {total} 张图")
    print("=" * 50)
    success, fail = 0, 0
    for i, item in enumerate(ALL_PROMPTS, 1):
        prompt, filename = item
        if generate(prompt, i, total, filename):
            success += 1
        else:
            fail += 1
        time.sleep(1)
    print(f"\n✅ 完成！成功 {success} 张，失败 {fail} 张")

if __name__ == "__main__":
    main()
