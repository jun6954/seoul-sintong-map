# 서울 신속통합기획 선정구역 지도

서울시 신속통합기획·일반 정비사업을 네이버 지도에서 확인하는 정적 웹사이트입니다.

## 제공 기능

- 신속통합기획·일반 정비사업·중복 사업장 3개 레이어 필터
- 구역 면적에 비례한 원형 마커·공식 사업 경계 폴리곤·상세 정보 패널
- 도로명·지번 검색과 사업지 주소 자동완성
- 겹치는 사업지 선택 메뉴와 지도/리스트 보기
- 전용 비밀 링크 기반 즐겨찾기 동기화(로그인 불필요)
- 모바일·태블릿·데스크톱 반응형 레이아웃
- 서울시 공식 목록을 매일 동기화하는 GitHub Actions 배치

## 실행 방법

`index.html`을 브라우저에서 열거나 정적 웹 서버로 제공하면 됩니다. 네이버 지도, Supabase, 서울시 위치도 이미지는 인터넷 연결이 필요합니다.

## 데이터와 한계

신속통합기획 데이터는 [서울시 정비사업 정보몽땅](https://cleanup.seoul.go.kr/cleanup/view/publicIntgrPlanArea.do), 일반 정비사업 데이터는 [사업장검색](https://cleanup.seoul.go.kr/cleanup/bsnssttus/lscrMainIndx.do)에서 수집합니다. 일반 정비사업은 서울시 도시공간포털 지도 레코드가 있는 경우에만 공식 도형의 중심점을 지도에 표시합니다. 지도 레코드가 없는 사업장은 임의 좌표로 표시하지 않습니다.

## 자동 동기화와 알림

GitHub Actions는 매일 05:15(KST)에 일반 정비사업 목록을 수집하고 변경 시 Pages를 갱신합니다. 텔레그램 알림은 기본적으로 꺼져 있으며, 재개하려면 저장소 Actions Variable `TELEGRAM_NOTIFICATIONS_ENABLED`를 `true`로 설정하고 `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` Secrets를 유지하면 됩니다.

## 즐겨찾기 Supabase 설정

1. Supabase Dashboard의 **SQL Editor**에서 [`supabase/migrations/20260726_create_favorites.sql`](supabase/migrations/20260726_create_favorites.sql) 전체를 실행합니다.
2. **Edge Functions**에서 `shared-favorites` 함수를 생성한 뒤 [`supabase/functions/shared-favorites/index.ts`](supabase/functions/shared-favorites/index.ts)의 내용을 배포합니다. `supabase/config.toml`의 설정처럼 JWT 검증은 끕니다.
3. **Edge Function Secrets**에 `FAVORITES_SHARE_SECRET`을 등록합니다. 이 값은 전용 링크의 `#favorites=` 뒤 값과 반드시 같아야 합니다.
4. 전용 링크를 아내분의 기기에만 전달합니다. 예: `https://jun6954.github.io/seoul-sintong-map/#favorites=<FAVORITES_SHARE_SECRET>`

즐겨찾기 테이블은 RLS와 권한 회수로 브라우저의 데이터 API에서 완전히 차단됩니다. Edge Function 내부의 비밀 키가 전용 링크 키를 검증한 뒤에만 읽고 쓰므로, secret/service_role 키는 브라우저 코드에 포함되지 않습니다. 전용 링크를 아는 사람은 즐겨찾기를 바꿀 수 있으므로 비밀번호처럼 보관해야 합니다.

## 네이버 외부 주소 검색 설정

외부 도로명·지번 주소 검색은 [`supabase/functions/naver-geocode/index.ts`](supabase/functions/naver-geocode/index.ts) Edge Function을 통해 호출합니다. Supabase **Edge Function Secrets**에 아래 두 값을 저장한 뒤 `naver-geocode` 함수를 배포합니다.

- `NAVER_MAPS_CLIENT_ID`
- `NAVER_MAPS_CLIENT_SECRET`

브라우저에는 Client Secret을 포함하지 않습니다. 함수는 신규 Maps VPC Geocoding URL `https://maps.apigw.ntruss.com/map-geocode/v2/geocode`만 호출합니다.

## 배포

GitHub Pages 배포 시 `Settings → Pages → Deploy from a branch → main / (root)`를 선택하면 공개 URL로 접근할 수 있습니다.
