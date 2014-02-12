import matplotlib.pyplot as plt
import pandas as pd
##

def wait_time(row):
	return sum(row['H1_Wait':'H9_Wait'])

def play_time(row):
	return sum(row['H1_Play':'H9_Play'])
	
ttn= {'fast': 3, 'medium': 2, 'slow': 1}
def type_to_num(type):
	return ttn[type]

df= pd.read_csv('prty_player_data.txt', sep='\t', index_col= False, 
				iterator= True, chunksize= 1000)				
df2= pd.concat([chunk for chunk in df], ignore_index= True)

srtd= df2.sort(columns= ['ID'])
srtd['Wait Time']= srtd.apply(wait_time, axis= 1)
srtd['Play Time']= srtd.apply(play_time, axis= 1)
#srtd['TTN']= srtd['Type'].apply(type_to_num)
#grpd= srtd.groupby(by= ['Type'])
#print grpd[['Wait Time', 'Play Time']].mean()
srtd_mean= srtd[['Wait Time', 'Play Time']].mean()
srtd_std= srtd[['Wait Time', 'Play Time']].std()
print srtd_mean
print srtd_std
# plt.scatter(srtd['Arr. Time'], srtd['TTN'], alpha= 0.2)
# plt.show()