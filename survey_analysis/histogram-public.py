import csv
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import shutil

shutil.rmtree(matplotlib.get_cachedir())
# from matplotlib.font_manager import _rebuild
# _rebuild() #reload一下
# -*- coding: utf-8 -*-
all=[]

for filename in ['随申码_有效_无转变经历.csv','随申码_有效_有转变经历.csv']:
    with open(filename,'r', encoding='utf-8') as fin:
        reader = csv.reader(fin)
        l = []
        for line in reader:
            l.append(line)
        all.append(l)

t1 = [34,35,36,37,38,39]
title_t1 = ['您对健康码展示页面各类颜色代表情形非常了解',
            '您对健康码各颜色所需做出的相应行为非常了解',
            '健康码保障了您和他人的安全',
            '健康码在疫情防控中发挥了重要作用',
            '健康码打开速度较快',
            '登录时身份认证方便（验证是否为本人操作）']
gap_1 =[0, 0]

t2 = [74,75,76]
title_t2 = ['您对健康码隐私与数据保护的认知\n您清楚您的个人信息被采集',
            '您对健康码隐私与数据保护的认知\n您了解到您个人信息采集后到处理以及存储情况',
            '您对健康码隐私与数据保护的认知\n您认为通过健康码采集后您的个人信息是安全的']

t2_ = [77,78]
title_t2_ = ['您对健康码保护隐私的满意度:隐藏姓名功能',
            '您对健康码保护隐私的满意度:隐藏身份证功能']

t3 = [80,81,82]
title_t3 = ['健康码出现以下问题的频率:崩溃打不开',
            '健康码出现以下问题的频率:打开时身份认证困难',
            '健康码出现以下问题的频率:个人信息错误']
t4 = [84]
title_t4=['当疫情趋于严重时，您认为健康码崩溃的可能性高吗？']
# gap_2 = [54,53,60,45]

for t,title in zip(t4,title_t4):
    t_5_code = [t]
    for add in gap_1:
        t_5_code.append(t_5_code[-1] + add)
    l_p = []
    for code in range(2):
        t_this = t_5_code[code]
        ans_count_list = []
        # ans_count = {'A.非常符合': 0,'B.比较符合': 0, 'C.难以判断': 0, 'D.不太符合': 0,'E.非常不符合': 0}
        # ans_count = {'A.非常满意': 0,'B.比较满意': 0, 'C.一般': 0, 'D.不太满意': 0,'E.非常不满意': 0, 'F.不了解该功能':0}
        # ans_count = {'A.没有遇到': 0,'B.偶尔': 0, 'C.一般': 0, 'D.经常': 0}
        ans_count = {'A.不可能崩溃': 0,'B.崩溃可能性低': 0, 'C.崩溃可能性一般': 0, 'D.崩溃可能性高': 0,'E.肯定会崩溃': 0}
        for line in all[code][1:]:
            ans_count[line[t_this]] = ans_count[line[t_this]] + 1
        # for key in ['A.非常符合','B.比较符合', 'C.难以判断', 'D.不太符合','E.非常不符合']:
        # for key in ['A.非常满意','B.比较满意', 'C.一般', 'D.不太满意','E.非常不满意','F.不了解该功能']:
        # for key in ['A.没有遇到','B.偶尔', 'C.一般', 'D.经常']:
        for key in ['A.不可能崩溃','B.崩溃可能性低', 'C.崩溃可能性一般', 'D.崩溃可能性高','E.肯定会崩溃']:
            ans_count_list.append(ans_count[key])
        sum1 = sum(ans_count_list)
        percentage = [x*1.0/sum1 for x in ans_count_list]
        l_p.append(percentage)
    x = ['无转变经历', '有转变经历']
    y = np.array(l_p).transpose()
    plt.title(title)
    # plt.bar(x, y[0], label='非常符合',fc = 'tab:green', width = 0.5)
    # plt.bar(x, y[1], bottom=y[0], label='比较符合',fc = 'tab:olive', width = 0.5)
    # plt.bar(x, y[2], bottom=y[0]+y[1], label='难以判断',fc = 'tab:gray', width = 0.5)
    # plt.bar(x, y[3], bottom=y[0]+y[1]+y[2], label='不太符合',fc = 'tab:pink', width = 0.5)
    # plt.bar(x, y[4], bottom=y[0]+y[1]+y[2]+y[3], label='非常不符合',fc = 'tab:red', width = 0.5)

    # plt.bar(x, y[0], label='非常满意',fc = 'tab:green', width = 0.5)
    # plt.bar(x, y[1], bottom=y[0], label='比较满意',fc = 'tab:olive', width = 0.5)
    # plt.bar(x, y[2], bottom=y[0]+y[1], label='一般',fc = 'tab:gray', width = 0.5)
    # plt.bar(x, y[3], bottom=y[0]+y[1]+y[2], label='不太满意',fc = 'tab:pink', width = 0.5)
    # plt.bar(x, y[4], bottom=y[0]+y[1]+y[2]+y[3], label='非常不满意',fc = 'tab:red', width = 0.5)
    # plt.bar(x, y[5], bottom=y[0]+y[1]+y[2]+y[3]+y[4], label='不了解该功能',fc = 'tab:blue', width = 0.5)

    # plt.bar(x, y[0], label='没有遇到',fc = 'tab:green', width = 0.5)
    # plt.bar(x, y[1], bottom=y[0], label='偶尔',fc = 'tab:olive', width = 0.5)
    # plt.bar(x, y[2], bottom=y[0]+y[1], label='一般',fc = 'tab:gray', width = 0.5)
    # plt.bar(x, y[3], bottom=y[0]+y[1]+y[2], label='经常',fc = 'tab:pink', width = 0.5)

    plt.bar(x, y[0], label='不可能崩溃',fc = 'tab:green', width = 0.5)
    plt.bar(x, y[1], bottom=y[0], label='崩溃可能性低',fc = 'tab:olive', width = 0.5)
    plt.bar(x, y[2], bottom=y[0]+y[1], label='崩溃可能性一般',fc = 'tab:gray', width = 0.5)
    plt.bar(x, y[3], bottom=y[0]+y[1]+y[2], label='崩溃可能性高',fc = 'tab:pink', width = 0.5)
    plt.bar(x, y[4], bottom=y[0]+y[1]+y[2]+y[3], label='肯定会崩溃',fc = 'tab:red', width = 0.5)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),  fancybox=True, ncol=6)
    plt.rcParams['font.sans-serif']=['SimHei']
    # plt.savefig(title)
    plt.show()


#
# name = all[0][0]
# for i,item in enumerate(name):
#     print(i,item) # 0开始

# t33 = []
# for li in l:
#     t33.append(li[33])
# t33 = t33[1:]
# print(t33)
# t33d = {'A.非常符合': 0,'B.比较符合': 0, 'C.难以判断': 0, 'D.不太符合': 0,'E.非常不符合': 0}
# for key in t33:
#     t33d[key] = t33d.get(key, 0) + 1
# print(t33d)
#
#
# t96 = []
# for li in l1:
#     t96.append(li[96])
# t96 = t96[1:]
# t96d = {'A.非常符合': 0,'B.比较符合': 0, 'C.难以判断': 0, 'D.不太符合': 0,'E.非常不符合': 0}
# for key in t96:
#     t96d[key] = t96d.get(key, 0) + 1
# print(t96d)
#
#
#
# x = ['随申码', '苏康码']
# a = np.array([91,23]) # 非常同意
# b = np.array([43,10])
# c = np.array([50,10])
# d = np.array([25,15])
# e = np.array([10,20])
# plt.bar(x, a, label='非常符合',fc = 'r')
# plt.bar(x, b, bottom=a, label='比较符合',fc = 'g')
# plt.bar(x, c, bottom=a+b, label='难以判断',fc = 'b')
# plt.bar(x, d, bottom=a+b+c, label='比较不符合',fc = 'c')
# plt.bar(x, e, bottom=a+b+c+d, label='非常不符合',fc = 'm')
# plt.legend()
# plt.show()

# 随申码
# 33 34 35 36 37 38 非常符合 比较符合 难以判断 比较不符合 非常不符合
# 73 74 75 76 77 非常符合 比较符合 难以判断 比较不符合 非常不符合
# 79 80 81 没有遇到 偶尔 一般 经常
# 83 不可能崩溃 崩溃可能性低 崩溃可能性一般 崩溃可能性高 肯定会崩溃
# g 63 63
# 苏康码
# 96 97 98 99 100 101
# 136 137 138 139 140
# 142 143 144
# 146
# g 63 44
# 北京健康宝
# 149 150 151 152 153 154
# 180 181 182 183 184
# 186 187 188
# 190
# g 52 60
# 粤康码
# 201 202 203 204 205 206
# 240 241 242 243 244
# 246 247 248
# 250
# g 61 45
# 西安一码通
# 262 263 264 265 266 267
# 285 286 287 288 289
# 291 292 293
# 295
