# Codeforces Rating Graph

Codeforces API를 활용하여 레이팅 변화량을 그래프로 나타냅니다.

Codeforces 프로필에서 기본으로 제공되지만, 제 자기소개 페이지에 넣고 싶어서 만들어봤습니다.

Codeforces 레이팅 범위를 반영한 동적 배경과 대회 이름 및 레이팅 변화를 시각적으로 표시합니다.


## 기능

- **동적 배경 색상**: Codeforces 레이팅 범위(예: Newbie, Expert, Specialist 등)에 따라 그래프 배경에 색상을 표시합니다.
- **레이팅 변화 시각화**: 사용자의 레이팅 변화를 선 그래프로 표시합니다.
- **대회 이름 및 레이팅 변화량 표시**: 각 대회 이름과 해당 대회에서의 레이팅 변화량(`Δ`)을 그래프에 주석으로 표시합니다.
- **사용자 친화적 설계**: 간단히 실행할 수 있으며, 시각적으로 명확한 결과물을 제공합니다.


## 요구 사항
- `requests`: Codeforces API 데이터를 가져오기 위해 사용됩니다.
- `matplotlib`: 시각화를 위해 사용됩니다.

```bash
pip install requests matplotlib
```


## 사용법

1. `user_handle` 변수에 자신의 핸들을 입력합니다.
2. 아래의 명령어를 통해 main.py 파일을 실행합니다.
   ```bash
   python3 main.py
   ```

실행 결과를 확인합니다:
<img src="https://gist.github.com/user-attachments/assets/39f393fb-647f-4acd-a605-c7275d61529d">

