# Codeforces Rating Graph

Codeforces API를 사용하여 특정 사용자의 레이팅 변화를 시각화하는 Python 도구입니다. 이 도구는 2차원 그래프를 생성하며,

Codeforces 레이팅 범위를 반영한 동적 배경과 대회 이름 및 레이팅 변화를 시각적으로 표시합니다.


## 기능

- **동적 배경 색상**: Codeforces 레이팅 범위(예: Newbie, Expert, Specialist 등)에 따라 그래프 배경에 색상을 표시합니다.
- **레이팅 변화 시각화**: 사용자의 레이팅 변화를 선 그래프로 표시합니다.
- **대회 이름 및 레이팅 변화량 표시**: 각 대회 이름과 해당 대회에서의 레이팅 변화량(`Δ`)을 그래프에 주석으로 표시합니다.
- **사용자 친화적 설계**: 간단히 실행할 수 있으며, 시각적으로 명확한 결과물을 제공합니다.


## 요구 사항

이 도구를 사용하려면 아래 Python 라이브러리가 필요합니다:

- `requests`: Codeforces API 데이터를 가져오기 위해 사용됩니다.
- `matplotlib`: 시각화를 위해 사용됩니다.

아래 명령어를 통해 필수 라이브러리를 설치할 수 있습니다:

```bash
pip install requests matplotlib
```


## 사용법

1. 이 저장소를 클론합니다:
   ```bash
   git clone https://github.com/yechan6855/CF_Graph.git
   cd CF_Graph
   ```

2. `main.py` 파일을 엽니다.

3. `user_handle` 변수에 Codeforces 사용자의 핸들을 입력합니다:
   ```python
   user_handle = "{handle}"  # 원하는 핸들로 변경
   ```

4. 스크립트를 실행합니다:
   ```bash
   python main.py
   ```

5. 실행 결과를 확인합니다:
![image](https://github.com/user-attachments/assets/e6755c50-5624-49f2-aafd-558a9bc1960c)



## 라이선스

이 프로젝트는 MIT 라이선스에 따라 제공됩니다. 자세한 내용은 아래 라이선스를 확인하세요.

```markdown
MIT License

Copyright (c) 2024 yechan6855

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새 기능 브랜치를 생성합니다: `git checkout -b feature/새로운-기능`.
3. 변경 사항을 커밋합니다: `git commit -m "새로운 기능 추가"`.
4. 브랜치에 푸시합니다: `git push origin feature/새로운-기능`.
5. 풀 리퀘스트를 생성합니다.


## 문의

[이슈](https://github.com/yechan6855/CF_Graph/issues)를 통해 문의해주세요.
