import os
import json

def convert_conll_to_jsonl(input_path, output_path):
    data = []
    with open(input_path, "r", encoding="utf8") as f:
        lines = f.readlines()

    text = ""
    entities = []
    offset = 0
    current_label = None
    current_start = None

    for line in lines:
        line = line.strip()
        if line == "":
            if text.strip():
                data.append({
                    "text": text.strip(),
                    "entities": entities
                })
            text = ""
            entities = []
            offset = 0
            current_label = None
            current_start = None
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        token = parts[0]
        tag = parts[-1]

        start = offset
        end = offset + len(token)

        if tag.startswith("B-"):
            if current_label is not None:
                entities.append([current_start, offset - 1, current_label])
            current_start = start
            current_label = tag[2:]
        elif tag.startswith("I-") and current_label:
            pass  # continue the entity
        else:
            if current_label is not None:
                entities.append([current_start, offset - 1, current_label])
                current_label = None
                current_start = None

        text += token + " "
        offset += len(token) + 1

    # Add last sentence
    if text.strip():
        if current_label is not None:
            entities.append([current_start, offset - 1, current_label])
        data.append({
            "text": text.strip(),
            "entities": entities
        })

    with open(output_path, "w", encoding="utf8") as out:
        for item in data:
            json.dump(item, out)
            out.write("\n")

    print(f"✔️ Successfully converted to: {output_path}")

if __name__ == "__main__":
    input_file = "data.txt"               # your dataset in root
    output_file = "train_data.jsonl"      # output file
    convert_conll_to_jsonl(input_file, output_file)
