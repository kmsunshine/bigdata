
import matplotlib

import matplotlib.pyplot as plt
import pandas as pd
import jieba
from wordcloud import WordCloud
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType, FloatType
from snownlp import SnowNLP

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 创建 SparkSession
spark = SparkSession.builder.appName("Weibo Sentiment Analysis").getOrCreate()

# 1. 读取 HDFS 中的 CSV 文件
input_path = "hdfs://localhost:9000/weibo/input/weibo_comments.csv"
df = spark.read.option("header", True).csv(input_path)

# 2. 数据清洗
df = df.dropna(subset=["评论内容"])

# 3. 情感值计算
@udf(FloatType())
def get_sentiment(text):
    try:
        return float(SnowNLP(text).sentiments)
    except:
        return None

df = df.withColumn("情感值", get_sentiment(col("评论内容")))

# 4. 提取小时
@udf(StringType())
def extract_hour(text):
    try:
        import dateutil.parser
        dt = dateutil.parser.parse(text)
        return str(dt.hour)
    except:
        return None

df = df.withColumn("小时", extract_hour(col("评论时间")))

# 5. 保存清洗后数据到 HDFS
output_path = "hdfs://localhost:9000/weibo/output/processed"
df.write.mode("overwrite").option("header", True).csv(output_path)

# 6. 词云图（本地生成）
pdf = df.select("评论内容").dropna().toPandas()
text = " ".join(jieba.cut(" ".join(pdf["评论内容"].astype(str).tolist())))
wordcloud = WordCloud(font_path="/home/hadoop/simhei.ttf", background_color="white", width=800, height=400).generate(text)
wordcloud.to_file("词云图.png")
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("6月17间谍冒充大学生窃密", fontsize=18)
plt.show()

# 7. 情感分布图
sent_pdf = df.select("情感值").dropna().toPandas()
plt.figure()
plt.hist(sent_pdf["情感值"], bins=20, color='skyblue', edgecolor='black')
plt.title("微博评论情感分布")
plt.xlabel("情感值（0=负面，1=正面）")
plt.ylabel("评论数")
plt.grid(True)
plt.savefig("情感分布图.png")
plt.show()

# 8. 每小时评论数量分布图
hour_pdf = df.select("小时").dropna().toPandas()
hour_pdf["小时"] = pd.to_numeric(hour_pdf["小时"], errors='coerce')
hour_counts = hour_pdf["小时"].value_counts().sort_index()
plt.figure()
hour_counts.plot(kind="bar", color="skyblue")
plt.title("每小时评论数量分布")
plt.xlabel("小时")
plt.ylabel("评论数量")
plt.grid(True)
plt.savefig("小时评论分布图.png")
plt.show()

spark.stop()



