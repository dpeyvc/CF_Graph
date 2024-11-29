import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# Codeforces API를 통해 특정 사용자의 레이팅 변화를 가져오는 함수
def get_user_rating_changes(handle):
    """
    사용자의 레이팅 변화를 Codeforces API에서 가져오는 함수.

    Args:
        handle (str): Codeforces 사용자 핸들.

    Returns:
        list: 레이팅 변화 데이터를 포함하는 리스트.

    Raises:
        ValueError: API 요청 실패 또는 잘못된 응답 시 예외를 발생.
    """
    url = f"https://codeforces.com/api/user.rating?handle={handle}"  # API URL
    response = requests.get(url)  # API 요청
    if response.status_code == 200:  # HTTP 상태 코드가 200이면 성공
        data = response.json()
        if data['status'] == 'OK':  # 응답 상태가 OK일 경우 데이터 반환
            return data['result']
        else:  # 응답에 문제가 있을 경우 예외 발생
            raise ValueError(f"API 응답 에러: {data['comment']}")
    else:  # HTTP 상태 코드가 200이 아닌 경우 예외 발생
        raise ValueError(f"데이터를 가져오지 못했습니다. HTTP 상태 코드: {response.status_code}")


# Codeforces 레이팅 점수 구간별로 배경 색상을 추가하는 함수
def add_background_colors(ax, min_rating, max_rating):
    """
    Codeforces 레이팅 구간에 따라 배경 색상을 추가하는 함수.

    Args:
        ax (matplotlib.axes.Axes): 그래프의 축 객체.
        min_rating (int): 그래프에서의 최소 레이팅.
        max_rating (int): 그래프에서의 최대 레이팅.
    """
    # Codeforces 레이팅 구간별 색상 정의
    color_ranges = [
        (0, 1199, 'gray'),  # Newbie: 0-1199, 회색
        (1200, 1399, 'green'),  # Pupil: 1200-1399, 초록색
        (1400, 1599, 'cyan'),  # Specialist: 1400-1599, 청록색
        (1600, 1899, 'blue'),  # Expert: 1600-1899, 파란색
        (1900, 2099, 'purple'),  # Candidate Master: 1900-2099, 보라색
        (2100, 2299, 'orange'),  # Master: 2100-2299, 주황색
        (2300, float('inf'), 'red')  # International Master 이상: 빨간색
    ]

    # 각 구간에 대해 배경색을 추가
    for start, end, color in color_ranges:
        # 레이팅이 그래프 범위 내에 있을 경우 배경 추가
        if start <= max_rating and end >= min_rating:
            ax.add_patch(
                Rectangle((0, start), 1, end - start, color=color, alpha=0.5,
                          transform=ax.get_yaxis_transform())
            )


# 사용자 레이팅 변화를 2차원 그래프로 시각화하는 함수
def plot_rating_changes(handle):
    """
    Codeforces 사용자 레이팅 변화를 시각화하는 함수.

    Args:
        handle (str): Codeforces 사용자 핸들.
    """
    try:
        # 사용자 레이팅 데이터를 API에서 가져오기
        rating_changes = get_user_rating_changes(handle)

        # 레이팅 변화 데이터를 준비
        contest_names = [entry['contestName'] for entry in rating_changes]  # 콘테스트 이름
        ratings = [entry['newRating'] for entry in rating_changes]  # 새로운 레이팅
        delta_ratings = [entry['newRating'] - entry['oldRating'] for entry in rating_changes]  # 레이팅 변화량

        # 그래프 생성
        plt.figure(figsize=(12, 6))  # 그래프 크기 설정
        ax = plt.gca()  # 현재 축 객체 가져오기

        # 배경 색상 추가
        min_rating = min(ratings)  # 최소 레이팅
        max_rating = max(ratings)  # 최대 레이팅
        add_background_colors(ax, min_rating, max_rating)  # 배경 색상 추가

        # 레이팅 변화 그래프 그리기
        plt.plot(ratings, marker='o', label='Rating', color='blue', linewidth=2)

        # 레이팅 변화량과 콘테스트 이름 주석 추가
        for i, (name, delta, rating) in enumerate(zip(contest_names, delta_ratings, ratings)):
            if delta != 0:  # 변화량이 0이 아닌 경우에만 표시
                plt.text(i, rating, f"{name}\nΔ{delta:+}", fontsize=8, ha='center', va='bottom')

        # 그래프 레이블 및 제목 설정
        plt.ylabel('Rating', fontsize=12)  # y축 레이블
        plt.title(f'{handle} Rating Changes', fontsize=14)  # 그래프 제목
        plt.grid(True, linestyle='--', alpha=0.7)  # 그리드 추가
        plt.legend()  # 범례 추가
        plt.tight_layout()  # 레이아웃 자동 조정

        # x축 눈금 및 라벨 제거
        plt.xticks([], [])  # x축 값 제거

        # 그래프 출력
        plt.show()
    except ValueError as e:
        # 예외 발생 시 에러 메시지 출력
        print(e)


# 사용 예시
user_handle = "iridescent24k"  # Codeforces 사용자 핸들
plot_rating_changes(user_handle)
