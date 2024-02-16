import argparse
import csv
from googletrans import Translator

translator = Translator()

parser = argparse.ArgumentParser(prog="AutoTranslator")
parser.add_argument("filename", help="CSV file to translate")
parser.add_argument("-s", "--src", help="Language to translate from", required=True)
parser.add_argument("-d", "--dest", help="Language to translate to", required=True)

args = parser.parse_args()

translated_dict: dict[str, str] = {}

with open(args.filename, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    translated_rows: list[list[str]] = []

    for idx, row in enumerate(csv_reader):
        to_translate = row[0].strip()
        translated = row[1].strip()

        if translated != "":
            translated_dict[to_translate] = translated

        translated_rows.append(row)

    for idx, row in enumerate(translated_rows):
        if idx == 0:
            continue

        if row[1].strip() != "":
            print(f"{idx}. SKIP: {row[1]}")
            continue

        if row[0].strip() == "":
            print(f"{idx}. SKIP: Empty")
            continue

        to_translate = row[0].strip()

        if to_translate in translated_dict:
            row[1] = translated_dict[to_translate]
            print(f"{idx}. DUPLICATE: {to_translate} -> {row[1]}")
            continue

        try:
            translation = translator.translate(
                to_translate, src=args.src, dest=args.dest
            )
            translation = str(translation.text).split("\n")
            translation = "\n".join(translation)
            translation = translation.capitalize()

            row[1] = translation
            translated_dict[to_translate] = translation
            print(f"{idx}. ADD: {to_translate} -> {row[1]}")
        except Exception as e:
            print(f"{idx}. ERROR: {to_translate}", e)

        translated_rows[idx] = row

with open(args.filename, "w", newline="") as new_file:
    csv_writer = csv.writer(
        new_file, delimiter=";", lineterminator="\n", quoting=csv.QUOTE_MINIMAL
    )
    csv_writer.writerows(translated_rows)
