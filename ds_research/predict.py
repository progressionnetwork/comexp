import os, sys
import pickle

import joblib
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
from sklearn import metrics

# print module versions for reproducibility
print('CatBoost version {}'.format(catboost.__version__))
print('NumPy version {}'.format(np.__version__))
print('Pandas version {}'.format(pd.__version__))

encoded_values_dict = {'WORK_NAME': {'remont_fasadov': 0,
                                     'remont_kryshi': 1,
                                     'remont_musoroprovoda': 2,
                                     'remont_podezdov_napravlennyi_na_vosstanovlenie_ikh_nadlezhashchego_sostoianiia_i_provodimyi_pri_vypolnenii_inykh_rabot_po_kapitalnomu_remontu_obshchego_imushchestva_v_mnogokvartirnom_dome': 3,
                                     'remont_podvalnykh_pomeshchenii_otnosiashchikhsia_k_obshchemu_imushchestvu_v_mnogokvartirnom_dome': 4,
                                     'remont_pozharnogo_vodoprovoda': 5,
                                     'remont_vnutrennego_vodostoka': 6,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_elektrosnabzheniia': 7,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_gazosnabzheniia': 8,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_goriachego_vodosnabzheniia_razvodiashchie_magistrali': 9,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_goriachego_vodosnabzheniia_stoiaki': 10,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_kholodnogo_vodosnabzheniia_razvodiashchie_magistrali': 11,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_kholodnogo_vodosnabzheniia_stoiaki': 12,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_teplosnabzheniia_razvodiashchie_magistrali': 13,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_teplosnabzheniia_stoiaki': 14,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_vodootvedeniia_kanalizatsii_stoiaki': 15,
                                     'remont_vnutridomovykh_inzhenernykh_sistem_vodootvedeniia_kanalizatsii_vypuski_i_sbornye_truboprovody': 16,
                                     'zamena_liftovogo_oborudovaniia': 17,
                                     'zamena_okonnykh_blokov_raspolozhennykh_v_pomeshcheniiakh_obshchego_polzovaniia': 18},
                       'ElevatorNumber': {'0': 0,
                                          '1': 1,
                                          '10': 2,
                                          '10а': 3,
                                          '10б': 4,
                                          '11': 5,
                                          '12': 6,
                                          '1а': 7,
                                          '1б': 8,
                                          '1в': 9,
                                          '2': 10,
                                          '2а': 11,
                                          '2б': 12,
                                          '2в': 13,
                                          '3': 14,
                                          '3а': 15,
                                          '3б': 16,
                                          '4': 17,
                                          '4а': 18,
                                          '4б': 19,
                                          '5': 20,
                                          '5а': 21,
                                          '5б': 22,
                                          '6': 23,
                                          '6а': 24,
                                          '6б': 25,
                                          '7': 26,
                                          '7а': 27,
                                          '7б': 28,
                                          '8': 29,
                                          '8а': 30,
                                          '8б': 31,
                                          '9': 32,
                                          '9а': 33,
                                          '9б': 34},
                       'incident_name': {'None': 0,
                                         'anomalnoe_znachenie_massy_v_podaiushchem_truboprovode': 1,
                                         'anomalnoe_znachenie_obema_v_obratnom_truboprovode': 2,
                                         'anomalnoe_znachenie_obema_v_podaiushchem_truboprovode': 3,
                                         'anomalnoe_znachenie_otpushchennoi_teplovoi_energii': 4,
                                         'anomalnoe_znachenie_raznitsy_temperatur': 5,
                                         'anomalnoe_znachenie_temperatury_v_obratnom_truboprovode': 6,
                                         'anomalnoe_znachenie_temperatury_v_podaiushchem_truboprovode': 7,
                                         'anomalnoe_znachenie_vremeni_narabotki': 8,
                                         'avariinaia_protechka_s_krovli': 9,
                                         'avariinaia_protechka_trub_v_podezde': 10,
                                         'avariinaia_protechka_v_podezde': 11,
                                         'avariinoe_povrezhdenie_lestnitsy': 12,
                                         'blokirovka_vkhodnoi_dveri': 13,
                                         'datchik_vibratsii': 14,
                                         'gul_shum_na_obekte_ao_mosgaz_zapakh_gaza_na_ulitse': 15,
                                         'gul_shum_vibratsiia_ot_gazoprovoda': 16,
                                         'izmenenie_kanala_sviazi': 17,
                                         'izmenenie_konfiguratsii_uspd': 18,
                                         'kachestvo_vody_rzhavaia_voda': 19,
                                         'kachestvo_vody_voda_s_zapakhom': 20,
                                         'khlopok_gaza': 21,
                                         'kolodtsy_khlopaet_kryshka': 22,
                                         'kolodtsy_liuk_raskolot': 23,
                                         'kolodtsy_liuk_sdvinut': 24,
                                         'kolodtsy_liuk_zanizhen': 25,
                                         'kolodtsy_liuk_zavyshen': 26,
                                         'kolodtsy_prochee': 27,
                                         'kolodtsy_proval_kolodtsa': 28,
                                         'kolodtsy_razrushen_asfalt_vokrug_kolodtsa': 29,
                                         'kritichnoe_otklonenie_temperatury_gvs_nizhe_normy_dnem_monitoring': 30,
                                         'kritichnoe_otklonenie_temperatury_gvs_nizhe_normy_nochiu_monitoring': 31,
                                         'lift_trebuet_remonta': 32,
                                         'nalichie_gribka_pleseni': 33,
                                         'nalichie_krys_myshei_nasekomykh_v_mestakh_obshchego_polzovaniia': 34,
                                         'nalichie_nadpisei_obiavlenii': 35,
                                         'narushenie_na_nastennom_gazoprovode': 36,
                                         'narushenie_na_nastennom_gazoprovode_zapakh_gaza_v_kukhne': 37,
                                         'narushenie_podachi_vody_net_vody_v_zdanii': 38,
                                         'narushenie_podachi_vody_prochee': 39,
                                         'narushenie_podachi_vody_slaboe_davlenie': 40,
                                         'narushenie_v_rabote_gazovogo_oborudovaniia': 41,
                                         'nedogrev_gvs': 42,
                                         'nedokomplekt_pozharnogo_shkafa': 43,
                                         'neispravnost_pozharnoi_signalizatsii': 44,
                                         'neispravnost_zapiraiushchego_ustroistva': 45,
                                         'neochishchennaia_krovlia': 46,
                                         'nerabotosposobnost_podemnoi_platformy_dlia_invalidov': 47,
                                         'nesovpadenie_seriinogo_nomera_pu_na_uspd': 48,
                                         'net_gaza': 49,
                                         'net_pitaniia_uspd': 50,
                                         'net_sviazi_s_pu': 51,
                                         'net_sviazi_s_uspd': 52,
                                         'neudovletvoritelnoe_sanitarnoe_soderzhanie_musoroprovoda': 53,
                                         'neudovletvoritelnoe_tekhnicheskoe_soderzhanie_musoroprovoda': 54,
                                         'nizkii_uroven_signala_gsm': 55,
                                         'obrushenie': 56,
                                         'opisanie_otsutstvuet': 57,
                                         'otklonenie_gvs_nizhe_normy_dnem_monitoring': 58,
                                         'otklonenie_gvs_nizhe_normy_nochiu_monitoring': 59,
                                         'otkryt_kolodets': 60,
                                         'otkryt_kolodets_mg': 61,
                                         'otkryt_kolodets_na_gazone': 62,
                                         'otkryt_shkaf_uspd': 63,
                                         'otritsatelnye_integralnye_znacheniia': 64,
                                         'otsutstvie_gvs_v_dome': 65,
                                         'otsutstvie_khvs_v_dome': 66,
                                         'otsutstvie_osveshcheniia_v_lifte': 67,
                                         'otsutstvie_osveshcheniia_v_mestakh_obshchego_polzovaniia': 68,
                                         'otsutstvie_otopleniia_v_dome': 69,
                                         'otsutstvie_sviazi': 70,
                                         'otsutstvuet_tsirkuliatsiia_gvs': 71,
                                         'otsutstvuiut_aktualnye_mgnovennye_znacheniia': 72,
                                         'otsutstvuiut_aktualnye_sutochnye_znacheniia': 73,
                                         'p1_0': 74,
                                         'p2_0': 75,
                                         'podtoplenie_kanala_teploseti': 76,
                                         'podtoplenie_postupaet_voda_v_kameru_teploseti': 77,
                                         'podtoplenie_povrezhdenie_vodoprovoda_vo_vnutrikvartalnom_kollektore': 78,
                                         'podtoplenie_prochee': 79,
                                         'podtoplenie_stroenii': 80,
                                         'podtoplenie_tech_truboprovoda_na_vodomernom_uzle': 81,
                                         'podtoplenie_tech_zadvizhki_na_vodomernom_uzle': 82,
                                         'podtoplenie_voda_postupaet_v_kotlovan_stroitelei': 83,
                                         'polomka_lifta': 84,
                                         'polomka_osveshcheniia_pered_podezdom': 85,
                                         'polomka_pandusa': 86,
                                         'polomka_pochtovykh_iashchikov': 87,
                                         'povrezhdenie_asfaltobetonnogo_pokrytiia': 88,
                                         'povrezhdenie_elementov_fasada': 89,
                                         'povrezhdenie_elementov_vkhodnoi_dveri': 90,
                                         'povrezhdenie_inzhenernykh_setei': 91,
                                         'povrezhdenie_kozyrka_podezda': 92,
                                         'povrezhdenie_krovli': 93,
                                         'povrezhdenie_mezhpanelnykh_shvov': 94,
                                         'povrezhdenie_otdelochnykh_pokrytii_pola_steny_stupenei_peril_drugikh_elementov': 95,
                                         'povrezhdenie_pola_steny_stupenei_peril_drugikh_elementov': 96,
                                         'povrezhdenie_polomka_svetilnika': 97,
                                         'povrezhdenie_sistemy_elektroprovodki_shchitovogo_oborudovaniia': 98,
                                         'povrezhdenie_vnutrennei_dveri': 99,
                                         'pozhar': 100,
                                         'pozhar_zadymlenie': 101,
                                         'proryv_teploseti_vodoprovoda': 102,
                                         'protechka_s_balkona_kozyrka': 103,
                                         'protechka_s_krovli': 104,
                                         'protechka_trub_v_podezde': 105,
                                         'protechka_v_podezde': 106,
                                         'proval': 107,
                                         'proval_na_meste_staroi_raskopki': 108,
                                         'provaly_prochee': 109,
                                         'proverit_nastennyi_gazoprovod': 110,
                                         'raskhozhdenie_vremeni_pu': 111,
                                         'razbito_slomano_povrezhdeno_okno_v_mestakh_obshchego_polzovaniia': 112,
                                         'silnaia_tech_v_sisteme_otopleniia': 113,
                                         't1_max': 114,
                                         't1_min': 115,
                                         'tech_v_sisteme_otopleniia': 116,
                                         'temperatura_gvs_nizhe_normy': 117,
                                         'temperatura_v_kvartire_nizhe_normativnoi': 118,
                                         'temperatura_v_pomeshchenii_obshchego_polzovaniia_nizhe_normativnoi': 119,
                                         'ugroza_vzryva': 120,
                                         'utechka_vody_iz_kolodtsa_postupaet_na_proezzhuiu_chast': 121,
                                         'utechka_vody_iz_kolodtsa_prochee': 122,
                                         'utechka_vody_iz_pod_asfalta_prochee': 123,
                                         'utechka_vody_iz_zemli_postupaet_na_proezzhuiu_chast': 124,
                                         'utechka_vody_iz_zemli_prochee': 125,
                                         'utechka_vody_prochee': 126,
                                         'vibriruet_gazovaia_truba': 127,
                                         'vzryv': 128,
                                         'zadymlenie': 129,
                                         'zagriaznenie_lifta': 130,
                                         'zagriaznenie_okna_v_mestakh_obshchego_polzovaniia': 131,
                                         'zagriaznenie_otdelochnykh_pokrytii': 132,
                                         'zagriaznenie_vkhodnoi_dveri': 133,
                                         'zagriaznenie_vody': 134,
                                         'zagriaznenie_zamusorennost_kozyrka': 135,
                                         'zagriaznenie_zamusorennost_podezda': 136,
                                         'zagriaznenie_zamusorennost_podvala_polupodvala': 137,
                                         'zagriaznenie_zamusorennost_territorii': 138,
                                         'zapakh_gari_v_kvartire_podezde': 139,
                                         'zapakh_gaza_iz_zakrytoi_kvartiry': 140,
                                         'zapakh_gaza_na_ulitse': 141,
                                         'zapakh_gaza_na_ulitse_zapakh_gaza_v_dome': 142,
                                         'zapakh_gaza_ot_gazovogo_oborudovaniia': 143,
                                         'zapakh_gaza_ot_kolonki': 144,
                                         'zapakh_gaza_ot_stoiaka': 145,
                                         'zapakh_gaza_s_ulitsy_v_kvartiru': 146,
                                         'zapakh_gaza_v_dome': 147,
                                         'zapakh_gaza_v_kholle': 148,
                                         'zapakh_gaza_v_kholle_i_kvartire': 149,
                                         'zapakh_gaza_v_kukhne': 150,
                                         'zapakh_gaza_v_kukhne_zapakh_gaza_v_dome': 151,
                                         'zapakh_gaza_v_kvartire': 152,
                                         'zapakh_gaza_v_kvartire_pomeshchenii': 153,
                                         'zapakh_gaza_v_kvartire_pomeshchenii_zapakh_gaza_v_dome': 154,
                                         'zapakh_gaza_v_podezde': 155,
                                         'zapakh_gaza_v_podezde_i_na_ulitse': 156,
                                         'zapakh_gaza_v_podezde_i_v_kvartire': 157,
                                         'zapakh_gaza_v_pomeshchenii': 158,
                                         'zasor_kanalizatsii': 159,
                                         'zasor_musoroprovoda': 160,
                                         'zasor_na_gorodskoi_seti': 161,
                                         'zasory_prochee': 162,
                                         'zasory_zasor_na_dvorovoi_seti': 163,
                                         'zastrevanie_v_lifte': 164},
                       'source': {'ASUPR': 0,
                                  'CAFAP': 1,
                                  'EDC': 2,
                                  'MGI': 3,
                                  'MOS_GAS': 4,
                                  'MVK': 5,
                                  'NG': 6},
                       'build_year': {'1900': 0,
                                      '1924': 1,
                                      '1930': 2,
                                      '1932': 3,
                                      '1939': 4,
                                      '1947': 5,
                                      '1950': 6,
                                      '1951': 7,
                                      '1952': 8,
                                      '1953': 9,
                                      '1954': 10,
                                      '1955': 11,
                                      '1956': 12,
                                      '1957': 13,
                                      '1958': 14,
                                      '1959': 15,
                                      '1960': 16,
                                      '1961': 17,
                                      '1962': 18,
                                      '1963': 19,
                                      '1964': 20,
                                      '1965': 21,
                                      '1966': 22,
                                      '1967': 23,
                                      '1968': 24,
                                      '1969': 25,
                                      '1970': 26,
                                      '1971': 27,
                                      '1972': 28,
                                      '1973': 29,
                                      '1974': 30,
                                      '1975': 31,
                                      '1976': 32,
                                      '1977': 33,
                                      '1978': 34,
                                      '1979': 35,
                                      '1980': 36,
                                      '1981': 37,
                                      '1982': 38,
                                      '1983': 39,
                                      '1984': 40,
                                      '1985': 41,
                                      '1988': 42,
                                      '1996': 43,
                                      '1997': 44,
                                      '1998': 45},
                       'project_series': {'2048744': 0,
                                          '2048745': 1,
                                          '2048751': 2,
                                          '2048752': 3,
                                          '2048755': 4,
                                          '2048756': 5,
                                          '2048757': 6,
                                          '2048758': 7,
                                          '2048759': 8,
                                          '2048763': 9,
                                          '2048764': 10,
                                          '2048765': 11,
                                          '2048776': 12,
                                          '2048777': 13,
                                          '2048779': 14,
                                          '2048780': 15,
                                          '2048781': 16,
                                          '2048783': 17,
                                          '2048785': 18,
                                          '2048787': 19,
                                          '2048789': 20,
                                          '2048798': 21,
                                          '2048803': 22,
                                          '2048824': 23,
                                          '2048842': 24,
                                          '2048850': 25,
                                          '2048912': 26,
                                          '56181305': 27,
                                          '56183238': 28,
                                          '56183241': 29,
                                          '56183243': 30,
                                          '56183245': 31,
                                          '56183251': 32,
                                          '56183254': 33,
                                          '56183255': 34,
                                          '56183256': 35,
                                          '56183257': 36,
                                          '56183261': 37,
                                          '56183262': 38,
                                          '56183263': 39,
                                          '56183435': 40,
                                          '73851631': 41},
                       'floars': {'10': 0,
                                  '11': 1,
                                  '12': 2,
                                  '13': 3,
                                  '14': 4,
                                  '16': 5,
                                  '17': 6,
                                  '19': 7,
                                  '22': 8,
                                  '3': 9,
                                  '4': 10,
                                  '5': 11,
                                  '6': 12,
                                  '7': 13,
                                  '8': 14,
                                  '9': 15},
                       'entrances': {'1': 0,
                                     '10': 1,
                                     '12': 2,
                                     '2': 3,
                                     '3': 4,
                                     '4': 5,
                                     '5': 6,
                                     '6': 7,
                                     '7': 8,
                                     '8': 9,
                                     '9': 10},
                       'energyefficiency_class': {'0': 0},
                       'wall_material': {'179625089': 0,
                                         '179625090': 1,
                                         '179625095': 2,
                                         '179625097': 3,
                                         '179625102': 4,
                                         '179625104': 5,
                                         '179625107': 6,
                                         '2048929': 7,
                                         '261908925': 8},
                       'passenger_elevators': {'0': 0,
                                               '1': 1,
                                               '10': 2,
                                               '12': 3,
                                               '16': 4,
                                               '18': 5,
                                               '2': 6,
                                               '3': 7,
                                               '4': 8,
                                               '5': 9,
                                               '6': 10,
                                               '7': 11,
                                               '8': 12,
                                               '9': 13},
                       'passenger_freight_elevators': {'0': 0,
                                                       '1': 1,
                                                       '10': 2,
                                                       '2': 3,
                                                       '3': 4,
                                                       '4': 5,
                                                       '5': 6,
                                                       '7': 7,
                                                       '9': 8},
                       'roof_cleaning': {'0': 0, '22289162': 1, '22289163': 2},
                       'COL_781': {'22289201': 0, '22289204': 1, '22289205': 2, '22289214': 3},
                       'management_status_MKD': {'45063109': 0, '45063584': 1, '45063585': 2},
                       'freight_elevators': {'0': 0}}


# predict date of work close
def predirct_work_end(df_merged):
    # Загрузка модели
    model = joblib.load('close_date_day_model.sav')

    # Выбор одной строки данных
    row = df_merged.iloc[0]

    input_data = row[
        ['external_create_date_month', 'time_delta', 'external_create_date_day', 'close_date_month']]

    # Преобразование строки в формат, ожидаемый моделью
    input_data = input_data.values.reshape(1, -1)

    # Предсказание с использованием загруженной модели
    prediction = model.predict(input_data)

    print(prediction)
    # print("Result: {0:.2f} %".format(100 * prediction))
    return prediction


### predict incident
def predict_incident(df_merged):
    # Загрузка модели
    best_inc_model = CatBoostClassifier()
    best_inc_model.load_model('catboost_best_incident_model.cbm')
    print('catboost_best_incident_model.cbm loaded!')

    # Выбор одной строки данных
    row = df_merged.iloc[4000]

    input_data = row.drop(['incident_name', 'UNOM'])

    # Преобразование строки в формат, ожидаемый моделью
    input_data = input_data.values.reshape(1, -1)

    # Предсказание с использованием загруженной модели
    predictions = best_inc_model.predict(input_data)[0]
    print(predictions)

    for prediction in predictions:
        original_prediction = None
        for feature, mapping in encoded_values_dict.items():
            if prediction in mapping.values():
                original_value = next(key for key, value in mapping.items() if value == prediction)
                original_prediction = (feature, original_value)
                break
        if original_prediction is not None and 'incident_name' in original_prediction:
            print(f"Предсказание: {original_prediction[0]} - {original_prediction[1]}")
        else:
            print("Неизвестное предсказание")

    return predictions


### predict work
def predict_work(df_merged):
    # Загрузка модели
    best_inc_model = CatBoostClassifier()
    best_inc_model.load_model('catboost_best_work_model.cbm')
    print('catboost_best_work_model.cbm loaded!')

    # Выбор одной строки данных
    row = df_merged.iloc[0]

    input_data = row.drop(['WORK_NAME', 'UNOM'])

    # Преобразование строки в формат, ожидаемый моделью
    input_data = input_data.values.reshape(1, -1)

    # Предсказание с использованием загруженной модели
    predictions = best_inc_model.predict(input_data)[0]
    print(predictions)

    for prediction in predictions:
        original_prediction = None
        for feature, mapping in encoded_values_dict.items():
            if prediction in mapping.values():
                original_value = next(key for key, value in mapping.items() if value == prediction)
                original_prediction = (feature, original_value)
                break
        if original_prediction is not None and 'WORK_NAME' in original_prediction:
            print(f"Предсказание: {original_prediction[0]} - {original_prediction[1]}")
        else:
            print("Неизвестное предсказание")

    return predictions


### predict fact date end day
def predirct_fact_date_day_end(df_merged):

    model = joblib.load('FACT_DATE_END_day.sav')

    # Выбор одной строки данных
    row = df_merged.iloc[0]

    input_data = row[
        ['PLAN_DATE_START_year',  'PLAN_DATE_START_month',  'PLAN_DATE_START_day',  'PLAN_DATE_END_year',
            'PLAN_DATE_END_month',  'PLAN_DATE_END_day',  'FACT_DATE_START_year',  'FACT_DATE_START_month',
            'FACT_DATE_START_day',
            'external_create_date_year',  'external_create_date_month',  'external_create_date_day',  'done_date_year',
            'done_date_month',  'done_date_day', 'close_date_year',  'close_date_month',  'close_date_day']]

    # Преобразование строки в формат, ожидаемый моделью
    input_data = input_data.values.reshape(1, -1)

    # Предсказание с использованием загруженной модели
    prediction = model.predict(input_data)

    print("FACT_DATE_END_day:", prediction)
    # print("Result: {0:.2f} %".format(100 * prediction))
    return prediction


### predict fact date start day
def predirct_fact_date_day_start(df_merged):
    model = joblib.load('FACT_DATE_START_day.sav')

    # Выбор одной строки данных
    row = df_merged.iloc[0]

    input_data = row[
        ['PLAN_DATE_END_year',
            'PLAN_DATE_END_month',  'PLAN_DATE_END_day',  'FACT_DATE_START_year',  'FACT_DATE_START_month',
            'FACT_DATE_END_year',  'FACT_DATE_END_month',  'FACT_DATE_END_day',
            'external_create_date_year',  'external_create_date_month',  'external_create_date_day',  'done_date_year',
            'done_date_month',  'done_date_day', 'close_date_year',  'close_date_month',  'close_date_day']]

    # Преобразование строки в формат, ожидаемый моделью
    input_data = input_data.values.reshape(1, -1)

    # Предсказание с использованием загруженной модели
    prediction = model.predict(input_data)

    print("FACT_DATE_START_day:", prediction)
    # print("Result: {0:.2f} %".format(100 * prediction))
    return prediction



df = pd.read_csv('dataset.csv')
# first_line = df.iloc[0]
# print(first_line)

# predirct_work_end(df)
# predict_incident(df)
# predict_work(df)
predirct_fact_date_day_start(df)
predirct_fact_date_day_end(df)
