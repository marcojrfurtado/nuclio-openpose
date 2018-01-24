# nuclio-openpose

This repository demonstrates how it is possible to run [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) to detect human bodies in images with nuclio. It is also a good example on how to combine nuclio and CUDA.

The instructions presented here are exclusively for local deployment (i.e. `nuctl` option `--platform local`)

## Requirements

* CUDA-enabled graphics card;

* [nuclio-cuda](https://github.com/marcojrfurtado/nuclio-cuda). Ensure all its requirements are met. Use it to build a CUDA-enabled processor and the `nuctl` tool.

### Important

Follow all instructions provided in `nuclio-cuda`. Most importantly, set the docker default runtime to `nvidia` by editing **/etc/docker/daemon.json**, and adding the line:

```
"default-runtime" : "nvidia"
```

And then restart the docker service.


## Deploy function

Simply call

```
./deploy_openpose_function_local.sh
```

I invite everyone to take a look at this script, as it is simply a one-liner that invokes the nuclio-cuda custom `nuctl` tool. The function will be deployed to the local machine.

NOTE (1): This should take several minutes, as it needs to build OpenCV 3 and OpenPose. Unless the command exited with an error, or if you are certain that the process is hanging, wait for its completion.

NOTE (2): You need at least 11GB of free storage space for deployment. Otherwise deployment will fail at any given moment.

After deployment, the command `docker images` should list an image called `openpose`.

## Invoke function

Simply call

```
./invoke_openpose.sh [Image URL]
```

The output is always in JSON format. The input expected is just an URL in plain text.

Please take a look at this script. It is a one-liner that calls `nuctl invoke`

Note: Function is optimized for landscape images


Example:

```
./invoke_openpose.sh https://resources.stuff.co.nz/content/dam/images/1/n/z/j/b/7/image.related.StuffLandscapeSixteenByNine.620x349.1nzjx5.png/1516496037265.jpg > response.json
```

## Visualizing results

The results returned by the OpenPose function in this repository are returned in JSON format.

The output format is based on the [OpenPose output definition](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md)

We output is very simple, illustrated as follows

```
{
	"persons" : list with dimensions  -> NPeople x CBodyJoints * 3
	"left_hands" : list with dimensions ->  NPeople x CHandsJoints * 3
	"right_hands" list with dimensions -> NPeople x CHandsJoints * 3
}
```

In which

* NPeople : Number of detected people;

* CBodyJoints (constant) : Number of body joints (e.g left wrist, head, etc. );

* CHandsJoints (constant) : Number of hand joints (e.g. tip of thumb, etc. );

The 3 floating-points values corresponding to each joint represent:

* X coordinate of joint, in image space;

* Y coordinate of joint, in image space;

* Confidence value for detected joint;

If joint is undetected, confidence and coordinates will be set to 0.0.

It is important to note that **persons**, **left\_hands** and **right\_hands** contain individuals in the same identification order.



### Requirements for visualization

* Python 2.7

* Pillow

I suggest to install Pillow with Pip, as follows

```
pip install Pillow
```

### Running

After invoking the openpose function, and saving its results, simply call the visualization script as follows

```
python visualize_results.py [Image URL] [Path to JSON file with results]
```

Example:

```
python visualize_results.py https://resources.stuff.co.nz/content/dam/images/1/n/z/j/b/7/image.related.StuffLandscapeSixteenByNine.620x349.1nzjx5.png/1516496037265.jpg response.json
```

Note: The visualization tool presented here is only a simple and rudimentary example on how to use and validate the JSON results. A much beter visualization is presented in the original [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) project.

#### Samples

After running the visualization program, output images will be written to **./results.png**. Here are a few samples.

![](./image_samples/sample1.jpg | width=100){:height="50%" width="50%"}

![](./image_samples/sample1_out.png | width=100){:height="50%" width="50%"}

![](./image_samples/sample2.jpg){:height="50%" width="50%"}

![](./image_samples/sample2_out.png){:height="50%" width="50%"}
