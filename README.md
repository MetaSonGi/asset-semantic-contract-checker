# 장비 의미 모델 계약 검사기

장비 속성을 semantic ID로 식별하고 단위 변환, 중복 의미, 값 범위, 장비 연결 참조 오류를 검사합니다.

## 핵심 기능

표시명 대신 semantic ID를 기준으로 연결합니다. Kelvin→섭씨와 mm/s→m/s처럼 차원이 같은 변환만 허용합니다. 변환 후 범위를 검사하며 잘못된 속성을 정상 출력에서 제외합니다. 전체 valid=false면 소비자가 부분 정상 속성을 제어용으로 사용하지 않아야 합니다.

## 설치·실행

Python 3.10 이상. 외부 패키지·API 키·장비 연결이 필요 없습니다.

```bash
git clone https://github.com/MetaSonGi/asset-semantic-contract-checker.git
cd asset-semantic-contract-checker
python -m pip install -r requirements.txt
python main.py
python main.py --input sample-input.json --html result.html
python -m unittest -v
```

Windows에서 python 대신 py를 사용할 수 있습니다. 다른 디렉터리에서 실행해도 기본 샘플은 main.py 옆 파일에서 읽습니다. 모든 출력 파일 경로는 명시한 위치에 생성합니다.

## 웹에서 결과 확인

다운로드한 `example-report.html`을 브라우저에서 열면 검증한 샘플 결과가 보입니다. 입력을 수정하고 `python main.py --input sample-input.json --html result.html`을 실행하면 새 결과를 브라우저로 볼 수 있습니다. 보고서는 HTML에 결과를 포함하므로 네트워크·CDN·서버가 필요 없습니다. 입력 문자열은 escape해 HTML/스크립트로 실행하지 않습니다. 이는 입력 편집용 웹 앱이 아닌 실행 결과 뷰어입니다.

## 입력·출력 예제

합성 입력: [sample-input.json](sample-input.json). 필드와 형식은 이 파일이 최소 실행 예제입니다. 반환 규칙은 main.py의 `run(data)`에 정의됩니다. 손상된 JSON·필수 필드 누락·잘못된 수치 입력은 CLI가 종료 코드 2로 보고합니다.

```json
{
  "contracts": {
    "urn:demo:temperature": {
      "kind": "temperature",
      "min": -20,
      "max": 100,
      "required": true
    },
    "urn:demo:speed": {
      "kind": "speed",
      "min": 0,
      "max": 2
    }
  },
  "assets": [
    {
      "id": "oht-1",
      "connected_to": [
        "station-1"
      ],
      "properties": [
        {
          "semantic_id": "urn:demo:temperature",
          "value": 303.15,
          "unit": "K"
        },
        {
          "semantic_id": "urn:demo:speed",
          "value": 850,
          "unit": "mm/s"
        }
      ]
    },
    {
      "id": "station-1",
      "connected_to": [
        "missing-robot"
      ],
      "properties": [
        {
          "semantic_id": "urn:demo:temperature",
          "value": 35,
          "unit": "Cel"
        },
        {
          "semantic_id": "urn:demo:speed",
          "value": 3,
          "unit": "m/s"
        }
      ]
    }
  ]
}
```

출력 미리보기(생략 표시 부분은 설명이며 JSON 입력으로 사용하지 마세요):

```text
{
  "valid": false,
  "normalized_properties": [
    {
      "asset_id": "oht-1",
      "semantic_id": "urn:demo:temperature",
      "value": 30.0,
      "unit": "Cel"
    },
    {
      "asset_id": "oht-1",
      "semantic_id": "urn:demo:speed",
      "value": 0.85,
      "unit": "m/s"
    },
    {
      "asset_id": "station-1",
      "semantic_id": "urn:demo:temperature",
      "value": 35,
      "unit": "Cel"
    }
  ],
  "errors": [
    {
      "asset_id": "station-1",
      "semantic_id": "urn:demo:speed",
      "reason": "value_out_of_range"
    },
    {
      "asset_id": "station-1",
      "target": "missing-robot",
      "reason": "dangling_connection"
    }
  ],
  "format": "local_semantic_contract_not_aas_certification"
}
```

전체 실행 결과: [example-output.json](example-output.json), [example-report.html](example-report.html).

## 설계 판단·통합

표시명 대신 semantic ID를 기준으로 연결합니다. Kelvin→섭씨와 mm/s→m/s처럼 차원이 같은 변환만 허용합니다. 변환 후 범위를 검사하며 잘못된 속성을 정상 출력에서 제외합니다. 전체 valid=false면 소비자가 부분 정상 속성을 제어용으로 사용하지 않아야 합니다.

장비 데이터 수집 계층에서 합성 예제를 실제 데이터 스키마로 변환한 뒤 `run(data)`를 호출할 수 있습니다. Nest.js/Python 작업 큐 또는 테스트 자동화에서 JSON 입출력을 사용하고 XR/WebGL 화면에는 검증된 결과만 표시하는 방식으로 연결할 수 있습니다. 프로그램에는 실제 제어·유료 서비스·사용자 계정 접근 코드가 없습니다.

## 한계

AAS 표준 전체·RDF·SPARQL·온톨로지 추론을 구현한 것이 아닙니다. 로컬 계약 예제이며 표준 인증이 아닙니다. 지원 단위와 물리량은 화이트리스트에 한정됩니다.

가상의 경력, 논문 성능 수치, 모델 재현 또는 실물 제조 검증을 주장하지 않습니다. 데이터가 합성 예제인 만큼 현장 적용 전 데이터 품질·운영 조건을 다시 검증해야 합니다.

## 검증·근거

의미 있는 정상·경계·오류 테스트 4개를 실제 실행했습니다. 기록은 [VALIDATION.txt](VALIDATION.txt)에 있습니다. 논문 날짜·상태·확인 범위와 개발자 해석은 [TRENDS.md](TRENDS.md)를 참고하세요.

실행 기준일: 2026-10-09 (Asia/Seoul). 기존 저장소를 수정하지 않고 독립 프로그램으로 구성했습니다.
