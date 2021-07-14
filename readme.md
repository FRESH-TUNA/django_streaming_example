# Cloudfront signed cookie를 활용한 회원전용 동영상 서비스 구축

## 프로젝트 개요
cloudfront는 edge location을 통한 컨텐츠의 빠른 다운로드, 업로드를 지원하는 서비스이다. 이외에도 signed cookie, signed url을 통해 허가된 사용자들에게만 컨텐츠를 제공하는 서비스를 구축할수 있다. 이번 시나리오에서 간단한 비디오 스트리밍 어플리케이션과 cloudfront를 사용하여 회원전용 동영상 서비스를 구축해보고자 한다.

## 블로그 주소
[https://lunacircle4.github.io/infra/2021/07/07/lambda-django/](https://lunacircle4.github.io/infra/2021/07/07/lambda-django/)<br/>

## 인프라 구조도
![Image Alt 텍스트](/scenario_6.png)

## cloudfront 설정 관련 코드
### cloudfront cookie 생성 로직
[<a href="/auth/services/cloudfront.py">클릭</a>]
### 컨트롤러
[<a href="/auth/views.py">클릭</a>]