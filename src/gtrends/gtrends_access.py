#!/usr/bin/env python
'''
Created on Aug 27, 2020

@author: paepcke
'''

import sys
from enum import Enum

from pytrends_patch import TrendReq
import pandas as pd

class GeoResolution(Enum):
    '''
    Enumeration for Google Trends Geo Resolution names
    '''
    CITY    = 'CITY'
    METRO   = 'DMA'
    REGION  = 'REGION' 
    COUNTRY = 'COUNTRY'
    
    
class GTrendsAccessor(object):
    '''
    Demonstrates use of pytrends for access 
    Google Trends API via pytrends module.
    
    References:
    
        pytrends package: https://pypi.org/project/pytrends/#related-topics
           Particularly: the API methods near the bottom
           
        pytrends Tutorial:
            https://towardsdatascience.com/google-trends-api-for-python-a84bc25db88f
        
        Rtrends Tutorial (for sometimes more detailed parameter descriptions):
            https://cran.r-project.org/web/packages/gtrendsR/gtrendsR.pdf
            
    Not included in these examples is method pytrends.get_historical_interest(),
    which returns hourly granularity:
            self.pytrend.get_historical_interest(self, 
                                        keywords, year_start=2018, month_start=1,
                                        day_start=1, hour_start=0, year_end=2018,
                                        month_end=2, day_end=1, hour_end=0, cat=0,
                                        geo='', gprop='', sleep=0):


    '''

    #------------------------------------
    # Constructor 
    #-------------------


    def __init__(self):
        '''
        Put this module through its paces: call
        each method to illustrate its use.
        '''
        self.pytrend = TrendReq()

        kwd = 'Voting'
        # Interest by region:
        df_count_by_geo = self.interest_by_region([kwd])
        
        sys.stdout.write(f"\nFirst 10 cities count for '{kwd}':\n")
        print(df_count_by_geo.head(10))
        
        _ax = self.plot_term_freq(f'{kwd}', df_count_by_geo)
        
        # Hourly interest:
        df = self.hourly_interest(kwd)
        
        # Related terms:
        df = self.related_terms(f'{kwd}')
        sys.stdout.write(f"\nTerms related to '{kwd}':\n")
        print(df)

    #------------------------------------
    # interest_by_region 
    #-------------------
    
    def interest_by_region(self, 
                           kw_list, 
                           country="US",
                           resolution=GeoResolution.REGION):
        '''
        Request from Google Trends the (self-relative)
        number of searches for a given [should be list of] keyword(s)
        Currently, only a single-string keyword works.
        
        Legal GeoResolution values are:

           o GeoResolution.CITY
           o GeoResolution.METRO
           o GeoResolution.REGION
           o GeoResolution.Country
           
        For the US, CITY returns about 25 entries
        for the keyword 'Voting'. Finest granularity
        is METRO, with many returned entries.
        
        COUNTRY returns the requested country's high-level
        region, such as States for US, or provinces for Canada.

        Returns a Pandas DataFrame of two columns: the
        location, and the percentage of searches in the 
        given region contained the search word.
        
        @param kw_list: currently a single keyword
        @type kw_list: str
        @param country: two-letter country code 
        @type country: str
        @param resolution: administrative resolution of
            returned entries. 
        @type resolution: GeoResolution
        @return dataframe of location/search-stats
        @rtype pd.DataFrame
        '''
        
        #  ,cat, timeframe, geo, gprop)
        self.pytrend.build_payload(kw_list,
                                   geo=country)  # 'CA' for Canada, etc.
        df = self.pytrend.interest_by_region(resolution=resolution.value)
        return df
    
    #------------------------------------
    # hourly_interest 
    #-------------------
    
    def hourly_interest(self,
                        keywords, year_start=2018, month_start=1,
                                day_start=1, hour_start=0, year_end=2018,
                                month_end=2, day_end=1, hour_end=0, cat=0,
                                geo='', gprop='', sleep=0):
                        
        df = self.pytrend.get_historical_interest(self, 
                                keywords, year_start=year_start, month_start=month_start,
                                day_start=day_start, hour_start=hour_start, year_end=year_end,
                                month_end=month_end, day_end=day_end, hour_end=hour_end,
                                geo='US', 
                                gprop='', 
                                cat=0,
                                sleep=0)

        return df

    #------------------------------------
    # plot_term_freq
    #-------------------

    def plot_term_freq(self, kwd, df_count_by_geo):
        '''
        Given a keyword, and a dataframe of location 
        and search hits, plot a barchart of the content.
        
        The barchart is sorted largest to smallest search
        count, and all zero-count entries are excluded.
        
        @param kwd: search word being charted. Only needed
            for title
        @type kwd: str
        @param df_count_by_geo: two-col df with location and 
            search count
        @type df_count_by_geo: pd.DataFrame
        @return: Matplotlib figure
        @rtype Figure
        '''
        
        # For brevity:
        df = df_count_by_geo
        
        # Remove automatically created row index:
        df = df.reset_index()
        
        # New columns: 
        df.columns = ["Location", f"Keyword Frequency"]
        
        # Need index (i.e. row labels) to replicate
        # Location col, so that x-labels will appear
        df.index = df['Location']
        
        # Sort df by decreasing keyword freq:        
        df_sorted = df.sort_values(by=["Keyword Frequency"], ascending=False)
        
        # Filter out the locations with zero 
        # occurrence of keyword:
        df_non_zero = df_sorted[df_sorted['Keyword Frequency'] > 0]
        
        ax = df_non_zero.plot(
                kind='bar',
                title=f"Frequencies of keyword: '{kwd}' by location",
                rot=90,
                xlabel='Location',
                ylabel='Freq relative to peak',
                # X label default font size for resolutions such
                # as States. Smaller for Metro: 
                fontsize=(None if len(df_non_zero)<=50 else 6),
                figsize=(120, 10)
                )
        
        fig = ax.get_figure()
        fig.show()
        return fig

    #------------------------------------
    # related_terms 
    #-------------------
    
    def related_terms(self, kw):
        '''
        Given a search keyword, return 
        related words
        
        @param kw: keyword for which similars are
            to be found
        @type kw: str
        @return dataframe of similars
        @rtype pd.DataFrame
        '''
        keywords = self.pytrend.suggestions(keyword=kw)
        df = pd.DataFrame(keywords)
        df = df.drop(columns= 'mid')   # This column makes no sense
        return df

        
# ------------------------ Main ------------
if __name__ == '__main__':
    
    GTrendsAccessor()
    input("Press ENTER to exit program...")