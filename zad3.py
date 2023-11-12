from datetime import datetime, timedelta
import pytz


def generate(period_start, period_end, data):

    # Przeksztalc string na datetime
    period_start_dt = datetime.fromisoformat(period_start)
    period_end_dt = datetime.fromisoformat(period_end)

    periods = []

    for contract in data:
        start = contract[0]
        end = contract[1]

        start = datetime.fromisoformat(start)
        start_tz = max(period_start_dt, start)


        if end == "-":
            end = period_end

        end = datetime.fromisoformat(end)
        end_tz = min(period_end_dt, end)

        if start_tz < end_tz:
            periods.append([start_tz, end_tz])

    results = []

    for period in periods:
        results.append([
            period[0].astimezone(pytz.timezone("Europe/Warsaw")).isoformat(),
            period[1].astimezone(pytz.timezone("Europe/Warsaw")).isoformat()
        ])

    print(results)



if __name__ == '__main__':

    period_start = "2023-01-01T00:00:00+01:00"
    period_end = "2023-05-01T00:00:00+02:00"

    """
    data = [
        ["2023-04-20T01:00:00+03:00", "2023-05-06T04:30:00+06:30"],
        ["2022-05-23T15:00:00-07:00", "2022-07-11T19:00:00-03:00"],
        ["2022-09-12T18:00:00-04:00", "2022-09-19T18:00:00-04:00"],
        ["2023-05-06T04:30:00+06:30", "-"],
        ["2022-09-29T18:00:00-04:00", "2023-04-20T01:00:00+03:00"],
        ["2022-08-11T00:00:00+02:00", "2022-08-30T05:00:00+07:00"]
    ]
    """

    data = [
        ["2023-03-31T22:00:00+00:00", "-"],
        ["2022-03-31T17:00:00-05:00", "2022-06-30T18:00:00-04:00"],
        ["2022-06-30T12:00:00-10:00", "2023-01-31T19:30:00-03:30"]
    ]

    # Posortuj wedlug daty
    data = sorted(data, key=lambda dat: dat[0])

    #dt = datetime.fromisoformat("2023-03-31T22:00:00-00:00")
    #dt = dt.astimezone(datetime.fromisoformat(period_start).tzinfo)
    #dt = dt.replace(day=1, hour=0, minute=0, second=0)
    #print(dt)

    generate(period_start, period_end, data)
