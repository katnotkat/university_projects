import pickle
from datetime import datetime, timedelta
import pandas as pd

from db_connection import Connection
from preprocessing import preprocess, preprocess_demand


def train_cancellations():
    where = "WHERE reservation_status IN ('Check-Out', 'Canceled', 'No-Show')"
    conn = Connection()
    data = pd.DataFrame(conn.collect_data_from_database(where))
    y = data['is_canceled']
    
    data = preprocess(data, fit_scaler=True)
    
    model = pickle.load(open('cancellation_prediction.sav', 'rb'))
    model.fit(data, y)
    
    pickle.dump(rfc, open('cancellation_prediction.sav', 'wb'))
    
    conn.close()
    

def train_demand():
    conn = Connection()
    data = pd.DataFrame(conn.collect_demand_train_data())
    y = data['occupancy_rate']
    
    data = preprocess_demand(data, fit_scaler=True)
    
    model = pickle.load(open('demand_prediction.sav', 'rb'))
    model.fit(data, y)
    
    pickle.dump(rfc, open('demand_prediction.sav', 'wb'))
    
    conn.close()


def predict():
    CITY = 1
    RESORT = 0
    
    conn = Connection()
    where = "WHERE reservation_status IN ('Check-In', 'Booked')"

    data = pd.DataFrame(conn.collect_data_from_database(where))
    
    model = pickle.load(open('cancellation_prediction.sav', 'rb'))
    
    predictions = model.predict(preprocess(data[data['reservation_status'] == 'Booked']))
    
    data.loc[data['reservation_status'] == 'Booked', 'is_canceled'] = predictions
    data.loc[data['reservation_status'] == 'Check-In', 'is_canceled'] = 0
    data['people_total'] = data['adults'] + data['children'] + data['babies']
    data['arrival_date'] = pd.to_datetime(
        data['arrival_date_year'].astype(str)  + \
        data['arrival_date_month'] + \
        data['arrival_date_day_of_month'].astype(str), 
        format='%Y%B%d'
    )
    data['checkout_date'] = data['arrival_date'] + timedelta(days=7)
    
    demand_data = pd.DataFrame(columns=['or_1yrbefore', 'or_2wbefore', 'year', 'month', 'day',
                                        'day_of_week', 'week_of_year', 'hotel'])
    demand_data.loc[RESORT, 'hotel'] = RESORT
    demand_data.loc[CITY, 'hotel'] = CITY
    
    or_1yrbefore = datetime.today() + timdelta(days=7) - timdelta(days=365)
    select = 'occupancy_rate'
    where = f"WHERE year={or_1yrbefore.year} AND month={or_1yrbefore.month} AND day={or_1yrbefore.day}"
    demand_data.loc[CITY, 'or_1yrbefore'] = conn.collect_demand_train_data(select, where + " AND hotel='City Hotel'")[0][0]
    demand_data.loc[RESORT, 'or_1yrbefore'] = conn.collect_demand_train_data(select, where + " AND hotel='Resort Hotel'")[0][0]
    
    or_2wbefore = datetime.today() - timdelta(days=7)
    where = f"WHERE year={or_2wbefore.year} AND month={or_2wbefore.month} AND day={or_2wbefore.day}"
    demand_data.loc[CITY, 'or_2wbefore'] = conn.collect_demand_train_data(select, where + " AND hotel='City Hotel'")[0][0]
    demand_data.loc[RESORT, 'or_2wbefore'] = conn.collect_demand_train_data(select, where + " AND hotel='Resort Hotel'")[0][0]
    
    the_day = datetime.today() + timdelta(days=7)
    demand_data['year'] = the_day.year
    demand_data['month'] = the_day.month
    demand_data['day'] = the_day.day
    demand_data['day_of_week'] = the_day.weekday()
    demand_data['week_of_year'] = the_day.isocalendar()[1]
    
    filter_city = (data['hotel'] == 'City Hotel')
    filter_resort = (data['hotel'] == 'Resort Hotel')
    
    for delta in range(0, 8):
        today = datetime.today() + timdelta(days=delta)
        filter_date = (data['arrival_date'] == today)
        filter_ch = (data['checkout_date'] == today)
        
        day = 8 - delta
        
        
        condition_c = filter_city & filter_date
        demand_data.loc[CITY, f'bookings_{day}dbefore'] = data[condition_c]['people_total'].sum()
        
        condition_r = filter_resort & filter_date
        demand_data.loc[RESORT, f'bookings_{day}dbefore'] = data[condition_r]['people_total'].sum()
        
        condition_c = condition_c & (data['is_canceled'] == 0)
        condition_r = condition_r & (data['is_canceled'] == 0)
        
        demand_data.loc[CITY, f'book_approved_{day}dbefore'] = data[condition_c]['people_total'].sum()
        demand_data.loc[RESORT, f'book_approved_{day}dbefore'] = data[condition_r]['people_total'].sum()
        
        condition_c = filter_city & filter_ch & (data['is_canceled'] == 0)
        condition_r = filter_resort & filter_ch & (data['is_canceled'] == 0)
        
        demand_data.loc[CITY, f'checkouts_{day}dbefore'] = data[condition_c]['people_total'].sum()
        demand_data.loc[RESORT, f'checkouts_{day}dbefore'] = data[condition_r]['people_total'].sum()
        
    demand_data_p = preprocess_demand(demand_data)
    
    model = pickle.load(open('demand_prediction.sav', 'rb'))
    demand_preds = model.predict(demand_data_p)
    
    id_numbers = data['id'][data['reservation_status'] == 'Booked'].values
    conn.upload_predictions(id_numbers, predictions)
    
    demand_data['or_prediction'] = demand_preds
    conn.upload(demand_data)
    
    conn.close()

