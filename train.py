"""
Train our RNN on extracted features or images.
"""
from exp_config_reader import *
import keras
from keras import backend as K
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger, LearningRateScheduler
from models import ResearchModels
from data import DataSet
import datetime
import os.path
import math


class LRTensorBoard(TensorBoard):
    def __init__(self, log_dir): # add other arguments to __init__ if you need
        super().__init__(log_dir=log_dir)

    def on_epoch_end(self, epoch, logs=None):
        logs.update({'lr': K.get_value(self.model.optimizer.lr)})
        super().on_epoch_end(epoch, logs)


def train(data_type, seq_length, model, saved_model=None,
          class_limit=None, image_shape=None,
          load_to_memory=False, batch_size=32, nb_epoch=100):
    # str of time
    current_datetime = datetime.datetime.now()
    str_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Helper: Save the model.
    checkpoint_path = os.path.join('data', 'checkpoints',
                                   EXP_NAME + '-' + model + '-' + data_type + \
                                   '.{epoch:03d}-{val_loss:.3f}' + '-' + str_datetime + '.hdf5')
    checkpointer = ModelCheckpoint(
        filepath=checkpoint_path,
        verbose=1,
        save_best_only=True)

    # Helper: Schedule learning rate decay
    def step_decay(epoch):
        initial_lr = INIT_LEARNING_RATE
        lr_drop_ratio = LR_DROP_RATIO
        epochs_drop = EPOCHS_DROP
        lr = initial_lr * math.pow(lr_drop_ratio, math.floor((1+epoch)/epochs_drop))
        return lr
    learning_rate = LearningRateScheduler(step_decay)

    # Helper: TensorBoard
    # tb = TensorBoard(log_dir=os.path.join('data', 'logs', EXP_NAME + str_datetime))
    tb = LRTensorBoard(log_dir=os.path.join('data', 'logs', EXP_NAME + str_datetime))

    # Helper: Save results.
    log_path = os.path.join('data',
                            'logs',
                            EXP_NAME + '-' + 'training-' + str_datetime + '.log')
    csv_logger = CSVLogger(log_path)

    # Helper: Stop when we stop learning.
    early_stopper = EarlyStopping(patience=PATIENTS)

    # Get the data and process it.
    if image_shape is None:
        data = DataSet(
            seq_length=seq_length,
            class_limit=class_limit
        )
    else:
        data = DataSet(
            seq_length=seq_length,
            class_limit=class_limit,
            image_shape=image_shape
        )

    # Get samples per epoch.
    # Multiply by 0.7 to attempt to guess how much of data.data is the train set.
    steps_per_epoch = (len(data.data) * 0.7) // batch_size

    if load_to_memory:
        # Get data.
        X, y = data.get_all_sequences_in_memory('train', data_type)
        X_test, y_test = data.get_all_sequences_in_memory('test', data_type)
    else:
        # Get generators.
        generator = data.frame_generator(batch_size, 'train', data_type)
        val_generator = data.frame_generator(batch_size, 'test', data_type)

    # Get the model.
    rm = ResearchModels(len(data.classes), model, seq_length, saved_model)

    # Get the optimizer:
    if OPTIMIZER == 'SGD':
        optimizer = keras.optimizers.SGD(lr=INIT_LEARNING_RATE, momentum=MOMENTUM, nesterov=False)
    elif OPTIMIZER == 'RMSProp':
        optimizer = keras.optimizers.RMSprop(lr=INIT_LEARNING_RATE, epsilon=None)
    elif OPTIMIZER == 'Adam':
        optimizer = keras.optimizers.Adam(lr=INIT_LEARNING_RATE, beta_1=0.9, beta_2=0.999, epsilon=None, amsgrad=False)

    rm.model.compile(loss=LOSS_FUNCTION, optimizer=optimizer, metrics=['accuracy'])

    # Fit!
    if load_to_memory:
        # Use standard fit.
        rm.model.fit(
            X,
            y,
            batch_size=batch_size,
            validation_data=(X_test, y_test),
            verbose=1,
            callbacks=[tb, early_stopper, csv_logger, learning_rate],
            epochs=nb_epoch)
    else:
        # Use fit generator.
        rm.model.fit_generator(
            generator=generator,
            steps_per_epoch=steps_per_epoch,
            epochs=nb_epoch,
            verbose=1,
            callbacks=[tb, early_stopper, csv_logger, checkpointer, learning_rate],
            validation_data=val_generator,
            validation_steps=40,
            workers=4)

def main():
    """These are the main training settings. Set each before running
    this file."""
    # model can be one of lstm, lrcn, mlp, conv_3d, c3d
    model = MODEL
    saved_model = SAVED_MODEL  # None or weights file
    class_limit = None  # int, can be 1-101 or None
    seq_length = SEQ_LENGTH
    load_to_memory = bool(LOAD_TO_MEMORY)  # pre-load the sequences into memory
    batch_size = BATCH_SIZE # The original batch_size = 32

    # Chose images or features and image shape based on network.
    if model in ['conv_3d', 'c3d', 'lrcn']:
        data_type = 'images'
        image_shape = (80, 80, 3)
    elif model in ['lstm', 'mlp']:
        data_type = 'features'
        image_shape = None
    else:
        raise ValueError("Invalid model. See train.py for options.")

    train(data_type, seq_length, model, saved_model=saved_model,
          class_limit=class_limit, image_shape=image_shape,
          load_to_memory=load_to_memory, batch_size=batch_size, nb_epoch=MAX_EPOCH)

if __name__ == '__main__':
    main()
