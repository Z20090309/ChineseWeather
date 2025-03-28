from tkinter import *
import requests



'''爬取'''
url = 'https://www.amap.com/service/cityList?version=202092419'
response = requests.get(url, verify=False)
dataAll = response.json()['data']['cityByLetter']
datalen = len(dataAll)


'''
抓取所有城市名称和编码
并存放到列表
生成字典
'''
citiseAndAdcodes = {}
cityName = []
adcodes = []
for i in dataAll:
    for x in range(len(dataAll[i])):
        name = dataAll[i][x]['name']
        cityName.append(name)
        adcode = dataAll[i][x]['adcode']
        adcodes.append(adcode)
        citiseAndAdcodes[f'{name}'] = adcode


class important:
    def __init__(self, code):
        urlCity = f'https://www.amap.com/service/weather?adcode={code}'
        self.response = requests.get(urlCity, verify=False)
    def now_time(self):
        weather_now = self.response.json()['data']['data'][0]['live']['weather_name']
        temperature = self.response.json()['data']['data'][0]['live']['temperature']
        return weather_now, temperature

    def today(self):
        min_temp = self.response.json()['data']['data'][0]['forecast_data'][0]['min_temp']
        max_temp = self.response.json()['data']['data'][0]['forecast_data'][0]['max_temp']
        weather_name = self.response.json()['data']['data'][0]['forecast_data'][0]['weather_name']
        return  max_temp, min_temp, weather_name
    def tomorrow(self):
        min_temp = self.response.json()['data']['data'][1]['forecast_data'][0]['min_temp']
        max_temp = self.response.json()['data']['data'][1]['forecast_data'][0]['max_temp']
        weather_name = self.response.json()['data']['data'][1]['forecast_data'][0]['weather_name']
        return max_temp, min_temp, weather_name



def on_button_click():
    # 获取输入框中的内容
    name = entry.get()
    if name == '张泽坤':
        output_label.config(text='恭喜你得到了作者的名字', font=('宋体', 20))
        return None
    if name == '王德胜':
        output_label.config(text='恭喜你得到了作者的御用男模的名字', font=('宋体', 20))
        return None
    code = citiseAndAdcodes[f'{name}']
    main = important(code)

    now_weather, now_temperature = main.now_time()
    today_max_temp, today_min_temp, today_weather = main.today()
    tomorrow_max_temp, tomorrow_min_temp, tomorrow_weather = main.tomorrow()
    output_label.config(text=f'{name}当前天气为：{now_weather}\n气温：{now_temperature}°C\n'
                             f'{name}今日天气为：{today_weather}\n气温：{today_min_temp}/{today_max_temp}°C\n'
                             f'{name}明日天气为：{tomorrow_weather}\n气温：{tomorrow_min_temp}/{tomorrow_max_temp}°C')

root = Tk()
root.title('高德天气查询')
root.geometry('1300x700')

txt = Text(root, width=200, height=45)

txt.insert(END, f'input(王德胜)有惊喜\n')

n = 0
for x, y in zip(cityName, adcodes):
    txt.insert(END, f'{x}:{y}\t')
    n += 1
    if n % 7 == 0:
        txt.insert(END, '\n\n')

button = Button(root, text='查询', command=on_button_click)
entry = Entry(root)
output_label = Label(root)
T = Label(root, text='请在下方输入城市名称')

T.pack()
entry.pack()
button.pack()
output_label.pack()
txt.pack()

# 运行主循环
root.mainloop()