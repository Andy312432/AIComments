import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import jieba

# 步驟1：載入資料
df = pd.read_csv("referance.csv")
print(df)

# 中文斷詞函數
def tokenize(text):
    return " ".join(jieba.cut(text))

# 進行斷詞處理
df['processed_text'] = df['text'].apply(tokenize)

# 步驟2：特徵萃取 (使用TF-IDF)
vectorizer = TfidfVectorizer(max_features=500000)
X = vectorizer.fit_transform(df['processed_text'])
y = df['label']

# 步驟3：建立與訓練模型
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)



# 步驟4：模型評估
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 步驟1：讀取資料
new_texts = pd.read_excel("data_all200.xlsx")

# 步驟2：前處理（斷詞）
new_texts = new_texts.dropna(subset=['內容'])
processed_texts = [tokenize(t) for t in new_texts['內容']]

# 步驟3：向量化
X_new = vectorizer.transform(processed_texts)

# 步驟4：分類預測
predictions = model.predict(X_new)

# 步驟5：儲存分類結果到原DataFrame
new_texts['分類'] = predictions

# 步驟6：儲存到新 Excel 檔
output_path = "result.xlsx"
new_texts.to_excel(output_path, index=False)
