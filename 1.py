# regular
'''изучаю регулярные выражения, tkinter и bs4'''

import requests
import re
from bs4 import BeautifulSoup
from tkinter import Tk, BOTH, Listbox, StringVar, Message, END
from tkinter.ttk import Frame

''' 
пример кода
<?xml version="1.0" encoding="windows-1251"?><ValCurs Date="19.02.2021" name="Foreign Currency Market">' 
<Valute ID="R01010"><NumCode>036</NumCode><CharCode>AUD</CharCode><Nominal>1</Nominal><Name>Австралийский ' 
доллар</Name><Value>57,2424</Value></Valute><Valute ID="R01020A"><NumCode>944</NumCode><CharCode>AZN</CharCode>' 
<Nominal>1</Nominal><Name>Азербайджанский манат</Name><Value>43,4229</Value></Valute><Valute ID="R01035">' 
<NumCode>826</NumCode><CharCode>GBP</CharCode><Nominal>1</Nominal><Name>Фунт стерлингов Соединенного королевства</Name>'
<Value>102,4742</Value></Valute><Valute ID="R01060"><NumCode>051</NumCode><CharCode>AMD</CharCode>' 
<Nominal>100</Nominal><Name>Армянских драмов</Name><Value>14,0704</Value></Valute><Valute ID="R01090B">' 
<NumCode>933</NumCode><CharCode>BYN</CharCode><Nominal>1</Nominal><Name>Белорусский рубль</Name>' 
<Value>28,4749</Value></Valute><Valute ID="R01100"><NumCode>975</NumCode><CharCode>BGN</CharCode>' 
<Nominal>1</Nominal><Name>Болгарский лев</Name><Value>45,4703</Value></Valute><Valute ID="R01115">' 
<NumCode>986</NumCode><CharCode>BRL</CharCode><Nominal>1</Nominal><Name>Бразильский реал</Name>' 
<Value>13,6349</Value></Valute></ValCurs>'
'''
class Show_me(Frame):
    def __init__(self, in_dict):
        super ().__init__ ()
        self.dictionary = in_dict
        self.my_list = []
        self.initUI ()


    def initUI(self):
        self.master.title ("Курс рубля по отношению к другим валютам")
        self.pack (fill = BOTH, expand = 1)

        lb = Listbox (self)
        '''Заполняю логику списка отображения'''
        for key_to_show in self.dictionary.keys():
            lb.insert (END, key_to_show)
            self.my_list.append(key_to_show)


        '''реакция на выбор'''
        lb.bind ("<<ListboxSelect>>", self.onSelect)
        lb.config (height = 10, width = 50)
        lb.pack (pady = 15)


        '''функция отображения выбора '''
        self.var = StringVar ()
        self.label = Message (self,
                            foreground = 'black',
                            font = 'Arial 10',
                            width = 500,
                            textvariable = self.var)
        self.label.pack ()


    '''функция логики отображения выбора'''
    def onSelect(self, val):
        sender = val.widget
        index = sender.curselection ()[0]
        value = 'Курс российского рубля' + '1 к ' + \
                (self.dictionary.get(self.my_list[index]))[1] + ' ' + \
                'к этой валюте = ' + (self.dictionary.get(self.my_list[index]))[0]
        self.var.set (value)

''' Описание поиска регулярных выражений для описания валюты
\b[А-я]+\b одно слово в валюте
\b[А-я]+\s+[А-я]+\b два слова в валюте
\b[А-я]+\s+[А-я]+\s+[А-я]+\b три слова в валюте
\b[А-я]+\s+[А-я]+\s+[А-я]+\s+[А-я]+\b четыре слова в валюте
\b[А-Я]+\s+\S[А-я]+\s+[А-я]+\s+[А-я]+\S\b четыре слова в валюте СДР
'''

class Get_dict_html():
    def __init__(self, url_path):
        self._url_p = url_path
        self._html_str = self.get_html()


    '''Функция получения странички'''
    def get_html(self):
        new_response = requests.get(self._url_p)
        return new_response.text


    '''Функция отчистки странички от мусора и формирования словаря'''
    def get_me_info(self, html_str):
        my_obj_soup = BeautifulSoup (html_str, 'lxml')
        nominal_re = re.findall (r'\b\d+\b', str (my_obj_soup.find_all ('nominal')))
        value_re = re.findall (r'\d+,\d{4}', str (my_obj_soup.find_all ('value')))
        name_re = re.findall (r'\b[А-Я]+\s+\S[А-я]+\s+[А-я]+\s+[А-я]+\b'
                              r'|\b[А-я]+\s+[А-я]+\s+[А-я]+\s+[А-я]+\b'
                              r'|\b[А-я]+\s+[А-я]+\s+[А-я]+\b'
                              r'|\b[А-я]+\s+[А-я]+\b'
                              r'|\b[А-я]+\b', str (my_obj_soup.find_all ('name')))
        return {name_re[index]: [value_re[index], nominal_re[index]] for index in range (len (nominal_re))}


class Visio():

    @staticmethod
    def selection_window(dictionary):
        window = Tk ()
        window.geometry ("500x300+700+350")
        Show_me (dictionary)
        window.mainloop ()
        pass




'''Рабочая функция'''
def main():
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    Visio.selection_window(Get_dict_html(url).get_me_info(Get_dict_html(url)._html_str))
    pass


if __name__ == '__main__':
    main()
    pass