import vk
import csv
from time import sleep
from datetime import datetime


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
    '''
    Работает вроде
    '''
    info = {}
    types = []
    for member in id_members:
        if member['is_closed'] or 'deactivated' in member: continue
        id = member['id']
        groups = vk_api.groups.get(user_id=str(id))['items'][:500]

        info_of_groups = vk_api.groups.getById(group_ids=groups, fields='activity')

        activity_of_member = {}
        for group in info_of_groups['groups']:
            if 'activity' not in group: continue
            types.append(group['activity'])

            if group['activity'] not in activity_of_member:
                activity_of_member[group['activity']] = 1
                continue

            activity_of_member[group['activity']] += 1

        # Возможно можно не делать id как str
        info[str(id)]=activity_of_member
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

    # Создаём ссесию для работы с ВК АПИ
    global vk_api
    vk_api = vk.session.API(access_token=token, v='5.199')


    # Список учатников группы
    members = vk_api.groups.getMembers(group_id=group_id, fields='status')
    # Айди участников группы
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
                if csv_table[i+3] not in users_personal[str(id_members[j])]:
                    csv_result.append(0)
                    continue

                csv_result.append(users_personal[str(id_members[j])][csv_table_personal[i]])

            for i in range(len(csv_table)-10):
                if str(id_members[j]) not in  groups_counts or csv_table[i+10] not in groups_counts[str(id_members[j])]:
                    csv_result.append(0)
                    continue

                csv_result.append(groups_counts[str(id_members[j])][csv_table[i+10]])

            file_write.writerow(csv_result)


if __name__ == "__main__":
    parsing(token="vk1.a.aF7jMwGP58s_y6kdrHZRFKyHBvvVUQ5N-BoS8rfLErNOzSVmzo-e2erLBCSBE1KOJndxmGSH_6zmqicottD3etowGKBZWOza1eml49MKifoeiZEQ-6sZhE9qNxH-ywBTgXfJYf9_QBbnReyg",
    group_id="warningbuffet")