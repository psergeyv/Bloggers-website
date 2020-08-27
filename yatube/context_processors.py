import datetime as dt


def year(request):
    date_today = dt.datetime.today()
    year =  date_today.year
    #return {'year':f'2010 - {year}'}
    return {'year':year}