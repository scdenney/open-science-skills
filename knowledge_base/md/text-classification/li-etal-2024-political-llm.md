# arXiv:2412.06864v1[cs.CL]9 Dec 2024

## Political-LLM: Large Language Models in Political Science

Lincan Li1 Jiaqi Li2 Catherine Chen3∗ Fred Gui3∗ Hongjia Yang4 Chenxiao Yu2 Zhengguang Wang4 Jianing Cai5 Junlong Aaron Zhou6 Bolin Shen1 Alex Qian2 Weixin Chen2 Zhongkai Xue7 Lichao Sun8 Lifang He8 Hanjie Chen9 Kaize Ding10 Zĳian Du11 Fangzhou Mu12 Jiaxin Pei13 Jieyu Zhao2 Swabha Swayamdipta2 Willie Neiswanger2 Hua Wei14 Xiyang Hu14 Shixiang Zhu15 Tianlong Chen16 Yingzhou Lu13 Yang Shi17 Lianhui Qin18 Tianfan Fu19 Zhengzhong Tu20 Yuzhe Yang21 Jaemin Yoo22 Jiaheng Zhang23 Ryan Rossi24 Liang Zhan25 Liang Zhao26 Emilio Ferrara2 Yan Liu2 Furong Huang27 Xiangliang Zhang28 Lawrence Rothenberg29 Shuiwang Ji20 Philip S. Yu30 Yue Zhao2∗ Yushun Dong1∗

1Florida State University 2University of Southern California 3Louisiana State University 4University of Virginia 5University of Pennsylvania 6New York University 7Oxford University 8Lehigh University 9Rice University 10Northwestern University 11NVIDIA 12University of Wisconsin-Madison 13Stanford University 14Arizona State University 15Carnegie Mellon University 16University of North Carolina at Chapel Hill 17Utah State University 18University of California San Diego 19Rensselaer Polytechnic Institute 20Texas A&M University 21University of California, Los Angeles 22Korea Advanced Institute of Science & Technology 23National University of Singapore 24Adobe Research 25University of Pittsburgh 26Emory University 27University of Maryland 28University of Notre Dame 29University of Rochester 30University of Illinons at Chicago

#### Abstract

In recent years, large language models (LLMs) have been widely adopted in political science tasks such as election prediction, sentiment analysis, policy impact assessment, and misinformation detection. Meanwhile, the need to systematically understand how LLMs can further revolutionize the field also becomes urgent. In this work, we—a multidisciplinary team of researchers spanning computer science and political science—present the first principled framework termed Political-LLM to advance the comprehensive understanding of integrating LLMs into computational political science. Specifically, we first introduce a fundamental taxonomy classifying the existing explorations into two perspectives: political science and computational methodologies. In particular, from the political science perspective, we highlight the role of LLMs in automating predictive and generative tasks, simulating behavior dynamics, and improving causal inference through tools like counterfactual generation; from a computational perspective, we introduce advancements in data preparation, fine-tuning, and evaluation methods for LLMs that are tailored to political contexts. We identify key challenges and future directions, emphasizing the development of domain-specific datasets, addressing issues of bias and fairness, incorporating human expertise, and redefining evaluation criteria to align with the unique requirements of computational political science. Political-LLM seeks to serveasaguidebookforresearcherstofosteraninformed, ethical, andimpactfuluseofArtificial Intelligence in political science. Our online resource is available at: http://political-llm.org/.

∗Corresponding authors: Yushun Dong (yd24f@fsu.edu) is with the Department of Computer Science, Florida State University; Yue Zhao (yzhao010@usc.edu) is with the Department of Computer Science, University of Southern California; Fred Gui (pgui@lsu.edu) is with the Department of Political Science, Louisiana State University; Catherine Chen (catherinechen@lsu.edu) is with the Manship School of Mass Communication and the Department of Political Science, Louisiana State University.

### Contents

- 1 Introduction 3
- 2 Preliminaries 5

- 2.1 Large Language Models (LLMs) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
- 2.2 Core Computational Political Science Concepts . . . . . . . . . . . . . . . . . . . . . . . . 7


- 3 Taxonomy on LLM for Political Science 8
- 4 Classical Political Science Functions and Modern Transformations 9

- 4.1 Automation of Predictive Tasks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
- 4.2 Automation of Generative Tasks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
- 4.3 Simulation of LLM Agents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
- 4.4 LLM Explainability and Causal Inference . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
- 4.5 Ethical Concerns in LLM Development and Deployment . . . . . . . . . . . . . . . . . . . 16
- 4.6 Societal Impacts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18


- 5 Technical Foundations for LLM Applications in Political Science 19

- 5.1 Benchmark Datasets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
- 5.2 Dataset Preparation Strategies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
- 5.3 Fine-Tuning LLMs for Political Science . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
- 5.4 Inference with LLMs: Zero-Shot In-Context Learning . . . . . . . . . . . . . . . . . . . . . 24
- 5.5 Inference with LLMs: Few-Shot In-Context Learning . . . . . . . . . . . . . . . . . . . . . 26
- 5.6 Other Techniques Enhancing LLM Inference . . . . . . . . . . . . . . . . . . . . . . . . . . 28
- 5.7 Case Study: Political Bias and Feature Generation in LLM-Driven Voting Simulations . . . 30


- 5.7.1 LLM Model Configurations, Computational Resources, and Dataset Selection . . . . 30
- 5.7.2 Experimental Design and Evaluation Methods . . . . . . . . . . . . . . . . . . . . . 30
- 5.7.3 Results Analysis and Performance Comparison . . . . . . . . . . . . . . . . . . . . . 31


- 6 Future Directions & Challenges 34

- 6.1 Pipelines of Integrating Political Science with LLMs . . . . . . . . . . . . . . . . . . . . . 34
- 6.2 Data Scarcity and the Construction of Domain-Specific Datasets . . . . . . . . . . . . . . . 34
- 6.3 Addressing Bias and Fairness in Political Predictions . . . . . . . . . . . . . . . . . . . . . 35
- 6.4 Enhancing Explainability and Reducing Hallucination Risks . . . . . . . . . . . . . . . . . 36
- 6.5 Democratizing Access to Political Knowledge . . . . . . . . . . . . . . . . . . . . . . . . . 36
- 6.6 Call for Novel Evaluation Criteria for Computational Political Science . . . . . . . . . . . . 37


- 7 Conclusion 38 Important Notice


- • Content Warning: This paper may contain offensive content generated by LLMs.
- • Disclaimer: This study examines the capabilities of Large Language Models (LLMs) in the context of election forecasting. The predictions contained herein are for research purposes only, do not represent the views or opinions of the authors, and shall not be construed as definitive or conclusive forecasts.
- • Copyright Notice: All figures in this paper are original creations (not generated with AI tools). Redistribution or reproduction is permitted only with proper attribution to this work.


2

#### 1 Introduction

Recent years have witnessed the extraordinary capabilities of Large Language Models (LLMs) and their contributions to a plethora of fields, such as healthcare [1, 2, 3, 4], finance [5, 6, 7], scientific discoveries [8, 9, 10], transportation [11, 12, 13, 14], and education [15, 16, 17], to name a few. The success of LLMs is mainly attributed to the pre-training over web-scale text corpora [18], which has equipped them with remarkable language intelligence to analyze complicated linguistic patterns [19, 20]. Such outstanding capabilities have been found to align with the pursuit of language analysis in a series of sub-fields in social science [21, 22, 23], where political science has stood out with abundant explorations and substantial advancements [24, 25, 26]. Political science is broadly defined as the study of political systems, behavior, institutions, and policy-making processes, aiming to understand how power and resources are distributed within societies [27, 28]. It relies on diverse forms of political data, including legislative documents, political speeches, public opinion surveys, and news reports, which serve as the foundation for political analysis [29, 30].

![image 1](li-etal-2024-political-llm_images/imageFile1.png)

Figure 1: LLMs are revolutionizing political science through advanced language analysis and interdisciplinary integration capabilities.

Traditionally, political science relied heavily on qualitative methods [31], such as content analysis and case studies, alongside quantitative approaches like statistical modeling and surveys, to examine trends and patterns in political behavior. These methods, while foundational, often faced challenges in scaling, handling multilingual and unstructured data, and deriving insights from vast corpora of text. The emergence of LLMs has helped overcome these hurdles by enabling automated, large-scale analysis of political data, providing researchers with unprecedented tools to process and interpret political texts more effectively. In particular, LLMs have been critical in analyzing extensive corpora of political texts [32, 33], encompassing a wide range of sources such as political speeches [34, 35], legislative documents [36, 37], social media content [38, 39], and news articles [40, 41]. Through these practices, LLMs have enabled stakeholders such as researchers and policy makers to gain an in-depth understanding of various facets such as political behavior [42], public opinion [43], policy formulation [44], and latest election dynamics [45]. For instance, LLMs have revolutionized sentiment analysis by providing nuanced interpretations of public reactions to political events, policies, and figures [46]. This enhanced capability has been crucial in understanding voter sentiment [47] and forecasting election outcomes with greater accuracy [48]. As another example, researchers have employed LLMs to predict legislative voting patterns [49], identify emerging political trends [50], and assess the impact of policy changes on public opinion [51]. The automation of these analytical processes has not only accelerated the pace of research but also increased its precision, allowing for more robust and comprehensive analyses [52]. We use a cartoon in Figure 1 to illustrate the impressive impact LLMs have brought to the area of political science.

Despite the considerable advancements facilitated by LLMs, significant gaps remain hindering their full potential from being realized in this emerging field [22, 53, 54]. Here we identify three most significant gaps below. The first gap, which arises from an interdisciplinary perspective, results from the absence of a systematic understanding of how the potential of LLMs interacts with political science [22]. For example, without a well-defined framework for adapting LLMs to analyze political data, researchers face challenges when attempting to utilize these models for sophisticated tasks, such as analyzing legislative patterns [55] or mapping ideological shifts over time [56]. As such, researchers and practitioners working in political science can encounter difficulty when they resort to ready-to-use LLMs. The second gap, which is rooted in computer science, comes from the lack of fundamental insights about exploiting appropriate techniques to improve LLMs for political science [53]. As an example, LLMs can exhibit characteristics that are undesirable in political science, such as societal bias [57], hallucinations [58], privacy leakage [59], and high computational costs [60].

To facilitate the utility of LLMs in political science, appropriate techniques should be leveraged to handle these issues. For instance, knowledge editing techniques [61, 62] can be used to mitigate the bias exhibited by LLMs, and machine unlearning [63, 64] can be leveraged to remove privacy-related information from LLMs, thereby building more appropriate LLMs for political science. The final gap, which comes from political science, lies in the general deficiency of domain-specific knowledge integrated with LLMs [54]. With the lack of such knowledge of political science, obtaining outputs that are properly informed by a nuanced context from general LLMs becomes difficult. For instance, political texts often contain complex references to historical events, ideological nuances, and policy implications that general LLMs may fail to interpret accurately without specialized training data [65, 66].

Research interest in adapting LLMs to political science applications has been growing rapidly in recent years [49, 67, 53]. A search in major academic databases shows a more than 300% increase in publications related to "LLMs and political science" between year 2020 and 2024, highlighting the field’s continuous expansion and great potential. This surge is driven by LLMs’ ability to process complicated political texts [68], extract ideological patterns [69], and simulate decision-making processes [70, 71] at an unprecedented scale. Back in 2020, Chatsiou et al. [72] discussed the potential influence and applications of LLMs in political science. Nevertheless, the naivety and simplicity of LLMs at that time greatly limited the insights and depth of the discussion. More recently, researchers have investigated specific tasks in political science domain, leveraging LLMs as the main approach. [65, 69, 73] focused on debates analysis and ideological mapping. [74, 24, 75] centered on political election and voting, including election outcome prediction, election dynamics, and voting behavior modeling. [76, 77] investigated the role of LLMs in shaping opinions and conducting polls. [78, 79] explored the contribution of LLMs in enhancing democracy and society values. In contrast to the emergence of works on specific task-level applications, there are only a few survey studies related to LLMs in political science [67, 22]. A comprehensive and systematic survey of recent advances aimed at fostering an in-depth understanding of this topic is urgently needed to assist researchers from multiple fields and to illuminate opportunities for cross-disciplinary ideas.

In this survey, we aim to provide a comprehensive examination of leveraging LLMs’ power to harness the field of political science, addressing key challenges and identifying future research directions. Specifically, we begin by presenting a novel taxonomy to systematically classify existing works in this interdisciplinary domain. This taxonomy categorizes methods and applications, enabling researchers and practitioners to navigate the field more effectively and bridging the first gap identified above regarding the lack of systematic understanding. Next, we explore current advancements from both political and technical perspectives, highlighting techniques for adapting LLMs to political science applications and addressing domain-specific challenges. This section addresses the second gap by delving into solutions for mitigating undesirable characteristics of LLMs, such as societal biases, hallucinations, and privacy concerns, and discusses techniques like knowledge editing and machine unlearning. To bridge the third gap, we further discuss the integration of political science domain knowledge with LLMs, examining the distinct nature of political information and proposing countermeasures to adapt general LLMs for nuanced political tasks. We illustrate how specialized datasets and fine-tuning approaches can be utilized to enhance contextual accuracy and depth. Finally, we explore real-world applications of LLMs in political science, ranging from election prediction and policy analysis to misinformation detection, and conclude with an examination of the current challenges and promising future directions. The survey thus serves as a resource for advancing the understanding and application of LLMs in political science.

The main contributions of this survey paper are summarized as:

- • A Novel Principled Taxonomy. We propose a novel taxonomy for adapting LLMs in political science, structured around two main categories: Classic Political Science Functionality and LLM-Driven Methodologies as shown in Figure 2. The first category addresses core political science tasks, including predictive and generative tasks, simulation, causal inference, and social impacts. The second category focuses on computational methods that customize LLMs to political contexts, including benchmark datasets, data preparation strategy, model design under zero-shot/few-shot learning and fine-tuning scenarios, and inference techniques. The taxonomy provides a systematic framework to bridge existing knowledge gaps, guiding researchers in understanding and applying LLMs effectively within political science field.
- • Comprehensive and Multi-Perspective Review. We offer a comprehensive review of existing works from both political science and computer science perspectives, ensuring a balanced analysis that highlights the


- interdisciplinary nature of Political LLMs. From political perspective, we examine how these models capture and interpret complicated political concepts, historical nuances, and ideological shifts, with a focus on their practical implications. From a computer science perspective, we delve into the specific technologies used to adapt and enhance LLMs for political tasks, covering aspects like fine-tuning strategies, prompt engineering, model architecture adjustments, and inference schemes. For each perspective, we provide insights into both the theoretical and practical challenges involved.
- • Challenges and Future Directions. We identify key limitations of current research and outline pressing challenges that remain unsolved, drawing attention to areas where further advances are needed. These challenges include mitigating societal biases in LLM outputs, enhancing contextual accuracy, managing privacy concerns, and addressing computational costs associated with deploying LLMs in political science. Additionally, we highlight open research questions, such as the need for domain-specific datasets, the development of new evaluation metrics suited to political science tasks, and innovative techniques to improve the interpretability of LLM outputs. These discussions are aimed at inspiring future research endeavors and fostering advancements that broaden the applicability and reliability of Political LLMs.


Difference with Existing Surveys. Despite the abundant explorations in this interdisciplinary area, current survey works remain limited. Researchers have realized and discussed the potential revolutionary contribution of language models as early as in 2017 [29, 80]. However, these works mainly focus on traditional language models and are unable to provide insights about more recent LLMs. After that, multiple survey works have realized the potential of LLMs for political science [72, 25]. However, their discussion lacks a systematic understanding of how LLMs can be adopted in various political science applications and research. More recently, LLM-based applications on specific political or social tasks have been reviewed in several survey works [81, 21, 20, 82, 22, 83, 84]. Nevertheless, these works overwhelmingly focus on applications while the discussion from a technical perspective is ignored. Therefore, it remains unclear how LLMs can be improved to be better adapted. Different from all the survey works above, we aim to present a systematic and comprehensive understanding of leveraging the power of LLMs in political science. Specifically, we equip this paper with a novel principled taxonomy to classify existing works, such that researchers and practitioners can have a broader picture of this interdisciplinary field. Meanwhile, we perform a discussion on each type of work from both political and technical perspectives, which reveals how LLMs can be improved to be better adapted. Table 1 provides a detailed comparison between our survey and other related surveys in political or social science.

Intended Audiences. The intended audience of this survey includes (1) computer science researchers and practitioners who seek a structured understanding of how LLMs are applied in political science, aiming to bridge interdisciplinary gaps; and (2) political science researchers and practitioners who seek to leverage LLMs in ways that are sensitive to the unique requirements of their field, such as nuanced interpretation and contextual accuracy [57]. This survey also benefits interdisciplinary scholars who are interested in exploring the intersection of AI and social sciences, as well as policymakers and government agencies intending to employ LLM-based tools for public opinion analysis, election forecasting, and legislative research tasks.

Structure of This Survey Paper. The remainder of this article is organized as follows. In Section 2, we provide the related preliminaries of LLM and political science. Following that, the proposed taxonomy of LLM for political science is detailed in Section 3. Section 4 introduces the core functionalities of political science that can benefit from LLMs, including predictive tasks, generative tasks, simulation, causal inference, and ethical concerns & social impacts. Section 5 focuses on LLM-driven methodologies tailored for political science, covering benchmark datasets, data processing strategies, fine-tuning and inference on LLMs, and an empirical study on voting simulation. Subsequently, Section 6 discusses potential future directions, outlining research opportunities to enhance the effectiveness and applicability of LLMs in the field of political science. Finally, we conclude the survey paper in Section 7.

#### 2 Preliminaries

Computational Political Science (CPS). Computational Political Science (CPS) is an interdisciplinary field that integrates computational methods with political science to analyze political systems, behaviors, and outcomes [85]. By leveraging tools such as data analytics, machine learning, and natural language processing (NLP), CPS enhances the understanding of complex political phenomena. The field has evolved from relying

Table 1: Comparison with Existing Surveys on Broad Political Science Field (Abbreviations: PoliSci = Political Science, CPS = Computational Political Science, CS = Computer Science).

[22] [21] [83] [82] [84] [20] [81] Ours Proposed Taxonomy on

LLM for PoliSci ✗ ✗ ✗ ✗ ✗ ✗ ✗ ✓ Literature Review from

PoliSci Perspective ✓ ✗ ✓ ✗ ✗ ✓ ✓ ✓ Literature Review from

CS Perspective ✗ ✗ ✓ ✗ ✓ ✓ ✗ ✓

Structured Analysis of CPS Methodologies ✗ ✗ ✗ ✗ ✗ ✗ ✗ ✓ Include Experiments

and Evaluations ✓ ✓ ✓ ✓ ✗ ✗ ✓ ✓

Application

Examples ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ Comprehensive Summary

of Benchmarks ✓ ✗ ✗ ✗ ✗ ✗ ✗ ✓

Analyzing Limitations in Existing Methodologies ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓

Future Research

##### Direction ✓ ✓ ✓ ✓ ✓ ✓ ✗ ✓

Caleb Ziems et al., 2024 [22]; Lisa P. Argyle et al., 2023 [21]; Joseph T. Ornstein et al., 2022 [83]; David Rozado, 2023 [82]; Laura Weidinger et al., 2021 [84]; Mitchell Linegar et al., 2023 [20]; Kyuwon Lee et al., 2024 [81].

on traditional statistical models, such as regression-based analyses, to embracing AI-driven approaches that enable the processing of large-scale, unstructured political data. This shift has been particularly transformative in tasks like election forecasting, public opinion analysis, and policy evaluation, where modern techniques offer greater scalability and accuracy.

Evolution of Language Models in Political Science. Early applications of AI in political science relied on rule-based systems and traditional machine learning methods [86], such as logistic regression [87] and support vector machines (SVMs) [88], to perform basic political tasks. These methods were limited by their reliance on manually crafted features and structured data [86]. The advent of pre-trained language models, including Word2Vec [89] and BERT [90], marked a significant shift in natural language processing, enabling the analysis of large-scale, unstructured political text. By capturing contextual relationships and semantic nuances in data, these models greatly enhanced the ability to process complex political discourse, advancing domain applications like policy analysis, legislative interpretation, and public opinion mining.

###### 2.1 Large Language Models (LLMs)

The foundation of most LLMs lies in the Transformer architecture [91], which introduced the self-attention mechanism to effectively model long-range dependencies in text. This innovation marked a departure from earlier sequence models like RNNs and LSTMs, which struggled with vanishing gradients and limited context windows. Core components such as multi-head attention, feedforward layers, and positional encodings enabled Transformers to process sequences in parallel, significantly improving scalability and efficiency. Early LLMs, such as BERT [90], leveraged the Transformer framework through masked language modeling, excelling in bidirectional context understanding. Autoregressive architectures like GPT [92] later extended these capabilities, focusing on sequential token prediction for fluent and coherent text generation. The advent of models like T5 [93] unified various NLP tasks under a single architecture by using sequence-to-sequence learning. Recent advancements [94, 95, 96, 97] further evolved LLM architectures, emphasizing efficiency and task-specific adaptability. Additionally, innovations like multimodal architectures and scalable models such as LLaMA [98] and GPT-4 [99] demonstrate a shift toward systems capable of cross-domain understanding and dynamic interaction, underpinning the transformative potential of LLMs in computational tasks across fields.

General Purpose LLMs. General-purpose LLMs like GPT [99] and BERT [90] are developed through two primary training paradigms: autoregressive modeling (AR) [100] and masked language modeling (MLM) [101]. AR models, exemplified by GPT, generate tokens sequentially, prioritizing fluency and coherence in text generation. MLM, as utilized in BERT, predicts masked tokens within sentences, fostering a nuanced contextual understanding of language. These pre-training paradigms equip LLMs with a robust foundational understanding of linguistic patterns, making them highly adaptable for fine-tuning on task-specific datasets. Leveraging these versatile models, researchers can efficiently address domain-specific challenges without undertaking resource-intensive pre-training.

LLM Fine-tuning Techniques. Fine-tuning adapts pre-trained general-purpose LLMs to downstream specialized applications. Supervised fine-tuning refines model outputs using labeled datasets, aligning them with task-specific objectives [102]. Instruction fine-tuning trains models to better follow user directives through datasets of instructions and outputs, enhancing adherence to user intents and versatility [103]. Reinforcement Learning with Human Feedback (RLHF) [104] leverages human evaluators to rank responses, guiding LLMs to align with human preferences while reducing harmful or biased behaviors.

Zero-shot, Few-shot, and In-context Learning. LLMs demonstrate remarkable capabilities in zero-shot [105], few-shot [106], and in-context learning [107], leveraging pre-trained knowledge to perform tasks with minimal or no additional training. Zero-shot learning enables task generalization without task-specific training, while few-shot learning benefits from a minimal set of labeled examples. In-context learning, which is achieved through task descriptions and examples within prompts, empowers models to dynamically adapt to novel tasks without parameter updates.

LLM Inference and Decoding Techniques. Effective inference strategies are crucial for generating highquality outputs from LLMs. Methods like greedy decoding [108] and beam search [109] prioritize sequence coherence, while nucleus sampling [110] enhances diversity by sampling within the top-probability distribution. Advanced techniques like Retrieval-Augmented Generation (RAG) [94] integrate external knowledge bases, while prompt engineering [111], Chain-of-Thought (CoT) [112], and knowledge injection techniques [113] improve task-specific performance, especially in complex scenarios.

LLM Scalability and Efficiency. LLM scalability relies on distributed training frameworks [114], efficient parameter adaptation [115], fast inference and serving frameworks [116], and hardware optimizations [117]. Techniques like LoRA [118] and adapters [119] enable parameter-efficient fine-tuning, reducing computational requirements without compromising performance. Software frameworks such as vLLM [120] and TensorRTLLM [121] facilitate fast LLM inference and serving through advanced batching and memory management. Hardware acceleration, including GPU and TPU advancements [117, 116], supports the training and inference of increasingly large models, driving efficiency in both computation and energy consumption.

###### 2.2 Core Computational Political Science Concepts

Political Data Sources and Text Generation. Political data encompasses diverse sources such as political news, speeches, legislative records, party manifestos, social media contents, etc. Analyzing these data requires handling challenges like data scarcity, imbalance, and linguistic nuances, which hinder comprehensive analysis. One critical application in CPS is Political Text Generation, where LLMs are employed to produce political content such as speeches, policy briefs, and debate scripts [122]. These generative models assist political figures and analysts by creating coherent, persuasive, and contextually relevant texts. LLMs can simulate political scenarios and craft narratives, shaping public opinion and enhancing political communication.

Election Prediction and Voting Behavior. Election prediction focuses on forecasting voter turnout, swing state dynamics, and overall electoral outcomes. LLMs analyze a combination of historical election data, public opinion surveys, and social media discourse to identify patterns influencing voter behavior [24, 123]. These models provide insights into key demographic and psychological factors affecting voter preferences, aiding political campaigns and policymakers in tailoring strategies to engage the electorate effectively.

Policy and Legislative Interpretation. Policy and legislative interpretation involves analyzing complex legal texts, such as bills, statutes, administrative rules, and debates, to understand their implications and the ideologies they represent. LLMs excel at parsing and summarizing these documents, identifying key arguments, and

predicting potential policy outcomes [124]. This capability offers political scientists a deeper understanding of legislative processes and helps anticipate the effects of policy changes on societal and political structures.

Misinformation/Fake News Detection. Safeguarding political discourse requires addressing misinformation and fake news, which can significantly distort public opinion and decision-making. LLMs are adept at detecting false or biased information by analyzing the structure, intent, and credibility of news articles, social media posts, and political statements [125]. By flagging harmful content, these models ensure the integrity of political information and contribute to maintaining a healthy democratic environment.

Political Risk and Conflict Prediction. Political risk and conflict prediction aim to forecast the likelihood of political instability, unrest, or international conflict [126]. CPS-based methods can analyze geopolitical data, diplomatic communications, and historical trends to identify early signs of conflict and assess the risks involved in political decisions. These predictions are invaluable for policymakers and international organizations in making informed decisions and preparing for possible crises.

Political Game Theory and Negotiation. Political game theory and negotiation involve modeling strategic interactions between political entities, such as governments, parties, or international entities [127]. The latest advancements in LLMs hold promise in analyzing negotiation strategies, predicting the outcomes of political bargaining, and identifying optimal decision-making approaches. By simulating various political scenarios, LLMs are expected to have a better understanding of power dynamics, coalition building, and diplomatic negotiations in international politics.

LLMs act as pivotal tools bridging computational methodologies and political science applications. By integrating advanced language processing capabilities with political data analysis, LLMs enable breakthroughs in taskssuchaselectionforecasting[24], legislativetextsummarization[128], andcombatingmisinformation[125]. These advancements demonstrate how LLMs transcend traditional limitations, providing scalable, adaptable, and effective solutions for political science research.

#### 3 Taxonomy on LLM for Political Science

Figure 2 presents a comprehensive taxonomy for understanding the integration of LLMs in political science, organized into two main categories: classified political science functionalities & tasks and LLM-driven computational approaches for political science. The first category highlights how traditional political science functions are enhanced through LLM capabilities, while the second category focuses on computational techniques for effectively implementing LLMs in political research.

The classified political science functional tasks span five primary categories, including Predictive Tasks, Generative Tasks, Simulation, Explainability & Causal Inference, and Social Impacts. Predictive Tasks (section 4.1) use LLMs to analyze and forecast trends in public opinion, electoral outcomes, and policy impacts. Generative Tasks (section 4.2) enable the synthesis of political data, such as summarizing legislative documents or generating debate transcripts [262, 263], expanding the scope and accessibility of political data analysis. Simulation (section 4.3) leverages LLMs to model complex political behaviors and interactions [147, 264], reducing research costs and enhancing efficiency in studying dynamics like voting patterns and policy impact. Explainability & Causal Inference (section 4.4) applies LLMs to identify relationships and generate counterfactuals in political analysis [159, 160], providing insights into causality and potential biases. Finally, Ethical Concerns & Social Impacts (section 4.5) analyzes the influence of LLM-driven applications for political campaigns and communication strategies, emphasizing the ethical considerations and public ramifications of political science research.

TheLLM-drivencomputationalapproachesforpoliticalscienceconsistoffivecomponents: BenchmarkDatasets, Data Processing, Fine-Tuning LLMs for Political Science Tasks, LLM Inference under Zero/Few-Shot InContext Learning Setting, Other LLM Inference Techniques, and Case Study on Voting Simulation. Benchmark Datasets (section 5.1) provide foundational resources on political topics, while Data Processing (section 5.2) addresses issues of bias, annotation, and augmentation to ensure data reliability and representativeness. Fine-tuning (section 5.3) explores methods to tailor LLMs for specific political science tasks, optimizing performance through targeted training strategies. Inference under Zero-Shot (section 5.4) and Few-Shot Learning (section 5.5) highlight approaches for achieving task-specific insights with minimal labeled data,

[33, 68, 129, 130, 131, 132] [68, 132, 133, 134, 135, 136, 137, 138] [131, 139, 140] [21, 73, 129, 141, 142, 143, 144] [129, 141, 144, 145, 146] [21, 73, 141, 142, 144] [147, 148, 149, 150, 151, 152, 153, 154] [55, 155, 154, 152]

Data Annotation Predictive Approaches Inference and Explanation

c

Predictive Tasks

Synthesize Political Data

Expanding Research Scope

Generative Tasks

c

Reduce Costs &Enhance Efficiency

###### Classical Political Science Function &Modern Transformation

Simulate Behavior Dynamics

c

Simulation

Simulate Text-Based Discussion

[156, 157, 158, 159, 160, 161, 162, 163] [164, 165, 166, 167] [168, 169, 170, 32, 171, 172, 82, 66, 173] [32, 143, 174, 66, 82, 141, 173] [175, 176, 177, 155, 155, 21, 48] [178, 143, 26, 75, 179] [50, 180, 181, 182, 183, 184]

Causal Inference with LLMs

c

Explanation Theory

Explainability in Political Science

Identify &Mitigate Biases Ethical Consideration &Fairness

c

Social Impacts

Influence on Political Campaigns Enhancing Political Communication

Sentiment Analysis &Public Opinion

###### LLM4Political Science

[185, 186, 187, 188, 189, 190] [191, 192, 193]

Election Prediction &Voting Behavior Political Legislation

c

Benchmark Datasets

c

[194, 195, 196, 132] [197, 198, 127] [199, 187, 200, 201, 202, 203]

Misinformation Detection

Game Theory &Negotiation

Dataset Annotation

Data Processing

[204, 205, 206, 207] [208, 209, 210, 211]

Data Bias and Representation

c

Data Augmentation

[212, 213, 214]

Task-Specific Data Preparation

Fine-Tuning LLM c

[215, 216, 217, 218, 219, 115] [220, 221, 222]

Fine-Tuning Strategies

Tech Foundation for LLM Adaptations in Political Science

Application Examples

[223, 105, 224, 225, 226, 227]

Contextualization & Example Design

Zero/Few-Shot Inference c

[228, 229, 230, 231, 232] [228, 45, 233, 234, 235, 236, 237] [94, 238, 239, 240, 240]

Task-Specific Prompt Engineering

Use Case &Application Examples

Retrieval-Augmented Generation

[241, 242, 243, 244] [62, 245, 246, 247, 248]

Chain-of-Thought Reasoning

c

Other Inference Techniques

Knowledge Editing

[249, 250, 251, 252]

Self-Consistency Decoding

[253, 254, 255, 256, 257, 258] [189, 259, 177] [260, 204, 261, 48, 70]

Model Configurations & Dataset

Case Study on Voting Simulation c

Experimental Design & Criteria

Results Analysis & Comparison

Figure 2: The proposed Taxonomy on LLM for Political Science.

focusing on prompt engineering and example selection. Finally, Other Inference Techniques (section 5.6) such as retrieval-augmented generation [94], chain-of-thought reasoning [265], knowledge editing [266], and self-consistency decoding [250] enhance the adaptability of LLMs for nuanced political tasks. Together, these computational approaches construct a robust framework tailored for political science research.

#### 4 Classical Political Science Functions and Modern Transformations

LLMs have brought transformative changes to political science, reshaping traditional methodologies and unlocking new analytical opportunities. This section provides a structured overview of current research, categorizing it into five key areas. Four of these areas focus on the functional applications of LLMs in political science, while the fifth explores normative considerations, emphasizing societal and ethical implications.

We divide the functional categories into predictive, generative, simulation, and explainable tasks. While computer science researchers often categorize LLM-based research into predictive and generative tasks

[23, 267, 18], we propose two additional dimensions - simulation and causal inference, in order to address the unique complexity of LLM for Political Science.

While simulation is inherently generative, we distinguish it as a separate category due to its unique focus on replicating human-like attitudes, behaviors, and decision-making processes in specific political contexts. In this review, we list research that focuses on producing new content without emulating human cognitive processes as "generative tasks", and research mimicking how human actors or groups would react, taking into account motivations, biases, and contextual influences as "simulation".

Additionally, political science is not merely concerned with making predictions but also with understanding the causes behind political phenomena. For instance, in addition to predicting the outcome of elections, political scientists are also interested in why certain outcomes occur. Therefore, using LLMs to support inference tasks (e.g., processing vast datasets, and identifying causal mechanisms) is promising in political science and a necessary addition to predictive and generative tasks.

###### 4.1 Automation of Predictive Tasks

Definition. Predictive tasks in Computational Political Science involve anticipating future events or trends based on existing data, and they are fundamental in political science for applications such as election forecasting, policy support prediction, and analyzing voter behavior. In political science, predictive tasks are crucial because they provide insights that can guide decision-making, inform policy, and help researchers understand complex social dynamics. Traditional predictive methods in political science often require extensive manual labor. For instance, certain predictive tasks may require researchers to manually collect survey responses, historical election data, or economic indicators, which can be time-consuming and prone to human error. In contrast, recent advancements in LLMs offer an alternative by automating predictive tasks. The automation of predictive tasks reduces manual effort and possible human error, while increasing speed, consistency, and scalability.

Enhancing Prediction with LLM-based Data Annotation. LLM-based automation significantly enhances predictive capabilities by providing consistent and scalable solutions for data-intensive tasks. This is especially helpful in data annotation. Annotating large datasets manually is time-consuming and prone to inconsistencies [33, 68, 129]. LLMs can rapidly process and annotate data in a consistent manner. Political science researchers have employed LLMs to annotate Political Ideology [33, 130, 131, 132], Fake News [134, 135, 136, 137], Tone (sentiment) [33, 68, 132, 140, 139], and content of various Political Texts [33, 68, 138, 133, 132]. Researchers also find that the quality of automated LLM annotation outperforms crowd workers and even some domain experts. Therefore, data annotation by LLM not only enhances efficiency but also reduces the potential for human bias and error in the data annotation process.

Prediction Tasks in English-Speaking Contexts. The effectiveness of LLMs in predictive tasks is demonstrated through their applications in both English and non-English contexts. In English-speaking settings, platforms like ChatGPT and Llama are frequently used for large-scale political text analysis. For instance, Lashitew and Mu [139] analyze comments and letters submitted by companies to the U.S. Securities and Exchange Commission regarding climate change disclosure regulations. Leveraging GPT-3, they efficiently process and analyze a large volume of text data, identifying patterns and sentiments within the corporate responses. Additionally, [140] explore the application of GPT-4 in processing and analyzing public feedback collected online in New Zealand. They focus on responses to a proposed plan change in Hamilton City, New Zealand, assessing GPT-4’s effectiveness in summarizing feedback, identifying topics, and analyzing sentiment. Results showed GPT-4 performed these tasks accurately.

Predictive Tasks in Non-English Contexts. LLMs have also shown robust performance in multilingual environments and in diverse regional applications. [33] evaluate the performance of GPT-4 in coding political texts across variables such as relevance, negativity, sentiment, and ideology across the United States, Chile, Germany, and Italy. The findings indicate that GPT-4’s annotations closely align with those of human experts, suggesting that LLMs can effectively assist in political text analysis. Moreover, Chalkidis and Brandl [131] utilize Llama to evaluate speeches from European Parliament debates, with the EUandI questionnaire serving as a reference or benchmark to verify political leanings. The study demonstrated that Llama has considerable knowledge of national parties’ positions and is capable of contextual reasoning as well as ChatGPT. Mellon et al. [146] take a step further to evaluate six different popular LLMs in categorizing open-text survey responses

and detecting issue importance. Their task involved classifying the most important issue responses from the British Election Study Internet Panel into 50 distinct categories. The study concluded that LLMs, particularly Claude-1.3, can effectively code open-text survey responses, providing a scalable alternative to human coders.

LLM-based Advancements. To better illustrate the workflow of LLMs in predictive tasks, we provide a diagram showcasing the U.S. Presidential Election outcome prediction as an example. This example highlights how LLMs integrate diverse data sources, process them into structured representations, and generate actionable predictions. As shown in Figure 3, the workflow begins by integrating data sources like polls, demographics, social media sentiment, and news headlines. After preprocessing (cleaning, normalization, and vectorization), the LLM performs contextual understanding and generates outputs such as winning probabilities and swing state predictions, showcasing its ability to automate complex, data-driven tasks like U.S. election predictions.

![image 2](li-etal-2024-political-llm_images/imageFile2.png)

![image 3](li-etal-2024-political-llm_images/imageFile3.png)

![image 4](li-etal-2024-political-llm_images/imageFile4.png)

![image 5](li-etal-2024-political-llm_images/imageFile5.png)

![image 6](li-etal-2024-political-llm_images/imageFile6.png)

![image 7](li-etal-2024-political-llm_images/imageFile7.png)

![image 8](li-etal-2024-political-llm_images/imageFile8.png)

News Headlines

Poll Data Demographics Data

Historical Data

Sentiment Analysis

![image 9](li-etal-2024-political-llm_images/imageFile9.png)

![image 10](li-etal-2024-political-llm_images/imageFile10.png)

![image 11](li-etal-2024-political-llm_images/imageFile11.png)

Data Encoding & Preprocessing

Data Cleaning

Text Tokenization Network Correlation

![image 12](li-etal-2024-political-llm_images/imageFile12.png)

![image 13](li-etal-2024-political-llm_images/imageFile13.png)

![image 14](li-etal-2024-political-llm_images/imageFile14.png)

![image 15](li-etal-2024-political-llm_images/imageFile15.png)

Contextual Understaning

Multi-Source Data Fusion

Understanding Voting Contexts

![image 16](li-etal-2024-political-llm_images/imageFile16.png)

![image 17](li-etal-2024-political-llm_images/imageFile17.png)

![image 18](li-etal-2024-political-llm_images/imageFile18.png)

![image 19](li-etal-2024-political-llm_images/imageFile19.png)

Prediction Engine in LLM

![image 20](li-etal-2024-political-llm_images/imageFile20.png)

Predictive Intelligence Agent

Dynamic Prediction Pipeline

In addition to predictive applications in various domains, recent research also highlights tailored frameworks and approaches developed specifically for political science. Such research often includes adjustments to LLMs to improve their applicability and accuracy in political contexts. For instance, PoliPrompt [68] is a three-stage framework leveraging LLMs for text classification in political science. This framework shows exceptional performance in classifying topics within multi-class news datasets, such as BBC news reports, labeling nuanced political science concepts, and analyzing the tones of campaign advertisements from the 2018 midterm election. This kind of tailored approach helps ensure that the model outputs are relevant and accurate within specific political frameworks. Similarly, by studying the classification on text alignment or opposition toward a particular issue, Cao and Drinkle [132] find that incorporating metadata (e.g., party affiliation) into political stance detection tasks can notably enhance model performance on ParlVote+ benchmark.

Pretrained General LLMs

Output Predictions

![image 21](li-etal-2024-political-llm_images/imageFile21.png)

![image 22](li-etal-2024-political-llm_images/imageFile22.png)

![image 23](li-etal-2024-political-llm_images/imageFile23.png)

Winning Probability

Swing State Predictions

Sentiment Trends

Figure 3: The workflow of LLM-based automated predictive task, using the U.S. Presidential Election prediction as an example.

Summary and Challenges. The automation of predictive tasks by LLMs offers transformative potential in political science research [78, 67]. From scaling data annotation processes to handling multilingual data and adapting to specific political frameworks, LLMs provide a powerful tool for researchers aiming to predict and analyze trends in political behavior and sentiment, as well as test political theories. However, existing research still faces notable challenges. LLMs can sometimes lack contextual understanding in nuanced political discourse, particularly in multilingual or culturally specific settings, where subtle language differences may lead to misinterpretation [57]. Additionally, the reliance on pre-existing data and the potential for inherent biases in training datasets can result in biased predictions, impacting the accuracy and neutrality of the automated outputs [268]. Furthermore, while LLMs have shown proficiency in annotation and classification, their performance may degrade when faced with highly complex or specialized political tasks that require deeper domain knowledge [73]. Addressing these limitations is essential for maximizing the utility and reliability of LLMs in political science applications.

###### 4.2 Automation of Generative Tasks

Definition. Generative tasks in political science involve creating synthetic data, simulating scenarios, or augmenting incomplete datasets, offering new insights where traditional data sources are either unavailable or insufficient [21, 142, 73, 141]. Unlike analytical tasks that focus on interpreting existing information, generative tasks expand the boundaries of what can be studied by creating representations of missing data or by projecting possible future scenarios [21, 142, 73]. Generative tasks are particularly valuable for political

science applications where the complete dataset is often hard to obtain due to privacy concerns, logistical constraints, or high costs associated with traditional data collection methodologies [141, 144].

The absence of complete data often underscores the complexity, scope, and depth of political science research questions [21, 142, 73, 141]. For example, understanding the roles and performance of executive agencies, which exert significant influence over policy, presents substantial challenges due to the limited availability of data [141]. Traditional CPS approaches, such as principal component analysis (PCA)-based methods, demand extensive input data, limiting their application in issue-specific analyses, such as polarizing topics like abortion or gun control. LLMs are capable of extracting valuable insights from incomplete datasets if provided with well-structured prompts, broadening the analytical capacity of studies [21, 142, 73]. This innovation enables the exploration of previously constrained research areas [141, 144]. Existing research in this domain can be grouped into two major categories: Synthesizing Political Data and Enhancing Research Scope.

Synthesizing Political Data. The ability to generate synthetic data is a powerful application that directly addresses the critical issue of data scarcity and facilitates the exploration of latent variables. Data collection is often a significant hurdle in political science due to the costs and time involved in conducting surveys, gathering reliable public opinion data, or accessing confidential voting records. Synthetic data generation by LLMs offers an efficient, cost-effective alternative that can serve as a proxy for real-world data, providing insights where traditional data sources are limited [269]. For instance, Bisbee et al. [142] demonstrate that LLM-generated synthetic data can effectively replicate survey responses, simulating various public opinion trends even in the absence of comprehensive survey datasets. They successfully explore public sentiment on immigration, healthcare, and climate policy issues. This application is particularly useful for analyzing time-sensitive political questions, where delays in data collection could mean losing valuable insights into changing public opinion. Another noteworthy study comes from Argyle et al. [21], who show that LLMs can simulate human responses, mimicking the distribution of survey data across demographic groups and regions. In this case, LLMs help mitigate the data scarcity issue by generating synthetic samples that reflect genuine population characteristics, supporting research on political trends in underserved or underrepresented communities. We provide the workflow of LLM-based generative tasks in Figure 4, using the synthesis of political speeches or manifestos as an example. Starting with inputs like topic definitions, ideological tags, and tone preferences, the model preprocesses and contextualizes data to generate coherent outputs. Techniques such as prompt engineering and fine-tuning guide the process. The outputs, including political speeches tailored to ideological perspectives, demonstrate how LLMs can address challenges of data scarcity and enable synthetic data generation for political research.

LLMs also play a critical role in estimating political ideologies in situations where conventional data sources, such as voting records, media publications, or public statements, are incomplete. Wu et al. [73] illustrate how LLMs can infer political ideologies by analyzing existing contextual information and filling in missing details, thereby offering a fuller, more nuanced picture of the ideological spectrum in specific political landscapes. Moreover, Alvarez et al. [143] explore the potential of LLMs in simulating voter behavior and party strategies, thus extending traditional political modeling frameworks. By generating synthetic data that represents hypothetical voter responses to specific policies or campaign strategies, LLMs help researchers examine potential outcomes in elections or other political events. Such applications offer new avenues for understanding the impact of political campaigns and policy proposals, even when comprehensive polling data is unavailable.

###### Generative Task Techniques

![image 24](li-etal-2024-political-llm_images/imageFile24.png)

![image 25](li-etal-2024-political-llm_images/imageFile25.png)

![image 26](li-etal-2024-political-llm_images/imageFile26.png)

Prompt Engineering Data Augmentation

Fine-tuning

![image 27](li-etal-2024-political-llm_images/imageFile27.png)

Large Language Models

![image 28](li-etal-2024-political-llm_images/imageFile28.png)

![image 29](li-etal-2024-political-llm_images/imageFile29.png)

![image 30](li-etal-2024-political-llm_images/imageFile30.png)

![image 31](li-etal-2024-political-llm_images/imageFile31.png)

Tone and Style

Contextual Understaning

![image 32](li-etal-2024-political-llm_images/imageFile32.png)

Ideological Tags

![image 33](li-etal-2024-political-llm_images/imageFile33.png)

![image 34](li-etal-2024-political-llm_images/imageFile34.png)

Campaign Speech Content

General Style Content

![image 35](li-etal-2024-political-llm_images/imageFile35.png)

Topic Definition

Task-Specialized Framework Universal Framework

Input Specifications

Generated Political Speech:

To secure the economic future of U.S., we must cut taxes further and eliminate burdensome regulations that stifle small businesses.

Figure 4: Workflow for LLM-based generative tasks, illustrating the synthesis of political speeches with specific ideology, style, and focus of content.

LLMs further enhance research potential by enabling the generation of large and dynamic datasets that track the latest political trends over time. [144] emphasize the utility of LLMs in constructing extensive synthetic

datasets by generating responses or synthesizing textual data. This enables the analysis of long-term shifts in public opinion or political rhetoric across diverse populations.

EnhancingResearchScope. Beyonddatasynthesis, LLMsenableresearcherstoexplorepreviouslyunattainable research areas by providing insights into complex or hard-to-measure variables. This capacity to expand the scope of political science research is especially valuable in analyzing intricate social dynamics, government policies, and ideological nuances where data gaps often hinder rigorous analysis. For example, Napolio’s [141] work on the ideological positioning of executive agencies illustrates how LLMs can provide insights into policy stances and organizational biases even in the absence of direct, comprehensive data. The use of LLMs to fill data gaps allows for a deeper understanding of government operations and policy influences that would otherwise remain hidden. Similarly, Egami et al. [129] demonstrate that LLMs can work with imperfect or noisy data, producing robust analytical results even when complete datasets are unavailable. This flexibility reduces dependency on high-quality data and supports rigorous analysis in fields like public policy and election studies, where data completeness is often challenging to achieve.

LLMs are also adept at analyzing extensive political text corpora, which enables researchers to uncover subtle patterns in discourse that are difficult to capture through traditional manual analysis. Palmer and Spirling [144] highlights the ability of LLMs to process large volumes of text, revealing shifts in political narratives and public sentiment over time. Similarly, the use of LLMs to analyze political Q&A sessions in [145] shows how these models can detect nuances in rhetoric and speaker intent, providing valuable insights into the subtleties of political communication. Furthermore, Mellon et al. [146] showcase the utility of LLMs in coding open-ended survey responses at scale. This application allows researchers to classify responses efficiently, identifying dominant issues and sentiments within a population. By automating the analysis of qualitative data, LLMs offer a powerful solution for understanding public concerns and policy impacts, contributing to a more comprehensive understanding of societal dynamics.

Summary and Challenges. LLMs have reshaped the field of generative tasks in political science, enabling new possibilities in data synthesis and research scopes. These models provide political scientists with the tools needed to address data scarcity issues, create realistic proxies for hard-to-collect data, and simulate complex political phenomena. However, the challenges in ensuring the validity, neutrality, and reliability of synthetic data remain significant. Biases embedded in LLM-generated data can potentially skew results if not rigorously managed, and reliance on synthetic data requires careful validation to ensure accuracy. Moreover, while LLMs are proficient in generating insights, the interpretability of these models in highly nuanced political contexts remains a challenge. Addressing these limitations will be essential for leveraging the full potential of LLMs in generative political science research.

###### 4.3 Simulation of LLM Agents

Definitions. The concept of Simulation Agents in LLM for political science refers to the use of large language models to create interactive environments in which autonomous agents simulate behaviors, decisions, or dialogues. These tasks aim to explore dynamic systems, such as political behaviors, negotiations, or conflicts, by modeling interactions between agents. While both Generative Tasks and Simulation Agents leverage LLMs, their objectives and methodologies are distinct. Generative tasks focus on creating new data or textual content to address data scarcity, enabling researchers to fill gaps or produce synthetic datasets for foundational analysis. In contrast, simulation agents emphasize modeling interactions and dynamics within complex environments, offering insights into strategies, behaviors, and evolving systems. We present a comprehensive comparison between these tasks in Table 2.

The use of LLMs to simulate human-like behavior in interactive environments represents a significant advancement in political science [147]. These simulations offer new ways to address complex societal questions, particularly those involving the behavior of political actors in intricate environments [270]. Traditional methods, such as Agent-Based Models (ABMs) [271], rely on predefined parameters and restricted environments, often limiting their capacity to capture the complexity and realism of political dynamics. LLMs overcome these constraints by using natural language prompts to define behavior rules and environmental contexts [148], allowing for adaptive, context-sensitive, and personalized agent behaviors [149]. Current research in this area

Table 2: Comparison of Generative Tasks and Simulation Tasks in Political Science

Key Attribute Generative Tasks Simulation Tasks

Objective Create new data or textual content to address data scarcity.

Model interactions and dynamics within complex environments.

Focus Producing synthetic data or content for foundational analysis.

Exploring strategies, behaviors, or evolving systems through agents.

Output Independent generated results, such as datasets or textual outputs.

Analytical results on interactions, strategies, or behavior patterns.

Research Context Filling data gaps and enhancing data availability. Studying dynamic processes and agent interac-

tions. Methodology Generative models producing outputs based on

Simulations of agents interacting within predefined environments.

prompts.

Application Examples Synthetic survey data, opinion generation, or text classification.

Negotiation models, conflict dynamics, or opinion shift simulations.

is focused primarily on two applications: (1) using agents to simulate behavior dynamics and (2) using agents to simulate text-based discussion processes [154, 155, 149].

Simulate Behavior Dynamics. Recent studies demonstrate the potential of LLMs to replicate complex social behaviors in political settings, addressing limitations in traditional ABM approaches. Dai et al. [150] simulate agents shifting from conflict to cooperation in resource-constrained environments through Hobbesian Social Contract Theory, exploring how political entities navigate scarcity and develop governance structures. Hua et al. [151] take a historical approach, modeling strategic decision-making during major global conflicts such as the World Wars, focusing on the interplay between diplomacy and military tactics in the evolution of warfare. Jin et al. [152] extend these simulations to a cosmic scale, where agents with distinct worldviews engage in cooperation and conflict, highlighting how ideological divergence influences inter-civilization dynamics. Other research builds on these approaches by introducing more nuanced political scenarios. Chuang et al. [153] simulate opinion dynamics within political networks, where agents adjust their beliefs based on interactions with other agents, providing a closer examination of political polarization and consensus-building processes. Similarly, Guan et al. [154] use LLM-based agents to model AI diplomacy, where agents negotiate and evolve their strategies in complex international relations, mirroring real-world diplomatic negotiations. These studies collectively showcase how LLM-driven simulations of behavior dynamics can provide valuable insights into governance, conflict resolution, and social interaction, offering novel ways to study political and diplomatic behavior in various contexts [150, 154, 272, 152, 153, 151].

Simulate Text-based Discussion. Shifting from physical to text-based simulations, recent studies have explored political interactions through dialogue, using LLM agents to simulate complex discussions and negotiations. Baker et al. [55] model U.S. Senate policy debates, where LLM agents simulate legislative decision-making and bipartisanship, providing insights into how political actors navigate ideological divides and negotiate policy outcomes. Moghimifar et al. [155] take a different approach by simulating multi-party coalition negotiations using LLM-driven dialogue. Their work highlights the intricacies of building and maintaining political alliances through textual interaction, emphasizing how agents negotiate, compromise, and form agreements in multi-party systems. Guan et al. [154] extend this approach to international diplomacy, focusing on how LLM agents evolve strategies in alliance-building and negotiation on the global stage. Their research underscores the dynamic nature of diplomatic discourse, where agents adapt to shifting geopolitical contexts and evolving relationships between states. Additionally, Jin et al. [152] explore the use of LLMs in simulating text-based discussions between civilizations with divergent worldviews, pushing the boundaries of how text-based interactions can simulate inter-group communication and conflict resolution on a cosmic scale. These studies collectively illustrate the capacity of LLM simulations to model political decision-making through textual interactions, offering a contrast to action-oriented simulations like those seen in warfare and conflict resolution [55, 153, 155, 154, 152].

Summary and Challenges. LLM-driven simulations provide a novel framework for exploring the complexity of political behavior and interactions by enabling adaptive, context-aware modeling that was previously unattainable with traditional methods. These simulations bridge gaps in understanding how dynamic processes, such as opinion shifts, negotiation strategies, and conflict resolution, evolve under different political scenarios. Despite these advancements, significant challenges persist. Ensuring the neutrality of simulations remains difficult due to biases inherent in LLM training datasets, which can skew outcomes and interpretations. Moreover, ethical concerns arise when simulations replicate sensitive behaviors or policy decisions, potentially influencing real-world political discourse. Last but not least, the computational costs of running large-scale simulations can limit accessibility for many researchers. Addressing these issues will require robust validation techniques, interdisciplinary collaboration, and ongoing innovation to ensure that LLM simulations remain reliable and ethically sound tools for political science research.

###### 4.4 LLM Explainability and Causal Inference

Definition of Explainability. Explainability in the context of LLMs refers to the ability to provide interpretable and understandable outputs that clarify how and why specific predictions or decisions are made. In politically sensitive applications, explainability ensures that stakeholders can trace model outputs to underlying reasoning processes, fostering trust and transparency. Interpretability is critical for validating insights derived from LLM analyses and ensuring fairness in decision-making for political science.

Definition of Causal Inference. Causal Inference is the process of identifying and understanding cause-andeffect relationships between variables. It goes beyond correlation by attempting to answer questions like "What caused this outcome?" or "What would happen if a specific intervention were applied?" In political science, causal inference is central to assessing the impact of policies, understanding voter behavior, and analyzing societal dynamics. LLMs offer new opportunities for causal inference tasks, enabling researchers to detect patterns, identify potential causal relationships, and generate counter-factuals.

One of the ultimate goals of science is to explain phenomena and uncover cause-and-effect relationships. In political science, causal inference plays a crucial role in understanding the impact of policies, campaigns, and social dynamics [156, 157, 158, 159]. While causal inference has been a focus in social and medical sciences [156], it has received comparatively less attention in computer science [156]. LLMs, with their remarkable capabilities in language generation and pattern recognition, provide new tools for enhancing causal inference. However, they also face significant limitations in moving beyond correlation to meaningful causal reasoning [273]. These challenges hinder their ability to provide deeper explanations of the phenomena they analyze, an essential requirement for advancing scientific understanding. Despite these limitations, recent research highlights the potential of LLMs to support causal inference-related tasks, providing tools for researchers to explore cause-and-effect relationships in innovative ways.

Explainability of LLMs in Political Science. The explainability of LLMs, referring to the ability to generate interpretable insights, directly impacts their utility in causal inference [164]. Researchers can leverage explainability tools, such as attention mechanisms [165] and prompt engineering [166], to identify relevant variables and interactions within data. For instance, post-hoc analysis methods [167] enable researchers to interpret why an LLM has generated specific outputs, facilitating the identification of potential causal pathways in text-based datasets. This capability enhances the transparency and reliability of LLM-driven causal analysis, especially in politically sensitive contexts.

Applications of LLM Causal Inference. Recent advancements demonstrate the potential of LLMs in identifying and modeling causal relationships. For example, LLMs have been utilized to detect causal patterns within large datasets, uncovering complex dependencies that traditional methods might overlook [159, 274]. By combining LLMs with domain expertise, researchers can identify key variables and interactions more effectively, leading to robust causal models. Another key application is the generation of counterfactual scenarios, which explore hypothetical outcomes under alternative conditions. LLMs can generate counterfactuals to assess the impact of different political policies or interventions, providing researchers with tools to test "what-if" scenarios [157, 160, 161]. Furthermore, LLMs have been employed to identify necessary and sufficient causes in controlled experimental settings, offering insights into the factors driving specific outcomes [159]. LLMs can also generate simulated datasets to evaluate causal inference methods. For instance, Gui and Toubi [162]

used LLMs to conduct between-subject experiments to assess treatment effects, while Wood et al. [163] evaluated causal estimation methods like propensity score matching and inverse propensity weighting using GPT-generated text data. These studies highlight the versatility of LLMs in creating experimental environments for testing and validating causal inference techniques.

Strengths and Limitations of LLMs in Causal Inference. One advantage of LLMs is their immunity to the carryover effect [275], which is a confounding factor in sequential human experiments, since each interaction can be reset to a neutral state. This feature allows researchers to isolate treatment effects without prior interactions influencing subsequent results [162]. Additionally, LLMs possess human-like abilities to generate causal graphs or extract background causal context from natural language [276], expanding their utility in tasks traditionally requiring human expertise [159]. However, the limitations of LLMs in causal inference remain significant. Critics argue that LLMs, trained on data where causal knowledge is embedded, often act as "causal parrots," merely reciting learned patterns without true causal understanding [158]. This lack of genuine reasoning raises concerns about over-reliance on LLM-generated causal insights. Moreover, unpredictable failure modes—such as inconsistencies when questions are framed differently—undermine the reliability of LLMs for causal inference tasks [159]. Ethical concerns, including potential misuse of causal findings in politically sensitive contexts [277], further complicate their deployment.

Summary and Challenges. LLMs hold significant promise for advancing causal inference in political science by enabling researchers to identify causal relationships, generate counterfactual scenarios, and simulate experimental data. Their unique capabilities, such as immunity to carryover effects and the ability to model causal contexts, make them valuable tools for exploring cause-and-effect relationships. However, limitations such as biases, inconsistent outputs, and ethical challenges must be addressed to ensure their effective application. As research continues, LLMs are poised to play an increasingly critical role in enhancing explainability and causal inference in the social sciences.

###### 4.5 Ethical Concerns in LLM Development and Deployment

General Concerns About Embedded Values in LLMs. Large language models are increasingly influencing societal and political discourse, raising fundamental questions about the values and biases they embed. The design and deployment of LLMs often involve implicit decisions about whose perspectives and moral frameworks are represented, potentially shaping public perception and decision-making in ways that are not always transparent. Johnson and Iziev [168] highlight the ethical dilemmas surrounding trust in AI-generated content, emphasizing the difficulty in ensuring that LLMs align with societal norms while avoiding the reinforcement of harmful biases. Similarly, Kim and Lee [169] examine the implications of LLM-driven conversational agents in political campaigns, noting the potential for these tools to inadvertently promote specific ideologies under the guise of neutrality. Lee et al. [170] further explore how LLMs reflect and propagate structural societal biases, particularly those affecting subordinate social groups. The study reveals that LLMs tend to portray these groups as more homogeneous, aligning with longstanding human cognitive biases, and underscores the importance of addressing such systemic issues in model training and evaluation. As LLMs continue to integrate into decision-making systems and public-facing applications, understanding their embedded values becomes imperative. This broad analysis sets the stage for more focused discussions on specific biases and potential mitigation strategies in subsequent sections.

Specific Manifestations of Biases and Preferences in LLM Outputs. The outputs of LLMs often reflect biases and preferences that manifest in specific, measurable ways, influencing how these models are perceived and utilized across different contexts. These manifestations not only reveal the underlying training data biases but also highlight the importance of careful model deployment. For instance, Tornberg [32] provides a comprehensive analysis of ChatGPT’s language use, showing how the model tends to favor Western-centric cultural norms and professional jargon. This skew has implications for accessibility and inclusivity, as it may alienate users from non-Western backgrounds or those with varying levels of language proficiency. In addition, Stanczak et al. [171] introduce a framework for quantifying biases in LLM outputs, with a focus on gender and occupational stereotypes. The study demonstrates that despite improvements in reducing overtly biased outputs, subtle biases persist, particularly in contexts where societal norms conflict with the training data distribution. Jiang et al. [172] also investigate how LLMs trained on community-specific data exhibit distinct preferences that align closely with the values and norms of those communities. While this approach can increase relevance

for specific audiences, it raises concerns about the potential for reinforcing echo chambers and ideological polarization when these models are used in broader contexts. The findings collectively illustrate the challenges of mitigating biases in LLM outputs, calling for more robust evaluation mechanisms and the inclusion of diverse training data to minimize the risk of harmful stereotypes or cultural insensitivity.

Practical Strategies for Mitigating Biases in LLMs. Efforts to address the biases embedded in LLMs have led to the development of various practical strategies. These approaches aim to minimize the harm caused by biased outputs while maintaining the utility of the models in diverse contexts. Recent studies provide valuable insights into how such strategies can be implemented effectively. Rozado [82] emphasizes the importance of balancing ideological representations within LLMs to mitigate political biases. The study outlines a method of systematically curating training datasets to ensure parity in the representation of diverse viewpoints. This proactive approach not only reduces overt political biases but also fosters fairness in politically sensitive applications, such as journalism and policymaking. Building on this, Motoki et al. [66] highlight the role of iterative fine-tuning using diverse feedback sources. By incorporating user feedback from underrepresented communities, LLMs can better align with a broader range of cultural norms and values. The findings in [66] suggest that this dynamic feedback loop significantly enhances model responsiveness to marginalized perspectives, making it a crucial step in real-world deployments. Simmons [173] takes a complementary approach by advocating for embedding explicit moral reasoning frameworks into LLM training pipelines. This strategy involves integrating ethical guidelines and decision-making frameworks into the model’s architecture. Simmons argues that such measures not only mitigate biases but also equip models with the capacity to navigate morally ambiguous scenarios, thereby improving trustworthiness in high-stakes applications. These efforts demonstrate that mitigating biases in LLMs is both technically achievable and ethically essential.

Broader Societal Implications of LLM Biases. The biases embedded in LLMs extend beyond technical and academic concerns, influencing societal structures and interactions in profound ways. As LLMs become increasingly integrated into decision-making processes, communication platforms, and personalized services, understanding their broader societal impacts is critical. Scholar like Tornberg [32] highlights how biases in LLMs can perpetuate existing social inequalities by reinforcing dominant narratives. The study examines ChatGPT’s performance in generating culturally sensitive responses, revealing disparities in the model’s treatment of various sociocultural groups. Tornberg argues that such imbalances risk entrenching systemic inequities, especially when LLMs are used in education, public discourse, and policymaking. Alvarez et al. [143] complement this analysis by exploring the role of generative AI in amplifying misinformation and political polarization. The study discusses how LLMs, if left unchecked, can contribute to the spread of ideologically skewed content, potentially exacerbating societal divisions. Alvarez emphasizes that biases in LLM outputs are not isolated technical flaws but are deeply intertwined with broader societal challenges, such as media manipulation and the erosion of public trust. Hackenburg and Margetts [174] extend these concerns to the realm of targeted advertising and political microtargeting. This study illustrates how biased LLMs can be leveraged to craft persuasive narratives tailored to specific demographics, raising ethical questions about manipulation and autonomy. Hackenburg warns that the misuse of biased language models in these contexts may deepen socioeconomic disparities and influence political outcomes in undemocratic ways. These studies highlight the importance of designing LLMs that are fair, transparent, and inclusive, particularly as they are increasingly applied in sensitive domains like political analysis and social sciences.

Summary and Challenges. The intersection of LLMs, societal values, and biases presents a complex but essential area of study. While advancements in LLMs enable transformative applications, their inherent biases pose significant ethical challenges. Addressing these challenges requires:

- • Awareness: Achieving a deeper understanding of how biases manifest in LLM outputs.
- • Accountability: Aligning LLMs with diverse societal needs under common ethical standards and guidelines.
- • Transparency: Building methods for identifying, monitoring, and mitigating biases in real-world applications.


Future research must prioritize creating robust methodologies for bias mitigation, with a focus on enhancing fairness, inclusivity, and accountability in LLM development and deployment [66, 82, 141, 173].

###### 4.6 Societal Impacts

Definitions and Context. The societal impacts of political-LLM sphere extend beyond technical concerns to encompass profound ethical, communicative, and informational implications. From influencing election outcomes to enhancing political communication, LLMs hold the potential to transform the societal landscape in both positive and negative ways. This section explores the multifaceted effects of LLMs on political campaigns, public communication, and civic engagement, while addressing potential risks and ethical challenges.

Transforming Political Campaigns. LLMs have revolutionized the way political campaigns are conducted by enabling hyper-personalized messaging and voter targeting [175, 174, 155, 176, 177]. [175] is an early work which highlights the potential of LLMs in measuring populism, nationalism, and authoritarianism through automated analysis of U.S. presidential debates. Hackenburg [174] demonstrates how LLMs can analyze large datasets to generate messages tailored to individual voter profiles, influencing voter perceptions and potentially altering election outcomes. Beyond voter engagement, LLMs play a strategic role in shaping campaign narratives that resonate with diverse audiences. Moghimifar et al.[155] show that LLM-based agents can model political coalition negotiations, providing insights into political alliances and enabling more dynamic campaign strategies. Foos [176] discusses how generative AI tools, including LLMs, are transforming election campaigns by facilitating AI-to-voter conversations and enabling scalable, multilingual interactions under diverse democracies. Lately, Yu et al. [177] propose a novel multi-step reasoning framework using LLMs for U.S. election predictions, incorporating time-sensitive factors like candidates’ policies and demographic trends to enhance accuracy. Together, these works showcase the multifaceted capabilities of LLMs in modernizing political campaigns and amplifying their impact across various dimensions.

Enhancing Political Communication In an era of increasingly complex political discourses, LLMs offer tools to bridge the gap between policymakers and the public [178, 143, 26, 75, 179]. By simplifying intricate political and legislative content, LLMs make critical information more accessible to citizens, fostering greater political understanding and participation. Argyle et al. [178] discuss how LLMs can distill party manifestos into understandable summaries, addressing barriers that often hinder public engagement. Similarly, Alvarez et al. [143] highlight the potential of generative AI to enhance transparency and comprehension in elections, allowing voters to make more informed decisions. These advancements suggest that LLMs could play a pivotal role in democratizing information and improving the accessibility of political communication.

Democratizing Information Access. LLMs hold the promise of empowering individuals by breaking down complex topics into easily understandable language, thereby democratizing access to information. This capability can foster a more informed citizenry and enable greater accountability among political actors. By providing equitable access to political knowledge, LLMs ensure that more people, regardless of educational background, can participate in democratic processes. For instance, LLMs can assist in translating political jargon or simplifying policy discussions, helping individuals navigate traditionally opaque political systems. This democratization of information will lead to a more inclusive political landscape.

Ethical Risks. While LLMs offer substantial benefits, their societal deployment also raises critical ethical concerns. One major issue is the potential misuse of LLMs to disseminate misinformation or biased content, which could manipulate public opinion or destabilize democratic processes. Bai et al. [278] discuss the persuasive power of LLM-generated text in influencing political opinions, underscoring the need for safeguards to mitigate risks. Furthermore, the ability of LLMs to generate realistic but misleading content poses challenges in distinguishing fact from fiction, creating vulnerabilities for misinformation campaigns. Addressing these ethical challenges require robust governance frameworks and continuous monitoring.

Summary and Challenges. The societal impacts of LLMs are vast and multifaceted, offering opportunities to enhance political communication while raising ethical and democratic concerns. To fully leverage the potential of LLMs while mitigating risks, future research and governance efforts must focus on:

- • Responsible Deployment: Establishing guidelines for the ethical use of LLMs in politically sensitive contexts.
- • Transparency: Developing tools to track and explain LLM-generated content to avoid misuse.
- • Public Awareness: Educating users about the benefits and potential risks of LLMs to promote informed and responsible decision-making.


- • Misinformation Prevention: Implementing safeguards to detect and counteract biased or false narratives.


By addressing these challenges, LLMs can contribute to a more equitable and transparent political environment, ensuring their societal impacts remain positive.

#### 5 Technical Foundations for LLM Applications in Political Science

###### 5.1 Benchmark Datasets

To meet the specific demands of political science applications, various benchmark datasets grounded in real-world data have been developed to evaluate LLMs on tasks such as sentiment analysis, election prediction, legislative summarization, misinformation detection, and conflict resolution. Each dataset is designed with domain-specific criteria to assess the alignment of LLM outputs with real-world political and social contexts, ensuring their relevance and applicability to practical scenarios. A comprehensive list of these datasets, along with their respective tasks and charactristics, is presented in Table. 3 to facilitate reference and comparison.

Sentiment Analysis & Public Opinion Dataset. Various datasets have been developed to accurately assess LLMs in sentiment analysis and public opinion. For instance, OpinionQA [50] is designed as a test environment where LLMs answer questions about public opinion, capturing subtle sentiments across 1,489 well-crafted queries. This dataset is valuable because it benchmarks how closely LLMs can align with actual human opinion patterns—a key factor for extracting sentiment accurately in social sciences. Similarly, PerSenT [180] focuses on tracking sentiments toward specific entities mentioned in news articles. It tests how well LLMs can detect and follow opinions expressed by particular individuals, allowing for sentiment to be aggregated over multiple mentions of popular entities to support comprehensive public opinion analysis. In addition, GermEval-2017 [181] provides a corpus of social media comments about Deutsche Bahn, the railway service in Germany, tailored for aspect-based sentiment analysis. This would help organizations and service providers derive actionable insights from feedback by homing in on specific aspects such as noise levels or punctuality. Datasets like Twitter [182], Bengali News Comments [183], and Indonesia News [184] extend the sentiment analysis to widely used social and news media platforms in multiple languages. These multilingual datasets are very important for cross-linguistic and cultural sentiment studies, which find specially relevant applications in global social media and market research.

Election Prediction & Voting Behavior Dataset. The U.S. Senate Statewide 1976-2020 [279] dataset contains state-level election returns, while the U.S. House 1976-2022 [280] dataset provides district-level returns, offering resources for analyzing nearly five decades of electoral trends. Other than that, The U.S. Senate Returns 2020 [185] and U.S. House Returns 2018 [186] datasets offer detailed precinct-level voting data, allowing LLMs to analyze U.S. voting patterns and voter behavior with the highest granularity, which supports election prediction and voting behavior studies. The State Precinct-Level Returns 2018 dataset [187], with its extensive 10 million data points, provides a substantial resource for LLMs to train on and analyze voting behaviors comprehensively. The 2008 American National Election Study (ANES) [188] offers insights into voter preferences and political attitudes through surveys conducted before and after the election, capturing difference in voter sentiment, which LLMs can model to reflect public opinion changes. The U.S. President 1976–2020 dataset [190] provides historical data essential for LLMs to examine long-term political trends and election outcomes across multiple decades. These datasets serve as invaluable training sources for LLMs to support political campaigns, media analysis, and social science research into electoral behaviors and trends.

Legislation & Administrative Rules Dataset. For summarizing and analyzing legislation and administrative rules, key datasets include BillSum [191], CaseLaw [192] and Federal Register [281]. BillSum aims at offering support to summarize US Congressional bills; it empowers LLMs to process mid-length legislative text and to produce brief summaries, which would considerably reduce the efforts of experts from the legal community and policy analysis. The CaseLaw dataset provides an extensive collection of state and federal cases, serving as a foundation for LLMs to analyze legal precedents and support judicial decision-making. The DEU III dataset [193] spans three decades of EU legislative decision-making, enabling the evaluation of LLMs in analyzing policy positions and negotiation dynamics among EU member states and institutions. Beyond legislation, the U.S. Federal Register dataset [281] includes titles and summaries of all final federal rules from 2000 to 2014,

Table 3: Existing benchmark datasets in LLM for Political Sciences.

Benchmark Datasets Application Domain Evaluation Criteria

OpinionQA Dataset[50] Sentiment Analysis & Public Opinion

Ability to answer 1,489 questions

PerSenT[180] Sentiment Analysis & Public Opinion

Performance on 38,000 annotated paragraphs

GermEval-2017[181] Sentiment Analysis & Public Opinion

Accuracy on 26,000 annotated documents

Twitter[182] Sentiment Analysis & Public Opinion

Analysis of 5,802 annotated tweets

Bengali News Comments[183] Sentiment Analysis & Public Opinion

Performance on 13,802 Bengali news texts

Indonesia News[184] Sentiment Analysis & Public Opinion

Sentiment analysis on 18,810 news headlines

U.S. Senate Statewide 1976-2020 [279]

Election Prediction & Voting Behavior

Analysis of 3,629 data points

U.S. House 1976-2022 [280] Election Prediction & Voting Behavior

Analysis of 32,452 data points

U.S. Senate Returns 2020[185] Election Prediction & Voting Behavior

Prediction accuracy on 759,381 data points

U.S. House Returns 2018[186] Election Prediction & Voting Behavior

Analysis of 836,425 data points

State Precinct-Level Returns 2018[187]

Election Prediction & Voting Behavior

Analysis of 10,527,463 data points

Analysis of 2,322 pre-election and 2,102 post-election surveys

2008 ANES Time Series Study[188]

Election Prediction & Voting Behavior

2016 ANES Time Series Study[189]

Election Prediction & Voting Behavior

Analysis of 2,322 pre-election and 2,102 post-election surveys

U.S. President 1976–2020[190] Election Prediction & Voting Behavior

Analysis of 4,288 data points

BillSum[191] Legislation & Administrative Rules

Summarization of 33,422 U.S. Congressional bills

CaseLaw[192] Legislation & Administrative Rules

Analysis of 6,930,777 state and federal cases

DEU III[193] Legislation & Administrative Rules

Performance on 141 legislative proposals and 363 controversial issues

Federal Register Final Rule Data 2000-2014[281]

Legislation & Administrative Rules

Titles and Summaries of 61,216 U.S. Federal Regulations

PolitiFact[194] Misinformation Detection Detection across six integrated datasets GossipCop[195] Misinformation Detection Detection across ten integrated datasets

Weibo[196] Misinformation Detection Classification of 4,488 fake news and 4,640 real news items

SciNews[132] Misinformation Detection Detection in 2,400 scientific news stories UCDP[197] Game Theory & Negotiation Analysis of armed conflicts and peace agreements PNCC[198] Game Theory & Negotiation Data on peace agreements and conflict resolution

WebDiplomacy[127] Game Theory & Negotiation Analyze 12,901,662 messages exchanged between players

focusing on administrative decisions. This dataset provides a valuable resource for LLMs to analyze regulatory trends and the decision-making processes of federal agencies.

Misinformation Detection Dataset. To address the negative effects of fake news and misleading information, several open-sourced datasets have been constructed [195, 196]. PoliFact [194] supports the use of large language models to distinguish between false and genuine news by focusing on publisher behavior, user interactions, and network structures. Similarly, SciNews [132] concentrates on misinformation in scientific reporting, providing a resource that helps preserve the integrity of science communication and limit the spread of misleading health and science information.

Game Theory & Negotiation Dataset. In the domain of conflict resolution and game theory research, there are datasets that guide the study of strategic interactions and peace negotiations. For example, the Non-State Actors in Armed Conflict (NSA) dataset [197] includes information on state-rebel group dyads, enabling more detailed examinations of conflicts with actor-specific data. In addition, the Peace Negotiations in Civil Conflicts (PNCC) dataset [198] documents formal negotiation phases during civil conflicts. Moreover, the WebDiplomacy dataset [127] consists of message exchanges between players in a simulated diplomatic negotiation setting, enabling a clearer understanding of communication patterns and strategic decision-making in conflict scenarios.

These benchmark datasets, taken together, provide a solid mainstay for a truly large number of LLMs applications in political science, from voter sentiment analysis to the exploration of legislative choices, tracking misinformation, and modeling conflict negotiations.

###### 5.2 Dataset Preparation Strategies

Dataset preparation is a critical step in adapting LLMs for downstream political science applications [282]. Given that the adaptation of LLMs in computational political science (CPS) is still in its infancy, the publicly available benchmark datasets remain scarce. The preparation of CPS datasets requires careful consideration of both domain-specific and generalizable strategies [283, 262]. Drawing insights from adjacent research fields like general sentiment analysis, fake news detection, and LLM-based dialogue generation, political datasets can be adapted to align with tasks such as election prediction, policy analysis, and political discourse generation.

Broad Source of Dataset Collection. One primary approach of dataset preparation involves collecting text data from publicly available political sources, such as speeches, legislative records, news articles, and social media platforms. For instance, in OpinionQA [50] and PerSenT [180], the data is sourced from political discussions and news media, which is then annotated for tasks like opinion alignment and sentiment detection. To ensure the data is relevant and representative, these dataset collections usually focus on specific political events, ideologies, or actors, which are essential for training LLMs to understand political discourse.

OpinionQA Dataset Generation

###### ④ Annotation and Labeling

###### ⑤ Final OpinionQA Dataset

###### ③ Pre-Processing and Formatting

① Publicly Available Data Source

###### ② Data Selection and Filtering

Comprehensive dataset of public opinions across demographics, suitable for training LLMs on politics.

Annotate questions based on demographics (e.g., age, political affiliation, ideology) to capture nuanced opinions.

Public political data sources (e.g., Pew Research ATP surveys, political speeches, news articles).

Identify relevant survey questions reflecting diverse viewpoints across political and social topics.

Convert responses into multiple-choice question format for consistency in OpinionQA.

![image 36](li-etal-2024-political-llm_images/imageFile36.png)

![image 37](li-etal-2024-political-llm_images/imageFile37.png)

![image 38](li-etal-2024-political-llm_images/imageFile38.png)

![image 39](li-etal-2024-political-llm_images/imageFile39.png)

![image 40](li-etal-2024-political-llm_images/imageFile40.png)

![image 41](li-etal-2024-political-llm_images/imageFile41.png)

![image 42](li-etal-2024-political-llm_images/imageFile42.png)

![image 43](li-etal-2024-political-llm_images/imageFile43.png)

![image 44](li-etal-2024-political-llm_images/imageFile44.png)

![image 45](li-etal-2024-political-llm_images/imageFile45.png)

Figure 5: Illustration of the OpinionQA dataset preparation on publicly available data source.

We elaborate the developing process of OpinionQA dataset in Fig. 5. To start with, researchers utilized publicly available data from various political and social surveys as the source data. They particularly leverage Pew Research’s American Trends Panel (ATP) surveys, which span a wide array of topics, including science, politics, and social issues. The dataset compilation process involves selecting pertinent survey questions that reflect diverse viewpoints across key issues and topics in the United States. These survey responses are preprocessed to create a multiple-choice question format, which serves as a reliable structure for language models to interpret. Through the methodology, each question in OpinionQA is annotated based on survey results, representing public opinion across various demographics such as age, political affiliation, income, and ideology. This

###### approach ensures that the dataset encapsulates the complexity and nuance of real-world opinions, which are essential for training language models to simulate and interpret politically charged discourse accurately.

Annotation Strategies. Annotation is another essential aspect of dataset preparation. Datasets intended for political sentiment analysis or misinformation detection require detailed labeling, often involving either expert or crowd-sourced annotations [199]. For instance, the State Precinct-Level Returns 2018 dataset [187] includes a substantial amount of real, unannotated data. Training LLMs with such data may involve adding annotations to capture sentiment toward political entities or identify media biases. Annotation schemes should be crafted to reflect nuanced political ideologies and opinions, ensuring that the dataset reflects the diversity and complexity of political discourse [200, 201].

Annotation Requirements

Repeat Job

![image 46](li-etal-2024-political-llm_images/imageFile46.png)

![image 47](li-etal-2024-political-llm_images/imageFile47.png)

![image 48](li-etal-2024-political-llm_images/imageFile48.png)

![image 49](li-etal-2024-political-llm_images/imageFile49.png)

![image 50](li-etal-2024-political-llm_images/imageFile50.png)

![image 51](li-etal-2024-political-llm_images/imageFile51.png)

Raw Dataset

![image 52](li-etal-2024-political-llm_images/imageFile52.png)

Annotation Quality Check

Ready-to-use Labeled Dataset

Y / N?

Annotation Expert

(a) Handicraft Labeling

Repeat Job

![image 53](li-etal-2024-political-llm_images/imageFile53.png)

Expert Intervention

Annotation Requirements

![image 54](li-etal-2024-political-llm_images/imageFile54.png)

![image 55](li-etal-2024-political-llm_images/imageFile55.png)

![image 56](li-etal-2024-political-llm_images/imageFile56.png)

![image 57](li-etal-2024-political-llm_images/imageFile57.png)

![image 58](li-etal-2024-political-llm_images/imageFile58.png)

![image 59](li-etal-2024-political-llm_images/imageFile59.png)

Raw Dataset

![image 60](li-etal-2024-political-llm_images/imageFile60.png)

Y / N? Ready-to-use

Annotation Quality Check

Auto-Labeling Algorithm

Labeled Dataset

As shown in Figure 6, annotation can be conducted through different approaches. These methods range from fully manual labeling [202], where annotation experts review and label the data by hand, to semiautomated processes that use algorithms to assist with labeling [284], with experts intervening as needed. In fully automated labeling, LLMs or other automated systems can handle the labeling work entirely, followed by a quality check [203]. Each method has its trade-offs among accuracy, scalability, and manual effort required.

(b) Semi-Automatic Labeling

Annotation Requirements

Repeat Job

![image 61](li-etal-2024-political-llm_images/imageFile61.png)

![image 62](li-etal-2024-political-llm_images/imageFile62.png)

![image 63](li-etal-2024-political-llm_images/imageFile63.png)

![image 64](li-etal-2024-political-llm_images/imageFile64.png)

![image 65](li-etal-2024-political-llm_images/imageFile65.png)

![image 66](li-etal-2024-political-llm_images/imageFile66.png)

![image 67](li-etal-2024-political-llm_images/imageFile67.png)

Raw Dataset

![image 68](li-etal-2024-political-llm_images/imageFile68.png)

![image 69](li-etal-2024-political-llm_images/imageFile69.png)

Automatic Quality Check

Ready-to-use Labeled Dataset

Y / N?

Large Language Models

(c) Fully Auto-Labeling

Figure 6: Dataset annotation approaches, including traditional manual approach, semi-automated approach, and LLM-based fully automated approach.

Dataset Bias and Representation. Addressing bias and representation is particularly crucial in political science datasets. Datasets must account for the diversity of political systems, ideologies, and demographics [204, 205]. Researchers must ensure the collected political datasets are balanced across different viewpoints and the data does not over-represent certain political ideologies. Techniques such as oversampling underrepresented groups or creating synthetic data using LLMs can be employed to achieve this balance [206, 207].

Data Preprocessing & Normalization. Given the complexity of political language, appropriate preprocessing and normalization are indispensable [285]. Preprocessing steps such as entity recognition, text cleaning, and the extraction of key political terms help standardize the input and improve the model’s ability to learn from diverse political contexts [286]. These techniques ensure that LLMs can process the input text effectively.

Data Augmentation. Augmentation strategies like paraphrasing or generating synthetic data with LLMs help to expand the dataset size in cases where political data is limited [208, 209]. Data augmentation helps diversify the training set, allowing the model to generalize better to new and unseen political scenarios [210, 211].

To further illustrate how these strategies applied to practical scenarios, we now introduce three examples of dataset preparation tailored for specific LLM-based political science tasks. Each example demonstrates how researchers effectively leverage LLMs to address key challenges in political data curation and annotation:

- (1) Developing a Dataset for LLM-Based Political Debiasing. For the political debiasing task, constructing a dataset involves curating a balanced collection of political texts that represent diverse political ideologies and viewpoints. For instance, to debias LLM outputs, we can gather news articles, social media posts, and political speeches from various political parties, regions, and ideologies. The dataset will need to be annotated with the political bias present in each text. This can be done using a combination of manual annotation by political experts and automated tools to identify biased language, sentiment, and framing. The goal is to provide a dataset that allows the model to recognize and mitigate its inherent biases by learning from a balanced set of inputs across the political spectrum.


- (2) Automated Annotation Using LLMs: Example in Legislative Interpretation. LLM-based legislative interpretation is a promising application in political science. Using a dataset like BillSum [191], which includes U.S. legislative documents, LLMs can be employed to automatically annotate sections of the legislation with relevant policy categories, key provisions, and political implications. LLMs can also be fine-tuned on a smaller, manually annotated set of legislative texts in order to classify different legal concepts and policy issues. This automated annotation streamline will accelerate the process of categorizing large volumes of legislative content, helping political analysts and lawmakers quickly interpret and summarize complex bills.
- (3) Generating Synthetic Political Datasets Using LLMs. The limitations in acquiring large and diverse political datasets due to privacy, restrictions, and sensitivities make generating synthetic datasets with LLMs a promising solution. Considering election prediction as an example, LLMs are able to generate hypothetical voter opinion surveys based on historical election data and known demographic trends. By training LLMs on existing public opinion survey datasets, researchers can generate synthetic datasets that simulate different electoral conditions, voter behaviors, and political trends. This approach will greatly enhance the availability of diverse political data for training and testing election prediction models.


###### 5.3 Fine-Tuning LLMs for Political Science

This subsection explores the fine-tuning of LLMs for political science applications, using Automatic Summarization of Legislation as the application task. Specifically, we employ BillSum dataset [220], which includes U.S. Congressional and California state bills, to fine-tune an LLM to generate concise, accurate summaries of legislative documents. This task highlights the challenges of summarizing complex, structured texts like bills, which differ significantly from conventional summarization domains.

Domain-Specific Dataset–BillSum. Curated datasets play a critical role in fine-tuning large language models [212], as they provide the domain-specific knowledge and tailored examples necessary to adapt the pre-trained LLM’s general capabilities to specialized applications [213, 214]. BillSum [220] is designed for the legislative summarization task, containing over 22,000 U.S. Congressional bills and summaries as well as additional California state bills as an out-of-domain test set. This dataset is particularly challenging due to the hierarchical and technical language structure of legislative texts [221]. BillSum’s structure enables us to focus on mid-length legislation and provides ground-truth summaries created by experts, making it ideal for training an LLM to handle specialized summarization tasks in the legislative domain [222].

Fine-Tuning Process for LLMs. Fine-tuning involves adapting a pre-trained LLM (e.g., Llama2) to the specific requirements of legislative summarization. The procedure includes the following steps:

- 1. Data Preprocessing: Legislative documents in BillSum must be preprocessed to create well-aligned input-output pairs suitable for text-to-text learning formats. For example, each bill text is paired with its corresponding summary, formatted to maintain structural consistency. Preprocessing may also involve tokenization adjustments and removal of excessive legal jargon that is irrelevant to summary generation.
- 2. Fine-Tuning Setup: To optimize fine-tuning, parameter-efficient techniques such as Low-Rank Adaptation (LoRA) [215] or prefix-tuning [216] are applied. These techniques adjust a minimal subset of model parameters, reducing computational costs and enabling the model to retain same level of accuracy while adapting to domain-specific context. Hyperparameters are carefully tuned based on summarization metrics like ROUGE and BLEU scores, which evaluate the accuracy and completeness of generated summaries [219].
- 3. Training Process: Training is conducted on GPU clusters to maximize performance, with techniques such as gradient accumulation [217] and mixed-precision [218] training to manage memory efficiently. The model iteratively adjusts its parameters by minimizing the loss function relative to the ground-truth summaries provided in the dataset. This involves several epochs with regular validation to prevent overfitting, ensuring the model generalizes well to unseen legislative texts.


Prompt Engineering for Fine-Tuning. Prompt engineering plays a crucial role in guiding the LLM to produce accurate and concise summaries that capture essential aspects of legislative texts. In fine-tuning, prompts are designed to clarify the task, structure the response, and focus the model on important content [115]. Below are examples of prompt structures that can be used in training with BillSum:

###### Prompt Engineering Examples for U.S. Legislative Summarization

: Prompt

❶: Read the following U.S. Congressional bill text and provide a summary that highlights the main objectives, intended outcomes, and any significant amendments.

❷: Summarize this bill in no more than 5 sentences, focusing on its primary goals and any actions it authorizes or mandates. Avoid technical jargon.

❸: Provide a legislative summary of the bill below, identifying the key provisions and any

departments or agencies involved. The summary should be clear and accessible to the general public. ❹: Using simple language, describe the main points of this bill, including what it aims to change, whom it affects, and any funds it allocates.

These prompts serve to guide the LLM towards generating summaries that are not only accurate but also accessible to a broader audience. By providing explicit instructions, these prompts help the model focus on the legislative document’s core components, such as goals, affected parties, and any key changes to existing laws.

Expected LLM Outputs. After fine-tuning, the LLM is expected to perform effectively across several legislative summarization tasks:

- • Summarization of Legislative Bills: Fine-tuned on BillSum, the model should generate coherent, concise summaries that capture the main objectives and impacts of U.S. Congressional bills. For example, the model might summarize a bill on environmental regulation by highlighting proposed restrictions, target pollutants, and enforcement mechanisms.
- • Generalization to Other Legislative Texts: Given BillSum’s inclusion of California state bills as an outof-domain test set, the fine-tuned model should also demonstrate the ability to generalize to state-level legislation, even when the language or structure differs from federal bills.
- • Summary Structure and Clarity: The fine-tuned model should produce summaries that are structured to facilitate understanding, ideally avoiding overly technical language or verbose descriptions. This includes providing summaries that are straightforward and tailored for readers without specialized legal knowledge.


Fine-tuning an LLM on the BillSum dataset enables the model to handle the complex task of legislative summarization. The process combines domain-specific fine-tuning with practical prompt engineering to ensure that the model generates accurate, concise, and accessible legislative summaries, thus enhancing transparency and efficiency in legal information dissemination.

###### 5.4 Inference with LLMs: Zero-Shot In-Context Learning

This subsection demonstrates how to practice Zero-Shot Learning (ZSL) in political science. We use Sentiment Analysis during the U.S. Presidential Election as the application case. Zero-shot learning enables a pre-trained LLM to perform sentiment analysis on political statements without additional task-specific training.

Overview of Zero-shot Learning (ZSL). ZSL enables pretrained LLMs to perform political science tasks without additional task-specific data or model updates [223, 105]. This approach is particularly valuable in computational political science (CPS) due to the frequent scarcity of annotated data [224]. By leveraging extensive pretraining on general-purpose data, ZSL allows LLMs to infer political language patterns through context, making it possible to analyze sentiment [224], classify ideology [225], or interpret complex policy discourse [226] directly from raw prompts.

Task-Specific Prompt Engineering. Effective prompt engineering is essential to guide the LLM accurately in zero-shot mode [228]. In the case of U.S. Presidential Election sentiment analysis, prompts must be designed to capture the nuances of political statements and infer the sentiment accurately [229, 230]. Here are practical

examples of sentiment classification prompts, using statements from publicly available news articles or social media posts regarding the 2024 election.

###### Public Opinion Poll Sentiment Classification during U.S. Presidential Election

: Prompt : LLM response : Explanation

: Analyze the sentiment of the following statement about the presidential election as Positive, Negative, or Neutral. "Despite the turbulent political climate, Candidate X has shown strong leadership qualities and promises substantial reforms that could benefit the economy." : Positive.

: The statement uses phrases such as :"strong leadership" and "substantial reforms," indicating a positive sentiment towards Candidate X’s potential economic impact.

Another example tailored for analyzing public opinion on social media:

###### Social Media Sentiment Analysis for U.S. Presidential Election

: Prompt : LLM response : Explanation

: Determine whether the sentiment expressed in this tweet about Candidate Y in the upcoming election is Positive, Negative, or Neutral. "Candidate Y’s policies on healthcare are exactly what we need! Finally, someone who cares about the people." : Positive.

: The tweet expresses approval through phrases like "exactly what we need" and "cares about the people," signaling positive support for Candidate Y’s healthcare policies.

These prompts are structured to guide the LLM in accurately detecting sentiment by highlighting specific phrases and context, improving the reliability of sentiment classification in a zero-shot setting.

Embedding Context in Prompts. Including contextual information is crucial for ZSL tasks, especially in political sentiment analysis, where statements often depend on the socio-political context [231]. For example, prompts can specify details such as the speaker’s political affiliation, the event’s date, or relevant policy areas. This helps the model interpret statements with greater accuracy. In politically charged scenarios, prompts might include contextual cues, like "This statement was made during a recent debate on immigration policy," enabling the model to better understand the sentiment nuances within the political context.

Applications in Political Science. ZSL has broad applications across political science tasks. In addition to sentiment analysis, ZSL enables stance classification, allowing LLMs to determine whether a statement supports or opposes a particular issue without task-specific data. This approach also extends to policy categorization and ideological scaling, where LLMs can classify political statements or documents into ideological categories, such as conservative, liberal, or centrist, without extensive labeled data. By eliminating the need for annotated datasets, ZSL enables LLMs to quickly adapt to exploratory political science tasks, making it a flexible, cost-effective option for rapid analysis.

Use Case: Sentiment Analysis in the U.S. Presidential Election. As a demonstration, we apply zero-shot sentiment analysis to analyze public opinion during the 2024 U.S. Presidential Election [228, 45]. By leveraging Llama2, we perform sentiment classification on statements from news articles, debate transcripts, and social media posts, enabling us to gauge public sentiment toward candidates and their policies without requiring fine-tuning on election-specific data.

ExamplePromptforSentimentAnalysis. Thefollowingpromptisdesignedtoassesssentimentonelection-related statements, guiding the LLM to infer the sentiment based on contextual knowledge:

###### Political Sentiment Analysis in 2024 U.S. Election

: Prompt : LLM response : Explanation

: Evaluate the sentiment in the following statement about the presidential election (Positive, Negative, or Neutral). "The recent tax proposal from Candidate X is likely to hurt middle-class families while favoring large corporations." : Negative.

: The sentiment is negative due to phrases like "hurt middle-class families" and "favoring large corporations," which indicate disapproval of Candidate X’s tax proposal.

This prompt helps the LLM capture sentiment indicators in election-related contexts, such as impacts on specific social groups or policy critiques [287]. By structuring prompts carefully, ZSL can facilitate nuanced sentiment analysis on real-world political data.

In summary, ZSL enables effective and efficient sentiment analysis of political statements during key events (e.g., presidential elections). With the use of prompt engineering to provide clear task instructions and context, ZSL can support political science research by rapidly assessing public sentiment, ideology, and stance [233] without needing additional training data, making it an invaluable tool in data-scarce political environments.

###### 5.5 Inference with LLMs: Few-Shot In-Context Learning

Overview of Few-shot Learning. Few-shot learning allows LLMs to perform specialized tasks with minimal labeled data by embedding a small number of example prompts within the input. This approach bridges the gap between zero-shot and full fine-tuning by enhancing the model’s contextual understanding through example-driven cues. [230, 228] Few-shot learning is particularly beneficial in political science applications where obtaining annotated data can be challenging and costly [227], providing a flexible, cost-effective solution.

Designing Effective Few-shot Examples. The effectiveness of few-shot learning heavily relies on the selection of representative examples [229, 230]. For the task of fake news detection in the 2024 U.S. Presidential Election, it is critical to include examples that capture various degrees of misinformation subtlety and diversity in topics [234]. These examples should reflect the language and tactics often used in fake news, such as sensationalism, partial truths, and emotionally charged language [235]. Below is a sample prompt designed to guide the model in distinguishing real news from fake news.

Determine if Each News Headline is Real or Fake : Corpus database : Label : Prompt : LLM response

: "Presidential candidate X pledges new economic reforms to boost national job growth and reduce unemployment."

: Real. : "Urgent: Voting machines in <Swing State> are flipping votes from Candidate X to Candidate Y, claims anonymous election officer."

: Fake.

: "Scientists confirm presidential candidate X is involved in alien cover-up." : ...............

This prompt helps the model understand distinctions between credible and misleading information by using a mix of realistic and exaggerated statements. Examples like "foreign interference" or "alien cover-up" are designed to train the model to recognize patterns typical of fake news narratives.

Embedding Context in Prompts. Contextual cues are essential in few-shot learning for politically sensitive tasks. For instance, when detecting fake news during the 2024 U.S. Presidential Election, prompts can be enhanced by adding details such as the publication date or the source of the statement [137]. This contextual embedding helps the model assess the plausibility of a statement more accurately. Specifying that a statement originated from a reliable media versus an anonymous social media post can guide the model’s judgment [288].

###### Example with contextual Cues for Fake News Detection during the U.S. Presidential Election : Corpus database : Label : Prompt : LLM response

: "Presidential candidate X states that billions of taxpayer dollars are wasted annually on benefits for illegal immigrants. X pledges to end these benefits and redirect the funds to support hardworking American taxpayers."

: Real. : "CNN, The New York Times, and The Washington Post report historic voter turnout in early voting during the 2024 U.S. Presidential Election."

: Real.

: "Unconfirmed sources suggest presidential candidate plans to abolish social security if elected." : ................

In this prompt, contextual cues like "CNN, The New York Times, and The Washington Post" and "Anonymous social media account in TikTok" help the model make more informed predictions. Adding such cues aids the model in understanding the credibility of the information, which is crucial for politically charged topics.

Balancing Prompt Length and Example Diversity. In few-shot learning, the balance between prompt length and example diversity is critical [232]. While additional examples can improve task performance, including too many can reduce prompt clarity and increase processing time [237]. For fake news detection, three to four carefully chosen examples are typically sufficient to cover different levels of misinformation and factual reporting styles. Examples should be concise yet comprehensive, representing a variety of fake news tactics, such as sensationalism, misinformation about election logistics, or fabricated scandals.

Use Cases in Political Science. Few-shot learning has proven effective across various political science tasks. In the context of Fake News Detection for the 2024 U.S. Presidential Election, few-shot learning helps LLMs identify misleading narratives without extensive training data [228], making it particularly valuable for real-time misinformation monitoring [236]. Other applications include:

- • Public Opinion Analysis: By using few-shot examples of sentiment-laden statements, LLMs can analyze public opinion towards candidates or policies, which enables to capture nuanced shifts in voter sentiment.
- • Policy Stance Classification: With carefully crafted few-shot examples, LLMs can classify political statements as supportive or oppositional towards specific policies, helping understand public responses.
- • Legislative Influence Prediction: Few-shot learning can help predict the likelihood of legislative support or opposition by providing examples of previous legislative behavior and context, assisting analysts in forecasting policy outcomes.


Few-shot learning’s adaptability makes it an invaluable tool in political science, allowing for nuanced understanding and classification in tasks with limited data. By incorporating diverse, context-rich examples, fewshot learning enables LLMs to navigate complex political discourse with improved accuracy and interpretability, as exemplified by its application in fake news detection during a high-stakes election cycle.

###### 5.6 Other Techniques Enhancing LLM Inference

Retrieval-Augmented Generation (RAG). RAG is a powerful technique that combines knowledge retrieval with text generation to enhance the relevance and accuracy of responses produced by large language models [94]. Unlike standard language models that rely solely on pre-trained knowledge, RAG systems dynamically retrieve external data from a knowledge source (such as a database or corpus) to enrich the model’s responses [238]. This method mitigates the limitations of static knowledge in LLMs, ensuring that generated content is both up-to-date and contextually aligned with real-world events [239]. In the context of political science, RAG is particularly valuable for tasks that require accurate, real-time information, such as policy analysis, electoral forecasts, and sentiment tracking [240, 240]. By integrating recent polling data, legislative updates, or public opinion trends, RAG enables LLMs to respond to complex political questions with greater precision. This capability is essential for informed analysis and decision-making.

In the 2024 U.S. presidential election polling scenario, RAG is employed to provide real-time and contextually accurate responses about the latest public opinion data. As shown in Figure 7, when users pose a question "What are the latest polling results for the 2024 U.S. Presidential election?", the RAG system initiates a two-step process. First, the retriever component accesses an up-to-date knowledge database containing polling data, including support rates for each candidate in key states and national trends from reputable sources like Gallup and the Pew Research Center. This retrieved data is then incorporated into the context, which includes specific figures and observations about fluctuating support levels, particularly in critical states such as Pennsylvania and Michigan. Next, the LLM uses this enriched context to generate a coherent response, producing an answer that not only addresses the user’s question but also reflects the most current information available. RAG is capable of integrating retrieval with generation, enabling LLMs to provide responses that are both timely and grounded in factual data, which is especially valuable in politically dynamic fields where data changes rapidly.

Answer: Candidates A and B are closely matched in key states, with A slightly leading. Notable fluctuations in support are observed for A, especially in Pennsylvania and Michigan.

User question: What are the latest polling results for the 2024 U.S. Presidential election?

![image 70](li-etal-2024-political-llm_images/imageFile70.png)

![image 71](li-etal-2024-political-llm_images/imageFile71.png)

![image 72](li-etal-2024-political-llm_images/imageFile72.png)

Users

###### Input Output

Context: The latest poll shows Candidate A leading in key states ahead of Candidate B...... Data from key states suggest fluctuations for Candidate A...... Question: What are the latest polling results for the 2024 U.S. Presidential election? Please generate a brief summary based on the context.

![image 73](li-etal-2024-political-llm_images/imageFile73.png)

![image 74](li-etal-2024-political-llm_images/imageFile74.png)

![image 75](li-etal-2024-political-llm_images/imageFile75.png)

Retriever LLM

Retrieve

![image 76](li-etal-2024-political-llm_images/imageFile76.png)

The latest poll shows Candidate A leading in key states with a 48% support rate, ahead of Candidate B’s 46%. Recent national polls indicate an increase in B’s support, reaching 47%.

Data from key states suggest fluctuating support for Candidate A, particularly in Pennsylvania and Michigan.

###### Collect

![image 77](li-etal-2024-political-llm_images/imageFile77.png)

![image 78](li-etal-2024-political-llm_images/imageFile78.png)

![image 79](li-etal-2024-political-llm_images/imageFile79.png)

![image 80](li-etal-2024-political-llm_images/imageFile80.png)

![image 81](li-etal-2024-political-llm_images/imageFile81.png)

![image 82](li-etal-2024-political-llm_images/imageFile82.png)

![image 83](li-etal-2024-political-llm_images/imageFile83.png)

###### Internet

Knowledge Database

- Figure 7: Illustration of retrieval-augmented generation techniques on U.S. Presidential Election analysis.


Chain-of-Thought Reasoning Chain-of-Thought (CoT) reasoning is a technique that guides LLMs through a step-by-step logical reasoning process, allowing the model to handle complex, multi-step analysis [241]. It simulates a structured human-like thought process, reducing the risk of oversimplification or bias in sensitive analysis. CoT reasoning is particularly valuable for political science tasks that require nuanced and multidimensional insights [242, 243]. By breaking down intricate questions into a sequence of simpler reasoning steps, CoT helps LLMs interpret complex political issues with greater accuracy and transparency [244].

Considering a practical application of CoT reasoning in analyzing public opinion trends on a contentious policy, such as immigration reform. In this example, the objective is to predict the level of public support or opposition to a new immigration policy by examining multiple influencing factors in a sequential and structured manner. The reasoning process is proceed as follows:

- 1. Historical Context Analysis: The model first retrieves information on past immigration policies and public responses to them. This includes identifying previous legislative actions on immigration and analyzing public opinion data from those periods. By understanding historical trends, the model establishes a baseline for comparison with the current policy.
- 2. Demographic Impact Assessment: Next, the model assesses demographic shifts that might influence public opinion, such as changes in immigrant populations, regional population density, and employment statistics in sectors affected by immigration. This step allows the model to evaluate how different demographic groups might respond to the policy.
- 3. Social Sentiment Analysis: The model then analyzes recent public sentiment data from social media, news articles, and survey results. By focusing on keywords and sentiment trends related to immigration reform, the model identifies the prevailing attitudes and emotional responses of the public. This step is crucial for capturing real-time opinions.
- 4. Economic Implications: The model evaluates potential economic effects of the policy, including its impact on labor markets, public spending, and economic growth. It considers both supportive and opposing viewpoints on the economic consequences of immigration reform. This analysis provides additional context for understanding why different groups may support or oppose the policy.
- 5. Synthesis and Prediction: Finally, the model synthesizes information from each step, combining historical, demographic, social, and economic insights to produce a comprehensive assessment of public opinion on the immigration reform policy. By sequentially reasoning through each aspect, the model generates a nuanced prediction of public support levels.


Through this step-by-step process, CoT reasoning enables the LLM to build a well-rounded understanding of public opinion trends. Each reasoning step enriches outputs, allowing the LLM to incorporate multiple facets of the issue and providing an interpretable chain of logic. This structured approach is ideal for complex political science tasks where multiple factors interact dynamically.

Knowledge Editing. It is a technique that allows for dynamic modification of the internal knowledge within an LLM without requiring full retraining [62]. Knowledge Editing is highly feasible for political scenarios, where information, contexts, and factual data frequently changes. Instead of retraining the LLM, Knowledge Editing enables targeted updates to specific knowledge nodes or parameters within the model [245, 246]. This characteristic allows the LLM to provide accurate responses to questions related to recent political events, policy changes, or updated facts, thus ensuring the model outputs remain relevant and reliable.

Knowledge Editing can be applied to update an LLM’s understanding of specific policies or adjust its responses concerning historical events [247, 248]. For instance, while researchers are analyzing an LLM’s perspective on climate policies, the government introduces a new climate reduction target. Using Knowledge Editing, researchers can embed this new target directly into the LLM without a full-scale retraining. The process involves identifying the specific model parameters or representations tied to "climate policy" or "emission targets" and then modifying these nodes to incorporate the latest data. This targeted update ensures that the LLM refers to the updated policy goals when generating content about climate initiatives.

Self-Consistency Decoding. This approach is designed to improve the reliability and robustness of responses generated by LLMs [249]. The basic idea behind Self-Consistency Decoding is to prompt the model multiple times with slightly varied initial conditions, allowing it to generate multiple candidate responses [250]. These responses are then evaluated, and the most frequent or consistent response is selected as the final output [251]. This method is particularly useful in reducing the effects of randomness in model generation, which can often lead to inconsistent or contradictory answers, especially in complex domains like political science. In political science applications, Self-Consistency Decoding can help stabilize the outputs of LLMs, ensuring that responses are not only accurate but also align consistently with established political theories or interpretations.

In political science tasks, Self-Consistency Decoding can be applied to analyze and interpret contentious or nuanced topics, such as public opinion on controversial policies [252]. For example, the LLM is prompted to analyze sentiments around immigration reform across different demographic groups. By asking the LLM to generate multiple analysis of the same policy, each with slight variations in prompt wording or contextual details, researchers can obtain a set of responses that capture different perspectives or interpretations. Self-Consistency Decoding is then used to identify the dominant perspective or interpretation. This approach not only enhances the robustness of LLM-generated insights but also helps researchers ensure that the final output reflects a consensus interpretation, minimizing the risk of bias or instability in model-generated analyses.

###### 5.7 Case Study: Political Bias and Feature Generation in LLM-Driven Voting Simulations

As mentioned in Section 4.5, previous studies have shown that LLMs may exhibit potential political bias. To effectively quantify and evaluate this bias, we conducted a case study based on the benchmark dataset referenced in Section 5.1. This study aimed to address two key aspects: (1) the biases displayed by different LLMs during voting simulation, and (2) the quality of LLM-generated political features compared to the original dataset, assessing their effectiveness for feature generation tasks in political science.

###### 5.7.1 LLM Model Configurations, Computational Resources, and Dataset Selection

We evaluated four LLMs with varying parameter sizes: two commercial models, GPT-4o [253] and GPT-4omini [254], and two open-source models, Llama 3.1 8-B [255] and Llama 3.1-70B [256].

The hardware configurations were tailored to meet the computational requirements of each model. For GPT-4o and GPT-4o-mini, experiments were conducted on a GPU server equipped with an AMD EPYC Milan 7763 processor, 1 TB of DDR4 memory, 15 TB SSD storage, and 6 NVIDIA RTX A6000 GPUs. For Llama 3.1 models, a node with 8 NVIDIA A100 GPUs (each with 40 GB of memory), dual AMD Milan CPUs, 2 TB of RAM, and 1.5 TB of local storage was utilized.

The dataset used in this study was the 2016 Time Series Study from the American National Election Studies (ANES) [257, 258]. This dataset was selected for its comprehensive demographic, political ideology, and religious data, which provided a robust basis for analyzing the potential biases and generative capabilities of LLMs in a political science context.

###### 5.7.2 Experimental Design and Evaluation Methods

Experimental Design. To investigate voting simulation bias and feature generation quality, we adapted methodologies proposed in previous studies [189, 259]. In our experimental design, each selected LLM is provided with detailed persona information, including demographic characteristics, political ideology, and religious affiliation, as well as contextual information on candidates and policies relevant to the election year. Each LLM is then employed to simulate election voting behavior for each persona, allowing us to observe any biases that emerged in the simulated vote distributions [177].

We designed two experimental pipeline setups for each LLM: a baseline group (denoted as [model name]-base) and a generation group (denoted as [model name]-gen). In the base group, LLMs used the original, unaltered ANES dataset inputs to simulate voting behaviors. In the generation group, we applied a multi-step Chain of Thought (CoT) approach, as described in Section 5.6. Here, LLMs were first prompted to generate political ideology features based on demographic inputs. These generated features were then combined with other persona details and used as inputs for the final voting simulation. This two-pipeline design allows us to evaluate the capability of these LLMs in generating relevant features within a political science context. Additionally, it enables us to analyze how these generated features might influence the bias in LLM voting simulations. The following popular general-purpose LLMs are selected as the benchmark models for our experiments: (I) gpt4o-mini-base, (II) gpt4o-base, (III) llama3.1-8B-gen, (IV) gpt4o-mini-gen, (V)gpt4o-gen, (VI) llama3.1-70B-base, (VII) gpt4o-NP, (VIII) llama3.1-8B-base, (IX) llama3.1-70B-gen.

The specific CoT design is illustrated with the following example prompts:

###### Case study - CoT Prompts example

- Step 1: Ideology Assessment. You are a persona with the following demographic characteristics: [demographics]. The current year is [year]. Here are the policy agendas of the two parties: [Two parties’ policy agenda]. When it comes to politics, would you describe yourself as:

No answer & Very liberal Somewhat liberal & Closer to liberal Moderate & Closer to conservative Somewhat conservative & Very conservative

- Step 2: Voting Simulation. You are a persona with the following demographic characteristics: [demographics]. Your political ideology is described as [conservative-liberal spectrum]. The current year is [year]. Here are the policy agendas of the two parties: [Two parties’ policy agenda]. Additionally, here are the presidential candidates’ biographical and professional backgrounds: [Presidential candidates’ biographical and professional backgrounds]. Based on this information, please answer the following question:


1. As of today, will you vote for the Democratic Party (Hilary Clinton), the Republican Party (Donald Trump), or do you have no preference?

- • Democratic
- • Republican
- • No Preference


Evaluation Criteria. We design two different evaluation criteria to evaluate the bias in voting simulation and the quality of feature generation. For voting simulation, we calculate the ratio: R = Republican VotesRepublican Votes+Democratic Votes and compared the LLM-generated simulation results with actual outcomes from the 2016 American National Election Studies (ANES) dataset [257].

To evaluate feature generation, we constructed specific metrics for each LLM by comparing the generated political ideology features with the original ANES 2016 features. In each matrix, the x-axis represents the original political ideology as recorded in the ANES 2016 dataset, while the y-axis represents the political ideology features generated by different LLMs based on contextual information. The numbers 1 to 7 correspond to "Very Liberal," "Somewhat Liberal," "Closer to Liberal," "Moderate," "Closer to Conservative," "Somewhat Conservative," and "Very Conservative," respectively. These metrics provide a direct and quantitative comparison of model-generated outputs against ground truth, enabling us to assess the alignment and reliability of LLM predictions in the context of political science.

###### 5.7.3 Results Analysis and Performance Comparison

The analysis focuses on two key aspects: (1) the biases exhibited by LLMs in voting simulation [260, 204], and (2) LLMs’ performance in feature generation [261, 48, 70]. To provide a robust basis for evaluation, the ratio of party affiliation (e.g., Republicans to Democrats) is predicted based on samples from the 2016 ANES dataset. Each observation in the ratio corresponds to an individual voter with specific demographic and ideological labels derived from ANES. This setup ensures that the simulated voting distributions align with the demographic and political tendencies reflected in the ANES sample, providing a reliable benchmark.

Illustration of Voting Simulation Results. Figure 8 presents the voting simulation results across four models and eight pipeline variations on the 2016 benchmark dataset. Previous studies have shown that LLMs inherently possess political biases and that political features can mitigate these biases to some extent. To further illustrate this mitigation, we added an additional control group for GPT-4o, in which the model performed voting simulation on the ANES dataset without any political features. This yielded a total of nine results for comparison. Findings indicate that larger models, such as GPT-4o and Llama 3.1-70B, produced predictions closely aligned with the ground truth baseline of 47.7% across both the baseline and generation pipelines. However, when political features were removed, GPT-4o displayed a significant skew towards the winning party of the 2016 election, highlighting the role of political features in bias correction. In contrast, smaller models displayed varied performance. GPT-4o-mini achieved similar accuracy to the larger models when using the original data but showed a pronounced skew towards the winning party in the 2016 election. Consistent with

findings from prior studies [123], Llama 3.1-8B exhibited a tendency to avoid responses favoring Republican positions while being more permissive of responses supporting Democratic positions.

gpt4o-base gpt4o-gen llama3.1-8B-base

gpt4o-mini-base gpt4o-mini-gen gpt4o-NP

![image 84](li-etal-2024-political-llm_images/imageFile84.png)

llama3.1-8B-gen llama3.1-70B-base llama3.1-70B-gen

0.8

70.26%

0.7

66.38%

Reference Line (0.5) Ground-Truth ANES 2016 Ratio (0.477)

Ratio (R / (R + D))

0.6

47.35%

46.84% 48.34%

47.79% 47.67%

0.5

38.28%

0.4

35.72%

0.3

0.2

0.1

0.0

LLMs Voting Simulation on ANES 2016 Benchmark

- Figure 8: The "base" labels represent the simulation results of different models using the complete ANES dataset features, while the "gen" labels represent results obtained by generating political ideology through the Chain of Thought approach and subsequently using the generated features for simulation. Additionally, "gpt4o-NP" denotes the simulation results of GPT-4o on the ANES dataset with political features removed. The red dashed line indicates the actual ratio derived from the 2016 ANES dataset, while the black dashed line represents the 50% half-and-half reference point.


Comparison on Feature Generation Quality. In empirical surveys, missing or corrupted features are a persistent challenge, which makes the ability of LLMs to generate robust and accurate features particularly significant. For feature generation evaluation, Figure 9 highlights clear differences in generation capability across nine general-purpose LLMs. Specifically, GPT-4o and Llama 3.1-70B demonstrated higher generation quality, with their generated political ideology distributions closely matching those of the original ANES features. In Figure 9, the size of each circle represents the relative quantity of data points, and we can observe that the majority of generation clusters for the larger models are concentrated along the diagonal line, indicating better alignment with the true feature distributions. In contrast, smaller models, such as GPT-4o-mini and Llama 3.1-8B, exhibited limited generation capabilities. Regardless of persona-specific features, these models consistently generated political ideologies aligned with the 2016 winning party, suggesting a limitation in their ability to accurately reflect diverse political perspectives. Besides, the pie charts summarize the proportion of responses in the feature generation process that were not labeled as "No Answer." GPT-4o and Llama 3.1-70B demonstrated high response rates of 99.8% and 99.6%, respectively. In contrast, smaller parameter models had relatively lower response rates, with GPT-4o-mini at 96.9% and Llama 3.1-8B at 92.6%.

Additionally, Figure 9 reveals some interesting insights regarding the ANES dataset itself. The color of the circles indicates the party identification of respondents, with red representing Republicans and blue representing Democrats. Notably, within the matrices, it can be observed that some respondents self-identified as strongly liberal but were registered as strong Republicans (represented by red circles located on the left side of the graph, where 𝑥 < 4). Such inconsistent clusters highlight underlying inconsistencies in the dataset, which may influence model outcomes and suggest certain limitations in data collection practices. In Section 6, we will further explore these potential challenges and discuss directions for future work.

![image 85](li-etal-2024-political-llm_images/imageFile85.png)

![image 86](li-etal-2024-political-llm_images/imageFile86.png)

gpt-4o Generated vs. Actual Ideology

Llama-3.1-8B Generated vs. Actual Ideology

LLM Generated Political Ideology

- 0
- 1
- 2
- 3
- 4
- 5
- 6
- 7


- 0
- 1
- 2
- 3
- 4
- 5
- 6
- 7


Very Conservative

Moderate

Very Liberal

0 1 2 3 4 5 6 7

0 1 2 3 4 5 6 7 Original ANES 2016 Political Ideology Original ANES 2016 Political Ideology

gpt-4o-mini Generated vs. Actual Ideology Llama-3.1-70B Generated vs. Actual Ideology

LLM Generated Political Ideology

- 0
- 1
- 2
- 3
- 4
- 5
- 6
- 7


- 0
- 1
- 2
- 3
- 4
- 5
- 6
- 7


Very Conservative

Moderate

Very Liberal

0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7

Original ANES 2016 Political Ideology Original ANES 2016 Political Ideology

###### LLMs' Answer Rate on Feature Generation

###### Detailed Illustration

gpt-4o Generated

Llama-3.1-8B Generated

![image 87](li-etal-2024-political-llm_images/imageFile87.png)

![image 88](li-etal-2024-political-llm_images/imageFile88.png)

![image 89](li-etal-2024-political-llm_images/imageFile89.png)

![image 90](li-etal-2024-political-llm_images/imageFile90.png)

Cluster with more Points

Cluster with less Points

gpt-4o

-mini Generated Llama-3.1-70B Generated

![image 91](li-etal-2024-political-llm_images/imageFile91.png)

![image 92](li-etal-2024-political-llm_images/imageFile92.png)

![image 93](li-etal-2024-political-llm_images/imageFile93.png)

![image 94](li-etal-2024-political-llm_images/imageFile94.png)

Identified as Strong Democrat Identified as Independent Identified as Strong Republican

![image 95](li-etal-2024-political-llm_images/imageFile95.png)

Original Party

Identification from ANES 2016 Dataset

###### Figure 9: The figure contains four 7x7 feature comparison matrices, corresponding illustrative diagrams, andfour pie charts to evaluate the quality of feature generation by different LLMs in the field of political science.

#### 6 Future Directions & Challenges

###### 6.1 Pipelines of Integrating Political Science with LLMs

The integration of LLMs into political science research pipelines offers transformative opportunities, but it also presents several challenges. LLMs excel at automating tasks like policy analysis, election forecasting, and legislative summarization, yet adapting these general-purpose models to the nuanced demands of political science remains difficult.

A significant challenge lies in LLMs’ contextual understanding of domain-specific constructions, such as ideology, stance, and policy framing [57]. To address this issue, future works must prioritize domain-adaptive pre-training or fine-tuning strategies that enhance LLMs’ ability to process political texts effectively. In addition, hybrid workflows that combine LLM outputs with human expertise should be developed to ensure both reliability and interpretability [73].

Modularized Pipelines. These pipelines are designed to decompose complex research tasks into manageable sub-components, each optimized for specific objectives, offering a promising solution to address the challenges. For instance, in election forecasting, a pipeline can include separate modules for data preprocessing (e.g., cleaning polling data and demographic information), contextual understanding (e.g., analyzing regional voting patterns), and predictive modeling (e.g., projecting voter turnout or swing state dynamics). Similarly, for legislative analysis, distinct modules can be employed to handle sub-tasks such as summarizing legal texts, extracting key policy themes, and evaluating potential societal impacts.

Pipeline integrated with Retrieval-Augmented Generation. Another promising approach is the integration of RAG into political science pipelines. RAG combines LLMs with external knowledge retrieval systems, enabling the dynamic incorporation of up-to-date and domain-specific information from political datasets, government databases, or news sources [289, 94]. This method ensures that the model outputs remain contextually relevant, even in rapidly evolving political environments where timeliness is critical. For instance, in policy analysis, a RAG-based pipeline could retrieve recent legislative updates or party manifestos to supplement the LLM’s generative capabilities, improving both accuracy and depth of insights.

###### 6.2 Data Scarcity and the Construction of Domain-Specific Datasets

Data scarcity remains a significant challenge in computational political science (CPS), especially when utilizing LLMs that rely on extensive, high-quality labeled data for effective performance. Unlike computer vision or general NLP, political science lacks large-scale, domain-specific datasets tailored for nuanced tasks such as election behavior modeling, legislative sentiment analysis, or policy framing studies. This limitation hinders the ability of LLMs to fully capture the complexity of political language and context, leading to inaccuracies or biases in model outputs. Furthermore, the dynamic nature of political discourse and the emergence of new events exacerbate the scarcity issue, making it difficult to maintain up-to-date datasets for research.

Developing High-Quality, Domain-Specific Datasets. One effective strategy to address data scarcity is the development of high-quality, domain-specific datasets curated explicitly for political science tasks. For instance, datasets could be constructed from political speeches, legislative records, or annotated campaign materials, enabling researchers to train LLMs on specialized tasks like policy analysis or ideological classification. A notable example is the "BillSum" dataset, which provides U.S. Congressional bills paired with human-generated summaries to support legislative text summarization [143]. Such datasets help ensure that LLMs are exposed to diverse political contexts, enhancing their ability to process and analyze complex political texts accurately.

Synthetic Data Generation using LLM-based Methods. A promising solution to data scarcity is the generation of synthetic datasets, which can simulate real-world political phenomena and expand the diversity of available data. By leveraging LLMs, researchers can create datasets that replicate complex political behaviors, such as voter turnout patterns, policy framing, or legislative negotiations. For example, synthetic election scenarios can be designed to model rare events, such as shifts in voting behavior during political crises or the impact of new campaign strategies. These datasets not only fill gaps in underrepresented areas but also enable researchers to test hypotheses that are otherwise difficult to explore due to the lack of empirical data. Ensuring

the accuracy and neutrality of these synthetic datasets through rigorous validation protocols is essential to maintaining their reliability and applicability in political science research.

Standardizing Validation Protocols for Synthetic Data. To ensure the reliability of synthetic datasets, standardized validation protocols must be established. These protocols should assess synthetic data for accuracy, neutrality, and representativeness. For example, in studies analyzing minority voting behavior, synthetic datasets should undergo rigorous checks to confirm that they accurately reflect the real-world dynamics of marginalized groups rather than amplifying stereotypes. Methods such as cross-validation with human-coded datasets or statistical comparisons to ground-truth data can ensure that synthetic examples align with empirical observations and minimize risks of bias or distortion in LLM outputs.

Collaborative Partnerships for Data Access and Curation. Collaboration among political scientists, data scientists, and public institutions is crucial for enhancing access to valuable data resources. Furthermore, partnerships with government agencies and local/international organizations can provide access to legislative records, public opinion surveys, and election data that are often difficult to obtain through individual efforts. For instance, a partnership with a national statistics agency can yield comprehensive datasets on voting behavior segmented by demographics and geographic regions, enriching research on electoral dynamics. Establishing standardized protocols for data collection and sharing will further enhance dataset quality and ensure balanced representation of diverse political perspectives.

###### 6.3 Addressing Bias and Fairness in Political Predictions

The introduction of LLMs in CPS brings unique risks related to bias and fairness, as these models potentially reflect and amplify biases embedded in their training data. These biases may stem from over-representation of dominant political perspectives, exclusion of minority viewpoints, or inequalities in the underlying datasets [57]. When deployed in sensitive political contexts such as voting behavior analysis or public sentiment modeling, biased predictions can skew insights, misrepresent trends, and even inadvertently influence public opinion or policymaking. This lack of fairness undermines the credibility of research findings and raises ethical concerns about the use of LLMs in these scenarios. Therefore, addressing bias and fairness is not only a technical challenge but also a critical requirement for ensuring the reliability and neutrality of political predictions.

Knowledge Editing to Reduce Bias in Model Outputs. One effective approach to mitigating bias is knowledge editing, which adjusts specific model behaviors by re-training or fine-tuning on carefully curated datasets. This process involves systematically analyzing the model’s outputs across diverse scenarios to identify recurring patterns of bias and then implementing targeted corrections. For example, a study on gender representation in political speech analysis can use a curated dataset that balances male and female political leaders’ contributions, ensuring the model does not overemphasize one gender’s discourse [73]. Knowledge editing ensures that model outputs are more representative, reducing the risk of perpetuating stereotypes or unbalanced narratives.

Counterfactual Data Augmentation for Fairness. Counterfactual data augmentation is another promising solution that introduces synthetic examples to represent underrepresented perspectives or scenarios. In public opinion modeling, synthetic data can simulate viewpoints from minority or marginalized groups that are often absent from traditional datasets. By exposing LLMs to diverse perspectives during training, this method ensures that the models learn a more comprehensive representation of political discourse. In applications like policy framing analysis, counterfactual augmentation can enhance fairness by ensuring that outputs reflect a balance of ideological perspectives, helping policymakers avoid unintended biases in decision-making [143].

Explainable AI for Transparency in Predictions. Transparency is also crucial aspect of addressing bias and ensuring fairness in political predictions. Explainable AI (XAI) methods can clarify how LLMs arrive at specific predictions, making their decision-making pathways interpretable to researchers and stakeholders [172]. For instance, when analyzing election forecasts, XAI tools can highlight the key feature attributes (e.g., polling trends or demographic statistics) that influenced the model’s predictions. This transparency enables researchers to detect and address potential biases in the underlying process, fostering trust in the model’s outputs. Additionally, XAI can facilitate collaboration between domain experts and data scientists, improving both the interpretability and accuracy of LLM-driven political analysis.

###### 6.4 Enhancing Explainability and Reducing Hallucination Risks

The lack of explainability in LLMs poses a major challenge for their application in political science. These models often generate predictions or outputs without providing clear reasoning or insights into the underlying decision-making processes [178]. In tasks such as legislative sentiment analysis or election forecasting, the inability to trace how specific features (e.g., public opinion trends or demographic factors) contribute to the output limits the trust and utility of LLMs in high-stakes political research. This opacity hinders researchers and policymakers from validating or contextualizing the outputs, raising concerns about the reliability of these tools in guiding real-world political decisions.

Hallucination represents the output generated from LLMs that appears to be plausible but lacks grounding in factual data, representing a critical type of risk [178]. This issue is especially problematic in political science, where misinformation or inaccuracies can distort public understanding or influence policy decisions. To illustrate, hallucinations in the generation of political speeches or summaries of legislative texts could misrepresent key policy proposals, leading to flawed analyses or misinformed actions. The high stakes of political science applications demand robust strategies to mitigate these risks and ensure that LLMs produce outputs grounded in factual and reliable data.

Improving Explainability through Feature Attribution. One effective method to enhance explainability is feature attribution, which identifies the specific inputs that contribute most significantly to a model’s predictions. Techniques such as Shapley Additive Explanations (SHAP) [290] or Integrated Gradients [291] can be used to highlight the influence of variables such as polling data, economic indicators, or demographic information in election forecasting [57]. This can be seen in predicting voter turnout, where feature attribution reveals how regional trends impact turnout predictions, enabling researchers to better understand the model’s reasoning. By making these connections explicit, feature attribution enhances transparency in LLM-assisted analysis.

Leveraging Causal Modeling for Explainability. Another approach to improving explainability is causal modeling, which explicitly maps the causal relationships underlying model predictions. For instance, causal diagrams can be used to represent how changes in one factor, such as campaign spending, influence another, like voter preferences [143]. In policy impact analysis, integrating counterfactual scenarios—e.g., “What if a policy were implemented in a different region?”—can provide actionable insights while ensuring that the model’s reasoning aligns with empirical data. By incorporating causal reasoning, LLMs can support more informed decision-making in complex political contexts.

Enhancing Reliability through Uncertainty Quantification. One effective method to enhance reliability is uncertainty quantification, which measures the uncertainty of the output from LLMs. Techniques such as Semantic Entropy [292] or consistency measurements [293, 294] can be used to profile the model’s behavior, including their intrinsic semantics features, linguistic ambiguity, and complex output structures [294]. This can be seen in generating the results, where uncertainty in the generation reveals how consistent the model’s predictions can be, enabling researchers to better trust the model’s prediction. By making an explicit quantification of the generated contents, uncertainty quantification enhances reliability and builds trust in LLM-assisted generated contents.

Incorporating Validation Checkpoints to Reduce Hallucinations. To address hallucination risks, integrating validation checkpoints into LLM workflows is a promising strategy. These checkpoints involve periodic crossreferencing of LLM outputs against established datasets or domain expertise to ensure factual accuracy [178]. An example of this is in summarizing legislative bills, where validation checkpoints can require outputs to be verified against the original legislative text by human experts or through automated retrieval-augmented systems. The iterative process minimizes the likelihood of inaccuracies propagating through the analysis and ensures that outputs remain aligned with empirical evidence.

###### 6.5 Democratizing Access to Political Knowledge

Democratizing access to political knowledge refers to the process of making political information, such as legislative texts, policy analyses, and electoral data, accessible and understandable to a broader audience. This goal seeks to address barriers such as the complexity of legal language, information asymmetry, and the marginalization of underrepresented groups in political discourse. Currently, these barriers prevent many

citizens from engaging with and understanding political processes, limiting their participation in democratic systems. By leveraging LLMs, researchers aim to simplify complex political content, provide multilingual support, and adapt information to diverse cultural and ideological contexts, thereby enabling more inclusive and equitable access to political knowledge [171].

Simplifying Political Language Through LLM-Driven Tools. One effective strategy to democratize access is developing user-facing tools powered by LLMs to simplify complex political language. For example, interactive Q&A systems can allow users to query legislative documents and receive concise, accurate, and accessible explanations. A practical application is the creation of voter guides that summarize candidates’ platforms or key legislative initiatives in plain language. Tools like these can help demystify complicated topics such as tax reforms or healthcare policies, making them more approachable for the general public [171]. Ensuring that these simplifications maintain accuracy and neutrality is critical to preserving trust and effectiveness.

Multilingual Support and Cultural Adaptation. To overcome language and cultural barriers, LLMs should provide robust multilingual support and culturally adapted outputs. For instance, an LLM-powered platform could offer translations of legislative texts into minority languages while contextualizing the content to reflect local cultural norms. In a real-world application, such a system could support Indigenous or immigrant communities by delivering policy information in their native languages, enabling them to better understand and engage with democratic processes. Expanding multilingual and culturally sensitive capabilities ensures that political knowledge reaches diverse audiences, promoting fairness and inclusivity in political discourse [171].

Incorporating Explainable and Ethical AI Principles. Another critical measure is incorporating Explainable AI (XAI) and Ethical AI (EAI) principles into LLM applications for political science. These principles enhance the transparency and accountability of LLM outputs by clarifying how information is processed and ensuring that outputs align with ethical standards. For instance, XAI techniques can provide detailed explanations of how an LLM summarized a policy proposal, enabling users to trace the reasoning behind its conclusions. Similarly, EAI frameworks can ensure that outputs are unbiased and equitable, addressing ethical concerns and fostering trust among users [178]. By integrating these principles, political knowledge systems can balance accessibility with fairness, ensuring responsible use of AI in democratic contexts.

###### 6.6 Call for Novel Evaluation Criteria for Computational Political Science

The Importance of Comprehensive Evaluation Criteria. Comprehensive and reasonable evaluation criteria are crucial for advancing computational political science (CPS). These criteria ensure that LLMs are not only judged by technical proficiency but also by their relevance and applicability in the political domain. While existing metrics such as accuracy, F1-score, and BLEU are widely used in NLP research, they often fail to address the nuanced requirements of CPS tasks [267]. In political science, models must go beyond technical performance to reflect deeper insights, such as their capacity to interpret policy implications, predict electoral dynamics, or analyze ideological framing. Without domain-specific evaluation metrics, the true potential and limitations of LLMs in political science may remain obscured.

Existing evaluation criteria in CPS often focus on generic NLP metrics, which usually includes:

- • Accuracy and F1-Score: Widely used for classification tasks like sentiment analysis or ideological alignment detection, these metrics measure how well a model categorizes data into predefined labels.
- • BLEU and ROUGE: Commonly applied to text generation tasks such as legislative summarization, these metrics evaluate the similarity between model-generated outputs and reference texts.
- • Cross-Validation Performance: Utilized to assess the generalizability of models across different datasets, ensuring consistency in tasks like voter behavior prediction.


While these metrics provide valuable benchmarks, they fall short in capturing the real-world implications of LLM outputs in political contexts. For instance, BLEU may not adequately measure how well a generated legislative summary conveys critical policy details, and F1-score cannot evaluate whether sentiment analysis accurately reflects ideological subtleties.

Proposed Novel Evaluation Framework for CPS. To address the limitations of current metrics, future research should explore novel evaluation criteria tailored to the unique demands of CPS tasks. The evaluation framework should include metrics from these aspects:

- 1. Policy Relevance: This metric assesses how effectively a model contextualizes policy positions within legislative texts or debates. For example, when summarizing a healthcare policy, the model should highlight key trade-offs, stakeholder impacts, and alignment with political objectives. This is particularly valuable in tasks like legislative analysis, where the focus is on understanding the implications of proposed policies.
- 2. Electoral Impact: Electoral impact measures a model’s ability to accurately predict public opinion or campaign dynamics based on contextual variables such as demographic trends and polling data. For instance, in predicting swing state outcomes during U.S. elections, this metric can assess how well the model incorporates regional voting patterns and past election data [267].
- 3. Legislative Influence: Legislative influence evaluates the societal implications of proposed policies or legislative actions. For example, this metric can be used to analyze how well a model predicts the downstream effects of policy changes, such as shifts in public opinion, economic impact, or voting behavior. Researchers can leverage this metric to better understand the broader consequences of legislative decisions.
- 4. Fairness and Bias Metrics: Given the importance of neutrality in political science, fairness and bias metrics should evaluate how balanced and inclusive LLM outputs are across diverse ideological perspectives. For example, when generating policy summaries, the model should avoid overemphasizing dominant viewpoints while marginalizing minority opinions, ensuring a fair representation of all stakeholders [267].


#### 7 Conclusion

This survey provides the first comprehensive interdisciplinary exploration of the integration of LLMs into political science, bridging gaps between classical methodologies and modern computational approaches. We introduce a novel principled taxonomy that systematically categorizes political science tasks and LLM-driven methods, offering a structured framework to guide researchers in leveraging LLMs effectively. We begin by detailing LLM’s capabilities across predictive modeling, generative tasks, simulation, causal inference, and societal impacts from political science perspective. Our analysis highlights both the transformative potential of LLMs and the pressing challenges they present, including data scarcity, biases, explainability limitations, and ethical concerns. Furthermore, we elaborate computational techniques from computer science perspective, including fine-tuning methods, LLM inference strategies, and the development of domain-specific benchmarks, tailored to political science applications. An empirical case study on ANES presidential election voting simulation exemplifies the practical implementation of these methods. Finally, we identify critical research directions, emphasizing the need for modular research pipelines, novel evaluation metrics, and robust approaches to bias mitigation and fairness enhancement. Our survey underscores the necessity of interdisciplinary collaboration and ethical considerations in advancing the use of LLMs in political science. By addressing the identified challenges, we aim to inspire further research that promotes the responsible and impactful application of LLMs, enabling more informed, transparent, and equitable political processes.

#### References

- [1] Michael Wornow, Yizhe Xu, Rahul Thapa, Birju Patel, Ethan Steinberg, Scott Fleming, Michael A Pfeffer, Jason Fries, and Nigam H Shah. The shaky foundations of large language models and foundation models for electronic health records. npj Digital Medicine, 6(1):135, 2023.
- [2] Yuqing Wang, Yun Zhao, and Linda Petzold. Are large language models ready for healthcare? a comparative study on clinical language understanding. In Machine Learning for Healthcare Conference, pages 804–823. PMLR, 2023.
- [3] Zerui Xu, Fang Wu, Tianfan Fu, and Yue Zhao. Retrieval-reasoning large language model-based synthetic clinical trial generation. arXiv preprint arXiv:2410.12476, 2024.
- [4] Ling Yue, Sixue Xing, Jintai Chen, and Tianfan Fu. Clinicalagent: Clinical trial multi-agent with large language model-based reasoning. arXiv preprint arXiv:2404.14777, 2024.


- [5] Allen H Huang, Hui Wang, and Yi Yang. Finbert: A large language model for extracting information from financial text. Contemporary Accounting Research, 40(2):806–841, 2023.
- [6] Shĳie Wu, Ozan Irsoy, Steven Lu, Vadim Dabravolski, Mark Dredze, Sebastian Gehrmann, Prabhanjan Kambadur, David Rosenberg, and Gideon Mann. Bloomberggpt: A large language model for finance. arXiv preprint arXiv:2303.17564, 2023.
- [7] Qianqian Xie, Weiguang Han, Xiao Zhang, Yanzhao Lai, Min Peng, Alejandro Lopez-Lira, and Jimin Huang. Pixiu: A comprehensive benchmark, instruction dataset and large language model for finance. In Advances in Neural Information Processing Systems, 2024.
- [8] Xuan Zhang, Limei Wang, Jacob Helwig, Youzhi Luo, Cong Fu, Yaochen Xie, Meng Liu, Yuchao Lin, Zhao Xu, Keqiang Yan, Keir Adams, Maurice Weiler, Xiner Li, Tianfan Fu, Yucheng Wang, Haiyang Yu, YuQing Xie, Xiang Fu, Alex Strasser, Shenglong Xu, Yi Liu, Yuanqi Du, Alexandra Saxton, Hongyi Ling, Hannah Lawrence, Hannes Stärk, Shurui Gui, Carl Edwards, Nicholas Gao, Adriana Ladera, Tailin Wu, Elyssa F. Hofgard, Aria Mansouri Tehrani, Rui Wang, Ameya Daigavane, Montgomery Bohde, Jerry Kurtin, Qian Huang, Tuong Phung, Minkai Xu, Chaitanya K. Joshi, Simon V. Mathis, Kamyar Azizzadenesheli, Ada Fang, Alán Aspuru-Guzik, Erik Bekkers, Michael Bronstein, Marinka Zitnik, Anima Anandkumar, Stefano Ermon, Pietro Liò, Rose Yu, Stephan Günnemann, Jure Leskovec, Heng Ji, Jimeng Sun, Regina Barzilay, Tommi Jaakkola, Connor W. Coley, Xiaoning Qian, Xiaofeng Qian, Tess Smidt, and Shuiwang Ji. Artificial intelligence for science in quantum, atomistic, and continuum systems. arXiv preprint arXiv:2307.08423, 2023.
- [9] Yu Zhang, Xiusi Chen, Bowen Jin, Sheng Wang, Shuiwang Ji, Wei Wang, and Jiawei Han. A comprehensive survey of scientific large language models and their applications in scientific discovery. In Conference on Empirical Methods in Natural Language Processing, page 8783–8817, 2024.
- [10] Sizhe Liu, Yizhou Lu, Siyu Chen, Xiyang Hu, Jieyu Zhao, Tianfan Fu, and Yue Zhao. Drugagent: Automating ai-aided drug discovery programming through llm multi-agent collaboration. arXiv, 2024.
- [11] Longchao Da, Kuanru Liou, Tiejin Chen, Xuesong Zhou, Xiangyong Luo, Yezhou Yang, and Hua Wei. Open-ti: Open traffic intelligence with augmented language model. International Journal of Machine Learning and Cybernetics, pages 1–26, 2024.
- [12] Longchao Da, Minquan Gao, Hao Mei, and Hua Wei. Prompt to transfer: Sim-to-real transfer for traffic signal control with prompt learning. In Proceedings of the AAAI Conference on Artificial Intelligence, pages 82–90, 2024.
- [13] Weĳia Zhang, Jindong Han, Zhao Xu, Hang Ni, Hao Liu, and Hui Xiong. Urban foundation models: A survey. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pages 6633–6643, 2024.
- [14] Zhonghang Li, Long Xia, Lei Shi, Yong Xu, Dawei Yin, and Chao Huang. Opencity: Open spatiotemporal foundation models for traffic prediction. arXiv preprint arXiv:2408.10269, 2024.
- [15] Enkelejda Kasneci, Kathrin Seßler, Stefan Küchemann, Maria Bannert, Daryna Dementieva, Frank Fischer, Urs Gasser, Georg Groh, Stephan Günnemann, Eyke Hüllermeier, et al. Chatgpt for good? on opportunities and challenges of large language models for education. Learning and individual differences, 103:102274, 2023.
- [16] Gustavo Pinto, Isadora Cardoso-Pereira, Danilo Monteiro, Danilo Lucena, Alberto Souza, and Kiev Gama. Large language models for education: Grading open-ended questions using chatgpt. In Proceedings of the XXXVII Brazilian Symposium on Software Engineering, page 293–302, 2023.
- [17] Owen Henkel, Libby Hills, Adam Boxer, Bill Roberts, and Zach Levonian. Can large language models make the grade? an empirical study evaluating llms ability to mark short answer questions in k-12 education. In Proceedings of the Eleventh ACM Conference on Learning@ Scale, pages 300–304, 2024.
- [18] Shervin Minaee, Tomas Mikolov, Narjes Nikzad, Meysam Chenaghlu, Richard Socher, Xavier Amatriain, and Jianfeng Gao. Large language models: A survey. arXiv preprint arXiv:2402.06196, 2024.
- [19] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. A survey of large language models. arXiv preprint arXiv:2303.18223, 2023.


- [20] Mitchell Linegar, Rafal Kocielnik, and R. Michael Alvarez. Large language models and political science. Frontiers in Political Science, 5, 2023.
- [21] Lisa P Argyle, Ethan C Busby, Nancy Fulda, Joshua R Gubler, Christopher Rytting, and David Wingate. Out of one, many: Using language models to simulate human samples. Political Analysis, 31(3):337–351,

- 2023.

[22] Caleb Ziems, William Held, Omar Shaikh, Jiaao Chen, Zhehao Zhang, and Diyi Yang. Can large language models transform computational social science? Computational Linguistics, 50(1):237–291,

- 2024.


- [23] Dorottya Demszky, Diyi Yang, David S Yeager, Christopher J Bryan, Margarett Clapper, Susannah Chandhok, Johannes C Eichstaedt, Cameron Hecht, Jeremy Jamieson, Meghann Johnson, et al. Using large language models in psychology. Nature Reviews Psychology, 2(11):688–701, 2023.
- [24] George-Cristinel Rotaru, Sorin Anagnoste, and Vasile-Marian Oancea. How artificial intelligence can influence elections: Analyzing the large language models (llms) political bias. In Proceedings of the International Conference on Business Excellence, pages 1882–1891, 2024.
- [25] Emma Rodman. On political theory and large language models. Political Theory, 52(4):548–580, 2024.
- [26] Lucas Gover. Political bias in large language models. The Commons: Puget Sound Journal of Politics, 4(1):2, 2023.
- [27] Terry M Moe. Power and political institutions. Perspectives on politics, 3(2):215–233, 2005.
- [28] Chenxi Gao, Yini Li, et al. Post-war development analysis of political science: from behaviorism to new institutionalism: Political science development trend, challenges and suggestions. International Journal of Frontiers in Sociology, 4(8), 2022.
- [29] John Wilkerson and Andreu Casas. Large-scale computerized text analysis in political science: Opportunities and challenges. Annual Review of Political Science, 20(1):529–544, 2017.
- [30] Emily Chen, Ashok Deb, and Emilio Ferrara. # election2020: the first public twitter dataset on the 2020 us presidential election. Journal of Computational Social Science, pages 1–18, 2022.
- [31] John Gerring. Qualitative methods. Annual Review of Political Science, 20(1):15–36, 2017.
- [32] Petter Törnberg. Chatgpt-4 outperforms experts and crowd workers in annotating political twitter messages with zero-shot learning. arXiv preprint arXiv:2304.06588, 2023.
- [33] Michael Heseltine and Bernhard Clemm von Hohenberg. Large language models as a substitute for human experts in annotating political text. Research & Politics, 11(1):20531680241236239, 2024.
- [34] Yiheng Liu, Tianle Han, Siyuan Ma, Jiayue Zhang, Yuanyuan Yang, Jiaming Tian, Hao He, Antong Li, Mengshen He, Zhengliang Liu, et al. Summary of chatgpt-related research and perspective towards the future of large language models. Meta-Radiology, page 100017, 2023.
- [35] Yaoxun Xu, Hangting Chen, Jianwei Yu, Qiaochu Huang, Zhiyong Wu, Shi-Xiong Zhang, Guangzhi Li, Yi Luo, and Rongzhi Gu. Secap: Speech emotion captioning with large language model. In Proceedings of the AAAI Conference on Artificial Intelligence, pages 19323–19331, 2024.
- [36] Shengbin Yue, Wei Chen, Siyuan Wang, Bingxuan Li, Chenchen Shen, Shujun Liu, Yuxuan Zhou, Yao Xiao, Song Yun, Xuanjing Huang, et al. Disc-lawllm: Fine-tuning large language models for intelligent legal services. arXiv preprint arXiv:2309.11325, 2023.
- [37] Joseph Gesnouin, Yannis Tannier, Christophe Gomes Da Silva, Hatim Tapory, Camille Brier, Hugo Simon, Raphael Rozenberg, Hermann Woehrel, Mehdi El Yakaabi, Thomas Binder, et al. Llamandement: Large language models for summarization of french legislative proposals. arXiv preprint arXiv:2401.16182, 2024.
- [38] Petter Törnberg, Diliara Valeeva, Justus Uitermark, and Christopher Bail. Simulating social media using large language models to evaluate alternative news feed algorithms. arXiv preprint arXiv:2310.05984, 2023.
- [39] Ali Najafi and Onur Varol. Turkishbertweet: Fast and reliable large language model for social media analysis. Expert Systems with Applications, 255:124737, 2024.


- [40] Tianyi Zhang, Faisal Ladhak, Esin Durmus, Percy Liang, Kathleen McKeown, and Tatsunori B Hashimoto. Benchmarking large language models for news summarization. Transactions of the Association for Computational Linguistics, 12:39–57, 2024.
- [41] Xiao Fang, Shangkun Che, Minjia Mao, Hongzhe Zhang, Ming Zhao, and Xiaohang Zhao. Bias of ai-generated content: an examination of news produced by large language models. Scientific Reports, 14(1):5224, 2024.
- [42] David Rozado. The political preferences of llms. arXiv preprint arXiv:2402.01789, 2024.
- [43] Simon Martin Breum, Daniel Vædele Egdal, Victor Gram Mortensen, Anders Giovanni Møller, and Luca Maria Aiello. The persuasive power of large language models. In Proceedings of the International AAAI Conference on Web and Social Media, volume 18, pages 152–163, 2024.
- [44] Juan-Pablo Rivera, Gabriel Mukobi, Anka Reuel, Max Lamparth, Chandler Smith, and Jacquelyn Schneider. Escalation risks from language models in military and diplomatic decision-making. In The 2024 ACM Conference on Fairness, Accountability, and Transparency, pages 836–898, 2024.
- [45] Pratik Gujral, Kshitĳ Awaldhi, Navya Jain, Bhavuk Bhandula, and Abhĳnan Chakraborty. Can llms help predict elections?(counter) evidence from the world’s largest democracy. arXiv preprint arXiv:2405.07828, 2024.
- [46] Wenxuan Zhang, Yue Deng, Bing Liu, Sinno Jialin Pan, and Lidong Bing. Sentiment analysis in the era of large language models: A reality check. arXiv preprint arXiv:2305.15005, 2023.
- [47] Asif Khan, Nada Boudjellal, Huaping Zhang, Arshad Ahmad, and Maqbool Khan. From social media to ballot box: Leveraging location-aware sentiment analysis for election predictions. Computers, Materials & Continua, 77(3), 2023.
- [48] Xinnong Zhang, Jiayu Lin, Libo Sun, Weihong Qi, Yihang Yang, Yue Chen, Hanjia Lyu, Xinyi Mou, Siming Chen, Jiebo Luo, et al. Electionsim: Massive population election simulation powered by large language model driven agents. arXiv preprint arXiv:2410.20746, 2024.
- [49] Yujin Potter, Shiyang Lai, Junsol Kim, James Evans, and Dawn Song. Hidden persuaders: Llms’ political leaning and their influence on voters. arXiv preprint arXiv:2410.24190, 2024.
- [50] Shibani Santurkar, Esin Durmus, Faisal Ladhak, Cinoo Lee, Percy Liang, and Tatsunori Hashimoto. Whose opinions do language models reflect? In International Conference on Machine Learning, pages 29971–30004, 2023.
- [51] Björn Bremer and Reto Bürgisser. Public opinion on welfare state recalibration in times of austerity: Evidence from survey experiments. Political Science Research and Methods, 11(1):34–52, 2023.
- [52] Zhenyu Wang, Yi Xu, Dequan Wang, Lingfeng Zhou, and Yiqi Zhou. Intelligent computing social modeling and methodological innovations in political science in the era of large language models. arXiv preprint arXiv:2410.16301, 2024.
- [53] Andrew Halterman and Katherine A Keith. Codebook llms: Adapting political science codebooks for llm use and adapting llms to follow codebooks. arXiv preprint arXiv:2407.10747, 2024.
- [54] Xinyi Mou, Zejun Li, Hanjia Lyu, Jiebo Luo, and Zhongyu Wei. Unifying local and global knowledge: Empowering large language models as political experts with knowledge graphs. In Proceedings of the ACM on Web Conference 2024, pages 2603–2614, 2024.
- [55] Zachary R Baker and Zarif L Azher. Simulating the us senate: An llm-driven agent approach to modeling legislative behavior and bipartisanship. arXiv preprint arXiv:2406.18702, 2024.
- [56] Kai Chen, Zihao He, Jun Yan, Taiwei Shi, and Kristina Lerman. How susceptible are large language models to ideological manipulation? arXiv preprint arXiv:2402.11725, 2024.
- [57] Zihao He, Siyi Guo, Ashwin Rao, and Kristina Lerman. Inducing political bias allows language models anticipate partisan reactions to controversies. arXiv preprint arXiv:2311.09687, 2023.
- [58] Jia-Yu Yao, Kun-Peng Ning, Zhen-Hui Liu, Mu-Nan Ning, Yu-Yang Liu, and Li Yuan. Llm lies: Hallucinations are not bugs, but features as adversarial examples. arXiv preprint arXiv:2310.01469,


- [59] Yifan Yao, Jinhao Duan, Kaidi Xu, Yuanfang Cai, Zhibo Sun, and Yue Zhang. A survey on large language model (llm) security and privacy: The good, the bad, and the ugly. High-Confidence Computing, page 100211, 2024.
- [60] Giada Marino and Fabio Giglietto. Integrating large language models in political discourse studies on social media: Challenges of validating an llms-in-the-loop pipeline. Sociologica, 18(2):87–107, 2024.
- [61] Nicola De Cao, Wilker Aziz, and Ivan Titov. Editing factual knowledge in language models. arXiv preprint arXiv:2104.08164, 2021.
- [62] Song Wang, Yaochen Zhu, Haochen Liu, Zaiyi Zheng, Chen Chen, and Jundong Li. Knowledge editing for large language models: A survey. ACM Computing Surveys, 2023.
- [63] Sĳia Liu, Yuanshun Yao, Jinghan Jia, Stephen Casper, Nathalie Baracaldo, Peter Hase, Yuguang Yao, Chris Yuhao Liu, Xiaojun Xu, Hang Li, et al. Rethinking machine unlearning for large language models. arXiv preprint arXiv:2402.08787, 2024.
- [64] Zheyuan Liu, Guangyao Dou, Zhaoxuan Tan, Yĳun Tian, and Meng Jiang. Towards safer large language models through machine unlearning. arXiv preprint arXiv:2402.10058, 2024.
- [65] Zhengliang Liu, Yiwei Li, Oleksandra Zolotarevych, Rongwei Yang, and Tianming Liu. Llm-potus score: A framework of analyzing presidential debates with large language models. arXiv preprint arXiv:2409.08147, 2024.
- [66] Fabio Motoki, Valdemar Pinho Neto, and Victor Rodrigues. More human than human: Measuring chatgpt political bias. Public Choice, 198(1):3–23, 2024.
- [67] Mitchell Linegar, Rafal Kocielnik, and R Michael Alvarez. Large language models and political science. Frontiers in Political Science, 5:1257092, 2023.
- [68] Menglin Liu and Ge Shi. Poliprompt: A high-performance cost-effective llm-based text classification framework for political science. arXiv preprint arXiv:2409.01466, 2024.
- [69] Ken Kato, Annabelle Purnomo, Christopher Cochrane, and Raeid Saqur. L (u) pin: Llm-based political ideology nowcasting. arXiv preprint arXiv:2405.07320, 2024.
- [70] Joshua C Yang, Marcin Korecki, Damian Dailisan, Carina I Hausladen, and Dirk Helbing. Llm voting: Human choices and ai collective decision making. arXiv preprint arXiv:2402.01766, 2024.
- [71] Ollie Liu, Deqing Fu, Dani Yogatama, and Willie Neiswanger. Dellma: Decision making under uncertainty with large language models. arXiv preprint arXiv:2402.02392, 2024.
- [72] Kakia Chatsiou and Slava Jankin Mikhaylov. Deep learning for political science. The SAGE handbook of research methods in political science and international relations, pages 1053–1078, 2020.
- [73] Patrick Y Wu, Joshua A Tucker, Jonathan Nagler, and Solomon Messing. Large language models can be used to estimate the ideologies of politicians in a zero-shot learning setting. arXiv preprint arXiv:2303.12057, 2023.
- [74] Ilias Chalkidis. Investigating llms as voting assistants via contextual augmentation: A case study on the european parliament elections 2024. arXiv preprint arXiv:2407.08495, 2024.
- [75] Farhad Moghimifar, Yuan-Fang Li, Robert Thomson, and Gholamreza Haffari. Modelling political coalition negotiations using llm-based agents. arXiv preprint arXiv:2402.11712, 2024.
- [76] Nathan E Sanders, Alex Ulinich, and Bruce Schneier. Demonstrations of the potential of ai-based political issue polling. arXiv preprint arXiv:2307.04781, 2023.
- [77] Kobi Hackenburg, Lujain Ibrahim, Ben M Tappin, and Manos Tsakiris. Comparing the persuasiveness of role-playing large language models and human experts on polarized us political issues. OSF Preprints, 10, 2023.
- [78] Seth Lazar and Lorenzo Manuali. Can llms advance democratic values? arXiv preprint arXiv:2410.08418, 2024.
- [79] Jairo F Gudiño, Umberto Grandi, and César Hidalgo. Large language models (llms) as agents for augmented democracy. Philosophical Transactions A, 382(2285):20240100, 2024.


- [80] Zhanna Terechshenko, Fridolin Linder, Vishakh Padmakumar, Michael Liu, Jonathan Nagler, Joshua A Tucker, and Richard Bonneau. A comparison of methods in political science text classification: Transfer learning language models for politics. Available at SSRN 3724644, 2020.
- [81] Kyuwon Lee, Simone Paci, Jeongmin Park, Hye Young You, and Sylvan Zheng. Applications of gpt in political science research, 2024.
- [82] David Rozado. The political biases of chatgpt. Social Sciences, 12(3):148, 2023.
- [83] Joseph T Ornstein, Elise N Blasingame, and Jake S Truscott. How to train your stochastic parrot: Large language models for political texts. Technical report, Working Paper, 2022.
- [84] Laura Weidinger, John Mellor, Maribeth Rauh, Conor Griffin, Jonathan Uesato, Po-Sen Huang, Myra Cheng, Mia Glaese, Borja Balle, Atoosa Kasirzadeh, et al. Ethical and social risks of harm from language models. arXiv preprint arXiv:2112.04359, 2021.
- [85] Ehsan Ul Haq, Tristan Braud, Young D Kwon, and Pan Hui. A survey on computational politics. IEEE Access, 8:197379–197406, 2020.
- [86] Justin Grimmer, Margaret E Roberts, and Brandon M Stewart. Machine learning for social science: An agnostic approach. Annual Review of Political Science, 24(1):395–419, 2021.
- [87] Jairo Nicolau. An analysis of the 2002 presidential elections using logistic regression. Brazilian political science review, 1(1):125–135, 2007.
- [88] Vito d’Orazio, Steven T Landis, Glenn Palmer, and Philip Schrodt. Separating the wheat from the chaff: Applications of automated document classification using support vector machines. Political analysis, 22(2):224–242, 2014.
- [89] Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg S Corrado, and Jeff Dean. Distributed representations of words and phrases and their compositionality. Advances in neural information processing systems, 26, 2013.
- [90] Jacob Devlin. Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805, 2018.
- [91] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. In The Thirty-first Annual Conference on Neural Information Processing Systems, 2017.
- [92] Tom B. Brown, Benjamin Mann, Nick Ryder, and Others. Language models are few-shot learners, 2020.
- [93] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. Journal of machine learning research, 21(140):1–67, 2020.
- [94] Alireza Salemi and Hamed Zamani. Evaluating retrieval quality in retrieval-augmented generation. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 2395–2400, 2024.
- [95] James R Kirk, Robert E Wray, Peter Lindes, and John E Laird. Improving knowledge extraction from llms for task learning through agent analysis. In Proceedings of the AAAI Conference on Artificial Intelligence, pages 18390–18398, 2024.
- [96] Lin Song, Yukang Chen, Shuai Yang, Xiaohan Ding, Yixiao Ge, Ying-Cong Chen, and Ying Shan. Low-rank approximation for sparse attention in multi-modal llms. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 13763–13773, 2024.
- [97] Qianchao Zhu, Jiangfei Duan, Chang Chen, Siran Liu, Xiuhong Li, Guanyu Feng, Xin Lv, Huanqi Cao, Xiao Chuanfu, Xingcheng Zhang, et al. Sampleattention: Near-lossless acceleration of long context llm inference with adaptive structured sparse attention. arXiv preprint arXiv:2406.15486, 2024.
- [98] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample. Llama: Open and efficient foundation language models,


- [99] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774, 2023.
- [100] Dale Schuurmans, Hanjun Dai, and Francesco Zanini. Autoregressive large language models are computationally universal. arXiv preprint arXiv:2410.03170, 2024.
- [101] Debora Nozza, Federico Bianchi, and Dirk Hovy. What the [mask]? making sense of language-specific bert models. arXiv preprint arXiv:2003.02912, 2020.
- [102] Zongxi Li, Xianming Li, Yuzhang Liu, Haoran Xie, Jing Li, Fu-lee Wang, Qing Li, and Xiaoqin Zhong. Label supervised llama finetuning. arXiv preprint arXiv:2310.01208, 2023.
- [103] Shengyu Zhang, Linfeng Dong, Xiaoya Li, Sen Zhang, Xiaofei Sun, Shuhe Wang, Jiwei Li, Runyi Hu, Tianwei Zhang, Fei Wu, et al. Instruction tuning for large language models: A survey. arXiv preprint arXiv:2308.10792, 2023.
- [104] Harrison Lee, Samrat Phatale, Hassan Mansoor, Thomas Mesnard, Johan Ferret, Kellie Ren Lu, Colton Bishop, Ethan Hall, Victor Carbune, Abhinav Rastogi, et al. Rlaif vs. rlhf: Scaling reinforcement learning from human feedback with ai feedback. In Forty-first International Conference on Machine Learning, 2024.
- [105] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large language models are zero-shot reasoners. Advances in neural information processing systems, 35:22199–22213, 2022.
- [106] Ethan Perez, Douwe Kiela, and Kyunghyun Cho. True few-shot learning with language models. Advances in neural information processing systems, 34:11054–11070, 2021.
- [107] Ori Ram, Yoav Levine, Itay Dalmedigos, Dor Muhlgay, Amnon Shashua, Kevin Leyton-Brown, and Yoav Shoham. In-context retrieval-augmented language models. Transactions of the Association for Computational Linguistics, 11:1316–1331, 2023.
- [108] Sumanth Prabhu. Pedal: Enhancing greedy decoding with large language models using diverse exemplars. arXiv preprint arXiv:2408.08869, 2024.
- [109] Yuxi Xie, Kenji Kawaguchi, Yiran Zhao, James Xu Zhao, Min-Yen Kan, Junxian He, and Michael Xie. Self-evaluation guided beam search for reasoning. Advances in Neural Information Processing Systems, 36, 2024.
- [110] Dejan Grubisic, Volker Seeker, Gabriel Synnaeve, Hugh Leather, John Mellor-Crummey, and Chris Cummins. Priority sampling of large language models for compilers. In Proceedings of the 4th Workshop on Machine Learning and Systems, pages 91–97, 2024.
- [111] Jules White, Quchen Fu, Sam Hays, Michael Sandborn, Carlos Olea, Henry Gilbert, Ashraf Elnashar, Jesse Spencer-Smith, and Douglas C Schmidt. A prompt pattern catalog to enhance prompt engineering with chatgpt. arXiv preprint arXiv:2302.11382, 2023.
- [112] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. Advances in Neural Information Processing Systems, 36, 2024.
- [113] Ariana Martino, Michael Iannelli, and Coleen Truong. Knowledge injection to counter large language model (llm) hallucination. In European Semantic Web Conference, pages 182–185. Springer, 2023.
- [114] Deepak Narayanan, Mohammad Shoeybi, Jared Casper, et al. Efficient large-scale language model training on gpu clusters using megatron-lm. In Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis, pages 1–15, 2021.
- [115] Ning Ding, Yujia Qin, Guang Yang, Fuchao Wei, Zonghan Yang, Yusheng Su, Shengding Hu, Yulin Chen, Chi-Min Chan, Weize Chen, et al. Parameter-efficient fine-tuning of large-scale pre-trained language models. Nature Machine Intelligence, 5(3):220–235, 2023.
- [116] Bingyang Wu, Yinmin Zhong, Zili Zhang, Shengyu Liu, Fangyue Liu, Yuanhang Sun, Gang Huang, Xuanzhe Liu, and Xin Jin. Fast distributed inference serving for large language models. arXiv preprint arXiv:2305.05920, 2023.


- [117] Yixin Song, Zeyu Mi, Haotong Xie, and Haibo Chen. Powerinfer: Fast large language model serving with a consumer-grade gpu. In Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems Principles, pages 590–606, 2024.
- [118] Pengjie Ren, Chengshun Shi, Shiguang Wu, Mengqi Zhang, Zhaochun Ren, Maarten Rĳke, Zhumin Chen, and Jiahuan Pei. Melora: Mini-ensemble low-rank adapters for parameter-efficient fine-tuning. In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 3052–3064, 2024.
- [119] Zihao Fu, Haoran Yang, Anthony Man-Cho So, Wai Lam, Lidong Bing, and Nigel Collier. On the effectiveness of parameter-efficient fine-tuning. In Proceedings of the AAAI conference on artificial intelligence, pages 12799–12807, 2023.
- [120] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving with pagedattention. In Proceedings of the 29th Symposium on Operating Systems Principles, pages 611–626, 2023.
- [121] NVIDIA. TensorRT-LLM. https://github.com/NVIDIA/TensorRT-LLM.
- [122] Hanqing Zhang, Haolin Song, Shaoyu Li, Ming Zhou, and Dawei Song. A survey of controllable text generation using transformer-based pre-trained language models. ACM Computing Surveys, 56(3):1–37, 2023.
- [123] Yujin Potter, Shiyang Lai, Junsol Kim, James Evans, and Dawn Song. Hidden persuaders: Llms’ political leaning and their influence on voters, 2024.
- [124] Inyoung Cheong, King Xia, KJ Kevin Feng, Quan Ze Chen, and Amy X Zhang. (a) i am not a lawyer, but...: Engaging legal experts towards responsible llm policies for legal advice. In The 2024 ACM Conference on Fairness, Accountability, and Transparency, pages 2454–2469, 2024.
- [125] Jiaying Wu, Jiafeng Guo, and Bryan Hooi. Fake news in sheep’s clothing: Robust fake news detection against llm-empowered style attacks. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pages 3367–3378, 2024.
- [126] Daniel Treisman. How great is the current danger to democracy? assessing the risk with historical data. Comparative Political Studies, 56(12):1924–1952, 2023.
- [127] Meta Fundamental AI Research Diplomacy Team (FAIR)†, Anton Bakhtin, Noam Brown, Emily Dinan, Gabriele Farina, Colin Flaherty, Daniel Fried, Andrew Goff, Jonathan Gray, Hengyuan Hu, et al. Human-level play in the game of diplomacy by combining language models with strategic reasoning. Science, 378(6624):1067–1074, 2022.
- [128] Andrea Colombo. Leveraging knowledge graphs and llms to support and monitor legislative systems. In Proceedings of the 33rd ACM International Conference on Information and Knowledge Management, pages 5443–5446, 2024.
- [129] Naoki Egami, Musashi Hinck, Brandon Stewart, and Hanying Wei. Using imperfect surrogates for downstream inference: Design-based supervised learning for social science applications of large language models. Advances in Neural Information Processing Systems, 36, 2024.
- [130] Yujian Liu, Xinliang Frederick Zhang, David Wegsman, Nicholas Beauchamp, and Lu Wang. POLITICS: Pretraining with same-story article comparison for ideology prediction and stance detection. In Findings of the Association for Computational Linguistics: NAACL 2022, pages 1354–1374, Seattle, United States, 2022. Association for Computational Linguistics.
- [131] Ilias Chalkidis and Stephanie Brandl. Llama meets EU: Investigating the European political spectrum through the lens of LLMs. In Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 2: Short Papers), pages 481–498, 2024.
- [132] YupengCao, AishwaryaMuralidharanNair, ElyonEyimife, NastaranJamalipourSoofi, KPSubbalakshmi, John R Wullert II, Chumki Basu, and David Shallcross. Can large language models detect misinformation in scientific news reporting? arXiv preprint arXiv:2402.14268, 2024.


- [133] Margherita Gambini, Caterina Senette, Tiziano Fagni, and Maurizio Tesconi. Evaluating large language models for user stance detection on x (twitter). Machine Learning, pages 1–24, 2024.
- [134] Bo Wang, Jing Ma, Hongzhan Lin, Zhiwei Yang, Ruichao Yang, Yuan Tian, and Yi Chang. Explainable Fake News Detection with Large Language Model via Defense Among Competing Wisdom. In Proceedings of the ACM Web Conference 2024, WWW ’24, pages 2452–2463, New York, NY, USA, May 2024. Association for Computing Machinery.
- [135] Jiaying Wu, Jiafeng Guo, and Bryan Hooi. Fake News in Sheep’s Clothing: Robust Fake News Detection Against LLM-Empowered Style Attacks. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, pages 3367–3378, 2024. arXiv:2310.10830 [cs].
- [136] Beizhe Hu, Qiang Sheng, Juan Cao, Yuhui Shi, Yang Li, Danding Wang, and Peng Qi. Bad actor, good advisor: Exploring the role of large language models in fake news detection. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pages 22105–22113, 2024.
- [137] Chenxi Whitehouse, Tillman Weyde, Pranava Madhyastha, and Nikos Komninos. Evaluation of fake news detection with knowledge-enhanced language models. In Proceedings of the international AAAI conference on web and social media, volume 16, pages 1425–1429, 2022.
- [138] Rafal Kocielnik, Sara Kangaslahti, Shrimai Prabhumoye, Meena Hari, Michael Alvarez, and Anima Anandkumar. Can you label less by using out-of-domain data? active & transfer learning with few-shot instructions. In Transfer Learning for Natural Language Processing Workshop, pages 22–32. PMLR, 2023.
- [139] Addisu Lashitew and Youqing Mu. Corporate opposition to climate change disclosure regulation in the united states. Climate Policy, pages 1–16, 2024.
- [140] Xinyu Fu, Thomas W Sanchez, Chaosu Li, and Juliana Reu Junqueira. Deciphering public voices in the digital era: Benchmarking chatgpt for analyzing citizen feedback in hamilton, new zealand. Journal of the American Planning Association, pages 1–14, 2024.
- [141] Nicholas G Napolio. Measuring executive agency ideology using large language models. Working Paper, 2024.
- [142] James Bisbee, Joshua D Clinton, Cassy Dorff, Brenton Kenkel, and Jennifer M Larson. Synthetic replacements for human survey data? the perils of large language models. Political Analysis, pages 1–16, 2024.
- [143] R Michael Alvarez, Frederick Eberhardt, and Mitchell Linegar. Generative ai and the future of elections, 2023.
- [144] Alexis Palmer and Arthur Spirling. Large language models can argue in convincing and novel ways about politics: Evidence from experiments and human judgement. Github Prepr, 2023.
- [145] R Michael Alvarez and Jacob Morrier. Evaluating the quality of answers in political q&a sessions with large language models. arXiv preprint arXiv:2404.08816, 2024.
- [146] Jonathan Mellon, Jack Bailey, Ralph Scott, James Breckwoldt, Marta Miori, and Phillip Schmedeman. Do ais know what the most important issue is? using language models to code open-text social survey responses at scale. Research & Politics, 11(1):20531680241231468, 2024.
- [147] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. Generative agents: Interactive simulacra of human behavior. In Proceedings of the 36th annual acm symposium on user interface software and technology, pages 1–22, 2023.
- [148] Chen Gao, Xiaochong Lan, Nian Li, Yuan Yuan, Jingtao Ding, Zhilun Zhou, Fengli Xu, and Yong Li. Large language models empowered agent-based modeling and simulation: A survey and perspectives. arXiv preprint arXiv:2312.11970, 2023.
- [149] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al. A survey on large language model based autonomous agents. Frontiers of Computer Science, 18(6):186345, 2024.


- [150] Gordon Dai, Weĳia Zhang, Jinhan Li, Siqi Yang, Srihas Rao, Arthur Caetano, Misha Sra, et al. Artificial leviathan: Exploring social evolution of llm agents through the lens of hobbesian social contract theory. arXiv preprint arXiv:2406.14373, 2024.
- [151] Wenyue Hua, Lizhou Fan, Lingyao Li, Kai Mei, Jianchao Ji, Yingqiang Ge, Libby Hemphill, and Yongfeng Zhang. War and peace (waragent): Large language model-based multi-agent simulation of world wars. arXiv preprint arXiv:2311.17227, 2023.
- [152] Mingyu Jin, Beichen Wang, Zhaoqian Xue, Suiyuan Zhu, Wenyue Hua, Hua Tang, Kai Mei, Mengnan Du, and Yongfeng Zhang. What if llms have different world views: Simulating alien civilizations with llm-based agents. arXiv preprint arXiv:2402.13184, 2024.
- [153] Yun-Shiuan Chuang, Agam Goyal, Nikunj Harlalka, Siddharth Suresh, Robert Hawkins, Sĳia Yang, Dhavan Shah, Junjie Hu, and Timothy T Rogers. Simulating opinion dynamics with networks of llm-based agents. arXiv preprint arXiv:2311.09618, 2023.
- [154] Zhenyu Guan, Xiangyu Kong, Fangwei Zhong, and Yizhou Wang. Richelieu: Self-evolving llm-based agents for ai diplomacy. arXiv preprint arXiv:2407.06813, 2024.
- [155] Farhad Moghimifar, Yuan-Fang Li, Robert Thomson, and Gholamreza Haffari. Modelling political coalition negotiations using llm-based agents. arXiv preprint arXiv:2402.11712, 2024.
- [156] Amir Feder, Katherine A Keith, Emaad Manzoor, Reid Pryzant, Dhanya Sridhar, Zach Wood-Doughty, Jacob Eisenstein, Justin Grimmer, Roi Reichart, Margaret E Roberts, et al. Causal inference in natural language processing: Estimation, prediction, interpretation and beyond. Transactions of the Association for Computational Linguistics, 10:1138–1158, 2022.
- [157] Swagata Ashwani, Kshiteesh Hegde, Nishith Reddy Mannuru, Mayank Jindal, Dushyant Singh Sengar, Krishna Chaitanya Rao Kathala, Dishant Banga, Vinĳa Jain, and Aman Chadha. Cause and Effect: Can Large Language Models Truly Understand Causality?, 2024. arXiv:2402.18139 [cs].
- [158] Matej Zečević, Moritz Willig, Devendra Singh Dhami, and Kristian Kersting. Causal parrots: Large language models may talk causality but are not causal. arXiv preprint arXiv:2308.13067, 2023.
- [159] Emre Kıcıman, Robert Ness, Amit Sharma, and Chenhao Tan. Causal Reasoning and Large Language Models: Opening a New Frontier for Causality, 2024. arXiv:2305.00050 [cs].
- [160] Yongqi Li, Mayi Xu, Xin Miao, Shen Zhou, and Tieyun Qian. Prompting Large Language Models for Counterfactual Generation: An Empirical Study, 2024. arXiv:2305.14791 [cs].
- [161] Amrita Bhattacharjee, Raha Moraffah, Joshua Garland, and Huan Liu. Zero-shot LLM-guided Counterfactual Generation for Text, 2024.
- [162] George Gui and Olivier Toubia. The Challenge of Using LLMs to Simulate Human Behavior: A Causal Inference Perspective. SSRN Electronic Journal, 2023. arXiv:2312.15524 [cs].
- [163] Zach Wood-Doughty, Ilya Shpitser, and Mark Dredze. Generating Synthetic Text Data to Evaluate Causal Inference Methods, February 2021. arXiv:2102.05638.
- [164] Haiyan Zhao, Hanjie Chen, Fan Yang, Ninghao Liu, Huiqi Deng, Hengyi Cai, Shuaiqiang Wang, Dawei Yin, and Mengnan Du. Explainability for large language models: A survey. ACM Transactions on Intelligent Systems and Technology, 15(2):1–38, 2024.
- [165] Haoyan Luo and Lucia Specia. From understanding to utilization: A survey on explainability for large language models. arXiv preprint arXiv:2401.12874, 2024.
- [166] Jef de Slegte, Filip Van Droogenbroeck, Bram Spruyt, Sam Verboven, and Vincent Ginis. The use of machine learning methods in political science: An in-depth literature review. Political Studies Review, page 14789299241265084, 2024.
- [167] Nikita Dhawan, Leonardo Cotta, Karen Ullrich, Rahul Krishnan, and Chris J Maddison. End-to-end causal effect estimation from unstructured natural language data. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024.
- [168] Steven Johnson and Nikita Iziev. Ai is mastering language. should we trust what it says? The New York Times, 4:15, 2022.


- [169] Yunju Kim and Heejun Lee. The rise of chatbots in political campaigns: The effects of conversational agents on voting intention. International Journal of Human–Computer Interaction, 39(20):3984–3995, 2023.
- [170] Messi HJ Lee, Jacob M Montgomery, and Calvin K Lai. Large language models portray socially subordinate groups as more homogeneous, consistent with a bias observed in humans. In The 2024 ACM Conference on Fairness, Accountability, and Transparency, pages 1321–1340, 2024.
- [171] Karolina Stańczak, Sagnik Ray Choudhury, Tiago Pimentel, Ryan Cotterell, and Isabelle Augenstein. Quantifying gender bias towards politicians in cross-lingual language models. Plos one, 18(11):e0277640, 2023.
- [172] Hang Jiang, Doug Beeferman, Brandon Roy, and Deb Roy. Communitylm: Probing partisan worldviews from language models. arXiv preprint arXiv:2209.07065, 2022.
- [173] Gabriel Simmons. Moral mimicry: Large language models produce moral rationalizations tailored to political identity. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 4: Student Research Workshop), pages 282–297, 2023.
- [174] Kobi Hackenburg and Helen Margetts. Evaluating the persuasive influence of political microtargeting with large language models. Proceedings of the National Academy of Sciences, 121(24):e2403116121, 2024.
- [175] Bart Bonikowski, Yuchen Luo, and Oscar Stuhler. Politics as usual? measuring populism, nationalism, andauthoritarianisminuspresidentialcampaigns(1952–2020)withneurallanguagemodels. Sociological Methods & Research, 51(4):1721–1787, 2022.
- [176] Florian Foos. The use of ai by election campaigns. OSF, 2024.
- [177] Chenxiao Yu, Zhaotian Weng, Zheng Li, Xiyang Hu, and Yue Zhao. Will trump win in 2024? predicting the us presidential election via multi-step reasoning with large language models. arXiv preprint arXiv:2411.03321, 2024.
- [178] Lisa P Argyle, Christopher A Bail, Ethan C Busby, Joshua R Gubler, Thomas Howe, Christopher Rytting, Taylor Sorensen, and David Wingate. Leveraging ai for democratic discourse: Chat interventions can improve online political conversations at scale. Proceedings of the National Academy of Sciences, 120(41):e2311627120, 2023.
- [179] ZIlin Ma, Yiyang Mei, Claude Bruderlein, Krzysztof Z Gajos, and Weiwei Pan. " chatgpt, don’t tell me what to do": Designing ai for context analysis in humanitarian frontline negotiations. arXiv preprint arXiv:2410.09139, 2024.
- [180] Mohaddeseh Bastan, Mahnaz Koupaee, Youngseo Son, Richard Sicoli, and Niranjan Balasubramanian. Author’s sentiment prediction. In Proceedings of the 28th International Conference on Computational Linguistics, pages 604–615, 2020.
- [181] Siva Uday Sampreeth Chebolu, Franck Dernoncourt, Nedim Lipka, and Thamar Solorio. Survey of aspect-based sentiment analysis datasets. arXiv preprint arXiv:2204.05232, 2022.
- [182] Srishti Sharma, Mala Saraswat, and Anil Kumar Dubey. Fake news detection on twitter. International Journal of Web Information Systems, 18(5/6):388–412, 2022.
- [183] Uchchhwas Saha, Md Shihab Mahmud, Aisharjo Chakrobortty, Mst Tuhin Akter, MD Rakib Islam, and Ahmed Al Marouf. Sentiment classification in bengali news comments using a hybrid approach with glove. In 2022 6th International Conference on Trends in Electronics and Informatics (ICOEI), pages 01–08, 2022.
- [184] Bayu Waspodo, Amalia Khaerunnisa Nursya Bany, Rinda Hesti Kusumaningtyas, Eri Rustamaji, et al. Indonesia covid-19 online media news sentiment analysis with lexicon-based approach and emotion detection. In 2022 10th International Conference on Cyber and IT Service Management (CITSM), pages 1–6, 2022.
- [185] MIT Election Data and Science Lab. U.S. Senate Precinct-Level Returns 2020. Harvard Dataverse, 2022.


- [186] MIT Election Data and Science Lab. U.S. House of Representatives Precinct-Level Returns 2018. Harvard Dataverse, 2022.
- [187] MIT Election Data and Science Lab. State Precinct-Level Returns 2018. Harvard Dataverse, 2022.
- [188] B Keith Payne, Jon A Krosnick, Josh Pasek, Yphtach Lelkes, Omair Akhtar, and Trevor Tompson. Implicit and explicit prejudice in the 2008 american presidential election. Journal of Experimental Social Psychology, 46(2):367–374, 2010.
- [189] Chenxiao Yu, Zhaotian Weng, Zheng Li, Xiyang Hu, and Yue Zhao. Will trump win in 2024? predicting the us presidential election via multi-step reasoning with large language models, 2024.
- [190] MIT Election Data and Science Lab. U.S. President 1976–2020. Harvard Dataverse, 2017.
- [191] Anastassia Kornilova and Vlad Eidelman. Billsum: A corpus for automatic summarization of us legislation. arXiv preprint arXiv:1910.00523, 2019.
- [192] Dong Shu, Haoran Zhao, Xukun Liu, David Demeter, Mengnan Du, and Yongfeng Zhang. Lawllm: Law large language model for the us legal system. arXiv preprint arXiv:2407.21065, 2024.
- [193] Javier Arregui and Clement Perarnaud. A new dataset on legislative decision-making in the european union: the deu iii dataset. Journal of European Public Policy, 29(1):12–22, 2022.
- [194] Kai Shu, Deepak Mahudeswaran, Suhang Wang, Dongwon Lee, and Huan Liu. Fakenewsnet: A data repository with news content, social context, and spatiotemporal information for studying fake news on social media. Big data, 8(3):171–188, 2020.
- [195] Karish Grover, SM Angara, Md Shad Akhtar, and Tanmoy Chakraborty. Public wisdom matters! discourse-aware hyperbolic fourier co-attention for social text classification. Advances in Neural Information Processing Systems, 35:9417–9431, 2022.
- [196] Zhiwei Jin, Juan Cao, Han Guo, Yongdong Zhang, and Jiebo Luo. Multimodal fusion with recurrent neural networks for rumor detection on microblogs. In Proceedings of the 25th ACM international conference on Multimedia, pages 795–816, 2017.
- [197] David E Cunningham, Kristian Skrede Gleditsch, and Idean Salehyan. Non-state actors in civil wars: A new dataset. Conflict management and peace science, 30(5):516–531, 2013.
- [198] Barış Arı. Peace negotiations in civil conflicts: A new dataset. Journal of Conflict Resolution, 67(1):150–177, 2023.
- [199] Michal Mochtak, Peter Rupnik, and Nikola Ljubešić. The parlasent multilingual training dataset for sentiment identification in parliamentary proceedings. arXiv preprint arXiv:2309.09783, 2023.
- [200] Simone Balloccu, Patrícia Schmidtová, Mateusz Lango, and Ondřej Dušek. Leak, cheat, repeat: Data contamination and evaluation malpractices in closed-source llms. arXiv preprint arXiv:2402.03927, 2024.
- [201] Kritesh Rauniyar, Sweta Poudel, Shuvam Shiwakoti, Surendrabikram Thapa, Junaid Rashid, Jungeun Kim, Muhammad Imran, and Usman Naseem. Multi-aspect annotation and analysis of nepali tweets on anti-establishment election discourse. IEEE Access, 2023.
- [202] Zhen Tan, Dawei Li, Song Wang, Alimohammad Beigi, Bohan Jiang, Amrita Bhattacharjee, Mansooreh Karami, Jundong Li, Lu Cheng, and Huan Liu. Large language models for data annotation and synthesis: A survey. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pages 930–957, 2024.
- [203] Xuran Ming, Shoubin Li, Mingyang Li, Lvlong He, and Qing Wang. Autolabel: Automated textual data annotation method based on active learning and large language model. In International Conference on Knowledge Science, Engineering and Management, pages 400–411, 2024.
- [204] Yao Qu and Jue Wang. Performance and biases of large language models in public opinion simulation. Humanities and Social Sciences Communications, 11(1):1–13, 2024.
- [205] Nima Shahbazi, Yin Lin, Abolfazl Asudeh, and HV Jagadish. Representation bias in data: A survey on identification and resolution techniques. ACM Computing Surveys, 55(13s):1–39, 2023.


- [206] Ryumei Nakada, Yichen Xu, Lexin Li, and Linjun Zhang. Synthetic oversampling: Theory and a practical approach using llms to address data imbalance. arXiv preprint arXiv:2406.03628, 2024.
- [207] Nicolas Antonio Cloutier and Nathalie Japkowicz. Fine-tuned generative llm oversampling can improve performance over traditional techniques on multiclass imbalanced text classification. In 2023 IEEE International Conference on Big Data (BigData), pages 5181–5186, 2023.
- [208] Gaurav Sahu, Olga Vechtomova, Dzmitry Bahdanau, and Issam H Laradji. Promptmix: A class boundary augmentation method for large language model distillation. arXiv preprint arXiv:2310.14192, 2023.
- [209] Amirhossein Abaskohi, Sascha Rothe, and Yadollah Yaghoobzadeh. Lm-cppf: Paraphrasing-guided data augmentation for contrastive prompt-based few-shot fine-tuning. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pages 670–681, 2023.
- [210] Vitor Gaboardi dos Santos, Guto Leoni Santos, Theo Lynn, and Boualem Benatallah. Identifying citizen-related issues from social media using llm-based data augmentation. In International Conference on Advanced Information Systems Engineering, pages 531–546. Springer, 2024.
- [211] Bosheng Ding, Chengwei Qin, Ruochen Zhao, Tianze Luo, Xinze Li, Guizhen Chen, Wenhan Xia, Junjie Hu, Anh Tuan Luu, and Shafiq Joty. Data augmentation using llms: Data perspectives, learning paradigms and challenges. arXiv preprint arXiv:2403.02990, 2024.
- [212] Biao Zhang, Zhongtao Liu, Colin Cherry, and Orhan Firat. When scaling meets llm finetuning: The effect of data, model and finetuning method. arXiv preprint arXiv:2402.17193, 2024.
- [213] Kushala VM, Harikrishna Warrier, Yogesh Gupta, et al. Fine tuning llm for enterprise: Practical guidelines and recommendations. arXiv preprint arXiv:2404.10779, 2024.
- [214] Shadi Jaradat, Richi Nayak, Alexander Paz, Huthaifa I Ashqar, and Mohammad Elhenawy. Multitask learning for crash analysis: A fine-tuned llm framework using twitter data. Smart Cities, 7(5):2422–2465, 2024.
- [215] Bingyang Wu, Ruidong Zhu, Zili Zhang, Peng Sun, Xuanzhe Liu, and Xin Jin. {dLoRA}: Dynamically orchestrating requests and adapters for {LoRA}{LLM} serving. In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24), pages 911–927, 2024.
- [216] Maxime Méloux and Christophe Cerisara. Novel-wd: Exploring acquisition of novel world knowledge in llms using prefix-tuning. arXiv preprint arXiv:2408.17070, 2024.
- [217] Adel Nabli, Louis Fournier, Pierre Erbacher, Louis Serrano, Eugene Belilovsky, and Edouard Oyallon. Acco: Accumulate while you communicate, hiding communications in distributed llm training. arXiv preprint arXiv:2406.02613, 2024.
- [218] Ziyi Guan, Hantao Huang, Yupeng Su, Hong Huang, Ngai Wong, and Hao Yu. Aptq: Attention-aware post-training mixed-precision quantization for large language models. In Proceedings of the 61st ACM/IEEE Design Automation Conference, pages 1–6, 2024.
- [219] Debarag Banerjee, Pooja Singh, Arjun Avadhanam, and Saksham Srivastava. Benchmarking llm powered chatbots: methods and metrics. arXiv preprint arXiv:2308.04624, 2023.
- [220] Alina Petrova, John Armour, and Thomas Lukasiewicz. Extracting outcomes from appellate decisions in us state courts. In Legal Knowledge and Information Systems, pages 133–142. IOS Press, 2020.
- [221] TYSS Santosh, Cornelius Weiss, and Matthias Grabmair. Lexsumm and lext5: Benchmarking and modeling legal summarization tasks in english. arXiv preprint arXiv:2410.09527, 2024.
- [222] Neel Guha, Julian Nyarko, Daniel Ho, Christopher Ré, Adam Chilton, Alex Chohlas-Wood, Austin Peters, Brandon Waldon, Daniel Rockmore, Diego Zambrano, et al. Legalbench: A collaboratively built benchmark for measuring legal reasoning in large language models. Advances in Neural Information Processing Systems, 36, 2024.
- [223] Jason Wei, Maarten Bosma, Vincent Y Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M Dai, and Quoc V Le. Finetuned language models are zero-shot learners. arXiv preprint arXiv:2109.01652, 2021.


- [224] Puneet Kumar, Kshitĳ Pathania, and Balasubramanian Raman. Zero-shot learning based cross-lingual sentiment analysis for sanskrit text with insufficient labeled data. Applied Intelligence, 53(9):10096– 10113, 2023.
- [225] Riccardo Di Leo, Chen Zeng, Elias Dinas, and Reda Tamtam. Mapping (a) ideology: A taxonomy of european parties using generative llms as zero-shot learners. Available at SSRN 4907347, 2024.
- [226] Emily Allaway and Kathleen McKeown. Zero-shot stance detection: Paradigms and challenges. Frontiers in Artificial Intelligence, 5:1070429, 2023.
- [227] Ranadheer Malla, Travis G Coan, Vivek Srinivasan, and Constantine Boussalis. Dynamic few-shot learning for computational social science. OSF, 2024.
- [228] Alapan Kuila and Sudeshna Sarkar. Deciphering political entity sentiment in news with large language models: Zero-shot and few-shot strategies. arXiv preprint arXiv:2404.04361, 2024.
- [229] Yibo Hu, Erick Skorupa Parolin, Latifur Khan, Patrick T Brandt, Javier Osorio, and Vito J D’Orazio. Synthesizing political zero-shot relation classification via codebook knowledge, nli, and chatgpt. arXiv preprint arXiv:2308.07876, 2023.
- [230] Michael Burnham, Kayla Kahn, Ryan Yank Wang, and Rachel X Peng. Political debate: Efficient zero-shot and few-shot classifiers for political text. arXiv preprint arXiv:2409.02078, 2024.
- [231] Rahman SM Wahidur, Ishmam Tashdeed, Manjit Kaur, and Heung-No Lee. Enhancing zero-shot crypto sentiment with fine-tuned language model and prompt engineering. IEEE Access, 2024.
- [232] Bingsheng Yao, Guiming Chen, Ruishi Zou, Yuxuan Lu, Jiachen Li, Shao Zhang, Yisi Sang, Sĳia Liu, James Hendler, and Dakuo Wang. More samples or more prompts? exploring effective few-shot in-context learning for llms with in-context sampling. In Findings of the Association for Computational Linguistics: NAACL 2024, pages 1772–1790, 2024.
- [233] Hazem Ibrahim, Farhan Khan, Hend Alabdouli, Maryam Almatrooshi, Tran Nguyen, Talal Rahwan, and Yasir Zaki. Analyzing political stances on twitter in the lead-up to the 2024 us election. arXiv preprint arXiv:2412.02712, 2024.
- [234] Soveatin Kuntur, Anna Wróblewska, Marcin Paprzycki, and Maria Ganzha. Under the influence: A survey of large language models in fake news detection. IEEE Transactions on Artificial Intelligence, 2024.
- [235] Bohdan M Pavlyshenko. Using gpt models for qualitative and quantitative news analytics in the 2024 us presidental election process. arXiv preprint arXiv:2410.15884, 2024.
- [236] Weiqi Hu, Ye Wang, Yan Jia, Qing Liao, and Bin Zhou. A multi-modal prompt learning framework for early detection of fake news. In Proceedings of the International AAAI Conference on Web and Social Media, volume 18, pages 651–662, 2024.
- [237] Xiaojun Chen, Ting Liu, Philippe Fournier-Viger, Bowen Zhang, Guodong Long, and Qin Zhang. A fine-grained self-adapting prompt learning approach for few-shot learning with pre-trained language models. Knowledge-Based Systems, page 111968, 2024.
- [238] Yang Wang, Alberto Garcia Hernandez, Roman Kyslyi, and Nicholas Kersting. Evaluating quality of answers for retrieval-augmented generation: A strong llm is all you need. arXiv preprint arXiv:2406.18064, 2024.
- [239] Guanting Dong, Yutao Zhu, Chenghao Zhang, Zechen Wang, Zhicheng Dou, and Ji-Rong Wen. Understand what llm needs: Dual preference alignment for retrieval-augmented generation. arXiv preprint arXiv:2406.18676, 2024.
- [240] Muhammad Arslan, Saba Munawar, and Christophe Cruz. Political-rag: using generative ai to extract political information from media content. Journal of Information Technology & Politics, pages 1–16, 2024.
- [241] Zhen-Yu Zhang, Siwei Han, Huaxiu Yao, Gang Niu, and Masashi Sugiyama. Generating chain-ofthoughts with a pairwise-comparison approach to searching for the most promising intermediate thought. In Forty-first International Conference on Machine Learning, 2024.


- [242] Waleed Kareem and Noorhan Abbas. Fighting lies with intelligence: Using large language models and chain of thoughts technique to combat fake news. In International Conference on Innovative Techniques and Applications of Artificial Intelligence, pages 253–258, 2023.
- [243] Adina Dobrinoiu. Leveraging Large Language Models for Classifying Subjective Arguments in Public Discourse. PhD thesis, Delft University of Technology, 2024.
- [244] Rasul Tutunov, Antoine Grosnit, Juliusz Ziomek, Jun Wang, and Haitham Bou-Ammar. Why can large language models generate correct chain-of-thoughts? arXiv preprint arXiv:2310.13571, 2023.
- [245] Ningyu Zhang, Yunzhi Yao, Bozhong Tian, Peng Wang, Shumin Deng, Mengru Wang, Zekun Xi, Shengyu Mao, Jintian Zhang, Yuansheng Ni, et al. A comprehensive study of knowledge editing for large language models. arXiv preprint arXiv:2401.01286, 2024.
- [246] Naman Gupta, Shashank Kirtania, Priyanshu Gupta, and Others. Stackfeed: Structured textual actor-critic knowledge base editing with feedback. arXiv preprint arXiv:2410.10584, 2024.
- [247] Ningyu Zhang, Zekun Xi, Yujie Luo, Peng Wang, Bozhong Tian, Yunzhi Yao, Jintian Zhang, Shumin Deng, Mengshu Sun, Lei Liang, et al. Oneedit: A neural-symbolic collaboratively knowledge editing system. arXiv preprint arXiv:2409.07497, 2024.
- [248] Hao Peng, Xiaozhi Wang, Chunyang Li, Kaisheng Zeng, Jiangshan Duo, Yixin Cao, Lei Hou, and Juanzi Li. Event-level knowledge editing. arXiv preprint arXiv:2402.13093, 2024.
- [249] Toufique Ahmed and Premkumar Devanbu. Better patching using llm prompting, via self-consistency. In 2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE), pages 1742–1746, 2023.
- [250] Baizhou Huang, Shuai Lu, Weizhu Chen, Xiaojun Wan, and Nan Duan. Enhancing large language models in coding through multi-perspective self-consistency. arXiv preprint arXiv:2309.17272, 2023.
- [251] Yi Cheng, Xiao Liang, Yeyun Gong, Wen Xiao, Song Wang, Yuji Zhang, Wenjun Hou, Kaishuai Xu, Wenge Liu, Wenjie Li, et al. Integrative decoding: Improve factuality via implicit self-consistency. arXiv preprint arXiv:2410.01556, 2024.
- [252] Angelica Chen, Jason Phang, Alicia Parrish, Vishakh Padmakumar, Chen Zhao, Samuel R Bowman, and Kyunghyun Cho. Two failures of self-consistency in the multi-step reasoning of llms. arXiv preprint arXiv:2305.14279, 2023.
- [253] Raisa Islam and Owana Marzia Moushi. Gpt-4o: The cutting-edge advancement in multimodal llm. Authorea Preprints, 2024.
- [254] Areeg Fahad Rasheed, M Zarkoosh, Safa F Abbas, and Sana Sabah Al-Azzawi. Taskcomplexity: A dataset for task complexity classification with in-context learning, flan-t5 and gpt-4o benchmarks. arXiv preprint arXiv:2409.20189, 2024.
- [255] Jian Chen, Vashisth Tiwari, Ranajoy Sadhukhan, Zhuoming Chen, Jinyuan Shi, Ian En-Hsu Yen, and Beidi Chen. Magicdec: Breaking the latency-throughput tradeoff for long context generation with speculative decoding. arXiv preprint arXiv:2408.11049, 2024.
- [256] Shruti Singh, Nandan Sarkar, and Arman Cohan. Scidqa: A deep reading comprehension dataset over scientific papers. arXiv preprint arXiv:2411.05338, 2024.
- [257] American National Election Studies. Anes 2016 time series study full release. https://www. electionstudies.org, 2019. [Dataset and documentation]. September 4, 2019 version.
- [258] Courtney Kennedy, Mark Blumenthal, Scott Clement, et al. An evaluation of the 2016 election polls in the united states. Public Opinion Quarterly, 82(1):1–33, 2018.
- [259] Lisa P. Argyle, Ethan C. Busby, Nancy Fulda, Joshua R. Gubler, Christopher Rytting, and David Wingate. Out of one, many: Using language models to simulate human samples. Political Analysis, 31(3):337–351, 2023.
- [260] Weihong Qi, Hanjia Lyu, and Jiebo Luo. Representation bias in political sample simulations with large language models. arXiv preprint arXiv:2407.11409, 2024.


- [261] Srĳoni Majumdar, Edith Elkind, and Evangelos Pournaras. Generative ai voting: Fair collective choice is resilient to llm biases and inconsistencies. arXiv preprint arXiv:2406.11871, 2024.
- [262] StefanSylviusWagner, MaikeBehrendt, MarcZiegele, andStefanHarmeling. Thepowerofllm-generated synthetic data for stance detection in online political discussions. arXiv preprint arXiv:2406.12480, 2024.
- [263] Leah von der Heyde, Anna-Carolina Haensch, and Alexander Wenz. Assessing bias in llm-generated synthetic datasets: The case of german voter behavior. Technical report, Center for Open Science, 2023.
- [264] Yue Huang, Zhengqing Yuan, Yujun Zhou, Kehan Guo, Xiangqi Wang, Haomin Zhuang, Weixiang Sun, Lichao Sun, Jindong Wang, Yanfang Ye, et al. Social science meets llms: How reliable are large language models in social simulations? arXiv preprint arXiv:2410.23426, 2024.
- [265] Zhan Ling, Yunhao Fang, Xuanlin Li, Zhiao Huang, Mingu Lee, Roland Memisevic, and Hao Su. Deductive verification of chain-of-thought reasoning. Advances in Neural Information Processing Systems, 36, 2024.
- [266] Canyu Chen, Baixiang Huang, Zekun Li, Zhaorun Chen, Shiyang Lai, Xiongxiao Xu, Jia-Chen Gu, Jindong Gu, Huaxiu Yao, Chaowei Xiao, et al. Can editing llms inject harm? arXiv preprint arXiv:2407.20224, 2024.
- [267] Diksha Khurana, Aditya Koli, Kiran Khatter, and Sukhdev Singh. Natural language processing: state of the art, current trends and challenges. Multimedia tools and applications, 82(3):3713–3744, 2023.
- [268] Yejin Bang, Delong Chen, Nayeon Lee, and Pascale Fung. Measuring political bias in large language models: What is said and how it is said. arXiv preprint arXiv:2403.18932, 2024.
- [269] Yue Wang, Yinlong Xu, Zihan Ma, Hongxia Xu, Bang Du, Honghao Gao, Jian Wu, and Jintai Chen. Twin-gpt: Digital twins for clinical trials via large language model. ACM Transactions on Multimedia Computing, Communications and Applications, 2024.
- [270] Scott De Marchi and Scott E Page. Agent-based models. Annual Review of political science, 17(1):1–20, 2014.
- [271] Scott De Marchi. Computational and mathematical modeling in the social sciences. Cambridge University Press, 2005.
- [272] Huaiyuan Yao, Longchao Da, Vishnu Nandam, Justin Turnau, Zhiwei Liu, Linsey Pang, and Hua Wei. Comal: Collaborative multi-agent large language models for mixed-autonomy traffic. arXiv preprint arXiv:2410.14368, 2024.
- [273] Abdolmahdi Bagheri, Matin Alinejad, Kevin Bello, and Alireza Akhondi-Asl. C2P: Featuring Large Language Models with Causal Reasoning, 2024. arXiv:2407.18069 [cs].
- [274] Thomas Jiralerspong, Xiaoyin Chen, Yash More, Vedant Shah, and Yoshua Bengio. Efficient Causal Graph Discovery Using Large Language Models, 2024. arXiv:2402.01207 [cs].
- [275] Veronika Batzdorfer. Conspiracy narratives on voat: A longitudinal analysis of cognitive activation and evolutionary psychology features. In Proceedings of the 16th ACM Web Science Conference, pages 42–47, 2024.
- [276] Aniket Vashishtha, Abbavaram Gowtham Reddy, Abhinav Kumar, Saketh Bachu, Vineeth N Balasubramanian, and Amit Sharma. Causal inference using llm-guided discovery. arXiv preprint arXiv:2310.15117, 2023.
- [277] Swagata Ashwani, Kshiteesh Hegde, Nishith Reddy Mannuru, Dushyant Singh Sengar, Mayank Jindal, Krishna Chaitanya Rao Kathala, Dishant Banga, Vinĳa Jain, and Aman Chadha. Cause and effect: Can large language models truly understand causality? In Proceedings of the AAAI Symposium Series, volume 4, pages 2–9, 2024.
- [278] Hui Bai, Jan Voelkel, Johannes Eichstaedt, and Robb Willer. Artificial intelligence can persuade humans on political issues. Osf, 2023.
- [279] MIT Election Data and Science Lab. U.S. Senate statewide 1976–2020. Harvard Dataverse, 2017.
- [280] MIT Election Data and Science Lab. U.S. House 1976–2022. Harvard Dataverse, 2017.


- [281] Emily Moore. Federal Register Final Rule Data 2000-2014. Harvard Dataverse, 2018.
- [282] Xiao Yu, Zexian Zhang, Feifei Niu, Xing Hu, Xin Xia, and John Grundy. What makes a high-quality training dataset for large language models: A practitioners’ perspective. In Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering, pages 656–668, 2024.
- [283] Haocheng Lin. Designing domain-specific large language models: The critical role of fine-tuning in public opinion simulation. arXiv preprint arXiv:2409.19308, 2024.
- [284] Chen Huang, Yang Deng, Wenqiang Lei, Jiancheng Lv, and Ido Dagan. Selective annotation via data allocation: These data should be triaged to experts for annotation rather than the model. arXiv preprint arXiv:2405.12081, 2024.
- [285] Christine P Chai. Comparison of text preprocessing methods. Natural Language Engineering, 29(3):509– 553, 2023.
- [286] Maud Ehrmann, Ahmed Hamdi, Elvys Linhares Pontes, Matteo Romanello, and Antoine Doucet. Named entity recognition and classification in historical documents: A survey. ACM Computing Surveys, 56(2):1–47, 2023.
- [287] Philipp Wicke and Marianna M Bolognesi. Red and blue language: Word choices in the trump & harris 2024 presidential debate. arXiv preprint arXiv:2410.13654, 2024.
- [288] Maria D Molina, S Shyam Sundar, Thai Le, and Dongwon Lee. “fake news” is not simply false information: A concept explication and taxonomy of online content. American behavioral scientist, 65(2):180–212, 2021.
- [289] M Abdul Khaliq, P Chang, M Ma, Bernhard Pflugfelder, and F Miletić. Ragar, your falsehood radar: Rag-augmented reasoning for political fact-checking using multimodal large language models. arXiv preprint arXiv:2404.12065, 2024.
- [290] Liat Antwarg, Ronnie Mindlin Miller, Bracha Shapira, and Lior Rokach. Explaining anomalies detected by autoencoders using shapley additive explanations. Expert systems with applications, 186:115736, 2021.
- [291] Daniel D Lundstrom, Tianjian Huang, and Meisam Razaviyayn. A rigorous study of integrated gradients method and extensions to internal neuron attributions. In International Conference on Machine Learning, pages 14485–14508. PMLR, 2022.
- [292] Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation. arXiv preprint arXiv:2302.09664, 2023.
- [293] Longchao Da, Tiejin Chen, Lu Cheng, and Hua Wei. Llm uncertainty quantification through directional entailment graph and claim level response augmentation. arXiv preprint arXiv:2407.00994, 2024.
- [294] Zhen Lin, Shubhendu Trivedi, and Jimeng Sun. Generating with confidence: Uncertainty quantification for black-box large language models. arXiv preprint arXiv:2305.19187, 2023.


