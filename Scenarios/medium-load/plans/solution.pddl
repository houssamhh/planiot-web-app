ff: parsing domain file
domain 'DOMAIN_NAME' defined
 ... done.
ff: parsing problem file
problem 'PROBLEM_NAME' defined
 ... done.



ff: search configuration is Enforced Hill-Climbing, then A*epsilon with weight 5.
Metric is ((1.00*[RF16](LATENCY_TOPIC30_APP16)1.00*[RF26](LATENCY_TOPIC26_APP6)1.00*[RF36](LATENCY_TOPIC22_APP5)1.00*[RF17](LATENCY_TOPIC30_APP15)1.00*[RF65](LATENCY_TOPIC13_APP12)1.00*[RF66](LATENCY_TOPIC13_APP11)1.00*[RF67](LATENCY_TOPIC13_APP10)1.00*[RF10](LATENCY_TOPIC5_APP6)1.00*[RF22](LATENCY_TOPIC28_APP8)1.00*[RF55](LATENCY_TOPIC17_APP10)1.00*[RF54](LATENCY_TOPIC17_APP16)1.00*[RF35](LATENCY_TOPIC22_APP9)1.00*[RF72](LATENCY_TOPIC11_APP15)1.00*[RF53](LATENCY_TOPIC17_APP7)1.00*[RF74](LATENCY_TOPIC10_APP9)1.00*[RF73](LATENCY_TOPIC11_APP12)1.00*[RF56](LATENCY_TOPIC16_APP4)1.00*[RF46](LATENCY_TOPIC2_APP13)1.00*[RF40](LATENCY_TOPIC21_APP1)1.00*[RF23](LATENCY_TOPIC28_APP14)1.00*[RF27](LATENCY_TOPIC26_APP11)1.00*[RF57](LATENCY_TOPIC16_APP3)1.00*[RF6](LATENCY_TOPIC7_APP5)1.00*[RF61](LATENCY_TOPIC14_APP5)1.00*[RF4](LATENCY_TOPIC8_APP14)1.00*[RF21](LATENCY_TOPIC29_APP11)1.00*[RF9](LATENCY_TOPIC6_APP11)1.00*[RF64](LATENCY_TOPIC14_APP1)1.00*[RF18](LATENCY_TOPIC3_APP3)1.00*[RF19](LATENCY_TOPIC3_APP2)1.00*[RF20](LATENCY_TOPIC29_APP9)1.00*[RF11](LATENCY_TOPIC5_APP4)1.00*[RF50](LATENCY_TOPIC19_APP13)1.00*[RF41](LATENCY_TOPIC20_APP6)1.00*[RF79](LATENCY_TOPIC1_APP1)1.00*[RF0](LATENCY_TOPIC9_APP8)1.00*[RF78](LATENCY_TOPIC1_APP3)1.00*[RF77](LATENCY_TOPIC1_APP5)1.00*[RF76](LATENCY_TOPIC1_APP7)1.00*[RF48](LATENCY_TOPIC19_APP5)1.00*[RF75](LATENCY_TOPIC10_APP11)1.00*[RF28](LATENCY_TOPIC26_APP1)1.00*[RF45](LATENCY_TOPIC2_APP15)1.00*[RF71](LATENCY_TOPIC11_APP8)1.00*[RF1](LATENCY_TOPIC9_APP7)1.00*[RF49](LATENCY_TOPIC19_APP2)1.00*[RF8](LATENCY_TOPIC6_APP4)1.00*[RF13](LATENCY_TOPIC4_APP3)1.00*[RF34](LATENCY_TOPIC23_APP13)1.00*[RF59](LATENCY_TOPIC15_APP6)1.00*[RF58](LATENCY_TOPIC16_APP16)1.00*[RF12](LATENCY_TOPIC5_APP14)1.00*[RF30](LATENCY_TOPIC25_APP16)1.00*[RF3](LATENCY_TOPIC8_APP6)1.00*[RF69](LATENCY_TOPIC12_APP2)1.00*[RF15](LATENCY_TOPIC30_APP7)1.00*[RF42](LATENCY_TOPIC20_APP14)1.00*[RF37](LATENCY_TOPIC22_APP2)1.00*[RF68](LATENCY_TOPIC12_APP9)1.00*[RF60](LATENCY_TOPIC15_APP15)1.00*[RF5](LATENCY_TOPIC7_APP8)1.00*[RF43](LATENCY_TOPIC2_APP9)1.00*[RF2](LATENCY_TOPIC9_APP2)1.00*[RF29](LATENCY_TOPIC25_APP7)1.00*[RF38](LATENCY_TOPIC21_APP8)1.00*[RF33](LATENCY_TOPIC23_APP3)1.00*[RF31](LATENCY_TOPIC24_APP15)1.00*[RF47](LATENCY_TOPIC2_APP1)1.00*[RF70](LATENCY_TOPIC12_APP10)1.00*[RF14](LATENCY_TOPIC4_APP13)1.00*[RF44](LATENCY_TOPIC2_APP7)1.00*[RF52](LATENCY_TOPIC18_APP10)1.00*[RF51](LATENCY_TOPIC18_APP12)1.00*[RF32](LATENCY_TOPIC24_APP14)1.00*[RF7](LATENCY_TOPIC7_APP12)1.00*[RF62](LATENCY_TOPIC14_APP16)1.00*[RF25](LATENCY_TOPIC27_APP3)1.00*[RF24](LATENCY_TOPIC27_APP4)1.00*[RF39](LATENCY_TOPIC21_APP4)1.00*[RF63](LATENCY_TOPIC14_APP13)) - () + 0.00)
COST MINIMIZATION DONE (WITH cost-minimizing relaxed plans).

Cueing down from goal distance:    2 into depth [1]
                                   1            [1]
                                   0

ff: found legal plan as follows
step    0: DROPPINGVS2AN2 TOPIC_ALL APP_ALL
        1: PRIORITIZE_RT_VS_TS_AN TOPIC_ALL APP_ALL
plan cost: 59.439987

time spent:    0.00 seconds instantiating 3689 easy, 0 hard action templates
               0.00 seconds reachability analysis, yielding 4 facts and 7 actions
               0.00 seconds creating final representation with 4 relevant facts, 80 relevant fluents
               0.00 seconds computing LNF
               0.00 seconds building connectivity graph
               0.00 seconds searching, evaluating 3 states, to a max depth of 1
               0.00 seconds total time