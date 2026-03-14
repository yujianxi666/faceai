import cv2
import mediapipe as mp
import subprocess
import time
import os
import numpy as np

# 关闭所有日志（不刷屏）
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['MEDIAPIPE_DISABLE_GPU'] = '1'
import logging
logging.disable(logging.CRITICAL)

# ====================== 配置 ======================
TARGET_MAC = "MAC地址"
COOLDOWN_TIME = 10
FACE_CHECK_INTERVAL = 1.0
MAX_FACE_SAMPLES = 5
THRESHOLD = 1.2  # 识别率
# ===================================================

# ====================== 模型初始化 ======================
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

# 提取人脸特征
def get_face_keypoints(img):
    try:
        with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as face_mesh:
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = face_mesh.process(rgb)
            if res.multi_face_landmarks:
                pts = []
                for lm in res.multi_face_landmarks[0].landmark:
                    pts.append([lm.x, lm.y, lm.z])
                return np.array(pts)
    except:
        return None

# 加载所有本人人脸库 me1.jpg ~ me5.jpg
my_face_features = []
for i in range(1, MAX_FACE_SAMPLES + 1):
    path = f"me{i}.jpg"
    if os.path.exists(path):
        img = cv2.imread(path)
        feat = get_face_keypoints(img)
        if feat is not None:
            my_face_features.append(feat)
            print(f"✅ 已加载：me{i}.jpg")

if len(my_face_features) == 0:
    print("❌ 请放入至少一张照片 me1.jpg")
    exit()

print(f"\n✅ 已加载 {len(my_face_features)} 张人脸图片")

# ====================== 人脸识别 ======================
def is_me(img):
    try:
        current = get_face_keypoints(img)
        if current is None:
            return False

        # 只要和任意一张样本接近，就判定为本人
        for feat in my_face_features:
            dist = np.linalg.norm(feat - current)
            if dist < THRESHOLD:
                return True
        return False
    except:
        return False

# ====================== OK手势 ======================
def is_ok_gesture(hand_landmarks):
    try:
        h = mp_hands.HandLandmark
        thumb = hand_landmarks.landmark[h.THUMB_TIP]
        index = hand_landmarks.landmark[h.INDEX_FINGER_TIP]
        dx = abs(thumb.x - index.x)
        dy = abs(thumb.y - index.y)
        return dx + dy < 0.05
    except:
        return False

# ====================== 开机 ======================
def wake_on_lan(mac):
    try:
        subprocess.run(["wakeonlan", mac], check=True)
        print("\n✅【识别成功】 → 开机指令发送成功！")
        return True
    except Exception as e:
        print("\n❌ 开机失败：", e)
        return False

# ====================== 主循环 ======================
cap = cv2.VideoCapture(0)
last_face_check = 0
last_trigger = 0
is_authorized = False

face_detector = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
hand_detector = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

print("="*60)
print("🤖 OK手势开机")
print("⚡ 人脸检测：1秒/次")
print("="*60)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_res = face_detector.process(rgb)

    # 每秒只进行一次人脸比对
    if time.time() - last_face_check > FACE_CHECK_INTERVAL:
        if face_res.detections:
            is_authorized = is_me(frame)
        else:
            is_authorized = False
        last_face_check = time.time()

    # 仅本人识别成功后才监听手势
    if is_authorized:
        print("\r✅【已识别】等待OK手势...", end="")
        try:
            hand_res = hand_detector.process(rgb)
            if hand_res.multi_hand_landmarks:
                for hand in hand_res.multi_hand_landmarks:
                    if is_ok_gesture(hand):
                        if time.time() - last_trigger > COOLDOWN_TIME:
                            wake_on_lan(TARGET_MAC)
                            last_trigger = time.time()
        except:
            pass
    else:
        if face_res.detections:
            print("\r⚠️  陌生人脸 （已忽略）", end="")
        else:
            print("\r👀 等待人脸...", end="")

cap.release()
