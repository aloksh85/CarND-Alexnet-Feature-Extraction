import pickle
import tensorflow as tf
from sklearn.model_selection import train_test_split
from alexnet import AlexNet
from  sklearn.utils import shuffle
import time
nb_classes = 43
epochs = 20
batch_size = 100
# TODO: Load traffic signs data.
with open('./train.p','rb') as f:
    data = pickle.load(f)
for key,value in data.items():
     print (key)


# TODO: Split data into training and validation sets.
X_train,X_valid,y_train,y_valid = train_test_split(data['features'],data['labels'],test_size=0.33)
print('data set stats:')
print('train set shape data: ', X_train.shape,', labels: ',y_train.shape)
print('valid set shape data: ', X_valid.shape,', labels: ',y_valid.shape)


# TODO: Define placeholders and resize operation.
x  = tf.placeholder(tf.float32,shape=(None,32,32,3))
resized =tf.image.resize_images(x,(227,227))
y = tf.placeholder(tf.int32,shape=(None))
one_hot_y = tf.one_hot(y,nb_classes)

# TODO: pass placeholder as first argument to `AlexNet`.
fc7 = AlexNet(resized, feature_extract=True)
# NOTE: `tf.stop_gradient` prevents the gradient from flowing backwards
# past this point, keeping the weights before and up to `fc7` frozen.
# This also makes training faster, less work to do!
fc7 = tf.stop_gradient(fc7)
# TODO: Add the final layer for traffic sign classification.

fc7_shape = (fc7.get_shape().as_list()[-1],nb_classes)
fc8W =tf.Variable(tf.truncated_normal(fc7_shape,mean =0.0, stddev=1e-2))
fc8b = tf.Variable(tf.zeros(nb_classes))
logits = tf.nn.xw_plus_b(fc7,fc8W,fc8b)

# TODO: Define loss, training, accuracy operations.
# HINT: Look back at your traffic signs project solution, you may
# be able to reuse some the code.
rate =0.001
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=one_hot_y)
loss_operation = tf.reduce_mean(cross_entropy)
optimizer = tf.train.AdamOptimizer(learning_rate=rate)
training_operation = optimizer.minimize(loss_operation)

correct_prediction = tf.equal(tf.argmax(logits,1),tf.argmax(one_hot_y,1))
accuracy_operation = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

# TODO: Train and evaluate the feature extraction model.
def evaluate(X_data,y_data,sess):
    num_examples = len(X_data)
    total_accuracy = 0.
    sess = tf.get_default_session()
    for offset in range(0,num_examples,batch_size):
        batch_x,batch_y=X_data[offset:offset+batch_size],y_data[offset:offset+batch_size]
        accuracy = sess.run(accuracy_operation,feed_dict={x:batch_x,y:batch_y})
        total_accuracy += (accuracy*len(batch_x))

    return total_accuracy/num_examples


with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
    sess.run(tf.global_variables_initializer())
    num_examples  = len(X_train)
    print('Start model training')
    print()
    for i in range (epochs):
        t0 = time.time()
        X_train,y_train = shuffle(X_train,y_train)
        for offset in range(0,num_examples,batch_size):
            end = offset + batch_size
            batch_x,batch_y =  X_train[offset:end],y_train[offset:end]
            sess.run(training_operation,feed_dict={x:batch_x,y:batch_y})
        
        training_accuracy =evaluate(X_train,y_train,sess)
        validation_accuracy = evaluate (X_valid,y_valid,sess)
        print("EPOCH {}...".format(i+1))
        print("time : %.3f sec" % (time.time()-t0))
        print("Training accuracy :{:.3f}".format(training_accuracy))
        print("Validation accuracy:{:.3f}".format(validation_accuracy))



