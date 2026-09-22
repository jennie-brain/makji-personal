# makji-personal 배포 메모

이 폴더는 `maybeaj/MakjiStock`의 화면 및 애플리케이션 소스를 복사한 독립 Vercel 프로젝트입니다. Vercel 프로젝트의 Root Directory를 `makji-personal`로 지정합니다.

## 현재 배포 범위

- `/market`, `/me`를 비롯한 화면과 클라이언트 동작은 원본 소스를 사용합니다.
- 원본 Supabase, Cafe24, 네이버, 한국은행 계정의 비밀값은 이 저장소에 포함하지 않습니다. 환경변수를 연결하기 전에는 실시간 가격, 잠금, 예측, 할인코드 발급이 원본 운영 서비스와 동일하게 동작하지 않습니다.
- `vercel.json`의 자동 가격 갱신 크론은 복사본에서 비활성화했습니다. 원본과 같은 운영 시스템에 중복으로 가격 변경·쿠폰 발급 요청을 보내지 않도록 하기 위한 설정입니다. 별도 데이터베이스와 상점 연동을 구성한 뒤에만 크론을 활성화합니다.

필요한 서버 설정은 [.env.example](.env.example)을 참조합니다. 비밀값은 Git에 추가하지 말고 Vercel 프로젝트의 Environment Variables에 입력합니다.
