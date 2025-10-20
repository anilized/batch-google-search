# 1) Gerekli paket:
py -m pip install requests

# 2) Örnek CSV oluşturun (noktalı virgül ile):
test1;test2

# Her sorguyu 10 kez çalıştır, tekrarlar arası 1.5 sn bekle (BACKGROUND)
py .\batch_search.py .\queries.csv -t 10 -d 1.5 --per-query-delay 3 --method HEAD

# Her sorgu 10 kez calistir, tekrarlar arası 1.5 sn bekle (BROWSER)
py .\batch_search.py .\queries.csv -t 10 -d 1.5 --per-query-delay 3 --method BROWSER

