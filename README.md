# 🥇 두부두부 LOTTE PROJECT
: 롯데 직원 - 롯데 취준생 소통 창구

## 🔨 개발 규칙
### 🔒 Django
: 가상 환경 ```.gitignore```로 두고 각자 따로 사용하기
> 디폴트로 myvenv 적어뒀으니까 각자 가상 환경 이름 ```.gitignore```에 추가하기

### 🔒 DB
: ```db.sqlite3```를 ```.gitignore```로 두고 pull 받을 때 마다 명령어 입력해 업데이트하기
> DB 꼬임 방지
```
python manage.py makemigrations
python manage.py migrate
```

### 🔑 COMMIT MESSAGE
```
[본인이름] | 한 작업
ex) [종명] | 게시글 상세 페이지 수정
```

### 🔓 FE + BE
: 따로 레포를 파서 작업 후 합쳐잉