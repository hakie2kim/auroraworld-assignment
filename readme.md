## 소개

<aside>
사용자가 자주 방문하는 웹사이트 링크를 저장하고, 카테고리별로 정리하여 관리할 수 있는 **워크 포털 웹 애플리케이션**을 개발합니다. 이를 통해 팀원 간 웹 링크를 공유하고, 읽기/쓰기 권한을 설정하여 협업 할 수 있도록 합니다.
</aside>

### 개발 환경

---

- FastAPI
- PostgreSQL

### 설치 패키지

---

```text
pip install annotated-types anyio cffi click colorama cryptography ecdsa fastapi fastapi-utils greenlet h11 httptools idna passlib psycopg2 pyasn1 pycparser pydantic pydantic_core python-dotenv python-jose python-multipart PyYAML rsa six sniffio SQLAlchemy starlette typing_extensions uvicorn watchfiles websockets
```

### 주요 기능

---

- **로그인**: 간편한 로그인 기능 제공
- **피드 관리**: 웹 링크 추가, 수정, 삭제 및 카테고리별 분류
- **공유 및 권한 관리**: 링크를 다른 사용자와 공유하고, 접근 권한(읽기/쓰기) 설정
- **검색 및 필터**: 키워드 검색 및 카테고리별 필터링

### 요구 사항

---

1. 사용자는 아이디와 비밀번호를 입력하여 회원 가입 할 수 있습니다.
- [x] 입력한 아이디가 중복되지 않는지 검사해야 합니다.
- [x] 비밀번호는 안전하게 저장할 수 있도록 처리해야 합니다.
  - bcrypt를 사용: salt 해시 추가, brute-force attack 방지, 단방향 해시

2. 사용자는 회원가입 후, 로그인과 로그아웃을 할 수 있습니다.
- [x] 로그인: 로그인 시 항상 토큰 발급
- [x] 로그아웃: 토큰은 일회용으로 사용하게 함

3. 사용자는  로그인 후 아래의 기능을 사용할 수 있습니다.
    - [x] 웹 링크 필수 속성은 다음과 같습니다. 추가적인 필드가 필요하면 자유롭게 정의하세요.
        - id : 고유한 식별자
        - created_by : 생성한 사용자 아이디
        - name : 웹 링크 이름
        - url : 저장할 웹 사이트의 URL
        - category : 카테고리(개인 즐겨 찾기, 업무 활용 자료, 참고 자료, 교육 및 학습 자료 등)
    - [x] **웹 링크 등록**: 사용자는 새로운 웹 링크를 추가할 수 있습니다.
    - [x] **웹 링크 수정**: 사용자는 자신이 등록했거나 쓰기 권한을 가진 웹 링크 정보를 일부 수정할 수 있습니다.
    - [x] **웹 링크 삭제**: 사용자는 자신이 등록한 웹 링크를 삭제할 수 있습니다.
    - [x] **웹 링크 공유**:
        - 사용자는 자신의 웹 링크를 특정 사용자와 공유할 수 있습니다.
        - 공유된 사용자에게 읽기/쓰기 권한을 설정할 수 있어야 합니다.
    - [x] **검색 및 필터링**:
        - 이름 또는 카테고리로 검색할 수 있어야 합니다.
        - 이름 검색은 부분 일치(like 검색)를 지원해야 합니다.
        - (예: "React"를 검색하면 "React Docs", "React Tutorial" 등 포함된 모든 항목이 검색됨)

4. **보안 요구사항**:
    - [x] 로그인하지 않은 사용자는 웹 링크 관련 API를 사용할 수 없어야 합니다.
      - /register, /token을 제외한 엔드포인트에 `current_user: User = Depends(get_current_user)` 추가
    - [x] 인증이 필요한 API 요청은 반드시 인가(Authorization) 처리를 해야 합니다.
      - 웹 링크 수정, 삭제, 공유에 인가 처리

### 구현

---

- [x] 데이터베이스 테이블 정의(DDL) 파일을 프로젝트 최상위 디렉토리에 포함해주세요.
- [x] JWT 토큰 기반 인증 방식을 사용하여 사용자 인증을 구현해주세요.