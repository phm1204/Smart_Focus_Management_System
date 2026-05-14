import win32gui
import time

# ==================================
# 비집중 키워드만 관리
# ==================================

distract_keywords = [
    "instagram",
    "youtube",
    "netflix",
    "tiktok",
    "facebook",
    "league of legends",
    "lol",
    "game",
    "discord"
]

# ==================================
# 변수 초기화
# ==================================

last_title = ""

focus_time = 0
distract_time = 0

print("실시간 집중도 분석 시작...\n")

# ==================================
# 메인 루프
# ==================================

while True:

    # 현재 활성 창 제목 가져오기
    title = win32gui.GetWindowText(
        win32gui.GetForegroundWindow()
    )

    title_lower = title.lower()

    # 기본 상태는 집중
    focused = True

    # ==================================
    # 비집중 키워드 검사
    # ==================================

    for word in distract_keywords:
        if word in title_lower:
            focused = False
            break

    # ==================================
    # 창 변경 시 출력
    # ==================================

    if title != last_title:

        print("\n" + "=" * 60)
        print(f"새로 감지된 창: {title}")

        if focused:
            print("현재 상태: 집중 중")
        else:
            print("현재 상태: 집중 이탈")

        print("=" * 60)

        last_title = title

    # ==================================
    # 시간 측정
    # ==================================

    if focused:
        focus_time += 1
    else:
        distract_time += 1

    # ==================================
    # 실시간 통계 출력
    # ==================================

    print(
        f"집중 시간: {focus_time}초 | "
        f"이탈 시간: {distract_time}초",
        end="\r"
    )

    time.sleep(1)