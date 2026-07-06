import pandas as pd
import sys
import os

# Берём путь из аргумента или используем по умолчанию
if len(sys.argv) > 1:
    jtl_path = sys.argv[1]
else:
    jtl_path = "report/result.jtl"

# Проверяем, что файл есть
if not os.path.exists(jtl_path):
    print(f"Файл не найден: {jtl_path}")
    print("Сначала запусти тест: jmeter -n -t test-plan.jmx -l report/result.jtl")
    sys.exit(1)

# Читаем JTL
df = pd.read_csv(jtl_path)

# Считаем метрики
total = len(df)
errors = df[df['success'] == False]
p50 = df['elapsed'].quantile(0.50)
p95 = df['elapsed'].quantile(0.95)
p99 = df['elapsed'].quantile(0.99)
avg = df['elapsed'].mean()
max_time = df['elapsed'].max()
min_time = df['elapsed'].min()
throughput = total / (df['timeStamp'].max() - df['timeStamp'].min()) * 1000

# Считаем по типам запросов
labels = df['label'].unique()

print("=" * 50)
print("РЕЗУЛЬТАТЫ НАГРУЗОЧНОГО ТЕСТИРОВАНИЯ")
print("=" * 50)
print(f"Всего запросов:       {total}")
print(f"Успешных:             {total - len(errors)}")
print(f"Ошибок:               {len(errors)} ({(len(errors)/total)*100:.2f}%)")
print(f"Throughput (средний): {throughput:.1f} req/s")
print()
print("ВРЕМЯ ОТКЛИКА (мс):")
print(f"  Минимум:            {min_time:.0f}")
print(f"  Среднее:            {avg:.0f}")
print(f"  Медиана (p50):      {p50:.0f}")
print(f"  95-й процентиль:    {p95:.0f}")
print(f"  99-й процентиль:    {p99:.0f}")
print(f"  Максимум:           {max_time:.0f}")
print()
print("ПО ТИПАМ ЗАПРОСОВ:")
for label in sorted(labels):
    subset = df[df['label'] == label]
    err_count = len(subset[subset['success'] == False])
    print(f"  {label}: {len(subset)} запросов, ошибок: {err_count}, среднее: {subset['elapsed'].mean():.0f} мс")
print("=" * 50)

# Оценка результата
error_rate = len(errors) / total * 100
if error_rate == 0 and p95 < 500:
    print("✅ ТЕСТ ПРОЙДЕН: 0 ошибок, 95-й процентиль в SLA (< 500 мс)")
elif error_rate < 1 and p95 < 1000:
    print("⚠️  ТЕСТ ПРОЙДЕН С ЗАМЕЧАНИЯМИ: ошибки или рост времени ответа")
else:
    print("❌ ТЕСТ ПРОВАЛЕН: ошибок > 1% или время ответа > 1000 мс")
