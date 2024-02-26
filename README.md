# Beyond Text-to-Image: Layout-Grounded Stable Diffusion Optimization for Accurate Image Generation


**Authors:** Jiatu Li, Wanting Mao, Zhengyun Nie, Jessica Song 

**Emails:** {jil165, wamao, znie, jwsong}@ucsd.edu


**Mentor:** Alex Cloninger, Rayan Saab  

**Emails:** {acloninger, rsaab}@ucsd.edu

## Motivation

Diffusion models have been shown as the state-of-the-art methods to generate realistic and diverse images based on text prompts. However, stable diffusion still often make mistakes regarding generating accurately according to numerical information and the object positions.

We utilize a new structure, Layout-Grounded Stable Diffusion (LMD) from [lian2023llmgrounded], as the backbone to optimize the following feats:

- Implement a front-end interface to accept detailed prompts from user
- Resolve numerical accuracy through bounding stable diffusion
- Achieve RGB-level color control over generated objects
- Optimize LMD's ability in generating more accurate and reliable photos
- Evaluate the quality of generated photos

  {"Bad Image" vs "Ours"}

## Background
In this project, we study diffusion models, the underlying idea behind many state-of-the-art image generation models like Midjourney, DALL-E and Stable Diffusion. There are two steps to diffusion models: forward and backward.

- **Forward diffusion:** slowly add random noise to training images
- **Backward diffusion:** learn to reverse the forward process to re-construct image from noise

For more mathematical details on diffusion models, we recommend [Lilian Weng's Blog on Diffusion Models](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/).

## Methods

### Canvas

![Canvas Demo](figures/canvas_demo.png)

1. **Label:** desired object to generate
2. **Color picker:** desired color of the object
3. **Background prompt:** desired background of image
4. **Negative prompt:** what not to include
5. **Canvas:** draw a bounding box of each object on where and how large you want it to be

### Precise Color Control [richtext]

- Use classifier-free guidance for each region to better match the prompt.
- When the color is specified, we apply gradient guidance on the current clean image prediction to exploit the RGB values
- We then compute an MSE loss \(L\) between the average color of \(\hat{x}\) weighted by the token map \(M_{e_i}\) and the RGB triplet \(a_i^c\).
- Apply cross attention with the tokens to control the color.

### Layout-grounded Stable Diffusion

A novel controller guides an off-the-shelf diffusion model for layout-grounded image generation.

![Per-box masked latent generation for instance-level control](LMD Stage 2.png)  
*Figure: Per-box masked latent generation for instance-level control [lian2023llmgrounded]*

**Frozen Step Ratio \(r\):** Number of masked-latents/ Number of total steps

Find the **best** frozen step ratio \(r\) through Experiments.

\(r = 0\): Stable Diffusion  
\(r = 1\): Copy & Paste

## Evaluation

- **Numerical Accuracy:** Yolov8 detects the number of objects in each image.
- **Image Quality:** Fréchet Inception Distance measures the distance between generated images and true images. True images are collected from Stanford Dogs Dataset and Kaggle Flowers Dataset.

## Results

### Numerical Accuracy

Generated xxx images with prompts "one dog", "five dogs", and "ten dogs"

```markdown
| r | prompt 1 | prompt 2 | prompt 3 |
|---|----------|----------|----------|
| 0 (Stable Diffusion) | 30% | 30% | 30% |
| 0.25 | 80% | 80% | 80% |
| 0.5 | 80% | 80% | 80% |
| 0.75 | 80% | 80% | 80% |
| 1 | 80% | 80% | 80% |
