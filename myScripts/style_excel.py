from  StyleFrame import StyleFrame , utils , Styler
import pandas as pd
import numpy as np
# sf = StyleFrame.read_excel("../report/(4._.2020)/params_result_222_1.xlsx", read_style=True)
df = pd.read_excel("../report/(4._.2020)/params_result_222_1.xlsx")

# sf.apply_style_by_indexes(indexes_to_style=sf[sf['T5_c_uci'] > -10],
#                           cols_to_style=['T5_c_uci'],
#                           styler_obj=Styler(bg_color='c4fcd5', bold=True, font_size=10))
# sf1= sf["T5_c_uci"]
# sf1.apply_style_by_indexes(indexes_to_style=sf[sf['T5_c_uci'] > -10],
#                           cols_to_style=['T5_c_uci'],
#                           styler_obj=Styler(bg_color='c4fcd5', bold=True, font_size=10))

# cols =[x.value for x in sf.columns]

# lst = [StyleFrame({'index':range(len(sf))}),
#        StyleFrame({'index':range(len(sf))}),
#        StyleFrame({'index':range(len(sf))}),
#        StyleFrame({'index':range(len(sf))})
#        ]
def create_df(datapath):
    df = pd.read_excel(datapath)
    cols =df.keys()
    lst = [
        pd.DataFrame(df,columns=['model','version','ntopics','alpha','beta']),
        pd.DataFrame(df,columns=['model','version','ntopics','alpha','beta']),
        pd.DataFrame(df,columns=['model','version','ntopics','alpha','beta']),
        pd.DataFrame(df,columns=['model','version','ntopics','alpha','beta']),
       ]
    for col in cols:
        cs = col.split("_")
        if len (cs) == 4:
            if cs[-3][-4:] =='1000':
                lst[0][col]= df[col].apply(lambda x: round(x,4)).values
            elif cs[-3][-4:] =='2000':
                lst[1][col]= df[col].apply(lambda x: round(x,4)).values
            elif cs[-3][-4:] =='8000':
                lst[2][col]= df[col].apply(lambda x: round(x,4)).values
        elif len (cs) == 3:
            lst[3][col]= df[col].apply(lambda x: round(x,4)).values
    new_lst = []
    for d,l in  zip(lst,["1000","2000","8000","total"]):
        new_lst.append((d,l))
    return new_lst

def style_sf(sf,sf_lst,label,colormap):
    cols =[x.value for x in sf.columns]
    topics = [x.value for x in sf['ntopics'].unique()]
    for col in cols:
        cs = col.split("_")
        if len(cs)>=3:
            sf.apply_style_by_indexes(indexes_to_style=sf[sf[col]!= None],
                                      cols_to_style=[col],
                                      styler_obj=Styler(bg_color=colormap[cs[-1]],
                                                        font_size=8))
            max_ind = sf[sf[col]==sf[col].max().value ][0].value
            sf.apply_style_by_indexes(indexes_to_style=sf[sf[col]==sf[col].max().value ],
                                      cols_to_style=[col],
                                      styler_obj=Styler(font_color=colormap['max'],
                                                        font_size=10,
                                                        bold = True
                                                        ))
            for t in topics:
                ind = np.argmax(sf.iloc[sf[sf['ntopics']==t]][col].values)
                ind = sf.iloc[sf[sf['ntopics']==t]][col].index[0].value + ind
                if ind == max_ind: continue
                sf.apply_style_by_indexes(indexes_to_style=[ind],
                                          cols_to_style=[col],
                                          styler_obj=Styler(bg_color=colormap[cs[-1]],
                                                            font_color=colormap['max2'],
                                                            font_size=10))

    sf_lst.append((sf,label))
    return sf_lst

def create_sf(lst,colormap):
    sf_lst = []
    for df,label in lst:
        sf = StyleFrame(df)
        sf_lst = style_sf(sf,sf_lst,label,colormap)
    return sf_lst

def creat_output(lst,outputpath):
    ew = StyleFrame.ExcelWriter(outputpath)
    for sf ,label in lst:
        sf.to_excel(ew,sheet_name=label)
    ew.save()

if __name__=="__main__":
    datapath = f"../params_result_total.xlsx"
    outputpath = f"../report/params_result_total_styled.xlsx"
    colormap ={
        "npmi":'fce5c7',
        "mass":'e4c5f9',
        "v":'fcd1d1',
        "uci":'ebf9d4',
        "max":"e00000",
        "max2":"3e31f7"

    }
    df_lst = create_df(datapath)
    sf_lst = create_sf(df_lst,colormap)
    creat_output(sf_lst,outputpath)


