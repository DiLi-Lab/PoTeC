# aufruf: python umwandlung.py <dateienliste> <versionenanzahl>
import sys, random


def ausgabe(*xs):
    for x in xs:
        #  if str.lstrip(str(x))=="": print(str(x),end='')
        #  pass
        print(str(x), end='')


def ausgabe2(xs):
    if str.lstrip(xs) != "": xs = str.lstrip(xs)
    for x in xs:
        ausgabe(x + "*")
    ausgabe("\t")


def untag(xs):
    y = ""
    no = False
    for x in xs:
        if x == "[":
            no = True
        elif x == "]":
            no = False
        elif no == False:
            y = y + x
    return y


ausgabe(
    "Version\tItemId\tTopic\tText\tHeadline\tT_Q1\tT_Q1_Button1\tT_Q1_Button2\tT_Q1_Button3\tT_Q1_Button4\tT_Q2\tT_Q2_Button1\tT_Q2_Button2\tT_Q2_Button3\tT_Q2_Button4\tT_Q3\tT_Q3_Button1\tT_Q3_Button2\tT_Q3_Button3\tT_Q3_Button4\tB_Q1\tB_Q1_Button1\tB_Q1_Button2\tB_Q1_Button3\tB_Q1_Button4\tB_Q2\tB_Q2_Button1\tB_Q2_Button2\tB_Q2_Button3\tB_Q2_Button4\tB_Q3\tB_Q3_Button1\tB_Q3_Button2\tB_Q3_Button3\tB_Q3_Button4\tOrder_BQs\tOrder_TQs\tOrder_BQ1Ans\t\tOrder_BQ2Ans\tOrder_BQ3Ans Order_TQ1Ans\tOrder_TQ2Ans\tOrder_TQ3Ans\tcorrAns_TQ1\tcorrAns_TQ2\tcorrAns_TQ3\tcorrAns_BQ1\tcorrAns_BQ2\tcorrAns_BQ3\ttrial\n")
dateien = sys.argv[1:-1]
for version in range(int(sys.argv[-1])):
    trial = 1
    random.shuffle(dateien)
    for datei in dateien:
        topic = "physik"
        if datei[0] == 'b':
            topic = "bio"
        itemID = datei[-6:-4]  # textid
        f = open(datei, 'r')
        text = f.read()
        f.close()
        # (headline, textbody, _, _, _, fragen[0],antworten[0][0],antworten[0][1],antworten[0][2],antworten[0][3],fragen[1],antworten[1][0],antworten[1][1],antworten[1][2],antworten[1][3],fragen[2],antworten[2][0],antworten[2][1],antworten[2][2],antworten[2][3],_,fragen[3],antworten[3][0],antworten[3][1],antworten[3][2],antworten[3][3],fragen[4],antworten[4][0],antworten[4][1],antworten[4][2],antworten[4][3],fragen[5],antworten[5][0],antworten[5][1],antworten[5][2],antworten[5][3])=text.split('\n')
        textteile = text.split('\n')
        headline = textteile[0]
        textbody = textteile[1]
        fragen = textteile[5:18:5] + textteile[21:34:5]
        antworten = [textteile[6:10], textteile[11:15], textteile[16:20], textteile[22:26], textteile[27:31],
                     textteile[32:36]]
        Order_BQs = 0  # tun wir nicht
        Order_TQs = 0  # tun wir nicht
        order = [1, 2, 3, 4]
        random.shuffle(order)
        Order_BQ1Ans = order.copy()  # 4231 die erste antwortmoeglichkeit wurde als 4. gezeigt, die 2. als 2. usw
        antworten[3] = [antworten[3][i - 1] for i in Order_BQ1Ans]
        #  corrAns_BQ1=Order_BQ1Ans[0]+2	#an welcher stelle wurde die korrekte (=1.) Antwort gezeigt
        corrAns_BQ1 = Order_BQ1Ans.index(1) + 3
        order = [1, 2, 3, 4]
        random.shuffle(order)
        Order_BQ2Ans = order.copy()
        antworten[4] = [antworten[4][i - 1] for i in Order_BQ2Ans]
        corrAns_BQ2 = Order_BQ2Ans.index(1) + 3
        order = [1, 2, 3, 4]
        random.shuffle(order)
        Order_BQ3Ans = order.copy()
        antworten[5] = [antworten[5][i - 1] for i in Order_BQ3Ans]
        corrAns_BQ3 = Order_BQ3Ans.index(1) + 3
        order = [1, 2, 3, 4]
        random.shuffle(order)
        Order_TQ1Ans = order.copy()
        antworten[0] = [antworten[0][i - 1] for i in Order_TQ1Ans]
        corrAns_TQ1 = Order_TQ1Ans.index(1) + 3
        order = [1, 2, 3, 4]
        random.shuffle(order)
        Order_TQ2Ans = order.copy()
        antworten[1] = [antworten[1][i - 1] for i in Order_TQ2Ans]
        corrAns_TQ2 = Order_TQ2Ans.index(1) + 3
        order = [1, 2, 3, 4]
        random.shuffle(order)
        Order_TQ3Ans = order.copy()
        antworten[2] = [antworten[2][i - 1] for i in Order_TQ3Ans]
        corrAns_TQ3 = Order_TQ3Ans.index(1) + 3
        ausgabe(version, "\t", itemID, "\t", topic, "\t")
        ausgabe2(untag(textbody))
        ausgabe(untag(headline), "\t")
        #  corr=[corrAns_BQ1, corrAns_BQ2, corrAns_BQ3, corrAns_TQ1, corrAns_TQ2, corrAns_TQ3]
        for i in range(len(fragen)):
            ausgabe2(fragen[i])
            for antwort in antworten[i]:
                ausgabe2(antwort)
        #   print(antworten[i][corr[i]-3])
        ausgabe(Order_BQs, "\t", Order_TQs, "\t", Order_BQ1Ans, "\t", Order_BQ2Ans, "\t", Order_BQ3Ans, "\t",
                Order_TQ1Ans, "\t", Order_TQ2Ans, "\t", Order_TQ3Ans, "\t", corrAns_TQ1, "\t", corrAns_TQ2, "\t",
                corrAns_TQ3, "\t", corrAns_BQ1, "\t", corrAns_BQ2, "\t", corrAns_BQ3, "\t", trial, "\n")
        trial = trial + 1
