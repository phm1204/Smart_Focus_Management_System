import cv2
import numpy as np


def tracking_eye():
    cap = cv2.VideoCapture(0)  # 웹캠 (0번 카메라)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # ROI (카메라 프레임에서 눈 영역 지정)
        roi = frame[269:795, 537:1416]

        rows, columns, _ = roi.shape

        # 그레이스케일 변환
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # 블러 처리
        gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)

        # Threshold 처리
        _, thre = cv2.threshold(
            gray_roi,
            3,
            255,
            cv2.THRESH_BINARY_INV
        )

        # 윤곽선 검출
        contours, _ = cv2.findContours(
            thre,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # 큰 윤곽선부터 정렬
        contours = sorted(
            contours,
            key=lambda x: cv2.contourArea(x),
            reverse=True
        )

        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)

            # 사각형 표시
            cv2.rectangle(
                roi,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            # 중심선 표시
            cv2.line(
                roi,
                (x + w // 2, 0),
                (x + w // 2, rows),
                (0, 255, 0),
                2
            )

            cv2.line(
                roi,
                (0, y + h // 2),
                (columns, y + h // 2),
                (0, 255, 0),
                2
            )

            break

        cv2.imshow("Eye Tracking", roi)

        # ESC 누르면 종료
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    tracking_eye()