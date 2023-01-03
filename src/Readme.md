# Instagram Crawler 

해당 수집기로 수집할 수 있는 데이터 목록입니다.
- 유저의 팔로워 리스트 목록 - `crawler.py`

---
## 필수 설치 항목
1. [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/)를 다운로드 하고 src 폴더에 넣어주세요:  
  `./instagrm_crawler/src/chromedriver`
2. Selenium을 설치해주세요:   
  `pip3 install selenium`

---
## 크롤러

```
인자:  
  -id ID, --insta_id ID
                        instagram ID  
  -pw PASSWORD, --insta_pw PASSWORD 
                        instagram PASSWORD   
  -n NUMBER, --number NUMBER  
                        number of follower list 
```

## 예시

`python3 process.py -id mooonyakkk -pw akdlsld0302@ -n 300`

1. `id`, `pw`는 필수 입력 인자로 수집할 때 꼭 입력해야합니다. 
2. `-n`, `--number`으로 게시물 수를 지정하지 않으면, 기본적으로 100개의 팔로워 목록을 수집합니다.

데이터 형식:
![screen shot 2018-10-11 at 2 33 09 pm](https://user-images.githubusercontent.com/3991678/46835356-cd521d80-cd62-11e8-9bb1-888bc32af484.png)
