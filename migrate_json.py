#!/usr/bin/env python

import json

cache = dict()

def replace_fks(item, fk_name, cache_name=None, nullable=False):
    if cache_name is None:
        cache_name = fk_name

    _id = item["fields"][fk_name]
    if not nullable or _id is not None:
        item["fields"][fk_name] = cache[cache_name][_id]
    return item

def replace_pks(item, pk_name):
    pk = item["fields"]["id"]
    del(item["fields"]["id"])
    item["fields"][pk_name] = item["pk"]
    item["pk"] = pk
    return item
    
def main():
    global cache
    new_list = list()
    
    with open("db.json") as json_data:
        data_list = json.load(json_data)

    name_models = [ "department",
                    "program",
                    "workcell"  ]

    for d in data_list:
        model = d["model"].split(".")[1]
        if model not in cache:
            cache[model] = dict()
        if "id" in d["fields"]:
            try:
                cache[model][d["pk"]] = d["fields"]["id"]
            except KeyError:
                print(d)
        
        if model in name_models:
            d = replace_pks(d, "name")
        elif model == "part":
            d = replace_fks(d, "program")
            d = replace_fks(d, "workcell")
            d = replace_pks(d, "part_number")
        elif model == "downtimecode":
            d = replace_pks(d, "code")

        elif model == "productionschedule":
            d = replace_fks(d, "workcell")
            d = replace_fks(d, "part")
        elif model == "startofshift":
            d = replace_fks(d, "workcell")
        elif model == "endofshift":
            d = replace_fks(d, "workcell")
        elif model == "scrapreport":
            d = replace_fks(d, "workcell")
            d = replace_fks(d, "part")
        elif model == "laborreport":
            d = replace_fks(d, "workcell")
        elif model == "downtime":
            d = replace_fks(d, "workcell")
            d = replace_fks(d, "code", cache_name="downtimecode")
        elif model == "processactivityreport":
            d = replace_fks(d, "workcell")
            d = replace_fks(d, "part", nullable=True)
            
        new_list.append(d)

    with open('new_db.json', 'wt') as out:
        res = json.dump(new_list,
                        out,
                        sort_keys=True,
                        indent=4,
                        separators=(',', ': '))


if __name__ == "__main__":
    main()








