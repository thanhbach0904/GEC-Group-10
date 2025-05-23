import csv

def apply_corrections(sentence, edits):
    tokens = sentence.split()
    corrected_tokens = tokens[:]
    offset = 0  # Track shifts in index due to edits

    for start, end, replacement in edits:
        start += offset
        end += offset
        corrected_tokens = (
            corrected_tokens[:start] + replacement.split() + corrected_tokens[end:]
        )
        offset += len(replacement.split()) - (end - start)

    return " ".join(corrected_tokens)

file_path_2 = "fce.test.gold.bea19.m2"

with open(file_path_2, "r", encoding="utf-8") as f:
    lines2 = f.readlines()

data2 = []
i = 0
while i < len(lines2):
    line = lines2[i]
    if line.startswith("S "):
        sentence = line[2:].strip()
        edits = []
        i += 1
        while i < len(lines2) and lines2[i].startswith("A "):
            parts = lines2[i].split("|||")
            span = parts[0].split()[1:3]
            replacement = parts[2]
            if replacement != "-NONE-":
                start, end = map(int, span)
                edits.append((start, end, replacement))
            i += 1
        if edits:
            corrected = apply_corrections(sentence, edits)
            data2.append((sentence, corrected))
        else:
            i += 1
    else:
        i += 1

# Save to CSV
output_csv_path2 = "official_2014_t5_format.csv"
with open(output_csv_path2, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Incorrect", "Corrected"])
    writer.writerows(data2)

print("Saved to:", output_csv_path2)
