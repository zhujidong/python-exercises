import tkinter as tk
from tkinter import filedialog, messagebox

from merge import merge


files = []


def open_files():
    # 打开文件选择对话框，允许选择多个文件
    global files
    files = filedialog.askopenfilenames(title="选择文件", filetypes=(("所有文件", "*.xlsx"),))

def merge_files():
    if files:
        cnt = merge(files)
        messagebox.showinfo("合并文件", F"合并{cnt}个文件完成，见output.xlsx")
    else:
        messagebox.showinfo("提示", "请先选择要合并的excel工作簿！")


def close_window():
    # 关闭窗口
    root.destroy()


# 创建主窗口
root = tk.Tk()
root.title("文件处理窗口")

# 创建并打开文件选择组件的按钮
open_button = tk.Button(root, text="选择所有要合并的excel工作簿", command=open_files)
open_button.pack(side='top', padx=10, pady=5)

# 创建合并按钮
merge_button = tk.Button(root, text="合并", command=merge_files)
merge_button.pack(side='left', padx=10, pady=5)

# 创建关闭按钮
close_button = tk.Button(root, text="退出", command=close_window)
close_button.pack(side='right', padx=10, pady=5)

# 运行主循环
root.mainloop()
