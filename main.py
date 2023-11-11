from datetime import datetime
from datetime import timedelta
import pytz

if __name__ == '__main__':

    data_list = []
    data_dict = {}
    group = {}

    file = open("data.txt", 'r')

    for line in file:

        data_dict["timestamp"] = line.rsplit(" ", 4)[0]
        data_dict["flour"] = line.replace(" ", "", 1).split(" ")[1]
        data_dict["groat"] = line.replace(" ", "", 1).split(" ")[2]
        data_dict["milk"] = line.replace(" ", "", 1).split(" ")[3]
        data_dict["egg"] = line.replace(" ", "", 1).split(" ")[4].replace("\n", "")

        data_list.append(data_dict)

        data_dict = {}

    for i, entry in enumerate(data_list):
        for value in entry.values():
            timestamp = datetime.fromisoformat(str(value))
            timestamp += timedelta(hours=int(str(value)[-6:-3]))
            date = timestamp.strftime("%Y-%m-%d %H:00:00")
            data_list[i]["timestamp"] = date
            break

    data_list.sort(key=lambda dct: datetime.strptime(dct["timestamp"], "%Y-%m-%d %H:00:00"))

    for i, entry in enumerate(data_list):
        date = entry["timestamp"]
        if date not in group:
            group[date] = {"flour": entry["flour"],
                             "groat": entry["groat"],
                             "milk": entry["milk"],
                             "egg": entry["egg"]}
        else:
            group[date]["flour"] = str(int(entry["flour"]) + int(group[date]["flour"]))
            group[date]["groat"] = str(int(entry["groat"]) + int(group[date]["groat"]))
            group[date]["milk"] = str(int(entry["milk"]) + int(group[date]["milk"]))
            group[date]["egg"] = str(int(entry["egg"]) + int(group[date]["egg"]))

    results = []

    for timestamp, value in group.items():
        final_result = {
            "timestamp": timestamp,
            "flour": round(float(value["flour"]) * 0.01, 2),
            "groat": round(float(value["groat"]) * 0.001, 2),
            "milk": round(float(value["milk"]) * 0.001, 2),
            "egg": int(value["egg"])
        }
        results.append(final_result)

    for i in results:
        print(i)
