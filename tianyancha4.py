#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 19:17:55 2017

@author: chen
"""
from time_change import stamp
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import pymysql
import time


def turn_page(next_xpath):
    driver.execute_script("arguments[0].scrollIntoView();", next_xpath)
    time.sleep(1)
    next_xpath.send_keys(Keys.UP)
    time.sleep(1)
    next_xpath.send_keys(Keys.UP)
    time.sleep(1)
    next_xpath.click()
    time.sleep(5)


# 判断字段是否存在，若存在返回第一个元素。若不存在返回空字符串
def if_exist (company):
    if company==[]:
        company=''
    else:
        company=company[0]
    return company

#将字典数据插入数据库
# def InsertData(TableName,dic):
#     conn = pymysql.connect("localhost","root","315135",'Company')
#     cur = conn.cursor()
#
#     conn.set_charset('utf8')
#     cur.execute('SET NAMES utf8;')
#     cur.execute('SET CHARACTER SET utf8;')
#     cur.execute('SET character_set_connection=utf8;')
#
#     COLstr=''   #列的字段
#     ROWstr=''  #行字段
#     ColumnStyle=' VARCHAR(20)'
#
#
#
#     for key in dic.keys():
#          COLstr=COLstr+' '+key+ColumnStyle+','
#          ROWstr=(ROWstr+'"%s"'+',')%(dic[key])
#
#     try:
#         cur.execute("SELECT * FROM  %s"%(TableName))
#         cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))
#     except :
#         print('ERROR such as PRIMARY key is exist')
#     else:
#         conn.commit()
#         cur.close()
#         conn.close()

# login = {'user': '17681825594', 'passwd': 'a585858585'}
#login = {'user': '14757151234', 'passwd': 'qq784814747'}
login = {'user': '15757130644', 'passwd': 'aA315135'}

driver = webdriver.Firefox()
driver.get('https://www.tianyancha.com/login')
driver.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input').send_keys(login['user'])
driver.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input').send_keys(login['passwd'])
driver.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]').click()



#com_list=['北京百度网讯科技有限公司','杭州投着乐网络科技有限公司']
com_list=['北京百度网讯科技有限公司']

for i in com_list:
    res_dic={}
    driver.get('https://www.tianyancha.com/search?key=%s&checkFrom=searchBox'%i)
    detal_url=driver.find_element_by_xpath('//*[@id="web-content"]/div/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/a')
    driver.get(detal_url.get_attribute('href'))

    response= etree.HTML(driver.page_source)
    
# `com_id` '公司ID',
    com_id=com_list.index(i)+1
    res_dic['com_id']=com_id

#  `company_name` '公司名称'
    company_name=response.xpath('//*[@id="company_web_top"]/div[2]/div[2]/div/span/text()')
    company_name=if_exist(company_name)
    res_dic['company_name']=company_name
    
#  `company_introduction` '公司简介'
    company_introduction=response.xpath('//*[@id="company_web_top"]/div[3]/span[1]/text()')
    company_introduction=if_exist(company_introduction)
    res_dic['company_introduction']=company_introduction


# 主要人员计数
    personnel_count=response.xpath('//*[@id="nav-main-staffCount"]/span/text()')
    personnel_count=int(if_exist(personnel_count))    
    for j in range(1,personnel_count+1):
        position_position=response.xpath('//*[@id="_container_staff"]/div/div/div[%s]/div/div[1]/span/text()'%j)
        position_position=if_exist(position_position)
        res_dic['position_position%s'%j]=position_position
        
        position_personnel=response.xpath('//*[@id="_container_staff"]/div/div/div[%s]/div/a/text()'%j)
        position_personnel=if_exist(position_personnel)
        res_dic['position_personnel%s'%j]=position_personnel

# 股东信息
    shareholder_count=response.xpath('//*[@id="nav-main-holderCount"]/span/text()')
    shareholder_count=int(if_exist(shareholder_count))    
    for j in range(1,shareholder_count+1):
        # 股东
        shareholder=response.xpath('//*[@id="_container_holder"]/div/table/tbody/tr[%s]/td[1]/a/text()'%j)
        shareholder=if_exist(shareholder)
        res_dic['shareholder%s'%j]=shareholder
        # 出资比例
        shareholder_ratio_of_investments=response.xpath('//*[@id="_container_holder"]/div/table/tbody/tr[%s]/td[2]/div/div/span/text()'%j)
        shareholder_ratio_of_investments=if_exist(shareholder_ratio_of_investments)
        res_dic['shareholder_ratio_of_investments%s'%j]=shareholder_ratio_of_investments
        # 认缴出资
        shareholder_subscribed_capital=response.xpath('//*[@id="_container_holder"]/div/table/tbody/tr[%s]/td[3]/div/span/text()'%j)
        shareholder_subscribed_capital=if_exist(shareholder_subscribed_capital)
        res_dic['shareholder_subscribed_capital%s'%j]=shareholder_subscribed_capital


    # # 对外投资
    # company_foreign_investment =[]
    # inverst_total_page = response.xpath('//*[@id="_container_invest"]/div/div[2]/div/text()')
    # if len(inverst_total_page) > 0:
    #     total_page = int(inverst_total_page[0])
    #     for a in range(0, total_page):
    #         inverst = response.xpath('//*[@id="_container_invest"]/div/div[1]/table/tbody/tr')
    #         for i in inverst:
    #             # 被投资企业名称
    #             inverst_company_name = if_exist(i.xpath('td[1]/a/span/text()'))
    #             # 被投资法定代表人
    #             company_legal_representative = if_exist(i.xpath('td[2]/span/a/text()'))
    #             # 注册资本
    #             company_registered_capital = if_exist(i.xpath('td[3]/span/text()'))
    #             # 投资数额
    #             investment_money = if_exist(i.xpath('/td[4]/span/text()'))
    #             # 投资占比
    #             investment_proportion = if_exist(i.xpath('td[5]/span/text()'))
    #             # 注册时间
    #             investment_date = if_exist(i.xpath('td[6]/span/text()'))
    #             # 状态
    #             company_operating_state = if_exist(i.xpath('td[7]/span/text()'))
    #             print inverst_company_name, company_legal_representative, company_registered_capital, investment_money, investment_proportion, stamp(investment_date), company_operating_state
    #             c = [inverst_company_name, company_legal_representative, company_registered_capital, investment_money,
    #                  investment_proportion, stamp(investment_date), company_operating_state]
    #             company_foreign_investment.append(c)
    #         next_page = driver.find_element_by_xpath('//*[@id="_container_invest"]/div/div[2]/ul/li[last()]/a')
    #         turn_page(next_xpath=next_page)
    #         response = etree.HTML(driver.page_source)

    # # 变更记录
    # company_change = []
    # change_total_page = response.xpath('//*[@id="_container_changeinfo"]/div/div[2]/div/text()')
    # if len(change_total_page) > 0:
    #     total_page = int(change_total_page[0])
    #     for a in range(0, total_page):
    #         change = response.xpath('//*[@id="_container_changeinfo"]/div/div[1]/table/tbody/tr')
    #         for i in change:
    #             # 变更时间
    #             company_change_time = if_exist(i.xpath('td[1]/div/text()'))
    #             # 变更项目
    #             company_change_matter = if_exist(i.xpath('td[2]/div/text()'))
    #             # 变更前
    #             company_change_before = ''.join(i.xpath('td[3]/div/text()'))
    #             # 变更后
    #             company_change_after = ''.join(i.xpath('td[4]/div/text()'))
    #             print company_change_time, company_change_matter, company_change_before, company_change_after
    #             c = [stamp(company_change_time), company_change_matter, company_change_before, company_change_after]
    #             company_change.append(c)
    #         next_page = driver.find_element_by_xpath('//*[@id="_container_changeinfo"]/div/div[2]/ul/li[last()]/a')
    #         turn_page(next_xpath=next_page)
    #         response = etree.HTML(driver.page_source)

        # 核心团队
#        company_team = []
#        team_total_page = response.xpath('//*[@id="_container_teamMember"]/div/div[6]/div/text()')
#        if len(team_total_page) > 0:
#            total_page = int(team_total_page[0])
#            for a in range(0, total_page):
#                team = response.xpath('//*[@id="_container_teamMember"]/div/div')
#                for i in team:
#                    # 成员照片
#                    team_member_photo = if_exist(i.xpath('div[1]/div[1]/img/@src'))
#                    # 成员名字
#                    team_member_name = if_exist(i.xpath('div[1]/div[2]/text()'))
#                    # 成员职位
#                    team_member_position = if_exist(i.xpath('div[2]/div/text()'))
#                    # 成员介绍
#                    team_member_introduce = '\n'.join(i.xpath('div[2]/ul/li/span/text()'))
#                    print(team_member_name, team_member_photo, team_member_position, team_member_introduce)
#                    c = [team_member_name, team_member_photo, team_member_position, team_member_introduce]
#                    company_team.append(c)
#                if a != total_page-1:
#                    next_page = driver.find_element_by_xpath('//*[@id="_container_teamMember"]/div/div[6]/ul/li[last()]/a')
#                    turn_page(next_xpath=next_page)
#                    response = etree.HTML(driver.page_source)




##企业业务
#    company_business = []
#    business_total_page = response.xpath('//*[@id="_container_firmProduct"]/div/div[2]/div/text()')
#    
#    
#    if len(business_total_page) > 0:
#        total_page = int(business_total_page[0])
#        for a in range(0, total_page):
#            team = response.xpath('//*[@id="_container_firmProduct"]/div/div[1]/div')
#    
#            for i in team:
#                # 企业照片
#                company_photo = if_exist(i.xpath('div[1]/img/@src'))
#                # 企业名称
#                company_name = if_exist(i.xpath('div[2]/div[1]/span/text()'))
#                # 企业领域
#                company_domain = if_exist(i.xpath('div[2]/div[2]/text()'))
#                # 企业介绍
#                company_introduce = '\n'.join(i.xpath('div[2]/div[3]/text()'))
#    
#                print(company_name, company_photo, company_domain, company_introduce)
#                c = [company_name, company_photo, company_domain, company_introduce]
#                company_business.append(c)
#            next_page = driver.find_element_by_xpath('//*[@id="_container_firmProduct"]/div/div[2]/ul/li[last()]/a')
#            turn_page(next_xpath=next_page)
#            response = etree.HTML(driver.page_source)

#法律诉讼
#    lawsuit_business = []
#    lawsuit_total_page = response.xpath('//*[@id="_container_lawsuit"]/div/div[2]/div/text()')
#
#    if len(lawsuit_total_page) > 0:
#        total_page = int(lawsuit_total_page[0])
#        for a in range(0, total_page):
#            team = response.xpath('//*[@id="_container_lawsuit"]/div/div[1]/table/tbody/tr')
#
#
#            for i in team:
#                # 日期
#                lawsuit_date = if_exist(i.xpath('td[1]/span/text()'))
#                # 裁判文书
#                lawsuit_paper = if_exist(i.xpath('td[2]/a/text()'))
#                # 案件类型
#                lawsuit_type = if_exist(i.xpath('td[3]/span/text()'))
#                # 案件号
#                lawsuit_number = if_exist(i.xpath('td[4]/span/text()'))
#
#                print(lawsuit_date, lawsuit_paper, lawsuit_type, lawsuit_number)
#                c = [lawsuit_date, lawsuit_paper, lawsuit_type, lawsuit_number]
#                lawsuit_business.append(c)
#            next_page = driver.find_element_by_xpath('//*[@id="_container_lawsuit"]/div/div[2]/ul/li[last()]/a')
#            turn_page(next_xpath=next_page)
#            response = etree.HTML(driver.page_source)

##法院公告
#    court_notice = []
#    court_total_page = response.xpath('//*[@id="_container_court"]/div/div[2]/div/text()')
#    if len(court_total_page) > 0:
#        total_page = int(court_total_page[0])
#        for a in range(0, total_page):
#            team = response.xpath('//*[@id="_container_court"]/div/div[1]/table/tbody/tr')
#            for i in team:
#                # 公告时间
#                court_date = if_exist(i.xpath('td[1]/text()'))
#                # 上诉方
#                court_appellant = if_exist(i.xpath('td[2]/span/text()'))
#                # 被诉方
#                court_defendant = if_exist(i.xpath('td[3]/span/text()'))
#                # 公告类型
#                announcement_type = if_exist(i.xpath('td[4]/span/text()'))
#                #法院
#                court_type = if_exist(i.xpath('td[5]/span/text()'))
#                
#                print(court_date, court_appellant, court_defendant,announcement_type,court_type)
#                c = [court_date, court_appellant, court_defendant,announcement_type,court_type]
#                court_notice.append(c)
#            next_page = driver.find_element_by_xpath('//*[@id="_container_court"]/div/div[2]/ul/li[last()]/a')
#            turn_page(next_xpath=next_page)
#            response = etree.HTML(driver.page_source)


#被执行人
#    execute_person = []
#    execute_total_page = response.xpath('//*[@id="_container_zhixing"]/div/div[2]/div/text()')
#
#    if len(execute_total_page) > 0:
#        total_page = int(execute_total_page[0])
#        for a in range(0, total_page):
#            team = response.xpath('//*[@id="_container_zhixing"]/div/div[1]/table/tbody/tr')
#            for i in team:
#                # 立案日期
#                execute_date = if_exist(i.xpath('td[1]/span/text()'))
#                # 执行标的
#                execute_matter = if_exist(i.xpath('td[2]/span/text()'))
#                # 案号
#                execute_type = if_exist(i.xpath('td[3]/span/text()'))
#                # 执行法院
#                execute_court = if_exist(i.xpath('td[4]/span/text()'))
#                print(execute_date, execute_matter, execute_type,execute_court)
#                c = [execute_date, execute_matter, execute_type,execute_court]
#                execute_person.append(c)
#            next_page = driver.find_element_by_xpath('//*[@id="_container_zhixing"]/div/div[2]/ul/li[last()]/a')
#            turn_page(next_xpath=next_page)
#            response = etree.HTML(driver.page_source)
            
#开庭公告
    announcement_court = []
    announcementcourt_total_page = response.xpath('//*[@id="_container_announcementcourt"]/div/div[2]/div/text()')
    if len(announcementcourt_total_page) > 0:
        total_page = int(announcementcourt_total_page[0])
        for a in range(0, total_page):
            team = response.xpath('//*[@id="_container_announcementcourt"]/div/div[1]/table/tbody/tr')
            for i in team:
                # 开庭日期
                announcementcourt_date = if_exist(i.xpath('td[1]/text()'))
                # 案由
                announcementcourt_matter = if_exist(i.xpath('td[2]/span/text()'))
                # 原告/上诉人
                announcementcourt_appellor = if_exist(i.xpath('td[3]/div/span/text()'))
                if (announcementcourt_appellor == ''):
                    announcementcourt_appellor = if_exist(i.xpath('td[3]/div/a/text()'))
                # 被告/被上诉人
                announcementcourt_appellee = if_exist(i.xpath('td[4]/div/a/text()'))
                print(announcementcourt_date, announcementcourt_matter, announcementcourt_appellor,announcementcourt_appellee)
                c = [announcementcourt_date, announcementcourt_matter, announcementcourt_appellor,announcementcourt_appellee]
                announcement_court.append(c)
            next_page = driver.find_element_by_xpath('//*[@id="_container_announcementcourt"]/div/div[2]/ul/li[last()]/a')
            turn_page(next_xpath=next_page)
            response = etree.HTML(driver.page_source)
            
    #print(res_dic)





#    InsertData('company_info',res_dic)

