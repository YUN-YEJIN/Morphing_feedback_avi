import os, cv2, json, numpy as np
from pipeline import enhance_landmarks_with_boundary, landmark_mask

# 입력 경로
IMG_PATH = r"C:/Users/NOW/Desktop/morph/image/A.png"
JSON_PATH = r"C:/Users/NOW/Desktop/morph/results/a_mouth_landmarks.json"

# 출력
OUT_DIR = os.path.join(os.path.dirname(__file__), "viz_outputs")
os.makedirs(OUT_DIR, exist_ok=True)

def save_img_unicode(path, img):
    ext = os.path.splitext(path)[1].lower()
    if ext not in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"]:
        ext = ".png"
        path = path + ext
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        print("인코딩 실패:", path)
        return False
    try:
        buf.tofile(path)
        print("저장됨:", path)
        return True
    except Exception as e:
        print("저장 실패:", path, e)
        return False

def load_xy(json_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return np.array([(float(p["x"]), float(p["y"])) for p in data], dtype=np.float32)

print("cwd:", os.getcwd())
print("OUT_DIR:", OUT_DIR)

img = cv2.imread(IMG_PATH)
assert img is not None, f"이미지 못 읽음: {IMG_PATH}"
pts = load_xy(JSON_PATH)

# 원본 포인트
orig = img.copy()
for (x, y) in pts:
    cv2.circle(orig, (int(x), int(y)), 2, (0, 255, 0), -1, lineType=cv2.LINE_AA)

# 경계 보강
enh1, enh2, soft_mask = enhance_landmarks_with_boundary(pts.tolist(), pts.tolist(), img.shape, is_tongue=False)

bound = img.copy()
for (x, y) in enh1:
    cv2.circle(bound, (int(x), int(y)), 2, (0, 0, 255), -1, lineType=cv2.LINE_AA)

# feather 마스크 히트맵
if soft_mask.dtype != np.uint8:
    soft_mask = soft_mask.astype(np.uint8)
mask_viz = cv2.applyColorMap(soft_mask, cv2.COLORMAP_JET)

# 저장
save_img_unicode(os.path.join(OUT_DIR, "시각자료1_원본랜드마크.png"), orig)
save_img_unicode(os.path.join(OUT_DIR, "시각자료1_경계보강후.png"), bound)
save_img_unicode(os.path.join(OUT_DIR, "시각자료1_mask히트맵.png"), mask_viz)
