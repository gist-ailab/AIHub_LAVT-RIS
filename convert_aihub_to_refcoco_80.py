import os
import json
import pickle
from datetime import datetime
import glob
import shutil
import random
import logging
from tqdm import tqdm
import csv


MANUFACT_CATEGORIES = [
    {"supercategory": "도구 및 장비", "id": 1, "name": "가스디퓨저"},
    {"supercategory": "도구 및 장비", "id": 2, "name": "가스토치"},
    {"supercategory": "도구 및 장비", "id": 3, "name": "간극 게이지"},
    {"supercategory": "도구 및 장비", "id": 4, "name": "구리스건"},
    {"supercategory": "도구 및 장비", "id": 5, "name": "그랩훅"},
    {"supercategory": "도구 및 장비", "id": 6, "name": "기어풀러"},
    {"supercategory": "도구 및 장비", "id": 7, "name": "스크레퍼(끌->스크레퍼로 명칭 변경)"},
    {"supercategory": "도구 및 장비", "id": 8, "name": "납흡입기"},
    {"supercategory": "도구 및 장비", "id": 9, "name": "니퍼"},
    {"supercategory": "도구 및 장비", "id": 10, "name": "대패"},
    {"supercategory": "도구 및 장비", "id": 11, "name": "덕트테이프"},
    {"supercategory": "도구 및 장비", "id": 12, "name": "도르레"},
    {"supercategory": "도구 및 장비", "id": 13, "name": "도배칼"},
    {"supercategory": "도구 및 장비", "id": 14, "name": "드라이버"},
    {"supercategory": "도구 및 장비", "id": 15, "name": "드릴 지그"},
    {"supercategory": "도구 및 장비", "id": 16, "name": "레이저 거리 측정기"},
    {"supercategory": "도구 및 장비", "id": 17, "name": "리베터기"},
    {"supercategory": "도구 및 장비", "id": 18, "name": "만력기"},
    {"supercategory": "도구 및 장비", "id": 19, "name": "망치"},
    {"supercategory": "도구 및 장비", "id": 20, "name": "멀티미터"},
    {"supercategory": "도구 및 장비", "id": 21, "name": "몽키 스패너"},
    {"supercategory": "도구 및 장비", "id": 22, "name": "미장칼"},
    {"supercategory": "도구 및 장비", "id": 23, "name": "바이스그립"},
    {"supercategory": "도구 및 장비", "id": 24, "name": "밴드쏘"},
    {"supercategory": "도구 및 장비", "id": 25, "name": "버니어 캘리퍼스"},
    {"supercategory": "도구 및 장비", "id": 26, "name": "볼트 커터"},
    {"supercategory": "도구 및 장비", "id": 27, "name": "분도기"},
    {"supercategory": "도구 및 장비", "id": 28, "name": "분사기"},
    {"supercategory": "도구 및 장비", "id": 29, "name": "브러쉬"},
    {"supercategory": "도구 및 장비", "id": 30, "name": "삼각자"},
    {"supercategory": "도구 및 장비", "id": 31, "name": "삽"},
    {"supercategory": "도구 및 장비", "id": 32, "name": "소음계"},
    {"supercategory": "도구 및 장비", "id": 33, "name": "수평계"},
    {"supercategory": "도구 및 장비", "id": 34, "name": "스크류잭"},
    {"supercategory": "도구 및 장비", "id": 35, "name": "스트립퍼"},
    {"supercategory": "도구 및 장비", "id": 36, "name": "스패너"},
    {"supercategory": "도구 및 장비", "id": 37, "name": "슬링훅"},
    {"supercategory": "도구 및 장비", "id": 38, "name": "시멘트교반기"},
    {"supercategory": "도구 및 장비", "id": 39, "name": "앵글 그라인더"},
    {"supercategory": "도구 및 장비", "id": 40, "name": "양구스패너"},
    {"supercategory": "도구 및 장비", "id": 41, "name": "연무기"},
    {"supercategory": "도구 및 장비", "id": 42, "name": "열풍기"},
    {"supercategory": "도구 및 장비", "id": 43, "name": "오링풀러"},
    {"supercategory": "도구 및 장비", "id": 44, "name": "용접홀더"},
    {"supercategory": "도구 및 장비", "id": 45, "name": "유리칼"},
    {"supercategory": "도구 및 장비", "id": 46, "name": "유리흡착기"},
    {"supercategory": "도구 및 장비", "id": 47, "name": "유압절단기"},
    {"supercategory": "도구 및 장비", "id": 48, "name": "육각 소켓 렌치"},
    {"supercategory": "도구 및 장비", "id": 49, "name": "육각렌치"},
    {"supercategory": "도구 및 장비", "id": 50, "name": "인두기"},
    {"supercategory": "도구 및 장비", "id": 51, "name": "임팩트랜치"},
    {"supercategory": "도구 및 장비", "id": 52, "name": "적외선온도계"},
    {"supercategory": "도구 및 장비", "id": 53, "name": "전동드릴"},
    {"supercategory": "도구 및 장비", "id": 54, "name": "절곡집게"},
    {"supercategory": "도구 및 장비", "id": 55, "name": "접이톱"},
    {"supercategory": "도구 및 장비", "id": 56, "name": "접지봉커넥터"},
    {"supercategory": "도구 및 장비", "id": 57, "name": "줄톱"},
    {"supercategory": "도구 및 장비", "id": 58, "name": "직쏘"},
    {"supercategory": "도구 및 장비", "id": 59, "name": "체인톱"},
    {"supercategory": "도구 및 장비", "id": 60, "name": "콤비네이션스퀘어"},
    {"supercategory": "도구 및 장비", "id": 61, "name": "타일절단기"},
    {"supercategory": "도구 및 장비", "id": 62, "name": "타카"},
    {"supercategory": "도구 및 장비", "id": 63, "name": "테이퍼게이지"},
    {"supercategory": "도구 및 장비", "id": 64, "name": "토크렌치"},
    {"supercategory": "도구 및 장비", "id": 65, "name": "톱"},
    {"supercategory": "도구 및 장비", "id": 66, "name": "파이프랜치"},
    {"supercategory": "도구 및 장비", "id": 67, "name": "파이프밴더"},
    {"supercategory": "도구 및 장비", "id": 68, "name": "파이프커터"},
    {"supercategory": "도구 및 장비", "id": 69, "name": "파이프확관기"},
    {"supercategory": "도구 및 장비", "id": 70, "name": "팜맥"},
    {"supercategory": "도구 및 장비", "id": 71, "name": "펜치"},
    {"supercategory": "도구 및 장비", "id": 72, "name": "프라이바"},
    {"supercategory": "도구 및 장비", "id": 73, "name": "플라이어"},
    {"supercategory": "도구 및 장비", "id": 74, "name": "플라이어 첼라"},
     {"supercategory": "도구 및 장비", "id": 75, "name": "핀게이지"},
    {"supercategory": "도구 및 장비", "id": 76, "name": "하이트게이지"},
    {"supercategory": "도구 및 장비", "id": 77, "name": "함마렌치"},
    {"supercategory": "도구 및 장비", "id": 78, "name": "항공가위"},
    {"supercategory": "도구 및 장비", "id": 79, "name": "도끼"},
    {"supercategory": "도구 및 장비", "id": 80, "name": "훅스패너"},
    {"supercategory": "도구 및 장비", "id": 81, "name": "힌지핸들"},
    {"supercategory": "도구 및 장비", "id": 82, "name": "T핸들"},
    {"supercategory": "자재 및 부품", "id": 83, "name": "45도 엘보 파이프"},
    {"supercategory": "자재 및 부품", "id": 84, "name": "90도 엘보 파이프"},
    {"supercategory": "자재 및 부품", "id": 85, "name": "각재"},
    {"supercategory": "자재 및 부품", "id": 86, "name": "경첩"},
    {"supercategory": "자재 및 부품", "id": 87, "name": "고압호스"},
    {"supercategory": "자재 및 부품", "id": 88, "name": "8자브라켓"},
    {"supercategory": "자재 및 부품", "id": 89, "name": "다목적가위"},
    {"supercategory": "자재 및 부품", "id": 90, "name": "도어 스토퍼"},
    {"supercategory": "자재 및 부품", "id": 91, "name": "도장용마스킹테이프"},
    {"supercategory": "자재 및 부품", "id": 92, "name": "라벨용지"},
    {"supercategory": "자재 및 부품", "id": 93, "name": "롤러 베어링"},
    {"supercategory": "자재 및 부품", "id": 94, "name": "금형스프링"},
    {"supercategory": "자재 및 부품", "id": 95, "name": "매직케이블"},
    {"supercategory": "자재 및 부품", "id": 96, "name": "바 클램프"},
    {"supercategory": "자재 및 부품", "id": 97, "name": "T조인트"},
    {"supercategory": "자재 및 부품", "id": 98, "name": "방청제"},
    {"supercategory": "자재 및 부품", "id": 99, "name": "밸브"},
    {"supercategory": "자재 및 부품", "id": 100, "name": "베벨기어"},
    {"supercategory": "자재 및 부품", "id": 101, "name": "베어링 플레이트"},
    {"supercategory": "자재 및 부품", "id": 102, "name": "캐스터바퀴"},
    {"supercategory": "자재 및 부품", "id": 103, "name": "보드마카"},
    {"supercategory": "자재 및 부품", "id": 104, "name": "볼베어링"},
    {"supercategory": "자재 및 부품", "id": 105, "name": "볼스크류"},
    {"supercategory": "자재 및 부품", "id": 106, "name": "볼트"},
    {"supercategory": "자재 및 부품", "id": 107, "name": "브라켓"},
    {"supercategory": "자재 및 부품", "id": 108, "name": "샤프트"},
    {"supercategory": "자재 및 부품", "id": 109, "name": "샤프트 홀더"},
    {"supercategory": "자재 및 부품", "id": 110, "name": "유량계"},
    {"supercategory": "자재 및 부품", "id": 111, "name": "스파이러 스프링"},
    {"supercategory": "자재 및 부품", "id": 112, "name": "슬라이드 레일"},
    {"supercategory": "자재 및 부품", "id": 113, "name": "실리콘실란트"},
    {"supercategory": "자재 및 부품", "id": 114, "name": "십자형 접속 파이프"},
    {"supercategory": "자재 및 부품", "id": 115, "name": "액체풀"},
    {"supercategory": "자재 및 부품", "id": 116, "name": "연마석"},
    {"supercategory": "자재 및 부품", "id": 117, "name": "용접자석"},
    {"supercategory": "자재 및 부품", "id": 118, "name": "컴프레셔 안전핀"},
    {"supercategory": "자재 및 부품", "id": 119, "name": "웜기어"},
    {"supercategory": "자재 및 부품", "id": 120, "name": "전구"},
    {"supercategory": "자재 및 부품", "id": 121, "name": "전선관"},
    {"supercategory": "자재 및 부품", "id": 122, "name": "절연테이프"},
    {"supercategory": "자재 및 부품", "id": 123, "name": "접착제"},
    {"supercategory": "자재 및 부품", "id": 124, "name": "에어레귤레이터"},
    {"supercategory": "자재 및 부품", "id": 125, "name": "축전기"},
    {"supercategory": "자재 및 부품", "id": 126, "name": "컷쏘날"},
    {"supercategory": "자재 및 부품", "id": 127, "name": "케이블"},
    {"supercategory": "자재 및 부품", "id": 128, "name": "코너비드"},
    {"supercategory": "자재 및 부품", "id": 129, "name": "코일 스프링"},
    {"supercategory": "자재 및 부품", "id": 130, "name": "퀵클램프"},
    {"supercategory": "자재 및 부품", "id": 131, "name": "타일"},
    {"supercategory": "자재 및 부품", "id": 132, "name": "파스너"},
    {"supercategory": "자재 및 부품", "id": 133, "name": "펀치"},
    {"supercategory": "자재 및 부품", "id": 134, "name": "평기어"},
    {"supercategory": "자재 및 부품", "id": 135, "name": "포스트잇"},
    {"supercategory": "자재 및 부품", "id": 136, "name": "주사용 납"},
    {"supercategory": "자재 및 부품", "id": 137, "name": "형광등 휴즈"},
    {"supercategory": "자재 및 부품", "id": 138, "name": "헬리컬 기어(-> 배선 차단기)"},
    {"supercategory": "자재 및 부품", "id": 139, "name": "호스"},
    {"supercategory": "자재 및 부품", "id": 140, "name": "C형클램프"},
    {"supercategory": "자재 및 부품", "id": 141, "name": "dc모터"},
    {"supercategory": "자재 및 부품", "id": 142, "name": "L형클램프"},
    {"supercategory": "자재 및 부품", "id": 143, "name": "T형 접속 파이프"},
    {"supercategory": "자재 및 부품", "id": 144, "name": "usb-c 파워 어댑터"},
    {"supercategory": "자재 및 부품", "id": 145, "name": "Y형 접속 파이프"},
    {"supercategory": "보관 및 포장", "id": 146, "name": "가위"},
    {"supercategory": "보관 및 포장", "id": 147, "name": "글루건"},
    {"supercategory": "보관 및 포장", "id": 148, "name": "단프라 박스"},
    {"supercategory": "보관 및 포장", "id": 149, "name": "라벨프린터"},
    {"supercategory": "보관 및 포장", "id": 150, "name": "문서재단기"},
    {"supercategory": "보관 및 포장", "id": 151, "name": "박스 테이프"},
    {"supercategory": "보관 및 포장", "id": 152, "name": "노끈"},
    {"supercategory": "보관 및 포장", "id": 153, "name": "스티로폼 박스"},
    {"supercategory": "보관 및 포장", "id": 154, "name": "실리카겔"},
    {"supercategory": "보관 및 포장", "id": 155, "name": "실리콘건"},
    {"supercategory": "보관 및 포장", "id": 156, "name": "아이스팩"},
    {"supercategory": "보관 및 포장", "id": 157, "name": "에어캡"},
    {"supercategory": "보관 및 포장", "id": 158, "name": "연필꽂이"},
    {"supercategory": "보관 및 포장", "id": 159, "name": "인덱스카드"},
    {"supercategory": "보관 및 포장", "id": 160, "name": "제침기"},
    {"supercategory": "보관 및 포장", "id": 161, "name": "종이 박스"},
    {"supercategory": "보관 및 포장", "id": 162, "name": "종이 완충제"},
    {"supercategory": "보관 및 포장", "id": 163, "name": "줄자"},
    {"supercategory": "보관 및 포장", "id": 164, "name": "커터칼"},
    {"supercategory": "보관 및 포장", "id": 165, "name": "테이프커터"},
    {"supercategory": "보관 및 포장", "id": 166, "name": "파일"},
    {"supercategory": "보관 및 포장", "id": 167, "name": "핸드 홀 펀"},
    {"supercategory": "안전 및 보호", "id": 168, "name": "교통삼각대"},
    {"supercategory": "안전 및 보호", "id": 169, "name": "귀덮개"},
    {"supercategory": "안전 및 보호", "id": 170, "name": "귀마개"},
    {"supercategory": "안전 및 보호", "id": 171, "name": "나침반"},
    {"supercategory": "안전 및 보호", "id": 172, "name": "메가폰"},
    {"supercategory": "안전 및 보호", "id": 173, "name": "방독마스크"},
    {"supercategory": "안전 및 보호", "id": 174, "name": "방진마스크"},
    {"supercategory": "안전 및 보호", "id": 175, "name": "보안경"},
    {"supercategory": "안전 및 보호", "id": 176, "name": "보안면"},
    {"supercategory": "안전 및 보호", "id": 177, "name": "소화기"},
    {"supercategory": "안전 및 보호", "id": 178, "name": "라바콘"},
    {"supercategory": "안전 및 보호", "id": 179, "name": "스톱워치"},
    {"supercategory": "안전 및 보호", "id": 180, "name": "신호봉"},
    {"supercategory": "안전 및 보호", "id": 181, "name": "안전모"},
    {"supercategory": "안전 및 보호", "id": 182, "name": "안전화"},
    {"supercategory": "안전 및 보호", "id": 183, "name": "작업등"},
    {"supercategory": "안전 및 보호", "id": 184, "name": "작업용우의"},
    {"supercategory": "안전 및 보호", "id": 185, "name": "장갑"},
    {"supercategory": "안전 및 보호", "id": 186, "name": "헤드랜턴"},
    {"supercategory": "기타 물품", "id": 187, "name": "도구 및 장비함"},
    {"supercategory": "기타 물품", "id": 188, "name": "멀티탭"},
    {"supercategory": "기타 물품", "id": 189, "name": "무전기"},
    {"supercategory": "기타 물품", "id": 190, "name": "바코드스캐너"},
    {"supercategory": "기타 물품", "id": 191, "name": "쌍안경"},
    {"supercategory": "기타 물품", "id": 192, "name": "자물쇠"},
    {"supercategory": "기타 물품", "id": 193, "name": "저울"},
    {"supercategory": "기타 물품", "id": 194, "name": "전선거치대"},
    {"supercategory": "기타 물품", "id": 195, "name": "페인트롤러"},
    {"supercategory": "기타 물품", "id": 196, "name": "페인트붓"},
    {"supercategory": "기타 물품", "id": 197, "name": "플라스틱 바구니"},
    {"supercategory": "기타 물품", "id": 198, "name": "헤드셋"},
    {"supercategory": "기타 물품", "id": 199, "name": "호루라기"},
    {"supercategory": "기타 물품", "id": 200, "name": "확대경"}
]

INDOOR_CATEGORIES = [
    {"supercategory": "생활용품", "id": 1, "name": "갑티슈"},
    {"supercategory": "생활용품", "id": 2, "name": "건전지"},
    {"supercategory": "생활용품", "id": 3, "name": "기저귀"},
    {"supercategory": "생활용품", "id": 4, "name": "노트북"},
    {"supercategory": "생활용품", "id": 5, "name": "눈썹칼"},
    {"supercategory": "생활용품", "id": 6, "name": "다리미"},
    {"supercategory": "생활용품", "id": 7, "name": "달력"},
    {"supercategory": "생활용품", "id": 8, "name": "도끼빗"},
    {"supercategory": "생활용품", "id": 9, "name": "두루마리 휴지"},
    {"supercategory": "생활용품", "id": 10, "name": "드라이어"},
    {"supercategory": "생활용품", "id": 11, "name": "딱풀"},
    {"supercategory": "생활용품", "id": 12, "name": "로션"},
    {"supercategory": "생활용품", "id": 13, "name": "면도기"},
    {"supercategory": "생활용품", "id": 14, "name": "면봉"},
    {"supercategory": "생활용품", "id": 15, "name": "모니터"},
    {"supercategory": "생활용품", "id": 16, "name": "물티슈"},
    {"supercategory": "생활용품", "id": 17, "name": "바가지"},
    {"supercategory": "생활용품", "id": 18, "name": "바구니"},
    {"supercategory": "생활용품", "id": 19, "name": "바리깡"},
    {"supercategory": "생활용품", "id": 20, "name": "반창고"},
    {"supercategory": "생활용품", "id": 21, "name": "베개"},
    {"supercategory": "생활용품", "id": 22, "name": "병따개"},
    {"supercategory": "생활용품", "id": 23, "name": "보조배터리"},
    {"supercategory": "생활용품", "id": 24, "name": "분무기"},
    {"supercategory": "생활용품", "id": 25, "name": "브러쉬빗"},
    {"supercategory": "생활용품", "id": 26, "name": "블루투스 이어폰"},
    {"supercategory": "생활용품", "id": 27, "name": "빗자루"},
    {"supercategory": "생활용품", "id": 28, "name": "빨래집게"},
    {"supercategory": "생활용품", "id": 29, "name": "색연필"},
    {"supercategory": "생활용품", "id": 30, "name": "샤프"},
    {"supercategory": "생활용품", "id": 31, "name": "손톱깎이"},
    {"supercategory": "생활용품", "id": 32, "name": "스마트폰"},
    {"supercategory": "생활용품", "id": 33, "name": "스케치북"},
    {"supercategory": "생활용품", "id": 34, "name": "스테이플러"},
    {"supercategory": "생활용품", "id": 35, "name": "스프레이 살충제"},
    {"supercategory": "생활용품", "id": 36, "name": "스피커"},
    {"supercategory": "생활용품", "id": 37, "name": "습기제거제"},
    {"supercategory": "생활용품", "id": 38, "name": "시계"},
    {"supercategory": "생활용품", "id": 39, "name": "쓰레받기"},
    {"supercategory": "생활용품", "id": 40, "name": "아령"},
    {"supercategory": "생활용품", "id": 41, "name": "연필"},
    {"supercategory": "생활용품", "id": 42, "name": "연필깎이"},
    {"supercategory": "생활용품", "id": 43, "name": "염색빗"},
    {"supercategory": "생활용품", "id": 44, "name": "옷걸이"},
    {"supercategory": "생활용품", "id": 45, "name": "전화기"},
    {"supercategory": "생활용품", "id": 46, "name": "지우개"},
    {"supercategory": "생활용품", "id": 47, "name": "책"},
    {"supercategory": "생활용품", "id": 48, "name": "청소기"},
    {"supercategory": "생활용품", "id": 49, "name": "청소솔"},
    {"supercategory": "생활용품", "id": 50, "name": "충전기"},
    {"supercategory": "생활용품", "id": 51, "name": "커피포트"},
    {"supercategory": "생활용품", "id": 52, "name": "크레파스"},
    {"supercategory": "생활용품", "id": 53, "name": "키보드"},
    {"supercategory": "생활용품", "id": 54, "name": "태블릿PC"},
    {"supercategory": "생활용품", "id": 55, "name": "테이프"},
    {"supercategory": "생활용품", "id": 56, "name": "헤드폰"},
    {"supercategory": "생활용품", "id": 57, "name": "헤어구르프"},
    {"supercategory": "생활용품", "id": 58, "name": "형광펜"},
    {"supercategory": "생활용품", "id": 59, "name": "화분"},
    {"supercategory": "식품", "id": 60, "name": "계란"},
    {"supercategory": "식품", "id": 61, "name": "고구마"},
    {"supercategory": "식품", "id": 62, "name": "고추"},
    {"supercategory": "식품", "id": 63, "name": "당근"},
    {"supercategory": "식품", "id": 64, "name": "도넛"},
    {"supercategory": "식품", "id": 65, "name": "딸기"},
    {"supercategory": "식품", "id": 66, "name": "레몬"},
    {"supercategory": "식품", "id": 67, "name": "멜론"},
    {"supercategory": "식품", "id": 68, "name": "바나나"},
    {"supercategory": "식품", "id": 69, "name": "박스과자"},
    {"supercategory": "식품", "id": 70, "name": "버섯"},
    {"supercategory": "식품", "id": 71, "name": "버터"},
    {"supercategory": "식품", "id": 72, "name": "복숭아"},
    {"supercategory": "식품", "id": 73, "name": "봉지과자"},
    {"supercategory": "식품", "id": 74, "name": "브로콜리"},
    {"supercategory": "식품", "id": 75, "name": "사과"},
    {"supercategory": "식품", "id": 76, "name": "샌드위치"},
    {"supercategory": "식품", "id": 77, "name": "소시지"},
    {"supercategory": "식품", "id": 78, "name": "아보카도"},
    {"supercategory": "식품", "id": 79, "name": "양파"},
    {"supercategory": "식품", "id": 80, "name": "오렌지"},
    {"supercategory": "식품", "id": 81, "name": "요거트"},
    {"supercategory": "식품", "id": 82, "name": "우유"},
    {"supercategory": "식품", "id": 83, "name": "음료캔"},
    {"supercategory": "식품", "id": 84, "name": "참치캔"},
    {"supercategory": "식품", "id": 85, "name": "컵라면"},
    {"supercategory": "식품", "id": 86, "name": "케쳡"},
    {"supercategory": "식품", "id": 87, "name": "쿠키"},
    {"supercategory": "식품", "id": 88, "name": "크래커"},
    {"supercategory": "식품", "id": 89, "name": "크림치즈"},
    {"supercategory": "식품", "id": 90, "name": "통조림햄"},
    {"supercategory": "식품", "id": 91, "name": "파"},
    {"supercategory": "식품", "id": 92, "name": "팩주스"},
    {"supercategory": "식품", "id": 93, "name": "포도"},
    {"supercategory": "식품", "id": 94, "name": "햄버거"},
    {"supercategory": "식품", "id": 95, "name": "호박"},
    {"supercategory": "주방용품", "id": 96, "name": "감자칼"},
    {"supercategory": "주방용품", "id": 97, "name": "거품기"},
    {"supercategory": "주방용품", "id": 98, "name": "계량스푼"},
    {"supercategory": "주방용품", "id": 99, "name": "계량컵"},
    {"supercategory": "주방용품", "id": 100, "name": "국자"},
    {"supercategory": "주방용품", "id": 101, "name": "나이프"},
    {"supercategory": "주방용품", "id": 102, "name": "냄비"},
    {"supercategory": "주방용품", "id": 103, "name": "대접"},
    {"supercategory": "주방용품", "id": 104, "name": "도마"},
    {"supercategory": "주방용품", "id": 105, "name": "뒤집개"},
    {"supercategory": "주방용품", "id": 106, "name": "뚝배기"},
    {"supercategory": "주방용품", "id": 107, "name": "물통"},
    {"supercategory": "주방용품", "id": 108, "name": "병솔"},
    {"supercategory": "주방용품", "id": 109, "name": "빵칼"},
    {"supercategory": "주방용품", "id": 110, "name": "수세미"},
    {"supercategory": "주방용품", "id": 111, "name": "숟가락"},
    {"supercategory": "주방용품", "id": 112, "name": "스테인레스볼"},
    {"supercategory": "주방용품", "id": 113, "name": "식칼"},
    {"supercategory": "주방용품", "id": 114, "name": "식판"},
    {"supercategory": "주방용품", "id": 115, "name": "알루미늄 호일"},
    {"supercategory": "주방용품", "id": 116, "name": "어린이용 젓가락"},
    {"supercategory": "주방용품", "id": 117, "name": "얼음 트레이"},
    {"supercategory": "주방용품", "id": 118, "name": "와플기"},
    {"supercategory": "주방용품", "id": 119, "name": "쟁반"},
    {"supercategory": "주방용품", "id": 120, "name": "접시"},
    {"supercategory": "주방용품", "id": 121, "name": "젓가락"},
    {"supercategory": "주방용품", "id": 122, "name": "주걱"},
    {"supercategory": "주방용품", "id": 123, "name": "주방세제"},
    {"supercategory": "주방용품", "id": 124, "name": "주방장갑"},
    {"supercategory": "주방용품", "id": 125, "name": "도시락"},
    {"supercategory": "주방용품", "id": 126, "name": "집게"},
    {"supercategory": "주방용품", "id": 127, "name": "채칼"},
    {"supercategory": "주방용품", "id": 128, "name": "컵"},
    {"supercategory": "주방용품", "id": 129, "name": "키친타월"},
    {"supercategory": "주방용품", "id": 130, "name": "텀블러"},
    {"supercategory": "주방용품", "id": 131, "name": "토스터"},
    {"supercategory": "주방용품", "id": 132, "name": "포크"},
    {"supercategory": "주방용품", "id": 133, "name": "포크 스푼"},
    {"supercategory": "주방용품", "id": 134, "name": "후라이팬"},
    {"supercategory": "잡화", "id": 135, "name": "계산기"},
    {"supercategory": "잡화", "id": 136, "name": "고데기"},
    {"supercategory": "잡화", "id": 137, "name": "공"},
    {"supercategory": "잡화", "id": 138, "name": "글러브"},
    {"supercategory": "잡화", "id": 139, "name": "남성 구두"},
    {"supercategory": "잡화", "id": 140, "name": "폼롤러"},
    {"supercategory": "잡화", "id": 141, "name": "다트"},
    {"supercategory": "잡화", "id": 142, "name": "독서대"},
    {"supercategory": "잡화", "id": 143, "name": "돋보기"},
    {"supercategory": "잡화", "id": 144, "name": "라이터"},
    {"supercategory": "잡화", "id": 145, "name": "레고"},
    {"supercategory": "잡화", "id": 146, "name": "루빅 큐브"},
    {"supercategory": "잡화", "id": 147, "name": "리모컨"},
    {"supercategory": "잡화", "id": 148, "name": "마우스"},
    {"supercategory": "잡화", "id": 149, "name": "머리띠"},
    {"supercategory": "잡화", "id": 150, "name": "머리핀"},
    {"supercategory": "잡화", "id": 151, "name": "메이크업 브러쉬"},
    {"supercategory": "잡화", "id": 152, "name": "반지"},
    {"supercategory": "잡화", "id": 153, "name": "마사지볼"},
    {"supercategory": "잡화", "id": 154, "name": "볼링핀"},
    {"supercategory": "잡화", "id": 155, "name": "붕대"},
    {"supercategory": "잡화", "id": 156, "name": "선글라스"},
    {"supercategory": "잡화", "id": 157, "name": "손전등"},
    {"supercategory": "잡화", "id": 158, "name": "슬리퍼"},
    {"supercategory": "잡화", "id": 159, "name": "신발주걱"},
    {"supercategory": "잡화", "id": 160, "name": "안경"},
    {"supercategory": "잡화", "id": 161, "name": "액자"},
    {"supercategory": "잡화", "id": 162, "name": "야구헬멧"},
    {"supercategory": "잡화", "id": 163, "name": "여권"},
    {"supercategory": "잡화", "id": 164, "name": "여성 구두"},
    {"supercategory": "잡화", "id": 165, "name": "열쇠"},
    {"supercategory": "잡화", "id": 166, "name": "온도계"},
    {"supercategory": "잡화", "id": 167, "name": "우산"},
    {"supercategory": "잡화", "id": 168, "name": "운동화"},
    {"supercategory": "잡화", "id": 169, "name": "인형"},
    {"supercategory": "잡화", "id": 170, "name": "자동차장난감"},
    {"supercategory": "잡화", "id": 171, "name": "자석"},
    {"supercategory": "잡화", "id": 172, "name": "장화"},
    {"supercategory": "잡화", "id": 173, "name": "주사위"},
    {"supercategory": "잡화", "id": 174, "name": "주판기"},
    {"supercategory": "잡화", "id": 175, "name": "지갑"},
    {"supercategory": "잡화", "id": 176, "name": "체스판"},
    {"supercategory": "잡화", "id": 177, "name": "체온계"},
    {"supercategory": "잡화", "id": 178, "name": "카메라"},
    {"supercategory": "잡화", "id": 179, "name": "카메라렌즈"},
    {"supercategory": "잡화", "id": 180, "name": "컴퍼스"},
    {"supercategory": "잡화", "id": 181, "name": "크록스"},
    {"supercategory": "잡화", "id": 182, "name": "키링"},
    {"supercategory": "잡화", "id": 183, "name": "타이머"},
    {"supercategory": "잡화", "id": 184, "name": "탬버린"},
    {"supercategory": "잡화", "id": 185, "name": "테이프클리너"},
    {"supercategory": "잡화", "id": 186, "name": "피규어"},
    {"supercategory": "잡화", "id": 187, "name": "필통"},
    {"supercategory": "잡화", "id": 188, "name": "핸드백"},
    {"supercategory": "잡화", "id": 189, "name": "USB"},
    {"supercategory": "욕실용품", "id": 190, "name": "뚜러뻥"},
    {"supercategory": "욕실용품", "id": 191, "name": "비누"},
    {"supercategory": "욕실용품", "id": 192, "name": "비누받침"},
    {"supercategory": "욕실용품", "id": 193, "name": "샤워기"},
    {"supercategory": "욕실용품", "id": 194, "name": "욕실세정제"},
    {"supercategory": "욕실용품", "id": 195, "name": "샴푸"},
    {"supercategory": "욕실용품", "id": 196, "name": "세수대야"},
    {"supercategory": "욕실용품", "id": 197, "name": "스퀴지"},
    {"supercategory": "욕실용품", "id": 198, "name": "치실"},
    {"supercategory": "욕실용품", "id": 199, "name": "치약"},
    {"supercategory": "욕실용품", "id": 200, "name": "칫솔"}
]

# 20241019 synthetic data error list
# manufact_error_list = [902, 910, 923, 945, 1029, 1076, 1120, 1145, 1148, 1158, 1165, 1167, 1273, 1333, 1713, 1737, 1762, 1820, 1824, 1913, 1950, 2078, 2092, 2149, 2156, 2187, 2257, 2308, 2321, 2346, 2398, 2474, 2544, 2558, 2607, 2619, 2652, 2656, 2696, 3277, 3364, 3369, 3372, 3459, 3502, 3541, 3585, 3654, 3685, 4165, 4198, 4199, 4219, 4345, 4395, 4410, 4719, 4780, 4832, 5419, 5460, 5580, 5606, 5868, 5908, 5968, 5994, 6003, 6181, 6304, 6336, 6378, 6401, 6405, 6496, 6509, 6529, 6535, 6655, 6659, 6800, 6839, 6908, 6917, 7046, 7105, 7128, 7317, 7355, 7417, 7803, 7823, 7885, 7888, 8158, 8168, 8175, 8271, 8294, 8396, 8410, 8501, 8525, 8944, 9046, 9204, 9249, 9303, 9360, 9421, 9443, 9489, 9528, 9662, 9689, 9742, 9769, 9861, 10056, 10490, 10532, 10534, 10612, 10676, 10691, 10877, 10895, 10899, 10978, 11146, 11151, 11210, 11237, 11273, 11440, 11445, 11449, 11700, 11724, 11785, 11982, 12073, 12170, 12292, 12356, 12865, 12904, 13384, 13520, 13925, 14000, 14210, 14283, 14314, 14348, 14378, 14411, 14460, 14472, 14529, 14602, 14603, 14620, 14626, 14651, 14656, 14658, 14677, 14703, 14732, 14740, 14758, 14768, 14771, 14780, 14790, 14815, 14821, 14832, 14850, 14857, 14901, 14907, 14912, 15126, 15133, 15159, 15160, 15189, 15199, 15204, 15234, 15242, 15274, 15290, 15295]
# indoor_error_list = [918, 927, 938, 957, 976, 1001, 1002, 1022, 1047, 1068, 1106, 1110, 1141, 1170, 1174, 1245, 1247, 1264, 1294, 1309, 1310, 1314, 1324, 1360, 1363, 1388, 1393, 1484, 1491, 1500, 1537, 1573, 1585, 1592, 1609, 2703, 2716, 2733, 2766, 2796, 2806, 2823, 2868, 2900, 2973, 2980, 2984, 2992, 2995, 3012, 3023, 3036, 3049, 3059, 3102, 3128, 3133, 3181, 3218, 3238, 3257, 3269, 3306, 3355, 3359, 3360, 3377, 3382, 3390, 3399, 3407, 3468, 3510, 3522, 3574, 3592, 4170, 4250, 4268, 4433, 4434, 4447, 4456, 4476, 4500, 4502, 4519, 4572, 4581, 4597, 4640, 4657, 4668, 4680, 4687, 4731, 4767, 4806, 4817, 4820, 4841, 4848, 4886, 4895, 4976, 4990, 5029, 5032, 5174, 5196, 5208, 5227, 5238, 5271, 5279, 5284, 5287, 5352, 5388, 5391, 5446, 5460, 5585, 5630, 5718, 5719, 5736, 5805, 5844, 5852, 5853, 5871, 5883, 5896, 5933, 5962, 5978, 6011, 6038, 6059, 6068, 6102, 6393, 6399, 6493, 6498, 6509, 6547, 6556, 6607, 6619, 6651, 6670, 6672, 6713, 6758, 6764, 6770, 6785, 6791, 6813, 6821, 6848, 6849, 6884, 6917, 6934, 6935, 6939, 6956, 6982, 7094, 7102, 7111, 7122, 7140, 7144, 7151, 7185]


# Function to split annotations from multiple files and save as JSON and Pickle files
def split_annotations_for_dataset(input_base_dir_1, input_base_dir_2, output_vision_file, output_referring_file, csv_file_path):
    # Prepare the COCO-style structure for vision annotations
    vision_annotations = {
        "info": {
            "description": "Custom COCO dataset",
            "url": "http://customdataset.org",
            "version": "1.0",
            "year": 2024,
            "contributor": "Custom Dataset Group",
            "date_created": str(datetime.now())
        },
        "images": [],
        "licenses": [
            {"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/", "id": 1, "name": "Attribution-NonCommercial-ShareAlike License"}
        ],
        "annotations": [],
        # "categories": MANUFACT_CATEGORIES
        "categories": INDOOR_CATEGORIES
    }

    referring_output = []
    ref_id = 0
    image_id_counter = 0

    # CSV 파일 로드하여 그룹 ID와 세트 매핑 딕셔너리 생성
    group_split_dict = {}
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            group_split_dict[row['group_id']] = row['set']  # 'train' 또는 'validation'


    # Iterate through all groups
    ann_list = glob.glob(os.path.join(input_base_dir_1, "*")) + glob.glob(os.path.join(input_base_dir_2, "*"))
    
    # 20241019 Use only synthetic data
    # group_dir_list = glob.glob(os.path.join(input_base_dir_2, "*"))
    # error_list = ["{0:06d}".format(i) for i in manufact_error_list]
    # error_list = ["{0:06d}".format(i) for i in indoor_error_list]

    error_file = open("referring_error.txt", 'w')
    error_file_vision = open("vision_error.txt", 'w')

    valid_num = 0
    train_num = 0
    for annotation_file in tqdm(ann_list):
        
        with open(annotation_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract image file name from the annotation and compare with the actual image file
        image_file = annotation_file.replace("annotation", "rgb")
        image_file = image_file.replace("json", "png")
        # try:
        #     assert image_file.split('/')[-1] == data['images']['file_name']
        # except AssertionError:
        #     # print(f"Error: {image_file} != {data['images']['file_name']}, annotation: {annotation_file}")
        #     # print(annotation_file)
        #     data = f"Error: JSON 이름: {annotation_file.split('/')[-3:]}, JSON 내부 png 이름: {data['images']['file_name']} \n"
        #     error_file.write(data)
        #     continue

        
        if image_file.split('/')[-3] == '실제데이터':
            file_name = f"real_{image_file.split('/')[-1]}"
        elif image_file.split('/')[-3] == '가상데이터':
            file_name = f"syn_{image_file.split('/')[-1]}"
        
        group_id = '_'.join(file_name.split('_')[0:2])
        
        # 그룹 ID를 사용하여 데이터 세트 할당
        split = group_split_dict.get(group_id)
        if split is None:
            print(f"Group ID {group_id} not found in CSV. Skipping.")
            continue
        elif split == 'train':
            train_num += 1
        elif split == 'validation':
            # valid_num += 1
            split = 'val'
            pass
        else:
            print(f"Unexpected split value {split} for group ID {group_id}")
            continue

        # Prepare vision annotation (COCO format)
        image_entry = {
            "file_name": file_name,
            # "file_name": data['images']['file_name'],
            "id": image_id_counter,  # Use a counter for unique image IDs
            "height": data['images']['height'],
            "width": data['images']['width'],
            "date_captured": str(datetime.now())  # Assuming current date
        }
        vision_annotations['images'].append(image_entry)

        # Process each annotation within the JSON file
        for ann in data['annotations']:
            # Vision annotation: Include bbox, segmentation, area, etc.
            try:
                vision_annotation = {
                    "image_id": image_id_counter,
                    "id": ann['id'],
                    "category_id": ann['category_id'],
                    "bbox": ann['bbox'],
                    "segmentation": ann['segmentation'],
                    "area": ann['area'],
                    "iscrowd": ann['iscrowd'],
                }
                # vision_annotations['annotations'].append(vision_annotation)
            except KeyError:
                print(annotation_file.split('/')[-3:])
                print("Error in annotation: ", ann)
                data = f"vision_annotation: {annotation_file.split('/')[-3:]}\n"
                error_file_vision.write(data)
                continue

            # Referring annotation format
            try:
                sentences = [
                    # {"tokens": ann['token'], "raw": ann['referring_expression'], "sent_id": i, "sent": ann['referring_expression']}
                    {"raw": ann['referring_expression'], "sent_id": i, "sent": ann['referring_expression']}
                    for i in range(len([ann['referring_expression']]))
                ]
            except KeyError:
                data = f"referring_expression: {annotation_file.split('/')[-3:]}\n"
                print(data)
                error_file.write(data)
                continue

            vision_annotations['annotations'].append(vision_annotation)
            valid_num += 1

            # randint_for_split = random.randint(0, 19)
            # # if randint_for_split == 8:
            # #     split = "val"
            # # elif randint_for_split == 9:
            # #     split = "test"
            # # else:
            # #     split = "train"
            # if train_num >= 400000:
            #     print("train is full!")
            #     split = "val"
            # else:
            #     if randint_for_split == 9:
            #         split = "val"
            #     else:
            #         split = "train"
            #         train_num += 1

            referring_annotation = {
                "ref_id": ref_id,
                "category_id": ann['category_id'],
                "image_id": image_id_counter,
                # "file_name": data['images']['file_name'],
                "file_name": file_name,
                "ann_id": ann['id'],
                "split": split,
                "sentences": sentences,
                "sent_ids": [i for i in range(len(sentences))]
            }
            referring_output.append(referring_annotation)
            ref_id += 1

        image_id_counter += 1
        
        # Move image to the output directory
        output_image_dir = os.path.join(os.path.dirname(output_vision_file), "images")
        shutil.copy(image_file, os.path.join(output_image_dir, file_name))
        # shutil.copy(image_file, os.path.join(output_image_dir, data['images']['file_name']))
    
    print(valid_num)
    print(train_num)

    # Save the vision annotations to a JSON file
    with open(output_vision_file, 'w', encoding='utf-8') as f:
        json.dump(vision_annotations, f, ensure_ascii=False, indent=4)

    # Save the referring annotations to a pickle file
    with open(output_referring_file, 'wb') as f:
        pickle.dump(referring_output, f)

    # f.close()


if __name__ == "__main__":
    # input_dir_1 = "/SSDa/sangbeom_lee/제조_실제"
    # input_dir_2 = "/SSDa/sangbeom_lee/제조_가상"
    # output_vision_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/manufact/instances.json"
    # output_referring_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/manufact/refs.p"

    # input_dir_1 = "/SSDa/sangbeom_lee/가정_실제"
    # input_dir_2 = "/SSDa/sangbeom_lee/가정_가상"
    # output_vision_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/indoor/instances.json"
    # output_referring_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/indoor/refs.p"

    # 80 percent AIHub indoor 
    input_dir_1 = "/SSDa/sangbeom_lee/22-39.가정환경/실제데이터/annotation"
    input_dir_2 = "/SSDa/sangbeom_lee/22-39.가정환경/가상데이터/annotation"
    output_vision_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/indoor_80/instances_2.json"
    output_referring_file = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/indoor_80/refs_2.p"
    csv_file_path = "/SSDa/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/indoor_80/group_split.csv"


    # 80 percent AIHub manufact 
    # input_dir_1 = "/SSDe/sangbeom_lee/22-38.제조환경/실제데이터/annotation"
    # input_dir_2 = "/SSDe/sangbeom_lee/22-38.제조환경/가상데이터/annotation"
    # output_vision_file = "/SSDe/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/manufact_80/instances.json"
    # output_referring_file = "/SSDe/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/manufact_80/refs.p"
    # csv_file_path = "/SSDe/sangbeom_lee/AIHub_LAVT-RIS/refer/data/aihub_refcoco_format/manufact_80/group_split.csv"

    # convert_to_refcoco_format(input_dir, output_file)
    split_annotations_for_dataset(input_dir_1, input_dir_2, output_vision_file, output_referring_file, csv_file_path)
    
    # import json

    # with open('refer/data/refcoco/instances.json', 'r') as f:

    #     json_data = json.load(f)

    # # print(json.dumps(json_data) )
    # # print(json_data["annotations"])
    # print(json_data.keys())
    # print(json_data["info"])
    # print(json_data["images"][0])
    # print(json_data["licenses"])
    # print(json_data["annotations"][0])
    # print(json_data["categories"])

    # import pickle

    # # Load the pickle file
    # with open("refer/data/refcoco/refs(unc).p", "rb") as f:
    #     data = pickle.load(f)

    # # Inspect the data
    # print(data[0])