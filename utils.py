import datetime as dt


def process_hhmm_time(txt: str)-> dt.time:
  """process the HH:MM period format to datetime time object"""

  raw_hour, minute_period = txt.split(':')
  minute = int(minute_period[:2])
  period = minute_period[-1]

  hour = int(raw_hour)
  if period == 'p' and hour != 12:
    hour += 12

  if hour > 23:
    raise ValueError('hour cannot be more than 23')
  if minute > 59:
    raise ValueError('minutes cannot be more than 59')

  return dt.time(hour=int(hour), minute=minute) 

def process_h_or_m_time(txt: str)-> dt.timedelta:
  """process the h or m time format, e.g. 10 m or 1 h"""
  if txt[-1] == 'h':
    # hours
    hours = int(txt[:-1].strip())
    if hours > 23:
      raise ValueError('hours cannot be more than 23')

    return dt.timedelta(hours=-hours)

  else:
    # minutes
    minutes = int(txt[:-1].strip())
    hours = 0
    while minutes > 60:
      hours += 1
      minutes -= 60

    return dt.timedelta(hours=-hours, minutes=-minutes)
    

def process_hm_time(txt: str):
  hours = int(txt.split('h')[0])
  minutes_str = txt.split()[1]
  if 'm' in minutes_str:
    minutes_str = minutes_str[:-1]
  
  minutes = int(minutes_str)

  if minutes > 59:
    raise ValueError('minutes cannot be more than 59')
  return dt.timedelta(hours=-hours, minutes=-minutes)
