import re


def parse_cities(input_file):
    cities_list = []

    with open(input_file, "r", encoding="utf-8") as fin:
        for line in fin:
            for entry in line.split():
                city = entry.strip(",")
                if "(" in city:
                    city = re.split("[()]", city)[:-1]
                    if "область" in city[1]:
                        city[1] = re.split("область", city[1])
                        city = "%s (%s %s)" % (city[0], city[1][0], "область")
                    elif "край" in city[1]:
                        city[1] = re.split("край", city[1])
                        city = "%s (%s %s)" % (city[0], city[1][0], "край")
                    else:
                        if city[1] == "Ханты-МансийскийАО–Югра":
                            city[1] = "Ханты-Мансийский АО"
                        city[1] = "(%s)" % city[1]
                        city = " ".join(city)

                letter = [letter for letter in city[1:] if letter.isupper()]

                if letter and "(" not in city and "-" not in city:
                    new_city = re.split(letter[0], city[1:])
                    new_city[1] = letter[0] + new_city[1]
                    city = city[0] + " ".join(new_city)

                cities_list.append(city)

    return cities_list


if __name__ == "__main__":
    cities_list = parse_cities("cities.txt")
