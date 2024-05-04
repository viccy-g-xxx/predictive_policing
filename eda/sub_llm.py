import pandas as pd
from openai import OpenAI

client = OpenAI()

test_df = pd.read_csv("test_files.csv")
