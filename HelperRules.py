from mlxtend.preprocessing import TransactionEncoder

from mlxtend.frequent_patterns import apriori, association_rules

import pandas, warnings

warnings.filterwarnings("ignore")

url = "/assets/AprioriFinal.csv"

usecols = ["TransactionID", "ItemCode"]

def OpenTable(url, **cols):
  """
  Open Pandas Table
  """
  table = pandas.read_table(url, sep=",", **cols)
  return table

def TraTable(table, columns):
  """
  Perform Transaction Encoder, Table Fit Transform on Encoder Table
  """
  transactions = table[columns].str.split(',').apply(lambda x: [item.strip() for item in x]).tolist()
  tranencoder = TransactionEncoder()
  te_array = tranencoder.fit(transactions).transform(transactions)
  encoder_table = pandas.DataFrame(te_array, columns=tranencoder.columns_)
  return encoder_table

def Helper(table, itemsets, sorting):
  """
  Helper to Maintain Result on Proper Format
  """
  for item in itemsets:
    table[item] = table[item].apply(lambda val : ", ".join(list(val)))
  table = table.round(5)
  table = table.sort_values(sorting, ascending=False)
  return table

def GetApriori(itemsets, confidence):
  """
  Apriori Rules
  """
  rules = association_rules(itemsets, metric="confidence", min_threshold=confidence, num_itemsets=1)
  rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
  rules = Helper(rules, ['antecedents', 'consequents'], "confidence")
  rules = rules.to_dict(orient="records")
  return rules

def HelperGetRules(support, confidence):
  """
  Helper Final Rules Output
  """
  if not (0.01 <= support <= 0.1):
    raise ValueError("Support is Must be Between 0.01 & 0.1")
  if not (0.1 <= confidence <= 1.0):
    raise ValueError("Confidence is Must be Between 0.1 & 1.0")
  
  encoder_table = TraTable(OpenTable(url, usecols=usecols), "ItemCode")
  itemsets = apriori(encoder_table, min_support=support, use_colnames=True)
  itemsets = itemsets.reindex(columns=itemsets.columns[::-1])
  rules = GetApriori(itemsets, confidence)
  return rules