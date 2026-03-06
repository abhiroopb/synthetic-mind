# Complex Filtering

Use Airtable's formula syntax for sophisticated queries.

## Date Ranges

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=IS_AFTER({Created},'2024-01-01')"

curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=IS_BEFORE({Date},TODAY())"
```

## Text Search

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=SEARCH('keyword',{Description})>0"

curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=FIND('text',{Field})>0"

curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=SEARCH('text',LOWER({Field}))"
```

## Multiple Conditions

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=AND(OR({Status}='Active',{Status}='Pending'),{Priority}!='Low')"

curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula=AND({Price}>=100,{Price}<=500)"
```

## Empty/Non-Empty Checks

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula={Field}!=BLANK()"

curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula={Field}=BLANK()"
```

## Numeric Comparisons

```bash
curl -G "https://api.airtable.com/v0/${BASE_ID}/{tableIdOrName}" \
  -H "Authorization: Bearer $AIRTABLE_TOKEN" \
  --data-urlencode "filterByFormula={Count}>10"
```

## Tips

- Use single quotes for string literals in formulas: `{Field}='value'`
- Ensure field names are wrapped in curly braces: `{Field Name}`
- Use `--data-urlencode` to properly encode complex formulas
- Formula field names are case-sensitive

## Reference

See the [Formula Field Reference](https://support.airtable.com/docs/formula-field-reference) for complete formula syntax documentation.
