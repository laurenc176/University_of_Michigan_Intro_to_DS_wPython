
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[2]:


def answer_one():
    import pandas as pd
    import numpy as np

    energy= pd.DataFrame(pd.read_excel('Energy Indicators.xls', usecols=[2,3,4,5], skiprows=17,skip_footer=38))
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy[['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']]=energy[['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']].replace('...',np.NaN)
    energy['Energy Supply']= energy['Energy Supply']*1000000
    

    def clean_txt(text):
        lst= text.split()
    
        if any([char.isdigit()for char in text]):
            va=[char for char in text if char.isalpha() or char ==" "]
            va=''.join(va)
            return va
        else:
            return text
    energy['Country']= energy['Country'].apply(clean_txt)
    energy['Country'] = energy['Country'].str.replace(" \(.*\)","")
    energy['Country']= energy['Country'].replace({"Republic of Korea": "South Korea",
    "United States of America": "United States","United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China Hong Kong Special Administrative Region": "Hong Kong","Bolivia Plurinational State of": "Bolivia","Venezuela (Bolivarian Republic of)": "Venezuela",
                                         "China Macao Special Administrative Region" : "Macao"})


    GDP = pd.DataFrame(pd.read_csv('world_bank.csv',skiprows=4))
    GDP['Country Name']= GDP['Country Name'].replace({"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"})

    columns = ['Country Name', '2006','2007','2008','2009','2010','2011','2012','2013','2014', '2015']
    GDP=GDP[columns]
    
    ScimEn = pd.DataFrame(pd.read_excel('scimagojr-3.xlsx'))
    ScimEn1 = ScimEn[:15]

    df = pd.merge(ScimEn1, energy, how='inner', left_on='Country', right_on='Country')

    df2= pd.merge(df, GDP, how='inner', left_on='Country', right_on='Country Name')
    final=df2.set_index('Country')

    columns = ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    answer=final[columns]
    return answer

answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[3]:


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[4]:


def answer_two():
    import pandas as pd
    import numpy as np

    energy= pd.DataFrame(pd.read_excel('Energy Indicators.xls', usecols=[2,3,4,5], skiprows=17,skip_footer=38))
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy[['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']]=energy[['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']].replace('...',np.NaN)
    energy['Energy Supply']= energy['Energy Supply']*1000000
    

    def clean_txt(text):
        lst= text.split()
    
        if any([char.isdigit()for char in text]):
            va=[char for char in text if char.isalpha() or char ==" "]
            va=''.join(va)
            return va
        else:
            return text
    energy['Country']= energy['Country'].apply(clean_txt)
    energy['Country'] = energy['Country'].str.replace(" \(.*\)","")
    energy['Country']= energy['Country'].replace({"Republic of Korea": "South Korea",
    "United States of America": "United States","United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China Hong Kong Special Administrative Region": "Hong Kong","Bolivia Plurinational State of": "Bolivia","Venezuela (Bolivarian Republic of)": "Venezuela",
                                         "China Macao Special Administrative Region" : "Macao"})


    GDP = pd.DataFrame(pd.read_csv('world_bank.csv',skiprows=4))
    GDP['Country Name']= GDP['Country Name'].replace({"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"})

    columns = ['Country Name', '2006','2007','2008','2009','2010','2011','2012','2013','2014', '2015']
    GDP=GDP[columns]
    GDP.columns=['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014', '2015']

    ScimEn = pd.DataFrame(pd.read_excel('scimagojr-3.xlsx'))
    ScimEn1 = ScimEn[:15]

    df = pd.merge(ScimEn, energy, how='inner', left_on='Country', right_on='Country')

    df= pd.merge(df, GDP, how='inner', left_on='Country', right_on='Country')
    final=df.set_index('Country')

    columns = ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    answer=final[columns]
    
    df2 = pd.merge(ScimEn, energy, how='outer', left_on='Country', right_on='Country')

    finaldf2= pd.merge(df2, GDP, how='outer', left_on='Country', right_on='Country')
    ans=finaldf2[columns]
    print(len(ans))
    print(len(answer))
    return len(finaldf2) - len(answer) + 1


answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[5]:


def answer_three():
    import pandas as pd
    import numpy as np
    
    Top15 = answer_one()
    columns=['2006','2007','2008','2009','2010','2011','2012','2013','2014', '2015']
    Top15['mean']= Top15[columns].mean(axis=1)
    avgGDP=Top15.sort_values(by='mean', ascending=False)['mean']    
        
    return avgGDP
answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[6]:


def answer_four():
    import pandas as pd
    import numpy as np
    
    Top15 = answer_one()
    columns=['2006','2007','2008','2009','2010','2011','2012','2013','2014', '2015']
    Top15['mean']= Top15[columns].mean(axis=1)
    avgGDP=Top15.sort_values(by='mean', ascending=False)['mean']    
    num_six=avgGDP.index[5]
    num_six_info= Top15.loc[num_six]
    
    
    return num_six_info.loc['2015'] -num_six_info.loc['2006']
answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[7]:


def answer_five():
    import pandas as pd
    import numpy as np
    
    Top15 = answer_one()
    energy_mean=Top15['Energy Supply per Capita']
    return energy_mean.mean()
answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[8]:


def answer_six():
    import pandas as pd
    import numpy as np
    
    Top15 = answer_one()
    max_renew=Top15['% Renewable']
    val=max_renew.max()
    
    return (Top15[Top15['% Renewable']==val].index[0], val)
answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[9]:


def answer_seven():
    import pandas as pd
    import numpy as np
    Top15 = answer_one()
    
    Top15['Ratios']= Top15['Self-citations'] / Top15['Citations']
    maxval= Top15['Ratios'].max()
    
    
    return (Top15[Top15['Ratios']==maxval].index[0], maxval)
answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[10]:


def answer_eight():
    import pandas as pd
    import numpy as np
    Top15 = answer_one()
    Top15['PopEstimate']= Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    estsorted=Top15.sort_values(by='PopEstimate', ascending=False)['PopEstimate']
    ans=estsorted.index[2]
    return ans
answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[11]:


def answer_nine():
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    
    
    return Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])
answer_nine()


# In[12]:


def plot9():
    
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])
    


# In[13]:


#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[15]:


def answer_ten():
    Top15 = answer_one()
    m= Top15['% Renewable'].median()
    Top15['HighRenew'] = [1 if num >= m else 0 for num in Top15['% Renewable']]
    
    return Top15['HighRenew']
answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[32]:


def answer_eleven():
    import pandas as pd
    import numpy as np
    
    Top15 = answer_one()
    ContinentDict= {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    #index=['Asia', 'Australia','Europe','North America','South America']
    #columns=['size','sum','mean','std']
    Top15=Top15.reset_index()
    Top15['Continent']= [ContinentDict[country] for country in Top15['Country']]
    Top15= Top15.set_index('Continent').groupby(level=0)['PopEst'].agg({'size':np.size
                                                                       ,'sum':np.sum,'mean':np.mean,
                                                                       'std':np.std})
    
    
    return Top15
answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[38]:


def answer_twelve():
    import pandas as pd
    import numpy as np
    
    Top15 = answer_one()
    ContinentDict= {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15=Top15.reset_index()
    Top15['Continent']= [ContinentDict[country] for country in Top15['Country']]
    Top15['bins'] = pd.cut(Top15['% Renewable'], 5)
    
    return Top15.groupby(['Continent', 'bins']).size()
answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[40]:


def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    
    lst=Top15['PopEst'].tolist()
    Top15['PopEst']= (Top15['PopEst'].apply(lambda x: "{:,}".format(x),lst))
        
    
    return Top15['PopEst']
answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[42]:


def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[43]:


#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!


# In[ ]:




