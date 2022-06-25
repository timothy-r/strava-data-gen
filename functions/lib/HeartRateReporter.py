import pandas as pd
from pandas import json_normalize

# Matplotlib is a data visualization library. 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

class HeartRateReporter:
    
    def __init__(self) -> None:
        pass
    
    def generate(self, activities:dict) -> str:
        """
            generate an image on local fs
            return file path
        """
        
        # prepare the data
        runs_with_hr = self._prepare_data(activities=activities)
        file_path_name = '/tmp/average-heart-rate-over-time.png'
        self._plot_average_hr(runs=runs_with_hr, file_path_name=file_path_name)
        
        return file_path_name
    
    def _prepare_data(self, activities):
        activities = json_normalize(activities.values())
        activities['start_date_local'] = pd.to_datetime(activities['start_date_local'])
        activities['start_time'] = activities['start_date_local'].dt.time
        activities['start_date_local'] = activities['start_date_local'].dt.date

        # extract run data from all activities & only activities that have hr data
        runs = activities.loc[activities['type'] == 'Run']
        runs_with_hr = runs.loc[runs['has_heartrate'] == True]
        
        return runs_with_hr
    
    def _plot_average_hr(self, runs, file_path_name):
        
        with plt.style.context('Solarize_Light2'):
    
            fig = plt.figure() #create overall container
            ax1 = fig.add_subplot(111) #add a 1 by 1 plot to the figure
            ax1.set_title('Heart rate over time')
                    
            # x is date
            x = np.asarray(runs.start_date_local)  #convert data to numpy array
            
            # y is hr
            y = np.asarray(runs.average_heartrate)
            
            # y_max is max hr
            y_max = np.asarray(runs.max_heartrate)
            
            # set target hr at 130 bpm
            target = np.full(len(x), 130, dtype=int)
            
            # plot data points in scatter plot on ax1
            ax1.scatter(x, y, c='#bf88f7', label='Average')
            ax1.scatter(x, y_max, c='#fab498', label='Max')
            
            x2 = mdates.date2num(x)
            
            # add trend line for average hr
            self._plot_line(plt, x2, y, '#6002bf', 'dashed')
            # add a max hr trend line
            self._plot_line(plt, x2, y_max, '#d4440b', 'dashed')
            # add target line
            self._plot_line(plt, x2, target, '#02bf21', 'dashed', 'Target')
            
            plt.ylabel('Heart rate')
            plt.legend()
            
            #format the figure and display
            fig.autofmt_xdate(rotation=45)    
            fig.tight_layout()
            
            fig.show()
            fig.savefig(file_path_name)
            plt.close(fig)

    def _plot_line(plt, x, y, colour, style, label = None):
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        plt.plot(x, p(x), colour, linestyle=style, label=label)
      
    