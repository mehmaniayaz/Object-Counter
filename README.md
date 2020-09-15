# Table of Contents
1. [Motivation](#motivation)
2. [Data Augmentation Methods](#augmentation)
3. [Results](#results)
4. [Conclusions](#conclusions)

## Motivation <a name="motivation"></a>
In this project, we are interested in building a neural network model that counts the number of objects in a picture. 
The user can gather their own images with a cell phone and augment them with the pipeline discussed in this project. Currently, we have focused 
on oranges in a relatively plain background. The project can be extended to incorporate more complex backgrounds and 
mixture of objects. 

## Data Augmentation Methods <a name="augmentation"></a>
Our project addresses an image classification task with 10 classes. We start with about 100 cellphone images that we have gathered 
for each class (Figure 1a). The initial dataset is extremely insufficient for the model to detect the differences
between 3 versus 4 oranges in a picture. To remediate this deficiency, we first conduct a "manual" augmentation technique
by stitching two images together and placing it in the appropriate class (Figure 1b). For instance, if we stitch an image from class 1
with an image from class 3 we end up with a new image in class 4. The manual augmentation will naturally result in 
an imbalanced dataset, with higher number classes containing more images (for example, there are more permutations to create class 10 
than there are for class 2). 

We subsequently compensate for the class imbalance by creating additional images using an "automatic" approach. The automatic approach 
comprises of image rotation, brightness manipulation, image flipping, and shearing (Figure 1c). The advantage of the manual method is that, once image
sizes are standardized, it gives the model cases with different orange sizes in a picture to learn. It furthermore, does not rely on 
image manipulation rules that the model can potentially pick up on when building  a large dataset.

![original](./disp-images/orig_IMG_6133.png "Original")
![manual](./disp-images/stitched_IMG_7024__IMG_6512.png "Manual")
![automatic](./disp-images/auto_IMG_6133___0_379.png "Autoamtic")

Figure 1:Image of oranges for class 8: original (a-left), manual (b-middle), automatic (c-right).



<img src="./disp-images/count_bar.png" width="80%"/>

Figure 2: Count bar for the final dataset. Notice that class imbalanced has been compensated with automatic image generation.

## Results <a name="results"></a>
We visualize the model's training and validation accuracy by plotting confusion matrices for both datasets (Figure3).
The training confusion matrix demonstrates considerable consistency for the accuracy of each class. This is in contrast
to the confusion matrix of the validation set that where, model's accuracy drops as number of oranges drops. A peculiar
mismatch is class 2 where all images are misclassified as class 10. I couldn't discover similarities between class 2 and class 10,
and despite running the model repeatedly and obtaining the same misclassification, I am left to determine that this issue
is due to model's inherent bias with the current dataset. 

<img src="./disp-images/training_confusionMatrix.png " width="25%"/>
<img src="./disp-images/validation_confusionMatrix.png " width="25%"/>

Figure 3: Confusion matrices for training (a-left) and validation (b-right) sets.

The history of the model's training is shown in Figure 4. We observe that the training accuracy reaches excellent accuracy
in the first epoch where as the validation accuracy drop from 70% to just above 60%. The model therefore demonstrates considerable
overfitting. However, reducing the model's complexity (using a shallower network with smaller number of parameters), droping out
parameters in a layer, and using a regularization parameter did not improve the validation sets accuracy above 70%.




<img src="./disp-images/training_validation_accuracy.png " width="60%"/>

Figure 4: History of training and validation loss and accuracy for various counter measures.





<img src="./disp-images/activation_filters.png " width="50%"/>

Figure 5: Activation filter visualization.

<img src="./disp-images/sample_image.png " width="50%"/>
<img src="./disp-images/feature_visualization1.png " width="50%"/>
<img src="./disp-images/feature_visualization2.png " width="50%"/>
<img src="./disp-images/feature_visualization3.png " width="50%"/>

Figure 6: Feature map visualization.

## Conclusions <a name="conclusions"></a>
We demonstrate that through a combination of manual and automatic data augmentation, accuracy of training and 
validation set can go up to X%. This is in contrast to a purely automatic augmentation method where the 
accuracy increases to x%. Future work will include an examination of non-ideal backgrounds and mixture of objects
of different kinds. 