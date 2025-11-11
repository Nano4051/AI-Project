from ultralytics import YOLO
import cv2
import numpy as np
import csv
import time

# --- 영상 파일 ---
VIDEO_PATH = "watermarked_preview.mp4"

# --- 모델 로드 (CPU용) ---
model = YOLO("yolov8n.pt")
VEHICLE_CLASSES = [2, 3, 5, 7]  # car, motorcycle, bus, truck

# --- 드래그 기반 슬롯 정의 ---
slots = []
drawing = False
ix, iy = -1, -1

cap = cv2.VideoCapture(VIDEO_PATH)
ret, frame = cap.read()
if not ret:
    print("영상 읽기 실패")
    cap.release()
    exit()

temp_frame = frame.copy()

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, temp_frame
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_frame = frame.copy()
            # 이미 정의된 슬롯 그리기
            for slot in slots:
                pts = np.array(slot, np.int32).reshape((-1,1,2))
                cv2.polylines(temp_frame,[pts], True, (0,0,255), 2)
            cv2.rectangle(temp_frame, (ix, iy), (x, y), (0,255,0), 2)
            cv2.imshow("Define Slots", temp_frame)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x1, y1 = ix, iy
        x2, y2 = x, y
        slot = [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]
        slots.append(slot)
        cv2.rectangle(temp_frame, (x1,y1), (x2,y2), (0,0,255), 2)
        cv2.imshow("Define Slots", temp_frame)
        print(f"Slot added: {slot}")

cv2.imshow("Define Slots", temp_frame)
cv2.setMouseCallback("Define Slots", draw_rectangle)
print("드래그로 슬롯 영역을 지정하세요. 완료 후 'q' 키를 누르세요.")

while True:
    cv2.imshow("Define Slots", temp_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()

# --- 슬롯 CSV 저장 ---
with open("slots.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['slot_id','x1','y1','x2','y2','x3','y3','x4','y4'])
    for idx, slot in enumerate(slots):
        row = [idx+1]
        for pt in slot:
            row.extend(pt)
        writer.writerow(row)

print("slots.csv 저장 완료")

# --- 차량 존재 판단 함수 ---
def is_slot_occupied(slot, boxes):
    slot_poly = np.array(slot)
    for box in boxes:
        cls = int(box.cls.item())
        if cls not in VEHICLE_CLASSES:
            continue
        xyxy = box.xyxy.cpu().numpy().reshape(-1,4)
        for x1, y1, x2, y2 in xyxy:
            cx, cy = int((x1+x2)/2), int((y1+y2)/2)
            if cv2.pointPolygonTest(slot_poly, (cx, cy), False) >= 0:
                return True
    return False

# --- 영상 순회하면서 빈 자리 표시 ---
cap = cv2.VideoCapture(VIDEO_PATH)
prev_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.2, imgsz=960)
    boxes = results[0].boxes
    annotated_frame = results[0].plot()

    # --- 슬롯별 빈 자리 표시 ---
    for slot in slots:
        color = (0,255,0) if not is_slot_occupied(slot, boxes) else (0,0,255)
        pts = np.array(slot, np.int32).reshape((-1,1,2))
        cv2.polylines(annotated_frame,[pts], isClosed=True, color=color, thickness=2)

    # --- FPS 표시 ---
    curr_time = time.time()
    fps = 1/(curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(annotated_frame, f"FPS: {fps:.2f}", (20,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255),2)

    cv2.imshow("Parking Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
