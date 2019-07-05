import kivy
from kivy import Config
Config.read("setting.ini")
from kivy.app import App
from kivy.core.text import LabelBase


from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
import re

kivy.require('1.0.7')


kivy.resources.resource_add_path('font/')
font = kivy.resources.resource_find('Alibaba-PuHuiTi-Light.ttf')

class FileProcess:
    def modifyFile(self, file):
        file.encode("UTF-8")
        temResult = re.split(r"[…、：\n]", file)
        temReturn = []
        for tem in temResult:
            if self.validParen(tem):
                temReturn.append(tem)
            else:
                tem = tem.replace('（', "")
                tem = tem.replace('）', "")
                temReturn.append(tem)
        temReturn = [x.strip() for x in temReturn if x.strip() != '']
        return temReturn

    def validParen(self, str):
        a = {'（': '）'}
        l = [None]
        for i in str:
            if i in a and a[i] == l[-1]:
                l.pop()
            else:
                l.append(i)
        return len(l) == 1


class GarbageSorting(object):
    Bin_Recycle = []
    Bin_Harmful = []
    Bin_Wet = []
    Bin_Dry = []

    File_recycle = []
    File_harmful = []
    File_wet = []
    File_dry = []

    def __init__(self):
        self.Bin_Recycle = []
        self.Bin_Harmful = []
        self.Bin_Wet = []
        self.Bin_Dry = []
        self.loadFile()
        print([{
            'Recycle bin': self.Bin_Recycle,
            'Harmful bin': self.Bin_Harmful,
            'Wet bin': self.Bin_Wet,
            'Dry bin': self.Bin_Dry
        }])

    def loadFile(self):
        self.File_recycle = open('recycleGarbageList.txt', 'r', encoding='UTF-8').read()
        self.File_harmful = open('harmfulGarbageList.txt', 'r', encoding='UTF-8').read()
        self.File_wet = open('wetGarbageList.txt', 'r', encoding='UTF-8').read()
        self.File_dry = open('dryGarbageList.txt', 'r', encoding='UTF-8').read()

        fp = FileProcess()
        self.File_recycle = fp.modifyFile(self.File_recycle)
        self.File_harmful = fp.modifyFile(self.File_harmful)
        self.File_wet = fp.modifyFile(self.File_wet)
        self.File_dry = fp.modifyFile(self.File_dry)

    def search(self, garbageThrow):
        if garbageThrow in self.File_recycle:
            self.Bin_Recycle.append(garbageThrow)
            return '丢进可回收垃圾桶!'
        elif garbageThrow in self.File_harmful:
            self.Bin_Harmful.append(garbageThrow)
            return '丢进有害垃圾桶!'
        elif garbageThrow in self.File_wet:
            self.Bin_Wet.append(garbageThrow)
            return '丢进湿垃圾桶!'
        elif garbageThrow in self.File_dry:
            self.Bin_Dry.append(garbageThrow)
            return '丢进干垃圾桶!'
        else:
            return '您丢的垃圾"%s"不属于生活垃圾或系统暂未识别!' % garbageThrow

    def showBin(self):
        print([{
            'Recycle bin': self.Bin_Recycle,
            'Harmful bin': self.Bin_Harmful,
            'Wet bin': self.Bin_Wet,
            'Dry bin': self.Bin_Dry
        }])
        self.showFile()
        return [{
            'Recycle bin': self.Bin_Recycle,
            'Harmful bin': self.Bin_Harmful,
            'Wet bin': self.Bin_Wet,
            'Dry bin': self.Bin_Dry
        }]

    def showFile(self):
        print([{
            'Recycle file': self.File_recycle,
            'Harmful file': self.File_harmful,
            'Wet file': self.File_wet,
            'Dry file': self.File_dry
        }])

    def clearBin(self):
        self.__init__()


class SortingApp(App):
    newSort = GarbageSorting()

    def on_click(self):
        result = self.entrence(self.text.get())
        print(result)
        if not self.isEmpty(result):
            tk.messagebox.showinfo("结果", result)
            self.text.set("")

    def on_click_bin(self):
        binList = self.newSort.showBin()
        tk.messagebox.showinfo("结果", binList)

    def on_click_clear(self):
        self.newSort.__init__()




class MyFirstApp(App):
    newSort = GarbageSorting()

    def on_click(self, btn):
        inputStr = self.textinput.text
        print("calling with %s" % inputStr)

        if self.isEmpty(inputStr):
            pass
        elif "clear" == inputStr:
            self.newSort.__init__()
        elif "showFile" == inputStr:
            self.newSort.showFile()
        else:
            self.label.text =self.newSort.search(inputStr)

    def on_click_bin(self, btn):
        binList = self.newSort.showBin()
        strshow=""
        for tem in binList:
            strshow+="".join(tem)
        self.label.text= strshow

    def on_click_clear(self, btn):
        self.newSort.__init__()

    def isEmpty(self, str):
        if str is None:
            return True
        elif len(str) == 0 or str.isspace():
            return True
        return False


    def build(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=20)
        txly = BoxLayout(orientation='vertical', padding=20, spacing=20)
        btnly = BoxLayout(orientation='horizontal', padding=20, spacing=20)
        imgbg = Image(source='bg.png')
        self.textinput = TextInput(hint_text='garbage name', font_size=30,font_name='Alibaba-PuHuiTi-Light')
        self.label = Label(font_name='Alibaba-PuHuiTi-Light')

        clearbtn = Button(text='Clear')
        clearbtn.bind(on_press=self.on_click_clear)
        confirmbtn = Button(text='Throw')
        confirmbtn.bind(on_press=self.on_click)
        showbtn = Button(text='Show bin')
        showbtn.bind(on_press=self.on_click_bin)
        txly.add_widget(self.textinput)
        txly.add_widget(self.label)
        btnly.add_widget(confirmbtn)
        btnly.add_widget(clearbtn)
        btnly.add_widget(showbtn)
        root.add_widget(imgbg)
        root.add_widget(txly)
        root.add_widget(btnly)
        return root

if __name__ == '__main__':
    MyFirstApp().run()
