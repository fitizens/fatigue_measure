from scipy.integrate import cumtrapz
import numpy as np
from scipy.signal import filtfilt


def smooth_column(df, column_name):
    window_size = 5
    b = np.ones(window_size) / window_size
    df[f"{column_name}_Smooth"] = filtfilt(b, 1, df[column_name])
    return df


def extract_exercises(series, peaks_list: list, column, threshold=2):
    exercises = []
    current_exercise = []

    index = 0
    is_add = False

    while index < len(series):
        info = series[index]
        if is_add:
            if index in peaks_list and abs(info[column]) < threshold:
                exercises.append(current_exercise)
                current_exercise = []
                is_add = False
            else:
                current_exercise.append(info)
        else:
            if len(peaks_list) >= 2 and index in peaks_list:
                if abs(info[column]) < threshold < abs(series[peaks_list[1]][column]):
                    is_add = True
        if index in peaks_list:
            peaks_list.remove(index)
        index += 1
    return exercises


def extract_jump(series, peaks_list: list, column):
    is_add = False
    data = []

    for index, info in enumerate(series):
        if index in peaks_list and info[column] > 0:
            if is_add:
                break
            else:
                is_add = not is_add
        if is_add:
            data.append(info)
        index += 1

    return data

def compute_height_initial_velocity(df, column):
    g = 9.81
    vertical_acc = df[column].values
    # dx = 1/ 104
    vertical_velocity = cumtrapz(vertical_acc, dx=0.00961538461, initial=0)
    v0 = vertical_velocity.max()
    return (v0 ** 2) / (2 * g)

