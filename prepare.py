import spacy
from spacy.tokens import DocBin
import json

nlp = spacy.blank("en")
db = DocBin()

with open("train_data.jsonl", "r", encoding="utf8") as f:
    for line in f:
        data = json.loads(line)
        doc = nlp.make_doc(data["text"])
        ents = []
        for start, end, label in data["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is not None:
                ents.append(span)
        doc.ents = ents
        db.add(doc)

db.to_disk("train.spacy")
