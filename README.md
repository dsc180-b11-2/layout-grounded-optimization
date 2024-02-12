# LLM-grounded Stable Diffusion Improvements
By: Jiatu Li, Vicky Mao, Zhengyun Nie, Jessica Song

In recent years, text-prompt image generation models like MidJourney, DALL·E, and ChatGPT have revolutionized the way we turn words into visuals, leveraging Stable Diffusion techniques to transform textual descriptions into intricate images. Despite their groundbreaking capabilities, these models face challenges in numerical accuracy, often failing to match the specific quantity of objects described in prompts. For instance, a request for an image depicting "five cats sitting around a table" might erroneously yield only three cats, highlighting a significant hurdle in achieving precise object count in generated images. 

In this project, we explore two dimensions of improving the existing Stable Diffusion text-to-image generation models. First of all, we build a Canvas interface for the an existing solution towards the numerical accuracy to diffusion model, [Lian et al.'s LLM-grounded Stable Diffusion](https://github.com/TonyLianLong/LLM-groundedDiffusion), which restricts referrenced objects to certain bounding boxes to generate a numerically accurate image. With this website, we allow users to draw objects on an existing canvas, specifying the number of objects they want in their image and ehtir respective locations. 

Moreover, through our experiments, we also discovered that Stable Diffusion (SD) often has problems with diffusing the produced bojects with their backgrounds together. With LMD's existing diffusion process, SD often produces unreallistic images. We discover that this phenonmena has to do with the training steps in creating each object's latent mask and diffusing them with existing backgrounds. Therefore, we also fine-tuned this $r_T$ parameter in the forward and backward diffusion process in order to produce more reallistic images. 

## Getting Started
You will need to download [VSCode](https://code.visualstudio.com/) and install the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension to successfully host the Canvas interface. Please download VSCode and install Live Server according to links. 

To run LMD successfully, please download the repository and run this in the command line:
```
pip install -r requirements.txt
```
## Canvas Input
Open the folder `Canvas Input` to `index.html` and click Go Live on the bottom right corner of VSCode. The interface should open up on your default browser. 

Necessary inputs:
- Label: the text label of the object that you want
- Color: the color of that object that you want
  
Then draw a box of where you want this object to be and how large you want it to be.

When you've drawn all objects, specify the background that you want all objects to be in in the background text input section. 
If you don't want any object to show up in the image, enter it in negative prompt section. Then click `Save Input`!

## Generate the image
As our model is not currently live on a server, we are not able to support direct image generation yet. 
The `Save Input` button should have generated a `data.json` file directly from the browser. Please move `data.json` to the `canvas_input` directory. 

Then, to generate the iamge, run 
```
python prompt_batch.py --prompt-type demo --model gpt-4 --auto-query --always-save --template_version v0.1
```
to pre-process your input as a layout. 

Then, run layout-to-image generation using the gpt-4 cache and LMD+:
```
python generate.py --prompt-type demo --model gpt-4 --save-suffix "gpt-4" --repeats 5 --frozen_step_ratio 0.5 --regenerate 1 --force_run_ind 0 --run-model lmd_plus --no-scale-boxes-default --template_version v0.1
```
The `--save-suffix` argument specifies the name of this run. 

You should find 5 iterations of generated images according to your canvas prompt in `img_generation`

<details>
Note: we set `--ignore-negative-prompt` in SD v1.5 so that SD generation does not depend on the LLM and follows a text-to-image generation baseline (otherwise we take the LLM-generated negative prompts and put them into the negative prompt). For other baselines, you can feel free to generate. Evaluation is similar to LMD+, except you need to change the image path in the evaluation command.
</details>


## Acknowledgements
This repo uses code from [LLM-grounded Diffusion](https://github.com/TonyLianLong/LLM-groundedDiffusion), which extended [diffusers](https://huggingface.co/docs/diffusers/index), [GLIGEN](https://github.com/gligen/GLIGEN), and [layout-guidance](https://github.com/silent-chen/layout-guidance). This code also has an implementation of [boxdiff](https://github.com/showlab/BoxDiff) and [MultiDiffusion (region control)](https://github.com/omerbt/MultiDiffusion/tree/master). Using their code means adhering to their license.
