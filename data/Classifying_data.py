
import pandas as pd

csv_files_data = ["Dataset71_80.csv", "Dataset83_86.csv", "Dataset87.csv", "Dataset88_100.csv",
                  "Dataset101_102.csv", "Dataset104_113.csv", "Dataset115_124.csv", "Dataset125_134.csv", "Dataset137_146.csv"]
df_data = pd.DataFrame(data=csv_files_data)
# Merging all the csv files
for i in csv_files_data:
    df = pd.read_csv(i)
    df_data = df_data.append(df, ignore_index=True)


df_50 = pd.read_csv("Dataset1-50.csv")

ls_1_20 = [i for i in range(6000, 15000)]
ls_21_40 = [i for i in range(0, 6000)]
ls_21_40_2 = [i for i in range(12000, 15000)]
ls_41_50 = [i for i in range(0, 12000)]

df_41_50 = df_50.drop(ls_41_50)
df_1_20 = df_50.drop(ls_1_20)
df_21_40 = df_50.drop(ls_21_40_2).drop(ls_21_40)

df_data = df_data.append(df_41_50, ignore_index=True)

df_data.to_csv('train.csv')
df_1_20.to_csv('test.csv')
df_21_40.to_csv("validation.csv")
