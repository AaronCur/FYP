from numpy import exp, array, random, dot

#The training set. We have 4 examples,
#and 1 output value.
training_set_inputs = array([[0,0,1],[1,1,1],[1,0,1],[0,1,1]])
training_set_oututs = array([[0,1,1,0]]).T

class NeuralNetwork():
    def __init__(self):

        #Now before going further, we need to initialise the weights
        #w1 w2 w2 to some random values to start with.

        random.seed(1)

        #We model a single neuron, with 3 input connections and 1 output connection.
        #We assign random weights to a 3 x 1 matrix, with values in the range -1 to 1
        # and mean 0

        self.synaptic_weights = 2 * random.random((3,1)) - 1

    #The sigmoid function, whihc describes an S shaped curve
    #We pass the weighted sum of the inputs through this fucntion
    #To normailise them betweem 0 and 1

    def __sigmoid(self, x):
        return 1/ (1 + exp(-x))

    #Next we define the derivative of the sigmoid function in order
    #to update the weights using gradient decent


    #The derivative of the Sigmoid function.
    #This is the gradient of the sigmoid curve
    #It indicates how confident we are about the exisitng weight

    def __sigmoid_derivative(self, x):
        return x * (1 - x)




    #We train the neural network through a process of trial and error
    #Adjusting the synaptic weights each time
    def train(self, training_set_inputs, training_set_oututs, number_of_trianing_iterations):
        for iteration in range(number_of_trianing_iterations):
                #Pass the training set through our neural network ( a single neuron).
                output = self.think(training_set_inputs)

                #Calculate the error (The difference between the desired output
                #and prected output)
                error = training_set_oututs - output

                #Multiply the error by the input and again by the gradient of the sigmoid curves
                #This means less confident weights and adjust more
                #this means inputs, which are zero, do not cause changes to the weights
                adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))

                #Adjust the weights
                self.synaptic_weights += adjustment

    #The neural network thinks
    def think(self, inputs):
        #Pass inputs through our nerual network (our single neuron)
        #Back probagation
        return self.__sigmoid(dot(inputs, self.synaptic_weights))

if __name__ == "__main__":

    #initialise a single neuron neural network
    neural_network = NeuralNetwork()

    print ("Random starting synaptic weights: ")
    print (neural_network.synaptic_weights)

    #The training set. We have 4 examples, each consisting of 3 input values
    #and 1 output values
    training_set_inputs = array([[0,0,1], [1,1,1], [1,0,1], [0,1,1]])
    training_set_oututs = array([[0, 1, 1, 0]]).T

    #Train the neural network using a training set
    #Do it 10,000 times and make small adjustments each time
    neural_network.train(training_set_inputs, training_set_oututs, 10000)

    print("New synaptic weights after training: ")
    print(neural_network.synaptic_weights)

    #Test the neural network with a new situation
    print("Considering new situation [1,0,0] -> ?: ")
    print(neural_network.think(array([1,1,0])))
