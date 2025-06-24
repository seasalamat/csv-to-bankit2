import csv
import argparse

def transform_data(input_file, output_file, identifier):
    with open(input_file, mode="r", newline="") as csvfile, open(output_file, mode="w") as txtfile:
        reader = csv.DictReader(csvfile, delimiter=",")

        # Write identifier text at the beginning if provided
        if identifier:
            txtfile.write(f"{identifier}\n")

        for row in reader:
            start, stop = row["start"], row["stop"]
            plus_minus = row["plus-minus"]
            partial = row.get("partial", "")

            # Determine column order based on strand orientation
            if plus_minus == "+":
                col1, col2 = start, stop
            elif plus_minus == "-":
                col1, col2 = stop, start
            else:
                continue  # Skip rows without valid strand information

            # Apply partial sequence notation
            if partial == "5":
                col1 = f">{col2}"
            elif partial == "3":
                col2 = f"<{col1}"

            # Write transformed data with corrected tab alignment and no extra spacing
            txtfile.write(f"{col1}\t{col2}\tgene\n")
            txtfile.write(f"\t\t\tgene\t{row['orf']}\n")
            txtfile.write(f"{col1}\t{col2}\tCDS\n")
            txtfile.write(f"\t\t\tproduct\t{row['annotation']}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform CSV data into formatted text file with tab delimiters.")
    parser.add_argument("-i", "--input", required=True, help="Path to input CSV file.")
    parser.add_argument("-o", "--output", required=True, help="Path to output text file.")
    parser.add_argument("-id", "--identifier", help="Identifier text to add at the beginning of the output file.")

    args = parser.parse_args()

    transform_data(args.input, args.output, args.identifier)