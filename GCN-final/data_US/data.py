import pandas as pd
import numpy as np
from geopy.distance import geodesic

df = pd.read_csv('time_series_covid19_confirmed_US.csv',index_col = 10)
df = df.drop(df[df.Lat==0].index) #清洗
df = df.sample(n=500)
#print(df)
df_graph = df.iloc[:,8:10]
df_confirmed = df.iloc[:,10:]
df_graph.to_csv('graph.csv')
df_confirmed.to_csv('confirmed.csv')
#df_graph = df.iloc[:5,8:10]
city_or_area_num = len(df_graph.index)
#print(city_or_area_num)
distance = np.full((city_or_area_num, city_or_area_num), np.nan)
col = -1
row = 0
tot = city_or_area_num*city_or_area_num
cnt = 0

for index1,row1 in df_graph.iterrows():
    col += 1
    row = -1
    Lat1 = row1['Lat']
    Lng1 = row1['Long_']
    for index2,row2 in df_graph.iterrows():
        cnt+=1
        row += 1
        Lat2 = row2['Lat']
        Lng2 = row2['Long_']
        if index1 == index2:
            distance[col][row] = 0
        elif np.isnan(distance[col][row]):
            distance[col][row] = round(geodesic((Lat1,Lng1), (Lat2,Lng2)).km,2)
            distance[row][col] = distance[col][row]
        if cnt % 1000 == 0:
            print('{}%'.format(round(cnt/tot*100,2)))

np.savetxt(fname="data.csv", X=distance, fmt="%.2f" ,delimiter=",")

#b = np.loadtxt(fname="data.csv", dtype=np.float, delimiter=",")
iu1 = np.triu_indices(city_or_area_num)
ravel_distance = distance[iu1]
#print(ravel_distance)
sorted_distance = np.sort(ravel_distance)
length = len(sorted_distance)
#----
split_a_index = round(length*1/5)
split_b_index = round(length*2/5)
split_c_index = round(length*3/5)
split_d_index = round(length*4/5)

split_a = sorted_distance[split_a_index]
split_b = sorted_distance[split_b_index]
split_c = sorted_distance[split_c_index]
split_d = sorted_distance[split_d_index]

relation1 = np.full((city_or_area_num, city_or_area_num), 0)
relation2 = np.full((city_or_area_num, city_or_area_num), 0)
relation3 = np.full((city_or_area_num, city_or_area_num), 0)
relation4 = np.full((city_or_area_num, city_or_area_num), 0)

#print(split_a,split_b,split_c)

for i in range(city_or_area_num):
    for j in range(city_or_area_num):
        dis = distance[i][j]
        if dis <= split_a:
            relation1[i][j] = 1
        if dis <= split_b:
            relation2[i][j] = 1
        if dis <= split_c:
            relation3[i][j] = 1
        if dis <= split_d:
            relation4[i][j] = 1

np.savetxt(fname="relation1.csv", X=relation1, fmt="%d",delimiter=",")
np.savetxt(fname="relation2.csv", X=relation2, fmt="%d",delimiter=",")
np.savetxt(fname="relation3.csv", X=relation3, fmt="%d",delimiter=",")
np.savetxt(fname="relation4.csv", X=relation4, fmt="%d",delimiter=",")

print(distance)

        
#print(df_confirmed)
