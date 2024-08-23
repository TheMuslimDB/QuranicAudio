import requests
import os
import json


with open("data-from-site.json","r") as f:
    data =  json.load(f)


def get_or(dic,key,default):
    if key in dic:
        if dic[key] != None:
            return dic[key] 
    return default

for key in  data["qaris"]["entities"].keys():
    info = data["qaris"]["entities"][key]
    fn = f"output/{info['name'].replace(' ','_')}.json"
    if os.path.exists(fn):
        continue

    
    # data from 82 and up is random reading from random websites
    if int(key) > 82:
        break


    print(key, info["name"])

    download_suffix =  info["relativePath"]

    res =  requests.get(f"https://quranicaudio.com/api/qaris/{info['id']}/audio_files/mp3")

    surahs_json = res.json()
    surahs = []

    for surah in surahs_json:
        file_name =  get_or(surah,"file_name")
        size = get_or(surah,"format",{}).get("size",-1)
        bitrate = get_or(surah,"format",{}).get("bit_rate",-1)
        duration = get_or(surah,"format",{}).get("duration",-1)
        title = get_or(surah,"metadata",{}).get("title",file_name)
        surahs.append({
            "file_name" : file_name,
            "size" : size,
            "bitrate" : bitrate,
            "duration" : duration,
            "title" : title,
            "link": f"https://download.quranicaudio.com/quran/{info['relativePath']}{file_name}"
        })

    reader_info  = {
        "id" : info["id"],
        "name" : info["name"],
        "arabicName" : info["arabicName"],
        "surahs": surahs,
    }
    
    with open(fn,"w") as f:
        json.dump(reader_info,f)

