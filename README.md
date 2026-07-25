# 서울 신속통합기획 선정구역 지도

서울시 신속통합기획(신통기획) 선정구역을 지도에서 확인하는 정적 웹사이트입니다.

## 제공 기능

- 신속통합기획·일반 정비사업·중복 사업장 3개 레이어 필터
- 구역 면적에 비례한 원형 마커와 상세 정보 패널
- 지하철역 표시/숨김
- 모바일·태블릿·데스크톱 반응형 레이아웃
- 서울시 공식 목록을 매일 동기화하는 GitHub Actions 배치

## 실행 방법

`index.html`을 브라우저에서 열거나 정적 웹 서버로 제공하면 됩니다. 지도 타일, Leaflet 라이브러리, 서울시 위치도 이미지는 인터넷 연결이 필요합니다.

## 데이터와 한계

신속통합기획 데이터는 [서울시 정비사업 정보몽땅](https://cleanup.seoul.go.kr/cleanup/view/publicIntgrPlanArea.do), 일반 정비사업 데이터는 [사업장검색](https://cleanup.seoul.go.kr/cleanup/bsnssttus/lscrMainIndx.do)에서 수집합니다. 일반 정비사업은 서울시 도시공간포털 지도 레코드가 있는 경우에만 공식 도형의 중심점을 지도에 표시합니다. 지도 레코드가 없는 사업장은 임의 좌표로 표시하지 않습니다.

## 자동 동기화와 알림

GitHub Actions는 매일 05:15(KST)에 일반 정비사업 목록을 수집하고 변경 시 Pages를 갱신합니다. Telegram 알림을 사용하려면 저장소 Secrets에 `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`를 설정해야 합니다.

## 배포

GitHub Pages 배포 시 `Settings → Pages → Deploy from a branch → main / (root)`를 선택하면 공개 URL로 접근할 수 있습니다.
