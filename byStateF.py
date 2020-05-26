import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os


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
  df_State = df[['date','state','positive','death','hospitalized', 'deathIncrease', 'hospitalizedIncrease', 'positiveIncrease']]
  df_State['date'] = pd.to_datetime(df_State['date'], format='%Y%m%d')
  df_State.fillna(0,inplace=True)
  return df_State

def plot_data(df,cat='deathIncrease'):
  df.groupby(['date', 'state']).sum()[cat].unstack().plot()
  plt.title("# Death increase by State")
  plt.grid(True)
  plt.show()

    
def nDF_top_cat(df,top=5,d='death'):
  #python3 -c 'import byStateF; byStateF.plot_data(byStateF.nDF_top_cat(byStateF.check_state_data(),5,"deathIncrease"), "positive")'
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

def get_states_in_list(df,l=['CA'],days=7):
  #python3 -c 'import byStateF; byStateF.plot_data(byStateF.get_states_in_list(byStateF.check_state_data(),["FL","CO","MI", "GA"],14), "deathIncrease")'
  past_seven_days = df['date'].unique()[0:days]
  df = df[df.date.isin(past_seven_days) & df.state.isin(l)]
  return df

if __name__ == "__main__":

  plot_data(check_state_data(),"CA", "MI")

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