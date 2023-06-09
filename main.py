import csv

from monash import Monash
from unimelb import Unimelb
from ranking_query import ask_arwu


def main():
    university = Monash()
    exchange_partner_list = university.get_exchange_info()
    # Start querying for ranking, using ARWU ranking here
    for partner in exchange_partner_list:
        info_dict = ask_arwu(partner.name)
        if info_dict:  # if the partner is found
            if info_dict["ranking"]:
                # for some reason, there are empty ranking (i.e. ranking="")
                partner.rank = info_dict["ranking"]
            partner.location = info_dict["region"]
    # sort it based on rankings, split to take care of 101-200th styled rankings
    exchange_partner_list.sort(key=lambda x: int(x.rank.split("-")[0]))
    # Writing to file
    write_to_csv(exchange_partner_list, "data_monash.csv")


def write_to_csv(university_list, file_name):
    with open(file_name, "wt", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",")
        # headers
        writer.writerow(["Name", "Rank", "Link", "Location", "Faculty"])
        # write attributes
        for i in range(len(university_list)):
            # print(list(uni_list[i].__dict__.values()))
            writer.writerow(list(university_list[i].__dict__.values()))
        f.close()


if __name__ == "__main__":
    main()
