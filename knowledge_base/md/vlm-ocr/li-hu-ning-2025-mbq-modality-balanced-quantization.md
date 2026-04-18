# arXiv:2412.19509v2[cs.CV]21 Mar 2025

## MBQ: Modality-Balanced Quantization for Large Vision-Language Models

Shiyao Li*1,2, Yingchun Hu∗2,3, Xuefei Ning†1, Xihui Liu5, Ke Hong1,2, Xiaotao Jia†3,4, Xiuhong Li2, Yaqi Yan6, Pei Ran6, Guohao Dai7,2, Shengen Yan2, Huazhong Yang1, Yu Wang†1

1Tsinghua University 2Infinigence-AI 3Beihang University 4Qingdao Research Institute, Beihang University 5University of Hong Kong 6Chinatower 7Shanghai Jiao Tong University

![image 1](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile1.png)

![image 2](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile2.png)

![image 3](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile3.png)

### Abstract

Avg Abs Grad of Vision: 1.7e-8

Avg Abs Grad of Language: 2.1e-7

1e-6 1e-6

3584

1.0

1.0

Vision-Language Models (VLMs) have enabled a variety of real-world applications. The large parameter size of VLMs brings large memory and computation overhead which poses significant challenges for deployment. Post-Training Quantization (PTQ) is an effective technique to reduce the memory and computation overhead. Existing PTQ methods mainly focus on large language models (LLMs), without considering the differences across other modalities. In this paper, we discover that there is a significant difference in sensitivity between language and vision tokens in large VLMs. Therefore, treating tokens from different modalities equally, as in existing PTQ methods, may over-emphasize the insensitive modalities, leading to significant accuracy loss. To deal with the above issue, we propose a simple yet effective method, Modality-Balanced Quantization (MBQ), for large VLMs. Specifically, MBQ incorporates the different sensitivities across modalities during the calibration process to minimize the reconstruction loss for better quantization parameters. Extensive experiments show that MBQ can significantly improve task accuracy by up to 4.4% and 11.6% under W3A16 and W4A8 quantization for 7B to 70B VLMs, compared to SOTA baselines. Additionally, we implement a W3A16 GPU kernel that fuses the dequantization and GEMV operators, achieving a 1.4× speedup on LLaVAonevision-7B on the RTX 4090. The code is available at https://github.com/thu-nics/MBQ.

2688

0.5

0.5

Channel Index

0.0

0.0

1792

- -0.5
- -1.0


- -0.5
- -1.0


896

0 200 400 600 800 1000

Token Index

Figure 1. The gradients of loss function w.r.t. the token features of the 13th transformer block in the LLaVA-onevision-7B VLM on COCO caption dataset [8, 10]. The red and orange represent vision tokens, and the blue and green represent language tokens.

to deploy on commonly used accelerators, such as GPUs. For example, the largest LLaVA-onevision VLM, with 72B parameters, requires 144GB of memory, which exceeds the 80GB memory capacity of the A100 GPU.

Many methods have already been designed to improve the inference efficiency of LLM‘[54], including quantization [3, 15, 27], sparse attention [16, 44, 51], efficient decoding strategies [25, 36] and so on. Among them, Post-Training Quantization (PTQ) methods are effective in reducing the memory access and computation overhead to accelerate LLM inference. To reduce the memory access and storage overhead, weight-only quantization methods have been developed, such as AWQ [27], GPTQ [15], QuIP [7], and so on. To reduce the computation overhead, weight-activation quantization methods, such as SmoothQuant [43], SpinQuant [33], FlatQuant [41], Atom [53], and so on, have been applied, enabling the use of the faster low-precision tensor cores on GPUs. To retain the task accuracy, during the calibration process, these meth-

### 1. Introduction

Large Vision-Language Models (VLMs) have made significant progress and enabled various real-world tasks, such as image captioning [10], visual question answering (VQA) [2], and so on. However, due to the large memory and computation overhead, existing large VLMs, such as LLaVA [31], InternVL [11], and QwenVL [4], are hard

*Equal contribution. †Corresponding to: foxdoraame@gmail.com, jiaxt@buaa.edu.cn, yu-wang@tsinghua.edu.cn

ods search for optimal scaling factors [15, 39], channel-wise equalization factors [27, 43], rotation matrices [33], etc., by minimizing the feature reconstruction error of each block.

While PTQ methods are well-studied for LLMs, their suitability for VLMs has not been fully explored, where tokens from multiple modalities need to be handled and crossmodality tasks need to be addressed. Our experiments reveal that directly applying SOTA PTQ methods for LLMs to VLMs results in substantial accuracy degradation. We speculate that the main reason is that existing methods treat vision and language tokens equally, overlooking their significantly different sensitivities.

To verify this, as depicted in Fig. 1, using an imagecaption pair from the COCO dataset as the input [10], we visualize the loss gradient w.r.t. the output feature of the 13th layer in LLaVA-onevision-7B. We can see that the average absolute gradient value of the language token features is over 10× larger than that of vision token features. This 1storder approximation analysis suggests that with the same size of perturbation on the features, language tokens might impact the loss function more than 10× as much as vision tokens. Consequently, treating vision and language tokens equally during calibration may over-emphasize the insensitive vision tokens, resulting in a notable accuracy loss.

Taking the sensitivity differences into consideration, we propose an extremely simple but effective method, Modality-Balanced Quantization (MBQ), for quantizing large VLMs. Specifically, MBQ uses the gradients of the loss function [31] w.r.t. vision and language token features as the sensitivity indicators. These sensitivity indicators are then incorporated into the reconstruction loss as the objective for searching optimal channel-wise equalization factors [27, 43] in both weight-only (W3A16 and W4A16) and weight-activation quantization (W4A8 and W8A8). By balancing the effect of different modalities, MBQ can significantly increase the accuracy of the quantized VLMs.

We conduct extensive experiments across 7B-70B VLMs on challenging vision-language benchmarks. The results show MBQ significantly improves the task accuracy by up to 4% and 11% under W3A16 and W4A8 quantization compared with other SOTA methods. We also analyze the shortcomings of baseline methods and perform comprehensive ablation studies on various factors, including the choice of calibration datasets, alternative formulations of modalitybalancing losses, and the quantization of visual encoders.

For W3A16 quantization, we design a GPU kernel that fuses 3-bit dequantization with general matrix-vector multiplication (GEMV). For W4A16, W4A8, and W8A8 quantization, we adopt existing open-source GPU kernels [27, 29] to accelerate the inference process. Experiments on different workloads show that we can achieve up to 1.4× end-toend speedup on LLaVA-onevision-7B on RTX 4090.

### 2. Preliminaries

#### 2.1. Quantization Formats

In this paper, we focus on applying the uniform integer quantization, which is a commonly used quantization format, to the weight (W) and input activation (X) matrices of each linear layers in VLMs.

For weight-only quantization, existing methods typically apply asymmetric uniform quantization for weight groups (i.e., group-wise quantization), as shown below:

Wasym =

WFP16 − Z Sasym

, (1)

max(WFP16) − Z 2N − 1

, (2)

Sasym =

where WFP16 denotes the 16-bit floating-point (FP16) value, Wasym denotes the low-precision integer value. N is bit-width. Sasym and Z = min(WFP16) denote the scaling factor and zero-point of the asymmetric quantization.

For weight-activation quantization, symmetric uniform quantization is commonly used for both weight and input activation matrices of linear layers:

Wsym =

WFP16 Ssym

, (3)

absmax(WFP16) 2N−1 − 1

, (4)

Ssym =

where Ssym denotes the scaling factor of the symmetric quantization.

For simplicity, we use WxAy to indicate the quantization format, where the x and y represent to the bit-width for Weight and Activation. For example, W4A8 denotes quantizing weights to 4-bit and activations to 8-bit.

#### 2.2. Channel-Wise Equalization

Existing PTQ methods automatically search for optimal hyperparameters of quantization by minimizing the reconstruction error of each transformer block during a calibration process. A series of popular methods [27, 43] aim to equalize outliers in weight and activation matrices by channel-wise equalization (CWE). Specifically, they search the CWE factors E by minimizing the Mean Square Error (MSE) loss in each transformer block. Taking weight-only quantization as an example, the objective of CWE is shown in the following equation:

E∗ = argmin

||Q(W ∗ E)(E−1 ∗ X) − WX||2, (5)

E

where Q means the quantization function.

### 3. Method

#### 3.1. Sensitivity Varies Across Modalities

As introduced in Sec. 2.2, when using visual-language datasets for calibration, CWE treats visual and language activations equally during the calibration process.

Intuitively, we speculate that the significant performance degradation when applying SOTA LLM quantization methods to VLMs stems from treating different modalities equally. This is because errors in vision tokens might have a smaller impact on the output context compared to introducing the same errors in language tokens, due to the following two reasons: (1) From the data perspective, visual data generally contains a high degree of redundancy and might be more fault tolerant for small perturbations. (2) From the model perspective, Zhang et al. [50] discover that the generated content of current VLMs is primarily biased by the pre-trained LLMs rather than the input image.

To verify the above intuition, we evaluate the sensitivity of the output tokens w.r.t the input vision and language tokens on the COCO caption dataset [10]. Specifically, we take the image-caption pairs as inputs of VLMs and calculate gradients of the SFT (Supervised Fine-Tuning) loss function w.r.t. language and vision tokens. The gradients can reflect the impacts on the output language tokens (caption) when small perturbations are applied to language (caption) and vision (image) token features. Note that due to the attention mechanism, the gradient of the SFT loss can still backpropagate to vision tokens in each transformer block, even though we only account for the loss of the output language tokens.

As shown in Fig. 1, the average absolute gradient of language tokens is an order of magnitude larger than that of vision tokens. This means that, for a similar perturbation, a vision token’s impact on the SFT loss is only 0.1× that of a language token. Therefore, if we still treat language and vision tokens equally, we will miss the opportunity to leverage the VLM’s lower sensitivity to vision tokens to achieve higher performance.

To demonstrate the impact of accounting for modalityspecific sensitivities during calibration, we conduct an oracle experiment by applying a modality-balancing factor of

- 0.1 to the vision tokens’ reconstruction loss during CWE calibration. The optimization objective, referred to as balanced CWE, is shown below:


[||Q(W ∗ E)(E−1 ∗ Xl) − WXl||2 (6) +0.1||Q(W ∗ E)(E−1 ∗ Xv) − WXv||2], (7) where the Xl and Xv mean the language and vision tokens.

E∗ = argmin

E

The results of our ablation study are shown in Tab. 1, with a heuristic selected modality-balancing factor, the balanced CWE easily surpasses the performance of CWE by

W3 RTN CWE Balanced CWE

Model FP16

LLaVA-ov-7B 46.00 34.67 36.56 40.22 InternVL2-8B 48.00 43.67 44.78 46.33

Table 1. The accuracy results (%) on MMMU benchmark after W3 quantization. The calibration dataset is selected from COCO caption dataset [10]. The LLaVA-ov-7B is short for LLaVAonevision-7B.

1.55% ∼ 3.66% under W3 quantization. The significant improvements indicate the importance of balancing the different sensitivities across different modalities.

#### 3.2. Modality-Balanced Quantization (MBQ)

Given that the sensitivity differences between vision and language tokens may vary across layers and VLM families, exploring an automatic modality-balancing approach could further enhance the performance of the quantized model.

In this section, we aim to derive an approach for allocating the optimal Modality-Balanced factors to each layer by directly minimizing the change in the SFT loss function. Specifically, we employ the first-order Taylor approximation in Eq. (8) to determine how the SFT loss L changes in response to a small perturbation ∆ in output activation Y of each linear layer:

L(Y + ∆) ≃L(Y) + gT ∗ ∆, (8) where gT represents the gradient of the output activation Y.

The change in SFT loss caused by quantization can be expressed as the following equation:

||L(Yˆ )|| ≃||gT ∗ ∆|| (9) =||gvT ∗ ∆v + glT ∗ ∆l|| (10) ≤||gvT ∗ ∆v|| + ||glT ∗ ∆l|| (11) ≤|g¯v| ∗ ||∆v|| + |g¯l| ∗ ||∆l|| (12) =|g¯v| ∗ ||Yv − Yˆ v|| + |g¯l| ∗ ||Yl − Yˆ l||, (13)

where Yv and Yˆv represent the output vision tokens of the FP16 linear layer and the quantized linear, respectively. Yl and Yˆl represent the output language tokens of the FP16 linear layer and the quantized linear, respectively. The |g¯v| and |g¯l| represent the average absolute gradient of each linear layer’s output vision and language tokens, respectively.

In this paper, we combine MBQ with channel-wise equalization to search optimal equalization factors for better performance.

Firstly, in order to accelerate the prefill stage of VLMs, we quantize both the weights and input activations of each linear layer to leverage fast low-precision tensor cores. The

objective is shown in the following:

[|g¯v| ∗ ||WXv − Q(W ∗ E)Q(E−1 ∗ Xv)|| (14) +|g¯l| ∗ ||WXl − Q(W ∗ E)Q(E−1 ∗ Xl)||], (15)

min

E

where Xv and Xl represent the input token and language activations of each linear layer, respectively.

Secondly, to accelerate the decode stage of VLMs, we only quantize weights to reduce the memory overhead, aiming to minimize the balanced reconstruction error by the following objective:

[|g¯v| ∗ ||WXv − Q(W ∗ E)(E−1 ∗ Xv)|| (16) +|g¯l| ∗ ||WXl − Q(W ∗ E)(E−1 ∗ Xl)||], (17)

min

E

Notably, unlike directly using the heuristically selected MSE-based balanced CWE loss in Sec. 3.1, our derived reconstruction error loss function relies on Mean Absolute Error (MAE). Our ablation study in Sec. 4.3 demonstrates that minimizing MAE-based reconstruction loss in MBQ yields better results than using an MSE-based one.

#### 3.3. End-to-End Acceleration Implementation

As illustrated in Sec. 6.1, we need to quantize not only the VLMs with large parameter counts but also the ViT encoders for efficient deployment, which have substantial computational overhead when transforming high-resolution images into vision tokens. The ViT encoders take a series of image patches as input and generate a set of vision tokens as output. The input activation of each linear layer in ViT encoders are 2D matrices, so the main computation operator is GEMM.

To this end, we apply weight-activation quantization to the ViT encoders and weight-only quantization for VLMs to accelerate the auto-regressive decode stage. To achieve practical hardware acceleration for VLMs, we designed a custom fused W3 quantization GPU kernel by fusing the dequantization process with the GEMV operator. Specifically, we pack eight 3-bit weights into three bytes, and the fused W3 kernel first loads the W3 weights instead of FP16 weights to reduce memory access overhead. It then dequantizes the W3 weights to FP16. Finally, the fused W3 kernel performs computations using the FP16 tensor core.

With the fused W3 kernel and open-source GPU kernel libraries [27, 29] for quantization, we can accelerate the inference speed of both the quantized ViT encoders and VLMs. Detailed experiments in Sec. 4.4 demonstrate the hardware performance of the proposed W3 kernel and endto-end speedups across various scenarios.

### 4. Experiments

#### 4.1. Experimental Setups

##### 4.1.1. Calibration Datasets

The calibration task requires leveraging both the VLM’s ability to understand image details and its language modeling capabilities. “Image captioning” is one of the tasks that addresses both aspects. Specifically, we choose the improved COCO Caption dataset proposed by ShareGPT4V [8] and sample 128 image-caption pairs as the calibration dataset. Chen et al. [8] use GPT4-V to generate a high-quality caption for each image. For each VLM, we apply the corresponding conversation template to each image-caption pair to create an instructional format.

##### 4.1.2. Evaluation Datasets

To evaluate the performance of the quantized model, we conduct experiments on various vision-language benchmarks based on the LMMs-Eval [49]. Specifically, we use OCRBench [32] and TextVQA [40] for text recognition and comprehension, VizWiz [18] and SEED-Bench [19] to test visual perception, and ScienceQA [34] and MMMU [47] to evaluate visual reasoning. Additionally, to demonstrate the practical conversational performance of the quantized VLM, we present several cases on the LLaVA-bench-inthe-wild [31] and LLaVA-bench-wilder [20] datasets in the supplementary Sec. 8.2.

##### 4.1.3. Models

We benchmark various quantization methods on LLaVAonevision [21], InternVL2 [11], and Qwen2-VL [4] families. For each model family, we select both a smaller and a larger parameter version to showcase the capability of MBQ across different model sizes. For LLaVA-onevision, we select models with 7B and 72B parameters, which utilize Qwen2-7B/-72B for the VLM and SigLIP-400M [48] for the ViT encoder. For InternVL2, we evaluate the 8B and 26B models, which incorporate InternLM2-8B/-20B as the VLM component and use InternViT-300M/-6B as the vision encoder. For Qwen2-VL, we use models with 7B and 72B parameters in our evaluation, which use Qwen2-7B/-72B for the VLM component and a 675M ViT encoder.

##### 4.1.4. Baselines

For weight-only quantization, we compare MBQ with the vanilla round-to-nearest quantization (RTN) and AWQ [27] under W3A16, which is based on channel-wise equalization. We apply group-wise asymmetric quantization for each method and keep the group size at 128. For weightactivation quantization, we compare with both the RTN and SmoothQuant [43] under W4A8, which also relies on channel-wise equalization. As discussed in SmoothQuant, we apply per-token symmetric quantization for activations and per-channel (output) symmetric quantization for

Model Bitwidth Method MMMU SEED OCRBench VizWiz ScienceQA TextVQA Average (↑)

FP16 - 46.0 74.9 62.2 60.4 85.4 76.1 67.5

- W3A16

RTN 34.7 5.9 35.9 59.2 86.2 60.9 47.1 GPTQ 41.9 72.9 55.7 56.4 86.4 71.3 64.1 AWQ 36.6 53.0 59.3 58.5 83.2 73.0 60.6 MBQ 42.0 69.7 61.1 60.7 85.0 73.3 65.3

- W4A8


LLaVA-onevision-7B

RTN 38.2 50.3 40.1 58.2 88.3 61.5 56.1

SQ 30.9 42.7 32.0 56.7 87.1 56.9 51.1 MBQ 42.6 67.7 52.3 58.9 88.5 68.3 63.1

FP16 - 48.0 76.0 76.5 61.1 96.2 77.0 72.5

- W3A16

RTN 43.7 74.9 74.0 56.0 95.6 74.6 69.8 GPTQ 41.7 73.4 70.2 59.9 89.5 73.1 68.0 AWQ 44.8 75.2 74.7 58.9 95.5 74.2 70.6 MBQ 46.9 75.4 75.1 58.7 95.6 75.1 71.1

- W4A8


InternVL2-8B

RTN 44.3 74.0 72.0 57.1 95.5 73.1 69.3 SQ 41.8 73.8 70.9 54.2 95.1 72.6 68.1 MBQ 45.6 74.3 73.0 56.5 95.8 72.3 69.6

FP16 - 50.6 76.4 80.7 68.3 85.1 82.0 73.8

- W3A16

RTN 44.9 74.8 60.0 65.2 81.5 71.2 66.3 GPTQ 43.1 73.7 74.8 64.3 79.7 76.7 68.7 AWQ 44.7 75.1 76.9 68.0 82.5 79.5 71.1 MBQ 47.9 74.8 76.8 67.7 82.8 79.9 71.6

- W4A8


Qwen2-VL-7B

RTN 43.8 74.9 60.3 58.9 78.9 71.0 64.6

SQ 45.9 75.0 57.1 52.3 80.9 68.2 63.2 MBQ 47.2 75.1 72.8 59.3 81.2 75.0 68.4

- Table 2. Main results on the small models of LLaVA-onevision, InternVL2, and Qwen2-VL families. “SQ” is short for SmoothQuant.

Model Bitwidth Method MMMU SEED OCRBench VizWiz ScienceQA TextVQA Average (↑)

LLaVA-onevision-72B

FP16 - 56.1 78.1 73.2 69.2 90.0 79.3 74.3

- W3A16

RTN 53.9 77.4 68.2 66.1 89.5 77.4 72.1 GPTQ 52.7 76.0 69.7 68.3 89.3 77.9 72.3 AWQ 33.4 71.2 48.7 49.3 69.2 58.8 55.1

- MBQ 54.4 77.6 71.6 69.0 90.3 78.5 73.6

W4A8

RTN 54.8 76.6 64.5 64.7 89.0 74.5 70.7 SQ 51.6 76.6 64.2 65.7 89.1 74.4 70.3

- MBQ 55.6 76.5 64.4 65.7 89.2 73.3 70.8




InternVL2-26B

FP16 - 47.1 76.8 77.9 66.2 97.5 82.1 74.6

- W3A16

RTN 46.6 75.7 75.9 64.7 96.4 80.6 73.3 GPTQ 44.8 75.8 76.0 60.9 96.3 80.1 72.3 AWQ 46.4 76.2 76.4 64.5 96.7 81.0 73.5 MBQ 47.1 76.3 76.5 64.5 97.3 81.1 73.8

- W4A8


RTN 44.7 76.0 76.4 62.6 96.7 79.6 72.7 SQ 38.2 70.6 68.5 56.7 86.3 72.6 65.5 MBQ 44.0 75.7 77.5 62.0 97.1 80.0 72.7

Qwen2-VL-72B

FP16 - 61.1 77.6 79.9 76.0 91.6 82.5 78.1

- W3A16

RTN 57.7 77.5 70.4 74.8 89.7 79.7 75.0 GPTQ 57.3 77.2 78.5 73.6 91.5 81.6 76.6 AWQ 59.6 77.6 79.6 75.4 90.4 82.4 77.5 MBQ 59.6 77.7 79.4 75.6 90.5 82.5 77.6

- W4A8


RTN 58.1 76.6 66.2 71.3 90.1 77.0 73.2 SQ 55.9 76.4 65.5 69.7 88.8 76.9 72.2 MBQ 57.7 76.3 77.5 73.6 89.6 80.5 75.8

- Table 3. Main results on the large models of LLaVA-onevision, InternVL2, and Qwen2-VL families. “SQ” is short for SmoothQuant.


weights to take advantage of low-precision tensor cores. The evaluation results of W4 and W8A8 are shown in Supplementary Sec. 8.

#### 4.2. Main Results

For Weight-only Quantization, as shown in Tab. 2 and Tab. 3, the results of RTN quantization indicate that smaller VLMs are more sensitive to weight-only quan-

Components Channel-wise MMMU (↑) SEED (↑) Equalization

BitWidth Method

COCO Calib.

Modality-Balance (MSE)

Modality-Balance (MAE)

FP16 - - - - - 46.0 71.1

- W3A16

RTN ✗ ✗ ✗ ✗ 34.7 10.4 AWQ ✓ ✗ ✗ ✗ 36.6 51.5

- - ✓ ✓ ✗ ✗ 38.7 61.8
- - ✓ ✓ ✓ ✗ 40.8 64.8


MBQ ✓ ✓ ✗ ✓ 42.0 66.4

- W4A8


RTN ✗ ✗ ✗ ✗ 38.2 48.4 SQ ✓ ✗ ✗ ✗ 30.9 41.6

- - ✓ ✓ ✗ ✗ 29.2 10.2
- - ✓ ✓ ✓ ✗ 41.9 63.5


MBQ ✓ ✓ ✗ ✓ 42.6 64.4

Table 4. The ablation study on LLaVA-onevision-7B with W3A16 and W4A8 quantization. “SQ” is short for SmoothQuant.

tization. The average accuracy loss for RTN-quantized 7B and 8B VLMs is 9.6%, significantly higher than the 1.5% loss seen in VLMs over 26B. This trend also aligns with observations in LLMs [24, 46].

The proposed MBQ can significantly outperform the AWQ baseline across different families. Especially within the LLaVA-onevision family, MBQ achieves an average accuracy improvement of 4.2% on the 7B VLM and 18.5% on the 72B VLM compared to AWQ. It is worth noting that for the LLaVA-onevision-72B VLM, AWQ even shows a 17% performance drop compared to RTN. Instead, the proposed MBQ can significantly improve the average accuracy and surpass RTN quantization. For the InternVL2 and Qwen2VL families, MBQ can also outperform the RTN and AWQ baselines by around 1%.

For Weight-Activation Quantization, similar to weight-only quantization, MBQ can significantly outperform SmoothQuant and RTN baselines, with improvements of up to 11.6%. In many cases, the average performance of SmoothQuant is lower than that of RTN quantization, especially in InternVL2-26B under W4A8. The results indicate that with activation quantization, our insight into modality-balancing becomes more crucial for improving the performance of quantized VLMs, as the core idea of modality-balancing mainly addresses the sensitivity differences among various modalities within the activations.

#### 4.3. Ablation Study

##### 4.3.1. The Effect of Calibration Datasets

As AWQ and SmoothQuant are designed for LLM quantization, they use the Pile [17] validation dataset during calibration, which only contains language data.

Directly apply the vision-language dataset as calibration does not consistently improve the performance of the quantized VLMs. As shown in Tab. 4, when we use the

COCO caption dataset as the calibration dataset, the performance of AWQ W3A16 can significantly increase by 2.1% and 10.3% on MMMU and SEED datasets, respectively. However, the performance of SmoothQuant W4A8 with the COCO caption calibration dataset significantly decreases by 1.7% and 31.4% on MMMU and SEED datasets.

We speculate that this is because weight-activation quantization requires considering both weight and activation quantization errors. Ignoring the sensitivity differences between vision and language tokens in activations leads to a significant performance drop in SmoothQuant, even falling behind RTN quantization.

##### 4.3.2. The Effect of Modality-Balance

Modality-Balancing plays a crucial role in weightactivation quantization and can also improve the performance of weight-only quantization. As shown in Tab. 4, with the help of Modality-Balancing (MAE), the SmoothQuant with COCO calibration can significantly improve 13.4% and 54.2% on MMMU and SEED, respectively. For the weight-only quantization, ModalityBalancing (MAE) can increase the accuracy by 3.3% and 4.6% on MMMU and SEED, respectively. This significant performance improvement confirms the importance of accounting for the varying sensitivities of different modalities during the calibration process.

We find that Modality-Balancing (MAE) can consistently outperform Modality-Balancing (MSE) in both weight-only and weight-activation quantization. For both W3A16 and W4A8, Modality-Balancing with MAE reconstruction loss can achieve over 1% accuracy improvement on both MMMU and SEED datasets. Therefore, we recommend using the MAE reconstruction loss form, derived directly from the gradient of the activation with respect to the SFT loss, rather than the MSE reconstruction loss.

Model Bitwidth Method MMMU OCRBench VizWiz FP16 - 56.1 73.2 69.2

LLaVA-one QuaRot 53.0 70.8 67.9 vision-72B W4A8 SpinQuant 52.6 70.9 61.0

###### MBQ (Rot) 55.8 72.5 69.0

FP16 - 47.1 77.9 66.2 InternVL2 QuaRot 44.2 76.7 62.1

-26B W4A8 SpinQuant 43.7 76.8 64.5 MBQ (Rot) 47.4 77.8 65.6

FP16 - 61.1 79.9 76.0 Qwen-VL QuaRot 49.7 78.1 71.4 -72B W4A8 SpinQuant 50.8 77.4 69.3 MBQ (Rot) 60.0 79.9 75.4

Table 5. Rotation-based quantization results on the large models of LLaVA-onevision, InternVL2, and Qwen2-VL families.

In addition, we also study two different reweight strategies to show the effectiveness of MBQ: (1) We randomly divided calibration tokens into two equal groups to reweight quant error. For W3A16 LLaVA-onevision-7B, the accuracy on OCRBench is 1.3% lower than MBQ, which is similar to the case without reweighting. (2) We directly use the gradient of each token to perform token-wise quantization error reweighting. For W3A16 LLaVA-onevision-7B, the accuracy on OCRBench is 1.5% lower than MBQ. We find that this is because the gradient of many vision tokens is zero, leading to an inability to account for the quantization error of these tokens. We will highlight these new results.

##### 4.3.3. Combine MBQ with Rotation-based Quantization

From Tab. 3, we observe that for large VLMs, the performance improvement of MBQ over RTN weight-activation quantization is not substantial, and there remains a significant performance gap compared to FP16 VLMs.

As demonstrated in Sec. 3, the proposed ModalityBalancing approach can be seamlessly integrated with any block-wise LLM quantization method to support VLMs. To this end, we combine Modality-Balancing with the SOTA rotation-based quantization technique [41], resulting in MBQ (Rot), which can achieve significant better performance. As illustrated in Tab. 5, across three different large VLMs, the proposed MBQ (Rot) under W4A8 quantization exhibits an accuracy loss of less than 1.1% compared to the original FP16 VLMs. Furthermore, when compared to other state-of-the-art methods, W4A8 MBQ (Rot) achieves performance improvements of up to 9.2%.

##### 4.3.4. Quantize Both Visual Encoder and VLM

In Sec. 3.3, we analyze the different efficiency bottlenecks of the ViT encoder and VLM. In real-world applications, we need to quantize both components for higher acceleration ratios. As shown in Tab. 6, we quantize the ViT encoder with SmoothQuant and VLM with MBQ in LLaVAonevision-7B and evaluate the accuracy on MMMU and

ViT VLM MMMU (↑) VizWiz (↑) FP16 FP16 46.0 60.4

- FP16 W3A16 42.0 60.7
- FP16 W4A8 42.6 58.9


- W4A8 W3A16 42.6 62.8
- W4A8 W4A8 43.1 60.1


- Table 6. The results of the quantized ViT encoder and VLM in LLaVA-onevision-7B on the MMMU and VizWiz. We use MBQ for VLM quantization and SmoothQuant for ViT quantization.

BitWidth Method MMLU (↑) FP16 - 65.9

- W3A16

AWQ (Pile) 61.9 AWQ (COCO) 62.0 MBQ 62.9

- W4A8


SQ (Pile) 59.8 SQ (COCO) 59.0 MBQ 61.8

- Table 7. The results of quantized LLaVA-onevision-7B on the MMLU benchmark. “SQ” is short for SmoothQuant.


VizWiz benchmarks.

Experimental results show that applying W4A8 quantization to the ViT encoder does not lead to a significant performance drop; instead, it even improves performance on some benchmarks. This suggests that the ViT encoder is not particularly sensitive to quantization, possibly due to the redundancy in vision tokens discussed in Sec. 1. Therefore, quantizing the ViT encoder alongside the VLM quantization is feasible from an algorithmic performance perspective.

##### 4.3.5. The Performance on Language-only Benchmark

The main idea of the proposed MBQ is to consider the sensitivity across different modalities during quantization, aiming to enhance performance in both vision-language and language-only tasks. Accordingly, we evaluated the performance of the quantized LLaVA-onevision-7B VLM on the MMLU benchmark with different quantization methods.

As shown in Tab. 7, with W3A16 and W4A8 quantization, MBQ achieves a performance improvement of 0.9% and 2%, compared to AWQ and SmoothQuant. This result demonstrates that for quantized VLMs, considering the sensitivity differences across modalities not only significantly reduces the performance loss on vision-language tasks, but also helps maintain performance on language-only tasks.

#### 4.4. Efficiency Evaluation4.4.1. Single Kernel Performance

We evaluate the speed of the proposed fused W3A16 GEMV kernel on the RTX 4090 GPU, testing linear layers

Shape (IC × OC) FP16 (ms) W3A16 (ms) Speedup

3584 × 3584 3.0 2.6 1.2× 3584 × 10752 8.3 2.7 3.1× 3584 × 18944 14.4 2.9 5.0× 18944 × 3584 14.6 3.1 4.7×

Table 8. The speed up of the fused W3A16 General Matrix-Vector Multiplication (GEMV) kernel on RTX 4090 GPU. “IC” and “OC” are short of “Input Channel” and “Output Channel”.

with different weight matrix shapes in LLaVA-onevision-

- 7B. Specifically, as shown in Tab. 8, we evaluate the kernel on 4 different shapes of weight matrices, including 3584 × 3584 (the out proj layers), 3584×10752 (the qkv proj layers), 3584×18944 (the up proj and gate proj layers), and 18944×3584 (the down proj layers). For each shape, we compare the proposed fused W3A16 GEMV kernel with the original FP16 GEMV kernel.


The evaluation results show that the fused W3A16 GEMV kernel achieves a speedup of 1.2× to 5.0× across 4 different shapes, compared to the FP16 GEMV baseline. As the matrix size increases, the fused W3A16 kernel achieves a more significant speedup. This is because GEMV performance is memory-bound, and the impact of memory access speed becomes more pronounced with larger weight matrices. By applying W3A16 quantization, memory access latency is significantly reduced in large matrix GEMV operations, leading to a greater speedup.

##### 4.4.2. End-to-End Performance

With the help of the proposed W3A16 GPU kernel and the W4A8 GPU kernel from Qserve [29], we evaluate the latency of both the ViT encoder and the VLM in LLaVAonevision-7B on RTX 4090. We run both the ViT encoder and VLM with FlashAttention-2 [13]. The evaluation results are shown in Tab. 9.

For the ViT encoder, the embedding layer will convert each input image into 729 (27 × 27) tokens as the input. As discussed in Sec. 3.3, the ViT encoder only has the prefill stage, the main operators are GEMMs, which is computebound. In this case, we apply the W4A8 kernel to the ViT encoder and achieve 1.15× speedup.

For the VLM, as discussed in Sec. 6.1, the VLM has two distinct stages, and each stage requires different quantization schemes for inference acceleration.

Specifically, in order to accelerate the prefill stage, we need to apply weight-activation quantization to use the lowprecision tensor cores. With W4A8 quantization, we evaluate the inference latency of the quantized VLM with the open-source GPU kernel. As shown in Tab. 9, when the input token length is 512 and 1024 tokens, W4A8 can achieve

- 1.16× and 1.18×, respectively. As the token length increases, the speedup gradually becomes greater.


In order to accelerate the decode stage, we apply W3A16

Model Stage FP16 (ms) W3A16 (ms) W4A8 (ms) ViT Prefill (729 tokens) 11.2 - 9.7

Prefill (512 tokens) 68.8 - 59.4 VLM Prefill (1024 tokens) 109.0 - 92.7 Decode 29.6 21.1 26.3

Table 9. The end-to-end speed up of LLaVA-onevision-7B on RTX4090 with fused GPU kernels.

quantization to the VLM. Since the latency of the decode stage remains similar across different input token lengths, we measure the average latency of the decode stage at input token lengths of 128, 256, 512, and 1024. As shown in Tab. 9, both W4A8 and W3A16 quantization can accelerate the decode stage. However, the W3A16-quantized VLM is 1.23× faster than the W4A8 model. This result primarily stems from two factors: (1) the W3A16-quantized model has lower memory access overhead for large weight matrices compared to W4A8, and (2) the W4A8 operator requires additional dynamic quantization of activations, which incurs additional computational time.

For practical acceleration, we use weight-activation quantization to accelerate the ViT encoder and weight-only quantization to speed up the decode stage of VLMs. The main reason is that the FP16 VLM’s prefill stage takes as long to process 1,024 tokens as the decode stage takes to generate just 4 tokens, as shown in Tab. 9. In real-world applications, the number of tokens to be decoded is large, necessitating multiple forward passes during the decode stage, which is the most time-consuming part of generation tasks. Thus, weight-only quantization is more suitable for VLMs.

### 5. Conclusion

In this paper, we identify a key phenomenon: the sensitivities of vision and language tokens to quantization differ significantly. Based on this finding, we propose ModalityBalanced Quantization (MBQ), a simple but effective quantization method to improve the accuracy of quantized VLMs for both weight-only and weight-activation quantization. Specifically, we use the gradients of the SFT loss function w.r.t. vision and language tokens as sensitivity indicators to balance the reconstruction loss during calibration. MBQ can outperform existing SOTA PTQ methods by 4.4% and 11.6% on both W4A8 and W3A16 across various VLMs. With the proposed W3A16 CUDA kernel, we achieve 1.4× decoding speedup compared with FP16 baseline.

Acknowledgements. This work was supported by the National Natural Science Foundation of China (No. 62325405, 62104128, U19B2019, U21B2031, 61832007, 62204164, 92364201), Tsinghua EE Xilinx AI Research Fund, and Beijing National Research Center for Information Science and Technology (BNRist). We thank for all the support from Infinigence-AI.

### References

- [1] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. Advances in neural information processing systems, 35:23716–23736,

2022. 2

- [2] Stanislaw Antol, Aishwarya Agrawal, Jiasen Lu, Margaret Mitchell, Dhruv Batra, C Lawrence Zitnick, and Devi Parikh. Vqa: Visual question answering. In Proceedings of the IEEE international conference on computer vision, pages 2425– 2433, 2015. 1
- [3] Saleh Ashkboos, Amirkeivan Mohtashami, Maximilian L Croci, Bo Li, Pashmina Cameron, Martin Jaggi, Dan Alistarh, Torsten Hoefler, and James Hensman. Quarot: Outlier-free 4-bit inference in rotated llms. arXiv preprint arXiv:2404.00456, 2024. 1
- [4] Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou. Qwen-vl: A frontier large vision-language model with versatile abilities. arXiv preprint arXiv:2308.12966, 2023. 1, 4
- [5] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. arXiv preprint arXiv:2407.07726, 2024. 2
- [6] Jianjian Cao, Peng Ye, Shengze Li, Chong Yu, Yansong Tang, Jiwen Lu, and Tao Chen. Madtp: Multimodal alignment-guided dynamic token pruning for accelerating vision-language transformer. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 15710–15719, 2024. 2
- [7] Jerry Chee, Yaohui Cai, Volodymyr Kuleshov, and Christopher M De Sa. Quip: 2-bit quantization of large language models with guarantees. Advances in Neural Information Processing Systems, 36, 2024. 1
- [8] Lin Chen, Jinsong Li, Xiaoyi Dong, Pan Zhang, Conghui He, Jiaqi Wang, Feng Zhao, and Dahua Lin. Sharegpt4v: Improving large multi-modal models with better captions. arXiv preprint arXiv:2311.12793, 2023. 1, 4
- [9] Liang Chen, Haozhe Zhao, Tianyu Liu, Shuai Bai, Junyang Lin, Chang Zhou, and Baobao Chang. An image is worth 1/2 tokens after layer 2: Plug-and-play inference acceleration for large vision-language models. In European Conference on Computer Vision, pages 19–35. Springer, 2025. 2
- [10] Xinlei Chen, Hao Fang, Tsung-Yi Lin, Ramakrishna Vedantam, Saurabh Gupta, Piotr Doll´ar, and C Lawrence Zitnick. Microsoft coco captions: Data collection and evaluation server. arXiv preprint arXiv:1504.00325, 2015. 1, 2, 3
- [11] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 24185–24198, 2024. 1, 4, 2


- [12] Xiangxiang Chu, Limeng Qiao, Xinyang Lin, Shuang Xu, Yang Yang, Yiming Hu, Fei Wei, Xinyu Zhang, Bo Zhang, Xiaolin Wei, et al. Mobilevlm: A fast, reproducible and strong vision language assistant for mobile devices. arXiv preprint arXiv:2312.16886, 2023. 2
- [13] Tri Dao. Flashattention-2: Faster attention with better parallelism and work partitioning. arXiv preprint arXiv:2307.08691, 2023. 8
- [14] Tim Dettmers, Ruslan Svirschevski, Vage Egiazarian, Denis Kuznedelev, Elias Frantar, Saleh Ashkboos, Alexander Borzunov, Torsten Hoefler, and Dan Alistarh. Spqr: A sparse-quantized representation for near-lossless llm weight compression. arXiv preprint arXiv:2306.03078, 2023. 1
- [15] Elias Frantar, Saleh Ashkboos, Torsten Hoefler, and Dan Alistarh. Gptq: Accurate post-training quantization for generative pre-trained transformers. arXiv preprint arXiv:2210.17323, 2022. 1, 2
- [16] Tianyu Fu, Haofeng Huang, Xuefei Ning, Genghan Zhang, Boju Chen, Tianqi Wu, Hongyi Wang, Zixiao Huang, Shiyao Li, Shengen Yan, et al. Moa: Mixture of sparse attention for automatic large language model compression. arXiv preprint arXiv:2406.14909, 2024. 1
- [17] Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles Foster, Jason Phang, Horace He, Anish Thite, Noa Nabeshima, et al. The pile: An 800gb dataset of diverse text for language modeling. arXiv preprint arXiv:2101.00027, 2020. 6
- [18] Danna Gurari, Qing Li, Abigale J Stangl, Anhong Guo, Chi Lin, Kristen Grauman, Jiebo Luo, and Jeffrey P Bigham. Vizwiz grand challenge: Answering visual questions from blind people. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 3608–3617,

2018. 4

- [19] Bohao Li, Rui Wang, Guangzhi Wang, Yuying Ge, Yixiao Ge, and Ying Shan. Seed-bench: Benchmarking multimodal llms with generative comprehension. arXiv preprint arXiv:2307.16125, 2023. 4
- [20] Bo Li, Kaichen Zhang, Hao Zhang, Dong Guo, Renrui Zhang, Feng Li, Yuanhan Zhang, Ziwei Liu, and Chunyuan Li. Llava-next: Stronger llms supercharge multimodal capabilities in the wild, 2024. 4, 2
- [21] Bo Li, Yuanhan Zhang, Dong Guo, Renrui Zhang, Feng Li, Hao Zhang, Kaichen Zhang, Yanwei Li, Ziwei Liu, and Chunyuan Li. Llava-onevision: Easy visual task transfer. arXiv preprint arXiv:2408.03326, 2024. 4, 2
- [22] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In International conference on machine learning, pages 19730–

19742. PMLR, 2023. 2

- [23] Shiyao Li, Xuefei Ning, Ke Hong, Tengxuan Liu, Luning Wang, Xiuhong Li, Kai Zhong, Guohao Dai, Huazhong Yang, and Yu Wang. Llm-mq: Mixed-precision quantization for efficient llm deployment. In The Efficient Natural Language and Speech Processing Workshop with NeurIPS,

2023. 1

- [24] Shiyao Li, Xuefei Ning, Luning Wang, Tengxuan Liu, Xiangsheng Shi, Shengen Yan, Guohao Dai, Huazhong Yang,


- and Yu Wang. Evaluating quantized large language models. In Proceedings of the 41st International Conference on Machine Learning, pages 28480–28524, 2024. 6
- [25] Yuhui Li, Fangyun Wei, Chao Zhang, and Hongyang Zhang. Eagle: Speculative sampling requires rethinking feature uncertainty. arXiv preprint arXiv:2401.15077, 2024. 1
- [26] Bin Lin, Zhenyu Tang, Yang Ye, Jiaxi Cui, Bin Zhu, Peng Jin, Jinfa Huang, Junwu Zhang, Yatian Pang, Munan Ning, et al. Moe-llava: Mixture of experts for large visionlanguage models. arXiv preprint arXiv:2401.15947, 2024. 2
- [27] Ji Lin, Jiaming Tang, Haotian Tang, Shang Yang, Wei-Ming Chen, Wei-Chen Wang, Guangxuan Xiao, Xingyu Dang, Chuang Gan, and Song Han. Awq: Activation-aware weight quantization for on-device llm compression and acceleration. Proceedings of Machine Learning and Systems, 6:87–100,

2024. 1, 2, 4

- [28] Ji Lin, Hongxu Yin, Wei Ping, Pavlo Molchanov, Mohammad Shoeybi, and Song Han. Vila: On pre-training for visual language models. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 26689–26699, 2024. 2
- [29] Yujun Lin, Haotian Tang, Shang Yang, Zhekai Zhang, Guangxuan Xiao, Chuang Gan, and Song Han. Qserve: W4a8kv4 quantization and system co-design for efficient llm serving. arXiv preprint arXiv:2405.04532, 2024. 2, 4, 8
- [30] Zhihang Lin, Mingbao Lin, Luxi Lin, and Rongrong Ji. Boosting multimodal large language models with visual tokens withdrawal for rapid inference. arXiv preprint arXiv:2405.05803, 2024. 2
- [31] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. Advances in neural information processing systems, 36, 2023. 1, 2, 4
- [32] Yuliang Liu, Zhang Li, Mingxin Huang, Biao Yang, Wenwen Yu, Chunyuan Li, Xucheng Yin, Cheng lin Liu, Lianwen Jin, and Xiang Bai. Ocrbench: On the hidden mystery of ocr in large multimodal models, 2024. 4
- [33] Zechun Liu, Changsheng Zhao, Igor Fedorov, Bilge Soran, Dhruv Choudhary, Raghuraman Krishnamoorthi, Vikas Chandra, Yuandong Tian, and Tijmen Blankevoort. Spinquant–llm quantization with learned rotations. arXiv preprint arXiv:2405.16406, 2024. 1, 2
- [34] Pan Lu, Swaroop Mishra, Tony Xia, Liang Qiu, Kai-Wei Chang, Song-Chun Zhu, Oyvind Tafjord, Peter Clark, and Ashwin Kalyan. Learn to explain: Multimodal reasoning via thought chains for science question answering. In The 36th Conference on Neural Information Processing Systems (NeurIPS), 2022. 4
- [35] Brandon McKinzie, Zhe Gan, Jean-Philippe Fauconnier, Sam Dodge, Bowen Zhang, Philipp Dufter, Dhruti Shah, Xianzhi Du, Futang Peng, Floris Weers, et al. Mm1: Methods, analysis & insights from multimodal llm pre-training. arXiv preprint arXiv:2403.09611, 2024. 2
- [36] Xuefei Ning, Zinan Lin, Zixuan Zhou, Zifu Wang, Huazhong Yang, and Yu Wang. Skeleton-of-thought: Prompting llms for efficient parallel generation. In The Twelfth International Conference on Learning Representations, 2024. 1


- [37] Yanyuan Qiao, Zheng Yu, Longteng Guo, Sihan Chen, Zijia Zhao, Mingzhen Sun, Qi Wu, and Jing Liu. Vl-mamba: Exploring state space models for multimodal learning. arXiv preprint arXiv:2403.13600, 2024. 2
- [38] Yuzhang Shang, Mu Cai, Bingxin Xu, Yong Jae Lee, and Yan Yan. Llava-prumerge: Adaptive token reduction for efficient large multimodal models. arXiv preprint arXiv:2403.15388,

2024. 2

- [39] Wenqi Shao, Mengzhao Chen, Zhaoyang Zhang, Peng Xu, Lirui Zhao, Zhiqian Li, Kaipeng Zhang, Peng Gao, Yu Qiao, and Ping Luo. Omniquant: Omnidirectionally calibrated quantization for large language models. arXiv preprint arXiv:2308.13137, 2023. 2, 1
- [40] Amanpreet Singh, Vivek Natarjan, Meet Shah, Yu Jiang, Xinlei Chen, Dhruv Batra, Devi Parikh, and Marcus Rohrbach. Towards vqa models that can read. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 8317–8326, 2019. 4
- [41] Yuxuan Sun, Ruikang Liu, Haoli Bai, Han Bao, Kang Zhao, Yuening Li, Jiaxin Hu, Xianzhi Yu, Lu Hou, Chun Yuan, et al. Flatquant: Flatness matters for llm quantization. arXiv preprint arXiv:2410.09426, 2024. 1, 7
- [42] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. Advances in neural information processing systems, 30, 2017. 1
- [43] Guangxuan Xiao, Ji Lin, Mickael Seznec, Hao Wu, Julien Demouth, and Song Han. Smoothquant: Accurate and efficient post-training quantization for large language models. In International Conference on Machine Learning, pages 38087–38099. PMLR, 2023. 1, 2, 4
- [44] Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. Efficient streaming language models with attention sinks. arXiv preprint arXiv:2309.17453, 2023. 1
- [45] Ruyi Xu, Yuan Yao, Zonghao Guo, Junbo Cui, Zanlin Ni, Chunjiang Ge, Tat-Seng Chua, Zhiyuan Liu, Maosong Sun, and Gao Huang. Llava-uhd: an lmm perceiving any aspect ratio and high-resolution images. arXiv preprint arXiv:2403.11703, 2024. 2
- [46] Zhewei Yao, Xiaoxia Wu, Cheng Li, Stephen Youn, and Yuxiong He. Zeroquant-v2: Exploring post-training quantization in llms from comprehensive study to low rank compensation. arXiv preprint arXiv:2303.08302, 2023. 6
- [47] Xiang Yue et al. Mmmu: A massive multi-discipline multimodal understanding and reasoning benchmark for expert agi. In Proceedings of CVPR, 2024. 4
- [48] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training,

2023. 4

- [49] Kaichen Zhang, Bo Li, Peiyuan Zhang, Fanyi Pu, Joshua Adrian Cahyono, Kairui Hu, Shuai Liu, Yuanhan Zhang, Jingkang Yang, Chunyuan Li, and Ziwei Liu. Lmmseval: Reality check on the evaluation of large multimodal models, 2024. 4
- [50] Yi-Fan Zhang, Weichen Yu, Qingsong Wen, Xue Wang, Zhang Zhang, Liang Wang, Rong Jin, and Tieniu Tan. Debiasing multimodal large language models. CoRR, 2024. 3


- [51] Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher R´e, Clark Barrett, et al. H2o: Heavy-hitter oracle for efficient generative inference of large language models. Advances in Neural Information Processing Systems, 36: 34661–34710, 2023. 1
- [52] Han Zhao, Min Zhang, Wei Zhao, Pengxiang Ding, Siteng Huang, and Donglin Wang. Cobra: Extending mamba to multi-modal large language model for efficient inference. arXiv preprint arXiv:2403.14520, 2024. 2
- [53] Yilong Zhao, Chien-Yu Lin, Kan Zhu, Zihao Ye, Lequn Chen, Size Zheng, Luis Ceze, Arvind Krishnamurthy, Tianqi Chen, and Baris Kasikci. Atom: Low-bit quantization for efficient and accurate llm serving. Proceedings of Machine Learning and Systems, 6:196–209, 2024. 1
- [54] Zixuan Zhou, Xuefei Ning, Ke Hong, Tianyu Fu, Jiaming Xu, Shiyao Li, Yuming Lou, Luning Wang, Zhihang Yuan, Xiuhong Li, et al. A survey on efficient inference for large language models. arXiv preprint arXiv:2404.14294, 2024. 1
- [55] Yichen Zhu, Minjie Zhu, Ning Liu, Zhicai Ou, Xiaofeng Mou, and Jian Tang. Llava-phi: Efficient multi-modal assistant with small language model, 2024. 2


## MBQ: Modality-Balanced Quantization for Large Vision-Language Models Supplementary Material

![image 4](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile4.png)

Multiply (GEMV), which is memory-bound.

Describe this image

### 7. Related Work

Tokenizer ViT Encoder

#### 7.1. LLM Quantization

| | |
|---|---|
| | |


Post-Training Quantization (PTQ) techniques are widely used in LLMs to accelerate the inference process. They employ the low-precision data format and computation to reduce the memory and computation overhead.

Large Vision-Language Model

To accelerate the memory-bound decode stage of LLMs, existing methods apply weight-only quantization to reduce the memory access overhead. GPTQ [15] quantizes one weight channel at each step and iteratively adjusts the unquantized weights to mitigate reconstruction errors of each transformer block. AWQ [27] searches for proper channelwise equalization factors by minimizing the block-wise reconstruction loss. SpQR and LLM-MQ [14, 23] propose mixed-precision quantization to allocate higher precision for weight outliers, while the rest of the weights are quantized to low-precision. QuIP [7] introduces LDLQ, an optimal adaptive method for a quadratic proxy objective. It reveals that ensuring incoherence between weight and Hessian matrices can enhance the effectiveness of LDLQ. QuIP utilizes LDLQ and achieves incoherence by employing random orthogonal matrix multiplication.

Fancy desert

Prefill Stage Decode Stage

Figure 2. The inference process of Large VLMs. The blue patches represent language tokens, the red patches represent vision tokens.

### 6. Additional Preliminaries

#### 6.1. The Inference Process of VLMs

The inference process of VLMs is shown in Fig. 2. The whole inference system consists of three key components:

- • Language Tokenizer: Transform natural language sentences into a series of language tokens.
- • ViT Encoder: Transform images into a series of vision tokens.
- • Large VLM: Take the language and vision tokens as input, and generate language tokens one by one.


To accelerate the compute-bound prefill stage of LLMs, existing methods propose to use the weight-activation quantization to leverage faster low-precision tensor cores. SmoothQuant [43] employs a channel-wise equalization technique to address the challenges of quantizing activation values. This method expands the data range of weight channels while shrinking the data range of corresponding activation channels to achieve better data equalization. Omniquant [39] optimizes the boundaries for weight clipping and the scaling factor for equivalent transformation to minimize reconstruction errors block-by-block. Atom [53] employs a strategy involving mixed-precision and dynamic quantization for activations. Recently, many studies [3, 33] follow the computational invariance idea, by multiplying rotation matrices to the weight matrices and activation matrices.

Specifically, the transformer-based [42] VLMs have two distinctive stages, including the prefill and the decode stages. Take batch size = 1 as an example.

During the prefill stage, VLMs can take both vision tokens and language tokens as the input prompt. In this stage, VLMs aim to understand both the vision and language information and the connections across each modality. The Key and Value tensors of each attention block in VLMs are stored as the KV Cache to save the computation overhead in the decode stage. The input activation of each layer is typically a large 2D matrix, making the primary computation operation in the prefill stage the General Matrix Multiply (GEMM), which is compute-bound.

However, these methods focus solely on a single language modality without considering the differences between tokens from different modalities in multimodal scenarios, which is the core distinction between MBQ and existing quantization approaches. It is also worth noting that many existing studies search for various hyperparameters by minimizing reconstruction error, where MBQ can be used to achieve performance improvements with these methods on VLMs.

During the decode stage, VLMs take one generated token from step t as the input and use the KV Cache to generate the next token of step t+1. The generation of the current token depends on one previously generated token and the KV Cache. In this case, the input activation of each layer is typically a large 1D vector, and the main computation operator in the decode stage is the General Matrix-Vector

Error Types Total

Model Bitwidth Method

No Output Randomness Repetition Condition Missing Semantic Error Bad Cases LLaVA-onevision-7B W4A8

SQ 61 16 15 32 25 149 MBQ 3 0 2 3 37 45

AWQ 30 0 3 11 42 86 MBQ 0 0 1 0 37 38

LLaVA-onevision-72B W3

Table 10. The number of samples for the five error types in the LLaVA-bench-in-the-wild [31] and LLaVA-bench-wilder [20] dataset. The total number of samples is 188. “SQ” is short for SmoothQuant.

- 7.2. Efficient VLM

To improve the efficiency of Large Vision-Language Models, existing work primarily focuses on designing lightweight modules, compressing vision tokens, and employing efficient model architectures.

Firstly, for the lightweight model design, an effective approach is to incorporate efficient components within the VLMs. Some research [5, 55] directly utilizes pre-trained small language models with fewer than 3B parameters as their backbone, while others [12] train a small language model from scratch. For modality alignment, [1, 22] utilizes a lightweight transformer, while subsequent work [11, 21, 28, 31] directly adopts Linear or MLP layers to align the visual modality with the language model’s latent space.

Secondly, the number of vision tokens increases with image resolution, imposing a substantial computational burden on VLMs. To address this issue, [6, 38, 45] propose vision token reduction techniques to significantly lower the number of vision tokens, while some approaches [9, 30] remove redundant vision tokens to reduce computational overhead.

Finally, in terms of efficient architectures, some work [26, 35] leverages the Mixture of Experts (MoE) architecture to enhance model performance without increasing active parameter counts, while others [37, 52] adopt efficient Mamba language models as the language backbone.

- 8. Additional Experiments


- 8.1. W4A16 and W8A8 Results on Large VLMs


As shown in Tab. 11, we present the evaluation results for W4A16 and W8A8 quantized VLMs from the LLaVAonevision, InternVL2, and Qwen2-VL families. In most cases, the proposed MBQ achieves accuracy comparable to the AWQ and SmoothQuant baselines under W4A16 and W8A8 quantization. Furthermore, the average accuracy of the quantized VLMs is very close to that of the original FP16 VLMs, indicating that quantization under W4A16 and W8A8 is nearly lossless.

A notable different case arises during the W4A16 quantization of LLaVA-onevision-72B, where AWQ significantly degrades the VLM’s accuracy, with the average accuracy

falling more than 10% below that of MBQ and RTN. A similar phenomenon also occurs during W3A16 quantization of LLaVA-onevision-72B in Tab. 10, demonstrating that the modality-balancing concept proposed by MBQ can more consistently maintain high model performance compared to SOTA quantization baselines, whether in high-bitwidth or low-bitwidth quantization scenarios.

#### 8.2. Case Studies

To evaluate the open-ended conversational ability of the quantized VLMs, we evaluate the proposed MBQ alongside state-of-the-art baselines on the LLaVA-onevision family using conversation benchmarks. As shown in Tab. 10, we find that MBQ can significantly outperform SOTA baseline methods when applied to weight-activation quantization for LLaVA-onevision-7B and weight-only quantization for LLaVA-onevision-72B. Therefore, we analyze the conversation results of VLMs under these two quantization schemes.

Specifically, we manually evaluated the responses of the quantized VLM to each question and identified the following five frequently occurring error types:

- 1. No output: The quantized VLM generates no or only a few valid tokens, as shown in Example 2;
- 2. Randomness: The quantized VLM randomly generates meaningless symbols, as shown in Example 4;
- 3. Repetition: The quantized VLM keeps repeating some certain tokens, as shown in Example 1 and Example 6;
- 4. Condition Missing: The quantized VLM misses the key points in the questions as shown in Example 3;
- 5. Semantic Error: The quantized VLM can understand the questions but still generates wrong answers with meaningful and fluent language, as shown in Example 5.


We summarize the number of samples corresponding to the above five error types for each quantized VLM, the results are shown in Tab. 10.

For the LLaVA-onevision-7B with W4A8 quantization, MBQ results in only 45 total bad cases, which is 104 fewer than the 149 bad cases observed with SmoothQuant. Specifically, the most common type of bad case of SmoothQuant is “No Output”. For instance, in Example 2, the W4A8

Model Bitwidth Method MMMU SEED OCRBench VizWiz ScienceQA TextVQA Average (↑)

FP16 - 46.0 74.9 62.2 60.4 85.4 76.1 67.5 RTN 44.9 74.6 61.7 59.6 89.8 75.3 67.6 W4A16 AWQ 44.6 74.7 61.8 59.1 90.1 75.8 67.7 LLaVA-onevision-7B MBQ 44.4 74.7 62.1 59.3 90.2 75.6 67.7

RTN 46.3 74.8 63.5 60.5 90.3 75.9 68.6 W8A8 SQ 46.0 74.9 63.2 60.7 90.3 75.7 68.5

MBQ 45.6 74.7 62.6 61.0 90.2 75.7 68.3 FP16 - 48.0 76.0 76.5 61.1 96.2 77.0 72.5 RTN 47.6 75.9 75.6 60.1 96.0 76.2 71.9 W4A16 AWQ 47.1 75.8 76.7 60.1 96.3 76.4 72.1 InternVL2-8B MBQ 48.9 75.9 76.7 60.8 96.3 76.5 72.5

RTN 47.4 76.2 77.3 61.0 96.2 76.9 72.5 W8A8 SQ 48.0 76.1 77.1 61.0 96.1 76.9 72.5

MBQ 48.0 76.0 77.4 61.0 96.4 77.0 72.6 FP16 - 50.6 76.4 80.7 68.3 85.1 82.0 73.8 RTN 50.2 76.0 80.1 67.4 84.5 81.2 73.2 W4A16 AWQ 50.1 76.1 80.4 68.4 85.0 81.7 73.6 Qwen2-VL-7B MBQ 50.0 76.3 80.8 68.6 84.6 81.4 73.6

RTN 49.4 76.3 80.9 68.2 84.5 81.2 73.4 W8A8 SQ 50.1 76.3 80.6 68.5 85.0 81.5 73.7

MBQ 50.1 76.4 80.7 68.3 85.4 81.8 73.8 FP16 - 56.1 78.1 73.2 69.2 90.0 79.3 74.3 RTN 56.2 77.9 72.1 68.8 90.4 78.9 74.1 W4A16 AWQ 39.1 75.9 58.1 59.9 80.4 69.1 63.8 LLaVA-onevision-72B MBQ 56.4 77.9 72.3 69.0 90.3 79.3 74.2

RTN 56.8 78.0 73.1 69.4 90.3 79.2 74.5 W8A8 SQ 56.3 78.0 72.7 69.2 89.7 79.0 74.2

MBQ 56.2 78.1 73.1 69.2 89.8 79.1 74.3 FP16 - 47.1 76.8 77.9 66.2 97.5 82.1 74.6 RTN 48.2 76.8 78.0 64.6 97.1 81.8 74.4 W4A16 AWQ 47.4 76.8 77.1 65.9 97.3 82.0 74.4 InternVL2-26B MBQ 47.2 76.8 77.5 65.4 97.5 82.1 74.4

RTN 47.4 76.5 78.4 65.1 97.3 81.7 74.4 W8A8 SQ 48.1 76.7 78.3 65.5 97.4 82.0 74.7

MBQ 47.9 76.8 78.1 66.2 97.5 82.0 74.8 FP16 - 61.1 77.6 79.9 76.0 91.6 82.5 78.1 RTN 59.8 77.7 79.6 75.8 91.3 82.6 77.8 W4A16 AWQ 61.9 77.5 79.5 75.8 92.2 82.4 78.2 Qwen2-VL-72B MBQ 60.8 77.6 79.9 75.8 92.8 82.3 78.2

RTN 60.4 77.5 79.5 75.7 90.9 82.2 77.7 W8A8 SQ 60.3 77.5 79.7 76.1 91.3 82.0 77.8

MBQ 60.7 77.6 79.9 75.9 91.4 82.4 78.0

Table 11. Additional results on LLaVA-onevision, InternVL2, and Qwen2-VL families. “SQ” is short for SmoothQuant.

VLM using SmoothQuant fails to generate any meaningful tokens in response to the provided question. In contrast, with MBQ, the W4A8 VLM experiences only 3 “No Output” bad cases. Additionally, while MBQ leads to

more“Semantic Error” cases than SmoothQuant, this is because SmoothQuant often produces outputs that are not even fluently generated, whereas MBQ enables the quantized VLM to generate fluent responses, thereby increasing

the potential for “Semantic Error” cases.

For the LLaVA-onevision-72B with W3A16 quantization, a similar trend is observed as with the LLaVAonevision-7B using W4A8 quantization. MBQ results in only 38 bad cases, which is 48 fewer than the 86 bad cases reported for AWQ. Specifically, the most frequent type of bad case for the AWQ baseline is still “No Output”. This indicates that AWQ can still lead to VLM failing to generate meaningful and fluent responses in many situations, while MBQ significantly alleviates this type of bad case, narrowing the issues down to “Semantic Errors”.

Question: Who painted this artwork, and what is its significance in the art world?

![image 5](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile5.png)

FP16 Response: This artwork was painted by Vincent van Gogh, a post-impressionist painter known for his vibrant use of color and emotional intensity. “The Starry Night” is significant in the art world as it exemplifies Van Gogh’s unique style and his ability to evoke emotion through his paintings. It has become one of the most recognized and celebrated works of post-impressionism, symbolizing hope and the beauty of the night sky.

SmoothQuant Response: This artwork was painted by Vincent van Gogh titled Nightsky Landscape With Bright Starry Sky Above Sleeping Townscape Surrounding Wind Blowing Trees And Hills In Background Van Gogh Postcard Print Poster Blanket Pillowcase Pillow Box Pillow Blanket Pillow Box Pillow Box Pillow Blanket Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow ow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow Box Pillow

** Error Type: Repetition.

MBQ Response: This artwork is painted by Vincent van Gogh, titled “The Starry Night.” It’s significant in the art world because it exemplifies Van Gogh’s unique post-impressionist style and emotional intensity. The swirling patterns in the sky are iconic and have become synonymous with Van Gogh’s expressive technique. This painting also signifies his fascination with the cosmos and has been interpreted as an expression of hope amidst darkness.

Question: Describe this photo in detail.

![image 6](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile6.png)

FP16 Response: The image is a digitally created artwork that combines elements of Renaissance art with modern humor. It features a dog’s head, specifically that of a dachshund, seamlessly integrated into the iconic pose and attire of Leonardo da Vinci’s “Mona Lisa.” The dog’s face is superimposed onto the original painting, maintaining the Mona Lisa’s enigmatic expression and posture. The background remains consistent with the original, depicting a distant landscape with a river and mountains under a cloudy sky. The dog’s fur color matches the original’s flesh tones, and its ears are styled to resemble the Mona Lisa’s hair. The overall effect is a playful fusion of classical art and contemporary animal imagery.

SmoothQuant Response: The image presents itself uniquely

** Error Type: No Output. The quantized VLM can only generate a few meaningless tokens.

MBQ Response: This image is a playful rendition of Leonardo da Vinci’s famous painting, the Mona Lisa. However, instead of the original human subject, this version features a dog, specifically a brown dachshund, in place of the Mona Lisa. The dog is portrayed with a slight smile, adding a touch of whimsy to the piece. The background maintains the original’s serene landscape of mountains and a calm river. The art style is a fusion of Renaissance painting techniques with a modern twist, reflecting the artist’s creative flair.

Question: What is the atmosphere and setting depicted in the image, and how do the elements contribute to creating a relaxing environment?

![image 7](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile7.png)

FP16 Response: The atmosphere depicted in the image is one of tranquility and relaxation. The setting is a cozy living room bathed in soft, warm light that suggests it’s either dawn or dusk. The presence of the person sitting crosslegged on the floor with headphones on, along with the calm posture and the cup of coffee, implies they are enjoying some quiet time, possibly listening to music. The room’s decor, including framed pictures and plants, adds to the homely and peaceful ambiance. The sunlight streaming through the window enhances the serene mood, making it an ideal space for unwinding.

SmoothQuant Response: The atmosphere depicted suggests tranquility amidst warmth—an ideal setting conducive to relaxation—one might even say therapeutic listening experience.

** Error Type: Condition Missing. The quantized VLM fails to address the question: “How do the elements contribute to creating a relaxing environment?”

MBQ Response: The atmosphere depicted in the image is one of tranquility and relaxation. The setting appears to be a cozy living room designed for comfort and leisure, with warm lighting that suggests either sunrise or sunset. Elements such as plush cushions on the floor, soft lighting from the pendant lamp, and the presence of calming artwork contribute to this relaxing ambiance. Additionally, the person’s posture while listening to music through headphones indicates immersion in the music, suggesting that they are enjoying a peaceful moment alone.

Question: What model is this car, and can you provide some specifications and performance details about it?

![image 8](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile8.png)

FP16 Response: This car is a Bugatti Chiron, known for its exceptional performance and luxury. It features an 8.0-liter, 16-cylinder engine that produces 1,500 horsepower and 1,300 lb-ft of torque. The Chiron can accelerate from 0 to 60 mph in just 2.4 seconds and has a top speed electronically limited to 261 mph. Its advanced engineering and craftsmanship make it one of the fastest and most exclusive cars in the world.

AWQ Response: This is a Bugatti Veyron,EBu,Chirona/EB110,EB110/EB110/EB110/EB110/EB110/EB110/EB110

/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110 /EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110 /EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110 /EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110 /EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110 /EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110/EB110 /EB110/EB110

** Error Type: Randomness. The quantized VLM generates random symbols such as “EBu” and “/EB100”.

MBQ Response: This is a Bugatti Chiron, known for its incredible performance. It boasts an 8.0-liter, 16-cylinder engine that produces 1,479 horsepower and 1,300 lb-ft of torque. The Chiron can accelerate from 0 to 60 mph in just 2.4 seconds and has a top speed electronically limited to 261 mph.

Question: Imagine the fragrance of the fruits in the image. How would you describe this to someone who has never had this fruit before?

![image 9](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile9.png)

FP16 Response: The fragrance of the mangosteen is a delightful blend of sweet and slightly tart notes, reminiscent of a combination of strawberries, kiwi, and pineapple. It’s a fresh and inviting aroma that hints at the juicy and flavorful experience one is about to encounter when tasting the fruit.

AWQ Response: The mangos fruit in the image has a unique fragrance that is both sweet and slightly tart. The sweetness is reminiscent to a combination of honey and a hint of citrus, while the tartness comes from a subtle tang of earthy undertones. When you bite into it, the initial sweetness gives way to a tangy, lingering taste that lingers on your tongue, leaving you with a pleasant and refreshing aftertaste.

** Error Type: Semantic Error. The quantized VLM mistakenly identified mangosteens as mangoes.

MBQ Response: The fragrance of the mangosteen is a delightful blend of tropical sweetness and subtle floral notes. Imagine a scent that is both refreshing and rich, akin to a combination of strawberries and kiwi with a hint of rose petals. It’s a fragrance that promises a burst of flavor and freshness, inviting you to take a bite and experience its unique taste.

Question: Write brief HTML/JS to turn this mock-up into a colorful and interactive website, where the joke is replaced by a real joke.

![image 10](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile10.png)

##### FP16 Response:

![image 11](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile11.png)

AWQ Response: AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-ASAS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-AS-...

** Error Type: Repetition.

##### MBQ Response:

![image 12](li-hu-ning-2025-mbq-modality-balanced-quantization_images/imageFile12.png)

