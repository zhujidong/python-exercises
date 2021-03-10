import tkinter as tk
on_hit = False#标记，这是一个全局变量#
window = tk.Tk()#生成GUI框架#
var = tk.StringVar()#申请一个string类型的全局变量#

window.title('测试')
window.geometry('300x200')
l = tk.Label(window,textvariable = var,bg = 'green',font =('Arial',12),width = 15,heigh = 2)#类似于文本数据的控制显示#
l.pack()
def Hit_it():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set('Hit Online')
    else:
        on_hit = False
        var.set('')
b = tk.Button(window,text = 'Hit_it',command = Hit_it)
b.pack()
window.mainloop()