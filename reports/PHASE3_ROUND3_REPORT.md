# Phase 3 Round 3 Report

## Verdict

`PHASE3_R3_EMPTY_SET`

All monetary inputs and results are **COSTS_PROVISIONAL**.

## Frozen protocol

Grid `297ba339e7794f47530efb218a6584bb9936e19945f825bbe9adc13a2afa8b47` was frozen before evaluation; F9–F12 contain 16, 16, 16, and 32 configurations respectively (all ≤48). The frozen session map `097c48f511626f1a5bb860ecb1c7f8888bd0eed877dab3b8ab7dd053bae4e9d7` was asserted. F1–F8 are retired. The sealed holdout was never read.

## Per-config forensic evidence

|Instrument|Family|ID|Trades|Gross E|Base E|2x E|Haircut E|Cost/stop p05 / median / p95|Confirm E|Random 95|Shuffle 95|DSR|PBO|LOYO min|Seam|Admission rejections|First failure|Verdict|
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|---|
|BTC|F9|0|1891|0.0428|-0.0435|-0.1298|-0.2231|0.0325 / 0.0789 / 0.1476|-0.0645|-0.0579|-0.0435|0.0000|0.4000|-0.0633|True|year_concentration, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F9|1|1841|0.0634|-0.0228|-0.1091|-0.2075|0.0325 / 0.0787 / 0.1476|-0.0173|-0.0430|-0.0228|0.0000|0.4000|-0.0394|True|year_concentration, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F9|2|1525|0.0572|-0.0282|-0.1135|-0.1991|0.0327 / 0.0800 / 0.1468|-0.0763|-0.0487|-0.0282|0.0000|0.4000|-0.0380|True|year_concentration, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F9|3|1493|0.0706|-0.0146|-0.0998|-0.2173|0.0330 / 0.0797 / 0.1468|-0.0537|-0.0383|-0.0146|0.0003|0.4000|-0.0303|True|year_concentration, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F9|4|1708|0.0369|-0.0489|-0.1347|-0.2290|0.0338 / 0.0791 / 0.1468|-0.0822|-0.0499|-0.0489|0.0000|0.4000|-0.0793|True|year_concentration, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F9|5|1661|0.0401|-0.0457|-0.1315|-0.2328|0.0335 / 0.0784 / 0.1468|-0.0717|-0.0434|-0.0457|0.0000|0.4000|-0.0692|True|year_concentration, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F9|6|1233|0.0817|-0.0047|-0.0912|-0.1920|0.0337 / 0.0804 / 0.1468|-0.1071|-0.0493|-0.0047|0.0015|0.4000|-0.0208|True|year_concentration, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F9|7|1190|0.1059|0.0191|-0.0677|-0.1922|0.0339 / 0.0809 / 0.1468|-0.1039|-0.0356|0.0191|0.0239|0.4000|0.0037|True|year_concentration, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x|year_concentration|KILL|
|BTC|F9|8|785|0.0510|-0.0212|-0.0935|-0.2210|0.0182 / 0.0661 / 0.1463|0.0378|-0.0061|-0.0212|0.0002|0.4000|-0.0259|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F9|9|766|0.0758|0.0037|-0.0684|-0.2108|0.0181 / 0.0657 / 0.1463|0.0429|0.0178|0.0037|0.0041|0.4000|-0.0076|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F9|10|730|0.0559|-0.0145|-0.0848|-0.1829|0.0181 / 0.0634 / 0.1453|0.0590|-0.0075|-0.0145|0.0006|0.4000|-0.0281|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F9|11|714|0.0608|-0.0098|-0.0804|-0.2100|0.0183 / 0.0635 / 0.1454|0.1375|0.0086|-0.0098|0.0011|0.4000|-0.0320|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F9|12|708|0.0438|-0.0283|-0.1005|-0.2189|0.0184 / 0.0647 / 0.1457|0.1584|-0.0101|-0.0283|0.0001|0.4000|-0.0381|True|random_entry_95, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F9|13|691|0.0426|-0.0295|-0.1015|-0.2281|0.0183 / 0.0645 / 0.1457|0.2013|0.0096|-0.0295|0.0001|0.4000|-0.0398|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F9|14|659|0.0081|-0.0627|-0.1336|-0.2480|0.0182 / 0.0643 / 0.1437|0.2077|-0.0078|-0.0627|0.0000|0.4000|-0.0864|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F9|15|642|0.0085|-0.0623|-0.1331|-0.2601|0.0182 / 0.0644 / 0.1438|0.2106|0.0139|-0.0623|0.0000|0.4000|-0.0763|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|0|1231|0.0009|-0.0825|-0.1659|-0.2468|0.0312 / 0.0792 / 0.1426|-0.0007|-0.0492|-0.0825|0.0000|0.1500|-0.1061|True|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|1|1198|0.0142|-0.0699|-0.1539|-0.2410|0.0318 / 0.0797 / 0.1426|0.0106|-0.0382|-0.0699|0.0000|0.1500|-0.0929|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|2|1111|-0.0086|-0.0912|-0.1738|-0.2457|0.0304 / 0.0770 / 0.1423|0.0272|-0.0400|-0.0912|0.0000|0.1500|-0.1154|True|random_entry_95, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|3|1082|0.0013|-0.0819|-0.1651|-0.2456|0.0317 / 0.0781 / 0.1424|0.0383|-0.0341|-0.0819|0.0000|0.1500|-0.1062|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|4|993|-0.0034|-0.0860|-0.1686|-0.2471|0.0340 / 0.0760 / 0.1450|0.0326|-0.0407|-0.0860|0.0000|0.1500|-0.1018|True|year_concentration, random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F10|5|967|0.0076|-0.0755|-0.1586|-0.2606|0.0343 / 0.0761 / 0.1451|0.0425|-0.0361|-0.0755|0.0000|0.1500|-0.0918|True|year_concentration, random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F10|6|867|-0.0023|-0.0840|-0.1657|-0.2446|0.0344 / 0.0748 / 0.1428|0.0679|-0.0438|-0.0840|0.0000|0.1500|-0.0976|True|year_concentration, random_entry_95, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F10|7|844|0.0083|-0.0738|-0.1560|-0.2616|0.0351 / 0.0751 / 0.1430|0.0742|-0.0348|-0.0738|0.0000|0.1500|-0.0897|True|year_concentration, random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F10|8|501|0.0435|-0.0263|-0.0961|-0.2078|0.0184 / 0.0623 / 0.1428|0.1337|0.0008|-0.0263|0.0002|0.1500|-0.0441|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|9|486|0.0424|-0.0275|-0.0973|-0.2512|0.0184 / 0.0622 / 0.1428|0.1612|0.0197|-0.0275|0.0003|0.1500|-0.0454|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|10|453|0.0101|-0.0590|-0.1281|-0.2174|0.0184 / 0.0623 / 0.1430|0.0781|0.0116|-0.0590|0.0000|0.1500|-0.0745|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|11|439|0.0119|-0.0573|-0.1265|-0.2395|0.0182 / 0.0628 / 0.1432|0.0985|0.0263|-0.0573|0.0000|0.1500|-0.0747|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|12|402|0.0088|-0.0604|-0.1296|-0.2395|0.0183 / 0.0610 / 0.1421|0.1810|0.0043|-0.0604|0.0000|0.1500|-0.0677|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|13|394|0.0289|-0.0402|-0.1093|-0.2558|0.0183 / 0.0610 / 0.1422|0.2170|0.0226|-0.0402|0.0001|0.1500|-0.0502|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|14|358|-0.0148|-0.0843|-0.1539|-0.2690|0.0187 / 0.0609 / 0.1427|0.1537|0.0181|-0.0843|0.0000|0.1500|-0.0933|True|random_entry_95, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F10|15|351|0.0003|-0.0693|-0.1389|-0.2998|0.0186 / 0.0612 / 0.1429|0.1628|0.0350|-0.0693|0.0000|0.1500|-0.0813|True|random_entry_95, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F11|0|926|-0.0169|-0.0973|-0.1778|-0.2432|0.0326 / 0.0734 / 0.1436|-0.0843|-0.0477|-0.0973|0.0000|0.2000|-0.1355|True|year_concentration, random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F11|1|517|-0.0220|-0.1027|-0.1834|-0.2624|0.0324 / 0.0735 / 0.1430|-0.1681|-0.0376|-0.1027|0.0000|0.2000|-0.1615|True|year_concentration, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F11|2|638|-0.0086|-0.0887|-0.1687|-0.2314|0.0332 / 0.0731 / 0.1436|-0.1189|-0.0418|-0.0887|0.0000|0.2000|-0.1177|True|year_concentration, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F11|3|343|-0.0038|-0.0843|-0.1649|-0.2796|0.0331 / 0.0731 / 0.1438|-0.1180|-0.0250|-0.0843|0.0000|0.2000|-0.1469|True|year_concentration, random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F11|4|724|-0.0141|-0.0927|-0.1714|-0.2466|0.0320 / 0.0718 / 0.1423|-0.0676|-0.0373|-0.0927|0.0000|0.2000|-0.1490|True|year_concentration, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F11|5|109|-0.0162|-0.0958|-0.1754|-0.2381|0.0323 / 0.0771 / 0.1410|-0.0370|0.0165|-0.0958|0.0000|0.2000|-0.1704|True|year_concentration, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F11|6|398|-0.0019|-0.0804|-0.1589|-0.2571|0.0332 / 0.0721 / 0.1436|-0.0561|-0.0242|-0.0804|0.0000|0.2000|-0.1156|True|year_concentration, random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F11|7|24|-0.0877|-0.1667|-0.2456|-0.2636|0.0366 / 0.0764 / 0.1311|0.1029|0.1070|-0.1667|0.0000|0.2000|-0.1980|True|sample_floor, year_concentration, random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|sample_floor|KILL|
|BTC|F11|8|593|0.0380|-0.0318|-0.1016|-0.2332|0.0179 / 0.0624 / 0.1435|-0.1097|-0.0116|-0.0318|0.0001|0.2000|-0.0523|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F11|9|201|0.0906|0.0260|-0.0386|-0.1472|0.0171 / 0.0524 / 0.1430|-0.0040|0.0206|0.0260|0.0117|0.2000|0.0079|True|sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x|sequence_shuffle|KILL|
|BTC|F11|10|468|0.0622|-0.0091|-0.0804|-0.2314|0.0180 / 0.0659 / 0.1425|-0.0682|-0.0069|-0.0091|0.0013|0.2000|-0.0474|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F11|11|144|0.1189|0.0526|-0.0137|-0.1126|0.0175 / 0.0583 / 0.1429|-0.0035|0.0441|0.0526|0.0261|0.2000|-0.0045|True|sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|sequence_shuffle|KILL|
|BTC|F11|12|454|0.0299|-0.0396|-0.1091|-0.1863|0.0191 / 0.0650 / 0.1441|-0.1362|-0.0084|-0.0396|0.0001|0.2000|-0.0726|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F11|13|43|0.0717|0.0093|-0.0531|-0.1331|0.0147 / 0.0561 / 0.1389|-0.0844|0.1028|0.0093|0.0038|0.2000|-0.0673|True|sample_floor, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|sample_floor|KILL|
|BTC|F11|14|343|0.0227|-0.0476|-0.1179|-0.2568|0.0192 / 0.0663 / 0.1438|-0.1941|0.0005|-0.0476|0.0000|0.2000|-0.0857|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F11|15|9|0.1390|0.0911|0.0433|-0.3202|0.0178 / 0.0364 / 0.0893|-1.0382|0.2625|0.0911|0.0103|0.2000|-0.0006|True|sample_floor, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, loyo|sample_floor|KILL|
|BTC|F12|0|814|0.0073|-0.0794|-0.1661|-0.2493|0.0340 / 0.0805 / 0.1473|-0.0329|-0.0405|-0.0794|0.0000|0.8500|-0.0923|True|year_concentration, random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F12|1|787|0.0102|-0.0767|-0.1636|-0.2503|0.0340 / 0.0809 / 0.1474|0.0124|-0.0293|-0.0767|0.0000|0.8500|-0.0909|True|year_concentration, random_entry_95, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F12|2|1226|0.0642|-0.0207|-0.1056|-0.1956|0.0313 / 0.0784 / 0.1474|-0.0279|-0.0464|-0.0207|0.0001|0.8500|-0.0417|True|sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|sequence_shuffle|KILL|
|BTC|F12|3|1194|0.0807|-0.0039|-0.0885|-0.2033|0.0313 / 0.0778 / 0.1472|-0.0059|-0.0380|-0.0039|0.0017|0.8500|-0.0213|True|confirmation_firewall, dsr, haircut, cost_2x, loyo|confirmation_firewall|KILL|
|BTC|F12|4|810|0.0310|-0.0563|-0.1436|-0.2167|0.0336 / 0.0818 / 0.1474|-0.0644|-0.0363|-0.0563|0.0000|0.8500|-0.1175|True|year_concentration, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F12|5|797|0.0486|-0.0388|-0.1262|-0.2144|0.0333 / 0.0817 / 0.1474|-0.0594|-0.0318|-0.0388|0.0000|0.8500|-0.0934|True|year_concentration, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F12|6|1238|0.0131|-0.0717|-0.1566|-0.2284|0.0321 / 0.0783 / 0.1472|-0.0117|-0.0461|-0.0717|0.0000|0.8500|-0.1090|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|7|1216|-0.0009|-0.0859|-0.1710|-0.2517|0.0320 / 0.0788 / 0.1473|0.0054|-0.0367|-0.0859|0.0000|0.8500|-0.1213|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|8|774|-0.0179|-0.1019|-0.1859|-0.2464|0.0337 / 0.0781 / 0.1466|-0.0463|-0.0369|-0.1019|0.0000|0.8500|-0.1375|True|year_concentration, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F12|9|757|0.0024|-0.0817|-0.1659|-0.2488|0.0340 / 0.0782 / 0.1467|-0.0226|-0.0285|-0.0817|0.0000|0.8500|-0.1250|True|year_concentration, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F12|10|1176|-0.0213|-0.1034|-0.1856|-0.2591|0.0326 / 0.0753 / 0.1475|-0.0433|-0.0474|-0.1034|0.0000|0.8500|-0.1326|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|11|1152|-0.0187|-0.1008|-0.1829|-0.2643|0.0329 / 0.0753 / 0.1476|-0.0458|-0.0323|-0.1008|0.0000|0.8500|-0.1307|True|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|12|773|0.0693|-0.0149|-0.0991|-0.2071|0.0340 / 0.0788 / 0.1469|-0.0370|-0.0411|-0.0149|0.0005|0.8500|-0.0385|True|year_concentration, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F12|13|761|0.0864|0.0023|-0.0819|-0.1832|0.0338 / 0.0788 / 0.1469|-0.0477|-0.0325|0.0023|0.0036|0.8500|-0.0349|True|year_concentration, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|year_concentration|KILL|
|BTC|F12|14|1166|0.0306|-0.0511|-0.1329|-0.2154|0.0332 / 0.0751 / 0.1472|-0.0080|-0.0424|-0.0511|0.0000|0.8500|-0.0595|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|15|1150|0.0498|-0.0319|-0.1135|-0.2111|0.0331 / 0.0744 / 0.1474|-0.0022|-0.0323|-0.0319|0.0000|0.8500|-0.0411|True|confirmation_firewall, dsr, haircut, cost_2x, loyo|confirmation_firewall|KILL|
|BTC|F12|16|429|0.0223|-0.0490|-0.1202|-0.2205|0.0191 / 0.0633 / 0.1459|0.1012|0.0085|-0.0490|0.0000|0.8500|-0.0738|True|random_entry_95, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|17|426|0.0358|-0.0352|-0.1063|-0.2101|0.0191 / 0.0646 / 0.1460|0.1527|0.0207|-0.0352|0.0001|0.8500|-0.0571|True|random_entry_95, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|18|544|0.0528|-0.0196|-0.0920|-0.2187|0.0193 / 0.0661 / 0.1447|0.0267|-0.0018|-0.0196|0.0004|0.8500|-0.0418|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|19|525|0.0641|-0.0086|-0.0812|-0.1984|0.0192 / 0.0663 / 0.1448|0.0276|0.0167|-0.0086|0.0013|0.8500|-0.0285|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|20|434|0.0682|-0.0025|-0.0733|-0.2021|0.0188 / 0.0621 / 0.1460|-0.0532|0.0061|-0.0025|0.0023|0.8500|-0.0334|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|21|430|0.0783|0.0073|-0.0637|-0.1686|0.0191 / 0.0627 / 0.1461|-0.0254|0.0192|0.0073|0.0049|0.8500|-0.0198|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|22|543|0.0478|-0.0242|-0.0963|-0.2062|0.0184 / 0.0656 / 0.1447|-0.0050|-0.0004|-0.0242|0.0002|0.8500|-0.0632|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|23|524|0.0527|-0.0197|-0.0922|-0.2289|0.0184 / 0.0659 / 0.1447|0.0388|0.0244|-0.0197|0.0004|0.8500|-0.0549|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|24|423|0.0348|-0.0321|-0.0989|-0.1821|0.0184 / 0.0596 / 0.1433|0.1283|0.0037|-0.0321|0.0001|0.8500|-0.0573|True|random_entry_95, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|25|420|0.0439|-0.0231|-0.0902|-0.1880|0.0187 / 0.0603 / 0.1433|0.1394|0.0308|-0.0231|0.0004|0.8500|-0.0474|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|26|528|0.0550|-0.0159|-0.0868|-0.2023|0.0194 / 0.0667 / 0.1456|0.0261|0.0020|-0.0159|0.0007|0.8500|-0.0404|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|27|499|0.0656|-0.0054|-0.0764|-0.2043|0.0195 / 0.0667 / 0.1461|0.0266|0.0205|-0.0054|0.0018|0.8500|-0.0330|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|28|426|0.0360|-0.0311|-0.0982|-0.1858|0.0185 / 0.0594 / 0.1432|-0.1354|0.0077|-0.0311|0.0001|0.8500|-0.0583|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|29|423|0.0488|-0.0183|-0.0854|-0.2146|0.0184 / 0.0593 / 0.1432|-0.1145|0.0248|-0.0183|0.0006|0.8500|-0.0510|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|30|530|0.0362|-0.0347|-0.1055|-0.2118|0.0193 / 0.0669 / 0.1459|-0.0185|0.0009|-0.0347|0.0001|0.8500|-0.0683|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|BTC|F12|31|509|0.0212|-0.0499|-0.1210|-0.2393|0.0193 / 0.0668 / 0.1465|-0.0078|0.0179|-0.0499|0.0000|0.8500|-0.0747|True|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo|random_entry_95|KILL|
|XAU|F9|0|6380|0.0487|-0.0618|-0.1722|-0.2528|0.0457 / 0.1010 / 0.1471|-0.0459|-0.0668|-0.0618|0.0000|0.0606|-0.0748|False|confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|confirmation_firewall|KILL|
|XAU|F9|1|6176|0.0634|-0.0474|-0.1581|-0.2487|0.0456 / 0.1010 / 0.1472|-0.0092|-0.0476|-0.0474|0.0000|0.0606|-0.0596|False|sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|sequence_shuffle|KILL|
|XAU|F9|2|5620|0.0411|-0.0743|-0.1897|-0.2770|0.0460 / 0.1069 / 0.1479|-0.0714|-0.0699|-0.0743|0.0000|0.0606|-0.0867|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|3|5384|0.0675|-0.0486|-0.1646|-0.2628|0.0461 / 0.1077 / 0.1480|-0.0170|-0.0521|-0.0486|0.0000|0.0606|-0.0625|False|sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|sequence_shuffle|KILL|
|XAU|F9|4|4299|0.0401|-0.0675|-0.1751|-0.2527|0.0449 / 0.0985 / 0.1445|-0.1003|-0.0589|-0.0675|0.0000|0.0606|-0.0754|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|5|4163|0.0641|-0.0442|-0.1524|-0.2479|0.0448 / 0.0990 / 0.1446|-0.0927|-0.0417|-0.0442|0.0000|0.0606|-0.0537|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|6|3596|0.0363|-0.0737|-0.1836|-0.2467|0.0447 / 0.0996 / 0.1451|-0.1116|-0.0582|-0.0737|0.0000|0.0606|-0.0861|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|7|3464|0.0603|-0.0506|-0.1616|-0.2602|0.0452 / 0.1009 / 0.1453|-0.0872|-0.0402|-0.0506|0.0000|0.0606|-0.0656|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|8|1818|0.0495|-0.0251|-0.0996|-0.2535|0.0243 / 0.0500 / 0.0924|-0.0183|-0.0079|-0.0251|0.0000|0.0606|-0.0372|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|9|1776|0.0644|-0.0091|-0.0826|-0.2333|0.0242 / 0.0499 / 0.0924|-0.0210|0.0145|-0.0091|0.0007|0.0606|-0.0247|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|10|1734|0.0417|-0.0331|-0.1079|-0.2346|0.0239 / 0.0498 / 0.0917|-0.0108|-0.0052|-0.0331|0.0000|0.0606|-0.0429|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|11|1690|0.0612|-0.0130|-0.0872|-0.2431|0.0242 / 0.0498 / 0.0906|0.0220|0.0203|-0.0130|0.0004|0.0606|-0.0205|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|12|1266|0.0632|-0.0105|-0.0843|-0.2281|0.0235 / 0.0487 / 0.0893|-0.0545|0.0052|-0.0105|0.0007|0.0606|-0.0258|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|13|1225|0.0821|0.0077|-0.0668|-0.2179|0.0235 / 0.0485 / 0.0893|-0.0283|0.0296|0.0077|0.0068|0.0606|-0.0082|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|14|1115|0.0380|-0.0360|-0.1101|-0.2375|0.0244 / 0.0485 / 0.0901|0.0188|0.0056|-0.0360|0.0000|0.0606|-0.0523|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F9|15|1080|0.0485|-0.0256|-0.0997|-0.2485|0.0244 / 0.0481 / 0.0892|0.0455|0.0332|-0.0256|0.0001|0.0606|-0.0432|False|random_entry_95, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|0|3864|0.0211|-0.0781|-0.1774|-0.2595|0.0371 / 0.0890 / 0.1430|-0.0937|-0.0554|-0.0781|0.0000|0.0000|-0.0846|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|1|3728|0.0432|-0.0572|-0.1575|-0.2337|0.0376 / 0.0902 / 0.1432|-0.0750|-0.0384|-0.0572|0.0000|0.0000|-0.0656|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|2|3512|0.0194|-0.0796|-0.1787|-0.2548|0.0370 / 0.0889 / 0.1436|-0.1076|-0.0523|-0.0796|0.0000|0.0000|-0.0865|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|3|3389|0.0372|-0.0629|-0.1630|-0.2299|0.0381 / 0.0902 / 0.1437|-0.0858|-0.0397|-0.0629|0.0000|0.0000|-0.0703|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|4|3325|0.0289|-0.0780|-0.1849|-0.2513|0.0444 / 0.0960 / 0.1439|-0.1255|-0.0560|-0.0780|0.0000|0.0000|-0.0864|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|5|3221|0.0519|-0.0558|-0.1635|-0.2462|0.0444 / 0.0967 / 0.1440|-0.1160|-0.0402|-0.0558|0.0000|0.0000|-0.0656|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|6|2922|0.0264|-0.0800|-0.1864|-0.2666|0.0438 / 0.0957 / 0.1441|-0.1202|-0.0551|-0.0800|0.0000|0.0000|-0.0887|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|7|2819|0.0498|-0.0575|-0.1648|-0.2601|0.0443 / 0.0965 / 0.1444|-0.1136|-0.0401|-0.0575|0.0000|0.0000|-0.0661|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|8|1098|0.0645|-0.0077|-0.0800|-0.2156|0.0231 / 0.0475 / 0.0918|0.0535|0.0026|-0.0077|0.0010|0.0000|-0.0150|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|9|1074|0.0804|0.0073|-0.0659|-0.2067|0.0232 / 0.0477 / 0.0915|0.0648|0.0328|0.0073|0.0063|0.0000|-0.0022|False|random_entry_95, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|10|988|0.0644|-0.0082|-0.0809|-0.2301|0.0230 / 0.0481 / 0.0917|0.0783|0.0086|-0.0082|0.0010|0.0000|-0.0185|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|11|968|0.0815|0.0081|-0.0654|-0.2156|0.0232 / 0.0482 / 0.0910|0.0930|0.0376|0.0081|0.0065|0.0000|-0.0033|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|12|972|0.0581|-0.0173|-0.0927|-0.2123|0.0238 / 0.0492 / 0.0892|0.0484|0.0133|-0.0173|0.0003|0.0000|-0.0260|False|random_entry_95, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|13|936|0.0774|0.0015|-0.0744|-0.2055|0.0238 / 0.0493 / 0.0892|0.0704|0.0363|0.0015|0.0033|0.0000|-0.0101|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|14|843|0.0789|0.0035|-0.0718|-0.2136|0.0240 / 0.0487 / 0.0904|0.0400|0.0182|0.0035|0.0041|0.0000|-0.0067|False|random_entry_95, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F10|15|812|0.0976|0.0219|-0.0537|-0.2004|0.0241 / 0.0487 / 0.0903|0.0673|0.0353|0.0219|0.0193|0.0000|0.0071|True|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x|random_entry_95|KILL|
|XAU|F11|0|2901|0.0050|-0.1040|-0.2130|-0.2921|0.0460 / 0.1017 / 0.1449|0.0090|-0.0745|-0.1040|0.0000|0.2762|-0.1138|False|random_entry_95, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|1|1732|-0.0116|-0.1208|-0.2301|-0.2888|0.0467 / 0.1014 / 0.1454|-0.0085|-0.0688|-0.1208|0.0000|0.2762|-0.1318|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|2|1924|0.0030|-0.1069|-0.2168|-0.2894|0.0489 / 0.1035 / 0.1451|-0.0333|-0.0699|-0.1069|0.0000|0.2762|-0.1198|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|3|1165|0.0058|-0.1050|-0.2158|-0.2743|0.0505 / 0.1033 / 0.1454|-0.0134|-0.0626|-0.1050|0.0000|0.2762|-0.1209|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|4|2292|-0.0206|-0.1262|-0.2317|-0.2971|0.0456 / 0.0927 / 0.1425|-0.0298|-0.0642|-0.1262|0.0000|0.2762|-0.1368|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|5|385|-0.0157|-0.1215|-0.2274|-0.2635|0.0459 / 0.0962 / 0.1425|-0.0853|-0.0323|-0.1215|0.0000|0.2762|-0.1346|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|6|1085|-0.0210|-0.1264|-0.2319|-0.2897|0.0467 / 0.0932 / 0.1434|-0.0333|-0.0600|-0.1264|0.0000|0.2762|-0.1426|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|7|94|0.0267|-0.0838|-0.1942|-0.1628|0.0502 / 0.0961 / 0.1426|-0.1020|0.0416|-0.0838|0.0000|0.2762|-0.1113|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|8|1441|0.0087|-0.0597|-0.1281|-0.2576|0.0237 / 0.0487 / 0.0909|-0.0083|-0.0235|-0.0597|0.0000|0.2762|-0.0708|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|9|580|0.0338|-0.0377|-0.1091|-0.2417|0.0231 / 0.0483 / 0.0918|0.1816|0.0070|-0.0377|0.0000|0.2762|-0.0529|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|10|1175|-0.0050|-0.0727|-0.1404|-0.2512|0.0237 / 0.0483 / 0.0892|0.0086|-0.0157|-0.0727|0.0000|0.2762|-0.0791|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|11|388|0.0574|-0.0151|-0.0877|-0.2177|0.0231 / 0.0490 / 0.0902|0.3020|0.0071|-0.0151|0.0008|0.2762|-0.0295|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|12|1133|0.0117|-0.0550|-0.1218|-0.2414|0.0243 / 0.0487 / 0.0855|-0.1102|-0.0109|-0.0550|0.0000|0.2762|-0.0680|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|13|104|0.1171|0.0393|-0.0384|-0.1966|0.0263 / 0.0476 / 0.0774|-0.5079|0.0572|0.0393|0.0123|0.2762|0.0115|True|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x|random_entry_95|KILL|
|XAU|F11|14|827|0.0022|-0.0650|-0.1322|-0.2554|0.0243 / 0.0483 / 0.0862|-0.0100|-0.0069|-0.0650|0.0000|0.2762|-0.0765|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F11|15|15|-0.0087|-0.0797|-0.1507|-0.2612|0.0211 / 0.0433 / 0.0727|-1.0367|0.2493|-0.0797|0.0007|0.2762|-0.1626|False|sample_floor, random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|sample_floor|KILL|
|XAU|F12|0|5622|0.0402|-0.0745|-0.1892|-0.2756|0.0464 / 0.1069 / 0.1479|-0.0552|-0.0711|-0.0745|0.0000|0.0903|-0.0855|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|1|5380|0.0680|-0.0476|-0.1631|-0.2551|0.0464 / 0.1079 / 0.1480|-0.0036|-0.0500|-0.0476|0.0000|0.0903|-0.0605|False|sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|sequence_shuffle|KILL|
|XAU|F12|2|3230|0.0251|-0.0742|-0.1735|-0.2041|0.0381 / 0.0791 / 0.1374|-0.0988|-0.0451|-0.0742|0.0000|0.0903|-0.0834|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|3|3204|0.0291|-0.0702|-0.1696|-0.2031|0.0382 / 0.0791 / 0.1373|-0.0970|-0.0299|-0.0702|0.0000|0.0903|-0.0789|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|4|5638|0.0269|-0.0878|-0.2024|-0.2821|0.0462 / 0.1071 / 0.1479|-0.0607|-0.0691|-0.0878|0.0000|0.0903|-0.0968|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|5|5409|0.0398|-0.0755|-0.1908|-0.2821|0.0464 / 0.1080 / 0.1479|-0.0433|-0.0507|-0.0755|0.0000|0.0903|-0.0835|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|6|3294|0.0072|-0.0920|-0.1911|-0.2226|0.0383 / 0.0794 / 0.1375|-0.0505|-0.0464|-0.0920|0.0000|0.0903|-0.0964|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|7|3274|0.0126|-0.0866|-0.1858|-0.2236|0.0383 / 0.0793 / 0.1374|-0.0507|-0.0352|-0.0866|0.0000|0.0903|-0.0920|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|8|5408|0.0456|-0.0595|-0.1645|-0.2517|0.0466 / 0.0951 / 0.1454|-0.0117|-0.0623|-0.0595|0.0000|0.0903|-0.0686|False|confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|confirmation_firewall|KILL|
|XAU|F12|9|5244|0.0639|-0.0413|-0.1465|-0.2540|0.0469 / 0.0950 / 0.1454|0.0087|-0.0455|-0.0413|0.0000|0.0903|-0.0506|False|sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|sequence_shuffle|KILL|
|XAU|F12|10|3145|0.0278|-0.0864|-0.2005|-0.2392|0.0457 / 0.0927 / 0.1453|-0.1015|-0.0528|-0.0864|0.0000|0.0903|-0.0936|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|11|3097|0.0335|-0.0810|-0.1956|-0.2488|0.0457 / 0.0929 / 0.1454|-0.0969|-0.0373|-0.0810|0.0000|0.0903|-0.0894|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|12|5473|0.0274|-0.0774|-0.1821|-0.2641|0.0466 / 0.0950 / 0.1454|-0.1031|-0.0615|-0.0774|0.0000|0.0903|-0.0806|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|13|5275|0.0413|-0.0631|-0.1675|-0.2511|0.0469 / 0.0950 / 0.1455|-0.0971|-0.0473|-0.0631|0.0000|0.0903|-0.0661|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|14|3192|-0.0063|-0.1172|-0.2281|-0.2648|0.0455 / 0.0928 / 0.1452|-0.1133|-0.0593|-0.1172|0.0000|0.0903|-0.1242|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|15|3169|0.0035|-0.1076|-0.2187|-0.2567|0.0456 / 0.0929 / 0.1453|-0.1016|-0.0363|-0.1076|0.0000|0.0903|-0.1162|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|16|1735|0.0408|-0.0328|-0.1063|-0.2441|0.0239 / 0.0497 / 0.0906|0.0043|-0.0070|-0.0328|0.0000|0.0903|-0.0425|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|17|1693|0.0571|-0.0171|-0.0912|-0.2567|0.0240 / 0.0496 / 0.0909|0.0262|0.0177|-0.0171|0.0002|0.0903|-0.0260|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|18|1602|0.0565|-0.0139|-0.0844|-0.2054|0.0239 / 0.0484 / 0.0887|-0.0659|-0.0065|-0.0139|0.0003|0.0903|-0.0273|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|19|1555|0.0709|-0.0013|-0.0735|-0.2382|0.0237 / 0.0483 / 0.0889|-0.0882|0.0222|-0.0013|0.0024|0.0903|-0.0120|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|20|1765|0.0247|-0.0476|-0.1199|-0.2567|0.0241 / 0.0501 / 0.0931|-0.0366|-0.0071|-0.0476|0.0000|0.0903|-0.0566|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|21|1705|0.0515|-0.0210|-0.0936|-0.2411|0.0238 / 0.0500 / 0.0932|-0.0720|0.0171|-0.0210|0.0001|0.0903|-0.0297|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|22|1610|0.0235|-0.0430|-0.1095|-0.2497|0.0238 / 0.0488 / 0.0902|-0.0013|-0.0045|-0.0430|0.0000|0.0903|-0.0542|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|23|1573|0.0396|-0.0286|-0.0968|-0.2411|0.0238 / 0.0488 / 0.0902|0.0534|0.0236|-0.0286|0.0000|0.0903|-0.0403|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|24|1702|0.0368|-0.0356|-0.1081|-0.2393|0.0243 / 0.0487 / 0.0857|0.0530|-0.0071|-0.0356|0.0000|0.0903|-0.0447|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|25|1665|0.0597|-0.0131|-0.0860|-0.2172|0.0245 / 0.0484 / 0.0856|0.0641|0.0194|-0.0131|0.0004|0.0903|-0.0276|False|random_entry_95, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|26|1576|0.0671|-0.0034|-0.0740|-0.2148|0.0242 / 0.0479 / 0.0846|0.2447|-0.0020|-0.0034|0.0017|0.0903|-0.0115|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|27|1530|0.0742|0.0035|-0.0673|-0.2214|0.0238 / 0.0481 / 0.0844|0.2581|0.0170|0.0035|0.0045|0.0903|-0.0045|False|random_entry_95, sequence_shuffle, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|28|1735|-0.0043|-0.0741|-0.1438|-0.2570|0.0241 / 0.0492 / 0.0857|-0.1865|-0.0096|-0.0741|0.0000|0.0903|-0.0815|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|29|1686|0.0222|-0.0477|-0.1176|-0.2523|0.0241 / 0.0490 / 0.0856|-0.1529|0.0216|-0.0477|0.0000|0.0903|-0.0572|False|random_entry_95, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|30|1590|0.0084|-0.0574|-0.1231|-0.2546|0.0241 / 0.0477 / 0.0852|-0.0513|-0.0002|-0.0574|0.0000|0.0903|-0.0664|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|
|XAU|F12|31|1558|0.0218|-0.0450|-0.1118|-0.2331|0.0242 / 0.0479 / 0.0851|-0.0115|0.0143|-0.0450|0.0000|0.0903|-0.0546|False|random_entry_95, sequence_shuffle, confirmation_firewall, dsr, haircut, cost_2x, loyo, xau_seam|random_entry_95|KILL|

## First-failing-gate attribution

Evaluated 160 configurations; 0 survived. Histogram: `confirmation_firewall`=4, `random_entry_95`=118, `sample_floor`=4, `sequence_shuffle`=7, `year_concentration`=27.

## CSCV PBO matrices

### BTC F9 (PBO `0.4000`)

|Config|2018|2019|2020|2021|2022|2023|
|---:|---:|---:|---:|---:|---:|---:|
|0|-0.0736|-0.1588|0.0223|-0.0145|-0.0482|-0.0908|
|1|-0.0707|-0.1300|0.0142|0.0014|-0.0254|-0.0490|
|2|0.0549|-0.0976|0.0440|-0.0345|-0.0023|-0.0964|
|3|0.0432|-0.0718|0.0825|-0.0403|0.0269|-0.0612|
|4|-0.0872|-0.1175|-0.0163|-0.0062|-0.0932|-0.0654|
|5|-0.0827|-0.1024|-0.0148|-0.0121|-0.0758|-0.0636|
|6|-0.0132|-0.0929|-0.0885|0.0182|0.0239|-0.0618|
|7|-0.0017|-0.0992|-0.0621|0.0415|0.0583|-0.0410|
|8|-0.0061|-0.0923|-0.0118|-0.0348|-0.0060|-0.0086|
|9|0.0109|-0.0478|-0.0264|-0.0248|0.0256|0.0398|
|10|0.0051|-0.1713|-0.0698|0.0264|-0.0295|0.0302|
|11|-0.0281|-0.2155|-0.0591|0.0574|-0.0481|0.0599|
|12|0.0717|-0.0752|-0.0578|-0.0483|-0.0404|-0.0030|
|13|0.0361|-0.0797|-0.0400|-0.0299|-0.0646|0.0036|
|14|-0.0667|-0.1510|-0.1036|-0.0695|0.0131|-0.0814|
|15|-0.0806|-0.1707|-0.0725|-0.0569|-0.0170|-0.0648|

### BTC F10 (PBO `0.1500`)

|Config|2018|2019|2020|2021|2022|2023|
|---:|---:|---:|---:|---:|---:|---:|
|0|-0.0662|-0.0027|0.0024|-0.0455|-0.1675|-0.0831|
|1|-0.0917|0.0162|0.0028|-0.0330|-0.1414|-0.0709|
|2|-0.1004|-0.0464|-0.0617|-0.0541|-0.1391|-0.1127|
|3|-0.1272|-0.0239|-0.0778|-0.0443|-0.1157|-0.1080|
|4|-0.0525|-0.0806|0.1301|-0.0650|-0.1694|-0.0796|
|5|-0.1160|-0.0651|0.1437|-0.0539|-0.1432|-0.0651|
|6|-0.0585|-0.0972|0.1283|-0.0662|-0.1421|-0.0973|
|7|-0.1445|-0.0951|0.1237|-0.0530|-0.1105|-0.0920|
|8|-0.0438|0.1735|0.0401|-0.0872|-0.0880|-0.0015|
|9|-0.0424|0.1903|0.0516|-0.0927|-0.0844|-0.0108|
|10|-0.0101|0.0410|0.0511|-0.1304|-0.1337|-0.0271|
|11|-0.0006|0.0892|0.0640|-0.1356|-0.1357|-0.0398|
|12|-0.0715|0.0333|-0.0062|-0.1010|-0.0695|-0.0567|
|13|-0.0860|0.0961|0.0001|-0.0772|-0.0588|-0.0208|
|14|-0.0679|0.0251|-0.0674|-0.1524|-0.0499|-0.0805|
|15|-0.1140|0.0950|-0.0625|-0.1319|-0.0309|-0.0621|

### BTC F11 (PBO `0.2000`)

|Config|2018|2019|2020|2021|2022|2023|
|---:|---:|---:|---:|---:|---:|---:|
|0|-0.1677|-0.0766|-0.1804|-0.0523|-0.0787|-0.2157|
|1|-0.0644|-0.0395|-0.1447|-0.0413|-0.1455|-0.2666|
|2|-0.1052|-0.1948|-0.2356|-0.0685|-0.0028|-0.2398|
|3|-0.0707|-0.2380|-0.0830|-0.0192|-0.1487|-0.1751|
|4|-0.4162|-0.2550|-0.1529|-0.0259|-0.0499|-0.2150|
|5|-0.5780|-0.8258|0.0000|-0.0045|-0.1253|-0.0086|
|6|-0.4109|-0.2415|-0.0801|-0.0402|0.0001|-0.2381|
|7|-0.4325|0.0000|0.0000|-0.1645|-0.0725|-0.0979|
|8|-0.0671|-0.0959|-0.0626|0.0292|-0.0154|-0.0651|
|9|0.0023|0.0499|0.1730|0.0631|-0.0371|-0.0100|
|10|-0.1422|0.0370|-0.1450|0.1071|0.0310|-0.0763|
|11|-0.2131|0.1235|0.1489|0.1704|-0.0273|0.0025|
|12|0.0278|-0.0674|-0.2745|0.0577|0.0157|-0.0992|
|13|-0.0382|0.7220|-0.3589|0.1681|-0.1719|0.0364|
|14|-0.0833|-0.0595|-0.1945|0.0699|-0.0602|-0.0716|
|15|0.0000|0.0000|-0.1348|0.2746|0.0167|0.0406|

### BTC F12 (PBO `0.8500`)

|Config|2018|2019|2020|2021|2022|2023|
|---:|---:|---:|---:|---:|---:|---:|
|0|-0.1945|-0.0596|-0.0073|-0.0854|-0.0445|-0.1052|
|1|-0.1906|-0.0598|-0.0440|-0.0786|-0.0381|-0.1073|
|2|0.0382|-0.1210|-0.0480|0.0148|-0.0402|-0.0531|
|3|0.0224|-0.0588|-0.0062|0.0256|-0.0145|-0.0420|
|4|-0.0666|-0.2177|-0.1828|0.0229|-0.1272|-0.0807|
|5|-0.0497|-0.2014|-0.2068|0.0327|-0.0755|-0.0851|
|6|-0.1108|-0.2366|-0.1643|-0.0100|-0.0660|-0.1309|
|7|-0.1411|-0.2456|-0.1382|-0.0263|-0.0875|-0.1363|
|8|-0.2028|-0.1328|-0.1062|-0.0602|-0.1616|-0.0637|
|9|-0.1898|-0.1328|-0.0701|-0.0297|-0.1425|-0.0734|
|10|-0.0508|-0.1956|-0.0219|-0.0566|-0.1169|-0.2054|
|11|-0.0519|-0.1664|-0.0023|-0.0529|-0.1280|-0.1918|
|12|-0.0527|0.0752|-0.1038|0.0133|-0.0223|-0.0613|
|13|-0.0680|0.0619|-0.0910|0.0470|0.0043|-0.0958|
|14|-0.1216|-0.1148|-0.1564|-0.0419|-0.0303|-0.0382|
|15|-0.1373|-0.0213|-0.1281|-0.0297|-0.0085|-0.0111|
|16|-0.0414|0.0561|-0.3239|-0.0577|0.0317|-0.0410|
|17|-0.0698|0.1084|-0.3060|-0.0578|0.0361|-0.0004|
|18|0.0753|-0.1486|-0.0019|0.0562|-0.0550|-0.0577|
|19|0.0545|-0.1479|0.0194|0.0602|-0.0660|-0.0084|
|20|-0.0988|-0.0420|0.1227|0.0873|0.0203|-0.1254|
|21|-0.0869|-0.0264|0.1240|0.0870|0.0375|-0.1089|
|22|-0.2748|0.0701|-0.1192|0.1048|-0.0506|-0.0076|
|23|-0.2446|0.0567|-0.0842|0.0986|-0.0619|0.0066|
|24|-0.0760|0.1227|-0.0657|0.0453|-0.0781|-0.0896|
|25|-0.0760|0.1722|-0.0326|0.0517|-0.0932|-0.0755|
|26|-0.0115|-0.1404|0.1822|0.0235|-0.0968|-0.0232|
|27|-0.0281|-0.1375|0.2172|0.0355|-0.1041|0.0026|
|28|-0.1068|-0.1552|-0.0126|0.0500|0.0016|-0.0837|
|29|-0.1124|-0.1446|0.0130|0.0782|-0.0031|-0.0670|
|30|-0.1710|0.0539|-0.2358|0.0202|0.0765|-0.0764|
|31|-0.1547|0.0446|-0.2425|0.0289|0.0331|-0.1026|

### XAU F9 (PBO `0.0606`)

|Config|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021|2022|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|0|-0.0780|-0.0199|-0.1062|0.0736|-0.0626|-0.1436|-0.1249|-0.1201|-0.1789|-0.0751|0.0558|-0.0881|-0.0355|
|1|-0.0605|-0.0213|-0.0810|0.0830|-0.0404|-0.1145|-0.0920|-0.1007|-0.1674|-0.1091|0.0495|-0.0385|-0.0285|
|2|-0.1574|-0.0455|-0.1021|0.0080|-0.1043|-0.1084|-0.1540|-0.0936|-0.1601|-0.0606|0.0550|-0.0939|-0.0164|
|3|-0.1254|0.0039|-0.0674|0.0307|-0.0801|-0.0931|-0.1283|-0.0811|-0.1537|-0.0632|0.0986|-0.0584|-0.0019|
|4|-0.1240|-0.0510|-0.0524|0.0158|-0.0742|-0.1355|-0.1023|-0.0986|-0.1312|-0.1320|0.0119|-0.1023|0.0044|
|5|-0.0963|-0.0204|-0.0173|0.0573|-0.0465|-0.1288|-0.0969|-0.0952|-0.1212|-0.1072|0.0496|-0.0803|0.0211|
|6|-0.1709|-0.0973|-0.0592|0.0601|-0.0901|-0.1166|-0.1152|-0.1096|-0.1038|-0.1202|-0.0267|-0.0503|-0.0141|
|7|-0.1363|-0.0671|-0.0460|0.1098|-0.0742|-0.1076|-0.0934|-0.1023|-0.0926|-0.0972|-0.0063|-0.0221|0.0048|
|8|-0.0313|0.1266|-0.0454|-0.0330|-0.0200|-0.0953|0.0174|-0.0140|-0.0625|-0.0569|0.0099|-0.1076|-0.0086|
|9|-0.0483|0.1840|-0.0254|0.0476|0.0630|-0.1167|0.0043|-0.0021|-0.1191|-0.0753|0.0478|-0.0803|0.0052|
|10|0.0278|0.0886|-0.0677|-0.0076|-0.0539|-0.0326|-0.0816|-0.0072|-0.1346|-0.0973|0.0085|-0.0855|0.0119|
|11|0.0058|0.0615|0.0119|0.0308|0.0097|0.0780|-0.0624|-0.0552|0.0289|-0.1464|0.0474|-0.1385|-0.0377|
|12|-0.0840|0.0701|-0.0551|0.0039|0.0625|-0.0785|0.0083|0.0360|-0.0941|0.0102|0.1693|-0.0731|-0.1123|
|13|-0.0522|0.0967|0.0051|0.0450|0.0727|-0.0724|0.0214|0.0324|-0.0954|0.0264|0.1943|-0.0778|-0.0934|
|14|-0.1771|0.0580|-0.1001|-0.0830|0.0515|-0.0514|0.0353|-0.0284|-0.0748|0.0667|0.1641|-0.1314|-0.1733|
|15|-0.1622|0.0606|-0.0617|-0.0613|0.0704|-0.0386|0.0144|-0.0206|-0.0711|0.0833|0.1894|-0.1453|-0.1557|

### XAU F10 (PBO `0.0000`)

|Config|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021|2022|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|0|-0.1360|-0.0314|-0.0237|-0.0407|-0.0945|-0.0895|-0.1240|-0.1395|-0.1654|-0.1012|-0.0094|-0.0888|-0.0313|
|1|-0.1058|0.0026|0.0048|-0.0081|-0.0820|-0.0933|-0.1092|-0.1463|-0.1588|-0.0775|0.0319|-0.0613|-0.0190|
|2|-0.1529|-0.0560|-0.0809|-0.0223|-0.0600|-0.1334|-0.0988|-0.1161|-0.1553|-0.0937|-0.0142|-0.0928|-0.0067|
|3|-0.1292|-0.0250|-0.0599|-0.0053|-0.0354|-0.1274|-0.0952|-0.1257|-0.1454|-0.0690|0.0154|-0.0679|-0.0041|
|4|-0.1484|-0.0972|-0.0894|0.0072|-0.0515|-0.1509|-0.0832|-0.1037|-0.1476|-0.1148|0.0069|-0.0710|-0.0323|
|5|-0.1274|-0.0604|-0.0620|0.0547|-0.0372|-0.1424|-0.0759|-0.0949|-0.1374|-0.0973|0.0294|-0.0464|-0.0062|
|6|-0.1704|-0.1160|-0.1005|-0.0500|-0.0280|-0.1994|-0.0708|-0.0816|-0.0944|-0.0996|0.0082|-0.0653|-0.0033|
|7|-0.1462|-0.0662|-0.0909|-0.0115|-0.0062|-0.1787|-0.0539|-0.0748|-0.0801|-0.0863|0.0282|-0.0294|0.0022|
|8|-0.1159|0.0210|-0.0410|0.0372|-0.0174|0.0211|0.0220|0.0542|-0.0486|-0.0140|0.0821|-0.0649|-0.0299|
|9|-0.1097|0.0548|-0.0380|0.0741|-0.0102|-0.0122|0.0368|0.0634|-0.0392|-0.0026|0.1263|-0.0480|0.0078|
|10|-0.0564|0.0561|-0.1013|0.1169|0.0635|0.0191|-0.0238|0.0504|-0.0749|-0.0144|0.0483|-0.1135|-0.0961|
|11|-0.0348|0.1001|-0.1042|0.1500|0.0709|-0.0115|-0.0068|0.0455|-0.0645|-0.0065|0.1187|-0.1209|-0.0491|
|12|-0.1337|0.0319|-0.0660|0.0040|-0.0518|-0.0363|0.0398|0.0133|-0.0505|0.0644|0.0857|-0.0429|-0.0842|
|13|-0.1213|0.0156|-0.0278|0.0437|-0.0293|-0.0350|0.0571|0.0302|-0.0505|0.0737|0.1414|-0.0282|-0.0405|
|14|-0.0509|0.0573|-0.1130|0.1478|0.0778|0.0093|0.0529|0.0150|-0.0838|0.0843|0.1173|-0.1076|-0.1706|
|15|-0.0345|0.0364|-0.0751|0.2215|0.0818|-0.0060|0.0709|0.0397|-0.0820|0.1169|0.1817|-0.0995|-0.1577|

### XAU F11 (PBO `0.2762`)

|Config|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021|2022|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|0|-0.0002|-0.1186|-0.0687|-0.2103|-0.1905|-0.0162|-0.1481|-0.1378|-0.0988|-0.0696|-0.1014|-0.0504|-0.1315|
|1|0.0027|-0.1005|-0.1472|-0.2446|-0.2752|-0.0496|-0.1437|-0.1751|-0.0704|-0.0744|-0.0447|-0.1133|-0.1228|
|2|0.0366|-0.1253|-0.0895|-0.2169|-0.1169|0.0499|-0.1913|-0.1721|-0.1207|-0.0145|-0.1686|-0.0379|-0.1506|
|3|0.0833|-0.0058|-0.1257|-0.2375|-0.1513|-0.0052|-0.2013|-0.1585|0.0056|-0.0250|-0.1596|-0.0874|-0.1495|
|4|-0.0151|-0.1318|-0.1127|-0.1909|-0.1459|-0.1101|-0.1539|-0.1577|-0.1096|-0.1593|-0.1498|-0.1224|-0.0977|
|5|0.0359|-0.3576|-0.2240|-0.0464|-0.1090|-0.2455|-0.1744|-0.1988|-0.0154|0.0714|-0.0092|-0.2131|0.0080|
|6|0.0587|-0.2154|-0.0753|-0.2148|-0.0795|-0.0000|-0.1401|-0.2310|-0.1572|-0.1380|-0.0977|-0.1610|-0.1866|
|7|0.1639|-0.2498|-0.3499|-0.1648|-0.1615|-0.3170|0.2791|-0.2540|0.6231|0.1180|0.1473|-0.2958|0.1520|
|8|-0.1878|-0.0987|0.0285|-0.0769|-0.0821|-0.0002|-0.0143|-0.1427|-0.0894|-0.0490|-0.0903|-0.0457|0.0704|
|9|-0.0455|-0.0336|-0.0115|-0.0066|-0.0479|0.0997|0.0078|-0.0333|-0.0984|-0.1562|-0.2303|-0.0312|0.1437|
|10|-0.1277|-0.0401|-0.0477|-0.1043|-0.0791|0.0024|-0.1514|-0.1524|-0.0870|-0.0694|-0.0938|0.0084|-0.0062|
|11|0.0628|0.1371|-0.1021|-0.0123|-0.0736|0.1769|-0.1727|-0.1536|-0.1606|-0.0199|-0.0983|0.1348|0.0470|
|12|-0.1095|-0.1050|0.1090|0.0150|-0.1082|-0.1775|-0.1296|-0.1085|0.0192|-0.0132|-0.0791|-0.0433|0.0175|
|13|0.2713|0.5555|-0.4519|-0.0244|0.1052|0.0273|-0.1612|-0.0402|0.2529|-0.3519|-0.1093|0.2860|0.3127|
|14|0.0433|-0.2281|0.0745|-0.1292|-0.0621|-0.0069|-0.1043|-0.2218|0.0084|-0.1316|-0.0867|-0.0278|0.0462|
|15|0.0411|0.7938|0.0000|0.0000|-0.0387|0.0000|0.0151|1.0799|-0.1560|0.0000|-0.3088|-0.5762|0.0000|

### XAU F12 (PBO `0.0903`)

|Config|2010|2011|2012|2013|2014|2015|2016|2017|2018|2019|2020|2021|2022|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|0|-0.1761|-0.0332|-0.1001|0.0268|-0.1109|-0.1031|-0.1559|-0.0916|-0.1666|-0.0752|0.0406|-0.0872|-0.0117|
|1|-0.1338|0.0179|-0.0681|0.0460|-0.0988|-0.0902|-0.1288|-0.0721|-0.1620|-0.0767|0.0886|-0.0556|0.0172|
|2|-0.0442|-0.0116|0.0129|-0.0260|-0.1370|-0.1354|-0.1131|-0.1270|-0.2631|-0.0819|0.0262|-0.0509|-0.0876|
|3|-0.0492|0.0009|0.0219|-0.0061|-0.1273|-0.1300|-0.1170|-0.1247|-0.2629|-0.0765|0.0243|-0.0419|-0.0961|
|4|0.0112|-0.1257|-0.0277|-0.1785|-0.1283|-0.1064|-0.0707|-0.1307|-0.1036|-0.1124|-0.1204|-0.0236|-0.0667|
|5|0.0144|-0.0928|-0.0318|-0.1889|-0.1033|-0.0917|-0.0809|-0.1190|-0.0825|-0.0756|-0.1016|-0.0046|-0.0503|
|6|-0.0929|-0.1461|-0.1177|-0.1006|-0.1283|-0.0741|-0.0686|-0.1532|-0.0229|-0.1172|-0.0839|-0.0469|-0.0433|
|7|-0.0876|-0.1458|-0.1197|-0.0809|-0.1126|-0.0678|-0.0480|-0.1458|-0.0274|-0.1155|-0.1024|-0.0476|-0.0262|
|8|-0.1110|-0.0450|-0.0654|-0.0261|-0.0800|-0.0961|-0.0398|-0.1041|-0.1514|-0.0515|0.0356|-0.0688|-0.0381|
|9|-0.0963|-0.0383|-0.0298|-0.0124|-0.0626|-0.0916|-0.0098|-0.0836|-0.1471|-0.0253|0.0540|-0.0440|-0.0219|
|10|-0.0707|-0.0108|-0.0601|-0.0676|-0.1631|-0.1486|-0.1502|-0.0488|-0.2275|-0.0713|-0.0622|-0.0285|-0.0861|
|11|-0.0605|0.0073|-0.0554|-0.0527|-0.1757|-0.1358|-0.1467|-0.0490|-0.2284|-0.0533|-0.0651|-0.0281|-0.0829|
|12|-0.0634|-0.0682|-0.0507|-0.0941|-0.0788|-0.0894|-0.0537|-0.1556|-0.1198|-0.1097|-0.1031|-0.0447|-0.0470|
|13|-0.0631|-0.0484|-0.0482|-0.0687|-0.0679|-0.0646|-0.0291|-0.1340|-0.0911|-0.0921|-0.0858|-0.0456|-0.0395|
|14|-0.1740|-0.1552|-0.1814|-0.0981|-0.0873|-0.0940|-0.0926|-0.2356|-0.0241|-0.1577|-0.1071|-0.0843|-0.0449|
|15|-0.1701|-0.1432|-0.1784|-0.0885|-0.0774|-0.0918|-0.0777|-0.2239|0.0028|-0.1493|-0.1100|-0.0763|-0.0181|
|16|0.0523|0.0882|-0.1300|-0.0164|-0.1118|-0.0811|-0.0382|-0.0445|-0.0606|-0.0868|0.0622|-0.0458|-0.0097|
|17|0.0920|0.0615|-0.0591|-0.0127|0.0093|-0.0279|-0.0151|-0.0606|-0.0557|-0.0804|0.0877|-0.0770|-0.0787|
|18|-0.0757|0.1478|-0.0144|0.0255|-0.0933|0.0297|0.0477|0.0188|-0.1297|-0.0406|0.0100|-0.1111|0.0055|
|19|-0.0607|0.1283|0.0244|0.0293|-0.0643|0.0111|0.0653|0.0432|-0.1220|0.0445|-0.0153|-0.0853|-0.0131|
|20|-0.0563|-0.0858|0.0025|-0.0433|0.0387|0.0614|-0.1155|-0.1124|-0.0560|-0.1270|-0.0331|0.0417|-0.1288|
|21|0.0558|-0.0775|0.0514|0.0454|0.0345|-0.0219|-0.0876|-0.1037|-0.0247|-0.0479|0.0000|0.0848|-0.1822|
|22|-0.0355|-0.0938|-0.0307|0.0844|-0.0477|-0.1012|-0.1423|-0.1530|-0.1132|-0.0843|0.0009|0.0620|0.0963|
|23|-0.0304|-0.0563|0.0398|0.0914|-0.0149|-0.1678|-0.1083|-0.1392|-0.1682|-0.0293|-0.0075|0.0963|0.1175|
|24|0.0004|0.0718|-0.0715|0.0628|-0.1031|-0.0194|-0.0410|0.0244|-0.2119|-0.1427|0.0016|-0.0860|0.0516|
|25|0.0240|0.1030|-0.0375|0.1564|-0.0627|-0.0297|0.0287|0.1091|-0.2100|-0.1397|-0.0430|-0.1070|0.0419|
|26|-0.0786|0.0881|0.0555|0.0210|-0.1096|0.0415|0.0542|0.0844|-0.1028|-0.0996|0.0449|-0.1302|0.0947|
|27|-0.0793|0.0738|0.0100|0.0353|-0.0679|0.0649|0.1035|0.0856|-0.1041|-0.0929|0.0547|-0.1210|0.0943|
|28|-0.0315|-0.1618|0.0151|-0.1214|-0.0435|-0.1632|-0.0642|-0.1210|0.0185|-0.0993|-0.0579|0.0091|-0.1349|
|29|-0.0337|-0.0966|0.0316|-0.1134|0.0212|-0.1541|-0.0039|-0.1826|0.0730|-0.0314|-0.0758|0.0442|-0.0874|
|30|0.0123|-0.1654|-0.0851|0.0013|-0.0242|-0.1289|-0.1185|-0.1530|-0.0593|0.0079|-0.0566|0.0534|-0.0257|
|31|-0.0045|-0.1415|-0.0453|0.0233|-0.0058|-0.0725|-0.1413|-0.1785|-0.0296|0.0674|-0.0335|0.0728|-0.0872|

## Controls auditor

**PASS.** Every random threshold is based on 200 tape replays with matched empirical holding and risk distributions, stop/target execution, XAU nightly swaps, and full provisional costs. Every shuffle threshold uses 200 permutations of the realized net trade sequence. The corrupt-data smoke test rejects duplicated timestamps.

## Leakage auditor

**PASS.** Detector rolling inputs are shifted to completed prior bars, verified by prefix/shift audits. Complete decision bars decide at close and execute next open. Walk-forward selection is development-only and confirmation is isolated.

## Statistical auditor

**PASS.** DSR uses full ledger multiplicity. CSCV PBO, LOYO, sample floors, year concentration, the 0.70 win haircut, and confirmation firewall fail closed.

## Cost and execution auditor

**PASS.** Entry cost/stop is capped at 0.15 and its realized distribution is reported. Stops, targets, and maximum holdings are fixed at entry. Base and 2x provisional costs are tested. XAU swaps are charged per UTC night and both sides of the 2017 seam must pass. BTC 4h records the `LOCK_A` funding evidence gap. Weekend-spanning policies are `SWING_REQUIRED`.

## Trial and reproducibility auditor

**PASS.** All 160 configurations are in the SHA-256 hash-chained ledger with the grid and session-map hashes. The 2,000-config cap is respected.

## Holdout seal

**PASS.** The holdout seal audit passed immediately before and after the gauntlet; no holdout shard or boundary was opened.

## Phase 4 disposition

No candidate survived Phase 3, so FTMO lifecycle optimization was not run. This is the mandated empty-set branch, not a skipped survivor evaluation.
