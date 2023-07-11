First I experimented by cutting the number of kernels used in the convolutional model compared to the number used in class. For my surprise, cutting in half didn't impact the accuracy that much, but significantly reduced the time to run the model.

The kernels size also impacted the results negatively by incresing it. 4x4 kernels where usually worse than 3x3 kernels.

Then I tried using MaxPooling and AveragePooling, and MaxPooling seemed better so I used it in the end. I also tried both in sequence but it didn't change much.

Using two hidden layers instead of one improved the results by a lot, and also the second layer didn't need to have as many nodes as the first one to achieve a good result.

When trying different optimizers, I could see that the best results came from "Adam", "RMSProp" and "Nadam".