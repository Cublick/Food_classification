import re
import os
# import pandas as pd
import json
import sys
import csv

# 크롤링된 음식점 데이터
file_path = r'C:\Users\com\Desktop\전국데이터\음식\KakaoMap(Scrape)_Restaurant_Seoul_20220304_51030.csv'

# def restart():
#     os.execl(sys.executable, sys.executable, *sys.argv)

# 총 13개의 카테고리
category_list = ['한식', '일식', '중식', '양식', '기타 외국식', '기타 음식', '기타', '제과점', '주점', '치킨', '카페&베이커리', '패스트푸드', '해물&생선',
                 '제외']
cate_food_list = {}
lines = []

# 크롤링된 데이터에서 음식(메뉴)부분만을 추출하기 위한 부분
for cate_idx, cate in enumerate(category_list):
    if not cate in cate_food_list:
        cate_food_list[cate] = []
    category_file = r'C:\Users\com\Desktop\전국데이터\음식\음식카테고리\\' + cate + '.txt'

    food_f = open(category_file, 'r', encoding='utf-8')
    f_rdr = csv.reader(food_f)
    for f_idx, food in enumerate(f_rdr):
        food = str(food)
        food = food.replace("']", "").replace("['", "").strip()
        if food in cate_food_list[cate]:
            continue
        else:
            cate_food_list[cate].append(food)

# -------------------------------------------------------------------------------------------------------------------------------

f = open(file_path, 'r', encoding='utf-8')
rdr = csv.reader(f)
lines, remain_list = [], []

for main_idx, line in enumerate(rdr):
    cate_to_food = []
    if main_idx == 0:
        line[0] = 'Unknownname'
        lines.append(line)
        continue
    if line[1] == 'GoogleMap' or line[10] == '정보없음':
        lines.append(line)
        continue
    try:
        if line[10] != '{}':
            search_food = eval(line[10]).keys()

            for food_idx, food in enumerate(search_food):
                food = re.sub('[^ ㄱ-ㅣ가-힣]+', '', food)
                food = food.strip()
                for cate in category_list:
                    if food in cate_food_list[cate]:
                        cate_to_food.append({food: cate})
                        break
                else:
                    if food in remain_list:
                        continue
                    if food == '':
                        continue
                    else:
                        remain_list.append(food)
                        print(food)
                        print('한식 : 1\t 중식 : 2\t 일식 : 3\t 양식 : 4\t 기타 외국식(동남아) : 5\t 해물,생선 : 6\t 제과점(빵,떡) : 7\t '
                              '패스트푸드 : 8\t 치킨 : 9\t 기타 음식(분식) : 10\t 카페 : 11\t 주점 : 12\t 기타(사찰) : 13\t 제외 :  ')

                        food_dict = {'1': '한식', '2': '중식', '3': '일식', '4': '양식', '5': '기타 외국식', '6': '해물, 생선', '7': '제과점',
                                     '8': '패스트푸드', '9': '치킨', '10': '기타 음식', '11': '카페, 베이커리', '12': '주점', '13': '기타', '0': '제외'}
                        s = input().strip()
                        if s == '':
                            s = food_dict['0']
                            remain_list.append(food)
                        else:
                            s = food_dict[s]

                        tmp = open(r'C:\Users\com\Desktop\전국데이터\음식\음식카테고리\\' + s + '.txt', 'a', encoding='utf-8')
                        tmp.write('\n' + food)
                        tmp.close()
        # # restart()

        else:
            lines.append(line)
            continue
    except:
        lines.append(line)
        continue

    line[10] = cate_to_food + remain_list

    lines.append(line)

f = open('gimcheon_restaurant_processing.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerows(lines)

f.close()
