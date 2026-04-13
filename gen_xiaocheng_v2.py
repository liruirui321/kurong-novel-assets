#!/usr/bin/env python3
"""萧承 · 以 scene_rain 脸为原型，生成表情/场景/服饰变体"""

import os, base64, time, requests

API_KEY = "sk-RMFwp3LflfDDQI13puzsrwOelBdZ1ougBYZCUa950F7Wa1A1"
API_URL = "https://api.yunwu.ai/v1/images/generations"
OUT_DIR = "/Users/cherry/.qclaw/workspace-agent-3ce5e1c4/character_refs"
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# 以 scene_rain 为参考脸，截取核心描述
# 基于 rain 图的特征：暴雨中美男、湿身黑汉服、白银配饰、绝美妖孽脸
FACE_PROMPT = (
    "same face as the reference image, identical facial features, same person, "
    "ancient Chinese male, idol-level gorgeous face, sword eyebrows, peach blossom eyes, "
    "delicate nose, seductive thin lips, translucent porcelain white skin, "
    "fine silky hair with wet strands on face, subtle elegant makeup, "
    "black wet hanfu clinging to body, silver accessories"
)

NEGATIVE = (
    "ugly, deformed, blurry, low quality, bad anatomy, extra fingers, "
    "fused fingers, bad proportions, watermark, text, logo, different face, "
    "dissimilar face, watermark on face, extra limbs"
)

# 加载参考图 base64
REF_PATH = os.path.join(OUT_DIR, "xiaocheng_scene_rain.png")
with open(REF_PATH, "rb") as f:
    ref_b64 = base64.b64encode(f.read()).decode()
ref_url = f"data:image/png;base64,{ref_b64}"

def generate_with_ref(prompt, idx, total, filename):
    print(f"[{idx}/{total}] 生成: {filename}")
    for attempt in range(3):
        try:
            resp = requests.post(API_URL, headers=HEADERS, json={
                "prompt": prompt,
                "negative_prompt": NEGATIVE,
                "model": "flux-schnell",
                "response_format": "b64_json",
                "strength": 0.35,    # 保持脸不变，只改场景/表情/服饰
                "init_image": ref_url,
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
                print(f"  ⚠️ 未知响应: {str(data)[:300]}")
        except Exception as e:
            print(f"  ❌ 异常: {e}")
        time.sleep(3)
    print(f"  ❌ 跳过 {filename}")
    return False

# 全部用参考脸生成变体
TASKS = [
    # 三视图变体
    (f"{FACE_PROMPT}, front view full body, standing pose, confident serious expression, palace grand hall, golden lanterns, cinematic lighting",
     "xiaocheng_v2_front.png"),
    (f"{FACE_PROMPT}, side profile full body, three-quarter turn, gazing into distance, misty mountain valley, dramatic natural lighting",
     "xiaocheng_v2_side.png"),
    (f"{FACE_PROMPT}, back view, showing black wet hanfu and long flowing hair, dramatic backlight silhouette against storm clouds",
     "xiaocheng_v2_back.png"),

    # 表情特写（保持同脸）
    (f"{FACE_PROMPT}, intense cold authoritative stare, barely perceptible smirk, dominance radiating, dark palace throne room, candlelight",
     "xiaocheng_v2_expr_cold.png"),
    (f"{FACE_PROMPT}, melancholic deeply moved expression, slightly furrowed brow, eyes glistening with tears restrained, rain outside window, intimate close-up",
     "xiaocheng_v2_expr_sad.png"),
    (f"{FACE_PROMPT}, seductive playful smirk, one eyebrow raised, dangerous playful energy, holding wine cup, luxury bedroom, soft bokeh",
     "xiaocheng_v2_expr_smirk.png"),
    (f"{FACE_PROMPT}, tender warm gentle smile, genuine happiness in eyes, cherry blossom petals falling around, spring scenery, soft golden light",
     "xiaocheng_v2_expr_joy.png"),
    (f"{FACE_PROMPT}, fierce angry expression, burning cold fury in eyes, dark aura, imposing overwhelming pressure, dramatic dark clouds lightning",
     "xiaocheng_v2_expr_angry.png"),
    (f"{FACE_PROMPT}, confused troubled expression, deep in thought, slight frown, dimly lit study, scattered scrolls, night",
     "xiaocheng_v2_expr_thoughtful.png"),

    # 场景（保持同脸）
    (f"{FACE_PROMPT}, by moonlit window at night, silver moonlight casting on face, contemplative gaze, silk curtains in gentle breeze, romantic atmosphere",
     "xiaocheng_v2_scene_moon.png"),
    (f"{FACE_PROMPT}, seated at ornate desk, one hand holding brush writing calligraphy, other hand supporting chin, scholar's study, candlelight, ink stones",
     "xiaocheng_v2_scene_study.png"),
    (f"{FACE_PROMPT}, walking through flower garden in spring, petals swirling around, soft breeze, warm sunshine, ethereal dreamlike quality",
     "xiaocheng_v2_scene_garden.png"),
    (f"{FACE_PROMPT}, on ancient battlefield ruins after battle, smoke and mist, battle-worn black armor over hanfu, blood on face yet still beautiful, epic scale, cinematic",
     "xiaocheng_v2_scene_battle.png"),
    (f"{FACE_PROMPT}, in grand throne room, seated on dragon throne, cold dignified expression, ministers kneeling below (blurred), golden palace interior, epic imposing",
     "xiaocheng_v2_scene_throne.png"),
    (f"{FACE_PROMPT}, in private courtyard at night, alone under wisteria, lantern glow, contemplative sitting on stone bench, autumn leaves falling, melancholic beauty",
     "xiaocheng_v2_scene_courtyard.png"),

    # 服装变体（保持同脸）
    (f"{FACE_PROMPT}, full body, different outfit: white silk hanfu with silver embroidery, elegant refined look, pure white sash, soft angelic white theme, standing in snow",
     "xiaocheng_v2_outfit_white.png"),
    (f"{FACE_PROMPT}, full body, outfit variation: crimson red outer robe over black hanfu, dramatic contrasting colors, luxurious fabric, grand hall background, dramatic lighting",
     "xiaocheng_v2_outfit_crimson.png"),
    (f"{FACE_PROMPT}, full body, outfit variation: dark navy blue hanfu with silver constellation pattern, mysterious celestial theme, starlit sky background, ethereal beauty",
     "xiaocheng_v2_outfit_navy.png"),
    (f"{FACE_PROMPT}, close-up upper body, silver crown headdress, intricate silver hairpins, silver necklaces and pendants, close-up on luxurious silver accessories",
     "xiaocheng_v2_accessories.png"),
]

def main():
    total = len(TASKS)
    print(f"萧承 v2 · 以 scene_rain 脸为原型，共 {total} 张图")
    print("参考图: xiaocheng_scene_rain.png")
    print("=" * 50)
    success, fail = 0, 0
    for i, (prompt, filename) in enumerate(TASKS, 1):
        if generate_with_ref(prompt, i, total, filename):
            success += 1
        else:
            fail += 1
        time.sleep(1)
    print(f"\n✅ 完成！成功 {success} 张，失败 {fail} 张")

if __name__ == "__main__":
    main()
