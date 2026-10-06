[English](README.md) · **한국어** · [简体中文](README.zh-CN.md)

# SoWhat Decks: 두괄식 PPT 발표 자료를 만드는 Claude Code 스킬

코딩 에이전트가 결론부터 말하는 PPT를 만들고, 바로 고칠 수 있는 파워포인트(.pptx) 파일로 넘겨 줍니다.

메모와 데이터를 에이전트에게 주세요. 에이전트가 스토리라인을 짜고, 내 템플릿 위에 네이티브 차트를 넣어 .pptx를 만들고, 다른 사람이 보기 전에 덱을 검토합니다. 이사회 보고, 투자자 업데이트, 전략 제안처럼 컨설팅 보고서 방식으로 쓰는 발표 자료에 맞췄습니다. 슬라이드마다 결론을 한 문장 제목으로 쓰고, 그 근거를 아래에 놓는 방식입니다.

무료 오픈소스(MIT)입니다. [Pro](#pro)는 고급 도표와 덱 레시피를 더합니다.

![예제 덱의 슬라이드 6장: 요약, 기울기 차트, 누적 막대, 선 차트, 결정 요청 슬라이드. 모두 제목이 한 문장으로 되어 있다](docs/img/hero.png)

## 제목만 읽어 보세요

같은 샘플 데이터로 만든 3분기 이사회 보고 두 가지입니다. 왼쪽 초안은 슬라이드마다 주제어를 제목으로 달았고, 오른쪽은 SoWhat Decks로 다시 만든 덱입니다. 둘 다 [`examples/03-review-before-after`](examples/03-review-before-after/)에 있습니다. 덱은 영어로 만들었고, 아래 제목은 우리말로 옮긴 것입니다.

| 초안 | SoWhat Decks로 다시 만든 덱 |
|---|---|
| 요약 | 3분기는 계획을 넘었지만 SMB 이탈로 연말 ARR이 $230k 모자란다. 채용 2명을 온보딩으로 돌리자고 제안한다 |
| 3분기 ARR 브리지 | 기말 ARR $11.05M은 계획을 1.4% 넘었지만, 이탈이 늘어 초과 폭이 신규 ARR보다 작다 |
| 세그먼트별 이탈 | SMB 이탈 ARR은 1분기 이후 두 배 넘게 늘어 이제 신규 계약의 3분의 1을 상쇄한다 |
| 온보딩 역량 | 담당자 1명당 신규 계정이 41% 늘면서 셋업 완료율이 68%에서 55%로 떨어졌다 |
| 다음 단계 | 이사회에 인력 재배치와 연말 전망 수정치 $11.85M 승인을 요청한다 |

오른쪽 열만 훑어도 무슨 일이 있었는지, 왜 그랬는지, 이사회가 무엇을 결정해야 하는지 알 수 있습니다. `deck-storyline`의 제목 검사는 초안 제목 14개 중 8개를 오류로, 3개를 경고로 표시합니다([출력](examples/storyline-tests/control-topic-titles/title-lint.txt)).

![스토리라인부터 검토가 끝난 덱까지: deck-review가 초안의 문제에 상자를 치고, deck-storyline이 제목을 다시 쓰고, deck-build가 슬라이드를 다시 만들고, 마지막 검토에서 high 0건, medium 0건이 나온다](docs/img/demo.gif)

## 써 보기

설치한 뒤(아래 참고) 다음 중 하나를 에이전트에게 붙여 넣으세요.

> ./my-deck.pptx에 deck-review를 써 줘. 가장 중요한 수정 다섯 가지를 알려 줘.

> deck-storyline으로 ./notes.md와 ./metrics.csv를 바탕으로 10장짜리 이사회 보고를 기획해 줘. 받아야 할 결정은 4분기 채용 계획 승인이야. 그다음 deck-build로 만들어 줘.

## 설치

**Claude Code 플러그인**

    /plugin marketplace add WQGGSEY/sowhat-decks
    /plugin install sowhat-decks@sowhat-decks

**skills CLI**

    npx skills add WQGGSEY/sowhat-decks

**Claude 앱(claude.ai):** [최신 릴리스](https://github.com/WQGGSEY/sowhat-decks/releases/latest)에서 스킬 ZIP을 내려받으세요. 릴리스마다 스킬별 ZIP과 네 개를 모두 담은 ZIP이 있습니다. Claude에서 Customize > Skills를 열고 +를 누른 뒤 Create skill, Upload a skill을 차례로 골라 스킬 ZIP을 한 번에 하나씩 올립니다(메뉴 이름은 영어 화면 기준). 코드 실행(Code execution)이 켜져 있어야 합니다. 이 방법은 아직 테스트하지 않았습니다.

**직접 설치:** `skills/` 안의 폴더를 `~/.claude/skills/`로 복사하세요.

Python 3.9 이상과 python-pptx가 필요합니다. LibreOffice와 pypdfium2는 선택입니다. 둘이 있으면 deck-build가 PDF와 PNG 미리보기를 내보내고, deck-review가 렌더링된 슬라이드까지 검사합니다. deck-review가 주석을 단 이미지를 만들려면 Pillow도 필요합니다. 스크립트는 아무것도 설치하지 않습니다.

macOS의 Claude Code에서 테스트했습니다. 다른 에이전트와 Claude 앱은 아직 테스트하지 않았습니다([한계](#한계) 참고).

## 작동 방식

| 스킬 | 하는 일 | 결과물 |
|---|---|---|
| `deck-storyline` | 목적, 청중, 받아야 할 결정, 자료를 하나의 핵심 메시지(governing message)와 SCQA로 정리하고, 슬라이드마다 한 문장 제목과 필요한 근거를 붙입니다. 빈 곳은 `[DATA NEEDED]`로 표시하고 제목만 읽는 테스트를 돌립니다. | `storyline.md`, 제목만 있는 고스트 덱 |
| `deck-build` | 내 .pptx나 .potx 템플릿 위에 덱을 만듭니다. 레이아웃 12종, 출처 줄, 쪽 번호, 발표자 노트, 영어·한국어·일본어 글꼴을 처리합니다. | `deck.pptx`, `deck.pdf`, 슬라이드 PNG |
| `deck-exhibits` | 메시지에 맞는 도표를 골라 네이티브 차트나 도형으로 그립니다. 막대, 선, 누적 막대, 강조 표, 2×2 매트릭스, 프로세스 셰브론. | 데이터가 파일 안에 들어 있는 차트 |
| `deck-review` | 어떤 도구로 만든 .pptx든 렌더링해서 제목, 글자 크기, 넘친 글, 슬라이드 밖 도형, 그림으로 붙인 차트, 빠진 출처를 검사하고, 슬라이드마다 평가 기준표로 점수를 매깁니다. 자동 수정은 글자와 숫자를 바꾸지 않습니다. | `review.md`, 주석을 단 PNG, `deck.fixed.pptx` |

스킬은 에이전트에게 내 자료나 출처를 밝힌 자료에 있는 숫자만 쓰라고 지시합니다. 자료가 주장을 뒷받침하지 못하면 슬라이드에 `[DATA NEEDED]`가 들어가고 검토에서 걸립니다. [`examples/storyline-tests`](examples/storyline-tests/)의 고스트 덱에서 두 단계를 모두 볼 수 있습니다. 덱을 보내기 전에 숫자를 확인하세요.

## 예제

폴더마다 브리프, 입력 자료, 스토리라인, 덱 명세, 덱(.pptx와 PDF), 슬라이드 PNG, 검토 결과, 출처가 있고, 덱을 다시 만드는 프롬프트와 명령을 적은 README가 있습니다. 최종 덱에는 deck-review 자동 검사의 high·medium 지적이 없고, `tests/test_examples.py`가 변경마다 이를 확인합니다. 예제 덱은 영어입니다.

| | 예제 | 바탕 자료 | 열기 |
|---|---|---|---|
| <img src="examples/01-investor-update/preview/slide-05.png" width="280" alt="슬라이드: 2025년 순이익의 대부분은 일회성 세금 혜택이다"> | **투자자 업데이트**, 13장 | 한 상장사의 FY2025 10-K와 주주서한 2통. 모든 숫자에 출처 표시 | [PDF](examples/01-investor-update/deck.pdf) · [PPTX](examples/01-investor-update/deck.pptx) · [스토리라인](examples/01-investor-update/storyline.md) · [검토](examples/01-investor-update/review.md) |
| <img src="examples/02-market-entry/preview/slide-06.png" width="280" alt="슬라이드: 소득을 감안하면 인도네시아 온라인 시장은 다른 후보의 두 배 이상이다"> | **동남아 어느 시장부터 들어갈까?** 13장 | 세계은행 지표, 출처 표시. 회사는 가상 | [PDF](examples/02-market-entry/deck.pdf) · [PPTX](examples/02-market-entry/deck.pptx) · [스토리라인](examples/02-market-entry/storyline.md) · [검토](examples/02-market-entry/review.md) |
| <img src="examples/03-review-before-after/preview/slide-02.png" width="280" alt="슬라이드: 요청으로 끝나는 이사회 보고 요약"> | **이사회 보고, 검토 후 다시 만들기**, 14장 | 샘플 데이터, 모든 슬라이드에 표시. 문제를 일부러 심은 초안과 그 검토 결과 포함 | [초안 검토](examples/03-review-before-after/review.md) · [초안 PDF](examples/03-review-before-after/before-review/render/before.pdf) · [다시 만든 PDF](examples/03-review-before-after/deck.pdf) · [프롬프트](examples/03-review-before-after/README.md#prompts-and-commands) |

## 어떤 덱이든 검토

`deck-review`는 어떤 도구나 사람이 만든 .pptx에도 쓸 수 있습니다. 슬라이드를 렌더링하고, 꼼꼼한 검토자가 잡아낼 문제를 나열하고, 약한 제목을 주장으로 다시 씁니다. 예제 03의 이사회 보고 초안에서는 high 1건, medium 18건, low 11건을 찾았습니다. 주제어 제목, 그림으로 붙인 차트 3개, 12pt보다 작은 글자, 출처 없는 도표, "TBD"로 남은 전망치입니다.

![왼쪽: deck-review가 주제어 제목과 그림으로 붙인 차트에 상자를 친 초안 슬라이드. 오른쪽: 한 문장 제목, 네이티브 누적 막대 차트, 출처 줄이 들어간 새 슬라이드](docs/img/review-before-after.png)

## 무료판과 Pro 비교

| | 무료 (MIT) | Pro ($29 일회성) |
|---|---|---|
| 스킬 | deck-storyline, deck-build, deck-exhibits, deck-review | 네 개 모두, 그리고 exhibits-pro, deck-recipes, brand-fit |
| 스토리라인 (핵심 메시지, SCQA, 액션 타이틀, 제목만 읽는 테스트) | ✓ | ✓ |
| 레이아웃 | 기본 레이아웃 12종 | 기본 레이아웃 12종, 그리고 덱 유형 10가지의 슬라이드 구성 |
| 내 템플릿 | 템플릿의 레이아웃과 개체 틀을 그대로 사용 | 복잡한 템플릿용 브랜드 맵을 더하고, 예전 덱을 새 템플릿으로 옮김 |
| 도표 | 6종: 막대, 선, 누적 막대, 강조 표, 2×2 매트릭스, 프로세스 셰브론 | 21종: 위 6종과 워터폴, 메코 차트, 간트 로드맵, 하비 볼 표, 밸류 드라이버 트리, 이슈 트리, 토네이도, 퍼널, 변화 화살표 막대, 사분면 산점도, 히트맵 표, RAG 스코어카드, 조직도, RACI, 벤치마크 점 도표 |
| 아무 .pptx 검토 | ✓ | ✓, 그리고 브랜드 검사 |
| 예제 | 덱 3개, 하나는 검토 전후 포함 | 레시피마다 하나씩 덱 10개 추가 |
| 스토리라인 워크시트 (PDF) | | ✓ |
| 업데이트 | 이 저장소 | 12개월 동안 모든 v1.x 릴리스 |
| 라이선스 | MIT | 1인, 덱 수 무제한 |

## Pro

무료판으로도 덱 한 벌을 끝까지 만들 수 있습니다. Pro는 더 어려운 덱을 위한 것입니다.

- **도표 15종 추가**, 모두 네이티브이고 수정 가능: 워터폴, 메코 차트, 간트 로드맵, 하비 볼 표, 밸류 드라이버 트리, 이슈 트리, 토네이도, 퍼널, 변화 화살표 막대, 사분면 산점도, 히트맵 표, RAG 스코어카드, 조직도, RACI, 벤치마크 점 도표
- **덱 레시피 10가지**, 각각 완성된 예제 덱(.pptx와 PDF) 포함: 전략 제안, 시장 진입, 이사회 리뷰, 투자 유치, 운영위원회, 사업 타당성, 실사, 제품 로드맵, 사후 분석, 고객 제안서
- **brand-fit**: 복잡한 회사 템플릿을 매핑하고 예전 덱을 새 템플릿으로 옮김
- 한 장짜리 스토리라인 워크시트, 12개월 동안 모든 v1.x 업데이트

$29 일회성 · 14일 환불 · 1인, 덱 수 무제한

**[SoWhat Decks Pro 구성 보기](https://sowhatlabs.gumroad.com/l/sowhat-decks-pro)**

## 한계

- 렌더링에는 LibreOffice를 씁니다. 없으면 deck-review는 구조 검사만 하고 시각 검사는 건너뜁니다.
- PowerPoint는 LibreOffice나 Keynote와 줄바꿈이 조금 다를 수 있습니다. 보내기 전에 최종 덱을 PowerPoint에서 열어 보세요.
- 무료판은 도표 6종을 그립니다. 워터폴, 메코 차트, 트리, 로드맵은 Pro에 있습니다.
- 슬라이드 마스터가 많거나 개체 틀이 특이한 템플릿은 무료판에서 레이아웃을 직접 매핑해야 할 수 있습니다.
- deck-review는 .pptx만 읽습니다. .ppt, .key, 암호가 걸린 파일은 열지 못하고, SmartArt나 포함된 개체 안은 보지 않습니다.
- deck-review의 자동 검사는 놓치는 것이 있습니다. 그림으로 붙인 차트 검사는 진한 축선을 찾는 방식이고, 주제어 제목 검사는 예제 03의 주제어 제목 12개 중 하나를 놓쳤습니다. 그 하나는 평가 기준표의 제목만 읽기 단계에서 잡혔습니다.
- Google 슬라이드: .pptx를 가져오세요. 스킬은 Google Slides API를 호출하지 않습니다.
- macOS의 Claude Code에서 영어와 한국어 덱으로 테스트했습니다. 일본어는 기본 동작만 확인했습니다. 다른 에이전트는 아직 테스트하지 않았습니다.
- Claude 앱과 Claude for PowerPoint: 각 SKILL.md에 채팅과 Claude for PowerPoint용으로 설계한 노코드 모드가 있지만, 그곳에서는 아직 테스트하지 않았습니다.

## 개인정보

스크립트는 내 컴퓨터에서 실행되고 네트워크를 호출하지 않습니다. 에이전트는 내가 준 파일을 봅니다. LibreOffice는 렌더링할 때 덱 안에 들어 있는 링크를 따라갈 수 있으니, 모르는 사람이 보낸 덱에는 deck-review를 `--no-render`로 실행하세요.

## 개발

    python3 -m pip install python-pptx pypdfium2 pytest
    python3 -m pytest -q

렌더링 테스트는 LibreOffice가 설치되어 있을 때만 돕니다. 저장소를 고치는 규칙은 `AGENTS.md`에 있습니다. `tools/build_skill_zips.py`는 릴리스 ZIP을 만들고(릴리스 워크플로가 `v*` 태그마다 실행), `tools/make_readme_images.py`는 예제 슬라이드로 `docs/img/`의 이미지를 다시 만듭니다.

## 라이선스

MIT. 예제 덱은 출처가 있는 공개 데이터나 샘플 데이터라고 표시한 데이터를 씁니다. 투자자 업데이트 예제는 공개 공시 자료로 만든 예시이며, 다룬 회사와 관계가 없습니다. 예제는 개발 중에 Claude Code 에이전트가 이 스킬을 따라 만들었고, 예제마다 README에 프롬프트와 명령을 다시 적어 두었습니다.

SoWhat Decks는 Anthropic이나 Microsoft와 관계없는 독립 프로젝트입니다.

이 문서는 [영어 README](README.md)를 옮긴 것입니다. 두 문서가 다르면 영어판을 따릅니다.
