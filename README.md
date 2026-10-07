# 생성형 AI 기반 음성 모의면접 코치

생성형AI응용 과제를 위해 수업의 **STT(귀) → LLM(머리) → TTS(입)** 구조를 응용한 음성 모의면접 프로젝트입니다.

## 주요 기능

1. 사용자가 마이크로 면접 답변을 녹음하거나 음성 파일을 업로드합니다.
2. Gemini Transcribe가 답변을 텍스트로 변환합니다.
3. Gemini Flash가 답변의 구체성, 논리성, 직무적합성, 전달력을 평가합니다.
4. 점수, 잘한 점, 개선점, 개선된 답변 예시, 후속 질문을 생성합니다.
5. Flash TTS가 후속 질문을 면접관 목소리로 읽어 줍니다.
6. Gradio 화면에서 전체 기능을 한 번에 실행할 수 있습니다.

## 파일
- `AI_면접코치.ipynb` : 제출용 Jupyter Notebook
- `기획서_및_프롬프트.md` : 기획서 + 프롬프트
- `voice_utils.py` : 수업 구조를 반영한 음성 공통 함수
- `requirements.txt` : 필요 라이브러리
- `.env.example` : API 키 설정 예시

## 실행 방법

```bash
pip install -r requirements.txt
```

`.env.example`을 복사해 `.env`로 바꾸고 API 키를 입력합니다.

```text
GEMINI_API_KEY=발급받은_API_키
```

그 다음 `AI_면접코치.ipynb`를 열어 위에서부터 실행합니다.

> `.env`는 GitHub에 올리지 않습니다. 실제 제출 전 본인 목소리로 한 번 이상 실행해 결과를 확인하세요.
