from datetime import timedelta
from datetime import time


def time_validation(time_logged):
    time_split = []
    time_format = []
    for x in time_logged:
    	h_m_s = x.split(':')
    	time_split.append(h_m_s)
    for x in time_split:
    	temp = timedelta(hours=int(x[0]), minutes=int(x[1]), seconds=int(x[2]))
    	time_format.append(temp)

    c = sum((time_format), timedelta())
    if(c.days >= 1):
    	return False
    else:
    	return True


def total_time(time_logged):
    res = []
    time_split = []
    time_format = []
    for x in time_logged:
    	h_m_s = x.split(':')
    	time_split.append(h_m_s)
    for x in time_split:
    	temp = timedelta(hours=int(x[0]), minutes=int(x[1]), seconds=int(x[2]))
    	time_format.append(temp)
    c = sum((time_format), timedelta())
    total = str(c)
    total = total.split(':')
    day = total[0]
    minut = total[1]
    day_sp = day.split(",")
    if(len(day_sp) > 1):
        days = day.split(" ")
        days = day[0]
        hours = day_sp[1]
        total_days = int(days)*24+(int(hours))
        final = str(total_days)
        res.append(final)
    else:
        hours = day_sp[0]
        res.append(hours)
    res.append(minut)
    s = ':'
    s = s.join(res) 
    return s

def time_function_filter(user_id, q_key, dt, mnth, yr):
    if(q_key==True):
        time_logged = []
        for x in q_key:
            if(bool(dt) == True or bool(mnth) == True or bool(yr) == True):
                gg = str(x.entry_date).split('-')
                if(gg[0] == yr):
                    time_logged.append(str(x.hours_logged))
                elif(gg[1] == mnth):
                    time_logged.append(str(x.hours_logged))
                elif(gg[2] == dt):
                    time_logged.append(str(x.hours_logged))
            else:
                time_logged.append(str(x.hours_logged)) 
        temp = total_time(time_logged)
        return temp
    else:
        return False

def time_function(q_key):
    if(q_key == True):
        time_logged = []
        for x in q_key:
            time_logged.append(str(x.hours_logged))
            temp = total_time(time_logged)
            return temp
    else:
        return False




