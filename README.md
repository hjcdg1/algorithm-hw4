테스트 케이스
- human : 조교님이 제공해주신 원래 human 파일
- human_40n : 조교님이 제공해주신 원래 human_40n 파일
- test : 논문에 나와 있는 예시 그림을 가지고 만든 예시 (더 간단하여 테스트하기 편리)
- test_40n : 논문에 나와 있는 예시 그림을 가지고 만든 예시 (더 간단하여 테스트하기 편리)

DAG 생성 방법
- DAG를 만드는 프로그램("program")의 실행파일 생성 : ./compile.sh
- 100개의 DAG 생성 (조교님이 주신 테스트 케이스) : ./program human human_40n 100 > human_40n.dag
- 100개의 DAG 생성 (논문 그림 테스트 케이스) : python main.py test test_40n 100 (지금은 화면으로 결과가 출력됨)

실행 
- (1) 기본 실행 : ./daf_1min -d human -q human_40n -n 100
- (2) 생성한 DAG를 가지고 DAF 실행 (조교님이 주신 테스트 케이스) : ./daf_1min -d human -q human_40n -a human_40n.dag -n 100
- (3) 생성한 DAG를 가지고 DAF 실행 (논문 그림 테스트 케이스) : ./daf_1min -d test -q test_40n -a test_40n.dag -n 100
- (1)과 (2)의 실행 결과는 당연히 (거의) 동일
