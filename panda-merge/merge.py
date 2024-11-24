import tkinter as tk
import pandas as pd


def merge(files=[],text=''):
    
    index_columns = ['资产名称', '账面价值', '取得日期','账面数量/面积']
    input_columns = [
        '资产编号','资产名称',  '账面价值','取得日期','规格型号',
        '使用部门','账面数量/面积','实有数量/面积','盘点结果',
        '使用状况','备注'
    ]
    output_columns = input_columns

    dfs = []
    for f in files:
        #将选择的文件读入到dataFrame
        text.delete('1.0', tk.END)
        text.insert('1.0', F"正在读取{f}")
        text.update()
        tmp = pd.read_excel(f, usecols=input_columns)
        tmp.drop(index=0, inplace=True)#删除第一个为列号的记录
        dfs.append(tmp)
    #合并读入的dataFrame
    df = pd.concat(dfs)

    text.delete('1.0', tk.END)
    tip = F"合并前：账面总值：{df['账面价值'].sum().round(2)} 数量：{df['账面数量/面积'].sum().round(2)}\n"
    text.insert('1.0', tip)
    text.insert('2.0', F"合并前行数：{len(df)}\n\n")
    text.update()
        
    #数重复的数量写入一个新字段；然后去重
    df['count'] = df.groupby(index_columns).transform('size')
    df = df.drop_duplicates(subset=index_columns)
    #调整相关列的值
    df['账面数量/面积'] = df['账面数量/面积']*df['count']
    df['实有数量/面积'] = df['账面数量/面积']
    df['账面价值'] = df['账面价值']*df['count']

    tip = F"合并后：账面总值：{df['账面价值'].sum().round(2)} 数量：{df['账面数量/面积'].sum().round(2)}\n"
    text.insert('3.0', tip)
    text.insert('4.0', F"合并后行数：{len(df)}")
    text.update()

    df.to_excel('output.xlsx', index=False, columns=output_columns)