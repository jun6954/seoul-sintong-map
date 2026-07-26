# 서울 신속통합기획 선정구역 지도

서울시 신속통합기획·일반 정비사업을 네이버 지도에서 확인하는 정적 웹사이트입니다.

## 제공 기능

- 신속통합기획·일반 정비사업·중복 사업장 3개 레이어 필터
- 구역 면적에 비례한 원형 마커·공식 사업 경계 폴리곤·상세 정보 패널
- 도로명·지번 검색과 사업지 주소 자동완성
- 겹치는 사업지 선택 메뉴와 지도/리스트 보기
- Supabase 이메일 매직링크 로그인 기반 즐겨찾기 동기화
- 모바일·태블릿·데스크톱 반응형 레이아웃
- 서울시 공식 목록을 매일 동기화하는 GitHub Actions 배치

## 실행 방법

`index.html`을 브라우저에서 열거나 정적 웹 서버로 제공하면 됩니다. 네이버 지도, Supabase, 서울시 위치도 이미지는 인터넷 연결이 필요합니다.

## 데이터와 한계

신속통합기획 데이터는 [서울시 정비사업 정보몽땅](https://cleanup.seoul.go.kr/cleanup/view/publicIntgrPlanArea.do), 일반 정비사업 데이터는 [사업장검색](https://cleanup.seoul.go.kr/cleanup/bsnssttus/lscrMainIndx.do)에서 수집합니다. 일반 정비사업은 서울시 도시공간포털 지도 레코드가 있는 경우에만 공식 도형의 중심점을 지도에 표시합니다. 지도 레코드가 없는 사업장은 임의 좌표로 표시하지 않습니다.

## 자동 동기화와 알림

GitHub Actions는 매일 05:15(KST)에 일반 정비사업 목록을 수집하고 변경 시 Pages를 갱신합니다. Telegram 알림을 사용하려면 저장소 Secrets에 `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`를 설정해야 합니다.

## 즐겨찾기 Supabase 설정

1. Supabase Dashboard의 **SQL Editor**에서 [`supabase/migrations/20260726_create_favorites.sql`](supabase/migrations/20260726_create_favorites.sql) 전체를 실행합니다.
2. **Authentication → URL Configuration**에서 Site URL과 Additional Redirect URLs에 `https://jun6954.github.io/seoul-sintong-map/`를 추가합니다.
3. Email 로그인 기능을 활성화합니다. 지도에서 **로그인**을 누르고 이메일로 받은 링크를 열면, 모든 브라우저·기기에서 동일한 즐겨찾기가 표시됩니다.

클라이언트에는 Supabase Publishable key만 포함되며, 행 수준 보안(RLS) 정책으로 각 사용자는 자신의 즐겨찾기만 읽고 수정할 수 있습니다. secret/service_role 키는 절대 브라우저 코드에 넣지 않습니다.

## 배포

GitHub Pages 배포 시 `Settings → Pages → Deploy from a branch → main / (root)`를 선택하면 공개 URL로 접근할 수 있습니다.
