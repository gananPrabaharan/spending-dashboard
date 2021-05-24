import csv

import pandas as pd

from GeoExtraction.geoextraction import GeoExtraction
from simplifications import sim1, sim2, sim3, sim4, sim5, sim6
from extractions import ext1, ext2, ext3, ext4
from difflib import SequenceMatcher


def similar(a, b):
    """
    function to check similarity between two strings
    :param a: (string) text
    :param b: (string) text
    :return: similarity score
    """
    # compares similarity of a and b based on Gestalt pattern matching algorithm
    return SequenceMatcher(None, a, b).ratio()


def pend1(memos_list):
    """
    Extract location terms
    :param memos_list:
    :return:
    """
    new_memos, location_dict = list(), dict()
    G = GeoExtraction()
    for m in memos_list:
        new_memos.append(m)
        new_m = G.remove_location(m)
        location_dict[new_m] = G.extract_location(m)

    return new_memos, location_dict


def fix(original_list, list_to_fix):
    """
    Simplify the patterns

    :param original_list:
    :param list_to_fix:
    :return:
    """
    assert len(original_list) == len(list_to_fix)
    for x in range(len(original_list)):
        if len(list_to_fix[x]) == 0:
            list_to_fix[x] = original_list[x]
    return list_to_fix


def fix_list(memos_list, ori):
    fix(memos_list, sim6(ori))
    fix(memos_list, sim5(ori))
    fix(memos_list, sim4(ori))
    fix(memos_list, sim3(ori))
    fix(memos_list, sim2(ori))
    simp_list = fix(memos_list, sim1(ori))
    return simp_list


def extract(simp_list, ext1_list, ext2_list, ext3_list, ext4_list):
    """
    Extraction of vendor name
    """
    final_list = []
    priority_list = [ext1_list, ext4_list, ext2_list, ext3_list, simp_list]
    for x in range(len(ext1_list)):
        # Extracting while prioritizing highest precision patterns first
        for inner_list in priority_list:
            if len(inner_list[x]) > 2:
                final_list.append(inner_list[x])
            else:
                # If no patterns matched, add empty string
                final_list.append('')

    return final_list


def flow(memos_list, output_file):
    # creating output lists for each pattern
    ori = [x for x in memos_list]

    simp_list = fix_list(memos_list, ori)

    sim1_list = sim1(memos_list)
    sim2_list = sim2(memos_list)
    sim3_list = sim3(memos_list)
    sim4_list = sim4(memos_list)
    sim5_list = sim5(memos_list)
    sim6_list = sim6(memos_list)
    ext1_list = ext1(memos_list)
    ext2_list = ext2(simp_list)
    ext3_list = ext3(simp_list)
    ext4_list = ext4(simp_list)
    final_output = extract(simp_list, ext1_list, ext2_list, ext3_list, ext4_list)

    # tracking changes created by the pattern functions
    geo = GeoExtraction()
    cleaned_output = []
    for entry in final_output:
        cleaned_entry = geo.remove_location(entry)
        cleaned_output.append(cleaned_entry)

    with open(output_file, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        title_row = ["memo", "sim1", "sim2", "sim3", "sim4", "sim5", "sim6", "ext1", "ext2", "ext3", "ext4", "output"]
        writer.writerow(title_row)
        for x in range(len(ori)):   # Write the change each pattern has on the memos
            writer.writerow([ori[x],sim1_list[x],sim2_list[x],sim3_list[x],sim4_list[x],sim5_list[x],sim6_list[x],simp_list[x],ext1_list[x],ext2_list[x],ext3_list[x],ext4_list[x],cleaned_output[x]])

    return final_output


if __name__ == "__main__":
    sample_file = "/Users/Ganan/PycharmProjects/spending-dashboard/flask_app/resources/bank_transations.csv"
    df = pd.read_csv(sample_file)
    flow(list(df["Memo"].values), 'tracking_bank.csv')
