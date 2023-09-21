# スケジューリングアルゴリズム（シミュレータ）

Description: This program simulates the Round Robin / First Come First Service / Shortest Processing Time First scheduling algorithm.  
Author: https://github.com/shisotem  
Date: 2023-07-29  


## 概要

以下3種類のスケジューリングアルゴリズムの動作をシミュレートするプログラムです．
- ラウンドロビン（rr.py）
- 到着順（fcfs.py）
- 処理時間順（sptf.py）


## 動作方法

- ラウンドロビン（rr.py）:
1. num_tasks（入力するプロセスの数）を入力します．
2. task_name（プロセス名），arrival_time（到着時刻），cost（処理時間）の順に半角スペース区切りで入力し，改行します．残りのプロセスについても，これと同様に入力します．
3. time_quantum（ラウンドロビンのタイムクォンタム）を入力します．

- 到着順（fcfs.py），処理時間順（sptf.py）:
1. num_tasks（入力するプロセスの数）を入力します．
2. task_name（プロセス名），arrival_time（到着時刻），cost（処理時間）の順に半角スペース区切りで入力し，改行します．残りのプロセスについても，これと同様に入力します．


## 動作結果

- ラウンドロビン（rr.py），到着順（fcfs.py），処理時間順（sptf.py）:
1. 各時刻において処理されるプロセスのプロセス名が出力されます．その時刻に処理が完了するプロセスの場合，併せて "Fin" と出力されます．また，プロセスが1つも到着していない場合等，何も処理が行われない時刻については，"-" と出力されます．
2. task_name，arrival_time に加え，finish_time（処理完了時刻），turnaround_time（応答時間，ターンアラウンドタイム）がプロセス毎に出力されます．さらに，ターンアラウンドタイムの平均値が出力されます．


## 動作例

- ラウンドロビン（rr.py）
```bash
$ python rr.py

--- INPUT ---

num_tasks:
4

task_name arrival_time cost:
A 0 2
B 1 10
C 3 7
D 5 3

time_quantum:
2

--- PROCESS ---

 1: A
 2: A => Fin
 3: B
 4: B
 5: C
 6: C
 7: B
 8: B
 9: D
10: D
11: C
12: C
13: B
14: B
15: D => Fin
16: C
17: C
18: B
19: B
20: C => Fin
21: B
22: B => Fin

--- RESULT ---

task_name  arrival_time  finish_time  turnaround_time
A          0             2            2              
B          1             22           21             
C          3             20           17             
D          5             15           10             

average_turnaround_time: 12.50

```

- 到着順（fcfs.py）
```bash
$ python fcfs.py

--- INPUT ---

num_tasks:
4

task_name arrival_time cost:
A 0 2
B 1 10
C 3 7
D 5 3

--- PROCESS ---

 1: A
 2: A => Fin
 3: B
 4: B
 5: B
 6: B
 7: B
 8: B
 9: B
10: B
11: B
12: B => Fin
13: C
14: C
15: C
16: C
17: C
18: C
19: C => Fin
20: D
21: D
22: D => Fin

--- RESULT ---

task_name  arrival_time  finish_time  turnaround_time
A          0             2            2              
B          1             12           11             
C          3             19           16             
D          5             22           17             

average_turnaround_time: 11.50

```

- 処理時間順（sptf.py）
```bash
$ python sptf.py

--- INPUT ---

num_tasks:
4

task_name arrival_time cost:
A 0 2
B 1 10
C 3 7
D 5 3

--- PROCESS ---

 1: A
 2: A => Fin
 3: B
 4: B
 5: B
 6: B
 7: B
 8: B
 9: B
10: B
11: B
12: B => Fin
13: D
14: D
15: D => Fin
16: C
17: C
18: C
19: C
20: C
21: C
22: C => Fin

--- RESULT ---

task_name  arrival_time  finish_time  turnaround_time
A          0             2            2              
B          1             12           11             
C          3             22           19             
D          5             15           10             

average_turnaround_time: 10.50

```


## ソース概要

プロセスのリストを入力から受け取り，それに対するスケジューリングアルゴリズムの処理手順をシュミレートします．  

例えば，run_round_robin 関数では，プロセスのリストを到着時刻に基づいてソートした後，全てのプロセスの状態が finished となるまでメインループを繰り返します．メインループ内では，新しいプロセスの到着を確認し，待ち行列の末尾に追加することに加えて，待ち行列の先頭要素のプロセスを取り出し（dequeue_task），次の処理対象（current_task）とします．なお，待ち行列が空であった場合，dequeue_task 関数は None を返し，current_task の値は None となるため，時刻を進めて次のループへと移ります．そうでない場合，current_task の処理を行います（execute_task）．  
execute_task 関数では，処理対象のプロセスが処理完了までに要する時間がタイムクォンタムよりも大きい場合，その回の execute_task 関数呼び出しでは処理が完了しないため，タイムクォンタムの時間だけ処理を進めます．各時刻における，新しいプロセスの到着の確認もこの関数内で行い，最後には処理対象のプロセスを待ち行列の末尾に戻し，タイムクォンタムの時間だけ進んだ時刻を返します．反対に，処理対象のプロセスが処理完了までに要する時間がタイムクォンタム以下である場合，最後にはプロセスの状態を finished に更新します．また，この execute_task 関数内において，各時刻の処理状況の出力を行います．  
メインループ終了の際には，各プロセスのインスタンス変数に保持されている値を用いて計算を行い，ターンアラウンドタイムの平均値等を出力します． 

以上はラウンドロビン（rr.py）のソース概要になりますが，他2つのアルゴリズムはこのコードを基に，一部を書き換えることにより実装されています．例えば，処理時間順（sptf.py）では，プロセスを待ち行列へ追加する（enqueue_task）際に，処理時間に基づいた待ち行列のソートを行うことにより実装されています． 