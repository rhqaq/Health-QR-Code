# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import json


def infoframe(each, frame=None, add=False):
    ''' 返回内容与长度统一的用户基本信息框 '''
    each_key = [i for i in each.keys()]
    frame_key = ['昵称', '真实姓名', '所在地', '性别', '性取向', '感情状况',
                 '生日', '血型', '博客地址', '个性域名', '简介', '注册时间', '关注', '粉丝', '微博', 'href']
    print(each)
    if add:
        frame.append([each[i] if i in each_key else '' for i in frame_key])
    else:
        frame_val = [each[i] if i in each_key else '' for i in frame_key]
        frame = [frame_key, frame_val]
    return frame


def get_info(driver, href, frame=None, add=False):
    ''' 爬取单个用户基本信息 '''
    button_path = r'/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div[4]/div/div/a/span'
    info_path = r'/html/body/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/ul'

    follow_info = enter_infopage(driver, button_path, href)
    print(follow_info)
    time.sleep(2)
    # if exist_href == False or exist_href == None:
    #     return False
    try:
        text_list = info_spider(driver, info_path)
    except:
        follow_info = enter_infopage(driver, button_path, href)
        time.sleep(2)
        text_list = info_spider(driver, info_path)
    if follow_info is None:
        return 'dead'
    # print(follow_info)
    print(text_list)

    if text_list != []:
        if "简介：\n注册时间" in text_list[0]:
            text_list[0] = text_list[0].replace("简介：\n注册时间","注册时间")
            print(text_list)
        info_list = text_list[0].split('\n')
        info_key = [info_list[i][:-1] for i in range(len(info_list)) if i % 2 == 0]
        info_val = [info_list[i] for i in range(len(info_list)) if i % 2 == 1]
    else:
        info_key = []
        info_val = []
    for i in range(len(follow_info)):
        info_key.append(follow_info[i].split()[1])
        info_val.append(follow_info[i].split()[0])
    info_key.append('href')  # 将用户主页加入到输出数据中
    info_val.append(href)
    each = {i: j for i, j in zip(info_key, info_val)}
    if add:
        return infoframe(each, frame, True)
    else:
        return infoframe(each)


def userinfo(href, username, password, driver, browser='Firefox', filepath=None, saved=False, newfile=False):
    '''
    主程序, 获取单个或所有用户的基本信息

    参数类型及含义
    ----------
    href : str or list  用户主页url或url列表
    username : str  用于登录的微博账号
    password : str  用于登录的微博密码
    filepath : str  文件保存路径
    saved : bool  是否保存文件, 若为False则仅返回数据而不保存
    newfile : bool  保存文件时是否创建新文件?若为True, 则创建新文件或覆盖原文件; 若为False则在原文件基础上追加数据

    使用范例
    ----------
    > myhref = 'https://weibo.com/weibokefu'
    > myusername = '123456'
    > mypassword = '123456'
    > myfilepath = 'C:/test.csv'
    > only_data = userinfo(myhref, myusername, mypassword)  # 仅获取爬取的数据
    > userinfo(myhref, myusername, mypassword, filepath=myfilepath, saved=True, newfilw=True)  # 将爬取的数据作为一个新文件保存到C盘
    '''

    frame_key = ['昵称', '真实姓名', '所在地', '性别', '性取向', '感情状况',
                 '生日', '血型', '博客地址', '个性域名', '简介', '注册时间', '关注', '粉丝', '微博', 'href']

    if isinstance(href, str):
        result = get_info(driver, href)
        # print(result)
        if result == 'dead':
            return 'dead'
        if result == False:
            print('这个href不可用 : %s' % href)
        else:
            if saved:
                save_userinfo(result, filepath, newfile)
            else:
                return result
    else:
        result = get_info(driver, href[0])
        if result == False:
            frame_val = ['' for i in frame_key]
            frame = [frame_key, frame_val]
        else:
            frame = result
        length = len(href) - 1
        count = 1
        for i in range(1, len(href)):
            result = get_info(driver, href[i], frame=frame, add=True)
            # print(result)
            if result == False:
                continue
            else:
                frame = result
            windows = driver.window_handles
            if len(windows) > 1:
                driver.switch_to.window(windows[0])
            print('距爬完还有%d条, 已爬取%d条' % (length, count))
            length -= 1
            count += 1
        if saved:
            save_userinfo(frame, filepath, newfile)
        else:
            return frame


def enter_infopage(driver, button_path, href):
    ''' 进入用户基本信息所在界面, 并爬取数据 '''
    check1 = driver.current_url
    driver.get(href)
    time.sleep(1.5)
    try:
        follow = driver.find_elements_by_xpath(
            '/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div/table/tbody/tr/td')
        # follow_number = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div/table/tbody/tr/td')
        follow_info = [i.text for i in follow]
    except:
        time.sleep(1.5)
        follow = driver.find_elements_by_xpath(
            '/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div/table/tbody/tr/td')
        # follow_number = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div/table/tbody/tr/td')
        follow_info = [i.text for i in follow]
    check2 = driver.current_url
    if check1 in check2:
        return follow_info
    try:
        driver.find_element_by_xpath(button_path).click()

        return follow_info
    except:
        try:
            WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.XPATH, button_path)))
            driver.find_element_by_xpath(button_path).click()

            return follow_info
        except:
            # driver.refresh()
            # enter_infopage(driver, button_path, href)
            return None


def info_spider(driver, info_path):
    ''' 爬取页面中的用户基本信息 '''
    texts = driver.find_elements_by_xpath(info_path)
    count = 0
    while texts == [] and count <= 2:
        time.sleep(1)
        texts = driver.find_elements_by_xpath(info_path)
        count += 1
        if count == 6:
            break

    return [i.text for i in texts]


def save_userinfo(data, filepath, newfile=False):
    '''
    以csv格式输出并保存爬取的数据
    参数类型及含义
    ----------
    data : array/list  爬取的用户基本信息数据
    filepath : str  文件保存路径
    newfile : bool  保存文件时是否创建新文件?若为True, 则创建新文件或覆盖原文件; 若为False则在原文件基础上追加数据
    '''
    if re.match(r'(.*?).csv$', filepath):
        if newfile:
            write_type = 'w'
        else:
            write_type = 'a+'
            data = data[1:]  # 去除标题行
        with open(filepath, write_type, newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            file.close()
    else:
        return ValueError('目前只支持输出csv格式')



driver1 = webdriver.Chrome(executable_path='chromedriver')
url = 'https://weibo.com/login.php'  # 微博主页面, 用于登录账户
login_path = '//div[@class="gn_login"]/ul[@class="gn_login_list"]/li[3]/a[@class="S_txt1"]'

driver1.get(url)

time.sleep(15)

with open('user_info.json', 'r', encoding='utf-8') as fp:
    user_info_list = json.load(fp)
with open('author_href_ongoing.json', 'r', encoding='utf-8') as fp:
    author_href_ongoing = json.load(fp)
with open('author_href_finish.json', 'r', encoding='utf-8') as fp:
    author_href_finish = json.load(fp)
with open('dead_author.json', 'r', encoding='utf-8') as fp:
    dead_author = json.load(fp)

while len(author_href_ongoing) != 0:

    href = author_href_ongoing[0]
    dic_user_info = {}
    a = userinfo(href, "", "", driver1, browser='Chrome', filepath=None, saved=False,
                 newfile=False)
    if a == 'dead':
        dead_author.append(href)
        dic_user_info['href'] = href
        dic_user_info['content'] = 'dead'
    elif a is not None:
        for i in range(len(a[0])):
            dic_user_info[a[0][i]] = a[1][i]
            dic_user_info['content'] = True
        author_href_finish.append(href)
    else:
        dic_user_info['href'] = href
        dic_user_info['content'] = False
    user_info_list.append(dic_user_info)

    author_href_ongoing.pop(0)
    with open('author_href_finish.json', 'w', encoding='utf-8') as fp:
        json.dump(author_href_finish, fp, indent=4, ensure_ascii=False)
    with open('author_href_ongoing.json', 'w', encoding='utf-8') as fp:
        json.dump(author_href_ongoing, fp, indent=4, ensure_ascii=False)
    with open('user_info.json', 'w', encoding='utf-8') as fp:
        json.dump(user_info_list, fp, indent=4, ensure_ascii=False)
    with open('dead_author.json', 'w', encoding='utf-8') as fp:
        json.dump(dead_author, fp, indent=4, ensure_ascii=False)
    print(a)
    print(len(user_info_list))
    print(len(author_href_ongoing))
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # time.sleep(0.5)
