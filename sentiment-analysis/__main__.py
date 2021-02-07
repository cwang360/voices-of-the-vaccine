import tensorflow as tf
import pandas as pd
from tensorflow import keras
import numpy as np
import re


df = pd.read_csv('covidVD.csv')
df_train = df.iloc[:50000]
df_test = df.iloc[50000:]

target_train = df_train.pop('sentiment')
train_dataset = tf.data.Dataset.from_tensor_slices((df_train.values, target_train.values))

target_test = df_test.pop('sentiment')
test_dataset = tf.data.Dataset.from_tensor_slices((df_test.values, target_test.values))

for feat, targ in train_dataset.take(5):
  print ('Features: {}, Target: {}'.format(feat, targ))
for feat, targ in test_dataset.take(5):
  print('Features: {}, Target: {}'.format(feat, targ))



BUFFER_SIZE = 10000
BATCH_SIZE = 64
padded_shapes = ([None],())

train_dataset = train_dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
test_dataset = test_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
for example, label in train_dataset.take(1):
  print('texts: ', example.numpy()[:3])
  print()
  print('labels: ', label.numpy()[:3])

VOCAB_SIZE=3000
encoder = tf.keras.layers.experimental.preprocessing.TextVectorization(
    max_tokens=VOCAB_SIZE)
encoder.adapt(train_dataset.map(lambda text, label: text))
vocab = np.array(encoder.get_vocabulary())
print(vocab[:20])
encoded_example = encoder(example)[:3].numpy()
print(encoded_example)


model = tf.keras.Sequential([
    encoder,
    tf.keras.layers.Embedding(
        input_dim=len(encoder.get_vocabulary()),
        output_dim=64,
        # Use masking to handle the variable sequence lengths
        mask_zero=True),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])
history = model.fit(train_dataset, epochs=10,
                    validation_data=test_dataset,
                    validation_steps=30)
model.save('sentiment-analysis-model')

# test_loss, test_acc = model.evaluate(test_dataset)
#
# print('Test Loss: {}'.format(test_loss))
# print('Test Accuracy: {}'.format(test_acc))


sample_text = ("I wouldn't want to get the covid vaccine")
predictions = model.predict(np.array([sample_text]))
print(predictions)

sample_text = ("I wish I could get the vaccine")
predictions = model.predict(np.array([sample_text]))
print(predictions)

sample_text = ("I love the vaccine so much!")
predictions = model.predict(np.array([sample_text]))
print(predictions)


file = open('cleaned_tweets.txt', 'r')
lines = file.readlines()
count = 0
predictions = 0
lat = []
long = []
val = []
num_tweets = []
for line in lines:
    if line[0] == 'b':
        text = str(line).replace('\n', '')
        predictions += model.predict(np.array([line]))[0][0]

        # print(np.array([text]))
        count += 1
    else:
        coors = re.split(',|:' , line)
        print(coors)
        if count > 0:
            avg = predictions/count
            lat.append(coors[0])
            long.append(coors[1])
            val.append(avg)
            num_tweets.append(count)
            count = 0
            predictions = 0
print(lat)
print(long)
print(val)
print(num_tweets)
a = np.array(lat)
b = np.array(long)
c = np.array(val)
d = np.array(num_tweets)
df = pd.DataFrame({"Latitude" : a, "Longitude" : b, "Sentiment":c, "Number of Tweets": d})
df.to_csv("plotting_points.csv", index=False)