#coding:utf-8
"""
综合项目:世行历史数据基本分类及其可视化
作者：吴星泽
日期:2020.06.10
"""

import csv
import math
import pygal
import pygal_maps_world  #导入需要使用的库


def read_csv(name_file, key, break_str, char): #读取原始csv文件的数据，格式为嵌套字典

    result={}

    with open(name_file, newline="")as csvfile:
        csvreader=csv.DictReader(csvfile, delimiter=break_str, quotechar=char)
        for row in csvreader:
            rowid=row[key]
            result[rowid]=row

    return result

def reconcile_countries(countries_plot, countries_gdp): #返回在世行有GDP数据的绘图库国家代码字典，以及没有世行GDP数据的国家代码集合

    
    dict_ = {}
    set_  = set()

    for pygal in countries_plot :
        if countries_plot[pygal] in countries_gdp :
            dict_[pygal] = countries_plot[pygal]   # 字典内容为在世行数据里的绘图库国家（键为绘图库各国家代码，值为对应的具体国名)

        else :
            set_.add(pygal)   #  集合内容为不在世行数据的绘图库国家代码

    tuple_ = (dict_, set_)

    return tuple_

def build_map(gdp_info, countries_plot, year):

    countries_year_gdp = {}
    set_2 = set()
    set_3 = dict()
    
    years_gdp = []
    
    for plot_countries_code in countries_plot :
        for isp_country_code in gdp_info :
            
            if gdp_info[isp_country_code]["Country Name"] == countries_plot[plot_countries_code] : # 判断绘图库里的国家在不在世界银行数据里
                
                gdp_number = ''
                country_imformations = []
                
                for country_imformation in gdp_info[isp_country_code] :
                    country_imformations.append(country_imformation)
                
                for year_1 in country_imformations[4:-1] :
                    gdp_number += gdp_info[isp_country_code][year_1]
                    
                if gdp_number == '' :
                    set_2.add(plot_countries_code)  # 把该国家归为不在世界银行数据里
                    
                else :
                    if gdp_info[isp_country_code][year] != '' :
                        
                        gdp_num = math.log10(float((gdp_info[isp_country_code][year])))
                        countries_year_gdp[plot_countries_code] = gdp_num    # 把该国家分类为该年有数据并以字典形式保存(键为绘图库中各国家代码，值为在具体年份(
                                                                                                        #  由year参数确定)所对应的世行GDP数据值)
                    else :
                        set_3[plot_countries_code] = '该年暂无数据'  # 把该国家分类为该年暂无数据
                        
                    # 当该绘图库里的国家在世界银行数据里时，判断该年有无数据，并进行分类（当其每一年的数据都没有时，把该国家归为不在世界银行数据里）
                    
                continue
    
    isp_countries = []
    for isp_country_code in gdp_info :
        isp_countries.append(gdp_info[isp_country_code]["Country Name"])

    in_countries, not_in_countries = reconcile_countries(countries_plot, isp_countries)
    
    for countries in not_in_countries :
        set_2.add(countries)
    # 绘图库里不在世界银行数据里的国家
    
    tuple_2 = (countries_year_gdp,set_2,set_3)
    
    return tuple_2
    

def render_world_map(gdpinfo, plot_countries, year, map_file): #将具体某年世界各国的GDP数据(包括缺少GDP数据以及只是在该年缺少GDP数据的国家)以地图形式可视化


    A_countries,B_countries,C_countries = build_map(gdpinfo, plot_countries, year)   # 导入清理好的数据，方便绘制到世界地图上

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = '世界银行%s年国家GDP数据'%(year)    #  添加图片标题
    worldmap_chart.add('该年在绘图库及世行有数据的国家及其GDP数据', A_countries)
    worldmap_chart.add('在绘图库数据里没有的国家',B_countries)
    worldmap_chart.add('该年在世行没有GDP数据的国家',C_countries)
    
    worldmap_chart.render()

    worldmap_chart.render_to_file(map_file)   # 输出生成 .svg 文件，查看时用浏览器打开

def test_render(year):  #测试函数
    """
    对各功能函数进行测试
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    } #定义数据字典
    
    gdp_csv = read_csv(gdpinfo['gdpfile'], gdpinfo['country_code'], gdpinfo['separator'], gdpinfo['quote'])

    pygal_countries = pygal.maps.world.COUNTRIES   # 获得绘图库pygal国家代码字典，读取pygal.maps.world中国家代码信息（为字典格式），其中键为pygal中各国代码，值为对应的具体国名
    
    isp_countries = []
    for isp_country_code in gdp_csv :
        isp_countries.append(gdp_csv[isp_country_code]["Country Name"])

    render_world_map(gdp_csv, pygal_countries, year, "isp_gdp_world_name_%s.svg"%(year))


#程序测试和运行
print("欢迎使用世行GDP数据可视化查询")
print('可以查询到1960-2015年的数据')
print("----------------------")
year=input("请输入需查询的具体年份:")

while float(year) < 1960 or float(year) > 2015 :
    
    print('对不起，不能查询到该年的数据\n可以查询到1960-2015年的数据')
    print("----------------------")
    print()
    year=input("请再次输入需查询的具体年份:")
    
else :
    test_render(year)
