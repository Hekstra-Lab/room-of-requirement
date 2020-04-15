import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow_probability import distributions as tfd
from tensorflow_probability import bijectors as tfb
from tqdm import tqdm


#This script shows how to conduct stochastic variational inference on the variational gaussian
#process object from tensorflow probability. In this model, each training step is conducted
#on a subset of the the data. The number of examples in the training step is controlled by 
#batch_size.

dtype = tf.float64
train_steps=1000
num_inducing_points = 100
batch_size=100
gridpoints = 1000

grid_x,grid_y = np.vstack(np.meshgrid(
    np.linspace(-10, 10, gridpoints),
    np.linspace(-10, 10, gridpoints),
)).reshape((2, gridpoints**2))


# y is the array of values at each x
y = np.sin(grid_x)*np.sin(grid_y/10.)

# X represents the full set of points for which we have 
# measured values
X = np.vstack((grid_x,grid_y)).T

if dtype == tf.float32:
    X = X.astype(np.float32)
    y = y.astype(np.float32)


# These are kernel parameters. We will use an automatic relevance determining rbf kernel
amplitude = tfp.util.TransformedVariable(
    tf.Variable(1., dtype=dtype), tfb.Softplus(), dtype=dtype, name='amplitude')
length_scale = tfp.util.TransformedVariable(
    tf.Variable(tf.ones(2, dtype=dtype)), tfb.Softplus(), dtype=dtype, name='length_scale')

#The FeatureScaled object is how you create ARD kernels in tfp
kernel = tfp.math.psd_kernels.FeatureScaled(
        tfp.math.psd_kernels.ExponentiatedQuadratic(amplitude=amplitude), 
        length_scale
    )


#This is the overall amount of noise associated with each y-value
#This is called β^{-1} in the Hensman paper. In practice, this could
#be tuned or learned.
observation_noise_variance = tfp.util.TransformedVariable(
    1., tfb.Softplus(), dtype=dtype, name='observation_noise_variance')

#Randomly select datapoints from X in order to initialize the inducing point
#locations, Z
idx = np.random.choice(np.arange(X.shape[0]), num_inducing_points, replace=False)
Z = tf.Variable(X[idx], dtype=dtype)

#These are closed form expressions from Hensman for the parameters of the variational
#distribution. Using these means that the parameters of the variational distribution 
#do not need to be learned separately.
#In my opinion this hould not be a static method of this class but rather a separate
#function entirely. What's more this should happen automatically when this class
#is instantiated. 
#In Hensman, these two are called m and S
variational_loc, variational_scale = (
    tfd.VariationalGaussianProcess.optimal_variational_posterior(
        kernel=kernel,
        inducing_index_points=Z,
        observation_index_points=X,
        observations=y,
        observation_noise_variance=observation_noise_variance,
    )
)

#Now we construct the actual vgp we're going to use
vgp = tfp.distributions.VariationalGaussianProcess(
	kernel, 
	X, 
	Z, 
	variational_loc, 
        variational_scale,
        observation_noise_variance=observation_noise_variance,
)

opt=tf.keras.optimizers.Adam(0.1)

@tf.function
def train_step(batch_y, batch_X):
    with tf.GradientTape() as tape:
       loss = vgp.variational_loss(batch_y, batch_X)
    gradients = tape.gradient(loss, vgp.trainable_variables)
    opt.apply_gradients(zip(gradients, vgp.trainable_variables))
    return float(loss), vgp.inducing_index_points

losses = [vgp.variational_loss(y)]
inducing_points = [vgp.inducing_index_points.numpy()]
for i in tqdm(range(train_steps)):
    idx = np.random.randint(0, len(y), size=batch_size)
    loss, points  = train_step(y[idx], X[idx])
    losses.append(loss)
    inducing_points.append(points.numpy())

inducing_points = np.array(inducing_points)

plot_points=10000
idx = np.random.randint(0, len(grid_x), plot_points)

plt.figure()
plt.subplot(121)
plt.title("Ground Truth")
plt.tricontourf(grid_x[idx], grid_y[idx], y[idx], 100)

plt.subplot(122)
plt.title("Variational GP Model")
plt.tricontourf(grid_x[idx], grid_y[idx], vgp.mean().numpy()[idx], 100)
for i in range(num_inducing_points):
    plt.plot(*inducing_points[:,i,:].T, 'w', scalex=False, scaley=False,)
for i in range(num_inducing_points):
    plt.plot(*inducing_points[-1,i,:].T, 'wo', scalex=False, scaley=False)

plt.figure()
plt.plot(losses)
plt.xlabel("-Evidence Lower BOund")
plt.xlabel("Iteration")
plt.semilogy()
plt.show()
