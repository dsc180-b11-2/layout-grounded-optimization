# Beyond Text-to-Image: Layout-Grounded Stable Diffusion Optimization
By: Jiatu Li, Wanting Mao, Zhengyun Nie, Jessica Song at UCSD

[Report](https://drive.google.com/file/d/1Hgf7WEn9rQQm7cLeB3rkD-8Uq2jj4tNe/view) | [Project Website](https://dsc180-b11-2.github.io/layout-grounded-optimization/) | [Poster](https://drive.google.com/file/d/1LxQnwsxSMfa9k9hL2L7ujU7k-nmTEof6/view) 


![Main Image](https://dsc180-b11-2.github.io/layout-grounded-optimization/static/images/gallery.png)

## Getting Started
We provide instructions to run our code in this section.

## Installation
You will need to download [VSCode](https://code.visualstudio.com/) and install the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension to successfully host the Canvas interface. Please download VSCode and install Live Server according to links. 

To run our model successfully, please download the repository and run this in the command line:
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

First, run the following command to generate related files in ```cache``` directory.
```
python prompt_batch.py --prompt-type demo --model gpt-4 --auto-query --always-save --template_version v0.1
```
To generate images using your own text prompt, do the following in order.
1. Open the file ```prompt.py``` and put your prompt in the list named ```prompts_demo_gpt4```.
2. Copy evrything in the variable ```templatev0_1``` at the start of the file and paste the template into [ChatGPT](https://chat.openai.com/). Make sure ```prompt``` in ```Caption: {prompt}``` is replaced by your own prompt.
3. Copy the answer given by GPT and paste it into the file ```cache/cache_demo_v0.1_gpt-4.json```, following the same format as the given key-value pairs.
4. Run the following command to generate images based on the prompt you specified.

```
python generate.py --prompt-type demo --model gpt-4 --save-suffix "gpt-4" --repeats 5 --frozen_step_ratio 0.5 --regenerate 1 --force_run_ind 0 --run-model lmd_plus --no-scale-boxes-default --template_version v0.1
```
Note that the version of GPT we used is GPT4. To use GPT3.5, replace ```prompts_demo_gpt4``` with ```prompts_demo_gpt3_5```, ```cache/cache_demo_v0.1_gpt-4.json``` with ```cache/cache_demo_v0.1_gpt-3_5.json```, and the command line argument ```gpt-4``` with ```gpt-3.5```. Then do the above steps.

You should find 5 iterations of generated images according to your canvas prompt in `img_generation`.

To use Stable Diffusion XL as the baseline model instead of Stable Diffusion, add command line argument --sdxl at the end of the above command. To use different frozen step ratio, chnage 0.5 to any value between 0 and 1.

## Acknowledgements
This repo uses code from [LLM-grounded Diffusion](https://github.com/TonyLianLong/LLM-groundedDiffusion), which extended [diffusers](https://huggingface.co/docs/diffusers/index), [GLIGEN](https://github.com/gligen/GLIGEN), and [layout-guidance](https://github.com/silent-chen/layout-guidance). This code also has an implementation of [boxdiff](https://github.com/showlab/BoxDiff) and [MultiDiffusion (region control)](https://github.com/omerbt/MultiDiffusion/tree/master). Using their code means adhering to their license.
