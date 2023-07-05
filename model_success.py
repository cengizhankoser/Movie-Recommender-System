import matplotlib.pyplot as plt

# Model adları, epoch değerleri, test size değerleri, RMSE ve MAE değerleri
models = ['Model 1', 'Model 2', 'Model 3', 'Model 4', 'Model 5', 'Model 6']
epochs = [45, 50, 30, 25, 30, 35]
test_sizes = [0.25, 0.25, 0.25, 0.30, 0.20, 0.10]
rmse_values = [0.9630, 0.9647, 0.9628, 0.9647, 0.9598, 0.9579]
mae_values = [0.7673, 0.7686, 0.7671, 0.7683, 0.7647, 0.7633]

# Çizgi grafiği oluşturma
fig, ax1 = plt.subplots()

ax1.plot(models, rmse_values, marker='o', label='RMSE')
ax1.plot(models, mae_values, marker='o', label='MAE')
ax1.set_xlabel('Modeller')
ax1.set_ylabel('Değerler')
ax1.set_title('RMSE ve MAE Değerleri')
ax1.legend(loc='upper left')

# Sağ tarafta epoch değerleri için ikinci eksen
ax2 = ax1.twinx()
ax2.plot(models, epochs, color='red', linestyle='--', marker='o', label='Epoch')
ax2.set_ylabel('Epoch')

# Sol tarafta test size değerleri için üçüncü eksen
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(models, test_sizes, color='green', linestyle='--', marker='o', label='Test Size')
ax3.set_ylabel('Test Size')

# Eksen etiketlerini ve y ekseni pozisyonlarını güncelleme
ax2.yaxis.label.set_color('red')
ax3.yaxis.label.set_color('green')
ax2.tick_params(axis='y', colors='red')
ax3.tick_params(axis='y', colors='green')

# Grafiği gösterme
plt.show()
