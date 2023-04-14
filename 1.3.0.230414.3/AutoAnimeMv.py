#!/usr/bin/python3
#coding:utf-8
from sys import argv
from os import system
from time import sleep
from re import findall,search,sub,I

def TitleMatch(VideoName):
    Season = '01' #定义初始剧季为1
    #匹配待去除
    SubtitleGroupDate = ['字幕','Raws','sub','汉化','搬运','月新番','Airota','Comicat','DMHY','NC-Raws','ANi','LoliHouse','Sakurato','TSDM','LoveEcho','EMe','Sakura','SweetSub','AHU-SUB','VCB-Studio','GM-Team','MingY','cc动漫','推しの子','喵萌奶茶屋','天月搬运组','萝莉社活动室','千夏生活向上委员会','酷漫404','拨雪寻春','霜庭云花Sub','FSD炸鸽社','雪飘工作室','丸子家族','驯兽师联盟','肥猫压制','离谱','虹咲学园烤肉同好会','AQUA工作室','晨曦制作','夜莺家族','Liella!の烧烤摊']
    #精准待去除
    FirstIntKeyWord = ['仅限港澳台地区']

    FileType = search(r'(.*?\.)',VideoName[::-1],flags=I).group()[::-1] #匹配视频文件格式
    #统一意外字符
    VideoName = sub(r',|，| ','-',VideoName,flags=I) 
    VideoName = sub(r'[^A-Za-z0-9_\s&/\-\u4e00-\u9fa5]','=',VideoName,flags=I)
    #匹配剧集
    Episodes = findall(r'[^0-9a-z\u4e00-\u9fa5][0-2]{1}[0-9]{1}[^0-9\u4e00-\u9fa5]',VideoName,flags=I)[0].strip(" =-_eE")
    #通过剧集截断文件名
    VideoName = sub(r'%s.*'%Episodes,'',VideoName,flags=I)
    #开始去除其他字符
    for i in range(len(FirstIntKeyWord)):
        VideoName = sub(r'%s'%FirstIntKeyWord[i],'',VideoName,flags=I)
    for i in range(len(SubtitleGroupDate)):
        VideoName = sub(r'=.*?%s.*?='%SubtitleGroupDate[i],'',VideoName,flags=I)
    VideoName = VideoName.replace('=','').replace(' ','').strip('-')
    #匹配剧季
    if ('/' in VideoName) == True: #按'/'进行双语言分类
        VideoName = VideoName.split("/", 1)
        #print(VideoName[1].replace('-','').isalnum())
        if VideoName[1].replace('-','').isalnum() == True: #双语言(中英)分类匹配英文Name中的剧季
            if search(r'[0-9]{0,1}[0-9]{1}S',VideoName[1][::-1],flags=I) != None :
                Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[1][::-1],flags=I).group(0)[::-1]
                TrueVideoName = VideoName[1].strip(Season)
                Season = search(r'[0-9]{0,1}[0-9]{1}S',VideoName[1][::-1],flags=I).group(0)[::-1].strip('Ss')
                #print(Season)
    elif search(r'季.*?第|[0-9]{0,1}[0-9]{1}S',VideoName[::-1],flags=I) != None :#单语言(中/英)匹配是否存在剧季
            Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1]
            TrueVideoName = VideoName.strip(Season)
            Season = search(r'(季.*?第|[0-9]{0,1}[0-9]{1}S)',VideoName[::-1],flags=I).group(0)[::-1].strip('第季Ss')
            if Season.isdigit() == True :
                #print(Season)
                pass
            else:#中文剧季转化
                digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
                Season = digit[Season]
                #print(Season)
    else:
        TrueVideoName = VideoName 
    TrueVideoName = TrueVideoName.strip('-')
    print(TrueVideoName,Season)
    return Season,Episodes,TrueVideoName,FileType

def GetArgv():#接受参数
    SavePath,VideoName,Star = argv[1],argv[2],argv[3]
    if Star != '动漫':#筛选'分类'
        exit()
    return SavePath,VideoName

def AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType):#整理+重命名
    NewName = f"S{Season}E{Episodes}{FileType}"
    NewVideoDir = f"{VideoTrueName}/Season_01"
    system(f'mkdir -p {SavePath}/{NewVideoDir}')
    sleep(2)
    system(f'mv "/{SavePath}/{VideoName}"  "{SavePath}/{NewVideoDir}/{NewName}"')

def Test(test):#测试TitleMatch函数
    return TitleMatch(test)

if __name__ == "__main__":
   #sleep(15)
   SavePath,VideoName = GetArgv()
   Season,Episodes,VideoTrueName,FileType = TitleMatch(VideoName)
   AutoMv(SavePath,VideoName,Season,Episodes,VideoTrueName,FileType)

