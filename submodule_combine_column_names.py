import pandas as pd
import numpy as np

def los(elem):
    # initialize an empty string
    str1 = ""

    if len(elem) > 1:

        listToStr = '~'.join([str(ele) for ele in elem])

        return listToStr.replace("~", ", ").replace("APT", "APT ").lower()

    else:

        for ele in elem:
            str1 += ele

        return str1.replace("APT", "APT ").lower()

def dedup_list(lst):

    #dedup
    mylist = list(dict.fromkeys(lst))

    if len(mylist) > 1:
        try:
            # remove empty
            mylist.remove("nil")

            return mylist

        except ValueError:

            return mylist

    else:

        return mylist


#----------------------------Combine APT Name Columns----------------------------#

def combine_column_names(df):

    col_name_list = []

    name_list = []

    df.columns = df.iloc[0]

    df = df[1:]

    df1 = df.dropna(subset=['Common Name'])

    df_filtered = df1[df1['Common Name'] != "?"]

    df2 = df_filtered.replace(np.nan, "nil")
    # df2 = df1.replace('nan', "nan")

    col_list = df2.columns.values.tolist()

    for i in range(len(col_list)):

        if col_list[i] == 'MITRE ATT&CK':

            mitre_attack_col_ref = i

        else:

            no_action = "no_action"

    for j in range(0, mitre_attack_col_ref):
        col_name_list.append(col_list[j])

    # print(col_name_list)

    for index, row in df2.iterrows():

        row_list = []
        for j in col_name_list:

            row_list.append(row[j])

            ListToString = los(dedup_list(row_list))

        name_list.append(ListToString)

    df2["Common Name"] = name_list

    df_dropped = df2.drop(df2.columns.difference(
        ["Common Name", "MITRE ATT&CK", "Origin", "Toolset / Malware", "Targets", "Modus Operandi"]), axis=1,
                          inplace=False)

    return df_dropped
