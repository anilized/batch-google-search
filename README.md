# 1) Gerekli paket:
py -m pip install requests

# 2) Örnek CSV oluşturun (noktalı virgül ile):
test1;test2

# 3) Arka planda calistirmak icin:
py .\search_requests_batch_windows.py .\queries.csv --method HEAD -t 10 -d 1.5 --per-query-delay 3

# 4) Tarayici acarak calistirmak icin:
py .\search_requests_batch_windows.py .\queries.csv --method BROWSER -t 3 -d 1.2
