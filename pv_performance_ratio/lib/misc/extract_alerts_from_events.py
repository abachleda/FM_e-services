def extract_alerts_from_events(events):
    alerts = [d['alerts']for d in events]
    total_list=[]
    for i in alerts: 
        i=alerts.index(i)
        for k in alerts[i]:
             k=alerts[i].index(k)
             total_list.append(alerts[i][k])
        
    return total_list