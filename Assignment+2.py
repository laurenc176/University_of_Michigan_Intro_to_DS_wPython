
# coding: utf-8

# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[1]:


import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[2]:


# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[3]:




def answer_one():
    df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

    for col in df.columns:
        if col[:2]=='01':
            df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
        if col[:2]=='02':
            df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
        if col[:2]=='03':
            df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
        if col[:1]=='№':
            df.rename(columns={col:'#'+col[1:]}, inplace=True)

    names_ids = df.index.str.split('\s\(') # split the index by '('

    df.index = names_ids.str[0] # the [0] element is the country name (new index) 
    df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

    df = df.drop('Totals')
    df.head()
    #copy_df = df.copy()
    #most_g = copy_df['Gold'].max()
    #return str(copy_df.[copy_df['Gold'] == most_g].index[0])

    most_g = max(df['Gold'])
    return df[df['Gold'] == most_g].index[0]




# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[4]:


answer_one()


# In[ ]:





# In[5]:


import pandas as pd
def answer_two():
    
    df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

    for col in df.columns:
        if col[:2]=='01':
            df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
        if col[:2]=='02':
            df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
        if col[:2]=='03':
            df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
        if col[:1]=='№':
            df.rename(columns={col:'#'+col[1:]}, inplace=True)

    names_ids = df.index.str.split('\s\(') # split the index by '('

    df.index = names_ids.str[0] # the [0] element is the country name (new index) 
    df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

    df = df.drop('Totals')
    df.head()

    countries = df.loc[:, ["Gold", "Gold.1"]]
    gold_diff = abs(df['Gold'] - df['Gold.1'])
    #print(countries)
    ans = gold_diff.idxmax()
    
    return str(ans)
answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[6]:


import pandas as pd


def answer_three():
    df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

    for col in df.columns:
        if col[:2]=='01':
            df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
        if col[:2]=='02':
            df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
        if col[:2]=='03':
            df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
        if col[:1]=='№':
            df.rename(columns={col:'#'+col[1:]}, inplace=True)

    names_ids = df.index.str.split('\s\(') # split the index by '('

    df.index = names_ids.str[0] # the [0] element is the country name (new index) 
    df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

    df = df.drop('Totals')
    df.head()
    countries = df.loc[:, ["Gold", "Gold.1"]]
    has_gold_summer = df.where(df['Gold'] >0)
    
    has_gold_winter = df.where(df['Gold.1'] > 0)
   
    has_gold = has_gold_winter + has_gold_summer
    has_gold = has_gold.dropna()
    #print(has_gold_summer.head())
    #print(has_gold_winter.head())
    gold_diff = (has_gold['Gold'] - has_gold['Gold.1']) / (has_gold['Gold'] + has_gold['Gold.1'])
    return str(gold_diff.idxmax())

answer_three()


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.
# 
# *This function should return a Series named `Points` of length 146*

# In[7]:


import pandas as pd


def answer_four():
    df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

    for col in df.columns:
        if col[:2]=='01':
            df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
        if col[:2]=='02':
            df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
        if col[:2]=='03':
            df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
        if col[:1]=='№':
            df.rename(columns={col:'#'+col[1:]}, inplace=True)

    names_ids = df.index.str.split('\s\(') # split the index by '('

    df.index = names_ids.str[0] # the [0] element is the country name (new index) 
    df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

    df = df.drop('Totals')
    df.head() 
    gold_points = df['Gold.2'] * 3
    silver_points = df['Silver.2'] * 2
    Points = gold_points + silver_points + df['Bronze.2']
    
    return Points

answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[8]:


import pandas as pd
census_df = pd.read_csv('census.csv')
census_df.head()



# In[9]:




df = census_df[census_df['SUMLEV'] == 50]

def answer_five():
    count = df['STNAME'].value_counts()
    return count.idxmax()


answer_five()


# ### Question 6
# **Only looking at the three most populous counties for each state**, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[10]:


def answer_six():
    state_df = census_df[census_df['SUMLEV'] == 50]
    #state_df = pd.DataFrame()
    #state_df['State'] = df['STNAME']
    #state_df['CENSUS2010POP'] = df['CENSUS2010POP']
    #state_df['Top3PoP'] = 0
    #state_df.set_index('State',inplace=True)
    top_counties_df = state_df.sort_values(by='CENSUS2010POP', ascending=False).groupby('STNAME').head(3)
    top3= top_counties_df.groupby('STNAME').sum().sort_values(by='CENSUS2010POP', ascending= False).head(3).index.tolist()
            
        
            
        #if type(countiespop) == pd.Series:
         #   stsum = sum(countiespop.count_values().head(3))
        #else:
         #   stsum = countiespop
        #state_df['Top3PoP'].loc[st] = stsum         
                

    return top3
answer_six()


# def answer_six():
#     df = census_df[census_df['SUMLEV'] == 50]
#     keepers = ['STNAME','CENSUS2010POP']
#     df= df[keepers]
#     df = df.set_index('STNAME', inplace=True)
#     df["Top3POP"] = 0
#     #for st in df.index:
#     #    countiespop = 0
#         
#     state_df = pd.DataFrame()    
#     
#     #for state in df.index:
#     #    countiespop = df.sort_values( ascending=False)    
#     #state_df['State']= lst
#         
#             #states.append(state)
#     #state_df = pd.DataFrame()
#     #state_df['State'] = states
#     #state_df['CENSUS2010POP'] = census_df['CENSUS2010POP']
#     return countiespop
# answer_six()
# 
# state_df = pd.DataFrame()
# state_df['State'] = $unique_state_names_list$
# 
# #intialise all state populations to 0
# state_df['Top3PoP'] = 0
# state_df.set_index('State',inplace=True)
# for st in state_df.index:
#     countiespop = $find_pop_of_st_cnties_sorted_descending(st)$
#     #check if countiespop has more than one number
#     #this check is needed because for states with one
#     #county only, countiespop is a number
#     if type(countiespop) == pd.Series:
#       stsum = sum(countiespop$.getfirst3$)
#     else:
#       stsum = countiespop
#     state_df['Top3PoP'].loc[st] = stsum
# 
# state_df$.sortDescAccordingToTop3PoP$
# state_df$.getfirst3States$
# 

# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[15]:


def answer_seven():
    c_df = census_df[census_df['SUMLEV']==50]
    c_df = c_df.set_index('CTYNAME')
    to_keep = ['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']
    val_max = c_df[to_keep].max(axis=1)
    val_min = c_df[to_keep].min(axis=1)
    difference = val_max - val_min
    c_df['difference'] = difference
    
    return c_df['difference'].idxmax()
answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[18]:


def answer_eight():
    c_df = census_df[census_df['SUMLEV']==50]
    
    return c_df[((c_df['REGION'] ==1) | (c_df['REGION'] ==2)) & (c_df['CTYNAME'] == 'Washington County') & (c_df['POPESTIMATE2015'] > c_df['POPESTIMATE2014'])][['STNAME','CTYNAME']]

answer_eight()


# In[ ]:




