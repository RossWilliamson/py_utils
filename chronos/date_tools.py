import datetime

def dt_to_mjd(dtime):
    mjd_start = datetime.datetime(1858,11,17,0,0)
    x = dtime - mjd_start
    return x.days + (x.seconds + x.microseconds*1e-6)/(60.0*60.0*24.0)

def mjdnow():
    t_date = datetime.datetime.utcnow()
    return dt_to_mjd(t_date)

def mjd_to_dt(mjd):
    mjd_start = datetime.datetime(1858,11,17,0,0)
    difference = datetime.timedelta(days=mjd)
    return mjd_start + difference

def date_toolkit(inp,outformat='mjd'):
    if inp == "now":
        t_date = datetime.datetime.utcnow()
    else:
        t_date = inp

    if outformat == 'mjd':
        return dt_to_mjd(t_date)

    if outformat == 'file':
        return t_date.strftime("%Y%m%d_%H%M%S")
