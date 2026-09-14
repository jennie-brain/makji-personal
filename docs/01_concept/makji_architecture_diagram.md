# MAKJI STOCK 시스템 아키텍처

기획안 '7-2. 시스템 구성안'을 바탕으로 시각화한 서비스 아키텍처 및 데이터 흐름도입니다.

```mermaid
flowchart TD
    %% 사용자 영역
    subgraph Client ["사용자 환경 (Client)"]
        UI["MAKJI STOCK 화면\n(시세/상품정보/예측)"]
    end

    %% 막지 스톡 백엔드 영역
    subgraph Backend ["MAKJI STOCK 팀 서버 (Backend)"]
        Server["메인 서버\n(가격 계산/예측 판정/쿠폰 배정)"]
        Scheduler["스케줄러\n(매일 오전 8:50 데이터 수집/계산)"]
        DB[(데이터베이스\n- 날짜별 시세\n- 참여 기록\n- 쿠폰/행동 기록)]
    end

    %% 외부 데이터 API 영역
    subgraph External ["외부 데이터 API"]
        Naver["NAVER API HUB\n(상품별 검색트렌드)"]
        KEXIM["한국수출입은행 API\n(USD/KRW 환율)"]
    end

    %% 카페24 (자사몰) 영역
    subgraph Cafe24_Mall ["막지 자사몰 (Cafe24)"]
        C24_API["Cafe24 API\n(상품가/쿠폰 연동)"]
        C24_Web["자사몰 결제/주문 화면"]
    end

    %% 관계 및 데이터 흐름 연결
    UI -- "오늘 빵값 확인 / 예측 참여" --> Server
    UI -- "상품 구매 이동 (URL)" --> C24_Web
    
    Scheduler -- "검색지수 수집" --> Naver
    Scheduler -- "환율 데이터 수집" --> KEXIM
    Scheduler -- "수집 데이터 전달 및 트리거" --> Server
    
    Server -- "데이터 읽기/쓰기" --> DB
    Server -- "최종 가격/쿠폰 동기화" --> C24_API
    
    C24_API -. "적용 결과" .-> C24_Web
```

### 💡 주요 아키텍처 설계 포인트
1. **스케줄러 선제 처리**: 오전 9시 트래픽 스파이크에 대비해 스케줄러가 외부 API 연동 및 복잡한 가격 계산 로직을 사전에 수행하고 DB에 캐싱합니다.
2. **독립적인 서버 운용**: 자사몰(Cafe24)에 부하를 주지 않고 참여 및 가격 계산은 '팀 서버'에서 100% 독립 처리하며, 결과값만 Cafe24 API로 연동(Sync)합니다.
3. **간결한 유입 동선**: 사용자는 별도의 가입 없이 MAKJI STOCK에서 확인하고, 실제 결제 시퀀스만 자사몰로 위임하여 결제 전환율을 방어합니다.
