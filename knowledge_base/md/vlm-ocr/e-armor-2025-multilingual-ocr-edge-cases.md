# E-ARMOR: Edge case Assessment and Review of Multilingual Optical Character Recognition

Aryan Gupta

Intern Sprinklr Gurgaon, India

Sanskar Soni

AI Team

Sprinklr Gurgaon, India

Nuruddin J.

AI Team

Sprinklr Gurgaon, India

Shushant Kumar

AI Team

Sprinklr Gurgaon, India

Anupam Purwar∗

AI Team

Sprinklr Gurgaon, India

Ratnesh Jamidar

AI Team

Sprinklr Gurgaon, India

## arXiv:2509.03615v1[cs.CL]3 Sep 2025

Abstract—Optical Character Recognition (OCR) in multilingual, noisy, and diverse real-world images remains a significant challenge for optical character recognition systems. With the rise of Large Vision-Language Models (LVLMs), there is growing interest in their ability to generalize and reason beyond fixed OCR pipelines. In this work, we introduce Sprinklr-Edge-OCR, a novel OCR system built specifically optimized for edge deployment in resource-constrained environments. We present a large-scale comparative evaluation of five state-of-the-art LVLMs (InternVL, Qwen, GOT OCR, LLaMA, MiniCPM) and two traditional OCR systems (Sprinklr-Edge-OCR, SuryaOCR) on a proprietary, doubly hand annotated dataset of multilingual (54 languages) images. Our benchmark covers a broad range of metrics including accuracy, semantic consistency, language coverage, computational efficiency (latency, memory, GPU usage), and deployment cost. To better reflect real-world applicability, we also conducted edge case deployment analysis, evaluating model performance on CPU only environments. Among the results, Qwen achieved the highest precision (0.54), while Sprinklr-EdgeOCR delivered the best overall F1 score (0.46) and outperformed others in efficiency, processing images 35× faster (0.17 seconds per image on average) and at less than 0.01× of the cost (0.006 USD per 1,000 images) compared to LVLM. Our findings demonstrate that the most optimal OCR systems for edge deployment are the traditional ones even in the era of LLMs due to their low compute requirements, low latency, and very high affordability.

Index Terms—Optical Character Recognition (OCR), Large Vision-Language Models (LVLMs), Multilingual Text Recognition, Semantic Accuracy, Edge Deployment.

I. INTRODUCTION

Optical Character Recognition (OCR) is a cornerstone technology for digitizing documents, automating data entry, and extracting information from images containing typed, handwritten, or printed text. It is the process of converting images containing typed, handwritten, or printed text into actual text data.

Traditional Optical Character Recognition (OCR) systems generally follow a multi stage pipeline encompassing four key steps: image pre-processing, layout analysis, character recognition, and post-processing. In the first stage, the input image is enhanced using techniques such as binarization, noise reduction, deskewing, and normalization to improve text clarity. Next, layout analysis or segmentation identifies textual regions, distinguishing them from non-textual elements like

∗Corresponding Author: Anupam Purwar (e-mail: anupam.aiml@gmail.com, https://anupam-purwar.github.io/page/)

graphics, and further segments them into lines, words, and characters. Character recognition follows, where each segmented character is identified using pattern recognition methods, typically involving feature extraction from the bitmap and classification via trained models. Finally, post-processing refines the output by incorporating linguistic context, including spell checking, error correction through n-gram models, and formatting adjustments; for instance, resolving ambiguities such as “an” versus “ar” based on likely language patterns. While effective in controlled environments, these pipelines are often brittle. Their performance degrades significantly with complex layouts, varied fonts, image distortions, and multilingual text, as each stage is prone to cascading errors.

Large Vision-Language Models (LVLMs) mark a significant departure from traditional approaches to visual information processing by enabling joint understanding of images and text within a unified framework. These multimodal models typically integrate a pre-trained vision encoder, such as a Vision Transformer (ViT) [4], with a Large Language Model (LLM), like LLaMA. The vision encoder first transforms the input image into a sequence of embeddings that capture its visual features. These embeddings are then projected into the same vector space as the LLM’s text embeddings via a specialized projection layer. Both the projected visual features and a user provided textual prompt are passed into the LLM, which generates a response by attending to both visual and textual inputs. Unlike traditional OCR systems that rely on fragile, multistage pipelines for segmentation and character recognition, LVLMs adopt an end-to-end reasoning approach that mimics human like understanding of visual scenes. This paradigm enables them to interpret text in context, offering several advantages: they eliminate the need for explicit character segmentation, support zero shot generalization across diverse languages and fonts, exhibit robustness against real world noise such as glare or skew, and provide prompt based control over outputs. With the help of prompt engineering, these models can be conditioned to generate OCR outputs for the inputted image. However, the high computational requirements of LVLMs often limit their deployment in resource constrained settings.

Despite these advances, there remains a critical gap in understanding the practical trade offs between traditional OCR systems and LVLM based approaches, particularly in multilingual, noisy, and real world scenarios. Most existing bench-

marks focus on monolingual or clean datasets, and very few studies systematically evaluate both accuracy and deployment efficiency such as latency, memory usage, and cost across a wide range of languages and real world conditions [27] [7]. There is a lack of comprehensive, real-world benchmarking that compares the performance and deployment feasibility of state-of-the-art LVLMs and traditional OCR systems on multilingual, noisy, and diverse image datasets, especially in resource-constrained environments.

Edge devices such as Raspberry Pi boards, smartphones, and embedded systems are increasingly used in real world OCR applications due to their portability and cost effectiveness. However, these devices typically operate under severe resource constraints, offering limited RAM (often between 1GiB to 8GiB), modest storage capacity, and low power CPUs or mobile GPUs. Unlike cloud based infrastructure, they lack the memory bandwidth and parallel compute required to run large scale transformer models in real time. As a result, deploying OCR models on such platforms requires careful optimization for latency, memory footprint, and inference efficiency, often through quantization, pruning, and hardware specific acceleration [32] [33].

In this work, we showcase Sprinklr-Edge-OCR, a compute optimized OCR system suited for edge deployment and inspired by PaddleOCR framework [5]. The proposed system incorporates multiple proprietary enhancements over the standard Paddle Structure pipeline, emphasizing modular design, reduced latency, and minimal memory usage. Our model introduces an optimized detection-recognition architecture paired with TensorRT accelerated inference, making it ideal for real time applications on devices with limited resources.

Building on this foundation, we present a comprehensive evaluation of comparison of both traditional OCR engines and state-of-the-art Large Vision-Language Models (LVLMs). Though comprehensive assessment of LLMs is reported [34] and prior studies which benchmark only standard or cloudbased OCR models, our approach is tailored for low-resource environments, enabling efficient and accurate text extraction on devices with limited computational capacity [30]. To the best of our knowledge, this is the first comprehensive comparative report that systematically evaluates both state-ofthe-art Large Vision-Language Models (LVLMs)—including InternVL, Qwen, GOT OCR, LLaMA, and MiniCPM—and traditional OCR systems (including our proposed SprinklrEdge-OCR and SuryaOCR) across a proprietary, doubly handannotated dataset spanning 54 languages and diverse, noisy, real-world image conditions [12] [15] [18] [21] [16]. Our benchmarking is uniquely novel in its focus on standardized testing for deployment efficiency, encompassing not only accuracy and semantic consistency but also critical metrics such as latency, memory footprint, GPU/CPU usage, and operational cost. Unlike existing research, which typically overlooks the practicalities of low-resource deployment and the impact of model quantization, our study provides actionable insights for practitioners seeking robust OCR solutions in language-rich and computationally constrained settings [29] [28].

![image 1](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile1.png)

Fig. 1. Distribution of Languages in the OCR Evaluation Dataset. The bar chart displays the percentage wise distribution of languages present in the OCR evaluation dataset. English overwhelmingly dominates the dataset, accounting for over 80% of the total samples. Other languages such as Chinese, Japanese, Korean, and Arabic are represented to a much lesser extent, each comprising less than 10% of the dataset. The ”Other” category includes several low resource and underrepresented languages. This skewed distribution reflects the real world prevalence of English language content in public datasets but also highlights the importance of evaluating model robustness across diverse linguistic contexts, especially in multilingual and non Latin script scenarios.

Our results demonstrate that, despite the impressive capabilities of LVLMs, quantized and optimized traditional OCR systems like Sprinklr-Edge-OCR offer superior performance for edge deployment, achieving lower latency, reduced memory usage, and minimal cost without sacrificing accuracy. This work sets a new standard for OCR benchmarking and deployment, bridging the gap between academic research and real-world application in multilingual, resource-limited environments.

II. METHODOLOGY

We curated a challenging, real-world dataset comprising of images with 54 distinct languages, with the majority of the images containing text written in English, Chinese, Japanese, Korean and Arabic (see Figure 1). The dataset has a high diversity of content, which includes posters, city view, memes, screenshots, and advertisements containing multilingual text, complex layouts, and various visual artifacts. To establish a high quality ground truth for evaluation, each image was doubly annotated by humans. Figure 2 illustrates the distribution of word counts per image, most images contain fewer than 10 words, with a long tail extending past 150. The distribution is highly skewed, indicating that while most images are text sparse (e.g., signs, labels, short messages), a smaller subset includes dense textual content such as documents, tables, or webpages. This variability poses challenges for OCR models, which must generalize across both minimal and high-density text scenarios.

A. Models

The models listed in Table 1 were selected to represent a diverse cross section of state-of-the-art open source OCR systems, spanning both traditional and modern deep learning approaches. Selection criteria included multilingual support, architectural diversity (from lightweight pipelines to large

![image 2](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile2.png)

- Fig. 2. Distribution of Word Counts per Image in the Dataset. The histogram shows the distribution of the number of words per image across the dataset. The majority of images contain a relatively small number of words, with a sharp peak at fewer than 10 words per image, and a long tail extending beyond 150 words.


TABLE I OVERVIEW OF POPULAR OPEN SOURCE OCR AND LVLMS. THE TABLE SUMMARIZES A RANGE OF WIDELY USED OPEN SOURCE OCR MODELS, INDICATING WHETHER THEY SUPPORTS MORE THAN FOUR LANGUAGES.

|Name<br><br>|Supports more than 4 Languages?|
|---|---|
|TesseractOCR (CPU only) [14] MMOCR [9] TrOCR [10] DOCTR [11] PARSEQ [2] ABINet [6] Smoldocling [26] Bridging-Text-Spotting [25] PyLaila [22] Kraken [23] (historical languages) InstructOCR [24] Paddle Structure [5] Sprinklr-Edge-OCR Surya [12] QWEN VL [1] Llama 3.2 V [15] GOT OCR 2.0 [16] InternVL [21] MiniCPM-V-2.6 [18]|Yes No No No No No No No No No No Yes Yes Yes Yes Yes Yes Yes Yes<br><br>|


multimodal models), availability of pretrained weights. This variety ensures a comprehensive evaluation across different document types, languages, and deployment scenarios.

Sprinklr-Edge-OCR engine is built upon the PaddleOCR framework, specifically optimized for edge deployment [5]. Unlike the traditional Paddle-Structure-v3 pipeline, which employs a comprehensive suite of modules, including layout detection, chart and table engines, and document orientation classification, our approach focuses on essential OCR tasks and integrates several proprietary modifications aimed at optimizing performance for resource constrained environments. These proprietary enhancements are based on recent advancements in lightweight and modular OCR design, resulting in a compact and efficient system (see Figure 3). To further boost run-time performance, the engine integrates TensorRT for accelerated inference on supported hardware. The engine supports multiple languages, including simplified Chinese, Chinese Pinyin, Traditional Chinese, English, and Japanese,

with extensibility to others through fine tuning. Designed for high-throughput, latency-sensitive edge applications. SprinklrEdge-OCR delivers strong recognition accuracy while maintaining a minimal computational footprint and delivers a highly compact, efficient, and scalable solution. The result is a state-of-the-art OCR system that is ideally suited for highthroughput, latency-sensitive applications at the edge, without sacrificing recognition accuracy.

The datalab’s toolkit SuryaOCR is a comprehensive, open-source document analysis suite that offers OCR, layout analysis, reading order detection, and table recognition in more than 90 languages. It leverages a SegFormer based detection model and a DONUT based recognition backbone [17] [8], delivering comparable performance to traditional engines like Tesseract and cloud services. It supports line-level text detection, structural region classification (e.g., headers, images, tables), and multi-column, right-to-left reading flow reconstruction. Outputs include richly annotated JSON with bounding boxes, polygons, confidence scores, and semantic region labels, as well as optional visual overlays.

The General OCR Theory 2.0 (GOT OCR 2.0) is a unified, end-to-end model designed to handle a diverse range of artificial optical signals, including plain text, mathematical formulas, molecular structures, tables, charts, sheet music, and geometric shapes. Developed by Haoran Wei et al., GOT OCR 2.0 uses a high compression encoder and a longcontext decoder to process and generate output from visual input. The encoder compresses 1024×1024 pixel images into 256 tokens of size 1024, while the decoder, based on the Qwen-0.5B model, can handle long contexts up to 8,000 tokens. Key features of GOT OCR 2.0 include interactive OCR with region-level recognition guided by coordinates or colors, dynamic resolution handling for ultra-high-resolution images, multi-page OCR capabilities, and support for various output formats such as plain text, Markdown, TikZ, SMILES notation, and LaTeX. These advancements make GOT OCR 2.0 a versatile tool for complex OCR tasks across different domains.

The OpenGVLab-InternVL2.5-1B is a multimodal foundation model designed for a wide range of vision-language tasks. It employs a ”ViT-MLP-LLM” architecture, integrating a Vision Transformer (InternViT-300M-448px-V2 5) for image processing, a Multilayer Perceptron (MLP) projector for crossmodal alignment, and a Large Language Model (Qwen2.50.5B-Instruct) for text understanding. This design allows the model to process and understand single images, multi-image datasets, and videos, with inputs resized to 448x448 pixels and normalized using ImageNet statistics [3]. InternVL2.5-1B has demonstrated strong performance across various benchmarks, including OCR, chart, and document understanding, as well as visual grounding and video comprehension tasks. Its architecture enables efficient processing and understanding of complex multimodal data, making it a versatile tool for applications requiring integrated vision and language capabilities.

The Unsloth/Llama-3.2-11B-Vision-Instruct 4Bit is a vision language model developed by Meta and optimized by Unsloth.

![image 3](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile3.png)

- Fig. 3. SE-OCR system pipeline for text extraction. The SE-OCR framework operates in two stages: text detection and text recognition. Given an input image containing text, the detection module first localizes individual text regions. These cropped regions are then passed to the recognition module, which transcribes the content into machine readable text. The final output is a sequence of recognized text tokens, accurately reflecting the textual information present in the original image.


It combines an 11-billion-parameter Llama 3.2 architecture with a vision adapter, enabling the model to process and understand both visual and textual inputs. The model utilizes Unsloth’s Dynamic 4-bit quantization, achieving approximately 2x faster inference and 60% reduced memory usage compared to the original implementation. This optimization allows for efficient deployment on consumer grade GPUs. The architecture includes a Vision Transformer (ViT) for image processing, cross-attention layers to integrate visual and textual information, and a language model to generate responses. It supports a wide range of vision-language tasks, including image captioning, visual question answering, and multimodal reasoning. In addition, it supports long context lengths, which improves its ability to handle extended conversations and complex visual inputs.

The openbmb/MiniCPM-V-2 6-int4 is a compact 8 billionparameter multimodal large language model (MLLM) optimized for edge devices. It integrates components from SigLip400M, and Qwen2-7B, delivering robust performance across vision, and language tasks [19]. We employ 4-bit quantization to enhance efficiency, enabling deployment on consumer grade hardware. It supports high resolution image processing and optical character recognition (OCR). Additionally, MiniCPMV-2 6-int4 offers real time continuous video/audio processing, multilingual support for English, Chinese, German, French, Italian, Korean, etc. Its versatility and efficiency, extremely low token density (i.e., number of pixels encoded into each visual token) make it suitable for a wide range of applications, including real time conversation, and multimodal streaming.

The JackChew/Qwen2-VL-2B-OCR is a specialized multimodal large language model (MLLM) developed to enhance optical character recognition (OCR) capabilities. It is a fine tuned version of Qwen2-VL-2B-Instruct, which employs a Vision Transformer (ViT - 600 M params) for image processing and QWEN2 large language models for text understanding. The model utilizes a dynamic resolution mechanism called Naive Dynamic Resolution support, allowing it to process images of varying sizes and complexities, thereby improving recognition accuracy across diverse image types and sizes.

Fine tuning ensures Qwen2-VL-2B-OCR particularly is more effective for applications requiring detailed document analysis, including form processing, invoice extraction, and multilingual text recognition.

B. Experimental Setup

The following LVLMs and OCR models were evaluated: InternVL, Qwen, GOT, LLaMA, MiniCPM, Sprinklr-EdgeOCR and SuryaOCR. Each model was provided with the same images, and the models that require prompt inputs had the same standard prompt.

![image 4](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile4.png)

All of the above mentioned models were benchmarked on NVIDIA T4 GPUs, along with 4 vCPUs (Intel Xeon Family (upto 2.5 GHz)) and 16 GiB of RAM.

The process begins with the multilingual image dataset paired with human annotated ground truth annotations. These images are passed through an OCR model, which is prompted to extract all visible text exactly as it appears. The OCR model’s output is then assessed by Qwen 3 (8B), a large language model, which is instructed to compare the OCR prediction with the ground truth and assign a similarity accuracy score. This comparison helps quantify similarity and extraction fidelity. The final benchmarking results are compiled to evaluate model performance comprehensively (see Figure 4).

C. Evaluation Metrics

To ensure a comprehensive evaluation, we employed a wide range of metrics, each providing a unique perspective on model performance. The Similarity Score (LLM Judge) metric employs the Qwen3-8B language model to evaluate word level similarity between the ground truth and the predicted text

[13] [20], as LLM as judge have shown great efficacy in evaluating ML model outputs [31]. A handcrafted prompt is provided to the model, instructing it to ignore word order, semantics, grammar, and extra content, and to focus solely on the presence of exact ground truth words within the prediction. The model returns a single digit score from 0 to 9, where:

- • 9 indicates that all ground truth words are present in the prediction.
- • 7–8 indicates most words are present, with minor omissions.
- • 4–6 indicates partial word overlap.
- • 1–3 indicates only a few ground truth words are retained.
- • 0 indicates no overlap at all.


This evaluation strategy is designed to capture nuances that traditional metrics often miss, such as spelling variations, translation errors, and word order. It reflects how much of the original textual content is in the predicted output, making it particularly useful for evaluating multilingual OCR models. Higher scores indicate stronger alignment with the source words, while lower scores highlight significant omissions or hallucinations.

III. RESULTS

The Sprinklr-Edge-OCR pipeline achieved a substantial reduction in latency, from 0.57 seconds to 0.17 seconds, and peak VRAM usage decreased from 9.7 GiB to 1.8 GiB when compared to the traditional Paddle structure pipeline. To validate competitive performance of the novel model, we ran benchmarking on sub-datasets from OCRBench v2 [7]. We evaluated our model on OCRBench v2’s English text recognition tasks, which included 3 datasets: full-page OCR, fine grained text recognition, and general text recognition. Across these three benchmarks, our model achieved an average score of 55.4/100, demonstrating competitive performance. This places it on par with many highly regarded multimodal models such as GPT-4o-mini and InternVL2.5-8B as seen in the OCRBench v2 leaderboard. Despite being lightweight and efficient, the model matches or outperforms several significantly larger models with more complex architectures.

The results highlight a contrast in edge deployment efficiency. Sprinklr-Edge-OCR outperformed Qwen-VL by more than 15× in terms of inference speed and used nearly 12× less memory. While Qwen-VL’s performance is constrained by its large model size and dependency on extensive compute resources, Sprinklr-Edge-OCR’s streamlined architecture demonstrates clear advantages for low latency, low footprint deployments on CPU.

These findings reinforce Sprinklr-Edge-OCR’s suitability for real time applications on edge devices such as embedded systems, kiosks, or offline document scanners contexts where latency, memory constraints, and power efficiency are critical.

For example, as demonstrated in our experiments, prompts can effectively guide the model to extract only the original language text, thereby avoiding unnecessary translations or image descriptions. The performance of each LVLM across

![image 5](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile5.png)

- Fig. 4. End-to-end benchmarking pipeline for OCR model evaluation. The pipeline begins with an image dataset annotated with ground truth text. The OCR model is prompted to extract the text from each image in its original language. These OCR predictions are then evaluated using the Qwen 3 8B language model, which is prompted as a language understanding system to compare the predicted text against the ground truth. The model assigns an information similarity score. Raw outputs and ground truth combined with the similarity score is then used to generate benchmarking metrics.


the evaluated metrics is summarized in Table 1. The bestperforming value for each metric is highlighted in bold. The cost calculations were based on the G4dn.xlarge AWS instance, which includes a T4 Tensor Core GPU, 4 vCPUs and 16 GiB of RAM. This instance is currently priced at $0.526 per hour under the On-Demand pricing model.

Figure 9 presents representative output examples generated by each of the evaluated models. Table 2 presents a comprehensive comparison of seven OCR systems across three key dimensions: error metrics, accuracy, and resource consumption. Among traditional OCR systems. Sprinklr-EdgeOCR consistently outperformed others, achieving the lowest Word Error Rate (WER = 0.8528) and second-best Character Error Rate (CER = 0.6713), while also recording the lowest average Levenshtein distance (109.94) and fewest missed words (18.48). Qwen VL, a Large Vision-Language Model (LVLM), showed high precision (0.5426) and the lowest average extra words (4.03), indicating strong text extraction discipline.

For overall accuracy, Sprinklr-Edge-OCR achieved the highest F1 Score (0.4570), demonstrating balanced performance in both precision and recall. MiniCPM achieved the highest recall (0.4134), though at the cost of extra words and slightly reduced precision. GOT OCR showed the best CER (0.6459), revealing strength in character-level recognition (see Figure 6 & 5).

In terms of semantic similarity, Sprinklr-Edge-OCR again led with a similarity score of 7.2, outperforming all other models.

The composite score was calculated by aggregating multiple evaluation metrics, including error rates (e.g., WER, CER), accuracy measures (e.g., F1 score, precision, recall), and similarity into a single normalized score ranging from 0 to 1, later scaled to 100 for readability. Each metric was first normalized

across all models, with higher is better metrics scaled directly and lower is better metrics inverted. The final score represents an average of these normalized values, providing a balanced view of both recognition quality and robustness. As shown in the results, Sprinklr-Edge-OCR outperformed all other models with a score of 92.6, followed by GOT (72.1) and Qwen (67.0). Models like InternVL scored significantly lower, highlighting trade offs between model type and OCR performance in realworld conditions (see Figure 8).

Sprinklr-Edge-OCR is also notable for the fastest average inference time (0.17 seconds), lowest maximum memory usage (1970 MiB), and lowest cost per 1,000 images ($0.006), making it highly suitable for real-time edge deployment. In contrast, LVLMs like MiniCPM and LLaMA consumed significantly more time, memory, and compute resources. For instance, MiniCPM’s average inference time was 13.21 seconds and peak memory usage exceeded 9.7 GiB (see Figure 7).

SuryaOCR offered moderate performance, better than InternVL and LLaMA in error metrics, but lagged behind Sprinklr-Edge-OCR in both speed and accuracy.

A. Edge Deployment Analysis on CPU

To assess the feasibility of real world deployment in resource constrained environments, we conducted CPU only inference benchmarking on a system equipped with an 8 core Intel Xeon 8375C (Ice Lake, 3.5 GHz) processor and 64 GiB of RAM. This setting simulates an edge deployment scenario where GPU access is unavailable.

We evaluated two contrasting, top-performing models: the large vision-language model QwenVL, and the lightweight, updated OCR pipeline Sprinklr-Edge-OCR (focused solely on detection and recognition). Table 3 summarizes average inference time per image and peak RAM usage during runtime

TABLE II EVALUATION OF OCR AND VISION-LANGUAGE MODELS ACROSS MULTIPLE DIMENSIONS. THE TABLE SUMMARIZES THE PERFORMANCE OF VARIOUS MODELS ACROSS THREE CATEGORIES: ERROR METRICS, ACCURACY METRICS, AND RESOURCE CONSUMPTION. THIS COMPREHENSIVE COMPARISON ENABLES ANALYSIS OF TRADE OFFS BETWEEN RECOGNITION QUALITY AND DEPLOYMENT EFFICIENCY.

### Metric InternVL Qwen GOT LLaMA MiniCPM Sprinklr-Edge-OCR Surya

Error Metrics (Lower is Better) WER 4.8320 0.8609 0.9875 2.7893 2.9658 0.8528 1.2482 CER 6.7943 1.0802 0.6459 3.9395 4.6542 0.6713 2.9562 Avg Levenshtein Dist 268.58 122.52 138.69 184.54 245.92 109.94 194.39 Avg Missed Words 26.12 23.10 22.10 22.10 19.49 18.48 24.09 Avg Extra Words 29.09 4.03 11.85 17.98 21.69 11.95 11.48 Mean Per-Word Levenshtein 2.6038 6.0008 2.2581 1.7896 1.7423 1.4949 8.0993

Accuracy Metrics (Higher is Better) F1 Score 0.1545 0.3690 0.3675 0.3193 0.3804 0.4570 0.2357 Precision 0.1573 0.5426 0.4511 0.3445 0.3833 0.5010 0.3013 Recall 0.1808 0.3149 0.3493 0.3467 0.4134 0.4398 0.2058 Similarity 4.8 6.0 5.8 5.7 6.6 7.2 6.5

Resource Consumption (Lower is Better) Params (B) 1 2 0.58 11 8 0.15 0.52 Avg Time (s) 7.02 5.83 3.64 10.21 13.21 0.17 1.16 Max Time (s) 28.67 31.59 151.07 62.07 258.61 6.32 32.62 Max Memory (MiB) 14239 12907 5857 8709 9761 1970 7471 Avg GPU Util (%) 42.57 89.76 31.16 78.41 91.26 2.07 3.51 Number of Threads 1 1 2 1 1 4 2 Cost per 1000 images ($) 1.02 0.85 0.27 1.49 1.93 0.006 0.08

![image 6](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile6.png)

- Fig. 5. Comparison of Accuracy Metrics Across OCR Models. This bar plot presents the performance of the seven selected OCR and visionlanguage models across four key accuracy metrics: F1 Score, Precision, Recall, and Similarity score. These metrics reflect the models’ ability to accurately recognize and reproduce textual content from images. Higher values indicate better performance. Among the models, SE-OCR consistently ranks highest across most metrics, notably achieving a Similarity score exceeding 7, indicating high semantic closeness between predicted and ground truth text. QWEN showcases the strongest performance in terms of precision. MiniCPM and GOT also perform well, with balanced precision and recall. In contrast, InternVL shows the lowest performance across all accuracy metrics, highlighting its limitations in text specific recognition tasks.


![image 7](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile7.png)

Fig. 6. Comparison of Error Metrics Across OCR Models (Lower is Better). The figure illustrates six key error metrics: Word Error Rate (WER), Character Error Rate (CER), Average Levenshtein Distance (scaled), Average Missed Words, Average Extra Words, and Mean Per-Word Levenshtein Distance for the seven selected OCR and vision-language models. These metrics quantify different aspects of recognition failure, including character level and word level discrepancies between predicted and ground truth text. SE-OCR consistently achieves the lowest error values across most metrics, reflecting high robustness and recognition precision. QWEn also showcases an extremely low error rate. GOT and MiniCPM also exhibit relatively low error rates, with balanced performance on both missed and extra words. In contrast, InternVL and Surya show significantly higher error rates across all dimensions, indicating poor alignment with ground truth text and increased frequency of both omissions and insertions.

IV. DISCUSSION

Our analysis reveals key qualitative insights into the behavior and trade-offs of Large Vision-Language Models (LVLMs) versus traditional OCR pipelines. LVLMs such as Qwen offer distinct advantages in multilingual and zero-shot settings,

where broader contextual reasoning and semantic alignment are essential. For instance, Qwen consistently produced output with high textual fidelity and minimal hallucinations, making it particularly suitable for applications where precision and strict adherence to source content are critical without any restrictions on available compute.

![image 8](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile8.png)

- Fig. 7. Comparison of Resource and Efficiency Metrics Across OCR Models (Lower is Better). The chart presents the computational efficiency of the seven selected OCR and vision language models, evaluated using four key resource related metrics: Model Size (in billions of parameters), Average Inference Time (in seconds), Maximum Inference Time (scaled by 1/10), and Peak Memory Usage (in GiB). Lower values across these metrics indicate better deployment efficiency. SE-OCR demonstrates exceptional efficiency, requiring minimal memory and computation time, and using significantly fewer parameters than LLM based counterparts. In contrast, MiniCPM shows the highest resource consumption, particularly in maximum inference time (peaking above 250 seconds before scaling) and memory usage. InternVL, Qwen, and LLaMA also incur high memory and parameter costs.

![image 9](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile9.png)

- Fig. 8. Composite Score Comparison Across OCR Models. The bar chart illustrates the normalized composite scores (out of 100%) for the seven OCR and vision-language models. Among all models, Sprinklr-Edge-OCR achieves the highest composite score at 92.6%, indicating strong overall performance in both accuracy and deployment efficiency. In contrast, InternVL ranks lowest at 25.2%, reflecting limitations in real world robustness and efficiency. This visualization also highlights the substantial performance variability across modern OCR systems.


Hybrid and emerging models like GOT OCR and MiniCPM showcased notable individual strengths, such as GOT’s lowest Character Error Rate (CER), but struggled to deliver consistent performance across all evaluation metrics. This suggests that while LVLMs and hybrid models can excel in specialized or multitask scenarios, they may not yet match the end to end reliability of established OCR systems.

Sprinklr-Edge-OCR, despite being based out of traditional Machine learning pipeline supports 5 languages, remained highly competitive. It outperformed or matched LVLMs on most core metrics, including F1 score, latency, and memory us-

TABLE III CPU-ONLY EDGE DEPLOYMENT PERFORMANCE COMPARISON

#### Metric Sprinklr-Edge-OCR Qwen-VL

Avg Inference Time (s) 4.36 69.38 Time Cost (×) 1.0 15.9× Peak RAM Usage (GiB) 0.89 10.8 Ram Required (×) 1.0 12.1×

age, making it particularly well suited for real world, resource constrained deployments. This highlights the continued relevance and strength of optimized, task specific OCR pipelines, especially when reliability and deployment efficiency are paramount.

To further evaluate the practicality of deploying these models in edge environments, we conducted CPU-only inference tests simulating scenarios without GPU acceleration. Using an 8-core Intel Xeon processor, we compared the large visionlanguage model Qwen-VL with the lightweight Sprinklr-EdgeOCR pipeline. The results demonstrate a stark contrast in resource requirements: Qwen-VL incurred significantly higher inference latency (69.38 seconds per image) and memory usage (10.8 GiB RAM), reflecting the computational demands of LVLMs. In contrast, Sprinklr-Edge-OCR achieved rapid inference (4.36 seconds per image) with minimal memory consumption (0.89 GiB RAM), underscoring its suitability for edge deployment. These findings reinforce that while LVLMs offer advanced capabilities, traditional OCR pipelines like Sprinklr-Edge-OCR remain far more efficient and practical for real-world applications on resource-constrained hardware.

V. CONCLUSION

This study provides a comprehensive evaluation of multilingual OCR models across a range of scenarios, including edge deployment and real world image complexity. The key finding is that there is no one size fits all solution. The optimal model depends on the intended application and deployment context.

LVLMs like Qwen offer compelling strengths in semantic reasoning, language generalization, and zero shot adaptability. While they currently lag behind in metrics such as latency and overall F1 score, they hold promise for next generation OCR systems that demand deeper contextual understanding. However, their current computational demands make them unsuitable for deployment on edge devices.

Conversely, for applications where efficiency, scalability, and low latency are critical, such as on device or edge environments, Sprinklr-Edge-OCR emerges as the top choice as it consistently delivering the best overall accuracy and performance with minimal computational overhead.

In sum, this work lays a practical evaluation of OCR models, balancing accuracy, cost, and adaptability, and guiding the development of systems for increasingly complex multilingual and real world OCR scenarios.

REFERENCES [1] Bai, J., Bai, S., Yang, S., Wang, S., Tan, S., Wang, P., Lin, J., Zhou, C.,

& Zhou, J. (2023). Qwen-VL: A Versatile Vision-Language Model for

![image 10](e-armor-2025-multilingual-ocr-edge-cases_images/imageFile10.png)

Fig. 9. Example outputs for a publicly available challenging image, time taken and similarity score of various models along with ground truth

Understanding, Localization, Text Reading, and Beyond. arXiv preprint arXiv:2308.12966.

- [2] Bautista, D., & Atienza, R. (2022). Scene text recognition with permuted autoregressive sequence models. In European Conference on Computer Vision (pp. 593–610). Springer.
- [3] Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., & Fei-Fei, L. (2009). Imagenet: A large-scale hierarchical image database. In 2009 IEEE Conference on Computer Vision and Pattern Recognition (pp. 248–255). IEEE.
- [4] Dosovitskiy, A., et al. (2021). An image is worth 16x16 words: Transformers for image recognition at scale. International Conference on Learning Representations.
- [5] Du, Y., et al. (2022). PP-OCRv3: More Robust and Accurate Scene Text Recognizer. arXiv preprint arXiv:2206.03001.
- [6] Fang, S., Xie, H., Wang, Y., Mao, Z., & Zhang, Y. (2021). Read like humans: Autonomous, bidirectional and iterative language modeling for scene text recognition. In CVPR (pp. 7098–7107).
- [7] Fu, L., et al. (2025). OCRBench v2: An Improved Benchmark for Evaluating Large Multimodal Models on Visual Text Localization and Reasoning. arXiv preprint arXiv:2501.00321.
- [8] Kim, G., et al. (2021). OCR-free document understanding transformer. arXiv preprint arXiv:2111.15664.
- [9] Kuang, Z., et al. (2021). MMOCR: A Comprehensive Toolbox for Text Detection, Recognition and Understanding. In arXiv preprint arXiv:2108.06543
- [10] Li, M., et al. (2023). TrOCR: Transformer-based Optical Character Recognition with Pre-trained Models. In https://doi.org/10.1609/aaai.v37i11.26538
- [11] Liao, H., et al. (2023). DocTr: Document Transformer for Structured Information Extraction in Documents. In arXiv preprint arXiv:2110.12942.
- [12] Paruchuri, V., & Datalab Team. (2025). Surya: A lightweight document OCR and analysis toolkit. GitHub repository: https://github.com/ datalab-to/surya
- [13] Qwen Team. (2025). Qwen3 Technical Report. arXiv preprint arXiv:2505.09388.
- [14] Smith, R. (2007). An overview of the Tesseract OCR engine. In ICDAR doi: 10.1109/ICDAR.2007.4376991.
- [15] Touvron, H., et al. (2023). LLaMA: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971.
- [16] Wei, H., et al. (2024). General OCR Theory: Towards OCR-2.0 via a Unified End-to-end Model. arXiv preprint arXiv:2409.01704.


- [17] Xie, E., et al. (2021). SegFormer: Simple and efficient design for semantic segmentation with transformers. In arXiv preprint arXiv:2105.15203
- [18] Yao, Y., et al. (2024). MiniCPM-V: A GPT-4V Level MLLM on Your Phone. arXiv preprint arXiv:2408.01800.
- [19] Zhai, X., et al. (2023). Sigmoid loss for language image pre-training. In arXiv preprint arXiv:2303.15343
- [20] Zheng, L., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. arXiv preprint arXiv:2306.05685.
- [21] Zhu, J., et al. (2025). InternVL3: Exploring Advanced Training and Test-Time Recipes for Open-Source Multimodal Models. arXiv preprint arXiv:2504.10479.
- [22] PyLaila: A Lightweight Multilingual OCR Library. GitHub repository: https://github.com/jpuigcerver/PyLaia
- [23] Kiessling, B. (2019). Kraken: An Universal Text Recognizer for the Humanities. In DH2019: Digital Humanities Conference. GitHub repository: https://github.com/mittagessen/kraken
- [24] InstructOCR: Instruction-Tuned Multilingual Scene Text Recognition. GitHub repository: https://github.com/AlibabaResearch/ AdvancedLiterateMachinery/tree/main/InstructOCR
- [25] Huang, M., Li, H., Liu, Y., Bai, X., & Jin, L. (2024). Bridging the Gap Between End-to-End and Two-Step Text Spotting. arXiv preprint arXiv:2404.04624.
- [26] Nassar, A., Marafioti, A., Omenetti, M., Lysak, M., Livathinos, N., Auer, C., Morin, L., Teixeira de Lima, R., Kim, Y., Gurbuz, A.S., Dolfi, M., Farr´e, M. and Staar, P.W.J. (2025). SmolDocling: An ultra-compact vision-language model for end-to-end multi-modal document conversion. arXiv preprint arXiv:2503.11576.
- [27] Zhibo Yang, Jun Tang, Zhaohai Li, Pengfei Wang, Jianqiang Wan, Humen Zhong, Xuejing Liu, Mingkun Yang, Peng Wang, Shuai Bai, LianWen Jin, and Junyang Lin. CC-OCR: A Comprehensive and Challenging OCR Benchmark for Evaluating Large Multimodal Models in Literacy. arXiv preprint arXiv:2412.02210, December 2024. :contentReference[oaicite:2]index=2
- [28] Sankalp Nagaonkar, Augustya Sharma, Ashish Choithani, and Ashutosh Trivedi. Benchmarking Vision-Language Models on Optical Character Recognition in Dynamic Video Environments. arXiv preprint arXiv:2502.06445, February 2025. :contentReference[oaicite:4]index=4
- [29] Suraj Singh, A Comparative Analysis of OCR Models on Diverse Datasets: Insights and Efficiency. WACV Workshop on VisionDocs

(2025), January 2025. :contentReference[oaicite:5]index=5

- [30] Bhawna Piryani, Jamshid Mozafari, Abdelrahman Abdallah, Antoine Doucet, and Adam Jatowt. MultiOCR-QA: Dataset for Evaluating


- Robustness of LLMs in Question Answering on Multilingual OCR Texts. arXiv preprint arXiv:2502.16781, February 2025. :contentReference[oaicite:6]index=6
- [31] Chitranshu Harbola and Anupam Purwar. KnowsLM: A framework for evaluation of small language models for knowledge augmentation and humanised conversations. arXiv preprint arXiv:2504.04569, April 2025. :contentReference[oaicite:1]index=1
- [32] Song Han, Huizi Mao, and William J. Dally. Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding. arXiv preprint arXiv:1510.00149, October 2015.
- [33] Seungmin Kim, Gwangjin Park, and Youngwoo Yi. Performance Evaluation of INT8 Quantized Inference on Mobile GPUs. IEEE Access, 2021.
- [34] B. Gautam and A. Purwar, Evaluating the Efficacy of Open-Source LLMs in Enterprise-Specific RAG Systems: A Comparative Study of Performance and Scalability, arXiv preprint arXiv:2406.11424, 2024.


