# Object-Counter
## Motivation
In this project, we are interested in building a neural network model that counts the number of objects in a picture. 
The user can gather their own images with a cell phone and augment them with the pipeline discussed in this project. Currently, we have focused 
on oranges in a relatively plain background. The project can be extended to incorporate more complex backgrounds and 
mixture of objects. 

## Data Augmentation Methods
This is an image classification task with 10 classes. We start with about 100 images that we have gathered with
a cellphone in each class. The initial dataset is extremely insufficient for the model the detect the differences
between 3 versus 4 oranges in a picture. To remediate this deficiency, we first conduct a "manual" augmentation technique
by stitching two images together and placing it in the appropriate class. For instance, if we stitch an image from class 1
with an image from class 3 we end up with a new image in class 4. The manual augmentation will naturally results in 
an imbalanced dataset with higher number classes containing more images (there are more permutations for class 10 than class 2 for instance). 
We subsequently compensate for the class imbalance by creating additional images using an "automatic" approach.<br/>

