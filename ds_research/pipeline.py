import os, sys
import pandas as pd
import numpy as np
import openpyxl
import catboost
from catboost import CatBoostClassifier, Pool, CatBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler
from slugify import slugify
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# print module versions for reproducibility
print('CatBoost version {}'.format(catboost.__version__))
print('NumPy version {}'.format(np.__version__))
print('Pandas version {}'.format(pd.__version__))

# path configurator

path_m = r'C:\\Users\\user\\Desktop\\10\\'
events_by_cat = path_m + '5_Типы событий, регистрируемых по типу объекта многоквартирный дом.xlsx'
work_types_by_support = path_m + '5_Типы событий, регистрируемых по типу объекта многоквартирный дом.xlsx'
work_types_by_cap = path_m + '4_Виды работ по капитальному ремонту многоквартирных домов.xlsx'
works_done = path_m + '3_Работы по капитальному ремонту, проведенные в многоквартирных домах.xlsx'
incidents = path_m + '2_Инциденты,_зарегистрированные_на_объектах_городского_хозяйства.xlsx'
multi_houses_characts = path_m + '1_Многоквартирные дома с технико-экономическими характеристиками.xlsx'


# function to process area
def deffer_area(input_val):
    total_area = 0
    val_total_area = int(input_val)
    if val_total_area <= 10:
        total_area = 10
        return total_area
    if val_total_area <= 50:
        total_area = 50
        return total_area
    if val_total_area <= 100:
        total_area = 100
        return total_area
    if val_total_area <= 150:
        total_area = 150
        return total_area
    if val_total_area <= 200:
        total_area = 200
        return total_area
    if val_total_area <= 250:
        total_area = 250
        return total_area
    if val_total_area <= 300:
        total_area = 300
        return total_area
    if val_total_area <= 500:
        total_area = 500
        return total_area
    if val_total_area <= 1000:
        total_area = 1000
        return total_area
    if val_total_area <= 5000:
        total_area = 5000
        return total_area
    if val_total_area <= 10000:
        total_area = 10000
        return total_area
    if val_total_area <= 15000:
        total_area = 15000
        return total_area
    if val_total_area <= 20000:
        total_area = 20000
        return total_area
    if val_total_area <= 25000:
        total_area = 25000
        return total_area
    if val_total_area <= 30000:
        total_area = 30000
        return total_area
    if val_total_area <= 35000:
        total_area = 35000
        return total_area
    if val_total_area <= 40000:
        total_area = 40000
        return total_area
    if val_total_area <= 45000:
        total_area = 45000
    return total_area


# function to preprocess some russian strings to slugs
def slug_me(str_inp):
    if type(str_inp) == str:
        str_inp = str_inp.replace('Российская Федерация, город Москва, ', '')
        if ', к.' in str_inp:
            str_inp = str_inp.split(',')[0:2]
            str_inp = ''.join(str_inp)
        if 'муниципальный округ' in str_inp:
            str_inp = str_inp.split(',')[1:3]
            str_inp = ''.join(str_inp)
        str_inp = str_inp.replace('Дом по адресу ', '')
        str_inp = str_inp.replace('Адрес ', '')
        str_inp = str_inp.replace('дом ', '')
        str_inp = str_inp.replace('район ', '')
        str_inp = str_inp.replace('улица ', '')
        str_inp = str_inp.replace('ул.', '')
        str_inp = str_inp.replace('д.', '')
        str_inp = str_inp.replace(',', '')
        rez = slugify(str_inp, allow_unicode=False, lowercase=True, save_order=True, separator="_")
        return rez
    else:
        rez = 'err'


# load xlsx datasets to mem
'''
df_incidents = pd.read_excel(incidents)
df_multi_houses_characts = pd.read_excel(multi_houses_characts)
df_work_types_by_cap = pd.read_excel(work_types_by_cap)
df_events_by_cat = pd.read_excel(events_by_cat)
df_works_done = pd.read_excel(works_done)

# re-save to csv
df_incidents.to_csv('incidents.csv')
df_multi_houses_characts.to_csv('objects.csv')
df_work_types_by_cap.to_csv('work_types_by_cap.csv')
df_events_by_cat.to_csv('events_by_cat.csv')
df_works_done.to_csv('works.csv')
'''
df_incidents = pd.read_csv('incidents.csv')
df_multi_houses_characts = pd.read_csv('objects.csv')
df_work_types_by_cap = pd.read_csv('work_types_by_cap.csv')
df_events_by_cat = pd.read_csv('events_by_cat.csv')
df_works_done = pd.read_csv('works.csv')

# create a tmp dataframes to avoid changing of originals

df_incidents_tmp = df_incidents
df_multi_houses_characts_tmp = df_multi_houses_characts
df_work_types_by_cap_tmp = df_work_types_by_cap
df_events_by_cat_tmp = df_events_by_cat
df_works_done_tmp = df_works_done

# filling NaNs with nulls

df_incidents_tmp = df_incidents_tmp.fillna(0)
df_multi_houses_characts_tmp = df_multi_houses_characts_tmp.fillna(0)
df_work_types_by_cap_tmp = df_work_types_by_cap_tmp.fillna(0)
df_events_by_cat_tmp = df_events_by_cat_tmp.fillna(0)
df_works_done_tmp = df_works_done_tmp.fillna(0)

df_inc = df_incidents_tmp
df_inc['Дата создания во внешней системе'] = pd.to_datetime(df_incidents['Дата создания во внешней системе'],
                                                            errors='coerce')
df_inc['Дата закрытия'] = pd.to_datetime(df_incidents['Дата закрытия'], errors='coerce')
df_inc['time_delta'] = (df_inc['Дата закрытия'] - df_inc['Дата создания во внешней системе']) / np.timedelta64(1, 'D')

#### 1

df_multi_houses_characts_tmp = df_multi_houses_characts_tmp.iloc[1:]  # to remove russian captions from ds

names = {
    'COL_754': 'dest',  # Назначение
    'COL_756': 'build_year',  # Год постройки
    'COL_757': 'reconst_year',  # Год реконструкции
    'COL_755': 'ownership',  # Форма собственности
    'COL_759': 'floars',  # Количество этажей
    'COL_760': 'entrances',  # Количество подъездов
    'COL_761': 'apartments',  # Количество квартир
    'COL_782': 'unom',  # unom
    'COL_758': 'project_series',  # Серия проекта
    'COL_762': 'total_area',  # Общая площадь
    'COL_763': 'living_area',  # Общая площадь жилых помещений
    'COL_764': 'nonliving_area',  # Общая площадь нежилых помещений
    'COL_765': 'construction_volume',  # Строительный объем
    'COL_766': 'depreciation_object',  # Износ объекта (по БТИ)
    'COL_767': 'energyefficiency_class',  # Класс энергоэффективности
    'COL_769': 'wall_material',  # Материал стен
    'COL_770': 'sign_building_failure',  # Признак аварийности здания
    'COL_771': 'passenger_elevators',  # Количество пассажирских лифтов
    'COL_3363': 'freight_elevators',  # Количество грузовых лифтов
    'COL_772': 'passenger_freight_elevators',  # Количество грузопассажирских лифтов
    'COL_775': 'roof_cleaning',  # Очередность уборки кровли
    'COL_2156': 'type_social_object',  # Вид социального объекта
    'COL_2463': 'type_housing_stock',  # Тип жилищного фонда
    'COL_3163': 'status_MKD',  # Статус МКД
    'COL_3243': 'management_status_MKD',  # Статус управления МКД
    'COL_3468': 'reason_changing_status_MKD',  # Причина Изменения Статуса МКД
    'COL_103506': 'category_MKD',  # Категория МКД
}

# rename column names
df_multi_houses_characts_tmp = df_multi_houses_characts_tmp.rename(columns=names)
df_multi_houses_characts_tmp['NAME'] = df_multi_houses_characts_tmp['NAME'].apply(slug_me)
df_multi_houses_characts_tmp['dest'] = df_multi_houses_characts_tmp['dest'].apply(slug_me)
df_multi_houses_characts_tmp['unom'] = df_multi_houses_characts_tmp['unom'].apply(int)

### 2
names = {
    'Наименование': 'incident_name',  # Наименование
    'Источник': 'source',  # Источник
    'Дата создания во внешней системе': 'external_create_date',  # Дата создания во внешней системе
    'Дата закрытия': 'close_date',  # Дата закрытия
    'Адрес': 'address',  # Адрес
    'Округ': 'district',  # Округ
    'Дата и время завершения события во': 'done_date',  # Дата и время завершения события во
}

# rename column names
df_incidents_tmp = df_incidents_tmp.rename(columns=names)

# prepare date format
df_incidents_tmp['external_create_date'] = pd.to_datetime(df_incidents_tmp['external_create_date'], errors='coerce')
df_incidents_tmp['external_create_date_year'] = df_incidents_tmp['external_create_date'].dt.year
df_incidents_tmp['external_create_date_month'] = df_incidents_tmp['external_create_date'].dt.month
df_incidents_tmp['external_create_date_day'] = df_incidents_tmp['external_create_date'].dt.day
df_incidents_tmp['done_date'] = pd.to_datetime(df_incidents_tmp['done_date'], errors='coerce')
df_incidents_tmp['done_date_year'] = df_incidents_tmp['done_date'].dt.year
df_incidents_tmp['done_date_month'] = df_incidents_tmp['done_date'].dt.month
df_incidents_tmp['done_date_day'] = df_incidents_tmp['done_date'].dt.day
df_incidents_tmp['close_date'] = pd.to_datetime(df_incidents_tmp['close_date'], errors='coerce')
df_incidents_tmp['close_date_year'] = df_incidents_tmp['close_date'].dt.year
df_incidents_tmp['close_date_month'] = df_incidents_tmp['close_date'].dt.month
df_incidents_tmp['close_date_day'] = df_incidents_tmp['close_date'].dt.day

# remove unnecsessary
df_incidents_tmp.drop('external_create_date', axis=1, inplace=True)
df_incidents_tmp.drop('close_date', axis=1, inplace=True)
df_incidents_tmp.drop('done_date', axis=1, inplace=True)
df_incidents_tmp.drop('district', axis=1, inplace=True)
df_incidents_tmp.drop('address', axis=1, inplace=True)

### 3
# prepare date format
df_works_done_tmp['PLAN_DATE_START'] = pd.to_datetime(df_works_done_tmp['PLAN_DATE_START'], dayfirst=True)
df_works_done_tmp['PLAN_DATE_START_year'] = df_works_done_tmp['PLAN_DATE_START'].dt.year
df_works_done_tmp['PLAN_DATE_START_month'] = df_works_done_tmp['PLAN_DATE_START'].dt.month
df_works_done_tmp['PLAN_DATE_START_day'] = df_works_done_tmp['PLAN_DATE_START'].dt.day

df_works_done_tmp['PLAN_DATE_END'] = pd.to_datetime(df_works_done_tmp['PLAN_DATE_END'], dayfirst=True)
df_works_done_tmp['PLAN_DATE_END_year'] = df_works_done_tmp['PLAN_DATE_END'].dt.year
df_works_done_tmp['PLAN_DATE_END_month'] = df_works_done_tmp['PLAN_DATE_END'].dt.month
df_works_done_tmp['PLAN_DATE_END_day'] = df_works_done_tmp['PLAN_DATE_END'].dt.day

df_works_done_tmp['FACT_DATE_START'] = pd.to_datetime(df_works_done_tmp['FACT_DATE_START'], dayfirst=True)
df_works_done_tmp['FACT_DATE_START_year'] = df_works_done_tmp['FACT_DATE_START'].dt.year
df_works_done_tmp['FACT_DATE_START_month'] = df_works_done_tmp['FACT_DATE_START'].dt.month
df_works_done_tmp['FACT_DATE_START_day'] = df_works_done_tmp['FACT_DATE_START'].dt.day

df_works_done_tmp['FACT_DATE_END'] = pd.to_datetime(df_works_done_tmp['FACT_DATE_END'], dayfirst=True)
df_works_done_tmp['FACT_DATE_END_year'] = df_works_done_tmp['FACT_DATE_END'].dt.year
df_works_done_tmp['FACT_DATE_END_month'] = df_works_done_tmp['FACT_DATE_END'].dt.month
df_works_done_tmp['FACT_DATE_END_day'] = df_works_done_tmp['FACT_DATE_END'].dt.day

df_works_done_tmp['unom'] = df_works_done_tmp['UNOM']

# remove unnecsessary
df_works_done_tmp.drop('PLAN_DATE_START', axis=1, inplace=True)
df_works_done_tmp.drop('PLAN_DATE_END', axis=1, inplace=True)
df_works_done_tmp.drop('FACT_DATE_END', axis=1, inplace=True)
df_works_done_tmp.drop('FACT_DATE_START', axis=1, inplace=True)
df_works_done_tmp.drop('Address', axis=1, inplace=True)

### 4
df_work_types_by_cap_tmp = df_work_types_by_cap_tmp.iloc[1:]  # to remove russian captions from ds

names = {
    df_work_types_by_cap_tmp.columns[0]: 'index',  # №\nп/п
    df_work_types_by_cap_tmp.columns[1]: 'code',  # Код
    df_work_types_by_cap_tmp.columns[2]: 'work_name',  # Наименование
    df_work_types_by_cap_tmp.columns[3]: 'owner_name',  # Наименование объекта общего имущества
    df_work_types_by_cap_tmp.columns[4]: 'work_type',  # Тип работ
    df_work_types_by_cap_tmp.columns[5]: 'work_group',  # Группа работ
    df_work_types_by_cap_tmp.columns[6]: 'slug_work',  # Сокращенное наименование работы
}

# rename column names
df_work_types_by_cap_tmp = df_work_types_by_cap_tmp.rename(columns=names)
df_work_types_by_cap_tmp['work_name'] = df_work_types_by_cap_tmp['work_name'].apply(slug_me)
df_work_types_by_cap_tmp['owner_name'] = df_work_types_by_cap_tmp['owner_name'].apply(slug_me)
df_work_types_by_cap_tmp['work_type'] = df_work_types_by_cap_tmp['work_type'].apply(slug_me)
df_work_types_by_cap_tmp['work_group'] = df_work_types_by_cap_tmp['work_group'].apply(slug_me)
df_work_types_by_cap_tmp['slug_work'] = df_work_types_by_cap_tmp['slug_work'].apply(slug_me)

#### merge
df_merged = df_works_done_tmp.merge(df_incidents_tmp, on='unom', how='left')
df_merged = df_merged.merge(df_multi_houses_characts_tmp, on='unom', how='left')

### clean unnecsessory
df_merged.drop('unom', axis=1, inplace=True)
# df_merged.drop('Address', axis=1, inplace=True)
# df_merged.drop('address', axis=1, inplace=True)
df_merged.drop('LOGIN', axis=1, inplace=True)
df_merged.drop('District', axis=1, inplace=True)
df_merged.drop('AdmArea', axis=1, inplace=True)
df_merged.drop('dest', axis=1, inplace=True)
df_merged.drop('category_MKD', axis=1, inplace=True)
df_merged.drop('reason_changing_status_MKD', axis=1, inplace=True)
df_merged.drop('status_MKD', axis=1, inplace=True)
df_merged.drop('type_housing_stock', axis=1, inplace=True)
df_merged.drop('type_social_object', axis=1, inplace=True)
df_merged.drop('sign_building_failure', axis=1, inplace=True)
df_merged.drop('reconst_year', axis=1, inplace=True)
df_merged.drop('ownership', axis=1, inplace=True)
df_merged.drop('global_id', axis=1, inplace=True)
df_merged.drop('ID', axis=1, inplace=True)
df_merged.drop('NAME', axis=1, inplace=True)
df_merged.drop('depreciation_object', axis=1, inplace=True)
df_merged.drop('construction_volume', axis=1, inplace=True)

# process values optimization
df_merged['nonliving_area'] = df_merged['nonliving_area'].apply(deffer_area)
df_merged['living_area'] = df_merged['living_area'].apply(deffer_area)
df_merged['total_area'] = df_merged['total_area'].apply(deffer_area)
df_merged['apartments'] = df_merged['apartments'].apply(deffer_area)

### process cat features
object_features = df_merged.select_dtypes(include='object').columns.tolist()
# print(object_features)
encoded_values_dict = {}

le = LabelEncoder()
for obj in object_features:
    df_merged[obj] = le.fit_transform(df_merged[obj].astype(str))
    encoded_values_dict[obj] = dict(zip(le.classes_, le.transform(le.classes_)))

for feature, mapping in encoded_values_dict.items():
    print(f"Колонка: {feature}")
    for original_value, transformed_value in mapping.items():
        print(f"Оригинальное значение: {original_value}, Трансформированное значение: {transformed_value}")
    print()


df_merged.to_csv('dataset.csv')