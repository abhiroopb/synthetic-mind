# Get a manager's direct reports with sub-team assignments

```bash
# Step 1: Get the manager's org node ID
ORG_ID=$(curl -s -H "Authorization: Token $PEOPLE_API_TOKEN" \
  "https://my.sqprod.co/people/api/p/eschlenker.json" | python3 -c "
import sys, json; d = json.load(sys.stdin)
print(d['org_chart_nodes'][0]['id'])")

# Step 2: Fetch direct reports filtered by parent_id
curl -s -H "Authorization: Token $PEOPLE_API_TOKEN" \
  "https://my.sqprod.co/people/api/org_chart_nodes.json?type=ALL&parent_id=$ORG_ID" | python3 -c "
import sys, json
for n in json.load(sys.stdin):
    st = n.get('sub_team_or_sub_function') or '(ungrouped)'
    print(f\"{n['employee_username']:15s} {st}\")
"
```
