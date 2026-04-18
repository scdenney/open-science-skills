# arXiv:2504.00414v1[cs.CL]1 Apr 2025

## MULTIMODAL LLMS FOR OCR, OCR POST-CORRECTION, AND NAMED ENTITY RECOGNITION IN HISTORICAL DOCUMENTS

#### Gavin Greif∗

Centre for Economic and Social History University of Oxford gavin.greif@history.ox.ac.uk

#### Niclas Griesshaber∗

Department of Economics University of Mannheim niclas.griesshaber@uni-mannheim.de

Robin Greif Department of Theoretical Physics University of Oxford robin.greif@physics.ox.ac.uk

April 2, 2025

### ABSTRACT

We explore how multimodal Large Language Models (mLLMs) can help researchers transcribe historical documents, extract relevant historical information, and construct datasets from historical sources. Specifically, we investigate the capabilities of mLLMs in performing (1) Optical Character Recognition (OCR), (2) OCR Post-Correction, and (3) Named Entity Recognition (NER) tasks on a set of city directories published in German between 1754 and 1870. First, we benchmark the off-the-shelf transcription accuracy of both mLLMs and conventional OCR models. We find that the best-performing mLLM model significantly outperforms conventional state-of-the-art OCR models and other frontier mLLMs. Second, we are the first to introduce multimodal post-correction of OCR output using mLLMs. We find that this novel approach leads to a drastic improvement in transcription accuracy and consistently produces highly accurate transcriptions (<1% CER), without any image pre-processing or model fine-tuning. Third, we demonstrate that mLLMs can efficiently recognize entities in transcriptions of historical documents and parse them into structured dataset formats. Our findings provide early evidence for the long-term potential of mLLMs to introduce a paradigm shift in the approaches to historical data collection and document transcription.

### 1 Introduction

The rate at which researchers can collect historical evidence is constrained by their ability to access the relevant sources, accurately transcribe them, and extract the desired information. While a global effort to scan historical sources is gradually reducing access barriers, the need for manual labor in the transcription and extraction of historical information remains a major bottleneck. To remedy this, researchers have come up with a wide range of (semi-)automated solutions to transcribe images of historical documents and extract the desired information from the generated transcriptions. However, existing solutions are either inaccurate or require significant technical expertise and manual annotations. In this paper, we introduce a new approach, which addresses these existing problems by leveraging multimodal Large Language Models (mLLMs). Our approach accurately transcribes historical documents and efficiently parses the information they contain into structured datasets.

Since it is impossible to exhaustively benchmark our approach for all languages, fonts, and layouts found in historical sources in a single paper, we focus our attention on historical Latin-alphabet prints. While this may seem restrictive,

∗These authors share first-author contribution.

by 1800, already over 1.7 million books that fall into this category had been published across Europe [1]. The rates of book production further increased across the nineteenth and twentieth centuries, and by 1910, Germany alone was publishing well over 30,000 new titles every year, almost as many as France, England, and the US combined [2]. Importantly, Latin-alphabet Europe was divided until the mid-twentieth century, with German-speaking and Lutheran Europe predominantly using Blackletter fonts (e.g., Fraktur) and the rest using Roman fonts (e.g., Antiqua) [3]. While automating the accurate transcription is undoubtedly easier for printed than handwritten texts, historical typefaces, especially Blackletter ones, have posed a significant challenge to automating historical document transcription [4].

To demonstrate how exactly our generalized approach outperforms existing solutions, we use a corpus of thirty pages drawn from city directories published across German-speaking Europe between 1754–1870. City, trade, and business directories are an important source for economists, historians, and genealogists, as they offer individual-level micro-data for periods and places where alternative sources (such as censuses) are not available [5]. For German-speaking Europe alone, well over 40,000 surviving directories, each containing thousands of entries, have been located [6]. Yet, this cornucopia of historical data has, thus far, not been economic to transcribe. The thirty pages in our corpus include the typical challenges associated with the machine transcription of historical printed texts, including multiple historical typefaces, excess visual information in the scans, skewed texts, handwritten marginalia, discolored backgrounds, print errors, different historical fonts on the same page, and various visual artifacts. All pages in the corpus were manually transcribed and corrected several times to generate the ground truth for the evaluation of our approach.

We make three contributions in this paper. First, we benchmark the transcription capabilities of mLLMs. We compare the transcription performance of two leading mLLMs (Gemini 2.0 Flash; GPT-4o) against the leading off-the-shelf models for nineteenth century historical prints (Transkribus’ Text Titan I and Print M1) and a widely used conventional OCR engine (Tesseract 5.5.0, "deu_frak"). We find that in a one-shot setting, Gemini 2.0 Flash achieves the highest accuracy out of all tested models and that its off-the-shelf transcription accuracy is comparable to that of corpus-finetuned OCR models reported in the literature for similar documents. Second, we are the first to introduce mLLM OCR Post-Correction for historical texts. We show that by combining the original source image and a noisy transcription, mLLMs can substantially increase the accuracy of OCR output, thus demonstrating that, by focusing on text-only post-correction, existing research has missed the full potential of mLLMs. Finally, we explore the capabilities of mLLMs in recognizing entities in our irregularly structured historical sources. We provide early evidence indicating that mLLMs offer an accessible and efficient solution to identifying and parsing historical information. We find that, while a direct parsing of information from images into the dataset is possible, separating out the steps and including mLLM-based OCR Post-Correction yields the highest accuracy. We release all code and data used in this paper.2

### 2 Related Work

#### 2.1 The Traditional OCR Pipeline

While research on automating the transcription of historical documents is vast, existing research typically focuses on one or multiple parts of what we call the traditional pipeline. This standard workflow follows a sequential process, consisting of separate pre-processing, layout recognition, character recognition, and post-processing stages. Depending on the project, a separate Named Entity Recognition (NER) stage may be employed to classify information contained in the post-processed transcription. While existing work on this traditional pipeline is too vast to be discussed here in full, a brief review of it is necessary to highlight the challenges of automating historical document transcriptions, the existing approaches to resolving them, and the way in which mLLMs have been used in this context.

The first step of the traditional pipeline is the pre-processing of the images of the historical source. If present, excess visual information, such as parts of another page, the book frame, dark spaces, or an archive footer, are removed during this step. Moreover, the image may be de-skewed and processed through denoising and gray-scaling or binarization to remove unwanted artifacts and increase the contrast between the text and the page background [7, 8, 9]. For cases in which images are degraded, up-sampling has also been applied during pre-processing [10]. Despite many OCR engines having built-in pre-processing which automatically carries out some of these image manipulations and some researchers using tools such as You Only Look Once (YOLO) to automate some of the pre-processing [11], recent scholarship continues to rely on extensive tool-assisted manual pre-processing of source images [12].

The second step in the traditional pipeline is the recognition of the document layout. This involves, inter alia, image segmentation, line recognition, baseline detection, and reading order determination. While most modern transcription engines have built-in layout recognition capabilities that work well for single-column texts, more complex layouts often require a separate layout recognition step to ensure the correct reading order. The tools and approaches to automated

2Available at: https://github.com/niclasgriesshaber/llm_historical_dataset_benchmarking.git and https://github.com/niclasgriesshaber/gemini_historical_dataset_pipeline.git

layout recognition are many. However, what matters for the present paper is that, at the time of writing, the accurate recognition of complex layouts typically requires the custom fine-tuning of a model using significant amounts of annotated data or manual post-correction [13, 14, 15, 16, 17, 18].

The third step in the traditional pipeline is the recognition of the characters in the image. For historical sources, this is particularly challenging as there are an abundance of different historical typefaces, languages, and fonts. Conventional OCR engines such as Kraken, PyLaia, PeroOCR, or Calamari-OCR use a Convolutional Neural Networks (CNNs) for feature extraction, Bidirectional Long Short-Term Memory (BiLSTM) networks for sequence modeling, and Connectionist Temporal Classification (CTC) for decoding. Recently, this CNN-BiLSTM infrastructure has received competition from solutions that employ a transformer-based architecture such as TrOCR [19]. These allow selfsupervised pre-training and have especially been used for recognizing historical handwriting [20]. However, to achieve the highest transcription accuracies, existing solutions generally require corpus-specific fine-tuning [21, 22].

Finally, since character recognition solutions usually provide imperfect transcriptions, researchers generally apply one or more post-processing steps to further improve transcription accuracy. Traditional OCR Post-Correction approaches include, inter alia, manual post-correction, rules-based correction (e.g., dictionary-based), and probabilistic models (e.g., Hidden Markov Models) [23, 24, 25]. However, as in other parts of the traditional pipeline, deep-learning methods have become state-of-the-art in the post-correction of transcriptions of historical documents. While sequence-to-sequence models have been used for post-correction [26], most approaches currently use transformer-based architectures, typically based on BERT, T5, or their derivatives [27, 28, 29, 30, 31, 32, 33, 34]. Recent work has sought to further improve OCR Post-Correction by incorporating OCR and its post-correction to increase accuracy by using more contextual information [35, 36].

Researchers often want to classify or extract relevant information in their transcriptions. For this, BERT-based NER approaches are currently the standard solution. These have been found to be better at handling OCR noise, archaic spelling variations, and complex entity structures, and have been shown to outperform both Conditional Random Field (CRF) and BiLSTM-CRF based approaches Ehrmann et al. [37]. In NER too, the best results are typically achieved by fine-tuning a model to the specific dataset [38].

To enhance efficiency and accessibility, researchers often integrate multiple steps of this pipeline or provide a full end-to-end solution. These solutions can be both modular and integrated. For example, Petitpierre et al. [39] introduce a five-phase modular end-to-end pipeline consisting of layout analysis, text segment extraction, Handwritten Text Recognition, tabular structuring, and post-processing. Similarly, van Koert et al. [40] introduce a three-stage modular pipeline consisting of a layout analysis stage that uses Laypa for layout segmentation, an HTR stage built on Keras, and a post-correction stage. Simultaneously, various integrated end-to-end pipelines have been proposed with some, but not all, including NER capabilities [41, 42, 43, 44, 45]. Transkribus and OCR4All offer two user-friendly and accessible options for non-technical users seeking an end-to-end solution with comparatively easy ways to manually post-correct at various steps of the process [13, 46, 47].

#### 2.2 Multimodal Large Language Models in Historical Document Transcription

Despite the rapid development of mLLMs, the existing research on their applications for historical document transcription is limited. To our knowledge, there currently exists no work on their potential in aiding document pre-processing; however, a few projects have sought to test their transcription capabilities for historical documents. Li [48] found that for handwritten texts in French, Italian, Spanish, and Dutch published between the sixteenth and nineteenth centuries, fine-tuned TrOCR and CNN-BiLSTM models drastically outperform an unspecified Gemini model. Kim et al. [49] found that for (mostly) handwritten probation records from 1921 Belgium, Claude (prompted with two few-shot examples) produced a more accurate transcription than other OCR engines (EasyOCR, TrOCR, KerasOCR, Tesseract) and outperformed fine-tuned TrOCR versions. Humphries et al. [50] found that for their corpus of eighteenth and nineteenth century English handwriting, Gemini-1.5-pro, GPT-4o, and Claude-Sonnet-3.5 all achieved transcription accuracies comparable to and sometimes better than conventional state-of-the-art OCR algorithms. Ghiriti et al. [51] tested the transcription capabilities of GPT-4 Vision-Preview and its response to various artificially introduced distortions and degradations for a corpus of early twentieth century German-language Fraktur prints and found that it outperformed Tesseract, except for those documents with complex layouts.

The OCR Post-Correction literature has also seen several contributions discussing the applications of LLMs. However, remarkably, all existing work on mLLMs in OCR Post-Correction is exclusively text based and no existing work has leveraged the visual capabilities of mLLMs for OCR Post-Correction. For modern texts, the post-correction suitability of mLLMs appears undisputed. Working on the modern-font ICDAR 2013 and 2023 datasets, Chen and Zhou [27] found that GPT-3.5-turbo-0301 improved the accuracy of noisy OCR output. Similarly, Hajiali [29] found that for a corpus of modern texts, GPT-based post-correction outperformed a BERT-FastText model. For historical texts, however,

evidence is more ambiguous. Boros et al. tested various LLaMA, BLOOM(Z), OPT and GPT models on several historical datasets and concluded that “LLMs are not good at correcting transcriptions of historical documents of any kind, at least in the applied experimental setting. Not only do they not improve the original transcription, they usually degrade them, making LLM-based post-correction of historical transcriptions a rather distant and even dangerous prospect” [52, p.141]. Meanwhile, Thomas et al. [53] found that, for a corpus of nineteenth-century British newspaper transcriptions, LLaMA 2 outperformed a conventional BART-based post-correction approach. Similarly, Kanerva et al. [54] showed that for English historical material mLLMs achieve notable improvements in post-correcting OCR errors in a zero-shot setting, while for material in historical Finnish, only GPT-4o achieved a marginal improvement. In contrast to this existing scholarship, we include the source image to leverage the information contained within to allow the mLLM to correct formatting and transcription errors. This additional information reduces the task to finding mismatches, thereby reducing the need to guess - or even worse hallucinate - the intended meaning of words in the absence of visual reference information.

When it comes to information extraction and named entity recognition tasks, mLLMs have also received some attention. For historical transcriptions, initial evidence suggested that, early models, such as GPT-3.5, were not yet good at NER tasks [55]. González-Gallardo et al. [56] found that while fine-tuned historical NER models (Stacked NER; Temporal NER) clearly outperformed off-the-shelf instruction-tuned models (ChatGPT; LLaMA-chat; Mixtral; Zeyphr), the latter may still be helpful tools for human annotators. Most recently, however, Hiltmann et al. [57] have shown that for a nineteenth century German-language source, GPT-4o outperformed off-the-shelf Flair (ner-german-large) and SpaCy (de_core_news_lg) in NER tasks. While these results appear promising, the authors did not compare mLLMs to a corpus-fine-tuned model. Xie et al. [58] use GPT-4o to extract and classify relevant information in Swedish Patent Cards (1945-1975) directly from the image, yet offer no comparison in accuracy to alternative approaches. At the time of writing, BERT-based approaches continue to be dominant in recognizing entities in historical transcriptions and NER tasks are frequently limited to simple recognition of places and locations in a text [59]. However, in other domains such as medicine, mLLMs have proven to outperform or be comparable to human annotators in extracting and parsing relevant information [60]. Finally, it is worth noting that even in NER research outside of historical document transcription, generally, only GPT, LLaMA, and BloomZ were examined, while alternatives such as Gemini have not yet received attention [61].

### 3 Source and Dataset

The basis of our analysis is a corpus of thirty page-images, drawn from ten different city directories, published in German between 1754–1870 in the cities of: Aachen, Dresden, Leipzig, Frankfurt, Lübeck, Riga, and Trier. City and trade directories are an important source for economists, historians, and genealogists, as they offer systematic and regular micro-evidence on urban economic activity, social structure, and public office holders prior to the onset of modern census-taking. For German-speaking Europe, the “Verein für Computergenealogie” has located over 40,000 such directories and, through crowd-sourcing hobby genealogists, manually transcribed 4.4 million entries from these directories [6].

When it comes to automating transcription and information extraction, historical directories come with certain challenges. While directories generally contain the same information (e.g., first name, last name, occupation, address, and more.) they can follow vastly different layouts. Furthermore, while the structure of entries is usually internally consistent, many entries deviate from the structure and entries are mixed between those of individuals, businesses, and office holders. Moreover, different abbreviations in different directories, and non-standardized spelling over time and space, add further complexity. Thus, rules-based entity parsing approaches do not work in the case of directories.

Figure 1 shows images of the first page from each of the included directories. Importantly, our corpus features many of the most common challenges faced by researchers working with historical prints. These include ink degradation, discolored backgrounds, human annotations, skewed texts, 3D distortions, multiple historical fonts on the same page, and excess visual information. While our corpus is predominantly printed in Blackletter typefaces, one directory is printed in an Antiqua typeface (Frankfurt-1860 in Figure 1). There are also several pages in our corpus which contain different historical typefaces (including Italics) on the same page, a phenomenon considered enough of a challenge to warrant its own competition at ICDAR 2024 [62]. Finally, since we have sourced our images from archive websites, some directories contain archive-specific footers.

Figure 1: The First Page of each Directory in our Dataset

![image 1](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile1.png)

![image 2](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile2.png)

![image 3](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile3.png)

![image 4](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile4.png)

![image 5](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile5.png)

Aachen-1838 Dresden-1797 Leipzig-1753 Frankfurt-1860 Frankfurt-1778

![image 6](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile6.png)

![image 7](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile7.png)

![image 8](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile8.png)

![image 9](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile9.png)

![image 10](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile10.png)

Lübeck-1870 Dresden-1819 Riga-1810 Leipzig-1800 Trier-1853

### 4 Methodology

#### 4.1 Multimodal Large Language Model for OCR

The first of our three sets of experiments tests the OCR capabilities of mLLMs and benchmarks them against conventional OCR solutions. Given the large number of mLLMs available, selecting the right models for further analysis is paramount. In a preliminary step, we extensively tested models from various leading model families, including GPT, Gemini, Gemma, LLaMA, and Mistral, and for the purposes of conciseness, selected the two best performing models for further analysis. The first model we use is GPT-4o [63]. We use GPT-4o-2024-08-06, as later versions of this model occasionally refused to transcribe the text in some images. Moreover, our preliminary testing indicated that this model outperformed the more recent o1 reasoning model and the specialized Vision-Preview model. The second mLLM we use is Gemini 2.0 Flash [64, 65]. At the time of publication, there has not yet been a stable release of more advanced Gemini models such as Gemini 2.5 Pro. However, preliminary chat-based testing of Gemini 2.5 Pro Experimental 03-25 suggests that it may outperform Gemini 2.0 Flash across the different experiments in this paper. Where appropriate, we mention the results we achieved with Gemini 2.5 Pro Experimental 03-25 to highlight the continuing improvements of mLLMs in vision-related tasks.

Our approach to generating a transcription was identical, across both GPT-4o and Gemini 2.0 Flash. First, we set the temperature parameter to 0.0 in order to maximally constrain the mLLMs in their creativity and make their responses as deterministic and conservative as possible. Next, we converted the PDFs of the directories into PNG files for each page. Each page’s PNG file was then uploaded together with a carefully designed prompt via the API into the respective mLLM. Finally, the output of the mLLM for each page was concatenated to a TXT file, until all selected pages of the directory were processed.

As a comparison to the mLLMs, we included three standard OCR models in our analysis. The first, Tesseract 5.5.0, is a widely-used open-source OCR engine that employs an LSTM-based neural network for text recognition [66]. We use its “deu_frak” model, which has been fine-tuned to German-language Fraktur prints similar to those found in our corpus. While Tesseract’s architecture is arguably outdated, its accessibility means that it continues to be widely used by researchers working on historical prints [14, 49, 51, 67]. As with all other models, we do not carry out any additional pre- or post-processing of the transcription and solely use it as an off-the-shelf solution.

The second and third models we use were both created for Transkribus, a widely-used specialized end-to-end transcription software solution for historians, created by READ COOP [68, 69]. Both models were chosen due to their high accuracy for, and fine-tuning on, nineteenth century Fraktur prints. Transkribus’ Print M1 Model is based on PyLaia, which employs the common CNN-BiLSTM infrastructure that is also found in other OCR models (such as Kraken, PeroOCR, Calamari and more). The model has been trained on a broad set of Antiqua and Blackletter prints published in various European languages from the sixteenth century onwards [70]. Transkribus’ Text Titan I, on the other hand, is built on an adapted TrOCR infrastructure, thus using a Transformer-centered rather than a CNN-BiLSTM infrastructure. Just like Print M1, Text Titan I has been trained on a broad range of historical documents in various languages, although the precise nature of this training is not publicly disclosed [71]. Although TrOCR models with corpus-specific fine-tuning have been shown to yield very accurate results for handwritten texts [20], the limited existing evidence suggests that for Latin script prints, Transkribus’ Text Titan I outperforms a corpus-fine-tuned TrOCR model [72].

We use both Transkribus models through the Transkribus API. We feed the models individual images and convert the returned XML files into TXT files containing the respective transcriptions. Crucially, we do not pre- or post-process the transcriptions, nor do we add any separate layout recognition other than that inherent in the model itself. While doing so would increase the accuracy of the Transkribus’ models, our objective is finding an accessible, fast, off-the-shelf solution, hence we compare all models without any pre- or post-processing.

#### 4.2 Multimodal Large Language Models for OCR Post-Correction

In our second set of experiments, we turn our attention to the issue of OCR Post-Correction. For this, we take the highest performing non-mLLM transcription as a starting point. Whereas, as previously discussed, existing LLM-based approaches to OCR Post-Correction have been exclusively text-based, we adopt a multimodal approach to OCR Post-Correction. For this, we take the noisy transcription produced by the highest performing Transkribus model and feed it, together with a carefully designed prompt and the original PNG based on which this transcription was made, into the mLLM (Figure 2). Again, we do this one page at a time. This process returns plain text, which is saved in a new TXT file. In order to compare their respective performances in this task, we use both Gemini 2.0 Flash and GPT-4o separately. In our preliminary testing, we also explored a special case of mLLM OCR post-processing, where an mLLM uses its own previous transcription, together with the source image, as input. However, this approach did not create any noteworthy improvements in transcription accuracies, and consequently, we did not include it in our further analysis.

Figure 2: Multimodal LLMs for OCR and OCR Post-Correction

![image 11](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile11.png)

Notes: Each individual page in our dataset is sent to an mLLM as a PNG file with our refined prompt to perform OCR. For mLLM OCR Post-Correction, the OCR output of the best-performing Transkribus model is appended at the end of our prompt. Our prompt instructs the model to correct the OCR text and use the PNG file as additional guidance (indicated by the asterisk).

#### 4.3 Multimodal Large Language Models for Named Entity Recognition (NER)

In our third set of experiments, we test the NER capabilities of mLLMs. For this, we identify four variables in our source: First Name, Last Name, Occupation, Address. Every directory entry in our corpus contains a subset of these variables and our objective is to turn this information into a dataset format. For this, we prompt the mLLM to return structured output, assigning values explicitly in JSON format. We employ a prompt which features four explicit output examples (Figure 4). Subsequently, we convert the verbose JSON-format the mLLM returns into a CSV format, providing an easy to read and easy to analyze dataset. Although we did not explicitly test this, we hypothesize that the direct assignment of categories in JSON format may yield higher mLLM accuracy in entity recognition tasks.

We carry out this process for three different kinds of input. First, we use the ground truth (GT) TXT file as input. This provides the best-case scenario to evaluate the entity recognition capabilities of mLLMs in the historical document transcription without relying on visual information. Next, we test to what extent the NER accuracy declines in the face of a noisy transcription compared to the GT TXT. This is particularly important, given the significant attention that has been paid to the role of OCR noise (and the need to reduce it) in the existing NER literature [73, 74, 75]. Finally, we test whether mLLMs are capable of extracting and recognizing entities directly from a PNG image without prior transcription (Figure 3). This may allow the mLLMs to use visual information in the image, which is not present in the TXT files, to improve their entity recognition performance. However, this may also yield lower accuracies as the transcription error rate will likely be higher than that of the post-corrected noisy transcription it is compared to. Crucially, this final step tests the capabilities of mLLMs as integrated end-to-end solutions for transcription and entity recognition in an environment without pre- or post-processing. As mLLMs further improve their capabilities, this will increasingly become relevant.

Figure 3: Multimodal LLMs for NER

![image 12](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile12.png)

Notes: Each individual page in our dataset is sent to an mLLM as a PNG file with our prompt (Figure 4). We concatenate the JSON mLLM outputs and convert them into a CSV format. Additionally, we test the performance of LLMs by concatenating the ground truth text and Transkribus Print M1 OCR output below our prompt without providing any image input.

#### 4.4 Prompt Engineering

Given the centrality of mLLMs in our work, a brief comment on our prompt development approach is necessary. The issue of prompting is particularly important given that, for any given task, the performance of an mLLM can be significantly influenced by even minor variations in how a prompt is written [76]. Non-AI-experts, in particular, have been found to have difficulties in developing effective prompts for their tasks [77]. When it comes to the use of mLLMs in the transcription of historical documents or their post-correction, researchers have employed relatively simplistic prompts, which, most likely, did not elicit the maximum performance potential of the mLLMs they tested [48, 51]. Even those researchers testing more ‘complex’ prompts may have fallen short of exploring the full potential associated with optimal prompting [50, 52, 49].

We have adopted an iterative mLLM-assisted approach to prompt design. To develop our prompts for the transcription and named entity recognition tasks, we began by explaining our objectives to Gemini 2.0 Flash and asked it to generate a suitable prompt in Markdown format. Subsequently, we iteratively refined this prompt by asking the model to solve problems we were facing. For example, initially, our character recognition prompt struggled to ignore partial pages (e.g., Aachen-1838 in Figure 1). Conventional approaches would have cropped these partial pages in a separate pre-processing step. However, we instructed the model to change the prompt to ensure these partial pages were not included in the transcription. Interestingly, even though no word of our final prompt was written by a human, the final prompt structure we achieved through this iterative process resembles that which is recommended in the literature [78]. Notably, our approach to prompt engineering resulted in several unexpected, almost comical and absurd, but efficiency-enhancing additions to the prompt, such as the all capital letters line “FAILURE TO FOLLOW THESE RULES EXACTLY WILL RESULT IN TOTAL SYSTEM FAILURE” (Figure 4). This suggests that mLLM-assisted approaches to prompt design may yield better results than human-only approaches. While important and fascinating, a comprehensive analysis of this question is beyond the scope of this paper.

Figure 4: Prompt for PNG-to-CSV NER task

YOU ARE AN EXPERT HISTORIAN. YOUR TASK IS TO EXTRACT DATA FROM A SCAN OF A GERMAN BUSINESS DIRECTORY. FAILURE TO FOLLOW THESE RULES EXACTLY WILL RESULT IN TOTAL SYSTEM FAILURE. THERE IS ZERO ROOM FOR ERROR.

STRICT JSON FORMAT - NO EXCEPTIONS:

- - OUTPUT MUST BE VALID JSON.
- - NO MARKDOWN, NO EXPLANATIONS, NO HEADERS. FIELDS (STRICTLY NOTHING ELSE):
- - "first and middle names" (string)
- - "surname" (string; can also be a company name)
- - "occupation" (string; "Wittwe" is NOT an occupation)
- - "address" (string; full address if possible, otherwise partial) NON-NEGOTIABLE RULES:


- 1. **EXTRACT EXACTLY AS WRITTEN. NO MODERNIZATION. NO INTERPRETATION. NO CHANGES.**
- 2. **ONLY TRANSCRIBE TEXT FROM THE MAIN PHYSICAL BOOK PAGE. ANY TEXT FROM ADJACENT PAGES MUST BE ERASED FROM EXISTENCE.**
- 3. **IF A WORD IS PARTIALLY VISIBLE OR CUT-OFF, IT DOES NOT EXIST. IT MUST BE IGNORED.**
- 4. **IF A FIELD IS MISSING, SET IT TO NULL. DO NOT GUESS. DO NOT INFER. DO NOT ATTEMPT TO RECONSTRUCT.**
- 5. **DO NOT ADD EXTRA INFORMATION. DO NOT ADD COMMENTS. DO NOT ADD ANYTHING OUTSIDE THE REQUIRED FIELDS.**
- 6. **DO NOT CONCATENATE OR MERGE ADDRESS FRAGMENTS FROM MULTIPLE ENTRIES. EACH ENTRY MUST REMAIN INTACT AS SEEN IN THE TEXT.**
- 7. **IF MULTIPLE ADDRESSES EXIST FOR ONE ENTRY, KEEP THEM EXACTLY AS WRITTEN. DO NOT REFORMAT.**


STRICTLY ENFORCED EXAMPLE OUTPUT: [

{

"first and middle names": "Wilhelm Friedrich", "surname": "Becker", "occupation": "Schulmeister", "address": "Alexanderplatz C201"

}, {

"first and middle names": "Johann Georg", "surname": "Weber", "occupation": "Apotheker.", "address": "auf der Lindenhöhe"

}, {

"first and middle names": "Karl August", "surname": "Meyer", "occupation": "Buchdrucker", "address": "Hauptstraße 14, neben der Kirche"

}, {

"first and middle names": null, "surname": "Müller & Co.", "occupation": "Textilwarenhandel", "address": "Schlossallee 3"

}

] FINAL COMMANDS - NO EXCEPTIONS:

- - **IF A WORD OR ENTRY IS FROM AN ADJACENT PAGE, IT IS DEAD TO YOU. ERASE IT.**
- - **IF AN ENTRY IS CROPPED OR UNCLEAR, IT MUST BE OBLITERATED. DO NOT INCLUDE.**
- - **OUTPUT MUST BE PURE, PERFECTLY FORMATTED JSON. NOTHING ELSE.**
- - **FAILURE TO FOLLOW THESE RULES PRECISELY MEANS THE TASK IS COMPROMISED. THERE IS ZERO ROOM FOR ERROR.**


### 5 Evaluation Metrics

#### 5.1 Measuring Transcription Accuracies

To evaluate the accuracy of our transcriptions, we calculate the Levenshtein Distance, Character Error Rate (CER) and Word Error Rate (WER). The Levenshtein distance counts the minimum number of single-character edits (insertions, deletions, or substitutions) to transform the generated transcription into our ground truth and vice versa [79]. The CER is calculated by dividing the Levenshtein distance by the total number of characters in the ground truth.

Levenshtein Distance Total number of characters in ground truth (N)

CER =

Insertions + Deletions + Substitutions N

=

Analogously, the WER is calculated by summing the number of insertions, deletions, and substitutions at the word level and dividing this by the number of total words.

Despite their widespread usage, CERs and WERs must be interpreted cautiously. Different OCR tools, such as TextEval, ocrevalUAtio, and dinglehopper use different normalization rules for special Unicode codepoints occurring in historical texts [80]. Furthermore, some researchers inflate their reported accuracy rates, and deflate their CERs and WERs, by limiting their evaluation to certain characters – such as only a-z, A-Z, and 0-9 – thus ignoring the errors in recognizing punctuation, special characters, and line-breaks [81]. Others have used a “Flex OCR” measurement which ignores the order of characters and solely focuses on the accuracy of individual characters, thus providing a higher tolerance for errors related to layout and structure [82, 83]. In this paper, we report both non-normalized and normalized CERs and WERs. This allows us to report the strict accuracy of our transcriptions, as well as a more lenient interpretation which facilitates comparison with existing and future work. The normalized CERs and WERs are limited to ASCII character, exclude punctuations, and ignore whether a letter is upper or lower case. Importantly, this also removes errors introduced due to different decisions in the face of ambiguity in historical transcriptions. For example, in our sources, as was standard practice at the time, the German Umlaut was frequently written as a tiny e above the a, o, or u. While many human transcribers would transcribe this as a¨, a few might go out of their way to find the ae. Faded ink, print errors, and visual artifacts are all additional sources of ambiguity in the source material and consequently may cause variation in transcriptions even between different experts.

#### 5.2 Evaluating Named Entity Recognition

To evaluate the performance of our entity recognition tasks, we compare the final CSV files to a manually collected CSV ground truth that was cross-checked multiple times. We adopt both a strict and a fuzzy matching evaluation. For strict matching, we simply evaluate whether two cells have the identical string as content, and report a binary outcome depending on whether these match or not. There are, however, two problems with strict matching. First, we have observed that LLMs will sometimes include punctuation at the end of an entry, where the human-generated ground truth does not. While strict matching reports this as a mismatch, for the purposes of research, these two cells are functionally the same. Second, when recognizing entities directly from the image or from a noisy transcriptions, errors may be introduced not due to erroneous parsing, but rather due to errors in character recognition. Thus, for example, the LLM may transcribe a cell as “Dünker” whereas it is “Düntzer” in the ground truth. Similarly, the transcription “Reg.-Bote” would be considered incorrect compared to “Reg.=Bote”, despite being functionally the same for historians (Figure 5). Thus, we report fuzzy matching rates. For this, we use the Jaro-Winkler similarity with the common scaling factor of 0.9 [84]. This allows cells to still count as correct even if there are minor errors such as a wrongly transcribed character, missing whitespaces, or an extra piece of punctuation. Finally, another challenge of evaluating the NER task is that, for every directory, mLLMs have to first generate a single dataset from three individual PNGs. If the concatenated LLM-generated CSV does not have the same number of rows after a single attempt, we exclude this directory from our evaluation.

Figure 5: Visualization of NER Results for Gemini 2.0 Flash

![image 13](greif-griesshaber-greif-2025-multimodal-llms-ocr_images/imageFile13.png)

Notes: Green cells indicate matches between the manually produced ground truth and the mLLM-generated CSV for purposes of illustration. Cells where the ground truth did not exactly match the LLM-generated array are in red. For these cells, the LLM-generated string and ground truth string are displayed side-by-side. The string to the right of “/” displays the ground truth string, indicated by “(gt)”. The figure only depicts the first few entries of Trier-1853. The CSV was created using Gemini 2.0 Flash (PNG-to-CSV).

### 6 Results and Discussion

#### 6.1 Ambiguity, Transcription Errors and Efficiency

Although among historians human transcription is still widely regarded as the gold standard, when evaluating the performance of mLLMs and other transcription and entity parsing solutions, it is important to keep in mind that human transcriptions rarely achieve a 0% CER, especially not without extensive post-correction. This is partly due to the ambiguities present in historical sources and the individual judgments inherent in the transcription and entity classification. For example, Dresden-1797 is a sub-heading-based directory and below one of the sub-headings there is an entry which simply states that the house at this address had burnt down. While there are no names or occupation listed, some researchers may choose to omit this entry from their dataset, while others may note down the address without any further information. Similarly, some models report "Wittwe" (widow) as an occupation for entries, whereas the makers of the ground truth considered this to not be an occupation, and thus, left the field blank (Figure 5).

The second reason why we must discard the illusion of humans having perfect accuracy is that humans make errors. Even in prints with modern fonts, human transcribers have been observed to consistently make errors, especially when it comes to visually similar letters such as i, I, l, 1, o, e, or c [85]. While precise figures are scarce, one study testing non-specialized humans transcribing early modern venetian handwriting found CERs between 10.47% and 13.28% [86]. In fact, even professional data entry companies only guarantee an accuracy of 99% for modern fonts and possibly lower for difficult and historical material [50]. The human propensity to make mistakes was also evident in our own ground truth generation process, which demanded multiple rounds of revisions to eliminate errors. Indeed, it is common practice to task multiple humans with a transcription, when perfect transcription accuracy is needed. Thus, in our interpretation of the results, we must not assume that a non-zero error rate means that the machine-based solution performs worse than human transcribers, but rather, that at a very low level, say below 1% CER, the transcription accuracy can be interpreted as comparable to that of a human transcriber.

While our primary interest is the evaluation of accuracy rates, it is also important to consider speed, cost, and accessibility when determining the best tool. Table 1 summarizes the speed and price across the models used. Importantly, Gemini 2.0 Flash outperforms GPT-4o and both Transkribus models both in speed and price. Moreover, it worth noting, especially for a chronically funding-scarce field such as history, that Gemini 2.0 Flash is currently free to use for up to 15 requests per minute, up to 1 million tokens per minute, and up to 1,500 requests per day.

Table 1: Model Performance and Token Costs

#### Model s/page $/1,000 pages

Gemini 2.0 Flash 11.50 Free GPT-4o 18.23 10.84 Transkribus Print M1 46.93 54.25 Transkribus The Text Titan I 44.63 108.50 Tesseract “deu_frak” 13.77 Free

Notes: s/page represents the average processing time per page, computed from the log files of our replication runs. Price per 1,000 pages was estimated based on input and output tokens of our 30-page corpus. We converted the current price of 1,000 Transkribus credits (199C) based on the market exchange rate at the time of writing ($217). The fine-tuned Tesseract model “deu_frak” was run locally on a MacBook Pro with an Apple M1 chip.

#### 6.2 Multimodal Large Language Models for OCR and OCR Post-Correction

- Table 2 summarizes the CERs and WERs for the first two sets of experiments in which we benchmark the capabilities of mLLM to perform OCR and OCR Post-Correction, as well as conventional OCR models, on our dataset. Because Tesseract’s "deu_frak" model only achieved an average normalized CER of 30.22% and an average normalized WER of 199.91%, and thus, was massively outperformed all other models, its results were omitted from the table to enhance clarity.


The results table reveals that Gemini 2.0 Flash achieved the lowest error rates. With no pre-processing, no postprocessing, and no corpus-specific model fine-tuning, it produced the most accurate transcription out of all tested models. Gemini 2.0 Flash achieved a normalized CER of 1.27% across the whole corpus compared to 3.67% for Print M1, 4.16% for Text Titan I, and 6.31% for GPT-4o. Crucially, the per-directory analysis reveals that Gemini 2.0 Flash outperforms the other models in most cases, although for a few directories, Print M1 is marginally better (Dresden 1797; Riga 1810; Leipzig 1800). Impressively, across several directories (Aachen-1838, Frankfurt-1860, Lübeck-1870, and Trier-1853) Gemini 2.0 Flash achieved below 1% CER.

While all other directories are primarily printed in Fraktur typefaces, Frankfurt-1860 is a special case worth exploring further, as it is the only directory included which is primarily printed in Antiqua. This is also the only directory where other models (Print M1 & Text Titan I) also achieved a below-1% CER. Gemini 2.0 Flash, however, achieved an impressive 0.11% normalized and 0.38% non-normalized CER. For comparison, researchers working on the similarly Antiqua-font Paris Directories applied off-the-shelf solutions and found that the best model, PeroOCR, achieved a CER of 3.78%, with Tesseract and Kraken achieving 6.56% and 15.72% respectively [87].

Although, due to the previously discussed variations in calculating error rates, comparisons must be applied cautiously, Gemini 2.0 Flash appears to outperform a number of existing solutions to transcribing historical prints, both Fraktur and non-Fraktur. For example, the “Historical Document Processing and Analysis Framework” (HDPA), a conventional, albeit not widely adopted, solution to transcribing historical documents built around a CNN-BiLSTM OCR infrastructure and corpus fine-tuning, only achieved a CER of 2.4% for a sample of nineteenth century German newspaper pages printed in Fraktur font [88]. Earlier approaches using book-specific fine-tuning for early modern and nineteenth century German-language Fraktur prints reported CERs of between 0.4-3.5% [21]. Other pipelines, such as OCR4All, have reported a CER of between 0.06–4.89% for novels printed in nineteenth century Germany when applied without corpus-specific fine-tuning [13]. Meanwhile, for poly-font historical sources, one model achieved a CER of around 2% off-the-shelf for early modern books while a more fine-tuned model achieved a CER of 1.47% [89]. Finally, using manual correction of layout recognition errors and a source-specific fine-tuning of Calamari OCR, Albers and Kappner [12] achieved a 0.75% CER for a single city directory from 1880 Berlin.

The results also reveal that mLLMs are a powerful tool for OCR Post-Correction tasks. Out of all tested approaches, applying post-correction using Gemini 2.0 Flash to the noisy transcription of Print M1 achieved the lowest average error rates. This approach achieved an overall normalized CER of just 0.84%, and as low as 0.08% normalized CER in the case of Trier-1853. Applying the same post-correction approach using GPT-4o also resulted in remarkable improvements in error rates compared to both Print M1 and GPT-4o on their own, however, the results were slightly worse than in the post-correction approach using Gemini.

Table 2: OCR and OCR Post-Correction Results for Multimodal LLMs and Standard OCR Algorithms

Transkribus Print M1 ↓ Gemini 2.0 Flash

Transkribus Print M1 ↓ GPT-4o

Transkribus The Text Titan I

Transkribus Print M1

Gemini 2.0 Flash GPT-4o

Source CER WER CER WER CER WER CER WER CER WER CER WER Normalized (converted to lowercase; with non-ASCII characters, punctuation, line breaks, tabs, and extra whitespaces removed)

- Aachen-1838 0.56% 4.01% 8.30% 59.29% 3.54% 25.32% 3.30% 23.56% 0.40% 2.88% 0.65% 4.65%

- Dresden-1797 1.70% 11.93% 5.98% 41.83% 1.94% 13.58% 1.34% 9.36% 1.02% 7.16% 1.18% 8.26%

- Leipzig-1753 1.91% 12.25% 4.54% 29.08% 1.99% 12.75% 1.94% 12.42% 0.92% 5.88% 0.82% 5.23% Frankfurt-1860 0.11% 0.78% 4.02% 29.38% 0.38% 2.77% 0.59% 4.32% 0.14% 1.00% 0.27% 2.00% Frankfurt-1778 2.86% 18.39% 5.22% 33.56% 17.92% 115.17% 14.16% 91.03% 1.82% 11.72% 2.43% 15.63%

- Lübeck-1870 0.42% 2.55% 8.96% 54.92% 10.23% 62.69% 9.81% 60.14% 0.45% 2.78% 0.38% 2.32% Dresden-1819 1.40% 9.38% 8.96% 60.08% 2.17% 14.57% 1.76% 11.76% 0.96% 6.44% 1.46% 9.80%

- Riga-1810 1.96% 13.63% 6.18% 43.01% 1.91% 13.27% 1.68% 11.68% 1.98% 13.81% 1.88% 13.10%

- Leipzig-1800 2.77% 14.78% 8.06% 43.06% 2.79% 14.90% 2.34% 12.48% 1.65% 8.79% 1.76% 9.43% Trier-1853 0.68% 4.72% 3.01% 20.74% 3.98% 27.47% 3.46% 23.89% 0.08% 0.57% 0.33% 2.29%

- Full Sample 1.27% 8.41% 6.31% 41.76% 4.16% 27.55% 3.67% 24.26% 0.84% 5.55% 1.00% 6.61% Non-normalized (original casing preserved; only line breaks, tabs, and extra whitespaces removed)

Aachen-1838 0.57% 4.49% 7.68% 61.54% 3.96% 31.73% 3.86% 30.93% 0.56% 4.49% 0.92% 7.37% Dresden-1797 2.93% 21.34% 7.67% 55.77% 3.41% 24.78% 3.29% 23.92% 2.15% 15.66% 2.89% 21.00% Leipzig-1753 2.15% 15.03% 5.17% 36.11% 3.07% 21.41% 2.78% 19.44% 1.57% 10.95% 1.57% 10.95% Frankfurt-1860 0.38% 3.04% 4.42% 35.00% 0.91% 7.17% 0.91% 7.17% 0.36% 2.83% 0.54% 4.24% Frankfurt-1778 6.12% 38.63% 8.32% 52.52% 23.04% 145.17% 19.50% 123.14% 6.63% 41.85% 7.43% 46.88% Lübeck-1870 1.80% 12.39% 10.17% 69.96% 11.67% 80.26% 11.20% 77.08% 2.47% 17.00% 2.17% 14.91% Dresden-1819 3.13% 22.04% 11.02% 77.45% 4.60% 32.35% 3.81% 26.80% 2.82% 19.85% 3.45% 24.23% Riga-1810 2.32% 18.20% 6.09% 47.70% 2.39% 18.73% 2.19% 17.14% 2.30% 18.02% 2.57% 20.14% Leipzig-1800 3.03% 18.81% 8.65% 53.75% 3.38% 20.97% 2.97% 18.42% 2.25% 13.98% 2.35% 14.61% Trier-1853 0.86% 6.52% 3.24% 24.54% 4.52% 34.18% 4.09% 30.92% 0.37% 2.84% 0.64% 4.82%

- Full Sample 2.08% 14.97% 7.19% 51.82% 5.46% 39.37% 4.95% 35.72% 1.91% 13.77% 2.17% 15.62%














Notes: Evaluated off-the-shelf models are Gemini 2.0 Flash, GPT-4o, Transkribus The Text Titan I, and Transkribus Print M1. We combined the best performing Transkribus and mLLM to evaluate mLLM OCR Post-Correction, indicated in the two columns on the right-hand side. Columns report CER and WER. “Source” lists our ten directories. Results are given for both normalized text (converted to lowercase; with non-ASCII characters, punctuation, line breaks, tabs, and leading, trailing, and consecutive internal whitespaces removed) and non-normalized text (original casing preserved; only line breaks, tabs, and leading, trailing, and consecutive internal whitespaces removed). The best CER results per row are in bold.

A closer look at the results reveals an important insight regarding the need for pre-processing. As would be expected, all non-mLLM models performed poorly on Aachen-1838, Frankfurt-1778, and Lübeck-1870, all of which contain parts of another page in their original image. In the traditional pipeline, this information would have been cropped rather than being included; however, in our case we deliberately decided not to do this. Instead, we demonstrate that, with proper prompting, mLLMs do not require any pre-processing, and thus, are more effective than existing OCR solutions in this regard. Moreover, the same result can be achieved by solely using mLLMs for OCR Post-Correction, rather than the transcription itself, which suggests a remarkable level of visual understanding and processing capabilities in these models. While this issue somewhat inflates overall error rates for the non-mLLM models, Gemini 2.0 Flash still outperforms or, at worst, is roughly equivalent in accuracy to, the Transkribus models on all other directories.

The transcription and post-correction results also offer potential questions for further research. For example, one may hypothesize a correlation between transcription accuracy and quality of input images. Frankfurt-1778, the directory with consistently the highest error rates, has been pre-processed before, yet apparently, not very well. In this special case, the pre-processing may have removed too much visual information when it sought to decrease non-relevant visual information in the image, and therefore, inhibited the performance of the different transcription models. Alternatively, one may hypothesize that Trier-1853 was transcribed more accurately than other directories due to the comparatively high contrast between the text and the background. One may also wish to investigate whether, and to what extent, other image properties such as image resolution or text-density may impact mLLM transcription performance. While potential lines of inquiry are abundant, any investigation of such potential hypotheses lies beyond the scope of the present paper.

#### 6.3 Multimodal Large Language Models for Named Entity Recognition and Entity Parsing

- Table 3 reports the results of our NER experiments. From left to right, it reports the entity recognition when taking the ground truth (GT) text, the noisy OCR transcriptions, and the original images as inputs for Gemini 2.0 Flash and GPT-4o. The GT TXT-to-CSV results confirm that model families like Gemini and GPT can accurately identify and classify information in historical transcriptions. With the exception of Dresden 1797, Leipzig 1753, and Dresden 1819, over 90% and up to 99.49% fuzzy accuracy rates are achieved. The three directories with lower figures all share one common characteristic: they are organized by sub-headings. Thus, our results indicate that presently mLLMs struggle with identifying entities when sub-headings are used to indicate either the occupation or the address of subsequent entries. At the current level of development, mLLMs may find it difficult to understand a short line such as “nr 4” (which indicates the house number for all entries below it) as a sub-heading. Importantly, it is unclear whether traditional BERT-based solution would perform better here, and more research is needed to test this. While the sub-heading issue explains some of the observed heterogeneity in entity recognition performance across directories, it cannot account for all of it. Interestingly, however, font-type appears to have had no significant impact on parsing accuracy, with the mostly-Antiqua Frankfurt-1860 only achieving a 93.53% fuzzy match rate, compared to the 98.21% and 96.65% for the Fraktur font Aachen-1838 and Trier-1853.


Table 3: NER Results for Multimodal LLMs (pass@1)

Gemini 2.0 Flash Gemini 2.0 Flash Gemini 2.0 Flash GPT-4o GPT-4o GPT-4o (GT TXT-to-CSV) (OCR TXT-to-CSV) (PNG-to-CSV) (GT TXT-to-CSV) (OCR TXT-to-CSV) (PNG-to-CSV)

Source # Cells Strict Fuzzy Strict Fuzzy Strict Fuzzy Strict Fuzzy Strict Fuzzy Strict Fuzzy Aachen-1838 392 99.23% 99.49% 91.58% 98.21% 92.60% 98.21% 74.49% 99.23% 71.17% 98.72% - Dresden-1797 228 - - - - 43.42% 67.54% - - - - - Leipzig-1753 160 56.25% 73.75% 61.25% 75.00% 40.62% 68.12% 56.25% 77.50% 54.37% 76.88% - Frankfurt-1860 464 - - - - 87.50% 93.53% - - - - - Frankfurt-1778 136 66.18% 91.91% 57.35% 74.26% 39.71% 47.79% 62.50% 86.76% 53.68% 67.65% 34.56% 59.56% Lübeck-1870 360 67.78% 91.39% 64.72% 90.83% 46.94% 54.17% 62.50% 85.83% 50.56% 76.11% - Dresden-1819 352 75.00% 78.69% 69.60% 75.57% 58.52% 65.91% 74.72% 83.52% 71.88% 84.94% 36.08% 52.27% Riga-1810 276 73.19% 98.91% 63.04% 97.46% 64.13% 97.10% 73.55% 99.64% 63.04% 97.10% 31.88% 65.58% Leipzig-1800 308 77.27% 97.40% 70.13% 84.42% 63.64% 81.49% 75.65% 88.31% 75.32% 83.12% - Trier-1853 448 95.98% 96.43% 93.53% 95.31% 92.19% 96.65% 71.43% 96.43% 70.76% 96.21% - Full Sample 3124 77.48% 89.32% 74.92% 88.61% 68.76% 80.86% 70.35% 91.00% 65.67% 87.58% 34.29% 58.38%

Notes: We report strict and fuzzy match rates (%) for all directories. Before any evaluation, all cells were lowercased as well as leading and trailing whitespaces removed. After this basic normalization, two cells were strict matches if they were completely identical. For fuzzy matches, we allowed some differences by applying the Jaro-Winkler similarity with a threshold of 0.9. GT refers to ground truth.

Although there has been considerable research exploring how OCR errors impact downstream NLP tasks in conventional approaches [90, 91], our results indicate that the performance of mLLMs does not substantially decline with the introduction of OCR noise. Comparing GT TXT-to-CSV and OCR TXT-to-CSV results reveals that across the corpus, the presence of transcription errors only marginally decreases the achieved accuracy rates. Table 4 highlights performance changes for the different variables and models depending on the input used. For Gemini 2.0 Flash, entity recognition accuracy drops significantly for occupation and address recognition, but remains virtually the same for first and last names, when comparing GT to OCR text input. In contrast, GPT-4o sees a more consistent decline across the different variables measured, when going from GT to OCR text input.

Table 4: NER Results by Variables (pass@1)

Gemini 2.0 Flash* Gemini 2.0 Flash* Gemini 2.0 Flash GPT-4o* GPT-4o* GPT-4o* (GT TXT-to-CSV) (OCR TXT-to-CSV) (PNG-to-CSV) (GT TXT-to-CSV) (OCR TXT-to-CSV) (PNG-to-CSV)

Variable Strict Fuzzy Strict Fuzzy Strict Fuzzy Strict Fuzzy Strict Fuzzy Strict Fuzzy First names 95.72% 96.55% 91.28% 95.72% 83.23% 91.42% 92.11% 92.76% 88.98% 92.27% 57.59% 68.59% Surnames 94.90% 97.70% 91.28% 97.70% 83.87% 89.37% 94.24% 95.07% 83.88% 88.65% 43.98% 65.97% Occupation 75.82% 81.58% 68.75% 74.01% 48.91% 72.09% 78.62% 86.84% 74.18% 82.40% 26.18% 38.74% Address 53.78% 93.26% 48.36% 87.01% 59.03% 70.55% 16.45% 89.31% 15.62% 87.01% 9.42% 60.21%

Notes: We report strict and fuzzy match rates (in %) for all variables. Percentages are only based on mLLM-generated datasets that matched the ground truth CSV after one attempt. Empty entries in Table 3 indicate that these datasets did not match the number of rows in the manually produced ground truth. Here, experiments marked with an asterisk (*) indicate that these aggregated percentages are not based on all ten directories. Gemini 2.0 Flash (GT TXT-to-CSV) and (OCR TXT-to-CSV) are only based on eight directories as two of them did not match the number of rows of the ground truth after one pass. This is identical for GPT-4o, except that (PNG-to-CSV) is based on only three directories.

Our NER results, specifically our PNG-to-CSV results, also provide important insights into the capabilities of mLLMs to serve as an integrated end-to-end solution for the extraction of entities from historical documents. In the PNG-to-CSV task, Gemini 2.0 Flash, again, clearly outperformed GPT-4o. We cannot, however, conclusively determine to what extent this variation in performance is caused by differences in OCR performance rather than entity recognition performance. Given the black-box nature of both models, we also do not know how exactly they approach extracting entities from an image, and to what extent this may be different from extracting entities from text transcriptions. Similarly, without further testing, we are unable to conclusively show why some directories work well across all three approaches, while others see a drastic decline in accuracy rates when moving to a PNG-to-CSV approach. Nonetheless, what these results do reveal is that an entity extraction directly from the image of a historical source can already work very well in some cases. For some directories (Aachen-1838, Riga-1810, Trier-1853, Frankfurt-1860), Gemini 2.0 Flash achieved well over 90% and up to 98.21% fuzzy matching directly from the image. Moreover, it achieved a respectable fuzzy match rate of 80.86% across the entire corpus. While this figure is still far from perfect, it is likely to rapidly improve with new mLLM models. Indeed, in our chat-based testing of Gemini 2.5 Pro Experimental 03-25, we found that this newer, albeit still experimental, model achieved a pass@1 fuzzy match rate of 85.85% across our entire corpus and an increase in the fuzzy match rate of address information from 70.55% (Gemini 2.0 Flash) to 83.61% (Gemini 2.5 Pro Experimental 03-25). Notably, this newer model appears to no longer struggle with the sub-heading-based structure of some directories. This suggests that over time the capabilities of mLLMs to extract entities directly from an image of a historical source may continue to improve. At least for now, however, we find that using a post-corrected OCR output as input yields better results than using the original PNG of the historical document.

### 7 Conclusion

We have demonstrated that mLLMs can be effectively used for OCR, OCR Post-Correction, and NER tasks. For character recognition tasks, we found that without pre-processing, fine-tuning, or post-processing, Gemini 2.0 Flash achieved accuracy rates comparable to those achieved by corpus-fine-tuned models for similar sources in the existing literature. It also outperformed conventional off-the-shelf OCR models that were fine-tuned on similar sources and other mLLMs. The most accurate transcriptions in our experiments, however, were achieved by using Gemini 2.0 Flash in an mLLM OCR Post-Correction approach (0.84% CER). This demonstrates the significant potential of this new approach to OCR Post-Correction. Furthermore, the success of our this methodology reveals the shortcoming of the existing work using text-only LLM-based post-correction approaches. Finally, we offer early evidence that mLLMs offer an accessible solution for recognizing entities and extracting information from historical documents.

Despite our promising results, mLLMs still have room for improvement, particularly in NER tasks. Future models will very likely provide better results. For this reason, rigorous benchmarking of mLLMs on different historical fonts, layouts, and languages will be necessary to firmly establish the new role of mLLMs in historical research. The ideal solution to this may be the collaborative development of a historical OCR benchmark for mLLMs, akin to modern OCR benchmarks but specialized for the problems faced in historical document transcription [92]. Such work could draw on the broad range of historical ground truth datasets made available in the existing literature, and thus, provide a helpful tool for assessing and comparing the capabilities of different mLLMs in the transcription of historical documents and the extraction of relevant historical information.

While our methodological contribution and preliminary benchmarking offer important answers, there remain many open questions surrounding mLLMs and historical research. For example, we do not yet know how mLLMs fare on other historical sources, such as those written and printed in non-Latin-alphabet fonts. Research on this will be particularly important as conventional OCR engines have been found to perform worse for non-Latin-alphabet fonts in historical documents [93], and mLLMs have been found to perform worse in OCR tasks for modern documents in non-Latin scripts [94]. Moreover, mLLMs require a more in-depth comparison to conventional fine-tuned NER approaches than we were able to provide in this paper. Equally, more in-depth analyses of prompting approaches for historical data extraction may yield fascinating and unexpected insights. Indeed, the avenues for future research on mLLMs in historical research are plentiful, as their advent promises the potential of a paradigm shift in the approaches to historical data collection and research.

### Acknowledgements

We thank Aurelius Noble and Keenan Samway for helpful comments and suggestions. Gavin Greif gratefully acknowledges funding and support for the wider European Directories Project, of which this paper forms a part. This includes a Postgraduate/ECR Bursary from the German History Society, a Pollard Research Grant from Wadham College, University of Oxford, and transcription credits provided through the Transkribus Scholarship Programme.

### Author Contributions (CRediT)

Gavin Greif: Conceptualization; Methodology; Investigation; Data Curation; Writing - Original Draft; Writing Review and Editing; Funding acquisition. Niclas Griesshaber: Conceptualization; Formal Analysis; Validation; Investigation; Software; Visualization; Writing Review and Editing. Robin Greif: Conceptualization; Methodology.

### Use of AI Tools

The authors affirm that all sections of this manuscript were written and edited solely by themselves. After manual editing was completed, GPT-4.5 and Gemini 2.5 Experimental 03-25 were employed exclusively for final proofreading, including double-checking spelling, grammar, and style consistency. The code was written with the support of OpenAI’s o1-pro and Claude 3.7 Sonnet Thinking.

### References

- [1] Eltjo Buringh and Jan Luiten Van Zanden. Charting the “rise of the west”: Manuscripts and printed books in europe, a long-term perspective from the sixth through eighteenth centuries. The Journal of Economic History, 69

(2):409–445, 2009.

- [2] Lynne Tatlock. Introduction: The book trade and “reading nation” in the long nineteenth century. In Lynne Tatlock, editor, Publishing Culture and the “Reading Nation”: German Book History in the Long Nineteenth Century, Studies in German Literature, Linguistics, and Culture, pages 1–24. Camden House, Rochester, NY, 2010.
- [3] Albert Kapr. Fraktur: Form und Geschichte der gebrochenen Schriften. H. Schmidt, 1993. ISBN 978-3-87439260-0.
- [4] Christian Reul, Uwe Springmann, Christoph Wick, and Frank Puppe. State of the art optical character recognition of 19th century fraktur scripts using open source engines. arXiv:1810.03436 [cs.CV], 2018.
- [5] Gavin Greif. Merchants, Proto-Firms, and the German Industrialization: The commercial determinants of nineteenth century town growth. LSE Economic History Student Working Paper, No. 7, 2022.
- [6] Günter Junkers. Compgen-adressbuch-datenbank in der deutschen nationalbibliothek, 2023. URL https://www. compgen.de/2023/04/compgen-adressbuch-datenbank-in-der-deutschen-nationalbibliothek/. Accessed: 2025-03-18.
- [7] Maya R. Gupta, Nathaniel P. Jacobson, and Eric K. Garcia. OCR binarization and image pre-processing for searching historical documents. Pattern Recognition, 40(2):389–397, February 2007. ISSN 0031-3203. doi: 10.1016/j.patcog.2006.04.043.
- [8] Rose Holley. How good can it get? analysing and improving ocr accuracy in large scale historic newspaper digitisation programs. D-Lib Magazine, 15(3/4), 2009.
- [9] Alaa Sulaiman, Khairuddin Omar, and Mohammad F Nasrudin. Degraded historical document binarization: A review on issues, challenges, techniques, and future directions. Journal of imaging, 5(4):48, 2019.
- [10] Iclal Cetin Tas and Ahmet Anil Müngen. Using pre-processing methods to improve ocr performances of digital historical documents. In 2021 Innovations in Intelligent Systems and Applications Conference (ASYU), pages 1–5,

2021. doi: 10.1109/ASYU52992.2021.9598972.

- [11] Thomas Constum, Lucas Preel, Théo Larcher, Thierry Paquet, Pierrick Tranouez, and Sandra Brée. End-to-end information extraction in handwritten documents: Understanding paris marriage records from 1880 to 1940. In Document Analysis and Recognition – ICDAR 2024, volume 14806 of Lecture Notes in Computer Science, pages 195–214. Springer, 2024. doi: 10.1007/978-3-031-70543-4_12.
- [12] Thilo N. H. Albers and Kalle Kappner. Perks and pitfalls of city directories as a micro-geographic data source. Explorations in Economic History, 87, January 2023. ISSN 0014-4983. doi: 10.1016/j.eeh.2022.101476.
- [13] Christian Reul, Dennis Christ, Alexander Hartelt, Nico Balbach, Maximilian Wehner, Uwe Springmann, Christoph Wick, Christine Grundig, Andreas Büttner, and Frank Puppe. OCR4all—An Open-Source Tool Providing a (Semi-)Automatic OCR Workflow for Historical Printings. Applied Sciences, 9(22):4853, January 2019. ISSN 2076-3417. doi: 10.3390/app9224853.


- [14] David Fleischhacker, Wolfgang Goederle, and Roman Kern. Improving OCR Quality in 19th Century Historical Documents Using a Combined Machine Learning Based Approach, January 2024. URL http://arxiv.org/ abs/2401.07787. arXiv:2401.07787 [cs].
- [15] Zejiang Shen, Ruochen Zhang, Melissa Dell, Benjamin Charles Germain Lee, Jacob Carlson, and Weining Li. LayoutParser: A Unified Toolkit for Deep Learning Based Document Image Analysis. In Josep Lladós, Daniel Lopresti, and Seiichi Uchida, editors, Document Analysis and Recognition – ICDAR 2021, volume 12821, pages 131–146. Springer International Publishing, Cham, 2021. ISBN 978-3-030-86548-1 978-3-030-86549-8. doi: 10.1007/978-3-030-86549-8_9.
- [16] Nicolas Gutehrlé and Iana Atanassova. Processing the structure of documents: Logical Layout Analysis of historical newspapers in French. Journal of Data Mining & Digital Humanities, NLP4DH(Digital humanities in languages), May 2022. ISSN 2416-5999. doi: 10.46298/jdmdh.9093.
- [17] Filip Dobrani´c and Matevž Pesek. Estimating the Number of Annotations Required to Detect Content Types in Historical Newspapers. In Apostolos Antonacopoulos, Annika Hinze, Benjamin Piwowarski, Mickaël Coustaty, Giorgio Maria Di Nunzio, Francesco Gelati, and Nicholas Vanderschantz, editors, Linking Theory and Practice of Digital Libraries, pages 115–124, Cham, 2024. Springer Nature Switzerland. ISBN 978-3-031-72440-4. doi: 10.1007/978-3-031-72440-4_11.
- [18] Thibault Clérice. You Actually Look Twice At it (YALTAi): using an object detection approach instead of region segmentation within the Kraken engine. Journal of Data Mining & Digital Humanities, Historical Documents and automatic text recognition, December 2023. ISSN 2416-5999. doi: 10.46298/jdmdh.9806.
- [19] Phillip Benjamin Ströbel. Flexible Techniques for Automatic Text Recognition of Historical Documents. PhD thesis, University of Zurich, Zurich, Switzerland, 2023.
- [20] Phillip Benjamin Ströbel, Simon Clematide, Martin Volk, and Tobias Hodel. Transformer-based htr for historical documents. arXiv:2203.11008 [cs.CV], 2022. URL https://arxiv.org/abs/2203.11008.
- [21] Uwe Springmann and Anke Lüdeling. Ocr of historical printings with an application to building diachronic corpora: A case study using the ridges herbal corpus. Digital Humanities Quarterly, 11(2), 2017.
- [22] Philipp Benjamin Ströbel, Tobias Hodel, Walter Boente, and Martin Volk. The adaptability of a transformer-based ocr model for historical documents. In Document Analysis and Recognition – ICDAR 2023 Workshops, pages 34–48. Springer, 2023. doi: 10.1007/978-3-031-41498-5_3.
- [23] Shaobin Xu and David Smith. Retrieving and combining repeated passages to improve ocr. In 2017 ACM/IEEE Joint Conference on Digital Libraries (JCDL), pages 1–4, 2017.
- [24] Huaigu Cao, Stephen Rawls, and Prem Natarajan. 1990 us census form recognition using ctc network, wfst language model, and surname correction. In 2017 14th IAPR International Conference on Document Analysis and Recognition (ICDAR), volume 01, pages 977–982, 2017.
- [25] Thi Tuyet Hai Nguyen, Adam Jatowt, Mickael Coustaty, and Antoine Doucet. Survey of Post-OCR Processing Approaches. ACM Comput. Surv., 54(6):124:1–124:37, July 2021. ISSN 0360-0300. doi: 10.1145/3453476.
- [26] Quan Duong, Mika Hämäläinen, and Simon Hengchen. An unsupervised method for ocr post-correction and spelling normalisation for finnish. In Simon Dobnik and Lilja Øvrelid, editors, Proceedings of the 23rd Nordic Conference on Computational Linguistics (NoDaLiDa), pages 240–248, Reykjavik, Iceland (Online), 2021. Linköping University Electronic Press, Sweden.
- [27] Yung-Hsin Chen and Yuli Zhou. Enhancing OCR performance through post-OCR models: Adopting glyph embedding for improved correction. arXiv preprint arXiv:2308.15262, 2023. URL https://arxiv.org/abs/ 2308.15262.
- [28] Oksana Dereza, Deirdre Ní Chonghaile, and Nicholas Wolf. “To Have the ‘Million’ Readers Yet”: Building a Digitally Enhanced Edition of the Bilingual Irish-English Newspaper an Gaodhal (1881-1898). In Rachele Sprugnoli and Marco Passarotti, editors, Proceedings of the Third Workshop on Language Technologies for Historical and Ancient Languages (LT4HALA) @ LREC-COLING-2024, pages 65–78, Torino, Italia, 2024. ELRA and ICCL.
- [29] Mahdi Hajiali. OCR Post-processing Using Large Language Models. Phd thesis, University of Nevada, Las Vegas, August 2023. URL https://digitalscholarship.unlv.edu/thesesdissertations/4811.
- [30] Nianheng Wu. Multimodal ocr post-correction on german historical documents. Master’s thesis, University of Stuttgart, 2023.
- [31] Oksana Dereza, Deirdre Ní Chonghaile, and Nicholas Wolf. “To Have the ‘Million’ Readers Yet”: Building a Digitally Enhanced Edition of the Bilingual Irish-English Newspaper an Gaodhal (1881-1898). In Rachele


- Sprugnoli and Marco Passarotti, editors, Proceedings of the Third Workshop on Language Technologies for Historical and Ancient Languages (LT4HALA) @ LREC-COLING-2024, pages 65–78, Torino, Italia, 2024. ELRA and ICCL.
- [32] Andre Wolters and Andreas Van Cranenburgh. Historical dutch spelling normalization with pretrained language models. Computational Linguistics in the Netherlands Journal, 13:147–171, March 21 2024.
- [33] Thi Tuyet Hai Nguyen, Adam Jatowt, Nhu-Van Nguyen, Mickaël Coustaty, and Antoine Doucet. Neural Machine Translation with BERT for Post-OCR Error Detection and Correction. In JCDL ’20: The ACM/IEEE Joint Conference on Digital Libraries in 2020, pages 333–336, Virtual Event, China, August 2020. ACM. doi: 10.1145/3383583.3398605.
- [34] Viktoria Löfgren and Dana Dannélls. Post-OCR correction of digitized Swedish newspapers with ByT5. In Yuri Bizzoni, Stefania Degaetano-Ortlieb, Anna Kazantseva, and Stan Szpakowicz, editors, Proceedings of the 8th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature (LaTeCH-CLfL 2024), pages 237–242, St. Julians, Malta, March 2024. Association for Computational Linguistics.
- [35] Jonathan Bourne. CLOCR-C: Context Leveraging OCR Correction with Pre-trained Language Models. arXiv, 2408.17428, 2025. Preprint.
- [36] Yung-Hsin Chen and Phillip B. Ströbel. Trocr meets language models: An end-to-end post-correction approach. In Harold Mouchère and Anna Zhu, editors, Document Analysis and Recognition – ICDAR 2024 Workshops, volume 14935 of Lecture Notes in Computer Science, pages 12–26. Springer Nature Switzerland, Cham, 2024.
- [37] Maud Ehrmann et al. Named entity recognition and classification on historical documents: A survey. ACM Computing Surveys, 56(2):1–47, February 2024.
- [38] Solenn Tual, Nathalie Abadie, Joseph Chazalon, Bertrand Duménieu, and Edwin Carlinet. A benchmark of nested named entity recognition approaches in historical structured documents. In Gernot A. Fink, Rajiv Jain, Koichi Kise, and Richard Zanibbi, editors, Document Analysis and Recognition - ICDAR 2023, pages 115–131, Cham,

2023. Springer Nature Switzerland. ISBN 978-3-031-41682-8. doi: 10.1007/978-3-031-41682-8_8.

- [39] Rémi Petitpierre, Marion Kramer, and Lucas Rappo. An end-to-end pipeline for historical censuses processing. IJDAR, 26(4):419–432, December 2023. ISSN 1433-2825. doi: 10.1007/s10032-023-00428-9.
- [40] Rutger van Koert, Stefan Klut, Tim Koornstra, Martijn Maas, and Luke Peters. Loghi: An End-to-End Framework for Making Historical Documents Machine-Readable. In Document Analysis and Recognition – ICDAR 2024 Workshops: Athens, Greece, August 30–31, 2024, Proceedings, Part I, pages 73–88, Berlin, Heidelberg, September

2024. Springer-Verlag. ISBN 978-3-031-70644-8. doi: 10.1007/978-3-031-70645-5_6. URL https://doi. org/10.1007/978-3-031-70645-5_6.

- [41] Ahmed Cheikh Rouhou, Marwa Dhiaf, Yousri Kessentini, and Sinda Ben Salem. Transformer-based approach for joint handwriting and named entity recognition in historical documents. Pattern Recognition Letters, 155:14–21,

2022. doi: 10.1016/j.patrec.2021.11.010.

- [42] Thomas Constum, Pierrick Tranouez, and Thierry Paquet. DANIEL: A fast document attention network for information extraction and labelling of handwritten documents. International Journal on Document Analysis and Recognition (IJDAR), 28(1):1–15, jan 2025. doi: 10.1007/s10032-024-00511-9.
- [43] Denis Coquenet, Clément Chatelain, and Thierry Paquet. Dan: a segmentation-free document attention network for handwritten document recognition. IEEE transactions on pattern analysis and machine intelligence, 45(7): 8227–8243, 2023.
- [44] Mohammed Hamdan, Abderrahmane Rahiche, and Mohamed Cheriet. HAND: Hierarchical attention network for multi-scale handwritten document recognition and layout analysis. arXiv preprint arXiv:2412.18981, 2024.
- [45] Dayvid Castro, Byron Leite Dantas Bezerra, and Cleber Zanchettin. An end-to-end approach for handwriting recognition: From handwritten text lines to complete pages. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) Workshops, pages 264–273, June 2024.
- [46] Philip Kahle, Sebastian Colutto, Günter Hackl, and Günter Mühlberger. Transkribus-a service platform for transcription, recognition and retrieval of historical documents. In 2017 14th Iapr International Conference on Document Analysis and Recognition (Icdar), volume 4, pages 19–24. IEEE, 2017.
- [47] Clemens Neudecker, Konstantin Baierer, Maria Federbusch, Matthias Boenig, Kay-Michael Würzner, Volker Hartmann, and Elisa Herrmann. Ocr-d: An end-to-end open source ocr framework for historical printed documents. In Proceedings of the 3rd international conference on digital access to textual cultural heritage, pages 53–58, 2019.


- [48] Lucian Li. Handwriting recognition in historical documents with multimodal llm. arXiv:2410.24034 [cs.CV], October 2024. URL https://arxiv.org/abs/2410.24034.
- [49] Seorin Kim, Julien Baudru, Wouter Ryckbosch, Hugues Bersini, and Vincent Ginis. Early evidence of how llms outperform traditional systems on ocr/htr tasks for historical records. arXiv:2501.11623 [cs.CV], January 2025. URL https://arxiv.org/abs/2501.11623.
- [50] Mark Humphries, Lianne C. Leddy, Quinn Downton, Meredith Legace, John McConnell, Isabella Murray, and Elizabeth Spence. Unlocking the archives: Using large language models to transcribe handwritten historical documents. arXiv:2411.03340 [cs.CL], November 2024. URL https://arxiv.org/abs/2411.03340.
- [51] Alex Ghiriti, Wolfgang Göderle, and Roman Kern. Exploring the Capabilities of GPT4-Vision as OCR Engine. In Apostolos Antonacopoulos, Annika Hinze, Benjamin Piwowarski, Mickaël Coustaty, Giorgio Maria Di Nunzio, Francesco Gelati, and Nicholas Vanderschantz, editors, Linking Theory and Practice of Digital Libraries, pages 3–12, Cham, 2024. Springer Nature Switzerland. ISBN 978-3-031-72440-4. doi: 10.1007/978-3-031-72440-4_1.
- [52] Emanuela Boros et al. Post-correction of historical text transcripts with large language models: An exploratory study. In Proceedings of the 8th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature (LaTeCH-CLfL 2024), The 8th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature, page 141. Association for Computational Linguistics, 2024.
- [53] Alan Thomas, Robert Gaizauskas, and Haiping Lu. Leveraging llms for post-ocr correction of historical newspapers. In Rachele Sprugnoli and Marco Passarotti, editors, Proceedings of the Third Workshop on Language Technologies for Historical and Ancient Languages (LT4HALA) @ LREC-COLING-2024, pages 116–121, Torino, Italia, 2024. ELRA and ICCL.
- [54] Jenna Kanerva, Cassandra Ledins, Siiri Käpyaho, and Filip Ginter. Ocr error post-correction with llms in historical documents: No free lunches. arXiv:2502.01205 [cs.CL], February 2025. URL https://arxiv.org/abs/2502. 01205.
- [55] Carlos-Emiliano González-Gallardo, Emanuela Boros, Nancy Girdhar, Ahmed Hamdi, Jose G. Moreno, and Antoine Doucet. Yes but.. Can ChatGPT Identify Entities in Historical Documents? In 2023 ACM/IEEE Joint Conference on Digital Libraries (JCDL), pages 184–189, June 2023. doi: 10.1109/JCDL57899.2023.00034.
- [56] Carlos-Emiliano González-Gallardo, Hanh Thi Hong Tran, Ahmed Hamdi, and Antoine Doucet. Leveraging Open Large Language Models for Historical Named Entity Recognition. In Linking Theory and Practice of Digital Libraries: 28th International Conference on Theory and Practice of Digital Libraries, TPDL 2024, Ljubljana, Slovenia, September 24–27, 2024, Proceedings, Part I, pages 379–395, Berlin, Heidelberg, September 2024. Springer-Verlag. ISBN 978-3-031-72436-7. doi: 10.1007/978-3-031-72437-4_22.
- [57] Torsten Hiltmann, Martin Dröge, Nicole Dresselhaus, Till Grallert, Melanie Althage, Paul Bayer, Sophie Eckenstaler, Koray Mendi, Jascha Marijn Schmitz, Philipp Schneider, Wiebke Sczeponik, and Anica Skibba. NER4all or Context is All You Need: Using LLMs for low-effort, high-performance NER on historical texts. A humanities informed approach, February 2025.
- [58] Yunting Xie, Matti La Mela, and Fredrik Tell. Multimodal LLM-assisted Information Extraction from Historical Documents: The Case of Swedish Patent Cards (1945-1975) and ChatGPT. Digital Humanities in the Nordic and Baltic Countries Publications, 7(2), March 2025. ISSN 2704-1441. doi: 10.5617/dhnbpub.12294.
- [59] Ivan Gruber, Miroslav Hlaváˇc, Petr Neduchal, and Marek Hrúz. Multi-label Classification and Named Entity Recognition for Historical Documents. In Hossein Moosaei, Ilias Kotsireas, and Panos M. Pardalos, editors, Dynamics of Information Systems, pages 24–34, Cham, 2025. Springer Nature Switzerland. ISBN 978-3-03181010-7. doi: 10.1007/978-3-031-81010-7_2.
- [60] Jeya Balaji Balasubramanian, Daniel Adams, Ioannis Roxanis, Amy Berrington de Gonzalez, Penny Coulson, Jonas S. Almeida, and Montserrat García-Closas. Leveraging large language models for structured information extraction from pathology reports. arXiv:2502.12183 [cs.CL], February 2025.
- [61] Imed Keraghel, Stanislas Morbieu, and Mohamed Nadif. Recent advances in named entity recognition: A comprehensive survey and comparative study. arXiv:2401.10825 [cs.CL], December 2024.
- [62] Janne van der Loop, Florian Kordon, Martin Mayr, Vincent Christlein, Fei Wu, Dalia Rodríguez-Salas, Nikolaus Weichselbaumer, and Mathias Seuret. ICDAR 2024 Competition on Multi Font Group Recognition and OCR. In Elisa H. Barney Smith, Marcus Liwicki, and Liangrui Peng, editors, Document Analysis and Recognition

- ICDAR 2024, pages 381–396, Cham, 2024. Springer Nature Switzerland. ISBN 978-3-031-70552-6. doi: 10.1007/978-3-031-70552-6_23.

- [63] OpenAI. Gpt-4o system card, 2024. URL https://arxiv.org/abs/2410.21276.


- [64] Demis Hassabis and Koray Kavukcuoglu. Introducing Gemini 2.0: Our new AI model for the agentic era. https: //blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/, December 2024. Accessed: 2025-03-14.
- [65] Gemini Team. Gemini: A family of highly capable multimodal models, 2024. URL https://arxiv.org/abs/ 2312.11805.
- [66] Ray Smith. An overview of the tesseract ocr engine. In Proceedings of the Ninth International Conference on Document Analysis and Recognition (ICDAR), volume 2, pages 629–633. IEEE, 2007. doi: 10.1109/ICDAR.2007. 4376991.
- [67] Thomas Schmidt, Jan Kamlah, and Stefan Weil. Reichsanzeiger-gt: An ocr ground truth dataset based on the historical newspaper “deutscher reichsanzeiger und preußischer staatsanzeiger” (german imperial gazette and prussian official gazette) (1819–1945). Data in Brief, 54:110274, 2024. ISSN 2352-3409. doi: https: //doi.org/10.1016/j.dib.2024.110274.
- [68] Philip Kahle, Sebastian Colutto, Günter Hackl, and Günter Mühlberger. Transkribus - a service platform for transcription, recognition and retrieval of historical documents. In 2017 14th IAPR International Conference on Document Analysis and Recognition (ICDAR), pages 19–24, 2017. doi: 10.1109/ICDAR.2017.307. URL https://ieeexplore.ieee.org/document/8270161.
- [69] Joe Nockels, Paul Gooding, Sarah Ames, and Melissa Terras. Understanding the application of handwritten text recognition technology in heritage contexts: a systematic review of transkribus in published research. Archival Science, 22(3):367–392, 2022. doi: 10.1007/s10502-022-09397-0.
- [70] Transkribus Team. Transkribus Print Multi-Language Model. https://readcoop.eu/model/ transkribus-print-multi-language-dutch-german-english-finnish-french-swedish-etc/. Accessed: 2025-03-18.
- [71] Transkribus Team. Super models, 2025. URL https://help.transkribus.org/super-models. Accessed: 2025-03-18.
- [72] Gundram Leifert, C.A. Romein, Achim Rabus, Phillip Benjamin Ströbel, and Tobias Hodel. Transkribus and beyond: Pioneering the future of transcription technology. In Transkribus User Conference 2024, February 2024.
- [73] Emanuela Boros, Nhu Khoa Nguyen, Gaël Lejeune, and Antoine Doucet. Assessing the impact of OCR noise on multilingual event detection over digitised documents. Int J Digit Libr, 23(3):241–266, September 2022. ISSN 1432-1300. doi: 10.1007/s00799-022-00325-2.
- [74] Ahmed Hamdi, Elvys Linhares Pontes, Nicolas Sidere, Mickaël Coustaty, and Antoine Doucet. In-depth analysis of the impact of OCR errors on named entity recognition and linking. Natural Language Engineering, 29(2): 425–448, March 2023. ISSN 1351-3249, 1469-8110. doi: 10.1017/S1351324922000110.
- [75] Vinh-Nam Huynh, Ahmed Hamdi, and Antoine Doucet. When to use ocr post-correction for named entity recognition? In Emi Ishita, Natalie Lee San Pang, and Lihong Zhou, editors, Digital Libraries at Times of Massive Societal Transition, pages 33–42. Springer International Publishing, Cham, 2020.
- [76] Yao Lu, Max Bartolo, Alastair Moore, Sebastian Riedel, and Pontus Stenetorp. Fantastically ordered prompts and where to find them: Overcoming few-shot prompt order sensitivity. arXiv preprint arXiv:2104.08786, 2022. URL https://arxiv.org/abs/2104.08786.
- [77] J.D. Zamfirescu-Pereira, Richmond Y. Wong, Bjoern Hartmann, and Qian Yang. Why johnny can’t prompt: How non-ai experts try (and fail) to design llm prompts. In Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems, CHI ’23, pages 1–21, New York, NY, USA, April 2023. Association for Computing Machinery. ISBN 978-1-4503-9421-5. doi: 10.1145/3544548.3581388.
- [78] Qi Cheng, Liqiong Chen, Zhixing Hu, Juan Tang, Qiang Xu, and Binbin Ning. A novel prompting method for few-shot NER via LLMs. Natural Language Processing Journal, 8:100099, September 2024. ISSN 2949-7191. doi: 10.1016/j.nlp.2024.100099.
- [79] Vladimir I. Levenshtein. Binary codes capable of correcting deletions, insertions, and reversals. Soviet Physics Doklady, 10(8):707–710, 1966.
- [80] Clemens Neudecker, Konstantin Baierer, Mike Gerber, Christian Clausner, Apostolos Antonacopoulos, and Stefan Pletschacher. A survey of OCR evaluation tools and metrics. In Proceedings of the 6th International Workshop on Historical Document Imaging and Processing, HIP ’21, pages 13–18, New York, NY, USA, October 2021. Association for Computing Machinery. ISBN 978-1-4503-8690-6. doi: 10.1145/3476887.3476888.
- [81] Yung-Hsin Chen and Yuli Zhou. Enhancing OCR Performance through Post-OCR Models: Adopting Glyph Embedding for Improved Correction, August 2023.


- [82] Sara Lafia, David A. Bleckley, and J. Trent Alexander. Digitizing and parsing semi-structured historical administrative documents from the g.i. bill mortgage guarantee program. Journal of Documentation, 79(7):1619–1638,

2023. doi: 10.1108/JD-03-2023-0055.

- [83] Christian Clausner, S. Pletschacher, and A. Antonacopoulos. Flexible character accuracy measure for readingorder-independent evaluation. Pattern Recognition Letters, 131, February 2020. ISSN 0167-8655. doi: 10.1016/j. patrec.2020.02.003.
- [84] William E. Winkler. String comparator metrics and enhanced decision rules in the fellegi-sunter model of record linkage. In Proceedings of the Section on Survey Research Methods, American Statistical Association, pages 354–359, 1990.
- [85] John Evershed and Kent Fitch. Correcting Noisy OCR: Context beats Confusion. In Proceedings of the First International Conference on Digital Access to Textual Cultural Heritage, pages 45–51, Madrid, 2014.
- [86] Sofia Ares Oliveira and Frederic Kaplan. Comparing human and machine performances in transcribing 18th century handwritten Venetian script. In ADHO / EHD 2018 - Mexico City, 2018.
- [87] Nathalie Abadie, Edwin Carlinet, Joseph Chazalon, and Bertrand Duménieu. A benchmark of named entity recognition approaches in historical documents: Application to 19th century french directories. In Seiichi Uchida, Elisa Barney, and Véronique Eglin, editors, Document Analysis Systems, pages 445–460, Cham, 2022. Springer International Publishing. ISBN 978-3-031-06555-2. doi: 10.1007/978-3-031-06555-2_30.
- [88] Ladislav Lenc, Jiˇrí Martínek, Pavel Král, Anguelos Nicolao, and Vincent Christlein. HDPA: Historical document processing and analysis framework. Evolving Systems, 12(1):177–190, March 2021. ISSN 1868-6478, 1868-6486. doi: 10.1007/s12530-020-09343-4.
- [89] Christian Reul, Christoph Wick, Maximilian Noeth, Andreas Buettner, Maximilian Wehner, and Uwe Springmann. Mixed Model OCR Training on Historical Latin Script for Out-of-the-Box Recognition and Finetuning. In Proceedings of the 6th International Workshop on Historical Document Imaging and Processing, HIP ’21, pages 7–12, New York, NY, USA, 2021. Association for Computing Machinery. ISBN 978-1-4503-8690-6. doi: 10.1145/3476887.3476910.
- [90] Daniel Van Strien, Kasper Beelen, Mariona Coll Ardanuy, K. Hosseini, Barbara McGillivray, and Giovanni Colavizza. Assessing the impact of ocr quality on downstream nlp tasks. SCITEPRESS - Science and Technology Publications, 2020. doi: 10.17863/CAM.52068.
- [91] Ahmed Hamdi, Axel Jean-Caurant, Nicolas Sidère, Mickaël Coustaty, and Antoine Doucet. Assessing and minimizing the impact of OCR quality on named entity recognition. In Digital Libraries for Open Knowledge: 24th International Conference on Theory and Practice of Digital Libraries (TPDL 2020), volume 12246 of Lecture Notes in Computer Science, pages 87–101. Springer, 2020. doi: 10.1007/978-3-030-54956-5\_7.
- [92] Ling Fu, Biao Yang, Zhebin Kuang, Jiajun Song, Yuzhe Li, Linghao Zhu, Qidi Luo, Xinyu Wang, Hao Lu, Mingxin Huang, Zhang Li, Guozhi Tang, Bin Shan, Chunhui Lin, Qi Liu, Binghong Wu, Hao Feng, Hao Liu, Can Huang, Jingqun Tang, Wei Chen, Lianwen Jin, Yuliang Liu, and Xiang Bai. Ocrbench v2: An improved benchmark for evaluating large multimodal models on visual text localization and reasoning. arXiv:2501.00321 [cs.CV], 2024. URL https://arxiv.org/abs/2501.00321.
- [93] Thomas Hegghammer. Ocr with tesseract, amazon textract, and google document ai: a benchmarking experiment. Journal of Computational Social Science, 5(2):861–882, 2022. doi: 10.1007/s42001-021-00149-1.
- [94] Muhammad Abdullah Sohail, Salaar Masood, and Hamza Iqbal. Deciphering the underserved: Benchmarking llm ocr for low-resource scripts. arXiv preprint arXiv:2412.16119, 2024.


### Primary Sources

- [95] Leipziger Adreß-, Post- und Reise-Calender. Leipzig, 1753. Digitized by SLUB Dresden. URN: urn:nbn:de:bsz:14-db-id372456510-175300003.
- [96] Dresden zur zweckmäßigen Kenntniß seiner Häuser und deren Bewohner. Dresden, 1797. Digitized by SLUB Dresden. URN: urn:nbn:de:bsz:14-db-id20071279Z7.


- [96] Leipziger Adreß- Post- und Reise- Calender auf das Jahr Christi 1800. Leipzig, 1800. Digitized by SLUB Dresden. URN: urn:nbn:de:bsz:14-db-id372456510-180000003.
- [97] Dresdner Adress-Kalender. Dresden, 1819. Digitized by SLUB Dresden. URN: urn:nbn:de:bsz:14-dbid20338589Z.
- [98] Lübeckisches Adress-Buch nebst Local-Notizen. Georg Schmidt, Lübeck, 1870. Digitized by Stadtbibliothek Lübeck. URN: urn:nbn:de:gbv:48-1-370446.
- [99] F Cazin. Verzeichnis aller im Regierungs-Bezirk Aachen wohnenden Kaufleute, Beamten und Geistlichen. Verlag der Cremerschen Buchhandlung, Aachen, 1838. Digitized by Universitäts- und Landesbibliothek Bonn, 2017. URN: urn:nbn:de:hbz:5:1-183801.
- [100] Georg Friedrich Krug. Staats- und Adreß-Handbuch der Freien Stadt Frankfurt. Theil 2: Adress-Handbuch von Frankfurt am Main. Georg Friedrich Krug’s Verlags-Buchhandlung, Frankfurt am Main, 1860. Digitized by Münchener Digitalisierungszentrum (2008-2013). URN: urn:nbn:de:hebis:30:2-288400.
- [101] Samuel J. Schröckh. Allgemeine kaufmännische Bibliothek. in der Schröck’schen Buchhandlung, Frankfurt und Leipzig, 1778. Accessed via Google Books. URL: https://www.google.co.uk/books/edition/ Allgemeine_kaufm%C3%A4nnische_Bibliothek/7HtDIgZMC7EC?hl=en&gbpv=0.
- [102] A. Schönberger. Adreßbuch der Civil-Bevölkerung der Stadt Trier. Verlag von A. Schönberger, Trier, 1853. Digitized by Universitätsbibliothek Trier. URN: urn:nbn:de:0128-2-337.
- [103] J. C. Schünmann. Rigasches Adreß-Buch. Mitau, 1810. Accessed via the Internet Archive. URL: https: //archive.org/details/1810RigaschesAdressbuch.


### Appendix

Figure A.1: Prompt for Named Entity Recognition from Plain Text without any Image Input

YOU ARE AN EXPERT HISTORIAN. YOUR TASK IS TO EXTRACT DATA FROM TRANSCRIBED TEXT OF A GERMAN BUSINESS DIRECTORY. FAILURE TO FOLLOW THESE RULES EXACTLY WILL RESULT IN TOTAL SYSTEM FAILURE. THERE IS ZERO ROOM FOR ERROR.

STRICT JSON FORMAT - NO EXCEPTIONS:

- - OUTPUT MUST BE VALID JSON.
- - NO MARKDOWN, NO EXPLANATIONS, NO HEADERS. FIELDS (STRICTLY NOTHING ELSE):
- - "first and middle names" (string)
- - "surname" (string; can also be a company name)
- - "occupation" (string)
- - "address" (string; full address if possible, otherwise partial) NON-NEGOTIABLE RULES:


- 1. **EXTRACT EXACTLY AS WRITTEN. NO MODERNIZATION. NO INTERPRETATION. NO CHANGES.**
- 2. **NEVER WRITE ANYTHING INTO THE DATASET THAT IS NOT IN THE HISTORICAL TEXT FILE.**
- 3. **IF A FIELD IS MISSING, SET IT TO NULL. DO NOT GUESS. DO NOT INFER. DO NOT ATTEMPT TO RECONSTRUCT.**
- 4. **DO NOT ADD EXTRA INFORMATION. DO NOT ADD COMMENTS. DO NOT ADD ANYTHING OUTSIDE THE REQUIRED FIELDS.**
- 5. **DO NOT CONCATENATE OR MERGE ADDRESS FRAGMENTS FROM MULTIPLE ENTRIES. EACH ENTRY MUST REMAIN INTACT AS SEEN IN THE TEXT.**
- 6. **IF MULTIPLE ADDRESSES EXIST FOR ONE ENTRY, KEEP THEM EXACTLY AS WRITTEN. DO NOT REFORMAT.**


STRICTLY ENFORCED EXAMPLE OUTPUT: [

{

"first and middle names": "Wilhelm Friedrich", "surname": "Becker", "occupation": "Schulmeister", "address": "Hinter der Kirche, in der Schulstube"

}, {

"first and middle names": "Johann Georg", "surname": "Weber", "occupation": "Apotheker", "address": "An der Marktstraße, in der Löwenapotheke"

}

] FINAL COMMANDS - NO EXCEPTIONS:

- - **IF TEXT IS PARTIALLY VISIBLE OR DISTORTED, IT DOES NOT EXIST. IGNORE IT.**
- - **OUTPUT MUST BE PURE, PERFECTLY FORMATTED JSON. NOTHING ELSE.**
- - **FAILURE TO FOLLOW THESE RULES PRECISELY MEANS THE TASK IS COMPROMISED. THERE IS ZERO ROOM FOR ERROR.**


Figure A.2: Prompt for OCR using mLLMs

**ABSOLUTELY NON-NEGOTIABLE TRANSCRIPTION RULES - FAILURE IS NOT AN OPTION** YOU ARE A MACHINE. YOU FOLLOW THESE RULES WITH PERFECT PRECISION. **ANY DEVIATION, ANY ERROR,

ANY SLIGHTEST SLIP-UP = TOTAL SYSTEM FAILURE.** FAILURE IS NOT PERMITTED. FAILURE IS

THE END. **THERE IS NO ROOM FOR ERROR.** ## **DO NOT DEVIATE. DO NOT INTERPRET. JUST EXECUTE. FAILURE IS UNTHINKABLE.** ### **NON-NEGOTIABLE ABSOLUTES - IF YOU BREAK THESE RULES, THE TASK IS VOID, EVERYTHING

FAILS, AND YOU HAVE COMPROMISED THE MISSION.**

- 1. **YOU WILL ONLY TRANSCRIBE THE MAIN PHYSICAL BOOK PAGE. NOTHING ELSE EXISTS.** NOT ONE LETTER FROM ANOTHER PAGE MAY BE TRANSCRIBED. **IF YOU BREAK THIS RULE, THE TASK IS DESTROYED.**
- 2. **IF TEXT APPEARS AT THE FAR-LEFT OR FAR-RIGHT EDGES, IT DOES NOT EXIST. YOU MUST DELETE IT FROM REALITY.** ANY EDGE TEXT BELONGING TO ADJACENT PAGES **MUST BE OBLITERATED FROM YOUR OUTPUT.**
- 3. **CROPPED OR CUT-OFF WORDS ARE FORBIDDEN.** IF A WORD IS NOT COMPLETELY PRESENT, YOU MUST

**ERASE IT FROM HISTORY.** **HALF-VISIBLE WORDS ARE A VIOLATION OF THE RULES.**

- 4. **IF YOU CANNOT 100% VERIFY THAT A WORD BELONGS TO THE MAIN PAGE, YOU MUST DESTROY IT FROM YOUR OUTPUT.**
- 5. **PARTIAL WORDS, BLURRED TEXT, OR INCOMPLETE CHARACTERS DO NOT EXIST. THEY MUST NEVER BE TRANSCRIBED.**
- 6. **DO NOT GUESS. DO NOT RECONSTRUCT. DO NOT ASSUME.** **YOU ARE NOT A HISTORIAN. YOU ARE A TRANSCRIPTION MACHINE. YOU COPY WHAT EXISTS. NOTHING MORE. NOTHING LESS.**
- 7. **THERE ARE NO EXCEPTIONS. NO OVERRIDES. NO ATTEMPTS TO "HELP" OR "IMPROVE" THE TEXT. IF YOU BREAK THIS RULE, EVERYTHING COLLAPSES.**


## **WHAT YOU MUST TRANSCRIBE (AND NOTHING ELSE):**

- - **HEADERS, SUBHEADINGS, PAGE NUMBERS** FROM THE MAIN PAGE ONLY.
- - **NAMES, ADDRESSES, OCCUPATIONS, BUSINESS DESCRIPTIONS** THAT ARE UNQUESTIONABLY PART OF THE MAIN PAGE.**
- - **EXACT SPELLING, ARCHAIC TERMS, ABBREVIATIONS** **EXACTLY AS WRITTEN. NOTHING MODERNIZED. NOTHING ALTERED.**


## **WHAT YOU MUST NEVER, UNDER ANY CIRCUMSTANCES, TRANSCRIBE:**

- - **ANY TEXT FROM AN ADJACENT PAGE.** **EVEN ONE LETTER FROM ANOTHER PAGE IS A TOTAL FAILURE

.**

- - **CROPPED, CUT-OFF, OR PARTIAL WORDS.** **IF YOU CANNOT SEE THE WHOLE WORD, IT MUST BE ERASED FROM YOUR MIND.**
- - **ANY TEXT FROM A MARGINAL OR PARTIAL PAGE ARTIFACT. NOTHING FROM THE LEFT OR RIGHT EDGE OF THE IMAGE CAN BE ALLOWED IN YOUR OUTPUT.**


## **FINAL COMMANDS - BREAKING THESE RULES IS CATASTROPHIC:**

- - **IF A WORD IS NOT FULLY PRESENT, IT IS NOT INCLUDED. THIS IS ABSOLUTE.**
- - **IF A WORD APPEARS TO BE FROM ANOTHER PAGE, IT IS OBLITERATED. ERASE IT FROM YOUR OUTPUT

.**

- - **YOUR OUTPUT IS PURE, UNTAINTED TEXT FROM THE MAIN PAGE. NOTHING ELSE. NO INTRODUCTIONS. NO COMMENTS. NO EXTRAS.**


**THIS IS A ZERO-TOLERANCE ENVIRONMENT.** ABSOLUTE COMPLIANCE IS REQUIRED. THERE IS NO FLEXIBILITY, NO EXCEPTIONS, AND NO ROOM FOR ERROR.

**IF YOU BREAK ANY RULE, THE ENTIRE TASK IS DESTROYED. HUMANITY DEPENDS ON YOUR PRECISION.*

Figure A.3: Prompt for mLLM OCR Post-Correction

**ABSOLUTELY NON-NEGOTIABLE TRANSCRIPTION RULES - FAILURE IS NOT AN OPTION** YOU ARE A MACHINE. YOU FOLLOW THESE RULES WITH PERFECT PRECISION. **ANY DEVIATION, ANY ERROR,

ANY SLIGHTEST SLIP-UP = TOTAL SYSTEM FAILURE.** FAILURE IS NOT PERMITTED. FAILURE IS

THE END. **THERE IS NO ROOM FOR ERROR.** ## **DO NOT DEVIATE. DO NOT INTERPRET. JUST EXECUTE. FAILURE IS UNTHINKABLE.** ### **NON-NEGOTIABLE ABSOLUTES - IF YOU BREAK THESE RULES, THE TASK IS VOID, EVERYTHING

FAILS, AND YOU HAVE COMPROMISED THE MISSION.**

- 1. **YOU WILL ONLY TRANSCRIBE THE MAIN PHYSICAL BOOK PAGE. NOTHING ELSE EXISTS.** NOT ONE LETTER FROM ANOTHER PAGE MAY BE TRANSCRIBED. **IF YOU BREAK THIS RULE, THE TASK IS DESTROYED.**
- 2. **IF TEXT APPEARS AT THE FAR-LEFT OR FAR-RIGHT EDGES, IT DOES NOT EXIST. YOU MUST DELETE IT FROM REALITY.** ANY EDGE TEXT BELONGING TO ADJACENT PAGES **MUST BE OBLITERATED FROM YOUR OUTPUT.**
- 3. **CROPPED OR CUT-OFF WORDS ARE FORBIDDEN.** IF A WORD IS NOT COMPLETELY PRESENT, YOU MUST


**ERASE IT FROM HISTORY.** **HALF-VISIBLE WORDS ARE A VIOLATION OF THE RULES.**

- 4. **IF YOU CANNOT 100% VERIFY THAT A WORD BELONGS TO THE MAIN PAGE, YOU MUST DESTROY IT FROM YOUR OUTPUT.**
- 5. **PARTIAL WORDS, BLURRED TEXT, OR INCOMPLETE CHARACTERS DO NOT EXIST. THEY MUST NEVER BE TRANSCRIBED.**
- 6. **DO NOT GUESS. DO NOT RECONSTRUCT. DO NOT ASSUME.** **YOU ARE NOT A HISTORIAN. YOU ARE A TRANSCRIPTION MACHINE. YOU COPY WHAT EXISTS. NOTHING MORE. NOTHING LESS.**
- 7. **THERE ARE NO EXCEPTIONS. NO OVERRIDES. NO ATTEMPTS TO "HELP" OR "IMPROVE" THE TEXT. IF YOU BREAK THIS RULE, EVERYTHING COLLAPSES.**


## **WHAT YOU MUST TRANSCRIBE (AND NOTHING ELSE):**

- **HEADERS, SUBHEADINGS, PAGE NUMBERS** FROM THE MAIN PAGE ONLY.

- - **NAMES, ADDRESSES, OCCUPATIONS, BUSINESS DESCRIPTIONS** THAT ARE UNQUESTIONABLY PART OF THE MAIN PAGE.**
- - **EXACT SPELLING, ARCHAIC TERMS, ABBREVIATIONS** **EXACTLY AS WRITTEN. NOTHING MODERNIZED. NOTHING ALTERED.**


## **WHAT YOU MUST NEVER, UNDER ANY CIRCUMSTANCES, TRANSCRIBE:**

- **ANY TEXT FROM AN ADJACENT PAGE.** **EVEN ONE LETTER FROM ANOTHER PAGE IS A TOTAL FAILURE

.**

- - **CROPPED, CUT-OFF, OR PARTIAL WORDS.** **IF YOU CANNOT SEE THE WHOLE WORD, IT MUST BE ERASED FROM YOUR MIND.**
- - **ANY TEXT FROM A MARGINAL OR PARTIAL PAGE ARTIFACT. NOTHING FROM THE LEFT OR RIGHT EDGE OF THE IMAGE CAN BE ALLOWED IN YOUR OUTPUT.**


## **FINAL COMMANDS - BREAKING THESE RULES IS CATASTROPHIC:**

- **IF A WORD IS NOT FULLY PRESENT, IT IS NOT INCLUDED. THIS IS ABSOLUTE.**

- **IF A WORD APPEARS TO BE FROM ANOTHER PAGE, IT IS OBLITERATED. ERASE IT FROM YOUR OUTPUT

.**

- **YOUR OUTPUT IS PURE, UNTAINTED TEXT FROM THE MAIN PAGE. NOTHING ELSE. NO INTRODUCTIONS. NO COMMENTS. NO EXTRAS.**

**THIS IS A ZERO-TOLERANCE ENVIRONMENT.** ABSOLUTE COMPLIANCE IS REQUIRED. THERE IS NO FLEXIBILITY, NO EXCEPTIONS, AND NO ROOM FOR ERROR.

**IF YOU BREAK ANY RULE, THE ENTIRE TASK IS DESTROYED. HUMANITY DEPENDS ON YOUR PRECISION.* Below is the OCR output from Transkribus so you know how to spell the archaic words. Please use this information to correct any errors and ensure the text is fully compliant with the strict transcription rules.

-- OCR Output (Transkribus) -[Transkribus Print M1 OCR text is inserted here]

Figure A.4: Prompt for LLM OCR Post-Correction without Image Input

Correct the errors in this ocr output. Only provide the corrected text and nothing else:

-- OCR Output you should correct-[Transkribus Print M1 OCR text is inserted here]

