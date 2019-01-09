import input_data

mnist = input_data.read_data_sets("data/", one_hot = True)

import tensorflow as tf

#Set parameters
learning_rate = 0.01
training_iteration = 30
batch_size = 100
display_step = 2

#TF graph input
x = tf.placeholder("float", [None, 784]) # mnist data image of shape 28*28=784
y = tf.placeholder("float", [None, 10]) # 0-9 digits recognition => 10 classes

#Create a model

#Set model wreights
w = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable (tf.zeros([10]))

with tf.name_scope("Wx_b") as scope:
    #Construct linear model
    model = tf.nn.softmax(tf.matmul(x,w) + b)

#Add summary ops to collect data
w_h = tf.summary.histogram("Weights", w)
b_h = tf.summary.histogram("biases", b)

#More name scopes will clean up graph representaion
with tf.name_scope("cost_function") as scope:
    #Minimize error using cross entropy
    #Cross entropy
    cost_function = - tf.reduce_sum(y*tf.log(model))
    #Create a summary to monitor the cost function
    tf.summary.scalar("cost_function", cost_function)

with tf.name_scope("train") as scope:
    #Gradiant decent
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

#Init the variables
init = tf.initialize_all_variables()

#merge all summaries into a single operator
merged_summary_op = tf.summary.merge_all()


#Lauch the graph
with tf.Session() as sess:
    sess.run(init)

    #Set logs writer to folder
    summary_writer = tf.summary.FileWriter('C:\College\Year4\FYP\Tutorials\Image Classifier', sess.graph)

    #Training cycle
    for iteration in range(training_iteration):
        avg_cost = 0
        total_batch = int(mnist.train.num_examples/batch_size)

        #loop over all batches
        for i in range(total_batch):
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            #fit training using batch data
            sess.run(optimizer, feed_dict={x: batch_xs, y:batch_ys})
            #compute the average loss
            avg_cost += sess.run(cost_function, feed_dict = {x: batch_xs, y: batch_ys}) / total_batch
            #write logs for each iteration
            summary_str = sess.run(merged_summary_op, feed_dict = {x: batch_xs, y: batch_ys})
            summary_writer.add_summary(summary_str, iteration * total_batch + i)
        # Display logs per iteration
        if iteration % display_step ==0:
            print ("Iteration", '%04d' % (iteration + 1), "cost=","{:.9f}".format(avg_cost))
