# Test Case
```
human, human_40n : 조교님이 제공해주신 데이터 그래프 G와 쿼리 그래프 q
test, test_40n : 논문에 나온 예시의 데이터 그래프 G와 쿼리 그래프 q (simpler)
```

# Select DAG
```
Original (DAG input) : ./program human human_40n 100 > human_40n.dag
Modified : python main.py human human_40n 100 > human_40n.dag
```

# Run DAF
```
Original : ./daf_1min -d human -q human_40n -n 100 > result_original
Modified : ./daf_1min -d human -q human_40n -a human_40n.dag -n 100 > result_modified
```

# Compare Result
```
python sort_result.py result_modified result_original
```
