# Need to be installed matplolib
# file kuka_robot.log needs to be placed in the same script dir

import re
from pathlib import Path
from datetime import datetime as dt

import matplotlib.dates
import matplotlib.pyplot as plt

CWD = Path(__file__).resolve().parent
INPUT_FILENAME = Path(CWD, "kuka_robot.log")

def parse_input_data():
    date_pattern = re.compile("(\d{4}-\d{0,2}-\d{2}\s\d{0,2}:\d{0,2}:\d{0,2}\.[0-9]+).*state.q1.*target.q6", re.MULTILINE)
    state_match_pattern = re.compile("task_name=follow\strajectory;.*state\.q1=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*state\.q2=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*state\.q3=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*state\.q4=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*state\.q5=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*state\.q6=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?)", re.MULTILINE) 
    target_match_pattern = re.compile("task_name=follow\strajectory;.*target\.q1=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*target\.q2=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*target\.q3=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*target\.q4=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*target\.q5=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?).*target\.q6=\s(-?[0-9]?\.?[0-9]+(?:e[+-][0-9]+)?)", re.MULTILINE)
    
    datetime_list = []
    state_list = []
    target_list = [] 
    
    with open(INPUT_FILENAME) as f:
        for line in f:
            state_match = state_match_pattern.search(line)
            target_match = target_match_pattern.search(line)
            date_match = date_pattern.search(line)

            if not (state_match and target_match and date_match):
                continue

            state = state_match.groups()
            target = target_match.groups()
            date_time = date_match.groups()

            state = [float(x) for x in state]
            target = [float(x) for x in target]     
            # date_time = [x[0] for x in date_time]   
            # print(date_time)    

            datetime_list.append(date_time[0])
            state_list.append(state)
            target_list.append(target)

        return state_list, target_list, datetime_list

def calculate_max_difference():
    '''
        Calculate maximum difference between current position and expected
        state for each robot join
    '''
    st, tr, dt_ = parse_input_data()

    # sum of joints
    sum_zip_position = [[x + y for x,y in zip(l1, l2)] for l1,l2 in zip(st,tr)]

    max_position_joint = []

    # maximum difference between current and expected position
    max_position_joint.append(max(sum_zip_position, key=lambda x: x[0])[0])
    max_position_joint.append(max(sum_zip_position, key=lambda x: x[1])[1])
    max_position_joint.append(max(sum_zip_position, key=lambda x: x[2])[2])
    max_position_joint.append(max(sum_zip_position, key=lambda x: x[3])[3])
    max_position_joint.append(max(sum_zip_position, key=lambda x: x[4])[4])
    max_position_joint.append(max(sum_zip_position, key=lambda x: x[5])[5])

    return max_position_joint

def draw_charts():
    '''
        Creates 6 charts for each joint: X axis for time Y axis for difference statetarget 
    '''
    st, tr, dt_ = parse_input_data()
    sum_zip_position = [[x + y for x,y in zip(l1, l2)] for l1,l2 in zip(st,tr)]

    position_joint_a1 = [x[0] for x in sum_zip_position]
    position_joint_a2 = [x[1] for x in sum_zip_position]
    position_joint_a3 = [x[2] for x in sum_zip_position]
    position_joint_a4 = [x[3] for x in sum_zip_position]
    position_joint_a5 = [x[4] for x in sum_zip_position]
    position_joint_a6 = [x[5] for x in sum_zip_position]
    
    matplottime_converted_time = [dt.fromisoformat(x) for x in dt_]
    dates = matplotlib.dates.date2num(matplottime_converted_time)

    plt.plot_date(dates, position_joint_a1)
    plt.xlabel('date-time')
    plt.ylabel('difference state-target')

    plt.plot_date(dates, position_joint_a2)
    plt.xlabel('date-time')
    plt.ylabel('difference state-target')

    plt.plot_date(dates, position_joint_a3)
    plt.xlabel('date-time')
    plt.ylabel('difference state-target')

    plt.plot_date(dates, position_joint_a4)
    plt.xlabel('date-time')
    plt.ylabel('difference state-target')

    plt.plot_date(dates, position_joint_a5)
    plt.xlabel('date-time')
    plt.ylabel('difference state-target')

    plt.plot_date(dates, position_joint_a6)
    plt.xlabel('date-time')
    plt.ylabel('difference state-target')

    plt.show()

def main():
    print(f"Maximum difference of each joint {calculate_max_difference()}")
    draw_charts()
    
if __name__ == "__main__":
    main()
