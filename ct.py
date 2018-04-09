#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 06:40:08 2018

@author: chen
"""

import pymysql


mySpiderSong='qq1'
def create_table():
    
    #自动建表语句
    db = pymysql.connect("localhost","root","315135","music" )  
   # db=pymysql.connect(host='127.0.0.1',user='root',passwd='315135',port=3306,db='music',charset='utf8mb4')
    cursor = db.cursor()   
    sql0 = """CREATE TABLE """+mySpiderSong+""" ( 
             userId INT(11), 
             nickname VARCHAR(60), 
             content VARCHAR(600), 
             time VARCHAR(19), 
             likedCount char(11), 
             beReplied INT(1))"""  
    cursor.execute(sql0)  
    print("CREATE TABLE OK")  
    #关闭数据库连接  
    db.close()   

create_table()