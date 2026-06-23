"""
Multilingual NER (mNER) training pipeline
Fine-tunes a multilingual transformer (XLM-RoBERTa) on WikiANN
for PER / LOC / ORG entity recognition across multiple languages.

Usage:
    pip install transformers datasets evaluate seqeval accelerate --break-system-packages
    python train.py
"""

import shutil
from pathlib import Path

import numpy as np
from datasets import load_dataset, concatenate_datasets, DatasetDict
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    DataCollatorForTokenClassification,
    EarlyStoppingCallback,
    pipeline
)
import evaluate
from pathlib import Path

# 1. Configuration — adjust languages / model here
MODEL_NAME = "xlm-roberta-base"          # multilingual backbone (covers vi + 100 langs)
LANGUAGES = ["en", "vi", "es", "fr"]      # WikiANN language codes to combine
LABEL_LIST = ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"]
label2id = {l: i for i, l in enumerate(LABEL_LIST)}
id2label = {i: l for i, l in enumerate(LABEL_LIST)}

# If short on time/compute, subsample train set per language (set to None to use all)
MAX_TRAIN_PER_LANG = 3000

# Where rolling checkpoints live during training (gets cleaned up afterwards)
CHECKPOINT_DIR = "./mner-xlmr"
# Where the final, official model is promoted to
PRODUCTION_DIR = str(Path(__file__).resolve().parent / "mner-production")


# 2. Load and combine WikiANN subsets for chosen languages
def load_multilingual_wikiann(languages, max_train_per_lang=None):
    train_sets, val_sets, test_sets = [], [], []
    for lang in languages:
        ds = load_dataset("unimelb-nlp/wikiann", lang)
        train_split = ds["train"]
        if max_train_per_lang is not None and len(train_split) > max_train_per_lang:
            train_split = train_split.shuffle(seed=42).select(range(max_train_per_lang))
        train_sets.append(train_split)
        val_sets.append(ds["validation"])
        test_sets.append(ds["test"])
    return DatasetDict({
        "train": concatenate_datasets(train_sets).shuffle(seed=42),
        "validation": concatenate_datasets(val_sets),
        "test": concatenate_datasets(test_sets),
    })


raw_datasets = load_multilingual_wikiann(LANGUAGES, MAX_TRAIN_PER_LANG)
print(raw_datasets)

# 3. Tokenize + align word-level labels to subword tokens
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(
        examples["tokens"], truncation=True, is_split_into_words=True
    )
    all_labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                # special tokens ([CLS], [SEP], padding)
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                # first subword of a word -> keep the real label
                label_ids.append(label[word_idx])
            else:
                # subsequent subwords of the same word -> ignore in loss
                label_ids.append(-100)
            previous_word_idx = word_idx
        all_labels.append(label_ids)
    tokenized_inputs["labels"] = all_labels
    return tokenized_inputs


tokenized_datasets = raw_datasets.map(
    tokenize_and_align_labels, batched=True, remove_columns=raw_datasets["train"].column_names
)

# 4. Model
model = AutoModelForTokenClassification.from_pretrained(
    MODEL_NAME, num_labels=len(LABEL_LIST), id2label=id2label, label2id=label2id
)

# 5. Metrics (seqeval -> precision/recall/F1 per entity + overall)
metric = evaluate.load("seqeval")


def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [
        [id2label[pp] for (pp, ll) in zip(pred, lab) if ll != -100]
        for pred, lab in zip(predictions, labels)
    ]
    true_labels = [
        [id2label[ll] for (pp, ll) in zip(pred, lab) if ll != -100]
        for pred, lab in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


# 6. Training
data_collator = DataCollatorForTokenClassification(tokenizer)

training_args = TrainingArguments(
    output_dir=CHECKPOINT_DIR,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=10,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=1,          # <-- keep only the most recent checkpoint;
                                  #     Trainer auto-deletes older ones on every save
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    logging_steps=50,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    processing_class=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    callbacks=[
        EarlyStoppingCallback(early_stopping_patience=2)
    ],
)

if __name__ == "__main__":
    trainer.train()

    test_results = trainer.evaluate(tokenized_datasets["test"])
    print("Test results:", test_results)

    # ----------------------------------------------------------------
    # 7. Promote the final trained model to the OFFICIAL production dir.
    #    This copy has only model weights + tokenizer (no optimizer/
    #    scheduler state), so it's lightweight and ready for serving.
    # ----------------------------------------------------------------

    trainer.save_model(PRODUCTION_DIR)
    tokenizer.save_pretrained(PRODUCTION_DIR)
    print(f"Official model saved to: {PRODUCTION_DIR}")

    # ----------------------------------------------------------------
    # 8. Clean up: once the official model is safely saved, the rolling
    #    checkpoints under CHECKPOINT_DIR are no longer needed. Remove
    #    the whole folder (every checkpoint-N/, optimizer states, etc.)
    #    so only the final official model remains on disk.
    # ----------------------------------------------------------------
    checkpoint_path = Path(CHECKPOINT_DIR)
    if checkpoint_path.exists():
        shutil.rmtree(checkpoint_path)
        print(f"Removed temp checkpoint folder: {CHECKPOINT_DIR}")

    # --------------------------------------------------------------
    # 9. Quick sanity check for the web demo backend
    # --------------------------------------------------------------

    nlp = pipeline(
        "ner",
        model=PRODUCTION_DIR,
        tokenizer=PRODUCTION_DIR,
        aggregation_strategy="simple",
    )
    samples = [
        "Nguyễn Phú Trọng sinh ra tại Hà Nội.",
        "Barack Obama was born in Honolulu.",
        "Lionel Messi joue pour le Paris Saint-Germain.",
    ]
    for s in samples:
        print(s, "->", nlp(s))