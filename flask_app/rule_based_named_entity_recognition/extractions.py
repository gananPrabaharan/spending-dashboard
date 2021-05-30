import re


def ext1(memos_list):
    """
    Anything in quotation marks = name
    :param memos_list:
    :return:
    """
    match_list = []
    for x in range(len(memos_list)):
        matches = re.findall(r'\"(.+?)\"',memos_list[x]) # take everything between quotes
        if matches != [] and len(matches) == 1: # if the pattern exists
            match_list.append(matches[0]) # add what is between quotation marks to output list
        else:
            match_list.append('') # add Null to output list
    return match_list   # return output list


def ext2(data_list):
    """
    Repeated words = name

    :param data_list:
    :return:
    """
    rep_list = []
    for data in data_list:
        name = ''
        words = data.split()
        word_set = set()
        for word in words:
            if word in word_set:
                name += word + ' '
            else:
                word_set.add(word)

        rep_list.append(name)
    return rep_list


def ext3(memos_list):
    """
    Memo length <=3 >> whole memo = name
    :param memos_list:
    :return:
    """
    name_list = []
    num_location = "[^\s]*\d\d\d[^\s]*|\sCA\s"  # numbers or "CA" california
    for i, m in enumerate(memos_list):
        tmp = m.split()
        if len(tmp) <= 3:
            tmp_s = re.sub(num_location, "", m)
            name_list.append(tmp_s.lstrip().rstrip())
        else:
            name_list.append('')
    return name_list


def ext4(memos_list):
    """
    Word before company suffixes = name
    :param memos_list:
    :return:
    """
    keywords = "(?i)\sinc.\s|(?i)\sLLC\s|(?i)\sCO\s|(?i)\sLimited\s|(?i)\sINC\s|(?i)\sCorporation\s|(?i)\s.com\s|(?i)\s.net\s"
    k = keywords.split("|")
    ans = list()
    new_memos = list()
    for m in memos_list:
        tmp = re.split(keywords, m)
        if len(tmp) > 1:
            ans.append(tmp[0])
        else:
            new_memos.append(m)
            ans.append('')
    return ans
