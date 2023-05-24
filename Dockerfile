##환경변수 지정 기본값을 3.9로 지정
ARG VARIANT=3.9

#파이썬 베이스 이미지를 사용하여 새로운 도커 이미지 생성
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

#환경변수 설정 및 Java 개발환경의 설치 경로 지정
ENV JAVA_HOME /usr/lib/jvm/java-1.7-openjdk/jre

#apt 업데이트, java 개발 키트 설치 및 git 설치 curl은 웹통신이나 파일전송에 사용
RUN apt-get update && apt-get install -y g++ default-jdk curl git

#파일에서 도커 이미지로 파일을 복사
ADD ./requirements.txt /tmp/requirements.txt

#파이썬 패키지 설치
RUN pip install --upgrade -r /tmp/requirements.txt

#유비콘 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

