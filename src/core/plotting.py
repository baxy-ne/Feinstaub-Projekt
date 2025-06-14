import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
from src.core.database import get_date_range_data
import matplotlib.dates as mdates

def plot_sensor_data(sensor_id, start_date=None, end_date=None):

    if start_date is None:
        start_date = '2025-05-01' 
    if end_date is None:
        end_date = '2025-05-31'    
        
    data = get_date_range_data(sensor_id, start_date, end_date)
    if not data:
        return None
        
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby('date').mean(numeric_only=True)
    
    full_range = pd.date_range(start=start_date, end=end_date, freq='D')
    df = df.reindex(full_range)
    df.index.name = 'date'
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
    fig.suptitle(f'Sensor {sensor_id} Air Quality Data', fontsize=14)
    
    # Plot P1 (PM10) data
    ax1.plot(df.index, df['max_p1'], 'r-', label='Max PM10', linewidth=1.5)
    ax1.plot(df.index, df['min_p1'], 'b-', label='Min PM10', linewidth=1.5)
    ax1.plot(df.index, df['avg_p1'], 'g-', label='Avg PM10', linewidth=1.5)
    ax1.set_ylabel('PM10 (µg/m³)', fontsize=10)
    ax1.set_title('PM10 Measurements', fontsize=12, pad=15)
    ax1.grid(True)
    ax1.legend(fontsize=9)
    
    # Plot P2 (PM2.5) data
    ax2.plot(df.index, df['max_p2'], 'r-', label='Max PM2.5', linewidth=1.5)
    ax2.plot(df.index, df['min_p2'], 'b-', label='Min PM2.5', linewidth=1.5)
    ax2.plot(df.index, df['avg_p2'], 'g-', label='Avg PM2.5', linewidth=1.5)
    ax2.set_xlabel('Date', fontsize=10, labelpad=10)
    ax2.set_ylabel('PM2.5 (µg/m³)', fontsize=10)
    ax2.set_title('PM2.5 Measurements', fontsize=12, pad=15)
    ax2.grid(True)
    ax2.legend(fontsize=9)
    
    for ax in [ax1, ax2]:
        ax.set_xlim([full_range[0], full_range[-1]])
        date_range = (full_range[-1] - full_range[0]).days
        if date_range <= 7:
            interval = 1
            date_format = '%Y-%m-%d'
        elif date_range <= 31:
            interval = 7
            date_format = '%Y-%m-%d'
        elif date_range <= 90:
            interval = 14
            date_format = '%Y-%m-%d'
        else:
            interval = 30
            date_format = '%Y-%m'
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=9)
        ax.tick_params(axis='y', labelsize=9)
    
    fig.subplots_adjust(left=0.13, right=0.95, top=0.90, bottom=0.12, hspace=0.35)
    
    return fig 