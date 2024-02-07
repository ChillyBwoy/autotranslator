import argparse
import csv
from googletrans import Translator

translator = Translator()

parser = argparse.ArgumentParser(prog="AutoTranslator")
parser.add_argument("filename")

args = parser.parse_args()

with open(args.filename, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    translated_rows: list[list[str]] = []

    for idx, row in enumerate(csv_reader):
        if idx == 0:
            continue

        if row[0]:
            try:
                translation: str = translator.translate(row[0], src="ja", dest="en")
                row[1] = translation.text
                print(f"{row[0]} -> {row[1]}")
            except IndexError:
                print(f"Error translating: {row[0]}")

        translated_rows.append(row)

with open(args.filename, "w", newline="") as new_file:
    csv_writer = csv.writer(new_file, delimiter=";")
    csv_writer.writerows(translated_rows)
