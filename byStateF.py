import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os
from datetime import timedelta


'''This Programs will download current state data on Covid19 and graph it for you'''
#------------State_Data_From_Github------------- 
def get_data_State():
  site = 'https://covidtracking.com/api/v1/states/daily.csv'
  df =  pd.DataFrame(pd.read_csv(site, error_bad_lines=False))
  df.to_csv(r'/home/bot/Documents/daily.csv')

#code to check the timestamp of the csv file if more than one day old then execute the github function above 
def check_state_data():
  try:
    get_file_last_edit = datetime.date.fromtimestamp(os.stat('/home/bot/Documents/daily.csv').st_mtime)
  except FileNotFoundError:
    get_file_last_edit = get_data_State()
    get_file_last_edit = datetime.date.fromtimestamp(os.stat('/home/bot/Documents/daily.csv').st_mtime)
  get_today_date = datetime.date.today()
  if get_today_date > get_file_last_edit:
    get_data_State()
    print('Refreshing Data...')
  else:
    print('Data Up to Date.')
  df =  pd.DataFrame(pd.read_csv('/home/bot/Documents/daily.csv'))
  df_State = df[['date','state','death','deathIncrease','hospitalizedIncrease','hospitalizedCurrently','hospitalizedCumulative','positive', 'positiveIncrease']]
  df_State['date'] = pd.to_datetime(df_State['date'], format='%Y%m%d')
  df_State.fillna(0,inplace=True)
  return df_State

def plot_data(df,cat='deathIncrease'):
  df.groupby(['date', 'state']).sum()[cat].unstack().plot()
  plt.title("# By "+cat)
  plt.grid(True)
  plt.show()

    
def nDF_top_cat(df,top=5,d='death'):
  #python3 -c 'import byStateF; byStateF.plot_data(byStateF.nDF_top_cat(byStateF.check_state_data(),5,"hospitalizedCurrently"), "hospitalizedCurrently")'
  #get dataframe for the top 5 for deathincrease, then plot the positves
  df.sort_values('date', ascending=False)                              #sort df in decending order
  latest_record = df[df['date'] == df['date'].iloc[0]]                 #gets all deaths as of most recent date
  rec_sorted = latest_record.sort_values(d, ascending=False)           #sort all death, cummulative death
  top_10_State = list(rec_sorted['state'][0:top])                        #get top S states with most death in list
  total_state = df[df.state.isin(top_10_State)]                        #filter df on stop S state
  return total_state

def nDF_top_cat_days(df,top=5,cat='death', days=7):
  #python3 -c 'import byStateF; byStateF.plot_data(byStateF.nDF_top_cat_days(byStateF.check_state_data(),5,"deathIncrease",7),"positive")'
  #bring in data framen that for the top 5 states with the highest deathIncrease for last seven days, plot this positive cases
  df.sort_values('date', ascending=False)                              #sort df in decending order
  latest_record = df[df['date'] == df['date'].iloc[0]]                 #gets all deaths as of most recent date
  rec_sorted = latest_record.sort_values(cat, ascending=False)           #sort all death, cummulative death
  top_10_State = list(rec_sorted['state'][0:top])                        #get top S states with most death in list
  past_seven_days = df['date'].unique()[0:days] 
  total_state = df[df.state.isin(top_10_State) & df.date.isin(past_seven_days)]             #filter df on stop S state
  return total_state

def show_top_S(df,top=5,d='death'):
  #python3 -c 'import byStateF; print(byStateF.show_top_S(byStateF.check_state_data(),5, "deathIncrease"))'
  df.sort_values('date', ascending=False)
  latest_record = df[df['date'] == df['date'].iloc[0]]                 #gets all deaths as of the latest time period, one date
  rec_sorted = latest_record.sort_values(d, ascending=False)     #sort all death on that one day this is a cummulative death
  top_10_State = list(rec_sorted['state'][0:top])                        #get top states with most death
  total_state = rec_sorted[rec_sorted.state.isin(top_10_State)]
  return total_state

def get_states_in_list(df,l=['CA'],days=7):
  #python3 -c 'import byStateF; byStateF.plot_data(byStateF.get_states_in_list(byStateF.check_state_data(),["FL","CO","MI", "GA", "AZ", "AR"],14), "deathIncrease")'
  past_seven_days = df['date'].unique()[0:days]
  df = df[df.date.isin(past_seven_days) & df.state.isin(l)]
  return df

def state_growth_rate(df, cat="positive", b=7):
  #python3 -c 'import byStateF; print(byStateF.state_growth_rate(byStateF.check_state_data(),"positive",7))'
  State_current_back_value = []
  recent_data_date = df.iloc[0,0]                                   #get the current date from the dataframe
  backward_date = recent_data_date - timedelta(days=b)              #how many days back do you want to go
  list_of_state = df['state'].unique()                              #get list of all state and create a new df for just the growth rate
  array_state = {'State':list_of_state, 'Growth':0}                 #create a dic for of state and zero growth for df, will delete Growth later
  df_state = pd.DataFrame(array_state)                             #create df from the above dic
  #loop through all states, for the current value and back value for time horizon specified and cat and add to the lis State_current_back_value
  for i in list_of_state:
    current_cat_value = int(df.loc[(df['state']==i) & (df['date']==recent_data_date)][cat])
    backward_cat_value = int(df.loc[(df['state']==i) & (df['date']==backward_date)][cat])
    State_current_back_value.append([i,current_cat_value, backward_cat_value])
  df_growth_rate = pd.DataFrame(State_current_back_value, columns=['State', 'Current', 'Back']) #takes list from loop and convert to df
  inner_df_growth = pd.merge(df_state, df_growth_rate, on='State', how='inner') #join the df_state and the df_growth_rate
  inner_df_growth[cat+ '+/-'] = inner_df_growth['Current']-inner_df_growth['Back']
  inner_df_growth[cat+ '%+/-'] = (inner_df_growth['Current']-inner_df_growth['Back'])/inner_df_growth['Back']
  inner_df_growth['Growth'] = (inner_df_growth['Current']-inner_df_growth['Back'])/b
  inner_df_growth.index.name =cat
  #inner_df_growth.sort_values(cat+ '%+/-', ascending=False, inplace=True)
  inner_df_growth.sort_values('Growth', ascending=False, inplace=True)
  return inner_df_growth


if __name__ == "__main__":

  sf.plot_data(sf.nDF_top_cat(sf.check_state_data(),10,"positiveIncrease"),"positiveIncrease")
  sf.plot_data(sf.nDF_top_cat_days(sf.check_state_data(),10,"positiveIncrease",14),"positiveIncrease")
  sf.plot_data(sf.get_states_in_list(sf.check_state_data(),["FL","CO","MI", "GA"],14), "deathIncrease")



  ##----------------------Plot Method #1 
  #ax = plt.gca()
  #df_State.plot(x='date',y='death')
  #plt.show()
  
  #----------------------Plot Method #2 
  #x = df_US['Date'] 
  #y = df_US['Confirmed']
  #plt.plot(x,y)
  #plt.show()
  
  #----------------------Plot Method #3 
  #lines = df_US.plot.line(x='Date', y='Confirmed')
  #plt.show()
  
  #---------------------Plot Method #4
  #df_US.plot()
  #plt.show()
  
  #---------------------Plot Method #5
  #top_10.plot(x='Date', y='Deaths', kind='line')
  

  #---------------------Plot death increase by date  
  #fig, ax = plt.subplots()
  #date_string= '2020-03-31'
  #date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")
  #As_of_April = total_state.iloc[0:list(total_state['date']).index(date_object)]
  #As_of_April.groupby(['date', 'state']).sum()['deathIncrease'].unstack().plot()
  #ax.grid()
  #plt.title("# Death increase by State")
  #plt.grid(True)
  #plt.show()