import cv2
import numpy as np

# =========================
# 얼굴 검출기
# =========================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_frontalface_default.xml'
)

# =========================
# 눈 검출기
# =========================
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    'haarcascade_eye.xml'
)

# =========================
# 웹캠 시작
# =========================
cap = cv2.VideoCapture(0)

# 이전 방향 저장
last_direction = ""

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # 좌우 반전
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # =========================
    # 얼굴 검출
    # =========================
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=8,
        minSize=(200, 200)
    )

    for (x, y, w, h) in faces:

        # 얼굴 박스
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        face_gray = gray[y:y+h, x:x+w]
        face_color = frame[y:y+h, x:x+w]

        # =========================
        # 눈 검출
        # =========================
        eyes = eye_cascade.detectMultiScale(
            face_gray,
            scaleFactor=1.1,
            minNeighbors=12,
            minSize=(40, 40),
            maxSize=(120, 120)
        )

        for (ex, ey, ew, eh) in eyes:

            # 눈 영역 박스
            cv2.rectangle(
                face_color,
                (ex, ey),
                (ex + ew, ey + eh),
                (0, 255, 0),
                2
            )

            # =========================
            # 눈 ROI
            # =========================
            eye_gray = face_gray[
                ey:ey + eh,
                ex:ex + ew
            ]

            eye_color = face_color[
                ey:ey + eh,
                ex:ex + ew
            ]

            # 블러
            blur = cv2.GaussianBlur(
                eye_gray,
                (9, 9),
                2
            )

            # =========================
            # 동공 원 검출
            # =========================
            circles = cv2.HoughCircles(
                blur,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=20,
                param1=50,
                param2=15,
                minRadius=5,
                maxRadius=25
            )

            # 눈 크기
            eye_h, eye_w = eye_gray.shape

            # 원 검출 성공
            if circles is not None:

                circles = np.uint16(
                    np.around(circles)
                )

                # 첫 번째 원만 사용
                for circle in circles[0, :1]:

                    cx, cy, radius = circle

                    # =========================
                    # 동공 원
                    # =========================
                    cv2.circle(
                        eye_color,
                        (cx, cy),
                        radius,
                        (255, 0, 255),
                        2
                    )

                    # 중심점
                    cv2.circle(
                        eye_color,
                        (cx, cy),
                        2,
                        (0, 0, 255),
                        3
                    )

                    # =========================
                    # 시선 방향 계산
                    # =========================
                    horizontal_ratio = cx / eye_w
                    vertical_ratio = cy / eye_h

                    direction = "CENTER"

                    # 좌우 방향
                    if horizontal_ratio < 0.35:
                        direction = "LEFT"

                    elif horizontal_ratio > 0.65:
                        direction = "RIGHT"

                    # 상하 방향
                    if vertical_ratio < 0.35:
                        direction = "UP"

                    elif vertical_ratio > 0.65:
                        direction = "DOWN"

                    # =========================
                    # 화면 출력
                    # =========================
                    cv2.putText(
                        eye_color,
                        direction,
                        (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

                    # =========================
                    # 터미널 출력
                    # =========================
                    if direction != last_direction:
                        print(f"현재 시선 방향: {direction}")
                        last_direction = direction

        # =========================
        # 콧구멍 ROI
        # =========================
        nose_gray = face_gray[
            int(h * 0.50):int(h * 0.80),
            int(w * 0.30):int(w * 0.70)
        ]

        nose_color = face_color[
            int(h * 0.50):int(h * 0.80),
            int(w * 0.30):int(w * 0.70)
        ]

        blur = cv2.GaussianBlur(
            nose_gray,
            (7, 7),
            0
        )

        _, nose_thresh = cv2.threshold(
            blur,
            50,
            255,
            cv2.THRESH_BINARY_INV
        )

        contours, _ = cv2.findContours(
            nose_thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        contours = sorted(
            contours,
            key=cv2.contourArea,
            reverse=True
        )

        nostril_count = 0

        for cnt in contours:

            area = cv2.contourArea(cnt)

            if area > 50 and area < 500:

                nx, ny, nw, nh = cv2.boundingRect(cnt)

                if nw < 40 and nh < 40:

                    cv2.rectangle(
                        nose_color,
                        (nx, ny),
                        (nx + nw, ny + nh),
                        (0, 255, 255),
                        2
                    )

                    nostril_count += 1

            if nostril_count >= 2:
                break

    # =========================
    # 출력 화면
    # =========================
    cv2.imshow(
        "Face / Eye / Pupil Tracking",
        frame
    )

    # ESC 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()