import psycopg2
from sklearn.linear_model import LogisticRegression

# Docker uzerindeki PostgreSQL veritabanina baglanma
conn = psycopg2.connect(
host="host.docker.internal",
    database="postgres",
    user="postgres",
    password="secret123",
    port=5432
)
cursor = conn.cursor()

# Veritabanindan hasta verilerini cekme
cursor.execute("SELECT id, age, glucose, blood_pressure, bmi FROM patients;")
records = cursor.fetchall()

# Model egitim verisi
X_train = [
    [50, 150, 80, 32.0],
    [25, 90, 65, 22.0],
    [60, 170, 95, 35.0],
    [30, 85, 70, 24.0]
]
y_train = [1, 0, 1, 0]

# Makine ogrenmesi modelinin egitilmesi
model = LogisticRegression()
model.fit(X_train, y_train)

# Tahminleme yapilmasi ve sonuclarin veritabanina kaydedilmesi
print("[BILGI] Model tahminleme sureci basladi...")
for row in records:
    patient_id = row[0]
    features = [row[1:]]
    prediction = int(model.predict(features)[0])
    
    cursor.execute("UPDATE patients SET prediction = %s WHERE id = %s;", (prediction, patient_id))
    print(f"[BILGI] Hasta ID: {patient_id} -> Tahmin: {prediction}")

# Degisiklikleri kaydet ve baglantiyi kapat
conn.commit()
cursor.close()
conn.close()
print("[BASARILI] Tum tahminler veritabanina basariyla kaydedildi.")
