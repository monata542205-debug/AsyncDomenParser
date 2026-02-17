import os
import sys
import datetime

def resource_path(rel_path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel_path)

def dates():
    today = str(datetime.datetime.today() - datetime.timedelta(days=1)).split()[0]
    print('yesterday: ', today)
    return today

def days_write(today):
    with open(resource_path('day.txt'), 'w', encoding='utf-8') as f:
        f.write(today + '\n')
    print('date is recorded')

def days_read():
    with open(resource_path('day.txt'), 'r', encoding='utf-8') as f:
        day = f.readlines()[0][:-1]
    print('recording day: ', day)
    return day

if __name__ == '__main__':
    today = dates()
    day = days_read()
    if day == today: print('day is respond')
    else: days_write(today)