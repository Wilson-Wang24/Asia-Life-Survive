import sys,re,html
want=["Meal at an Inexpensive Restaurant","Rice","Milk","Eggs","Chicken","Apples","Tomato","One-Way Ticket","Basic Utilities","Broadband Internet","Internet","1 Bedroom Apartment Outside","Apartment (1 bedroom) Outside","Outside of Centre","Average Monthly Net Salary"]
for f in sys.argv[1:]:
    t=open(f,encoding='utf-8',errors='replace').read()
    print("==",f.split('/')[-1], re.search(r'<title>([^<]*)',t).group(1)[:80])
    for m in re.finditer(r'<tr[^>]*>(.*?)</tr>',t,re.S):
        row=m.group(1)
        tds=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
        if len(tds)<2: continue
        label=html.unescape(re.sub(r'<[^>]+>','',tds[0])).strip()
        if any(w.lower() in label.lower() for w in want):
            val=html.unescape(re.sub(r'<[^>]+>','',tds[1])).strip().replace('\xa0',' ')
            print(f"  {label[:75]:75} | {val}")
    m=re.search(r'Last update[^<]*',t); print("  ",m.group(0) if m else "no last update")
    m=re.search(r'There are (\d+) entries[^<]*',t); print("  ",m.group(0)[:120] if m else "")
