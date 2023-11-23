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


def clean_types(types: list[str]) -> list[str]:
    '''
    Чисти типы группы
    '''
    types = list(set(types))
    new_types = []
    for type in types:
        if 'Этот материал заблокирован' not in type or type[0].isnumeric():
            continue
        new_types.append(type)
    return new_types


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
            groups = vk_api.groups.get(user_id=str(id))['items'][:500]
            info_of_groups = vk_api.groups.getById(group_ids=groups, fields='activity')
        except vk.exceptions.VkAPIError:
            sleep(0.5)
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
        info[id]=activity_of_member
    return info, clean_types(types)


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
             sex[str(id_members[i])]=member_info['sex'] #1 - ж 2 - м 0 - н
        else:
            sex[str(id_members[i])]="0"

        if 'bdate' in member_info:
            bdate[str(id_members[i])]=member_info['bdate'] #D.M.YYYY or D.M(secret)
        else:
            bdate[str(id_members[i])]="0"

        if 'personal' in member_info:
            personal[str(id_members[i])]=member_info['personal']
        else:
            personal[str(id_members[i])]="0"

    return sex, bdate, personal


def parsing(token, group_id):

    # Создаём ссесию для работы с ВК АПИ
    global vk_api
    vk_api = vk.session.API(access_token=token, v='5.199')


    # Получаем интересы участников группы
    members = vk_api.groups.getMembers(group_id=group_id, fields='status')
    groups_counts, groups_types = groups(members['items'])

    # Получаем общую информацию по участникам группы
    id_members = vk_api.groups.getMembers(group_id=group_id)['items']
    users_sex, users_bdate, users_personal = users(id_members)

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
    parsing(token="vk1.a.NC8Ti_ySNNUDCbi3TyhB8ooRNZ73PrXCbOZJYfQgcajrZ9I8iIVrFX-fpZfqOaxyTm7zigtQuFDWnEPpjWeFLaX2PgWS2kqx3kcWPm4z1Neq5Ga0wr2XovmTf2JG1-kgrefzv93bqfFfod9yDqN5JawOtD0yGoPqt1rciWNn0fEsbgPrNv3CraGvs2eUBC4Px6Uqhrj5g_aDlOfk9xAGiQ",
    group_id="warningbuffet")