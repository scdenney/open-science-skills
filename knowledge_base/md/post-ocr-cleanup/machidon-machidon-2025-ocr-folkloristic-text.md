DIGITAL HERITAGE (2025) S. Campana, D. Ferdani, H. Graf, G. Guidi, Z. Hegarty, S. Pescarin, and F. Remondino (Editors)

## Comparing OCR Pipelines for Folkloristic Text Digitization

O.M. Machidon1 and A.L. Machidon1

1University of Ljubljana, Faculty of Computer and Information Science, Slovenia

# arXiv:2507.19092v1[cs.DL]25 Jul 2025

### Abstract

The digitization of historical folkloristic materials presents unique challenges due to diverse text layouts, varying print and handwriting styles, and linguistic variations. This study explores different optical character recognition (OCR) approaches for Slovene folkloristic and historical text digitization, integrating both traditional methods and large language models (LLMs) to improve text transcription accuracy while maintaining linguistic and structural integrity. We compare single-stage OCR techniques with multi-stage pipelines that incorporate machine learning-driven post-processing for text normalization and layout reconstruction. While LLM-enhanced methods show promise in refining recognition outputs and improving readability, they also introduce challenges related to unintended modifications, particularly in the preservation of dialectal expressions and historical structures. Our findings provide insights into selecting optimal digitization strategies for large-scale folklore archives and outline recommendations for developing robust OCR pipelines that balance automation with the need for textual authenticity in digital humanities research.

### CCS Concepts

• Information systems → Information systems applications; • Applied computing → Arts and humanities;

### 1. Introduction

The digitization of historical folkloristic texts is a key priority in digital heritage research, enabling long-term preservation, accessibility, and computational analysis of cultural narratives. However, these materials present unique challenges for automated transcription due to their diverse physical and linguistic properties. Folkloristic collections often include a mixture of typewritten and handwritten documents, irregular layouts, archaic or dialectal language, and visual artifacts such as marginal notes or embedded illustrations [FKG25]. These factors complicate the use of standard optical character recognition (OCR) pipelines, which are typically trained on contemporary printed text with relatively clean layouts.

The accuracy of OCR is critical in the digital humanities, where text fidelity directly impacts linguistic analysis, pattern detection, and structural interpretation. In folkloristics, even small errors—such as the misrecognition of dialectal variants or disrupted narrative structures—can lead to misinterpretation of cultural meanings. Consequently, researchers require OCR solutions that balance high throughput with sensitivity to textual authenticity.

Recent advances in OCR and language technologies have introduced new possibilities for improving digitization outcomes. Traditional OCR engines, such as Tesseract or Kraken, have been adapted for historical documents with varying degrees of success, often requiring layout-specific preprocessing and custom model training. In parallel, the emergence of large language models

© 2025 The Author(s). Proceedings published by Eurographics - The European Association for Computer Graphics. This is an open access article under the terms of the Creative Commons Attribution License, which permits use, distribution and reproduction in any medium, provided the original work is properly cited.

(LLMs) has opened up opportunities for post-OCR correction, normalization, and formatting [KLKG25]. LLMs such as ChatGPT † and Claude ‡ can refine noisy transcriptions and reconstruct coherent paragraphs, but they also raise concerns about textual hallucinations and unintended modernization, which may obscure the original character of folkloric texts.

This paper presents a comparative evaluation of OCR pipelines for the digitization of Slovenian folkloristic materials, with a focus on two main approaches: a single-stage pipeline using the opensource tool olmOCR, and a two-stage pipeline combining Tesseract with LLM-based post-processing. Through a series of experiments on typewritten fairy tales, historical newspapers, and children’s magazines, we assess the impact of scan quality, document layout, and language variation on OCR accuracy and usability. Our goal is to provide practical insights and recommendations for digital heritage practitioners seeking scalable, accurate, and contextsensitive solutions for folklore digitization.

The contributions of this study are threefold:

- 1. a comparison of OCR pipelines on authentic folkloristic corpora in Slovene,
- 2. an evaluation of LLM-assisted post-processing with respect to both readability and linguistic authenticity, and


† https://chatgpt.com/ ‡ https://chat.chatbot.app/

- 3. guidelines for selecting or customizing OCR workflows based on document characteristics and scholarly requirements.


This work contributes to ongoing efforts in the digital humanities to reconcile automation with cultural preservation, advancing best practices for large-scale, historically informed text digitization.

- 2. Related Work


- 2.1. OCR for Historical and Folkloristic Texts


Digitizing historical and folkloristic texts via OCR is a wellstudied yet challenging task. Such materials often exhibit diverse layouts, including multi-column pages, marginalia, and irregular text blocks, which pose difficulties for automatic layout analysis [FKG25]. Degraded print quality (faded ink, stains, bleedthrough) and unusual typography (e.g., 19th-century fonts like Fraktur) further contribute to high OCR error rates [KLKG25]. Handwritten folkloric manuscripts add another layer of complexity due to handwriting variation, requiring specialized handwriting recognition models. Additionally, these texts frequently contain dialectal or archaic language not seen in modern training data, confounding standard OCR engines that assume contemporary vocabulary and spelling. As a result, off-the-shelf OCR methods on folkloristic archives can produce noisy output, and fully automatic recognition remains an open challenge in digital heritage preservation [KLKG25,FKG25].

Over the past decade, numerous OCR systems and pipelines have been developed to address these challenges. Tesseract—an opensource engine—and the Transkribus platform are widely used for printed and handwritten historical documents, respectively, and are often considered baseline solutions in the cultural heritage community [FKG25]. These general-purpose tools offer pretrained models for many languages; however, they struggle with the peculiarities of historical folkloristic material, such as complex page layouts or antiquated fonts, often requiring significant manual intervention to achieve acceptable accuracy [FKG25]. Even with modern OCR technology, pages with decorative borders or interleaved song lyrics and commentary may need human-guided segmentation to avoid recognition errors [FKG25].

More specialized OCR approaches have emerged. The OCR4all toolkit integrates advanced layout analysis and model training into an end-to-end workflow, achieving top-tier accuracy on recent historical OCR benchmarks [FKG25]. Likewise, the opensource Kraken OCR engine, designed with historical and non-Latin scripts in mind, has demonstrated superior accuracy on challenging texts compared to Tesseract in many cases [MLK20]. Kraken’s trainable neural OCR models have proven effective on early print typefaces and manuscripts, especially with domain-specific training data. For example, ensemble LSTM OCR models like Calamari have reduced the character error rate on 19th-century Fraktur prints below 1%, outperforming both Tesseract and commercial engines [RSWP18].

Several large-scale heritage projects have adopted customized OCR pipelines to handle domain-specific challenges. For printed folklore compilations, it is common to fine-tune OCR models on sample pages from a collection. For handwritten archives, platforms like Transkribus enable tailored handwritten text recognition

(HTR) models for each scribe or region, improving accuracy over generic models [FKG25]. Recent literature shows a clear trend toward domain-adaptive OCR in the humanities: researchers combine layout-specific processing, specialized engines, and post-correction methods to handle the varied nature of historical folklore texts. Our work situates itself in this context by comparing such OCR pipeline components and configurations on folkloristic material.

### 2.2. Language Model-Assisted Post-Processing andNormalization

Given that raw OCR outputs can contain substantial errors, postprocessing is often applied to improve text quality. Earlier approaches used dictionaries, spelling variation databases, or statistical models to correct obvious errors. In recent years, however, neural language models have become the preferred method for automatic error correction [KLKG25]. For example, the bestperforming systems in the ICDAR 2019 competition on postOCR correction § used a two-step process: a Transformer-based model (BERT) detected probable errors, followed by a sequenceto-sequence model for corrections [KLKG25].

Large Language Models (LLMs) have been explored as a more powerful alternative [KLKG25]. Bourne et al. [Bou24] demonstrated that GPT-based correction could reduce character error rates by over 60% on historical datasets. Recent work has treated historical-to-modern normalization as a translation task, fine-tuning large encoder–decoder models, such as the “Transnormer,” to map 18th–19th century texts to contemporary German [Ehr24]. These techniques achieved state-of-the-art performance, making texts more accessible for search and analysis.

Despite these advances, researchers have cautioned against potential drawbacks [KLKG25, BER∗24]. LLMs, being generative models, may introduce plausible but historically inaccurate content, or over-correct dialectal or archaic expressions. Boros et al. [BER∗24] found that prompting GPT-4 for OCR correction sometimes decreased overall accuracy due to hallucinated outputs. Even with strong normalization models, perfect automatic standardization remains elusive, with residual error rates reported around 1% [Ehr24].

Recent work emphasizes careful integration of LLMs, such as constraining outputs or employing human-in-the-loop validation, to ensure authenticity is preserved [KLKG25,BER∗24].

In summary, the field has evolved from generic OCR engines toward specialized, context-aware OCR pipelines and is now exploring how large language models can refine recognition results. Our work addresses the remaining gap by systematically evaluating complete OCR pipelines on folkloristic corpora, building on prior advancements in both OCR and LLM-assisted post-processing.

### 3. Materials and methods3.1. Data Sources

To evaluate OCR pipelines on real-world folkloristic and cultural heritage materials, we selected three representative Slovene-

§ https://icdar2019.org/competitions-2/

language datasets. These sources span different time periods, media formats, and linguistic registers, providing a robust foundation for assessing recognition accuracy, layout sensitivity, and postprocessing strategies.

### 3.1.1. Kmetijske in rokodelske novice

The first dataset is drawn from the historical periodical Kmetijske in rokodelske novice [kme02], a prominent 19th-century Slovenelanguage newspaper. Published between 1843 and 1902, this source played a central role in standardizing the Slovene language and promoting literacy and civic education among rural populations. As shown in Figure 1, the periodical uses antiquated fonts (including Fraktur and early Antiqua), multi-column layouts, and historical orthography. These characteristics present significant OCR challenges, including segmentation errors, character confusion, and reduced accuracy on linguistic variants. This dataset is well-suited for evaluating OCR robustness on early printed heritage texts.

![image 1](machidon-machidon-2025-ocr-folkloristic-text_images/imageFile1.png)

Figure 1: A sample page from Kmetijske in rokodelske novice, dated November 7, 1855. This historical periodical, written in 19th-century Slovene and printed using antiquated fonts and multicolumn layouts, poses significant challenges for OCR due to typographic complexity, degraded print quality, and early orthographic conventions.

### 3.1.2. Ciciban

The second dataset comprises issues from Ciciban [Cic45], a children’s magazine first published in 1945 and still in circulation today. Targeted at early readers, the magazine blends poems, short stories, games, and rich visual content. Figure 2 presents an example page combining illustrated verse and narrative prose. OCR on this corpus is complicated by the interplay of text and images, decorative and variable fonts, and non-linear layout elements. It is especially valuable for testing layout-aware OCR systems and assessing how post-processing models handle stylistically diverse texts intended for pedagogical or literary purposes.

![image 2](machidon-machidon-2025-ocr-folkloristic-text_images/imageFile2.png)

Figure 2: A sample page from the children’s magazine Ciciban, featuring a combination of poetic text, short narrative, and illustrations. Documents like this pose layout-specific OCR challenges due to mixed content (e.g., stylized fonts, embedded images, decorative headings), as well as language aimed at young readers. The visual richness of the page exemplifies the need for robust layout analysis and content-sensitive post-processing in OCR workflows.

### 3.1.3. Inštitut za narodopisje – skenirane pravljice

The third corpus used in this study consists of typewritten folkloristic stories collected by the Inštitut za narodopisje (Institute of Folklore Studies) of the Slovene Academy of Sciences and Arts. These materials, created in the mid-20th century, document oral narratives transcribed using typewriters and later digitized as scanned images. A sample page is shown in Figure 3.

This collection presents several interesting challenges for OCR development. Although the documents are typewritten, they vary in quality due to degradation of the paper, ink fading, and scanning inconsistencies. Additionally, the typewriter fonts themselves often introduce visual noise (e.g., irregular spacing or smudged glyphs), which complicates character recognition. The texts sometimes contain handwritten annotations, underlines, or editorial marks, further affecting the recognition accuracy.

![image 3](machidon-machidon-2025-ocr-folkloristic-text_images/imageFile3.png)

- Figure 3: Sample page from the Inštitut za narodopisje – skenirane pravljice collection. The document is typewritten and shows typical layout and character spacing of mid-20th century folkloristic transcriptions. Despite visual uniformity, OCR can be challenged by faded ink, uneven typewriter impressions, and page-level degradation.


### 3.2. OCR Pipeline and Processing Workflow

We evaluated two distinct OCR pipelines to assess their suitability for digitizing Slovene-language folkloristic and historical materials: a single-stage pipeline based on olmOCR and a multi-stage workflow combining Tesseract OCR with large language model (LLM)-based post-processing.

Pipeline A: olmOCR (Single-Stage) The first pipeline employs olmOCR, an open-source toolkit developed by the Allen Institute for AI for high-throughput conversion of PDFs and scanned

documents into plain text [PBD∗25]. olmOCR ¶ leverages a finetuned 7B vision-language model and a novel document-anchoring prompting technique to extract text in natural reading order while preserving structured content such as sections, tables, equations, and handwritten text. It is optimized for scalable, GPU-based batch processing, with an estimated cost of under $190 per million pages, making it suitable for large-scale digitization workflows.

olmOCR was trained primarily on English academic and technical documents and is not explicitly adapted for Slovene. Nonetheless, in our experiments, it produced surprisingly robust results on typewritten Slovene folkloristic texts and relatively clean layouts. A key advantage is that it operates entirely locally, avoiding thirdparty API calls and maintaining full data privacy. However, it exhibited limitations when handling documents with complex visual structure (e.g., multi-column formats or image-overlaid text), occasionally misordering content or omitting layout-sensitive elements. Additionally, while olmOCR includes heuristics to reduce hallucinations, some semantic drift was observed on degraded inputs.

Pipeline B: Tesseract + LLM (Multi-Stage) The second pipeline adopts a modular, multi-stage approach. In the first stage, scanned pages are processed using the Tesseract OCR engine with Slovene language support. The resulting raw OCR text is then passed to a large language model (LLM) for post-processing. We used OpenAI’s ChatGPT-4 (GPT-4.o version model, accessed through the OpenAI API ∥) to correct OCR-induced errors (e.g., fragmented words, spacing inconsistencies, misrecognized characters) and to reconstruct coherent paragraph structure. Prompt engineering was applied to minimize semantic drift and hallucinations. While this post-processing step improved readability and structural clarity, it occasionally led to unintended normalization of dialectal or archaic terms, raising concerns about fidelity in cultural heritage contexts.

To improve performance on documents with complex or visually rich layouts—such as Ciciban—we optionally tested the integration of LayoutParser prior to OCR. This tool was used to detect and segment visual elements (e.g., text blocks, images, headings), enabling a more logical reading order for downstream processing. However, its impact on overall accuracy was limited in practice and did not consistently resolve all layout-related issues.

Image Preprocessing Additional preprocessing experiments were conducted on selected samples using standard enhancement techniques such as grayscale conversion, binarization, and dilation ∗∗ . However, for degraded documents like Kmetijske in rokodelske novice, these steps did not significantly improve OCR accuracy. In some cases, preprocessing introduced artifacts that worsened recognition quality. As a result, most evaluations were conducted using raw scans or lightly optimized images.

¶ https://olmocr.allenai.org/blog ∥ https://openai.com/api/ ∗∗ Dilation is a morphological image processing operation that expands or thickens the shapes of objects in a binary image. In OCR preprocessing, it is sometimes used to close small gaps in characters or connect fragmented parts of text to improve recognition accuracy.

Output Evaluation For all pipelines, the output was manually reviewed for recognition accuracy, layout preservation, and language integrity. OCR performance was compared across document types to assess robustness in the presence of historical typography, irregular structure, and linguistic variation. Where relevant, we evaluated the impact of LLMs not only on surface-level error correction, but also on the preservation of culturally meaningful features such as dialectal vocabulary, narrative flow, and typographic cues.

### 4. Results and discussion

OCR performance was significantly influenced by the quality of the scanned documents. As shown in the experiments on the Kmetijske in Rokodelske novice dataset, documents scanned at low quality produced OCR results that were largely unusable, while higherquality scans enabled acceptable transcription accuracy even with minimal preprocessing (for an example of different scan qualities on this dataset see Figure 4). Attempts to improve lower-quality scans using traditional image preprocessing techniques (grayscale conversion, binarization, dilation) did not yield better results, and in some cases even worsened recognition. This suggests that advanced preprocessing techniques, such as adaptive histogram equalization or deep learning-based enhancement models, may be needed for robust OCR of low-quality historical scans.

![image 4](machidon-machidon-2025-ocr-folkloristic-text_images/imageFile4.png)

![image 5](machidon-machidon-2025-ocr-folkloristic-text_images/imageFile5.png)

(a) Poor scan quality (b) Acceptable scan quality

- Figure 4: Comparison of scan quality. Left: low-quality scan with noise and degradation; Right: higher-quality scan enabling more accurate OCR results.


- 4.1. Comparison of OCR Approaches


- 4.1.1. olmOCR (Single-Stage Pipeline)


The single-stage pipeline based on olmOCR offered significant advantages in terms of simplicity and privacy. Since olmOCR can be deployed locally, documents were processed without involving third-party services. OlmOCR demonstrated good robustness across different materials: for instance, in the case of the typewritten fairy tales, it produced cleaner and more usable outputs compared to Tesseract-based pipelines. It was particularly effective on relatively simple layouts. However, olmOCR showed limitations when processing documents with complex structures, such as the Ciciban magazine, occasionally misordering text blocks due to its limited layout analysis capabilities.

- 4.1.2. Tesseract + LLM (Two-Stage Pipeline)

The two-stage approach employed Tesseract as the OCR engine, followed by a post-processing stage using ChatGPT-4 or other LLMs (such as Gemini and Claude) for error correction and formatting. This method enabled corrections of common OCR issues, such as fragmented words, missing punctuation, and inconsistent spacing. Furthermore, integration with LayoutParser provided a mechanism for analyzing and reconstructing document layouts, partially mitigating problems with complex page structures.

However, this pipeline also introduced new challenges. LLMbased post-processing occasionally altered the text content beyond correcting errors, replacing dialectal or archaic words with their modern equivalents (e.g., storjice became zgodbe). This "normalization" effect, while improving readability, posed a risk of losing linguistic authenticity, which is critical for folklore studies. Additionally, minor hallucinations were observed, especially when text fragments were highly degraded or incomplete.

- 4.2. Evaluation on Different Document Types


- 4.2.1. Folkloristic Newspapers (Kmetijske in rokodelske novice)

On degraded historical newspaper scans, both pipelines faced difficulties. olmOCR showed moderate performance, but Tesseract+LLM achieved better readability after post-correction. However, as shown in Figure 5, LLMs sometimes replaced historical terms with modern or unrelated words (e.g., žlahnega → glavnega), which may introduce semantic drift. More specialized OCR training or validation-aware post-processing would be necessary for reliable digitization of these materials.

- 4.2.2. Children’s Magazines (Ciciban)

The Ciciban corpus, consisting of mid- and late-20th-century children’s periodicals, features high-quality scans and modern, typewritten fonts. These characteristics allowed Tesseract to achieve strong OCR performance with minimal character-level errors. When combined with ChatGPT-4 in a two-stage pipeline, the output quality improved further: the LLM corrected formatting issues such as broken lines and inconsistent punctuation, while maintaining the semantic integrity of the text. As shown in Figure 6, the post-processed output was more readable and coherent, without any hallucinations or modernizing alterations.

While olmOCR also produced reasonable results on Ciciban, it lacked sufficient layout awareness and occasionally misordered paragraphs or merged unrelated text segments—particularly in visually complex issues that featured poetry, prose, and images in non-linear arrangements. In such cases, incorporating LayoutParser into the Tesseract-based pipeline helped recover reading order and segment content more effectively. This makes the Tesseract+LLM pipeline, optionally augmented with LayoutParser, the most reliable solution for processing Ciciban documents with mixed layout structures.

- 4.2.3. Typewritten Fairy Tales


For the corpus of mid-20th-century typewritten fairy tales, olmOCR consistently outperformed the Tesseract+LLM pipeline. Tesser-

![image 6](machidon-machidon-2025-ocr-folkloristic-text_images/imageFile6.png)

|Kaj je namen umnega plemenenja in kaj o tem skušnje uče? Namen umnega plemenenja je, da si gospodar priredi dobre in lepe živine, kakoršne potrebuje za svoje gospodarstvo, Navadno je gospodarjem bolj vstreženo z dobro živino, kakor z lepo; če pa zamore oboje zediniti, je pa tolikanj bolje. Lepota se tudi rada vjema z dobroto, in tako gospodar, ki potrebuje težke živine, močnega konja imenuje leega, čeravno ni izdelan v vsem životu po razmerah žlahnega Arabca. Dobra, živina je mnogokrat tudi lepa, zlasti kar vprežno živino zadeva, ker lista naprava in postava glave, vratu, herbta, križa in nog, ki dela konja lepega, ga dela večidel tudi dobrega. "|
|---|
|Kaj je namen umnega plemenjenja in kaj o tem skušnje uče? Namen umnega plemenjenja je, da si gospodar priredi dobro in lepo živino, kakršne potrebuje ga svoje gospodarstvo. Navadno je gospodarjem bolj všeč z dobro živino kot z lepo; če pa zmore oboje uskladiti, je pa toliko bolje. Lepota se tudi rada vjema z dobroto, in tako gospodar, ki potrebuje težke delovne, imenuje lepega, Gerayno ni izdelan v vsem životu po razmerah glahnega Arabca. Dobra živina je mnogokrat tudi lepa, zlasti kar se prebavne živine zadeva, ker ta naprava in postava glave, vratu, hrbta, križa in nog, ki dela konja lepega, ga dela večidel tudi dobrega.<br><br>|


- Figure 5: OCR and post-processing comparison on a historical page from Kmetijske in rokodelske novice. Top: original scan. Middle: raw OCR output using Tesseract. Bottom: ChatGPT-4 enhanced output. Yellow highlights indicate tokens where ChatGPT modified the original OCR text—some represent helpful corrections (e.g., spacing, grammar), while others reveal unintended substitutions or normalizations that may impact authenticity.


act produced noisy raw OCR with numerous errors in character recognition, punctuation, and names—particularly affecting diacritics and borrowed terms. When passed to ChatGPT-4 for post-processing, these issues were only partially corrected. In some cases, the LLM introduced new hallucinations or fabricated plausible-sounding alternatives, which diverged from the original meaning. In contrast, olmOCR yielded more accurate transcrip-

![image 7](machidon-machidon-2025-ocr-folkloristic-text_images/imageFile7.png)

|»Poglejte, tam so lestve, jim je rekla, »pojdite in pričnite trgati. Sladko je.,« | si Pobrali so košare, splezali na lestve in pričeli trgati zrelo grozdje. Smeli so ga zobati po mili volji. Nekaj časa so kar molčali, tako so ga hiteli jesti. »Kako je dobro,« so si potem pripovedovali in se veselili, da so splezali tako visoko. | »Poglejte, kje sem!« je vpila Anka.|
|---|
|»Poglejte, tam so lestve,« jim je rekla, »pojdite in pričnite trgati. Sladko je.« Pobrali so košare, splezali na lestve in pričeli trgati zrelo grozdje. Smeli so ga zobati po mili volji. Nekaj časa so kar molčali, tako so ga hiteli jesti. »Kako je dobro,« so si potem pripovedovali in se veselili, da so splezali tako visoko. »Poglejte, kje sem!« je vpila Anka.|


- Figure 6: Comparison between raw Tesseract OCR and ChatGPTenhanced output for a passage from Ciciban. The scan quality and font are clean and modern, allowing Tesseract to transcribe the text with high accuracy. ChatGPT-4 further improves readability by restoring correct sentence structure, resolving broken lines, and fixing punctuation—without introducing hallucinations or modifying the original meaning.

tions directly, with lower hallucination rates and better preservation of the original sentence structure. A representative comparison is shown in Figure 7.

|Tesseract: tawa (l9oo) s DO lbice/Stolvizza v nezlji, kl je od avgusta 1966 do o zaih ot O anAn 4 di avgusta l970 povedala že čez 400 tekstov. V našem izboru je zastopene z zgodbico "Le ﬁlle gul vouleit tuer son petit" (etr. ]). Pra|
|---|
|Tesseract + ChatGPT: tawa (1900) s Polbice/Stolvizza v Medžiji, ki je od avgusta 1966 do avgusta 1970 povedala že čez 400 tekstov. V našem izboru je zastopana z zgodbico "Le ﬁlle qui voulait tuer son petit" (str. 1). Pravo<br><br>|
|olmOCR:<br><br>tava (1900) s Solbice/Stolvisca v Reziji, ki je od avgusta 1966 do avgusta 1970 povedala že čez 400 tekstov. V našem izboru je zastopana z zgodbico "La ﬁlle qui voulait tuer son petit" (str.[]). Pravo|


![image 8](machidon-machidon-2025-ocr-folkloristic-text_images/imageFile8.png)

- Figure 7: Comparative OCR output for a sample from the typewritten fairy tale corpus. Tesseract produced a low-quality raw transcription with significant errors in names, diacritics, and word structure. ChatGPT-4 post-processing attempted to restore coherence but introduced additional hallucinations. In contrast, olmOCR preserved the correct linguistic form with fewer distortions and greater fidelity to the original.


### 4.3. Summary of Findings

Our evaluation across the three distinct folkloristic datasets demonstrates that OCR pipeline performance varies considerably depending on document layout complexity, scan quality, and language

Table 1: Summary of OCR pipeline performance by dataset

Kmetijske in rokodelske novice (19th century, historical newspapers, degraded scans) Preferred pipeline: Tesseract + LLM Strengths: Recovers degraded text, improves readability Weaknesses: Some semantic drift, normalization of historical terms Notes: Minor hallucinations; simple layouts help

Ciciban (mid-20th century, children’s magazine, complex layout) Preferred pipeline: Tesseract + LLM (+LayoutParser) Strengths: High accuracy, effective formatting fixes Weaknesses: Layout inversion risk without parser Notes: Low hallucination risk; layout parsing recommended

Typewritten fairy tales (mid-20th century, typewritten stories, clean scans) Preferred pipeline: olmOCR Strengths: High fidelity, few hallucinations Weaknesses: Sensitive to scan quality Notes: Best for simple, uniform text

characteristics. A summary of our findings is presented in Table 1. Specifically:

- • Tesseract+LLM outperformed other approaches on wellscanned historical newspapers (Kmetijske), where ChatGPT-4 helped reconstruct readable text from initially noisy OCR outputs. However, this came at the cost of occasional hallucinations and normalization of historical terms.
- • For Ciciban, which features high scan quality and typographic clarity but complex layouts, the Tesseract+LLM pipeline, optionally enhanced with LayoutParser, provided the most reliable results. Tesseract handled the base recognition effectively, and ChatGPT-4 improved formatting without semantic distortion.
- • On typewritten fairy tales, olmOCR outperformed the Tesseractbased pipeline. Tesseract produced poor raw transcriptions, which the LLM could not reliably correct—sometimes compounding errors with hallucinations. In contrast, olmOCR generated more accurate results.
- • Scan quality remained a critical factor across all datasets. No pipeline was able to reliably salvage degraded or poorly digitized material through conventional preprocessing alone.


We conclude that no single pipeline is universally optimal. Instead, a document-sensitive strategy is recommended: in our case, the use olmOCR for clean, typewritten texts, deploying Tesseract+LLM for materials with higher layout complexity and language variation, and applying LayoutParser selectively when complex visual structure threatens reading order.

### 5. Conclusions

This study compared OCR pipeline configurations for the digitization of historical and folkloristic Slovene texts, focusing on three

distinct datasets: historical newspapers (Kmetijske in rokodelske novice), children’s magazines (Ciciban), and typewritten fairy tales. Our experiments evaluated both a single-stage pipeline using olmOCR and a multi-stage pipeline combining Tesseract OCR, ChatGPT-4 post-processing, and optionally LayoutParser for layout analysis.

Our findings show that pipeline performance depends heavily on document characteristics. For high-quality, typewritten materials, olmOCR proved more effective, offering good transcription fidelity with minimal hallucinations. In contrast, Tesseract struggled with initial recognition, and LLM-based correction sometimes amplified errors. For historical newspapers, the Tesseract+LLM pipeline was more successful in reconstructing coherent output, though it introduced some normalization and semantic drift. For richly formatted children’s magazines, Tesseract+LLM again performed well—especially when augmented with layout-aware preprocessing to resolve reading order and structure.

While LLMs significantly enhance formatting and readability, they must be applied with caution to avoid distorting historically and linguistically meaningful content. Similarly, scan quality remains a critical determinant of OCR success; no post-processing approach could fully recover degraded input.

We conclude that no single OCR pipeline is universally optimal. Instead, best practices in folklore digitization call for a tailored strategy. Future work should prioritize the development of domainadapted OCR models and the integration of validation mechanisms that ensure semantic authenticity during post-correction with LLMs.

### Acknowledgments

The research presented in this paper was funded by the Slovenian Research Agency through the Gravitacija project “Veliki jezikovni modeli za digitalno humanistiko” (GC-0002).

### References

[BER∗24] BOROS E., EHRMANN M., ROMANELLO M., NAJEMMEYER S., KAPLAN F.: Post-correction of historical text transcripts with large language models: An exploratory study. In Proceedings of the 8th joint SIGHUM workshop on computational linguistics for cultural heritage, social sciences, humanities and literature (LaTeCH-CLfL 2024) (2024), Association for Computational Linguistics, pp. 133–159. 2

[Bou24] BOURNE J.: CLOCR-C: Context leveraging OCR correction with pre-trained language models. arXiv preprint arXiv:2408.17428

(2024). 2

[Cic45] CICIBAN: Ciciban magazine collection. https://www. dlib.si/details/URN:NBN:SI:DOC-1R8Y8Z7L, from 1945. Digitized by the National and University Library of Slovenia (NUK). 3

[Ehr24] EHRMANNTRAUT A.: Historical German text normalization using type-and token-based language modeling. arXiv preprint arXiv:2409.02841 (2024). 2

[FKG25] FLEISCHHACKER D., KERN R., GÖDERLE W.: Enhancing OCR in historical documents with complex layouts through machine learning. International Journal on Digital Libraries 26, 1 (2025), 3. 1, 2

[KLKG25] KANERVA J., LEDINS C., KÄPYAHO S., GINTER F.: OCR error post-correction with llms in historical documents: No free lunches. arXiv preprint arXiv:2502.01205 (2025). 1, 2

[kme02] Kmetijske in rokodelske novice. https://nl.ijs.si/ imp/nuk/dl/NUKP14041-1843.html, (1843–1902). Digitized by the National and University Library of Slovenia (NUK). 3

[MLK20] MARTÍNEK J., LENC L., KRÁL P.: Building an efficient OCR system for historical documents with little training data. Neural Computing and Applications 32 (2020), 17209–17227. 2

[PBD∗25] POZNANSKI J., BORCHARDT J., DUNKELBERGER J., HUFF R., LIN D., RANGAPUR A., WILHELM C., LO K., SOLDAINI L.: olmOCR: Unlocking trillions of tokens in pdfs with vision language models. arXiv preprint arXiv:2502.18443 (2025). 4

[RSWP18] REUL C., SPRINGMANN U., WICK C., PUPPE F.: State of the art optical character recognition of 19th century fraktur scripts using open source engines. arXiv preprint arXiv:1810.03436 (2018). 2

