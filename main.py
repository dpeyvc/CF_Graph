import requests
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Rectangle
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.widgets import Cursor
import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import platform
import os

# Codeforces 레이팅 구간 정의
RATING_CATEGORIES = [
    {"name": "Newbie", "range": (0, 1199), "color": "#808080"},
    {"name": "Pupil", "range": (1200, 1399), "color": "#008000"},
    {"name": "Specialist", "range": (1400, 1599), "color": "#03a89e"},
    {"name": "Expert", "range": (1600, 1899), "color": "#0000ff"},
    {"name": "Candidate Master", "range": (1900, 2099), "color": "#aa00aa"},
    {"name": "Master", "range": (2100, 2299), "color": "#ff8c00"},
    {"name": "International Master", "range": (2300, 2399), "color": "#ff8c00"},
    {"name": "Grandmaster", "range": (2400, 2599), "color": "#ff0000"},
    {"name": "International Grandmaster", "range": (2600, 2999), "color": "#ff0000"},
    {"name": "Legendary Grandmaster", "range": (3000, float('inf')), "color": "#ff0000"}
]


# 시스템별 기본 한글 폰트 설정
def set_korean_font():
    system = platform.system()

    if system == 'Darwin':  # macOS
        font_paths = [
            '/System/Library/Fonts/AppleSDGothicNeo.ttc',
            '/System/Library/Fonts/Supplemental/AppleGothic.ttf',
            '/Library/Fonts/NanumGothic.ttf'
        ]
    elif system == 'Windows':  # Windows
        font_paths = [
            'C:/Windows/Fonts/malgun.ttf',
            'C:/Windows/Fonts/gulim.ttc',
            'C:/Windows/Fonts/NanumGothic.ttf'
        ]
    else:  # Linux
        font_paths = [
            '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc'
        ]

    # 폰트 경로가 존재하는지 확인
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_prop = fm.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                plt.rcParams['font.family'] = font_name
                return True
            except:
                continue

    # 시스템 기본 폰트 중에서 한글 지원 폰트 찾기
    for font in fm.findSystemFonts():
        try:
            font_prop = fm.FontProperties(fname=font)
            font_name = font_prop.get_name()
            if any(name in font_name.lower() for name in ['gothic', 'gulim', 'batang', 'malgun', '나눔', '맑은', '고딕']):
                plt.rcParams['font.family'] = font_name
                return True
        except:
            continue

    return False


def get_user_info(handle):
    """사용자 정보를 가져오는 함수"""
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            return data['result'][0]
        else:
            raise ValueError(f"API 응답 에러: {data.get('comment', '알 수 없는 오류')}")
    else:
        raise ValueError(f"데이터를 가져오지 못했습니다. HTTP 상태 코드: {response.status_code}")


def get_user_rating_changes(handle):
    """사용자의 레이팅 변화를 Codeforces API에서 가져오는 함수"""
    url = f"https://codeforces.com/api/user.rating?handle={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            return data['result']
        else:
            raise ValueError(f"API 응답 에러: {data.get('comment', '알 수 없는 오류')}")
    else:
        raise ValueError(f"데이터를 가져오지 못했습니다. HTTP 상태 코드: {response.status_code}")


def get_rating_category(rating):
    """레이팅에 해당하는 카테고리와 색상을 반환하는 함수"""
    for category in RATING_CATEGORIES:
        if category["range"][0] <= rating <= category["range"][1]:
            return category["name"], category["color"]
    return "Unknown", "gray"


def add_background_colors(ax, min_rating, max_rating):
    """Codeforces 레이팅 구간에 따라 배경 색상을 추가하는 함수"""
    # 그래프 범위 여유 추가
    padding = (max_rating - min_rating) * 0.1
    min_display = max(0, min_rating - padding)
    max_display = max_rating + padding

    # 레이팅 구간별 배경색 추가
    for category in RATING_CATEGORIES:
        start, end = category["range"]
        color = category["color"]
        name = category["name"]

        if start <= max_display and end >= min_display:
            ax.add_patch(
                Rectangle((0, start), 1, end - start, color=color, alpha=0.2,
                          transform=ax.get_yaxis_transform())
            )
            # 구간 이름 표시
            if start >= min_display and start < max_display:
                ax.text(1.01, start + 10, name, transform=ax.get_yaxis_transform(),
                        fontsize=8, color=color, ha='left', va='bottom')

    return min_display, max_display


def create_rating_graph(root, handle):
    """레이팅 그래프를 생성하고 표시하는 함수"""
    try:
        # 사용자 정보와 레이팅 데이터 가져오기
        user_info = get_user_info(handle)
        rating_changes = get_user_rating_changes(handle)

        if not rating_changes:
            messagebox.showinfo("정보", f"{handle}님의 레이팅 이력이 없습니다.")
            return

        # 현재 사용자 레이팅과 최고 레이팅
        current_rating = user_info.get('rating', 0)
        max_rating = user_info.get('maxRating', 0)

        # 레이팅 변화 데이터 준비
        contest_numbers = list(range(1, len(rating_changes) + 1))
        contest_names = [entry['contestName'] for entry in rating_changes]
        contest_dates = [entry.get('ratingUpdateTimeSeconds', 0) for entry in rating_changes]
        old_ratings = [entry['oldRating'] for entry in rating_changes]
        new_ratings = [entry['newRating'] for entry in rating_changes]
        delta_ratings = [new - old for new, old in zip(new_ratings, old_ratings)]

        # 그래프를 위한 Figure 생성
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.subplots_adjust(right=0.85)  # 오른쪽 여백 추가

        # 배경 색상 추가
        min_rating_val = min(old_ratings + new_ratings)
        max_rating_val = max(max_rating, max(new_ratings))
        min_display, max_display = add_background_colors(ax, min_rating_val, max_rating_val)

        # 시각적으로 구분되는 마커 설정
        positive_color = '#4CAF50'  # 레이팅 상승
        negative_color = '#F44336'  # 레이팅 하락
        neutral_color = '#2196F3'  # 레이팅 유지

        # 레이팅 변화에 따른 색상 마커 설정
        colors = []
        for delta in delta_ratings:
            if delta > 0:
                colors.append(positive_color)
            elif delta < 0:
                colors.append(negative_color)
            else:
                colors.append(neutral_color)

        # 레이팅 라인 플롯
        line, = ax.plot(contest_numbers, new_ratings, '-', color='#7986CB', linewidth=2, zorder=1)

        # 각 대회별 마커 플롯
        scatter = ax.scatter(contest_numbers, new_ratings, c=colors, s=50, zorder=2)

        # 최고 레이팅 지점 표시
        max_rating_idx = new_ratings.index(max(new_ratings))
        ax.scatter([contest_numbers[max_rating_idx]], [new_ratings[max_rating_idx]],
                   color='gold', s=100, zorder=3, edgecolor='black', marker='*')

        # 축 레이블 및 제목 설정
        ax.set_title(f'{handle}의 Codeforces 레이팅 변화', fontsize=14, fontweight='bold')
        ax.set_xlabel('대회 참가 횟수', fontsize=12)
        ax.set_ylabel('레이팅', fontsize=12)

        # 그리드 설정
        ax.grid(True, linestyle='--', alpha=0.6)

        # y축 범위 조정
        ax.set_ylim(min_display, max_display)

        # x축 설정
        ax.set_xlim(0.5, len(contest_numbers) + 0.5)
        ax.set_xticks(contest_numbers)

        if len(contest_numbers) > 15:  # 대회가 많으면 x축 숫자 간격 조정
            step = max(1, len(contest_numbers) // 10)
            ax.set_xticks(contest_numbers[::step])

        # 호버 기능 추가
        annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="b", lw=1, alpha=0.8))
        annot.set_visible(False)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                cont, ind = scatter.contains(event)
                if cont:
                    idx = ind["ind"][0]
                    x = contest_numbers[idx]
                    y = new_ratings[idx]
                    annot.xy = (x, y)
                    delta = delta_ratings[idx]
                    text = f"대회: {contest_names[idx]}\n이전 레이팅: {old_ratings[idx]}\n새 레이팅: {y}\n변화: {delta:+}"
                    annot.set_text(text)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()

        # 정보 박스 추가 - 오른쪽 상단
        current_category, current_color = get_rating_category(current_rating)
        max_category, max_color = get_rating_category(max_rating)

        info_text = (
            f"현재 레이팅: {current_rating} ({current_category})\n"
            f"최고 레이팅: {max_rating} ({max_category})\n"
            f"참가 대회 수: {len(rating_changes)}회\n"
            f"평균 변화량: {sum(delta_ratings) / len(delta_ratings):.1f}"
        )

        # 텍스트 정보 추가
        props = dict(boxstyle='round', facecolor='white', alpha=0.7)
        ax.text(0.97, 0.97, info_text, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', horizontalalignment='right', bbox=props)

        # 커서 추가
        cursor = Cursor(ax, useblit=True, color='gray', linewidth=0.8)

        # 플롯을 Tkinter 창에 삽입
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 호버 이벤트 연결
        fig.canvas.mpl_connect("motion_notify_event", hover)

        # 레이팅 변화 추세선 (이동 평균) 추가 - 5개 대회 기준
        if len(new_ratings) >= 5:
            window_size = min(5, len(new_ratings))
            trend = np.convolve(new_ratings, np.ones(window_size) / window_size, mode='valid')
            trend_x = np.arange(window_size - 1, len(new_ratings))
            ax.plot(trend_x + 1, trend, '--', color='#FF9800', linewidth=1.5, label='추세선 (5대회 평균)')
            ax.legend(loc='upper left')

    except Exception as e:
        messagebox.showerror("오류", f"데이터를 가져오는 중 오류가 발생했습니다: {e}")


def main():
    # 한글 폰트 설정
    korean_font_set = set_korean_font()
    if not korean_font_set:
        print("경고: 한글 폰트를 찾을 수 없습니다. 일부 텍스트가 깨질 수 있습니다.")

    # matplotlib 설정
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

    # Tkinter 루트 윈도우 생성
    root = tk.Tk()
    root.title("Codeforces 레이팅 시각화")
    root.geometry("1000x600")

    # 입력 프레임
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    # 핸들 입력 필드
    tk.Label(input_frame, text="Codeforces 핸들:").pack(side=tk.LEFT, padx=5)
    handle_entry = tk.Entry(input_frame, width=20)
    handle_entry.pack(side=tk.LEFT, padx=5)
    handle_entry.insert(0, "KongSoonE")  # 기본값 설정

    # 그래프 생성 버튼
    def on_generate():
        handle = handle_entry.get().strip()
        if handle:
            # 이전 그래프 삭제
            for widget in root.winfo_children():
                if widget != input_frame:
                    widget.destroy()

            # 새 그래프 생성
            create_rating_graph(root, handle)
        else:
            messagebox.showwarning("경고", "Codeforces 핸들을 입력해주세요!")

    # 시각화 테마 선택 옵션 추가
    theme_var = tk.StringVar(value="light")

    def change_theme():
        theme = theme_var.get()
        if theme == "dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('default')

        # 테마 변경 후 그래프 다시 그리기
        on_generate()

    theme_frame = tk.Frame(input_frame)
    theme_frame.pack(side=tk.LEFT, padx=10)

    tk.Radiobutton(theme_frame, text="밝은 테마", variable=theme_var, value="light", command=change_theme).pack(
        side=tk.LEFT)
    tk.Radiobutton(theme_frame, text="어두운 테마", variable=theme_var, value="dark", command=change_theme).pack(
        side=tk.LEFT)

    generate_btn = tk.Button(input_frame, text="그래프 생성", command=on_generate)
    generate_btn.pack(side=tk.LEFT, padx=5)

    # 저장 버튼 추가
    def save_graph():
        try:
            handle = handle_entry.get().strip()
            if handle:
                filename = f"{handle}_rating_graph.png"
                plt.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("저장 완료", f"그래프가 '{filename}' 파일로 저장되었습니다.")
        except Exception as e:
            messagebox.showerror("저장 오류", f"그래프 저장 중 오류가 발생했습니다: {e}")

    save_btn = tk.Button(input_frame, text="그래프 저장", command=save_graph)
    save_btn.pack(side=tk.LEFT, padx=5)

    # 초기 그래프 생성
    create_rating_graph(root, "KongSoonE")

    # 메인 루프 실행
    root.mainloop()


if __name__ == "__main__":
    main()