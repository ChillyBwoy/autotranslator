import argparse
import csv
from googletrans import Translator

translator = Translator()

parser = argparse.ArgumentParser(prog="AutoTranslator")
parser.add_argument("filename")

args = parser.parse_args()

translated_dict: dict[str, str] = {}

with open(args.filename, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    translated_rows: list[list[str]] = []

    for idx, row in enumerate(csv_reader):
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
            translation = translator.translate(to_translate, src="ja", dest="en")
            translation = str(translation.text)
            translation = translation.capitalize()

            row[1] = translation
            translated_dict[to_translate] = translation
            print(f"{idx}. ADD: {to_translate} -> {row[1]}")
        except Exception as e:
            print(f"{idx}. ERROR: {to_translate}", e)

        translated_rows[idx] = row

with open(args.filename, "w", newline="") as new_file:
    csv_writer = csv.writer(new_file, delimiter=";", lineterminator="\n")
    csv_writer.writerows(translated_rows)
