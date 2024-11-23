import pandas as pd


def merge(files):
    
    index_columns = ['资产名称', '账面价值', '取得日期']
    output_cloumns = [
        '资产编号','资产名称',  '账面价值','取得日期','规格型号',
        '使用部门','账面数量/面积','实有数量/面积','盘点结果',
        '使用状况','备注'
    ]

    dfs = []
    cnt = 0
    for f in files:
        tmp = pd.read_excel(f)
        dfs.append(tmp)
        cnt = cnt + 1    
    df = pd.concat(dfs)

    df['实有数量/面积'] = df.groupby(index_columns).transform('size')
    df = df.drop_duplicates(subset=index_columns)
    df['账面数量/面积'] = df['实有数量/面积']
    df['账面价值' ] = df['账面价值' ] * df['账面数量/面积']
    
    df.to_excel('output.xlsx', index=False, columns=output_cloumns)
    return cnt