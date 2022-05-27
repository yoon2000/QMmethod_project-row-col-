import math
import copy

def solution(minterm):
    answer = []

    v_num = minterm[0]
    min_num = minterm[1]
    bin_minterms = [[] for i in range(v_num + 1)]
    combined_check = []
    implement = []

    #2진수로 변환시키기
    for i in range(2, 2 + min_num):
        bin_min = bin(minterm[i])[2:]
        while (len(bin_min) < v_num):
            bin_min = '0' + bin_min
        bin_minterms[bin_min.count('1')].append(bin_min)

    implement.append(bin_minterms)
    bin_uppairs, check = combined(bin_minterms)
    combined_check.append(check)
    implement.append(bin_uppairs)

    while (True):
        bin_uppairs, check = combined(bin_uppairs)
        if (len(check) == 0):
            break
        combined_check.append(check)
        implement.append(bin_uppairs)

    # print(implement)
    # print(combined_check)

    #리스트 1차원으로 쓸수있게 변환
    combined_check_1D = sum(combined_check, [])
    implement_2D = sum(implement, [])
    implement_1D = sum(implement_2D, [])

    # print(implement_1D)
    # print(combined_check_1D)

    #answer에 pi넣고 정렬하기
    for i in implement_1D:
        if i not in combined_check_1D:
            answer.append(i)
    for i in range(len(answer)):
        answer[i] = answer[i].replace('-', '2')
    answer.sort()
    for i in range(len(answer)):
        answer[i] = answer[i].replace('2', '-')

    unselect_pi_cover_min = [[] for i in range(int(math.pow(2, v_num)))]

    pi_len = len(answer)
    #각 minterm 별로 포함하는 pi개수 세기
    for i in range(pi_len):
        _num = answer[i].count('-')
        for j in range(int(math.pow(2, _num))):
            cp_answer = answer[i]
            bin_min = bin(j)[2:]
            while (len(bin_min) < _num):
                bin_min = '0' + bin_min
            for k in range(_num):
                idx = cp_answer.find('-')
                cp_answer = cp_answer[:idx] + bin_min[k] + cp_answer[idx + 1:]
            unselect_pi_cover_min[int(cp_answer,2)].append(answer[i])

    # print("pi_cover_min =  ", pi_cover_min)

    select_pi = []
    unselect_pi = answer[0:]

    print("unselect_pi_cover_min = ", unselect_pi_cover_min)

    #epi 찾아서 넣기 epi, answer list에 append함
    answer.append("EPI")
    for i in range(pi_len):
        if(check_epi(answer[i], unselect_pi_cover_min)):
            #epi는 무조건 사용하는 pi 이기때문에 바로 select_pi 리스트에 넣어주기
            select_pi.append(answer[i])
            answer.append(answer[i])

    #pi list에서 epi 지우기
    for i in select_pi:
        if i in unselect_pi:
            unselect_pi.remove(i)

    print("unselect_pi = ",unselect_pi)
    print("select_pi = ", select_pi)

    for i in select_pi:
        unselect_pi_cover_min = except_pi_minterm(i,unselect_pi_cover_min)

    print("unselect_pi_cover_min = ", unselect_pi_cover_min)

    #row_dominance 당해서 안쓰는 pi들 넣는 리스트
    do_not_using_pi = []

    #while문으로 row column dominance 계속 하기
    while(True):
        column_dominated_minterm, unselect_pi_cover_min = column_dominance(unselect_pi_cover_min)
        print("unselec_pi_cover_min = ", unselect_pi_cover_min)
        row_dominated_pi, unselect_pi_cover_min = row_dominance(unselect_pi, unselect_pi_cover_min)
        for i in range(len(row_dominated_pi)):
            if (i % 2):
                for j in range(len(row_dominated_pi[i])):
                    do_not_using_pi.append(row_dominated_pi[i][j])

        for i in do_not_using_pi:
            if i in unselect_pi:
                unselect_pi.remove(i)

        for i in unselect_pi:
            if (check_epi(i, unselect_pi_cover_min)):
                select_pi.append(i)
                except_pi_minterm(i, unselect_pi_cover_min)

        for i in select_pi:
            if i in unselect_pi:
                unselect_pi.remove(i)

        print("---------------after row col dominance--------------------")
        print("unselect_pi = ", unselect_pi)
        print("select_pi = ", select_pi)
        print("do_not_using_pi = ", do_not_using_pi)
        print("unselect_pi_cover_min = ", unselect_pi_cover_min)

        #second epi를 구하는 도중 모든 minterm들을 다 포함할 때 바로 break 하기
        cnt = 0
        for i in unselect_pi_cover_min:
            cnt += len(i)
        if(cnt == 0):
            print("all minterm cover")
            break

        if(len(column_dominated_minterm) < 1 and len(row_dominated_pi) < 1):
            break
    print("--------------------------------------------------------------")
    print("unselect_pi = ", unselect_pi)
    print("select_pi = ", select_pi)
    print("do_not_using_pi = ", do_not_using_pi)
    print("unselect_pi_cover_min = ", unselect_pi_cover_min)

    return answer

def column_dominance(unselect_pi_cover_min):
    print("----------------column dominance------------------")
    column_dominated_minterm = []
    for i in range(len(unselect_pi_cover_min)):
        dominate_min = i
        dominated_min = []
        if len(unselect_pi_cover_min[i]) == 0: continue
        for j in range(len(unselect_pi_cover_min)):
            if len(unselect_pi_cover_min[j]) == 0: continue
            #자기자신을 확인할때 무시하기위해서
            if(i==j): continue
            #다른애들이랑 비교할 때
            check = True
            for k in range(len(unselect_pi_cover_min[i])):
                if unselect_pi_cover_min[i][k] not in unselect_pi_cover_min[j]:
                    check = False
            if(check and (len(unselect_pi_cover_min[i]) <= len(unselect_pi_cover_min[j]))):
                dominated_min.append(j)
        if(len(dominated_min)):
            column_dominated_minterm.append(dominate_min)
            column_dominated_minterm.append(dominated_min)
    for i in range(len(column_dominated_minterm)):
        if(i%2):
            for j in range(len(column_dominated_minterm[i])):
                unselect_pi_cover_min[column_dominated_minterm[i][j]].clear()

    print("column_dominated_minterm = ", column_dominated_minterm)
    return column_dominated_minterm, unselect_pi_cover_min

def row_dominance(unselect_pi, unselect_pi_cover_min):
    print("---------------row_dominance-------------------")
    pi_cover_min = [[] for i in range(len(unselect_pi))]
    dominated_pi = copy.deepcopy(pi_cover_min)
    pi_idx = unselect_pi
    for i in range(len(unselect_pi_cover_min)):
        #잠깐 don't care 예시 볼려고 넣은 조건문 실제 실행시 지워야함
        # if(i == 13 or i == 15): continue
        for j in range(len(unselect_pi_cover_min[i])):
            if unselect_pi_cover_min[i][j] in pi_idx:
                pi_cover_min[pi_idx.index(unselect_pi_cover_min[i][j])].append(i)

    for i in range(len(pi_cover_min)):
        if(len(pi_cover_min[i]) == 0): continue
        for j in range(len(pi_cover_min)):
            if(j == i or len(pi_cover_min[j]) == 0): continue
            check = True
            for k in pi_cover_min[j]:
                if k not in pi_cover_min[i]:
                    check = False
                    break
            if(check):
                dominated_pi[i].append(pi_idx[j])
                continue

    row_dominace_pi = []

    for i in range(len(dominated_pi)):
        if(len(dominated_pi[i])):
            row_dominace_pi.append(pi_idx[i])
            row_dominace_pi.append(dominated_pi[i])

    #row_dominance_pi 서로가 서로를 지배하는 경우 한가지를 삭제하기
    remove_pi = []
    not_remove_pi = []
    for i in range(len(row_dominace_pi)):
        if((i%2) == 0):
            for j in range(len(row_dominace_pi)):
                if(i == j): continue
                if (j%2) == 0:
                    if (row_dominace_pi[i] in row_dominace_pi[j+1]) and (row_dominace_pi[j] in row_dominace_pi[i+1]):
                        if row_dominace_pi[j] not in not_remove_pi:
                               if row_dominace_pi[j] not in remove_pi:
                                   remove_pi.append(row_dominace_pi[j])
                                   not_remove_pi.append(row_dominace_pi[i])

    print("Each_other_dominance_pi_to_remove = ",remove_pi)
    new_row_dominance_pi = []
    for i in range(len(row_dominace_pi)):
        if (i%2) == 0:
            if row_dominace_pi[i] in remove_pi:
                okay = False
            else:
                new_row_dominance_pi.append(row_dominace_pi[i])
                okay = True
        else:
            if(okay):
                new_row_dominance_pi.append(row_dominace_pi[i])

    print("new row dominance_pi = ", new_row_dominance_pi)
    row_dominace_pi = new_row_dominance_pi


    # row dominace_pi include minterm들을 row dominace pi 하나로 바꾸기
    for i in range(len(row_dominace_pi)):
        if((i % 2) == 0):
            for j in range(len(unselect_pi_cover_min)):
                if len(unselect_pi_cover_min[j]) == 0: continue
                if row_dominace_pi[i] in unselect_pi_cover_min[j]:
                    unselect_pi_cover_min[j].clear()
                    unselect_pi_cover_min[j].append(row_dominace_pi[i])

    print("row_dominance_pi = ", row_dominace_pi)
    print("unselec_pi_cover_min =_", unselect_pi_cover_min)
    return row_dominace_pi, unselect_pi_cover_min

def except_pi_minterm(pi, cnt_pi):
    _num = pi.count('-')
    for j in range(int(math.pow(2, _num))):
        cp_pi = pi
        bin_min = bin(j)[2:]
        while (len(bin_min) < _num):
            bin_min = '0' + bin_min
        for k in range(_num):
            idx = cp_pi.find('-')
            cp_pi = cp_pi[:idx] + bin_min[k] + cp_pi[idx + 1:]
        cnt_pi[int(cp_pi, 2)].clear()
    return cnt_pi

def check_epi(pi, cnt_pi):
    _num = pi.count('-')
    for j in range(int(math.pow(2, _num))):
        cp_pi = pi
        bin_min = bin(j)[2:]
        while (len(bin_min) < _num):
            bin_min = '0' + bin_min
        for k in range(_num):
            idx = cp_pi.find('-')
            cp_pi = cp_pi[:idx] + bin_min[k] + cp_pi[idx + 1:]
        if((len(cnt_pi[int(cp_pi, 2)]) == 1) and pi in cnt_pi[int(cp_pi,2)]):
            return True
    return False


def combined(bin_minterms):
    ret = [[] for i in range(len(bin_minterms))]
    ret2 = []
    bit_len = len(bin_minterms) - 1
    for i in range(len(bin_minterms) - 1):
        for j in range(len(bin_minterms[i])):
            for k in range(len(bin_minterms[i + 1])):
                HD = 0
                for l in range(bit_len):
                    if (bin_minterms[i][j][l] != bin_minterms[i + 1][k][l]):
                        HD += 1
                        HD_idx = l
                if (HD == 1):
                    data = bin_minterms[i][j]
                    data2 = bin_minterms[i + 1][k]
                    if (data not in ret2):
                        ret2.append(data)
                    if (data2 not in ret2):
                        ret2.append(data2)
                    data = data[:HD_idx] + "-" + data[HD_idx + 1:]
                    if (data not in ret[data.count('1')]):
                        ret[data.count('1')].append(data)
    return ret, ret2


if __name__ == '__main__':
    # minterm = [4,8,0,4,8,10,11,12,13,15]
    # minterm = [4,8,1,3,4,5,6,7,9,11]
    # minterm = [4,10,0,1,2,5,6,7,8,9,10,14]
    minterm = [4,13,0,2,3,4,5,6,7,8,9,10,11,12,13]
    # minterm = [4,11,0,2,5,6,7,8,10,12,13,14,15]
    print("answer = ", solution(minterm))
