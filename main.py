import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score
from tensorflow.keras.layers import Concatenate, Dense, Input  # type: ignore
from tensorflow.keras.models import Model  # type: ignore


def main():
    # Extract SWE data with pandas and save it as a new CSV
    df = pd.read_csv("./data/SWE_values_all.csv")
    swe_df = df[['SWE']]
    swe_df.to_csv("./my_data/swe.csv", index=False)

    # ensure we have a num py array
    X = df[['SWE']].values.astype("float32")

    # set the target equal to the output
    y = X.copy()

    # Define inputs (for testing, using a shape of 10)
    input1 = Input(shape=(1,))
    #input2 = Input(shape=(10,))

    # Process the inputs with Dense layers
    x1 = Dense(32, activation='relu')(input1)
    #x2 = Dense(32, activation='relu')(input2)

    # Concatenate the layers
    #concatenated = Concatenate()([x1, x2])

    # Output layer
    output = Dense(1, activation='sigmoid')(x1)

    # Build and compile the model using tf.keras.Model
    model = Model(inputs=[input1], outputs=output)
    model.compile(optimizer='adam', loss='binary_crossentropy')

    # train the model
    model.fit(X, y, epochs=50, batch_size=4)

    # model.summary()

    # test the model with a new input
    test_input = np.array([[123.0]])
    prediction = model.predict(test_input)
    print ("Prediction for input 123.0: ", prediction)

if __name__ == "__main__":
    main()
