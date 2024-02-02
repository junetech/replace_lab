#!/bin/bash
LOG_FILE="run_record.log"
exec 3>&1 1>>"${LOG_FILE}" 2>&1

StartTime=$(date +%s)    # 종료 시간 기록
echo "명령 시작 시각: $(date -d @$StartTime)" | tee /dev/fd/3

# 여기에 실행할 명령어를 작성하세요.
replace < bigblue1.tcl

EndTime=$(date +%s)    # 종료 시간 기록
echo "명령 종료 시각: $(date -d @$EndTime)" | tee /dev/fd/3

# 실행 시간 계산
Duration=$((EndTime - StartTime))

# 터미널 출력을 로그 파일에 추가
echo "명령 소요 시간: $Duration 초" | tee /dev/fd/3


StartTime=$(date +%s)    # 종료 시간 기록
echo "명령 시작 시각: $(date -d @$StartTime)" | tee /dev/fd/3

# 여기에 실행할 명령어를 작성하세요.
replace < bigblue2.tcl

EndTime=$(date +%s)    # 종료 시간 기록
echo "명령 종료 시각: $(date -d @$EndTime)" | tee /dev/fd/3

# 실행 시간 계산
Duration=$((EndTime - StartTime))

# 터미널 출력을 로그 파일에 추가
echo "명령 소요 시간: $Duration 초" | tee /dev/fd/3


StartTime=$(date +%s)    # 종료 시간 기록
echo "명령 시작 시각: $(date -d @$StartTime)" | tee /dev/fd/3

# 여기에 실행할 명령어를 작성하세요.
replace < adaptec4.tcl

EndTime=$(date +%s)    # 종료 시간 기록
echo "명령 종료 시각: $(date -d @$EndTime)" | tee /dev/fd/3

# 실행 시간 계산
Duration=$((EndTime - StartTime))

# 터미널 출력을 로그 파일에 추가
echo "명령 소요 시간: $Duration 초" | tee /dev/fd/3
