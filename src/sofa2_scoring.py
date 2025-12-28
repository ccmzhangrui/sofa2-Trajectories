import pandas as pd


def calc_resp(pao2, fio2, vent_mode):
    if pd.isna(pao2) or pd.isna(fio2):
        return 0
    ratio = pao2 / fio2
    if vent_mode == 'high_flow':
        if ratio >= 300:
            return 0
        elif ratio >= 200:
            return 1
        elif ratio >= 100:
            return 3
        else:
            return 4
    else:
        if ratio >= 400:
            return 0
        elif ratio >= 300:
            return 1
        elif ratio >= 200:
            return 2
        elif ratio >= 100:
            return 3
        else:
            return 4


def calc_cardio(map_val, vaso_dose):
    if pd.isna(map_val):
        return 0
    if map_val >= 70 and vaso_dose == 0:
        return 0
    elif vaso_dose > 0 and vaso_dose <= 0.1:
        return 2
    elif vaso_dose > 0.1:
        return 4
    else:
        return 1


def calc_renal(creatinine, rrt):
    if pd.isna(creatinine):
        return 0
    if rrt: return 4
    if creatinine < 1.2:
        return 0
    elif creatinine < 2.0:
        return 1
    elif creatinine < 3.5:
        return 2
    elif creatinine < 5.0:
        return 3
    else:
        return 4


def calculate_sofa2(row):
    resp_score = calc_resp(row['PaO2'], row['FiO2'], row['ventilation_mode'])
    cardio_score = calc_cardio(row['MAP'], row['vasopressor_dose'])
    renal_score = calc_renal(row['creatinine'], row['RRT'])
    # Placeholders for other systems
    liver_score = 0
    coag_score = 0
    neuro_score = 0
    return resp_score + cardio_score + renal_score + liver_score + coag_score + neuro_score
