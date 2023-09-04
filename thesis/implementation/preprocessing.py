import pandas as pd
import numpy as np
import pickle
import datetime

from sklearn.preprocessing import StandardScaler

def preprocess(data, fit_scaler=False):
    
    drop_cols = [
        'country',
        'assigned_room_type',
        'reservation_status',
        'reservation_status_date',
        'is_canceled',
        'predicted_cancellations',
        'id'
    ]
    
    cat_cols = [
        'meal',
        'market_segment',
        'distribution_channel',
        'reserved_room_type',
        'deposit_type',
        'customer_type'
    ]

    binary_cols = [
        'hotel',
        'is_repeated_guest'
    ]

    num_cols = [
        'lead_time',
        'arrival_date_year', 
        'arrival_date_month',
        'arrival_date_day_of_month',
        'arrival_date_week_number',
        'stays_in_weekend_nights', 
        'stays_in_week_nights', 
        'adults', 
        'children',
        'babies',
        'previous_cancellations',
        'previous_bookings_not_canceled',
        'booking_changes',
        'agent', 
        'company',
        'days_in_waiting_list',
        'adr',
        'required_car_parking_spaces', 
        'total_of_special_requests'
    ]
    # копируем оригинальны датасет
    copy = data.copy()
    
    # удаляем ненужные колонки
    copy = copy.drop(columns=drop_cols)
    
    # заполняем пропуски нулями
    copy = copy.fillna(0)
    
    # бинарные переменные заменяем на 0 и 1
    for col in binary_cols:
        values = sorted(data[col].unique())

        mapping = dict(zip(values, range(len(values))))

        copy[col] = copy[col].map(mapping)
    
    # месяцы заменяем на их номера
    copy['arrival_date_month'] = data['arrival_date_month'].apply(lambda x: \
                                                                  datetime.datetime.strptime(x, '%B').month)
    
    # кодируем категориальные переменные с помощью OHE
    copy = copy.drop(columns=cat_cols)
    copy = pd.concat((copy, pd.get_dummies(data[cat_cols])), axis=1)
    
    if fit_scaler:
        scaler = StandardScaler()
        # масштабируем числоывые переменные
        copy[num_cols] = scaler.fit_transform(copy[num_cols])
        # обновляет скейлер
        with open('scaler.pkl','wb') as f:
            pickle.dump(scaler, f)
        
        return copy
    
    # загружаем скейлер   
    with open('scaler.pkl','rb') as f:
        scaler = pickle.load(f)
    
    # масштабируем числовые переменные
    copy[num_cols] = scaler.transform(copy[num_cols])
    
    return copy


def preprocess_demand(data, fit_scaler=False):
    drop_cols = [
        'occupancy_rate',
        'or_prediction'
    ]
    
    copy = data.copy()
    if fit scaler:
        copy.drop(columns=drop_cols, inplace=True)
    
    copy = copy.fillna(copy.median())
    
    if fit_scaler:
        scaler = StandardScaler()
        # масштабируем числоывые переменные
        copy = scaler.fit_transform(copy)
        # обновляет скейлер
        with open('demand_scaler.pkl','wb') as f:
            pickle.dump(scaler, f)
        
        return copy
    
    # загружаем скейлер   
    with open('demand_scaler.pkl','rb') as f:
        scaler = pickle.load(f)
    
    return scaler.transform(copy)
    