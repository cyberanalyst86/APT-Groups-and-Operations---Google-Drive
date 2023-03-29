import pandas as pd

def check_string(row):

    if type(row) != str:

        row_str = row.to_string()

    else:

        row_str = row

    return row_str

def dedup(lst):

    lower = (map(lambda x: x.lower(), lst))
    lowered = list(lower)

    dedup_list = list(dict.fromkeys(lowered))

    # initialize an empty string
    str1 = ""

    if type(dedup_list) == list:
    # traverse in the string

        if len(dedup_list ) > 1:

            listToStr = '~'.join([str(elem) for elem in dedup_list ])


            str1 = listToStr.replace("~", ", ")

            # return string
            return str1.replace("nil, ", "")

        else:

            listToStr = "".join([str(elem) for elem in dedup_list])

            str1 = listToStr

            return str1.replace("nil, ", "")

    else:

        # return string
        return dedup_list.replace("nil, ", "")

def dedup_list(lst):

    dedup_list = list(dict.fromkeys(lst))

    return dedup_list


def check_intersection(a_set, b_set, a, b):

    if a != b:

        if a_set & b_set:

            return True

        else:


            return False

    else:

        return False


def lower_case(lst):
    lower = (map(lambda x: x.lower(), lst))
    lowered = list(lower)

    return lowered

#----------------------------Find Duplication----------------------------#

def find_dup(df):

    df.set_index('Index', inplace=True)

    index_list = df.index.tolist()

    for i in range(len(index_list)):

        #df_aptmap["first seen"].loc[id]

        a = check_string(df["Common Name"].loc[index_list[i]])

        excel_lowercase1 = lower_case(list(a.split(", ")))

        a_set = set(excel_lowercase1)

        for j in range(len(index_list)):

            b = check_string(df["Common Name"].loc[index_list[j]])

            excel_lowercase2 = lower_case(list(b.split(", ")))

            b_set = set(excel_lowercase2)

            check = check_intersection(a_set, b_set,  a, b)

            if check:

                df.loc[index_list[j], ['id']] = df["id"].loc[index_list[i]]

            else:

                no_action = "no_action"


    return df

#----------------------------Deduplicate Row Content in the Dataframe----------------------------#

def dedup_within(df):

    index_list = df.index.tolist()

    for id in index_list:

        df.loc[id, ['Common Name']] = dedup(df["Common Name"].loc[id].split(","))
        df.loc[id, ['Origin']] = dedup(df["Origin"].loc[id].split(","))
        df.loc[id, ['Toolset / Malware']] = dedup(df["Toolset / Malware"].loc[id].split(","))
        df.loc[id, ['Targets']] = dedup(df["Targets"].loc[id].split(", "))
        df.loc[id, ['Modus Operandi']] = dedup(df["Modus Operandi"].loc[id].split(","))
        df.loc[id, ['Location']] = dedup(df["Location"].loc[id].split(","))
        df.loc[id, ['MITRE ATT&CK']] = dedup(df["MITRE ATT&CK"].loc[id].split(","))


    print("output------------------------------------------")

    return df
