import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os


'''This Programs will download current state data on Covid19 and graph it for you'''
#------------Stat_Data_From_Github------------- 
def get_data_State():
  site = 'https://covidtracking.com/api/v1/states/daily.csv'
  df =  pd.DataFrame(pd.read_csv(site, error_bad_lines=False))
  df.to_csv(r'/home/bot/Documents/daily.csv')

#code to check the timestamp of the csv file if more than one day old then execute the github function above 
def check_state_data():
  get_file_last_edit = datetime.date.fromtimestamp(os.stat('/home/bot/Documents/daily.csv').st_mtime)
  get_today_date = datetime.date.today()
  if get_today_date > get_file_last_edit:
    get_data_State()
    print('Refreshing Data...')
  else:
    print('Data Up to Date.')
  df =  pd.DataFrame(pd.read_csv('/home/bot/Documents/daily.csv'))
  df_State = df[['date','state','death','hospitalized', 'deathIncrease']]
  df_State['date'] = pd.to_datetime(df_State['date'], format='%Y%m%d')
  df_State.fillna(0,inplace=True)
  return df_State

def plot_data(df,*args):
  '''Here we are plotting the data we got and cleaned
     The *args here let us take in optional arguments so we can leave thing in or out
     For top_10 states, put the top_10 function in for the df, no other argumens
     For specific cities, put in your df and the city you want as strings, plot_data(df, 'CA', 'MI', 'NJ')
     To execute from cml python3 -c 'import byStateF; byStateF.plot_data(byStateF.check_state_data(),'CA', 'NY', 'NJ', 'GA'))
     Doesnt work from CLI prob bceuase of singlen ending double quote'''
  s=[]
  if len(args) > 0:
    for i in args:
      s.append(i)
      df = df[df.state.isin(s)]
  df.groupby(['date', 'state']).sum()['deathIncrease'].unstack().plot()
  plt.title("# Death increase by State")
  plt.grid(True)
  plt.show()

    
def plot_top_S(df,s,d='death'):
  #python3 -c 'import byStateF; byStateF.plot_data(byStateF.plot_top_S(byStateF.check_state_data(),5,"death"))'
  df.sort_values('date', ascending=False)                              #sort df in decending order
  latest_record = df[df['date'] == df['date'].iloc[0]]                 #gets all deaths as of most recent date
  rec_sorted = latest_record.sort_values(d, ascending=False)           #sort all death, cummulative death
  top_10_State = list(rec_sorted['state'][0:s])                        #get top S states with most death in list
  total_state = df[df.state.isin(top_10_State)]                        #filter df on stop S state
  return total_state

def data_top_S_week(df,top=5,cat='death', days=7):
  #python3 -c 'import byStateF; byStateF.plot_data(byStateF.data_top_S_week(byStateF.check_state_data(),5,"death",7))'
  df.sort_values('date', ascending=False)                              #sort df in decending order
  latest_record = df[df['date'] == df['date'].iloc[0]]                 #gets all deaths as of most recent date
  rec_sorted = latest_record.sort_values(cat, ascending=False)           #sort all death, cummulative death
  top_10_State = list(rec_sorted['state'][0:top])                        #get top S states with most death in list
  past_seven_days = df['date'].unique()[0:days] 
  total_state = df[df.state.isin(top_10_State) & df.date.isin(past_seven_days)]             #filter df on stop S state
  return total_state


def show_top_10(df,s,d='death'):
  #python3 -c 'import byStateF; print(byStateF.show_top_10(byStateF.check_state_data(),5, "deathIncrease"))'
  df.sort_values('date', ascending=False)
  latest_record = df[df['date'] == df['date'].iloc[0]]                 #gets all deaths as of the latest time period, one date
  rec_sorted = latest_record.sort_values(d, ascending=False)     #sort all death on that one day this is a cummulative death
  top_10_State = list(rec_sorted['state'][0:s])                        #get top states with most death
  total_state = rec_sorted[rec_sorted.state.isin(top_10_State)]
  return total_state

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

