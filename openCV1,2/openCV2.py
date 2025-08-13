import os, cv2, json, numpy as np
from pipeline import enhance_landmarks_with_boundary, calculate_delaunay_triangles

# 경로 편집
IMG_PATH  = r"C:/Users/NOW/Desktop/morph/image/A.png"
JSON_PATH = r"C:/Users/NOW/Desktop/morph/results/A_mouth_landmarks.json"

OUT_DIR = os.path.join(os.path.dirname(__file__), "viz_outputs")
os.makedirs(OUT_DIR, exist_ok=True)

def save_img_unicode(path, img):
    ext = os.path.splitext(path)[1].lower()
    if ext not in [".png",".jpg",".jpeg",".bmp",".tiff",".tif",".webp"]:
        ext = ".png"; path = path + ext
    ok, buf = cv2.imencode(ext, img)
    if not ok: print("인코딩 실패:", path); return False
    try: buf.tofile(path); print("저장됨:", path); return True
    except Exception as e: print("저장 실패:", path, e); return False

def load_xy(p):
    with open(p, encoding="utf-8") as f:
        data = json.load(f)            # [{name,x,y}, ...]
    return np.array([(float(d["x"]), float(d["y"])) for d in data], np.float32)

img = cv2.imread(IMG_PATH); assert img is not None, IMG_PATH
pts = load_xy(JSON_PATH)

# 경계 보강
enh1, enh2, _ = enhance_landmarks_with_boundary(pts.tolist(), pts.tolist(), img.shape, is_tongue=False)
landmarks = np.asarray(enh1, np.float32)

h, w = img.shape[:2]
tris = calculate_delaunay_triangles((0,0,w,h), landmarks.tolist())

# 오버레이
mesh = img.copy()
for (x,y) in landmarks:
    cv2.circle(mesh, (int(x),int(y)), 2, (0,255,0), -1, lineType=cv2.LINE_AA)
for (i,j,k) in tris:
    poly = np.array([landmarks[i], landmarks[j], landmarks[k]], dtype=np.int32)
    cv2.polylines(mesh, [poly], True, (0,200,255), 1, lineType=cv2.LINE_AA)

save_img_unicode(os.path.join(OUT_DIR, "시각자료2_메쉬오버레이.png"), mesh)