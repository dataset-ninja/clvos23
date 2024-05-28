The authors proposed the **CLVOS23: A Long Video Object Segmentation Dataset for Continual Learning** - new long-video object segmentation dataset for continual learning, as a realistic and significantly greater challenge for testing VOS(Video Object Segmentation) methods on long videos. The frames for dataset were taken from the [Long Videos dataset](https://www.kaggle.com/datasets/gvclsu/long-videos)(**_rat_**, **_dressage_**, **_blueboy_** videos) and from the YouTube (**_car_**, **_dog_**, **_parkour_**, **_skating_**, **_skiing_**, **_skiing-long_** videos).

## Motivation

The goal of Video Object Segmentation (VOS) is to accurately extract a target object at the pixel level from each frame of a given video. VOS solutions are generally divided into two categories: semi-supervised (or one-shot) VOS, where ground-truth masks of the target objects are provided for at least one frame during inference, and unsupervised VOS, where the model has no prior knowledge about the objects.

In semi-supervised VOS, online approaches update part of the VOS model based on evaluated frames and estimated masks. The idea is that videos contain relevant information beyond just the current frame's mask, which a model can leverage by learning during the evaluation process. However, online model learning raises questions about how effectively the model adapts from frame to frame, especially when new frames differ significantly from the initial ground-truth frame. This challenge falls under the domain of continual learning, a type of machine learning where a model is trained on a sequence of tasks and is expected to continuously improve its performance on each new task while maintaining its ability to perform well on previously learned tasks.

Current state-of-the-art semi-supervised and online VOS methods excel on short videos, typically a few seconds or up to 100 frames long, as seen in datasets like [DAVIS16](https://davischallenge.org/), [DAVIS17](https://davischallenge.org/), and [YouTube-VOS18](https://youtube-vos.org/). However, these methods often struggle to maintain performance on long videos, such as those found in the [Long Videos dataset](https://www.kaggle.com/datasets/gvclsu/long-videos). This issue has not been thoroughly investigated or addressed within the VOS field, particularly through the lens of continual learning.

Continual learning methods are usually evaluated on classification datasets like [MNIST](http://yann.lecun.com/exdb/mnist/), [CIFAR10](https://www.cs.toronto.edu/~kriz/cifar.html), and [ImageNet](https://www.image-net.org/), or on datasets specifically designed for continual learning, such as [Core50](https://vlomonaco.github.io/core50/). In these scenarios, the classification dataset is presented to the model as a sequential data stream in online continual learning methods. Unlike these datasets and testing scenarios, long video object segmentation has numerous real-world applications, including video summarization, human-computer interaction, and autonomous vehicles, which necessitate robust performance over extended sequences.

## Dataset description

In the ideal case, where the samples in a video sequence are independent and identically distributed (i.i.d.), machine learning problems are made significantly easier, since there is then no need to handle distributional drift and temporal dependency in VOS. However, i.i.d. assumption is not valid in video data.

The dataset consisted of three long sequences with a total of 7411 frames. The i.i.d. assumption is invalid for "dressage" videos due to the significant distribution drifts that occur, which align more closely with the non-i.i.d. assumptions of continual learning. This new continual learning-based interpretation of long video sequences is being discussed for the first time in the context of VOS and continual learning. The [Long Videos dataset](https://www.kaggle.com/datasets/gvclsu/long-videos) currently selects evaluation label masks uniformly, failing to adequately test how well a VOS solution handles sudden shifts in the target’s appearance. The authors propose an alternative approach: annotating frames for evaluation based on the distribution drifts occurring in each video sequence.

<img src="https://github.com/dataset-ninja/clvos23/assets/120389559/901b7f3a-9e3c-45ec-ac9b-693f1c9fc664" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">A subset of frames from “dressage” video of the Long Videos dataset. The video consists of 23 sub-chunks that are separated from each other by significant distributional drifts or discontinuities. The lower (sparse) row, in each set, show the annotated frames. The annotations provided by are shown without a border, whereas the annotated masks added via this paper, and made available via the
CLVOS23 dataset, are shown with blue borders. The four sub-chunks that are missing from the Long Videos dataset are encircled in red.</span>

Image above shows 23 sub-chunks of videos in the “dressage” video of the Long Videos dataset. Each sub-chunk is separated from its previous and next sub-chunks based on the distribution drifts. When an online or offline event, such as a sports competition, is recorded using multiple cameras, these distribution drifts are common in mediaprovided videos. As a result, in the authors proposed dataset, they first utilize the following strategy to select candidate frames for annotation and evaluation.

- They select the first frame of each sub-chunk S. It is interesting to see how VOS models handle the distribution drift that happens in the sequence, which is arriving a new task in continual learning.
- The last frame of each sequence is also selected. The first frame ground truth label mask is given to the model as it is set in the semi-supervised VOS scenario.
- One frame from the middle of each sub-chunk is also selected for being annotated.

For CLVOS23, in addition to the 3 videos from the Long Videos dataset, the authors added the other 6 videos form YouYube. All frames of the 6 new added videos are extracted with the rate of 15 Frames Per Second (FPS). To ensure that all distribution drifts are captured, the authors only annotate the first frame of each sub-chunk in the Long Videos dataset and add them to the uniformly selected annotated frames. The proposed dataset has following advantages over the Long Videos dataset.

- It added 5951 frames to 7411 frames of the Long Videos dataset.
- CLVOS23 increased the number of annotation frames from 63 in the Long Videos dataset to 284.
- It increases the number of videos from 3 to 9.
- The selected annotated frames are chosen based on the distribution drift that happens in the videos (subchunks) rather than being uniformly selected.

| Video name  | #Sub-chunks (tasks) | #Frames | #Annotated frames |
| ----------- | ------------------- | ------- | ----------------- |
| dressage    | 23                  | 3589    | 43                |
| blueboy     | 27                  | 2406    | 47                |
| rat         | 22                  | 1416    | 42                |
| car         | 18                  | 1109    | 37                |
| dog         | 12                  | 891     | 25                |
| parkour     | 24                  | 1578    | 49                |
| skating     | 5                   | 778     | 11                |
| skiing      | 5                   | 692     | 11                |
| skiing-long | 9                   | 903     | 19                |

<span style="font-size: smaller; font-style: italic;">Each video sequence’s specifications in the proposed CLVOS23 dataset. The first three videos (Dressage, Blueboy, and Rat) are taken directly from the Long Videos dataset and the authors added additional annotated ground-truth frames to each of them to make them more appropriate for continual learning.</span>

It is worth noting that for a long VOS dataset, it is very expensive and sometimes unnecessary to annotate all the frames of videos for evaluation. It is worth mentioning that the authors utilized the [Toronto Annotation Suite](https://keymakr.com/) to annotate the selected frames for evaluation. The frames of new 6 videos were resized to have a height of 480 pixels. The width of each frame is defined as proportionate to its height.
