import vk
import csv
import pandas as pd
from time import sleep
from datetime import datetime


def interests(id_members):
    '''
    Временно не используются почему-то
    '''
    result = []
    info = vk_api.users.get(user_ids=",".join(map(str, id_members)), fields="interests")
    for i in range(len(info)):
        if ['intetests'] in info[i]:
            result.append(info[i]['interests'])
    return result


def activities(id_members):
    '''
    Времено не используются почему-то
    '''
    result = []
    info = vk_api.users.get(user_ids=",".join(map(str, id_members)), fields="activities")
    for i in range(len(info)):
        if ['activities'] in info[i]:
            result.append(info[i]['activities'])
    return result


def groups(id_members):
    '''
    Работает вроде
    '''
    info = {}
    types = []
    for member in id_members:
        if member['is_closed'] or 'deactivated' in member: continue
        id = member['id']

        try:
            info_of_groups = vk_api.groups.get(user_id=str(id),extended=1,fields='activity')['items'][:500]
        except vk.exceptions.VkAPIError:
            sleep(0.5)
            info_of_groups = vk_api.groups.get(user_id=str(id),extended=1,fields='activity')['items'][:500]

        activity_of_member = {}
        for group in info_of_groups:
            if 'activity' not in group or 'Этот' in group['activity'] or group['activity'][0].isnumeric(): continue
            types.append(group['activity'])

            if group['activity'] not in activity_of_member:
                activity_of_member[group['activity']] = 1
                continue

            activity_of_member[group['activity']] += 1

        # Возможно можно не делать id как str
        info[id]=activity_of_member
    return info, list(set(types))


def users(id_members):
    '''
    Вроде тоже верно
    '''
    sex = {}
    bdate = {}
    personal = {}
    info = vk_api.users.get(user_ids=id_members, fields="sex, bdate, personal")
    for i,member_info in enumerate(info):

        if 'sex' in member_info:
             sex[id_members[i]]=member_info['sex'] #1 - ж 2 - м 0 - н
        else:
            sex[id_members[i]]="0"

        if 'bdate' in member_info:
            bdate[id_members[i]]=member_info['bdate'] #D.M.YYYY or D.M(secret)
        else:
            bdate[id_members[i]]="0"

        if 'personal' in member_info:
            personal[id_members[i]]=member_info['personal']
        else:
            personal[id_members[i]]="0"

    return sex, bdate, personal


def parsing(token, group_id):

    # Создаём ссесию для работы с ВК АПИ
    global vk_api
    vk_api = vk.session.API(access_token=token, v='5.199')


    # Получаем интересы участников группы
    start_time = datetime.now()
    members = vk_api.groups.getMembers(group_id=group_id, fields='status')
    groups_counts, groups_types = groups(members['items'])
    print("Groups done for: ", datetime.now()-start_time)

    # Получаем общую информацию по участникам группы
    start_time = datetime.now()
    id_members = vk_api.groups.getMembers(group_id=group_id)['items']
    users_sex, users_bdate, users_personal = users(id_members)
    print("Users done for: ", datetime.now()-start_time)

    start_time = datetime.now()
    csv_table_personal = ["political", "religion", "inspired_by", "people_main", "life_main", "smoking", "alcohol"]
    csv_table = ["id", "sex", "bdate", "political", "religion", "inspired_by", "people_main", "life_main", "smoking", "alcohol"] + groups_types

    with open("content.csv", mode="w", encoding="utf-8") as w_file:
        file_write = csv.writer(w_file, delimiter = ",")
        file_write.writerow(csv_table)
        for id in id_members:
            csv_result = []
            csv_result.append(id)
            csv_result.append(users_sex[id])
            csv_result.append(users_bdate[id])

            for i,persona in enumerate(csv_table_personal):
                if csv_table[i+3] not in users_personal[id]:
                    csv_result.append(0)
                    continue
                csv_result.append(users_personal[id][persona])

            for i,type_ in enumerate(csv_table[10:]):
                if id not in  groups_counts or type_ not in groups_counts[id]:
                    csv_result.append(0)
                    continue
                csv_result.append(groups_counts[id][type_])

            file_write.writerow(csv_result)
    
    print("CSV done for: ",datetime.now()-start_time)


if __name__ == "__main__":
    parsing(token="vk1.a.pg91yFJ9SEV4fRy1PIPgVSoHxFXPnRaIgUuKRrUtjmU8RjoiB1tUyrHRbGv3QRuLq3B6zn5hIZkwI_k5SpZPlqEHTLeZZUsTGL0OdWa0QJq_P3kGR_IMwcGBl1XlF5ugvQyBHymUKP6cbOYtiW5UKvyT2LJ0HOmQC0pSBeBizvp4hke81B80ggSSJZiRdpO61mVFxabhMuofaYChu9kJkg",
    group_id="warningbuffet")