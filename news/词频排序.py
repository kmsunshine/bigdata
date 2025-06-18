import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['KaiTi']
with open(r'C:\Users\康萌\Desktop\bigdata\bigdata\词频统计结果\out.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
dic = {}
for line in lines[:-1]:
    lk = line.strip("\n").split()
    dic[lk[0]] = dic.get(lk[0],int(lk[1]))
li = list(dic.items())
li.sort(key=lambda x:x[1],reverse=True)
print('词频前5：',li[:5])
print("-------------------------------------------------")
print('词频前10：',li[:10])
print("-------------------------------------------------")
print('词频前20：',li[:20])
print("-------------------------------------------------")
print('词频前50：',li[:50])

top_items = li[:20]
words = [item[0] for item in top_items]
frequencies = [item[1] for item in top_items]

# 创建水平条形图
plt.figure(figsize=(12, 10))
y_pos = range(len(words))
plt.barh(y_pos, frequencies, align='center')
plt.yticks(y_pos, words)
plt.xlabel('词频')
plt.title('词频统计Top20')
plt.gca().invert_yaxis()  # 最高频的词在顶部
plt.tight_layout()
plt.savefig('词频统计_Top20.png', dpi=300, bbox_inches='tight')
plt.show()