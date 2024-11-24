import tkinter as tk
from tkinter import filedialog, messagebox
from time import sleep
from merge import merge


files = []


def open_files():
    # 打开文件选择对话框，允许选择多个文件
    global files
    files = filedialog.askopenfilenames(title="可按住Ctrl键多选", filetypes=(("Excel", "*.xlsx"),))
    if files:
        tip = F'您选择了{len(files)}文件：\n'+'\n'.join(files)+'\n请按 开始合并'
        text.delete('1.0', tk.END)
        text.insert('1.0',tip)

def merge_files():
    if files:
        merge(files,text)
        messagebox.showinfo("合并文件", F"合并完成，见output.xlsx")
    else:
        messagebox.showinfo("提示", "请先选择要合并的excel工作簿！")


def close_window():
    # 关闭窗口
    root.destroy()


# 创建主窗口
root = tk.Tk()
root.geometry('430x250')
root.title("盘点表同类合并")

tip = '将资产报表导出的盘点表中资产名称、账面价值、取得日期和账面数量四项相同的记录合并为一条，数量/面积与账面价格变为它们的和。\n\n'
tip = tip + '请一次选择所有要合并的盘点表，它们将被合并为一个文件。\n'
tip = tip + '（按Ctrl+鼠标左键多选；按shift+鼠标左键连续选）'
text = tk.Text(root, height=8, width=50, wrap='word', pady=5)
text.insert('1.0',tip)
text.pack()


# 创建并打开文件选择组件的按钮
open_button = tk.Button(root, text="选择所有需合并的excel", command=open_files)
open_button.pack()

# 创建合并按钮
merge_button = tk.Button(root, text="开始合并", command=merge_files)
merge_button.pack(side='left', padx=20)

# 创建关闭按钮
close_button = tk.Button(root, text="退出程序", command=close_window)
close_button.pack(side='right', padx=20)

# 运行主循环
root.mainloop()