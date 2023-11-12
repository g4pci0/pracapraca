from datetime import datetime, timedelta
import pytz
from dateutil.relativedelta import relativedelta

def generate(period_start, period_end, data):

    # Przeksztalc string na datetime
    period_start_dt = datetime.fromisoformat(period_start)
    period_end_dt = datetime.fromisoformat(period_end)

    periods = []

    for contract in data:
        start = contract[0]
        end = contract[1]

        # Ustaw poczatek i koniec
        # Uzywamy funkcji min i max aby "zacisnac" wartosci miedzy przedzialami czasowymi
        start = datetime.fromisoformat(start)
        start_tz = max(period_start_dt, start)

        if end == "-":
            end = period_end

        end = datetime.fromisoformat(end)
        end_tz = min(period_end_dt, end)

        if start_tz < end_tz:
            periods.append([start_tz, end_tz])

    results = []
    time = period_start_dt

    for period in periods:
        if time < period[0]:
            results.append([
                time.astimezone(pytz.timezone("Europe/Warsaw")).replace(day=1).isoformat(),
                period[0].astimezone(pytz.timezone("Europe/Warsaw")).replace(day=1).isoformat()
            ])

        results.append([
            period[0].astimezone(pytz.timezone("Europe/Warsaw")).replace(day=1).isoformat(),
            period[1].astimezone(pytz.timezone("Europe/Warsaw")).replace(day=1).isoformat()
        ])

        time = period[1]

    if time < period_end_dt:
        results.append([
            time.astimezone(pytz.timezone("Europe/Warsaw")).replace(day=1).isoformat(),
            period_end_dt.astimezone(pytz.timezone("Europe/Warsaw")).replace(day=1).isoformat(),
        ])

    for result in results:
        start = datetime.fromisoformat(result[0])
        end = datetime.fromisoformat(result[1])

        if start == end:
            end = (end + relativedelta(months=1)).replace(tzinfo=start.tzinfo)
            result[1] = end.isoformat()

    # Usuwanie duplikatow za pomoca krotki i zbioru
    results = list(set(tuple(result) for result in results))
    results.sort(key=lambda dat: datetime.fromisoformat(dat[0]))

    for result in results:
        print(f"{result[0]} - {result[1]}")


if __name__ == '__main__':

    period_start = "2022-08-16T00:00:00+02:00"
    period_end = "2023-05-30T00:00:00+02:00"

    data = [
        ["2023-04-20T01:00:00+03:00", "2023-05-06T04:30:00+06:30"],
        ["2022-05-23T15:00:00-07:00", "2022-07-11T19:00:00-03:00"],
        ["2022-09-12T18:00:00-04:00", "2022-09-19T18:00:00-04:00"],
        ["2023-05-06T04:30:00+06:30", "-"],
        ["2022-09-29T18:00:00-04:00", "2023-04-20T01:00:00+03:00"],
        ["2022-08-11T00:00:00+02:00", "2022-08-30T05:00:00+07:00"]
    ]
    """
    period_start="2023-01-01T00:00:00+01:00"
    period_end ="2023-05-01T00:00:00+02:00"

    data = [
        ["2023-01-01T00:00:00+01:00", "2023-02-01T00:00:00+01:00"],
        ["2023-02-01T00:00:00+01:00", "2023-04-01T00:00:00+02:00"],
        ["2023-04-01T00:00:00+02:00", "2023-05-01T00:00:00+02:00"]
    ]
    """
    # Posortuj wedlug daty
    data = sorted(data, key=lambda dat: dat[0])

    generate(period_start, period_end, data)
