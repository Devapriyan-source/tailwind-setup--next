import random
import jsonlines

# Load quotes from JSONL file
with jsonlines.open("../data/quotes.json") as reader:
    quotes_data = [quote for quote in reader]

def get_random_quote() -> str:
    return random.choice(quotes_data)["quote"]
