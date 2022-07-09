import vk
import csv
from time import sleep

def interests(id_members):
    result = []
    info = vk_api.users.get(user_ids=",".join(map(str, id_members)), fields="interests")
    for i in range(len(info)):
        if ['intetests'] in info[i]:
            result.append(info[i]['interests'])
    return result

def activities(id_members):
    result = []
    info = vk_api.users.get(user_ids=",".join(map(str, id_members)), fields="activities")
    for i in range(len(info)):
        if ['activities'] in info[i]:
            result.append(info[i]['activities'])
    return result

def groups(id_members):
    info = {}
    errors = []
    types = []
    for i in range(len(id_members)):
        try:
            groups = vk_api.groups.get(user_id=str(id_members[i]))['items']
            groups_of_member = list(map(str, groups))
            info_of_groups = vk_api.groups.getById(group_ids=','.join(groups_of_member), fields='activity')
            info_activity = []
            info_of_activity = {}
            for j in range(len(info_of_groups)):
                if 'activity' in info_of_groups[j]:
                    info_activity.append(info_of_groups[j]['activity'])
                    types.append(info_of_groups[j]['activity'])
            for j in range(len(list(set(info_activity)))):
                info_of_activity[list(set(info_activity))[j]] = info_activity.count(list(set(info_activity))[j])
            info[str(id_members[i])]=info_of_activity
            sleep(1)
        except Exception as e:
            errors.append(e)
    print(errors)
    return info, list(set(types))

def users(id_members):
    sex = {}
    bdate = {}
    personal = {}
    info = vk_api.users.get(user_ids=",".join(map(str, id_members)), fields="sex, bdate, personal")
    for i in range(len(info)):
        if 'sex' in info[i]:
             sex[str(id_members[i])]=info[i]['sex'] #1 - ж 2 - м 0 - н
        else:
            sex[str(id_members[i])]="0"
        if 'bdate' in info[i]:
            bdate[str(id_members[i])]=info[i]['bdate'] #D.M.YYYY or D.M(secret)
        else:
            bdate[str(id_members[i])]="0"
        if 'personal' in info[i]:
            personal[str(id_members[i])]=info[i]['personal']
        else:
            personal[str(id_members[i])]="0"
    return sex, bdate, personal

def parsing(token, group_id):
    token = token
    global session
    session = vk.Session(access_token=token)
    global vk_api
    vk_api = vk.API(session, v="5.131")

    members = vk_api.groups.getMembers(group_id=group_id)
    id_members = members['items']
    groups_info = groups(id_members)
    groups_counts, groups_types = groups_info[0], groups_info[1]
    users_info = users(id_members)
    users_sex, users_bdate, users_personal = users_info[0], users_info[1], users_info[2]
    csv_table_personal = ["political", "religion", "inspired_by", "people_main", "life_main", "smoking", "alcohol"]
    csv_table = ["id", "sex", "bdate", "political", "religion", "inspired_by", "people_main", "life_main", "smoking", "alcohol"] + list(map(str, groups_types))

    with open("content.csv", mode="w", encoding="utf-8") as w_file:
        file_write = csv.writer(w_file, delimiter = ",")
        file_write.writerow(csv_table)
        for j in range(len(id_members)):
            csv_result = []
            csv_result.append(id_members[j])
            csv_result.append(users_sex[str(id_members[j])])
            csv_result.append(users_bdate[str(id_members[j])])
            for i in range(len(csv_table_personal)):
                if csv_table[i+3] in users_personal[str(id_members[j])]:
                    csv_result.append(users_personal[str(id_members[j])][csv_table_personal[i]])
                else:
                    csv_result.append(0)
            for i in range(len(csv_table)-10):
                if str(id_members[j]) in  groups_counts:
                    if csv_table[i+10] in groups_counts[str(id_members[j])]:
                        csv_result.append(groups_counts[str(id_members[j])][csv_table[i+10]])
                    else:
                        csv_result.append(0)
                else:
                    csv_result.append(0)
            file_write.writerow(csv_result)