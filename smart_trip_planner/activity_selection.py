def greedy_schedule(selected_df, total_days):
if selected_df.empty:
return []
sel = selected_df.copy()
sel['Score'] = sel['Popularity'] / sel['TimeRequired']
sel = sel.sort_values('Score', ascending=False).reset_index(drop=True)


schedule = []
remaining = total_days
for _, row in sel.iterrows():
if remaining >= row['TimeRequired']:
schedule.append({
'Destination': row['Destination'],
'TimeRequired': row['TimeRequired']
})
remaining -= row['TimeRequired']
return schedule