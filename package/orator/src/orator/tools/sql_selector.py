from rapidfuzz import fuzz

def select_sql_db(user_query, db_schemas):
    """
    Ranks DB schemas by fuzzy similarity to the user query.
    Returns list of schemas sorted by relevance (best match first).
    """
    ranked = sorted(
        db_schemas,
        key=lambda schema: fuzz.token_sort_ratio(user_query, schema),
        reverse=True
    )
    return ranked
