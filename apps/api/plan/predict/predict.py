import os
import sys
import warnings
from datetime import date

import catboost
import joblib
import numpy as np
import openpyxl
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor, Pool
from sklearn import metrics
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from slugify import slugify

warnings.filterwarnings("ignore", category=UserWarning)
# print module versions for reproducibility
# print("CatBoost version {}".format(catboost.__version__))
# print("NumPy version {}".format(np.__version__))
# print("Pandas version {}".format(pd.__version__))

source_dict = {"ASUPR": 0, "CAFAP": 1, "EDC": 2, "MGI": 3, "MOS_GAS": 4, "MVK": 5, "NG": 6}


encoded_values_dict = {
    "WORK_NAME": {
        "ремонт фасадов": 0,
        "ремонт крыши": 1,
        "ремонт мусоропровода": 2,
        "ремонт подъездов, направленный на восстановление их надлежащего состояния и проводимый при выполнении иных работ по капитальному ремонту общего имущества в многоквартирном доме": 3,
        "ремонт подвальных помещений, относящихся к общему имуществу в многоквартирном доме": 4,
        "ремонт пожарного водопровода": 5,
        "ремонт внутреннего водостока": 6,
        "ремонт внутридомовых инженерных систем электроснабжения": 7,
        "ремонт внутридомовых инженерных систем газоснабжения": 8,
        "ремонт внутридомовых инженерных систем горячего водоснабжения (разводящие магистрали)": 9,
        "ремонт внутридомовых инженерных систем горячего водоснабжения (стояки)": 10,
        "ремонт внутридомовых инженерных систем холодного водоснабжения (разводящие магистрали)": 11,
        "ремонт внутридомовых инженерных систем холодного водоснабжения (стояки)": 12,
        "ремонт внутридомовых инженерных систем теплоснабжения (разводящие магистрали)": 13,
        "ремонт внутридомовых инженерных систем теплоснабжения (стояки)": 14,
        "ремонт внутридомовых инженерных систем водоотведения (канализации) (стояки)": 15,
        "ремонт внутридомовых инженерных систем водоотведения (канализации) (выпуски и сборные трубопроводы)": 16,
        "замена лифтового оборудования": 17,
        "замена оконных блоков, расположенных в помещениях общего пользования": 18,
    },
    "ElevatorNumber": {
        "0": 0,
        "1": 1,
        "10": 2,
        "10а": 3,
        "10б": 4,
        "11": 5,
        "12": 6,
        "1а": 7,
        "1б": 8,
        "1в": 9,
        "2": 10,
        "2а": 11,
        "2б": 12,
        "2в": 13,
        "3": 14,
        "3а": 15,
        "3б": 16,
        "4": 17,
        "4а": 18,
        "4б": 19,
        "5": 20,
        "5а": 21,
        "5б": 22,
        "6": 23,
        "6а": 24,
        "6б": 25,
        "7": 26,
        "7а": 27,
        "7б": 28,
        "8": 29,
        "8а": 30,
        "8б": 31,
        "9": 32,
        "9а": 33,
        "9б": 34,
    },
    "incident_name": {
        "None": 0,
        "аномальное значение массы в подающем трубопроводе": 1,
        "аномальное значение объема в обратном трубопроводе": 2,
        "аномальное значение объема в подающем трубопроводе": 3,
        "аномальное значение отпущенной тепловой энергии": 4,
        "аномальное значение разницы температур": 5,
        "аномальное значение температуры в обратном трубопроводе": 6,
        "аномальное значение температуры в подающем трубопроводе": 7,
        "аномальное значение времени наработки": 8,
        "аварийная протечка с кровли": 9,
        "аварийная протечка труб в подъезде": 10,
        "аварийная протечка в подъезде": 11,
        "аварийное повреждение лестницы": 12,
        "блокировка входной двери": 13,
        "датчик вибрации": 14,
        "гул (шум) на объекте ао мосгаз; запах газа на улице": 15,
        "гул (шум, вибрация) от газопровода": 16,
        "изменение канала связи": 17,
        "изменение конфигурации успд": 18,
        "качество воды - ржавая вода": 19,
        "качество воды - вода с запахом": 20,
        "хлопок газа": 21,
        "колодцы, хлопает крышка": 22,
        "колодцы, люк расколот": 23,
        "колодцы, люк сдвинут": 24,
        "колодцы, люк занижен": 25,
        "колодцы, люк завышен": 26,
        "колодцы, прочее": 27,
        "колодцы, провал колодца": 28,
        "колодцы, разрушен асфальт вокруг колодца": 29,
        "критичное отклонение температуры гвс ниже нормы днем (мониторинг)": 30,
        "критичное отклонение температуры гвс ниже нормы ночью (мониторинг)": 31,
        "лифт требует ремонта": 32,
        "наличие грибка/плесени": 33,
        "наличие крыс/мышей/насекомых в местах общего пользования": 34,
        "наличие надписей/объявлений": 35,
        "нарушение на настенном газопроводе": 36,
        "нарушение на настенном газопроводе; запах газа в кухне": 37,
        "нарушение подачи воды, нет воды в здании": 38,
        "нарушение подачи воды, прочее": 39,
        "нарушение подачи воды, слабое давление": 40,
        "нарушение в работе газового оборудования": 41,
        "недогрев гвс": 42,
        "недокомплект пожарного шкафа": 43,
        "неисправность пожарной сигнализации": 44,
        "неисправность запирающего устройства": 45,
        "неочищенная кровля": 46,
        "неработоспособность подъемной платформы для инвалидов": 47,
        "несовпадение серийного номера пу на успд": 48,
        "нет газа": 49,
        "нет питания успд": 50,
        "нет связи с пу": 51,
        "нет связи с успд": 52,
        "неудовлетворительное санитарное содержание мусоропровода": 53,
        "неудовлетворительное техническое содержание мусоропровода": 54,
        "низкий уровень сигнала gsm": 55,
        "обрушение": 56,
        "описание отсутствует": 57,
        "отклонение гвс ниже нормы днем (мониторинг)": 58,
        "отклонение гвс ниже нормы ночью (мониторинг)": 59,
        "открыт колодец": 60,
        "открыт колодец мг": 61,
        "открыт колодец на газоне": 62,
        "открыт шкаф успд": 63,
        "отрицательные интегральные значения": 64,
        "отсутствие гвс в доме": 65,
        "отсутствие хвс в доме": 66,
        "отсутствие освещения в лифте": 67,
        "отсутствие освещения в местах общего пользования": 68,
        "отсутствие отопления в доме": 69,
        "отсутствие связи": 70,
        "отсутствует циркуляция гвс": 71,
        "отсутствуют актуальные мгновенные значения": 72,
        "отсутствуют актуальные суточные значения": 73,
        "p1 <= 0": 74,
        "p2 <= 0": 75,
        "подтопление канала теплосети": 76,
        "подтопление, поступает вода в камеру теплосети": 77,
        "подтопление, повреждение водопровода во внутриквартальном коллекторе": 78,
        "подтопление, прочее": 79,
        "подтопление строения": 80,
        "подтопление, течь трубопровода на водомерном узле": 81,
        "подтопление, течь задвижки на водомерном узле": 82,
        "подтопление, вода поступает в котлован строителей": 83,
        "поломка лифта": 84,
        "поломка освещения перед подъездом": 85,
        "поломка пандуса": 86,
        "поломка почтовых ящиков": 87,
        "повреждение асфальтобетонного покрытия": 88,
        "повреждение элементов фасада": 89,
        "повреждение элементов входной двери": 90,
        "повреждение инженерных сетей": 91,
        "повреждение козырька подъезда": 92,
        "повреждение кровли": 93,
        "повреждение межпанельных швов": 94,
        "повреждение отделочных покрытий пола/стены/ступеней/перил/других элементов": 95,
        "повреждение пола/стены/ступеней/перил/других элементов": 96,
        "повреждение/поломка светильника": 97,
        "повреждение системы электропроводки/щитового оборудования": 98,
        "повреждение внутренней двери": 99,
        "пожар": 100,
        "пожар; задымление": 101,
        "прорыв теплосети (водопровода)": 102,
        "протечка с балкона/козырька": 103,
        "протечка с кровли": 104,
        "протечка труб в подъезде": 105,
        "протечка в подъезде": 106,
        "провал": 107,
        "провал на месте старой раскопки": 108,
        "провалы, прочее": 109,
        "проверить настенный газопровод": 110,
        "расхождение времени пу": 111,
        "разбито/сломано/повреждено окно в местах общего пользования": 112,
        "сильная течь в системе отопления": 113,
        "t1 > max": 114,
        "t1 < min": 115,
        "течь в системе отопления": 116,
        "температура гвс ниже нормы": 117,
        "температура в квартире ниже нормативной": 118,
        "температура в помещении общего пользования ниже нормативной": 119,
        "угроза взрыва": 120,
        "утечка воды из колодца, поступает на проезжую часть": 121,
        "утечка воды из колодца, прочее": 122,
        "утечка воды из-под асфальта, прочее": 123,
        "утечка воды из земли, поступает на проезжую часть": 124,
        "утечка воды из земли, прочее": 125,
        "утечка воды, прочее": 126,
        "вибрирует газовая труба": 127,
        "взрыв": 128,
        "задымление": 129,
        "загрязнение лифта": 130,
        "загрязнение окна в местах общего пользования": 131,
        "загрязнение отделочных покрытий": 132,
        "загрязнение входной двери": 133,
        "загрязнение воды": 134,
        "загрязнение/замусоренность козырька": 135,
        "загрязнение/замусоренность подъезда": 136,
        "загрязнение/замусоренность подвала/полуподвала": 137,
        "загрязнение/замусоренность территории": 138,
        "запах гари в квартире/подъезде": 139,
        "запах газа из закрытой квартиры": 140,
        "запах газа на улице": 141,
        "запах газа на улице; запах газа в доме": 142,
        "запах газа от газового оборудования": 143,
        "запах газа от колонки": 144,
        "запах газа от стояка": 145,
        "запах газа с улицы в квартиру": 146,
        "запах газа в доме": 147,
        "запах газа в холле": 148,
        "запах газа в холле и квартире": 149,
        "запах газа в кухне": 150,
        "запах газа в кухне; запах газа в доме": 151,
        "запах газа в квартире": 152,
        "запах газа в квартире (помещении)": 153,
        "запах газа в квартире (помещении); запах газа в доме": 154,
        "запах газа в подъезде": 155,
        "запах газа в подъезде и на улице": 156,
        "запах газа в подъезде и в квартире": 157,
        "запах газа в помещении": 158,
        "засор канализации": 159,
        "засор мусоропровода": 160,
        "засор на городской сети": 161,
        "засоры, прочее": 162,
        "засоры, засор на дворовой сети": 163,
        "застревание в лифте": 164,
    },
    "source": {"ASUPR": 0, "CAFAP": 1, "EDC": 2, "MGI": 3, "MOS_GAS": 4, "MVK": 5, "NG": 6},
    "build_year": {
        "1900": 0,
        "1924": 1,
        "1930": 2,
        "1932": 3,
        "1939": 4,
        "1947": 5,
        "1950": 6,
        "1951": 7,
        "1952": 8,
        "1953": 9,
        "1954": 10,
        "1955": 11,
        "1956": 12,
        "1957": 13,
        "1958": 14,
        "1959": 15,
        "1960": 16,
        "1961": 17,
        "1962": 18,
        "1963": 19,
        "1964": 20,
        "1965": 21,
        "1966": 22,
        "1967": 23,
        "1968": 24,
        "1969": 25,
        "1970": 26,
        "1971": 27,
        "1972": 28,
        "1973": 29,
        "1974": 30,
        "1975": 31,
        "1976": 32,
        "1977": 33,
        "1978": 34,
        "1979": 35,
        "1980": 36,
        "1981": 37,
        "1982": 38,
        "1983": 39,
        "1984": 40,
        "1985": 41,
        "1988": 42,
        "1996": 43,
        "1997": 44,
        "1998": 45,
    },
    "project_series": {
        "2048744": 0,
        "2048745": 1,
        "2048751": 2,
        "2048752": 3,
        "2048755": 4,
        "2048756": 5,
        "2048757": 6,
        "2048758": 7,
        "2048759": 8,
        "2048763": 9,
        "2048764": 10,
        "2048765": 11,
        "2048776": 12,
        "2048777": 13,
        "2048779": 14,
        "2048780": 15,
        "2048781": 16,
        "2048783": 17,
        "2048785": 18,
        "2048787": 19,
        "2048789": 20,
        "2048798": 21,
        "2048803": 22,
        "2048824": 23,
        "2048842": 24,
        "2048850": 25,
        "2048912": 26,
        "56181305": 27,
        "56183238": 28,
        "56183241": 29,
        "56183243": 30,
        "56183245": 31,
        "56183251": 32,
        "56183254": 33,
        "56183255": 34,
        "56183256": 35,
        "56183257": 36,
        "56183261": 37,
        "56183262": 38,
        "56183263": 39,
        "56183435": 40,
        "73851631": 41,
    },
    "floars": {
        "10": 0,
        "11": 1,
        "12": 2,
        "13": 3,
        "14": 4,
        "16": 5,
        "17": 6,
        "19": 7,
        "22": 8,
        "3": 9,
        "4": 10,
        "5": 11,
        "6": 12,
        "7": 13,
        "8": 14,
        "9": 15,
    },
    "entrances": {"1": 0, "10": 1, "12": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 9, "9": 10},
    "energyefficiency_class": {"0": 0},
    "wall_material": {
        "179625089": 0,
        "179625090": 1,
        "179625095": 2,
        "179625097": 3,
        "179625102": 4,
        "179625104": 5,
        "179625107": 6,
        "2048929": 7,
        "261908925": 8,
    },
    "passenger_elevators": {
        "0": 0,
        "1": 1,
        "10": 2,
        "12": 3,
        "16": 4,
        "18": 5,
        "2": 6,
        "3": 7,
        "4": 8,
        "5": 9,
        "6": 10,
        "7": 11,
        "8": 12,
        "9": 13,
    },
    "passenger_freight_elevators": {"0": 0, "1": 1, "10": 2, "2": 3, "3": 4, "4": 5, "5": 6, "7": 7, "9": 8},
    "roof_cleaning": {"0": 0, "22289162": 1, "22289163": 2},
    "COL_781": {"22289201": 0, "22289204": 1, "22289205": 2, "22289214": 3},
    "management_status_MKD": {"45063109": 0, "45063584": 1, "45063585": 2},
    "freight_elevators": {"0": 0},
}


### predict incident
def predict_incident(df_merged, UNOM, source):
    pred = {}

    # Загрузка модели
    best_inc_model = CatBoostClassifier()

    try:
        best_inc_model.load_model("catboost_best_incident_model.cbm")
        print("catboost_best_incident_model.cbm loaded!")
        # Дальнейшие действия с моделью
    except FileNotFoundError:
        print("Ошибка: файл модели catboost_best_incident_model не найден")
        return 0
    except Exception as e:
        print("Ошибка загрузки модели:", str(e))
        return 0

    # Выбор одной строки данных
    row = df_merged.loc[df_merged["UNOM"] == UNOM]
    if row.empty:
        print("UNOM not found!")
        return 0

    source_feature = source_dict[source]
    # print(source_feature)

    # Выбор одной строки данных по UNOM + source
    for index, row in df_merged.loc[(df_merged["UNOM"] == UNOM) & (df_merged["source"] == source_feature)].iterrows():
        if row.empty:
            print("UNOM + source not found!")
            return 0

        input_data = row.drop(["incident_name", "UNOM"])

        # Преобразование строки в формат, ожидаемый моделью
        input_data = input_data.values.reshape(1, -1)

        # Предсказание с использованием загруженной модели
        predictions = best_inc_model.predict(input_data)[0]
        # print(predictions)

        for prediction in predictions:
            original_prediction = None
            for feature, mapping in encoded_values_dict.items():
                if prediction in mapping.values():
                    original_value = next(key for key, value in mapping.items() if value == prediction)
                    original_prediction = (feature, original_value)
                    break
            if original_prediction is not None and "incident_name" in original_prediction:
                # print(f"Предсказание: {original_prediction[0]} - {original_prediction[1]}")
                pred[index] = original_prediction[1]
            else:
                print("Неизвестное предсказание")
    result = dict()
    for value in (values := list(pred.values())):
        result[value] = values.count(value) / len(values)
    return result


### predict work
def predict_work(df_merged, UNOM, source):
    pred = {}

    # Загрузка модели
    best_inc_model = CatBoostClassifier()
    best_inc_model.load_model("catboost_best_work_model.cbm")
    print("catboost_best_work_model.cbm loaded!")

    # Выбор одной строки данных по UNOM
    row = df_merged.loc[df_merged["UNOM"] == UNOM]
    if row.empty:
        print("UNOM not found!")
        return 0

    source_feature = source_dict[source]
    # print(source_feature)

    # Выбор одной строки данных по UNOM + source
    for index, row in df_merged.loc[(df_merged["UNOM"] == UNOM) & (df_merged["source"] == source_feature)].iterrows():
        if row.empty:
            print("UNOM + source not found!")
            return 0

        input_data = row.drop(["WORK_NAME", "UNOM"])

        # Преобразование строки в формат, ожидаемый моделью
        input_data = input_data.values.reshape(1, -1)

        # Предсказание с использованием загруженной модели
        predictions = best_inc_model.predict(input_data)[0]
        # print(predictions)

        for prediction in predictions:
            original_prediction = None
            for feature, mapping in encoded_values_dict.items():
                if prediction in mapping.values():
                    original_value = next(key for key, value in mapping.items() if value == prediction)
                    original_prediction = (feature, original_value)
                    break
            if original_prediction is not None and "WORK_NAME" in original_prediction:
                # print(f"Предсказание: {original_prediction[0]} - {original_prediction[1]}")
                pred[index] = original_prediction[1]
            else:
                print("Неизвестное предсказание")

    return pred


### predict fact date end day
def predirct_fact_date_day_end(df_merged, UNOM, source):
    predictions = []

    model = None
    try:
        model = joblib.load("FACT_DATE_END_day.sav")
        print("Модель FACT_DATE_END_day успешно загружена")
        # Дальнейшие действия с моделью
    except FileNotFoundError:
        print("Ошибка: файл модели FACT_DATE_END_day не найден")
        return 0
    except Exception as e:
        print("Ошибка загрузки модели:", str(e))
        return 0

    # Выбор одной строки данных по UNOM
    row = df_merged.loc[df_merged["UNOM"] == UNOM]
    if row.empty:
        print("UNOM not found!")
        return 0

    source_feature = source_dict[source]
    # print(source_feature)

    # Выбор одной строки данных по UNOM + source
    for index, row in df_merged.loc[(df_merged["UNOM"] == UNOM) & (df_merged["source"] == source_feature)].iterrows():
        if row.empty:
            print("UNOM + source not found!")
            return 0

        input_data = row[
            [
                "PLAN_DATE_START_year",
                "PLAN_DATE_START_month",
                "PLAN_DATE_START_day",
                "PLAN_DATE_END_year",
                "PLAN_DATE_END_month",
                "PLAN_DATE_END_day",
                "FACT_DATE_START_year",
                "FACT_DATE_START_month",
                "FACT_DATE_START_day",
                "external_create_date_year",
                "external_create_date_month",
                "external_create_date_day",
                "done_date_year",
                "done_date_month",
                "done_date_day",
                "close_date_year",
                "close_date_month",
                "close_date_day",
            ]
        ]

        # Преобразование строки в формат, ожидаемый моделью
        input_data = input_data.values.reshape(1, -1)

        # Предсказание с использованием загруженной модели
        prediction = round(model.predict(input_data)[0], 0)
        predictions.append(prediction)
        # print(prediction)
        date_work_start = (
            f"{int(row['PLAN_DATE_START_day'])}.{int(row['PLAN_DATE_START_month'])}.{int(row['PLAN_DATE_START_year'])}"
        )
        pred_str = f"Ориентировочная фактическая дата окончания работ c момента начала ({date_work_start}) на данном объекте: {prediction} дней."
        # print(pred_str)
    return predictions


### predict fact date start day
def predirct_fact_date_day_start(df_merged, UNOM, source):
    predictions = []
    model = None

    try:
        model = joblib.load("FACT_DATE_START_day.sav")
        print("Модель FACT_DATE_START_day успешно загружена")
        # Дальнейшие действия с моделью
    except FileNotFoundError:
        print("Ошибка: файл модели FACT_DATE_START_day не найден")
        return 0
    except Exception as e:
        print("Ошибка загрузки модели:", str(e))
        return 0

    # Выбор одной строки данных по UNOM
    row = df_merged.loc[df_merged["UNOM"] == UNOM]
    if row.empty:
        print("UNOM not found!")
        return 0

    source_feature = source_dict[source]
    # print(source_feature)

    # Выбор одной строки данных по UNOM + source
    for index, row in df_merged.loc[(df_merged["UNOM"] == UNOM) & (df_merged["source"] == source_feature)].iterrows():
        if row.empty:
            print("UNOM + source not found!")
            return 0

        input_data = row[
            [
                "PLAN_DATE_END_year",
                "PLAN_DATE_END_month",
                "PLAN_DATE_END_day",
                "FACT_DATE_START_year",
                "FACT_DATE_START_month",
                "FACT_DATE_END_year",
                "FACT_DATE_END_month",
                "FACT_DATE_END_day",
                "external_create_date_year",
                "external_create_date_month",
                "external_create_date_day",
                "done_date_year",
                "done_date_month",
                "done_date_day",
                "close_date_year",
                "close_date_month",
                "close_date_day",
            ]
        ]

        # Преобразование строки в формат, ожидаемый моделью
        input_data = input_data.values.reshape(1, -1)

        # Предсказание с использованием загруженной модели
        prediction = round(model.predict(input_data)[0], 0)
        predictions.append(prediction)
        # print(prediction)
        # pred_str = f"Ориентировочная фактическая дата начала работ данном объекте: {prediction} дней."
        # print(pred_str)
    return predictions


# predict date of work close
def predirct_work_end(df_merged, UNOM, source):
    predictions = []
    model = None

    try:
        model = joblib.load("close_date_day_model.sav")
        print("Модель close_date_day_model успешно загружена")
        # Дальнейшие действия с моделью
    except FileNotFoundError:
        print("Ошибка: файл модели close_date_day_model не найден")
        return 0
    except Exception as e:
        print("Ошибка загрузки модели:", str(e))
        return 0

    # Выбор одной строки данных
    row = df_merged.loc[df_merged["UNOM"] == UNOM]
    if row.empty:
        print("UNOM not found!")
        return 0

    source_feature = source_dict[source]
    print(source_feature)

    # Выбор одной строки данных по UNOM + source
    for index, row in df_merged.loc[(df_merged["UNOM"] == UNOM) & (df_merged["source"] == source_feature)].iterrows():
        if row.empty:
            print("UNOM + source not found!")
            return 0

        input_data = row[["external_create_date_month", "time_delta", "external_create_date_day", "close_date_month"]]

        # Преобразование строки в формат, ожидаемый моделью
        input_data = input_data.values.reshape(1, -1)

        prediction = round(model.predict(input_data)[0], 0)
        predictions.append(prediction)
        # print(prediction)
        # pred_str = f"Ориентировочная дата закрытия заявки на данном объекте: {prediction} дней."
        # print(pred_str)

    return prediction


df = pd.read_csv("dataset.csv")
# first_line = df.iloc[0]
# print(first_line)

# unique_unom = df['UNOM'].unique().tolist()
# for unom in unique_unom:
#     print(unom)


def get_works(unom: int, sourcesytem: str) -> dict:
    works = predict_work(df, unom, sourcesytem)
    works = list(works.values())
    fact_date_start = predirct_fact_date_day_start(df, unom, sourcesytem)
    fact_date_end = predirct_fact_date_day_end(df, unom, sourcesytem)
    works_with_date = list(zip(works, fact_date_start, fact_date_end))
    agg_works: dict = dict()
    for work in works_with_date:
        if work[0] not in list(agg_works.keys()):
            all_works = list(filter(lambda x: x[0] == work[0], works_with_date))
            start_day = [x[1] for x in all_works]
            end_day = [x[2] for x in all_works]
            agg_works[work[0]] = {
                "start_day": sum(start_day) / len(start_day),
                "end_day": sum(end_day) / len(end_day),
                "acc": len(all_works) / len(works_with_date),
            }
    return agg_works


def get_incident(unom: int, sourcesytem: str) -> dict:
    return predict_incident(df, unom, sourcesytem)


if __name__ == "__main__":
    print(get_works(27715, "ASUPR"))
    print(get_incident(27715, "ASUPR"))
