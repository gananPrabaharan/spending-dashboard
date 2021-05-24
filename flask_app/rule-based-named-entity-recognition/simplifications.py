import re


def sim1(memos_list):
    """
    Remove financial shorthand
    :param memos_list
    """
    changed_list = []
    for i, mem in enumerate(memos_list):
        if len(mem.split()) <= 3:
            # memos less than or equal to three words are left alone
            changed_list.append('')
        else:
            shorthands = "(?i)debit card|credit card|debit|credit|card|crd|ref|cashier check purchase|paypal| NY | New York | Las Vegas | NV | San Francisco | SF | San Francis |San Mateo | San Jose | Port Melbourn | CA | JAMAICA | Sydney | NS | Log Angeles | AU | Surry Hills | Singapore | SG "
            mem = re.sub(' +',' ',re.sub(shorthands, '', mem)) #remove abbreviations listed in shorthands
            changed_list.append(mem) # append simplified memo to output list
    return changed_list


def sim2(memos_list):
    """
    Remove mixed alphanumerics
    :param memos_list:
    :return:
    """
    num = "[^s]*\d\d\d\d\d+[^s]*"  # more than 5 numbers
    alt_alphanum = "(?i)[^s][a-z]+\d+\w*[^s]"  # alternating numbers and alphabets (alphabets come first)
    alt_alphanum_2 = "(?i)[^s]\d+[a-z]+\w*[^s]"  # alternating numbers and alphabets (numbers come first)
    L = list()
    for m in memos_list:
        # remove the string of numbers and alphanumeric strings from all the memos
        tmp = re.split(num + "|" + alt_alphanum + "|" + alt_alphanum_2, m) # split the string using the the string of numbers, the alphanumeric strings as separators
        tmp = [x.lstrip().rstrip() for x in tmp]
        tmp = ' '.join(tmp).lstrip().rstrip()

        if tmp:
            L.append(tmp)
        else:   # if the memo string is entirely made up of alphanumeric strings or strings of numbers, add the entire memo back to the list.
            L.append('')
    return L


def sim3(memos_list):
    """
    Remove the date from the string (assume format of date - "MM/DD")
    :param memos_list:
    :return:
    """
    date = "[^\s]*\d\d/\d\d[^\s]*"  # date
    ref = "(?i)[^\s]*ref[\d^\s]*"  # reference number in format "REF...""
    crd = "(?i)[^\s]*crd[\d^\s]*"  # credit number in format "CRD..."
    new_list = []
    for i, memo in enumerate(memos_list):
        # remove the dates, reference numbers and credit numbers from the memo string
        # remove the dates
        tmp = re.split(date, memo)
        tmp = [x.lstrip().rstrip() for x in tmp]
        tmp = ' '.join(tmp).lstrip().rstrip()

        # remove the reference numbers
        tmp = re.split(ref, tmp)
        tmp = [x.lstrip().rstrip() for x in tmp]
        tmp = ' '.join(tmp).lstrip().rstrip()

        # remove the credit numbers
        tmp = re.split(crd, tmp)
        tmp = [x.lstrip().rstrip() for x in tmp]
        tmp = ' '.join(tmp).lstrip().rstrip()
        if tmp == memo:
            new_list.append('')
        else:
            new_list.append(tmp)
    return new_list


def sim4(memos_list):
    """
    Ignore online/bank transfers
    :param memos_list:
    :return:
    """
    changed_list = []
    for x in range(len(memos_list)):
        # if memo string contains "internet transfer" or "online transfer", remove the memo string from the list.
        if 'internet transfer' in memos_list[x].lower():
            changed_list.append('')
        elif 'online transfer' in memos_list[x].lower():
            changed_list.append('')
        else: # the memo string does not contain the word "internet transfer" or "online transfer"
            changed_list.append(memos_list[x])

    return changed_list


def sim5(memos_list):
    """
    Remove the last instance of * and anything before it

    :param memos_list:
    :return:
    """
    sim_list = []
    for x in range(len(memos_list)):
        if '*' in memos_list[x]: # check if * exists
            sim_list.append(memos_list[x][memos_list[x].rfind('*')+1:]) # remove everything before and including the *
        else:
            sim_list.append('')
    return sim_list


def sim6(memos_list):
    """
    Remove punctuation

    :param memos_list:
    :return:
    """
    sim_list = []
    a = ['"', ',', '.']
    for x in range(len(memos_list)):
        # if any of the listed punctuation is present, delete it
        temp = ''
        if any(i in memos_list[x] for i in a):
            temp = memos_list[x].replace('"', "")
            temp = temp.replace(',', "")
        sim_list.append(temp)
    return sim_list
