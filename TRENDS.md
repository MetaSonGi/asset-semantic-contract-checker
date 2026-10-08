# 논문 근거와 개발자 해석

조사 기준일: **2026-10-09 (Asia/Seoul)**. 확인 범위: 저자 원문 저장소 arXiv의 초록·제출 이력·comments·관련 DOI. 전문 실험·부록·코드 및 성능 재현은 확인하지 않았습니다. 최신 검색에 나온 일부 원문(2609.09625, 2609.32923)은 열기 실패로 설계 근거에서 제외했습니다. 아래는 완전한 최신 문헌 조사나 최신 순위가 아닙니다.

## Industrial Semantics-Aware Digital Twins: A Hybrid Graph Matching Approach for Asset Administration Shells

- 원문: https://arxiv.org/abs/2601.06613
- 발표/제출일: 2026-01-10
- 상태: arXiv v1; CCNC 관련 DOI(10.1109/CCNC65079.2026.11366338) 연결 확인, 학회 최종본 전문 미확인
- 확인한 사실(초록): AAS의 서로 다른 어휘와 모델링 관례에 대응해 SPARQL 사전 필터와 RDF2vec 유사도 결합을 제안합니다.
- 개발자 해석: 속성 표시명보다 semantic ID·단위·장비 관계를 명시하는 계약이 먼저 필요합니다.

## Grounding Time-Series Foundation Models in Digital Twin Topology for Predictive Maintenance

- 원문: https://arxiv.org/abs/2609.40071
- 발표/제출일: 2026-09-30
- 상태: arXiv preprint v1; RESS 투고 표기, 게재 확정 아님
- 확인한 사실(초록): 동결 TSFM의 C-MAPSS RUL 평가와 물리 연결 구조를 이용한 융합을 제안합니다.
- 개발자 해석: 여러 센서의 연결과 운영 조건을 명시하고 입력 품질·후행 검증을 모델 평가와 분리하는 설계가 유용합니다.

## 이 프로그램의 적용

표시명 대신 semantic ID를 기준으로 연결합니다. Kelvin→섭씨와 mm/s→m/s처럼 차원이 같은 변환만 허용합니다. 변환 후 범위를 검사하며 잘못된 속성을 정상 출력에서 제외합니다. 전체 valid=false면 소비자가 부분 정상 속성을 제어용으로 사용하지 않아야 합니다.

논문의 TSFM·임베딩·LLM·실험 모델을 재현한 것이 아닙니다. 표준 라이브러리 기반의 설명 가능한 오프라인 도구입니다. 논문 성능 수치나 물리 장비 검증을 주장하지 않습니다.
