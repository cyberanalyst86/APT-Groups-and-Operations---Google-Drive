import pandas as pd
import re
import numpy as np
import openpyxl
from submodule_combine_column_names import *
from submodule_dedup_dataframe import *

#----------------------------Declare Variables----------------------------#

dataframe_list = []

#----------------------------Declare File Paths----------------------------#
input_filepath = "C:\\Users\Admin\\Downloads\\APT_Excel\\APT Groups and Operations.xlsx"
output_filepath = "C:\\Users\Admin\\Downloads\\APT_Excel\\deduplicated.xlsx"

#----------------------------Define Excel Sheets ----------------------------#

sheet_list = ["China", "Russia", "North Korea", "Iran", "Israel", "NATO", "Middle East", "Others", "Unknown"]

#----------------------------Iterate Through Excel Sheets------------------------------#
for sheet in sheet_list:

    print("process " + str(sheet))

    location_list = []

    df = pd.read_excel(input_filepath, sheet_name=sheet)

    df_new = combine_column_names(df)

# ----------------------------Tag APT Country of Origin to DataFrame-----------------------------#

    for i in range(len(df_new.index)):

        location_list.append(sheet)

    df_new["Location"] = location_list

    dataframe_list.append(df_new)

df_concat = pd.concat(dataframe_list)

# ----------------------------Tag Arbitary ID to DataFrame for Subsequent Reference-----------------------------#

id_lst = []

for i in range(len(df_concat["Common Name"])):
    id = i + 100
    id_lst.append(id)


df_concat["id"] = id_lst

# ----------------------------Create Index Column with the IDs-----------------------------#

index_list = df_concat["id"].values.tolist()

df_concat["Index"] = index_list

# ----------------------------Discover Duplicated Rows with Matching APT Names-----------------------------#

df_dup = find_dup(df_concat)

# ----------------------------Deduplicate the Dataframe-----------------------------#

df_dedup = df_dup.groupby(['id']).agg(lambda col: ','.join(col))

df_final = dedup_within(df_dedup)

# ----------------------------Remove Unecessary Content from DataFrame-----------------------------#

df_filtered = df_final[df_final['Common Name'] != "???"]

# ----------------------------Re-Tag Arbitary ID to DataFrame for Subsequent Reference-----------------------------#

range_list = df_filtered["Common Name"].values.tolist()

id_lst = []

for i in range(len(range_list)):
    id = i + 100
    id_lst.append(id)

df_filtered["id"] = id_lst

# ----------------------------Output Deduplicated Dataframe to Excel-----------------------------#

df_filtered.drop_duplicates(subset=['Common Name']).to_excel(output_filepath, index=False)