# Using Machine Learning to Test Causal Hypotheses in Conjoint Analysis

Dae Woong Ham†1, Kosuke Imai‡1,2, and Lucas Janson§1

- 1Department of Statistics, Harvard University
- 2Department of Government, Harvard University August 24, 2022


Abstract

Conjoint analysis is a popular experimental design used to measure multidimensional preferences. Researchers examine how varying a factor of interest, while controlling for other relevant factors, inﬂuences decision-making. Currently, there exist two methodological approaches to analyzing data from a conjoint experiment. The ﬁrst focuses on estimating the average marginal eﬀects of each factor while averaging over the other factors. Although this allows for straightforward design-based estimation, the results critically depend on the distribution of other factors and how interaction eﬀects are aggregated. An alternative model-based approachcancomputevariousquantitiesofinterest, butrequiresresearchersto correctlyspecify the model, a challenging task for conjoint analysis with many factors and possible interactions. In addition, a commonly used logistic regression has poor statistical properties even with a moderate number of factors when incorporating interactions. We propose a new hypothesis testing approach based on the conditional randomization test to answer the most fundamental question of conjoint analysis: Does a factor of interest matter in any way given the other factors? Our methodology is solely based on the randomization of factors, and hence is free from assumptions. Yet, it allows researchers to use any test statistic, including those based on complex machine learning algorithms. As a result, we are able to combine the strengths of the existing design-based and model-based approaches. We illustrate the proposed methodology through conjoint analysis of immigration preferences and political candidate evaluation. We also extend the proposed approach to test for regularity assumptions commonly used in conjoint analysis. An open-source software package is available for implementing the proposed methodology.1

We thank Naoki Egami for advice. Imai thanks the Alfred P. Sloan Foundation for partial support (Grant # 2020– 13946). Ham and Janson were partially supported by a CAREER grant from the National Science Foundation (Grant # DMS-2045981).

†Email: daewoongham@g.harvard.edu ‡Email: imai@harvard.edu, URL: https://imai.fas.harvard.edu §Email: ljanson@fas.harvard.edu, URL: http://lucasjanson.fas.harvard.edu 1The proposed methodology is implemented via an open-source software R package CRTConjoint, available

through the Comprehensive R Archive Network (https://cran.r-project.org/package=CRTConjoint).

## 1 Introduction

Conjoint analysis, introduced more than half a century ago (Luce and Tukey, 1964), is a factorial survey-based experiment designed to measure preferences on a multidimensional scale. Under a commonly used “forced-choice” design, respondents are presented with two alternative proﬁles of randomly selected attributes (e.g., candidates with diﬀerent traits or products with diﬀerent features). They are then asked to choose their preferred proﬁle. Conjoint analysis has been extensively used by marketing ﬁrms to determine desirable product characteristics (e.g., Bodog and Florian, 2012; Green, Krieger and Wind, 2001). Recently, it has gained popularity among social scientists (Hainmueller, Hopkins and Yamamoto, 2014; Raghavarao, Wiley and Chitturi, 2010) who are interested in studying individual preferences concerning elections (e.g., Ono and Burden, 2018), immigration (e.g., Hainmueller and Hopkins, 2015), employment (e.g., Popovic, Kuzmanovic and Martic, 2012), and other issues.

When analyzing conjoint experiments, the design-based approach, pioneered by Hainmueller, Hopkins and Yamamoto (2014), has been by far the most popular among social scientists. The main advantage of this nonparametric approach is its simplicity—it uses the diﬀerence-in-means estimator or linear regression to infer the average marginal component eﬀect (AMCE) of each factor by averaging over the distribution of other factors. However, because the AMCE makes inferences about the marginal eﬀects averaged over all the other factors, it may fail to capture important interactions. This is potentially problematic given that practitioners tend to use AMCE-based conﬁdence intervals that are narrow and contain zero to conclude that a factor has a weak causal eﬀect (Hainmueller, Hopkins and Yamamoto, 2014; Hainmueller and Hopkins, 2015; Ono and Burden, 2018). However, a narrow AMCE-based conﬁdence interval containing zero only implies that a factor has a weak marginal eﬀect, not necessarily that its total causal inﬂuence is weak.

A possible solution is the model-based approach that ranges from traditional parametric regression models (McFadden, 1973; Green and Srinivasan, 1990; Campbell, Mhlanga and Lesschaeve, 2013) to more recent machine learning algorithms (Egami and Imai, 2019; de la Cuesta, Egami and Imai, 2022; Abramson et al., 2020; Bansak et al., 2020; Goplerud, Imai and Pashley, 2022). While this approach can eﬃciently estimate various quantities of interest, it has the potential drawback of model misspeciﬁcation, producing biased inference. Although researchers can reduce model misspeciﬁcation by adopting a more complicated model (e.g., adding interaction terms of increasing order), such an approach can substantially reduce statistical power and produce invalid -values even when the model is correctly speciﬁed (Candès and Sur, 2018). While subgroup analysis, a common practice to analyze only a subset of the data, is simpler, it suﬀers from well-known problems of multiple testing and -hacking, which are of serious concern in conjoint analysis given a large number of possible causal eﬀects of interest (see, e.g., Szucs, 2016; Harking, 2021). Finally, the use of machine learning algorithms, which is becoming increasingly common, cannot yield even consistent estimates in high-dimensional settings without strong assumptions.

In this paper, we propose a new approach to analyzing data from conjoint analysis that combines the strengths of the existing design-based and model-based approaches (Section 3). Speciﬁcally, we show how to conduct assumption-free hypothesis testing based on the conditional randomization test (CRT; Candès et al., 2018). In the causal inference literature, the CRT has been used to test interference between units (Aronow, 2012; Athey, Eckles and Imbens, 2018) and in other causal applications such as genetic studies (Bates et al., 2020). Instead of focusing on a particular causal eﬀect, we ask the most fundamental question of conjoint analysis: Does a factor of interest matter

in any way given the other factors? The proposed approach allows one to answer this question with greater statistical power than the AMCE by utilizing ﬂexible machine learning algorithms but without making any assumption about the underlying causal structure (e.g., presence or absence of interaction eﬀects, patterns of heterogeneous eﬀects, or within-respondent correlation across proﬁle comparisons). Despite its ﬂexibility, the CRT has an attractive statistical property that the resulting -values are exactly valid regardless of the sample size or the number of factors. We also extend the proposed approach to test whether speciﬁc factor levels of interest, rather than all levels of a factor, inﬂuence respondent preferences in any way (Section 3.4).

The proposed methodology can also test the validity of assumptions commonly invoked in conjoint analysis (Hainmueller, Hopkins and Yamamoto, 2014) (Section 3.5). First, we show how to test for the presence of the proﬁle order eﬀect. Under the forced conjoint design, for example, reversing the order in which two proﬁles are presented within each evaluation may change the choice of proﬁle. Second, we test the assumption of no carryover eﬀect, which states that each respondent’s response only depends on the current proﬁles and is not aﬀected by previous evaluations. This assumption may be violated if respondents learn over several proﬁle evaluations. Third, we test the assumption of no fatigue eﬀect, which precludes the possibility that as respondents evaluate more proﬁles, they get tired and answer questions diﬀerently (Bansak et al., 2018, 2019). Thus, the proposed hypothesis testing approach can serve as the ﬁrst step of analyzing conjoint data without assumptions, complementing existing approaches that estimate causal quantities of interest.

After presenting the proposed methodology, we conduct simulation studies in Section 4 to show that the CRT can achieve a higher statistical power than the AMCE by exploiting machine learning algorithms to detect complex treatment interactions. For empirical illustration, we apply the proposed methodology to two existing conjoint analyses (Section 5). The ﬁrst pertains to immigration preferences among United States (U.S.) citizens. While some researchers contend that U.S. citizens generally prefer high-skilled immigrants regardless of their countries of origin, others have suggested that racially prejudiced respondents discriminate against non-European immigrants (Hainmueller and Hopkins, 2015; Newman and Malhotra, 2019). By combining machine learning algorithms with the CRT, we ﬁnd that respondents do diﬀerentiate according to whether immigrants are from Mexico or European countries. The second application considers the role of gender in candidate evaluation (Ono and Burden, 2018). The original analysis found that voters discriminate between male and female candidates only for presidential elections but not for Congressional elections. However, a recent study suggests that this ﬁnding about congressional candidates may critically depend on the distribution of other characteristics such as partisanship and policy positions (de la Cuesta, Egami and Imai, 2022). We apply the proposed methodology and show that gender does play a statistically signiﬁcant role in voter evaluation of Congressional candidates.

We emphasize that the CRT complements other existing methods by oﬀering a useful test of whether a factor of interest matters at all. The test can be useful even when the AMCE fail to detect any statistically signiﬁcant result.

## 2 Empirical Application

In this section, we brieﬂy describe two empirical applications concerning the role of ethnocentrism in immigration preferences and gender discrimination in political candidate evaluations. We also outlinethelimitationsofthecommonlyusedapproachbasedontheAMCEtomotivatetheproposed

methodology. In Section 5, we revisit these applications and apply our hypothesis testing approach.

### 2.1 Role of Country of Origin in Immigration Preference

Immigration is one of the most contentious issues in the United States today. A large body of literature investigates how cultural, economic, and racial factors shape public attitudes towards immigration (see, e.g., Hainmueller and Hopkins, 2014, and references therein). In an inﬂuential study, Hainmueller and Hopkins (2015) use a conjoint analysis to empirically examine the immigrant characteristics favored or disfavored by U.S. citizens. The survey was ﬁelded between December 2011 and January 2012 on a nationally representative sample of U.S. citizens. The study used the forced-choice design, in which each respondent was presented with a pair of hypothetical immigrant proﬁles and asked which immigrant they would “personally prefer to see admitted to the United States.” Each of 1,396 respondents rated 5 pairs of proﬁles.

An immigrant proﬁle consists of nine factors—prior trips to the U.S., reason for application, country of origin, language skills, profession, job experience, employment plans, education level, and gender, each of which has multiple levels (see Table 2 of Appendix D as well as the original article for details). Most factors are independently and uniformly randomized across their levels with the exception of two restrictions to avoid implausible pairs. First, immigrant proﬁles that list escape persecution as the “reason of immigration” can only have Iraq, Sudan, or Somalia as their “country of origin”. Second, a high-skill “profession” such as ﬁnancial analyst, research scientist, doctor, and computer programmer is possible only if the “education level” is at least 2 years of college. This restricted randomization scheme induces dependencies between these factors that must be properly accounted for when analyzing the data. The survey also contains information about respondents’ age, education, ethnicity, gender, and ethnocentrism. The study contains a random sample of 14,018 proﬁles.

In this study, Hainmueller and Hopkins estimate the AMCE, which represents the marginal eﬀect of a factor of interest averaging over the other factors. Based on the statistically insigniﬁcant estimates for the AMCEs of the “country of origin” factor for Mexico and European countries (reproduced in Figure 1), they conclude that “despite media frames focusing on low-skilled, unauthorized immigration from Mexico, there is little evidence of penalty speciﬁc to Mexicans.” (p. 539). The authors obtain these estimates by ﬁtting a linear regression model, where the outcome variable indicates whether the proﬁle is selected and the predictors are the nine randomized factors. To account for the restricted randomization, they also include two sets of interaction terms, one between “country of origin” and “reason of immigration” and the other between “profession” and “education level”. To obtain the estimated AMCE of Germany, for example, Hainmueller and Hopkins take the main eﬀect of Germany (the baseline is India) and then add it to the average of all the interaction terms between Germany and the “reason of immigration” factor. Clustered standard errors are computed by clustering on each respondent to account for dependency within a respondent.

Despite this overall ﬁnding, the AMCE-based approach may mask relevant interactions and heterogeneous treatment eﬀects. Indeed, Hainmueller and Hopkins conduct a subgroup analysis and ﬁnd that the “country of origin” factor has statistically signiﬁcant interactions with the respondents’ ethnocentrism. They measure ethnocentrism using the feeling thermometer score (ranging from 0 to 100) for the respondent’s own groups minus the average feeling thermometer across the other groups. In addition, Newman and Malhotra (2019) reanalyze the same dataset and estimate three-

|-0.1<br><br>0.0<br><br>0.1<br><br>France Mexico Germany Poland<br><br>AMCE|
|---|


###### AMCE

- Figure 1: The estimated Average Marginal Component Eﬀects (AMCEs) of immigrants’ countries of origin in the Hainmueller and Hopkins (2015) study. The plot shows the estimated AMCEs for France, Germany, Mexico, and Poland, which represent the average diﬀerences in the estimated probability of choosing an immigrant proﬁle with a speciﬁc level of the “country of origin” factor, marginalizing other attributes. The baseline factor level is India, and the 95% conﬁdence intervals are also shown.


way interactions among respondents’ ethnocentrism, “country of origin”, and “profession”. The authors compute the AMCEs of high-skilled immigrants (baseline of janitor) separately for each country of origin and respondent’s ethnocentric group. They ﬁnd that these AMCEs are diﬀerent between Mexican and European immigrants when compared among highly ethnocentric respondents (see Figure 1 in Newman and Malhotra, 2019, for further details).

In this paper, we apply the proposed hypothesis testing approach to testing whether or not immigrants from Mexico and those from Europe are viewed diﬀerently in any way while controlling for all the other experimental factors as well as the respondent characteristics. The rejection of this null hypothesis would mean that the country of origin of an individual plays a statistically signiﬁcant role in some United States citizens’ preferences about that individual’s immigration to the United States.

### 2.2 Role of Gender in Political Candidate Evaluation

Perhaps the most common political science application of conjoint analysis is the measurement of voters’ candidate preferences. Recently, several scholars have used conjoint analysis to study the role of gender discrimination in candidate evaluation (e.g., Ono and Burden, 2018; Teele, Kalla and Rosenbluth, 2018). We revisit the study by Ono and Burden (2018) which examines whether voters prefer candidates of one gender over those of another after controlling for other candidate characteristics.2 The study is based on a sample of voting-eligible adults in the U.S. collected in March 2016 and also uses the forced-choice conjoint design. The following 13 factors are independently and uniformly randomized across their levels: gender, age, race, family, experience in public oﬃce, salient personal characteristics, party aﬃliation, policy area of expertise, position on national security, position on immigrants, position on abortion, position on government deﬁcit, and favorability among the public (see Table 3 in Appendix D and the original article for details). The survey also contains information about the respondents’ educational background, gender, age, region, social

2This study treats gender as a binary factor with levels Male and Female.

0.02

0.00

###### AMCE

−0.02

−0.04

Congress President

- Figure 2: The estimated Average Marginal Component Eﬀect (AMCE) of candidate’s gender in the Ono and Burden


(2018) study. We present the estimates for congressional candidates (left) and presidential candidates (right). The 95% conﬁdence intervals are also shown.

class, partisanship, political interest, and ethnocentrism. There were 1,583 respondents each given 10 tasks, resulting in 15,830 observations, half of which were for congressional candidates and the other half for presidential candidates.

The original study yields a negative estimate of the AMCE of female candidates, relative to male counterparts, for presidential candidates. However, the estimated AMCE of female candidates is not statistically distinguishable from zero for congressional candidates, based on a simple -test for the coeﬃcient of Male from the linear regression with cluster standard errors. This ﬁnding led to the authors’ conclusion that gender discrimination “is limited to presidential rather than congressional elections” (p. 583). Figure 2 reproduces these AMCE estimates. Like the immigration example, the authors ﬁt a linear regression with all fourteen factors as predictors to obtain these estimates.

In this paper, we use the CRT to formally test whether the gender of congressional candidates matters in any way for voters’ preferences while controlling for the other candidate characteristics. The rejection of this null hypothesis would indicate that gender does matter even for congressional candidates.

### 2.3 Limitations of Existing Approaches

Although the AMCE is a useful causal quantity of interest and can be easily and reliably estimated, it is not free of limitations. The AMCE is a marginal eﬀect based on two types of averaging: (1) averaging over the distribution of other attributes, and (2) averaging over the responses (and hence respondents). Recall that in the standard causal inference setting with a binary treatment, a zero average treatment eﬀect does not necessarily imply zero treatment eﬀect for everyone. The treatment may beneﬁt some and harm others, and these positive and negative eﬀects can cancel out through averaging. The AMCE suﬀers from a similar problem, potentially masking important causal heterogeneity if there are interactions among attributes and/or between attributes and respondent characteristics. In the immigration conjoint experiment described above, for example, the overall AMCE estimates suggest little diﬀerence across countries of origin. And yet Hainmueller and Hopkins show that respondents with high ethnocentrism may have a certain preference over certain countries of origin when compared to those with low ethnocentrism.

Additionally, although an AMCE-based conﬁdence interval that does not contain zero represents evidence that the factor matters, a narrow AMCE-based conﬁdence interval that contains zero only implies that a factor has a weak marginal eﬀect. Nevertheless, practitioners tend to use narrow AMCE-based conﬁdence intervals that contain zero to conclude that a factor does not matter. For example, Hainmueller, Hopkins and Yamamoto (2014) conclude that the “candidates’ income does not matter much” and that the “candidates’ racial and ethnic backgrounds are even less inﬂuential”, based on the AMCE-based conﬁdence interval for income and ethnicity (p. 19). Similarly, Ono and Burden conclude that gender eﬀects are “limited to only Congressional candidates” (p. 3), based on AMCE-based conﬁdence interval of gender for Congressional candidate.

Although the AMCE is popular in conjoint analysis, especially among political scientists, there also exist model-based approaches to ﬂexibly estimate potentially any quantity of interest. In particular, logistic regression remain a popular model-based alternative in conjoint analysis (McFadden, 1973; Green and Srinivasan, 1990; Campbell, Mhlanga and Lesschaeve, 2013) especially in marketing research.3 Despite the ﬂexibility of logistic regression, model misspeciﬁcation remains a signiﬁcant challenge. Although researchers may add more interactions to account for all possible eﬀects, such an approach can reduce statistical power and more importantly lead to invalid -values (Candès and Sur, 2018). We show in Appendix J Figure 9 that using logistic regression and accounting for all two-way interactions to reduce model misspeciﬁcation can easily lead to invalid

-values.

Consequently, a consensus among researchers has emerged that ﬂexible machine learning algorithms are necessary for capturing these causal interactions (de la Cuesta, Egami and Imai, 2022; Abramson et al., 2020; Bansak et al., 2020; Goplerud, Imai and Pashley, 2022). Yet machine learning algorithms, despite their ﬂexibility, cannot yield consistent estimates in high-dimensional settings without strong assumptions. In addition, statistical inference in small samples remains a challenge (Dezeure et al., 2015; Chernozhukov et al., 2017; Imai and Li, 2021). Our goal is to address these problems through an assumption-free approach based on the conditional randomization test.

## 3 The Proposed Methodology

In this section we describe the proposed methodology based on the Conditional Randomization Test (CRT; Candès et al., 2018). We show how to apply the CRT to conjoint analysis in order to test whether a factor of interest matters, without making any assumptions. We discuss various test statistics that can be used with the CRT and several useful extensions for conjoint analysis.

### 3.1 Notation and Setup

For concreteness, we focus on the forced-choice conjoint design, under which a respondent is asked to choose one of two proﬁles. Our methodology is general and can be extended to other designs. Let be the total number of respondents. As is often done in practice, suppose that each respondent evaluates pairs of proﬁles, yielding a total of responses (for notational simplicity, we assume the same number of evaluations for each respondent).

3Although a hierarchical modeling approach remains another popular model-based alternative in conjoint studies, we do not consider it here because it is based on a Bayesian framework rather than frequentist approach taken in this paper (Andrews, Ansari and Currim, 2002).

We use {0,1} to represent the binary outcome variable for evaluation by respondent

, which equals 1 for selecting the left proﬁle and 0 for choosing the right proﬁle. Although for convenience we use “left” and “right” to distinguish two proﬁles under each evaluation, the proﬁles do not necessarily have to be placed side by side on the actual survey platform. We use the following ×1 stacked vector representation for this outcome variable = [ 1; 2;…; ], where

= [ 1; 2;…; ] of dimension × 1 denotes the outcome variable for respondent . We use [ 1; 2;…; ] to denote a vertical stacking of vectors or matrices 1, 2,…,  . We often observe some characteristics of the respondents, and we use to denote a × -dimensional matrix of pre-treatment covariates for respondent that are repeated across rows.

Next, let represent the total number of attributes or factors used for each conjoint proﬁle. We use a scalar   {1,2,…,  } to denote the value of the th factor of interest for evaluation by respondent , where the superscript distinguishes the factors for the left ( ) and right ( ) proﬁles,

and 2 is the total number of factor levels for factor . We use = [ 1;…; ] to denote a -dimensional column vector, containing all factors of interest for the left proﬁle for respondent

in the th evaluation where . We deﬁne similarly for the right proﬁle. In addition, we use

= [ ; ] as a column vector of length 2 to represent the main factors of interest from two proﬁles together. Lastly, the remaining ( − ) factors are denoted by = [ ; ], where each term is similarly deﬁned. For example in the immigration conjoint experiment, if the main factor of interest is “country of origin”, the other factors include “education” and “profession”.

As done for the outcome variable, we stack all evaluation-speciﬁc factors to deﬁne respondentlevel factor matrices, which are further combined to yield the factor matrix = [ 1; 2;…; ] and = [ 1; 2;…; ] of dimension × 2 and × 2( − ), respectively, where = [ 1; 2;…; ] and = [ 1; 2;…; ] are matricies of dimension × 2 and × 2( − ), respectively. Lastly, we also stack all respondent characteristics = [ 1; 2;…; ] of dimension

× . Finally, we use ( , ) to denote the -dimensional vector of the potential outcomes when

= and = . This notation implies that we avoid assuming the no interference eﬀect in the Stable Unit Treatment Value Assumption (SUTVA) since our vector of potential outcomes is a function of the entire set of treatments and (Rubin, 1990). We assume a super-population framework, where the potential outcomes ( , ) are assumed to be drawn from a population of inﬁnite size. In Appendix B, we discuss how our framework is related to a ﬁnite-population framework, which is the basis of Fisher’s randomization test. In conjoint analysis, the proﬁle attributes are randomized according to a known distribution, ( , ). Our framework is general, allowing for any randomization distribution. For example, some may randomize each factor independently using complete randomization whereas others may induce dependency among factors by removing a certain set of attribute combinations. In general, the randomization of the factors implies the following independence relation,

( , ) ( , ) for all , and , (1)

where we use and to represent the support of and that of , respectively (see Chapter 3.6 of (Imbens and Rubin, 2015)).

### 3.2 The Conditional Randomization Test

The Conditional Randomization Test (CRT) is an assumption-free approach that combines designbased inference with ﬂexible machine learning algorithms. For ease of presentation, we ﬁrst introduce the CRT without incorporating the respondent characteristics and then return in Section 3.6 to show how can be incorporated in all the proposed methods. The CRT allows us to examine whether the factors of interest change the response while holding the other factors constant. Speciﬁcally, we test the following null hypothesis,

- 0 ( , ) = ( , ) for all , , and , (2)

where we use = to denote distributional equality. As a reminder, 0 states that our entire vector of potential outcomes are equal in distribution for any values of . Our alternative hypothesis states that aﬀects in some way while keeping unchanged. This is formalized as,

- 1 ( , ) ( , ) for some , , and . (3)


We emphasize that the null hypothesis deﬁned in Equation (2) implies the absence of any causal eﬀects involving the main factor(s) of interest. For example, the null hypothesis is false if aﬀects

for any individual respondent or subgroup of respondents. Similarly, the null hypothesis does not hold if inﬂuences only when takes a certain set of values. Thus, the null hypothesis precludes any heterogeneous or interaction eﬀects as well.

Contrast this hypothesis test formulation with that of the standard AMCE-based analysis, which asks whether each factor of interest matters on average. More speciﬁcally, Hainmueller, Hopkins and Yamamoto assume each individual’s potential outcome is only a function of its own proﬁle task, i.e., ( , ) = ( , ), and computes the marginal importance of by averaging each individual potential outcome over as well as the respondents, which are assumed to be exchangeable, leading to the following null hypothesis,

0 { ( , )} = { ( , )}, (4)

AMCE

where and are the speciﬁed values of the main factors and the expectation is taken over (other factors) and the respondents. As brieﬂy explained in Section 2.3, the limitation of the AMCE-based approach is that averaging over other factors can mask important causal interaction and heterogeneity.

We now establish the equivalence between the null hypothesis about the potential outcomes deﬁned in Equation (2) and the conditional independence relation among observed variables. This result allows us to use the CRT, which is a general assumption-free methodology for testing conditional independence relations in designed experiments (Candès et al., 2018). We state this result as the following theorem whose proof is given in Appendix A.

Theorem 3.1 (Equivalence). The null hypothesis deﬁned in Equation (2) is equivalent to the following conditional independence hypothesis under the randomization assumption of Equation (1),

CRT

0 .

Algorithm 1: Conditional Randomization Test (CRT) Input: Data ( , , ), test statistic ( , , ), total number of re-samples , conditional

distribution ; for = 1,2,…,  do

Sample ( ) from the distribution of conditionally independently of and ; Output: -value  = 1 +1 1 + =1 { ( ( ), , ) ( , , )} 4

The CRT is a general assumption-free methodology in designed experiments that produces exact -values without asymptotic approximation. The CRT combines the advantages of both designbased and model-based approaches by enabling the use of any test statistic, including ones based on complex machine learning (ML) algorithms, while making no modeling assumptions. In the conjoint analysis literature, researchers have used traditional regression modeling (e.g., Barone, Lombardo and Tarantino, 2007; Hauber et al., 2016; McFadden, 1973) and more recently modern ML algorithms (e.g., Egami and Imai, 2019; Abramson et al., 2020). However, the validity of these analyses critically depends on modeling assumptions, parameter tuning, and/or asymptotic approximation. In contrast, the CRT assumes nothing about the conditional distribution of the outcome given ( , ). Indeed, it does not even require the data to be independently or identically distributed, a property which we use later to test carryover and proﬁle order eﬀects. The only requirement is the speciﬁcation of the conditional distribution of given , which is readily available from the experimental design of conjoint analysis. Although the power of the CRT critically depends on the test statistic, the CRT always controls type 1 error no matter what the true model is. This contrasts with other model based approaches that require modeling assumptions to be valid (see Appendix J for more details).

Algorithm 1 summarizes the general procedure used to compute the exact -value for the CRT. Note that if and are independently randomized, as is often the case, one can simply sample ( ) from the marginal distribution of . If, on the other hand, certain combinations of and values (e.g., doctor without a college degree in the immigration conjoint experiment) are excluded, then we must use the appropriate conditional distribution of given . Critically, Algorithm 1 is valid for complicated experimental designs, so long as one can sample from the conditional distribution given . The CRT can be computationally intensive since it requires computing the test statistic a total of +1 times. However these computations can easily be parallelized. Furthermore, recent works (Tansey et al., 2018; Liu et al., 2020) have shown that certain test statistic constructions also alleviate the need for these computations. In Appendix I, we detail several tricks that can be used to dramatically reduce the computation time when implementing the CRT. For the main application results presented in Section 5 (ﬁrst column of Table 1), we note that the parallelized computational time was approximately six minutes with 50 cores to calculate each -value with = 2,000. Our software package makes it easy for practitioners to use multiple cores and provides a step-by-step instruction for using many cores on Amazon Web Services.5

- 4We add one to the numerator and denominator so that the distribution of the -value is stochastically dominated by the uniform distribution as suggested by (Candès et al., 2018).
- 5The detailed instructions and example use cases can be found in a vignette of our open-source software package in https://cran.r-project.org/web/packages/CRTConjoint/vignettes/CRTConjoint.html.


The -value of the CRT is valid6 regardless of sample size and test statistic (Candès et al., 2018). To see this, it suﬃces to recognize that under the null hypothesis all +1 test statistics, ( , , ),

( (1), , ), …, ( ( ), , ), are exchangeable given ( , ). While any test statistic produces a valid -value under the CRT, the choice of test statistic determines the statistical power. We now turn to this practically important consideration.

### 3.3 Test Statistics

To obtain a powerful test statistic that does not mask important interactions, we consider a test statistic based on the Lasso logistic regression with hierarchical interactions, or HierNet (Bien, Taylor and Tibshirani, 2013). We note that if researchers wish to target main eﬀects without considering interactions, the -statistic from a standard linear regression of the response on is a reasonable test statistic to use. HierNet allows for the regularization of all possible two-way interaction terms while respecting their hierarchy. Speciﬁcally, HierNet constrains the two-way interaction eﬀects to be smaller in magnitude than their corresponding main eﬀects. For example, this implies that a two-way interaction eﬀect will be set to zero if its relevant main eﬀects are all zero. A stricter regularization on the interactions is desirable because the space of possible two-way interactions is large and grows quadratically, and we expect many to be indistinguishable from zero. Lastly, when ﬁtting HierNet, we use the dummy variable encoding (i.e., each factor level is represented by its own dummy variable) but do not omit the baseline level. We can ﬁt this overparameterized model because of the regularization of HierNet. The primary advantage of this approach is that the results are no longer dependent on the choice of baseline levels (Egami and Imai, 2019).

We begin by considering the simplest case where we have a single main factor of interest ( = 1). Without loss of generality, we assume that this is the ﬁrst factor among the total of factors. There are two types of interaction eﬀects to consider (de la Cuesta, Egami and Imai, 2022). First, a within-proﬁle interaction eﬀect represents the interaction between one level of the main factor and another level of a diﬀerent factor within the same proﬁle. Second, a between-proﬁle interaction eﬀect represents the factor interaction between two proﬁles (left versus right) that are being compared under the forced choice design.

Our proposed test statistic is based on the sum of relevant squared main and interaction eﬀects after subtracting their respective means,

HierNet =

1

( − )2

+

=1

=2

1

( 1 − 1 )2

+

=1 =1

=1

1

( 1 − 1 )2

,

=1 =1

(5)

main eﬀects

within-proﬁle interaction eﬀects

between-proﬁle interaction eﬀects

where is the estimated main eﬀect coeﬃcient for the th level of our factor of interest with

denoting the average of these estimated main eﬀect coeﬃcients, and 1 and 1 represent the estimated within-proﬁle and between-proﬁle interaction eﬀect coeﬃcients between the th level of the factor of interest and the th level of the th factor, respectively. Similar to the main eﬀects,

1 and 1 denote the averages of their corresponding estimated interaction eﬀect coeﬃcients. We do not consider third or higher order interactions because of the typical sample size in a conjoint

6That is, under 0, ( -value ) for all   [0,1].

experiment and a lack of powerful methods to detect such interactions. However, in Section 5 we illustrate how to incorporate third order interactions when prior substantive knowledge is available.

This test statistic can be easily generalized to the setting where there is more than one factor of interest ( > 1). In such a case, we simply compute Equation (5) for each factor of interest, and then sum the resulting values to arrive at the ﬁnal test statistic. HierNet aims to capture any diﬀerential eﬀects the levels of have on the response through their main eﬀects and relevant interaction eﬀects. For example, suppose that is “gender” in the political candidate conjoint experiment (Section 2.2). Under 0, we would expect all main eﬀects and any interaction eﬀects of male and female to be roughly equivalent, thus making HierNet close to zero. However, suppose that male candidates with a certain “education level” were favored more than female candidates with a certain “education level”. Then, we would expect these interactions to diﬀer, making HierNet further from zero.

We use cross-validation7 to choose the value of HierNet’s tuning parameter, which controls the degree of regularization. In addition, when the sample size and the number of factors are large, ﬁtting HierNet can be computationally demanding. To alleviate this issue, we propose computational speedups of the HierNet test statistics, which are detailed in Appendix I. In particular, we drop when ﬁtting the HierNet tuning parameter via cross-validation. Since this computationally expensive step does not depend on , we do not need to re-run it for each .

So far, we have constructed our test statistic as if there is no proﬁle order eﬀect. This implies that the eﬀects of each factor do not depend on whether it belongs to the left or right proﬁle. Formally, we have imposed the following symmetry constraints in our HierNet test statistic,

= = − , 1 = = − , = − , (6)

where the superscripts and denote the left and right proﬁle eﬀects, respectively. denotes the between proﬁle interaction between the th level of factor in the left proﬁle with the th level of factor in the right proﬁle.8 The signs of the estimated coeﬃcients reﬂect the fact that the response variable is recorded as 1 if the left proﬁle is chosen and as 0 if the right proﬁle is selected. These constraints reduce the dimension of parameters to be estimated by half.

Importantly, the validity of the proposed tests does not depend on whether the assumption of no proﬁle order eﬀect holds. Through simulations, Figure 4 of Appendix E shows that these constraints can signiﬁcantly increase statistical power when there is no proﬁle order eﬀect. To incorporate this symmetry constraint, we append another copy of the dataset below the original data set, where the appended copy is identical to the original dataset except that the order of left and right proﬁles is ﬂipped and the response variable is transformed as − before ﬁtting HierNet (see Appendix E for details). In Section 3.5, we show how to use the CRT for testing the validity of the assumption of no proﬁle order eﬀect.

Because the validity of the CRT does not depend on modeling assumptions, one can incorporate a variety of assumptions into test statistics. In general, test statistics have a greater statistical power

- 7The CRT remains valid if used with cross-validation so long as the resampled test statistics based on similarly uses cross-validation. This ensures exchangeability.
- 8Equation (6) also implies that the between-proﬁle interactions in Equation (5) for the same factor obey = − for any factor and levels  ,  . In particular this implies that = 0, i.e., between-proﬁle interactions of the same factor and same level are zero, while are counted twice in Equation (5), i.e., between-proﬁle interactions of the same factor and levels and are counted twice in Equation (5).


if the assumptions hold in the true (unknown) data generating process. Therefore, as much as possible the choice of test statistic should reﬂect researchers’ substantive knowledge as illustrated in one of our empirical analyses (see Section 5.2).

### 3.4 Generalization of the Null Hypothesis and Test Statistic

Researchers are often interested in testing only a few levels of interest as opposed to testing the whole factor. Yet, simply dropping the observations that correspond to those irrelevant factor levels can lead to a loss of statistical power. An advantage of the formulation described below is that we can retain all observations including those whose factor levels are irrelevant, which can improve statistical power. For example, suppose we are interested in how respondents diﬀerentiate immigrants from Mexico and Germany. If the way in which respondents diﬀerentiate between immigrants from Mexico and those from China is diﬀerent from how they distinguish between immigrants from Germany and those from China, then this implies that the respondents are viewing immigrants from Mexico diﬀerently than those from Germany. Therefore, detecting any diﬀerences for even the irrelevant levels may help improve the statistical power.

Here, we generalize the null hypothesis and test statistic, given in Equations (2) and (5), so that the methodology can accommodate any combinations of factor levels. We introduce a coarsening function that groups factor levels of interest while assigning other factor levels to themselves. Formally, this coarsening function is deﬁned as , where . Thus, for our aforementioned immigration example, will assign the same value to immigrants from Mexico and Germany while leaving all other combinations mapped to diﬀerent values.

Under this setup, we can test the null hypothesis that speciﬁc levels within do not aﬀect the potential outcome in any way. Formally,

0 ( , ) = ( , ) for all , , such that ( ) = ( ) and . (7) The condition ( ) = ( ) enables the comparison of the factor levels of interest alone. Additionally, 0 is a special case of 0 General when the coarsening function is the identity function. Finally, applying the same argument as the one used to prove Theorem 3.1, it can be shown that 0 General is equivalent to the following conditional independence relation,

General

( ), . (8)

To test this null hypothesis, we ﬁrst ﬁt the same HierNet with the main eﬀects and two-way interaction eﬀects. To incorporate the coarsening function , our test statistic takes the same form as the one given in Equation (5) but is based only on the estimated coeﬃcients that correspond to the factor levels of the group induced by the function, i.e., Mexico and Germany in the above example. Appendix F.1 contains further details of testing the general null hypothesis and the corresponding

CRT algorithm. In Section 5.1, we also provide an example of applying 0 General that contains more details on this test statistic. Under our framework, we do not need to drop observations that have

irrelevant factor levels, thus increasing statistical power as mentioned above. Finally, Appendix C details how to further generalize 0 General when a researcher is interested in grouping factor levels, i.e., combining levels France, Germany, and Poland into one level Europe when testing 0 General. Although coarsening via also involved “grouping” levels, the grouping described in Appendix C aggregates factor levels to allow comparison between higher-level categories while the coarsening

function allows us to focus our hypothesis test only on diﬀerences between a subset of factor levels of interest.

### 3.5 Testing the Regularity Assumptions of Conjoint Analysis

To further demonstrate the ﬂexibility of the CRT, we also show how to use the CRT for testing the validity of several commonly made assumptions of conjoint analysis. Although we were interested in rejecting 0 above, we are interested in accepting the null hypothesis for the hypotheses presented in this section. Therefore, we propose test statistics that are designed to be reasonably powerful for general settings in conjoint analysis.

Proﬁle Order Eﬀect. The assumption of no proﬁle order eﬀect states that changing the order of proﬁles, i.e., left versus right, does not aﬀect the actual proﬁle chosen (since the value of corresponds to whether the left or right proﬁle is chosen, should be recoded as − when the proﬁle order is changed). We denote the potential outcome ( , , , ), which is now a function of left and right proﬁles. Although not necessary, we assume here no interference between responses for notational clarity (see Appendix F.2 for the general case). Lastly, we use ind and ind to denote the support of [ ; ] and that of [ ; ] respectively, representing the support of factors used in each individual’s evaluation (hence “ind” in the subscript).

We formally state the assumption of no proﬁle order eﬀect as the following null hypothesis that reordering of the left and right proﬁles has no eﬀect on the adjusted response:

0 ( , , , ) = 1 − ( , , , ), for all  , ,[ ; ]   ind, [ ; ]   ind.

Order

We modify the HierNet test statistic in Equation (5) with the same HierNet ﬁt on ( , , ) but without enforcing the constraints in Equation (6) as,

Order

HierNet( , , ) =

=1 =1

+ 2 +

=1 =1 =1 =1

+ 2

+ 2 .

+

=1 =1 =1 =1

Since the symmetry constraints given in Equation (6) must hold under 0 Order, a large value of this test statistic indicates a potential violation of the null hypothesis. To conduct the CRT for testing

0 , we resample and recompute our test statistics. Appendix F.2 provides details about the testing procedure.

Order

Carryover Eﬀect. Researchers also often rely on the assumption of no carryover eﬀect (Hainmueller, Hopkins and Yamamoto, 2014). The assumption states that the order of the evaluations each respondent performs has no eﬀect on the outcomes. This assumption is violated, e.g., if respondents use information from their previous evaluations when assessing a given pair of proﬁles. To test this carryover eﬀect, we assume no interference across respondents but consider potential interference across evaluations within each respondent.

Let  ,1 ( −1) represent all the proﬁle attributes that were presented to respondent from the ﬁrst evaluation to the ( − 1)th evaluation. Then, the potential outcome can be written as a function of both current and previous proﬁles, i.e.,  ,1 ( −1),  ,1 ( −1), , for 2, where we assume no interference between respondents but allow intereference within a respondent. Our null hypothesis is that, for a given evaluation 2, the response is independent of all the previous proﬁles conditional on the current proﬁles:

Carryover

0  ,1 ( −1),  ,1 ( −1), , =  ,1 ( −1),  ,1 ( −1), , ,

where for all 1, 2,  ,1 ( −1),  ,1 ( −1) ind −1,  ,1 ( −1),  ,1 ( −1) ind −1, ind, ind with ind −1 and ind −1 denoting the support of  ,1 ( −1) and that of  ,1 ( −1), respectively.

We test this null hypothesis by using a test statistic that targets whether the immediately preceding evaluation aﬀects the current evaluation. We believe targeting the lag-1 eﬀect in the test statistic is reasonable because if a carryover eﬀect exists, respondents are likely to be aﬀected most by the immediately preceding evaluation. For example, if respondents believe that they have placed too much weight on proﬁles’ professions in the previous evaluation, they might decide to rely on the current proﬁles’ “country of origin” factor more than its “profession” factor in order to balance across evaluations. Under this scenario, we would expect a signiﬁcant interaction between previous proﬁles’ “profession” factor and current proﬁles’ “country of origin” factor.

We modify the test statistic given in Equation (5) in the following way. Suppose that is even (if is odd, simply consider − 1 evaluations). We ﬁrst deﬁne a new response vector

= [ 2; 4;…; ] by taking every other evaluation. Similarly, we can deﬁne new factors of interest = [[ 1; 1] ;[ 3; 3] ,…;[  , −1;  , −1] ] and a new set of conditioning variables = [[ 2; 2] ;[ 4; 4] ,…;[ ; ] ]. We then ﬁt HierNet with the new response

= [ 1; 2;…; ] on ( , ), where = [ 1; 2;…; ] and is deﬁned similarly. For this particular scenario, HierNet will estimate all main eﬀects and interaction eﬀects of

, and the interaction eﬀects between and , which are of primary interest. To increase the power of the test, we set all main and interaction eﬀects of to zero since we do not expect the previous proﬁle alone to impact the respondent’s choice. Furthermore, we also do not expect the interaction eﬀects between and to diﬀer, depending on the ordering (left versus right) of the relevant factors. Therefore, we enforce all these interaction eﬀects to have equal magnitude as done in Equation (6) (see Appendix E for further details). This leads to the following test statistic,

Carryover

2 ,

HierNet ( , , ) =

=1 =1 =1 =1

where represents the coeﬃcient of an interaction term between the th level of the th factor of the proﬁle used in the previous evaluation and the th level of the th factor of the proﬁle used in the current evaluation. Appendix F.2 explains how to resample the test statistic in this setting.

Fatigue Eﬀect. Researchers may be concerned that a respondent performing a large number of conjoint evaluations may experience the “fatigue eﬀect,” resulting in a declining quality of responses. Recently, Bansak et al. (2018) conducted an empirical study, in which they examine how the pattern of responses depends on the number of evaluations each respondent performs. While

a typical conjoint experiment asks each respondent to carry out 5 to 10 evaluations, the authors increase this number up to 30 evaluations. They ﬁnd that the results are robust to increasing the number of evaluations. Here, we show how to use the CRT to formally test the presence of the fatigue eﬀect.

Similar to the carryover eﬀect, we investigate whether there is a fatigue eﬀect within each respondent’s potential outcome ( , ), where we again assume no interference eﬀect as done when testing no proﬁle order eﬀect. We test the following null hypothesis that the potential outcome is unaﬀected if respondent evaluated the same pair of proﬁles ( , ) but at a later or earlier evaluation :

Fatigue

0 ( , ) = ( , ) for all  , ,  , ind, and ind.

We propose a similar HierNet test statistic that reﬂects a scenario where respondents will only pay attention to a shrinking number of factors as they rate more proﬁles. In this case, we would expect interactions between the factors and the evaluation order index = ( 1, 2,…,  ), which represents an -dimensional integer vector with = (1,2,…, ) for all = 1,2,…, . Again, for the sake of statistical power, we impose the absence of proﬁle order eﬀects on HierNet as done in Equation (5). Our proposed test statistic is the following from a HierNet ﬁt of on ( , , ),

Fatigue

2 ,

HierNet( , , , ) =

=1 =1

where represents the coeﬃcient of an interaction term between and level of factor . Appendix F.2 shows how to resample and recompute the test statistics to test 0 Fatigue.

### 3.6 Incorporating Respondent Characteristics

In conjoint experiments, researchers often expect factors of interest to interact strongly with respondent characteristics (Ono and Burden, 2018; Hainmueller and Hopkins, 2015; Newman and Malhotra, 2019). It is possible to exploit this fact when applying the CRT by directly incorporating respondent characteristics, , into the test statistic. Doing so can substantially increase the statistical power.

We incorporate respondent characteristics in the CRT procedure by appending to and holding both ( , ) constant. Since respondent characteristics are not randomized factors, unlike , is not guaranteed to be independent of the potential outcomes. We can test the following causal null hypothesis that conditions upon ,

0 ( , ) = ( , )   for all , , and . (9)

Theorem 3.1 can be easily extended to show that this null hypothesis is equivalent to the conditional independence relation , . Algorithm 1 also stays the same except we sample from the distribution of   ( , ) and our test statistic is now a function of ( , , , ).

A major beneﬁt of incorporating respondent characteristics is the ability to capture respondent characteristic interactions into the test statistic. Consequently, we incorporate an additional predic-

tor when ﬁtting HierNet and modify the HierNet test statistic in Equation (5) as,

HierNet =

1

( − )2

+

=1

=2

1

( 1 − 1 )2

=1 =1

main eﬀects

within-proﬁle interaction eﬀects

(10)

1

1

( 1 − 1 )2

( 1 − 1 )2

+

+

,

=1 =1

=1

=1 =1

=1

respondent interaction eﬀects

between-proﬁle interaction eﬀects

where 1 represents the interaction between the th level of our factor of interest and the th level of the th factor of a respondent characteristic. If a respondent characteristic is a numeric variable, we could either coarsen it into a factor variable or directly include it in the model as a numeric variable.9 Again, 1 denotes the average of these estimated interaction coeﬃcients. Similar to Equation (10), we add the additional constraint that = = , where the superscript and similarly denotes the left and right proﬁle eﬀects. Finally, we modify HierNet Order similarly by adding =1 =1 =1 =1( + )2 to the original test statistic in HierNet Order to account for respondent characteristic interactions. For all empirical applications in Section 5, we incorporate and use the modiﬁed test statistics to test 0 and the no proﬁle order eﬀect.

## 4 Simulation Studies

A primary advantage of the CRT is that it can yield powerful statistical tests by incorporating machinelearningalgorithmstocapturecomplexinteractionsinhighdimensions. TheCRTachieves thiswhilemaintainingtheﬁnitesamplevalidityoftheresulting -values. Inthissection, weconduct simulation studies to show that the CRT with the HierNet test statistic can be substantially more powerful than the AMCE-based test.

For simplicity, our simulation setting assumes one evaluation for each respondent ( = 1). We show additional simulations with multiple evaluations with respondent random eﬀects in Figure 7 of Appendix G.4. In addition, there is only one main factor of interest ( = 1) and ten other factors and no . Each factor is assumed to have two levels and is independently and uniformly randomized. To clearly separate main and interaction eﬀects, we use the sum-to-zero constraint by coding each binary factor as (−0.5,0.5). Our response model, Pr( = 1   , ), follows a logistic regression that includes main eﬀects for ( , ) and within-proﬁle and between-proﬁle interaction eﬀects between and and among . Our setup also has no proﬁle order eﬀects.

Our goal is to examine the diﬀerence in statistical power between the CRT and AMCE-based tests in the presence of interactions. Thus, we vary the size of the interaction eﬀect as well as the number of non-zero interaction eﬀects between and . Throughout all of our simulations, we use an eﬀect size of 0.1 for all main eﬀects for ( , ) and an eﬀect size of 0.05 for all interactions among and ﬁx the sample size to = 3,000. We also make all non-zero interactions between and equal in size for all simulations. As shown in Appendix G.2, the power of the CRT remains

9HierNet standardizes all variables when performing the ﬁt. Therefore, even if a numeric variable is on a diﬀerent scale, all estimated coeﬃcients remain comparable.

AMCE CRT

1.00

1.00

0.75

0.75

Power

0.50

0.50

0.25

0.25

0.00

0.00

0 10 20 30 40

0 5 10 15

% Variance explained by interaction

##### Number of interactions

- Figure 3: The ﬁgure shows how the power of the CRT and AMCE-based tests varies as the size of interaction eﬀects (left plot) or the number of non-zero interaction eﬀects (right) increases. The AMCE-based test (red circles) is based on the -test from the estimated regression coeﬃcient. The CRT uses the HierNet test statistic given in Equation (5). The sample size is = 3,000. Finally, the standard errors are negligible with a maximum value of 0.016.


identical if there are heterogeneous interaction eﬀects with varying sizes. Appendix G provides further details of our simulation setup.

For each simulated data set, we test the null hypothesis of no causal eﬀect using the CRT and AMCE-based approaches. We then compute the proportion of times each test rejects the null hypothesis. For the CRT, we use the HierNet test statistic given in Equation (5) obtained by ﬁtting the response on our predictors ( , ) and enforcing the constraints shown in Equation (6). For the AMCE, we use the -test based on the estimated regression coeﬃcient of obtained through ﬁtting the response on a single predictor .10

The left plot of Figure 3 shows how the statistical power of each test varies as the size of interaction eﬀects between and increases. The number of non-zero interaction eﬀects between and is ﬁxed at six. For ease of interpretation, we plot the percentage of total outcome variance explained by the interaction eﬀects between and on the -axis.11 In our setup, the total variance represents the outcome variance explained by all main and interaction eﬀects under the latent representation of the logistic regression model (see Appendix G for details). Consistent with our theoretical expectation, the CRT (blue triangles) becomes more powerful than the AMCE-based test (red circles) as the interaction size increases. For example, when the interaction size is strong enough to account for about 30% of the total variance, the CRT is approximately 20 percentage points more powerful than the AMCE-based test. When there is no interaction eﬀect, the CRT is

- 10Although this is a valid procedure to compute the AMCE estimate for , practitioners typically compute the AMCE estimates of all factors ( , ) simultaneously with a single linear regression of on all ( , ). Figure 6 of Appendix G.3 shows that the power of the AMCE remains indistinguishable when using all factors ( , ) in a single linear regression. Lastly, although our goal is to compare the CRT with the AMCE, we acknowledge that practitioners may also use the omnibus -test for testing interactions by including all the two-way interactions. We show in Appendix J that such an approach leads to inﬂated -values, thus we omit this as a baseline comparison here.
- 11The -axis ticks correspond to interaction sizes of 0,0.025,0.05,0.075,0.1, and 0.125, respectively. For example, the 20% point on the -axis refers to an interaction size of 0.05.


only slightly less powerful (by about 3 percentage points) than the AMCE-based test.

The right plot of Figure 3 shows how the power of the tests change as one varies the number of non-zero interaction eﬀects. The size of interaction eﬀects is ﬁxed to 0.06, around half the size of the main eﬀect. We ﬁnd that as expected, the CRT becomes more powerful than the AMCEbased test as the number of interaction increases. For example, when there are twelve interactions the CRT is approximately 10 percentage points more powerful than the AMCE-based test. Even when there is no interaction eﬀect at all, the loss of statistical power is minimal. Appendix E presents additional simulation results, showing that the use of no proﬁle order constraints given in

- Equation (6) increases the power of test.

5 Application to Conjoint Experiments

In this section, we apply the proposed CRT to the two conjoint studies introduced in Section 2.

- 5.1 Immigration Preferences and Ethnocentrism


We begin our analysis of the immigration conjoint experiment by testing whether respondents differentiate between immigrants from Mexico and those from European countries. We use the same data set as the one used in Hainmueller and Hopkins (2015). This gives us a total sample of 6,980 observations with = 1,396 respondents each rating = 5 tasks. Our main factor of interest is the “country of origin” variable. Since we are only interested in testing how respondents diﬀerentiate Mexican and European candidates, we use the generalized hypothesis 0 General deﬁned in

- Equation (7) and coarsen the three levels — Germany, France, and Poland — into one level called


Europe (see Appendix C for a formal treatment). Furthermore, the function in 0 General takes the “country of origin” variable and maps the relevant levels of Mexico and Europe to one output

and the remaining levels to other unique outputs. We include all the other randomized factors and respondent characteristics (see Section 2.1) as and , respectively, except the ethnocentrism variable, which is only measured for a subset of respondents. We incorporate this variable at the end of this section.

We ﬁt HierNet using as the response and our main factor , other randomized factors , and respondent characteristics as the predictors. We then compute the test statistic given in Equation (10) while imposing the implied no proﬁle order eﬀect constraints given in Equation (6) (with the constraints applied to the respondent characteristic interactions too). As mentioned brieﬂy in Section 3.4, we slightly modify this test statistic by only using the estimated coeﬃcients for Mexico and Europe while ignoring the other coeﬃcients.

As shown in the left upper cell of Table 1, the CRT -value of this test statistic is 0.042, providing evidence that respondents diﬀerentiate immigrants from Mexico and Europe. For comparison, we also compute the -value based on the estimated AMCE of being from Mexico compared to being from Europe. We apply a commonly used linear regression approach described in Section 2.1 to compute this -value. Speciﬁcally, we ﬁrst ﬁt a linear regression model using “country of origin”, “reason of immigration”, and their interaction as predictors to account for the restricted randomization (Hainmueller, Hopkins and Yamamoto, 2014). The standard errors are clustered by respondent. We then use the -test of the linear equality constraint that implies the null hypothesis under the

CRT AMCE Proﬁle order eﬀect Carryover eﬀect Fatigue eﬀect

Immigration 0.042 0.27 0.80 0.12 0.45 Gender 0.026 0.93, 0.40 0.15 0.97 0.66

- Table 1: The -values based on the Conditional Randomization Test (CRT) and the Average Marginal Component Eﬀect (AMCE) Estimation. The two rows represent the diﬀerent applications. The ﬁrst two columns present the values from the HierNet-based CRT and AMCE-based test statistics. The ﬁrst row presents the -values for testing whether the immigrant’s “country of origin” (Mexico or Europe) matters for immigration preferences while the second row tests whether candidate’s “gender” matters for voters’ preferences of Congressional candidates, respectively. The second AMCE-based -value for “gender” corresponds to a fair comparison with the CRT-based -value by additionally testing the “gender” interaction with the candidate’s “party aﬃliation” (Democratic or Republican). The remaining columns report the -values for testing no proﬁle order eﬀect, no carryover eﬀect, and no fatigue eﬀect for the respective application.


linear model. As shown in the upper cell of the second column of Table 1, the resulting -value for the diﬀerence between Mexico and Europe is 0.27, which is statistically insigniﬁcant.

The above result suggests that the CRT may be able to capture complex interactions and yield greater statistical power than the AMCE-based test. The two largest interactions in the observed test statistic are within-proﬁle interactions between “country of origin” and “education” and between “country of origin” and “prior trips to U.S.” factors, which included whether or not the immigrant entered the U.S. illegally. Thus, we next assess the degree to which the interaction eﬀects account for this diﬀerence in statistical power. To do this, we use a Lasso logistic regression without interaction terms where we only include the main eﬀects of ( , , ). The CRT -value of using only the relevant levels of the main eﬀects of as the test statistic is 0.082, which is somewhat larger than the -value based on HierNet test statistic. This suggests that interactions play some role in yielding a more powerful test than the AMCE-based approach.

Hainmueller and Hopkins suggest that respondents do not diﬀerentiate between immigrants from Mexico and those from Europe based on the results of their main analysis (see Figure 1, which replicates this analysis). However, they also conduct a subgroup analysis and ﬁnd that “country of origin” has statistically signiﬁcant interaction(s) with the respondent’s ethnocentrism through a subgroup analysis (see also Newman and Malhotra, 2019, for related ﬁndings). Thus, we now repeat the same analysis as above except that we include this ethnocentrism variable as an additional respondent characteristic in . Note that unlike the original analysis, we do not dichotomize this variable and use the original continuous scale. Since ethnocentrism is only measured for white and black respondents, the number of total respondents is reduced to = 1,135. Despite this reduction in sample size, the inclusion of the ethnocentrism variable produces the -value of 0.019, which is smaller than the -value of the analysis without this variable. As expected, the largest interaction in the observed test statistic involves the ethnocentrism variable. All together, our analysis provides evidence that respondents diﬀerentiate immigrants from Mexico and Europe.

Lastly, we use the CRT to test the the three commonly made regularity assumptions of conjoint analysis: no proﬁle order eﬀect, no carryover eﬀect, and no fatigue eﬀect. The last three columns in Table1presentthe -valuesfromthevarioustestsdescribedinSection3.5. Weﬁndnoevidencethat these assumptions are violated in the immigration conjoint experiment (the ﬁrst row). In particular, the fact that we do not detect proﬁle order eﬀects suggests that imposing the symmetry constraint as done in Equation (6) likely improves power.

### 5.2 Role of Gender in Candidate Evaluation

For the gender conjoint experiment, we test whether or not the gender of Congressional candidates matters in voter preferences. We use the same data as the one used in Ono and Burden (2018). The Congressional dataset consists of 7,915 observations with 5 tasks performed by each of = 1,583 respondents. Our main factor of interest is a binary variable representing male or female. In addition, we use the remaining 12 randomized factors and all the respondent characteristics

(see Section 2.2). We test the main null hypothesis 0 introduced in Section 3.2.

As mentioned in Section 3.3, the use of substantive knowledge can improve the power of the test. To demonstrate this, we leverage the Presidential candidate dataset from the same conjoint experiment to ﬁnd the strongest interaction with the gender of candidates. We then include this interaction term as an additional main eﬀect in HierNet when computing the test statistic given in Equation (10).12 By including it as a main eﬀect, HierNet applies less shrinkage on this interaction term. In addition, HierNet will consider potential three-way interactions involving this interaction term and other variables in . The power will be greater if strong interactions in the Presidential candidate data are also present in the Congressional candidate data.

To ﬁnd the strongest interaction in the Presidential candidate dataset, we obtain a CRT -value for each variable in ( , ) with a test statistic that focuses on the interaction strength for the corresponding variable under consideration. Speciﬁcally, the test statistic uses Lasso logistic regression with all main eﬀects of ( , , ) and an additional interaction between and one variable from ( , ) (see Appendix H for more details). We choose the variable with the lowest -value as the strongest interaction. The Presidential data shows that the candidate’s “party aﬃliation” (Democratic or Republican) had the most signiﬁcant interaction with their “gender”. Appendix H contains further details and a robustness check by repeating the same analysis but choosing the variable with the second lowest -value as the additional main eﬀect.

As shown in the second row of Table 1, the CRT -value using the HierNet test statistic is 0.026, showing that gender may matter even for Congressional candidates. We ﬁnd the largest two interactions in the observed test statistic were two three-way interactions: one between “gender”, “party aﬃliation”, and “respondent’s political interest” and the other between “gender”, “party afﬁliation”, and the “respondent’s party aﬃliation”. This result is consistent with the ﬁndings in de la Cuesta, Egami and Imai (2022), which suggests the existence of higher order interactions involving party aﬃliation. We assess the role of interaction eﬀects using the same procedure above in the immigration example. The resulting CRT -value from a Lasso logistic regression with only the main eﬀects of ( , , ) and the additional interaction with “gender” and “party aﬃliation” is 0.15, suggesting that the other interactions were also helpful in detecting signiﬁcance.

For comparison, we compute the -value based on the estimated AMCE of “gender” for Congressional candidates as presented in Figure 2. Similar to the common strategy used for the immigration conjoint experiment, we ﬁt a linear regression model using “gender” as the sole predictor while clustering standard errors by respondents. We ﬁnd that the -value is 0.89. However, since the CRT leveraged the Presidential candidate data to up-weight the interaction with “party aﬃliation”, we also create a fair comparison by obtaining analogous -values for the AMCE. To do this,

12Our test statistic HierNet( , , , ) is not only a function of the Congressional dataset ( , , , ) but also the entire presidential dataset ( ). Therefore, we must now hold all ( , , ) ﬁxed in the resampling procedure. However, this does not change Algorithm 1 and the resulting -value remains valid because ( , , ) is still an independent fair coin ﬂip between the levels of male and female.

we again ﬁt a linear regression using “gender” but with an additional main eﬀect of “party aﬃliation” and the interaction of “gender” and “party aﬃliation”. We then report the -value from a

- -test for both the main eﬀect of “gender” and the interaction with “party aﬃliation”. The resulting
- -value is 0.40, showing that the AMCE-based result remains statistically insigniﬁcant. Finally, the


last three columns in the second row show no evidence that the regularity assumptions are violated for this conjoint experiment.13

## 6 Concluding Remarks

Conjoint analysis is a popular methodology for analyzing multi-dimensional preferences and decision making. In this paper, we propose an assumption-free approach for conjoint analysis based on the conditional randomization test (CRT). The proposed methodology allows researchers to test whether a set of factors of interest matter at all without assuming a statistical model. We also extend the proposed methodology to test for diﬀerential eﬀects for any combination of factor levels and other regularity assumptions commonly invoked in conjoint analysis like the proﬁle order effect. Unlike the standard AMCE analysis, the CRT can avoid masking important interactions due to averaging over other factors. When constructing CRT test statistics, researchers can use machine learning algorithms and/or domain knowledge to detect complex interactions among factors, without making modeling assumptions. The CRT is easy to implement and provides exact (i.e., non-asymptotic) -values that are valid even in high dimensions. We believe that this ﬂexibility combined with its assumption-free nature makes the CRT a powerful tool for conjoint analysis. The CRT can complement the existing methods like the AMCE analysis by providing a useful way to examine whether a factor of interest matters at all.

13We only test the no proﬁle order eﬀect assumption for Congressional candidates because this is the data relevant to the research question. However, for testing the carryover eﬀect and fatigue eﬀect, we use the full dataset including the Presidential candidates in order to increase power.

## References

Abramson, Scott, Korhan Kocak, Asya Magazinnik and Anton Strezhnev. 2020. Improving Preference Elicitation in Conjoint Designs using Machine Learning for Heterogeneous Eﬀects. Technical Report. The Annual Summer Meeting of the Society for Political Methodology.

Andrews, Rick L., Asim Ansari and Imran S. Currim. 2002. “Hierarchical Bayes versus Finite Mixture Conjoint Analysis Models: A Comparison of Fit, Prediction, and Partworth Recovery.” Journal of Marketing Research 39:87–98. URL: https://doi.org/10.1509/jmkr.39.1.87.18936

Aronow, Peter M. 2012. “A General Method for Detecting Interference Between Units in Randomized Experiments.” 41:3–16.

Athey, Susan, Dean Eckles and Guido W. Imbens. 2018. “Exact P-values for Network Interference.” Journal of the American Statistical Association 113:230–240.

Bansak, Kirk, Jens Hainmueller, Daniel Hopkins and Teppei Yamamoto. 2020. “Using Conjoint Experiments to Analyze Elections: The Essential Role of the Average Marginal Component Eﬀect (AMCE).” SSRN Electronic Journal.

- Bansak, Kirk, Jens Hainmueller, Daniel J. Hopkins and Teppei Yamamoto. 2018. “The Number of Choice Tasks and Survey Satisﬁcing in Conjoint Experiments.” Political Analysis 26:112–119.

- Bansak, Kirk, Jens Hainmueller, Daniel J. Hopkins and Teppei Yamamoto. 2019. “Beyond the breaking point? Survey satisﬁcing in conjoint experiments.” Political Science Research and Methods.


Barone, Stefano, Alberto Lombardo and Pietro Tarantino. 2007. “A weighted logistic regression for conjoint analysis and Kansei engineering.” Quality and Reliability Engineering International 23:689 – 706.

Bates, Stephen, Matteo Sesia, Chiara Sabatti and Emmanuel Candès. 2020. “Causal inference in genetic trio studies.” Proceedings of the National Academy of Sciences 117:24117–24126. URL: https://www.pnas.org/content/117/39/24117

Bien, Jacob, Jonathan Taylor and Robert Tibshirani. 2013. “A lasso for hierarchical interactions.” Ann. Statist. 41:1111–1141.

Bodog, Simona and G.L. Florian. 2012. “Conjoint Analysis in Marketing Research.” Journal of Electrical and Electronics Engineering 5:19–22.

Campbell, Benjamin L, Saneliso Mhlanga and Isabelle Lesschaeve. 2013. “Consumer Preferences for Peach Attributes: Market Segmentation Analysis and Implications for New Marketing Strategies.” Agricultural and resource economics review 42:518–541.

Candès, Emmanuel J. and Pragya Sur. 2018. “The phase transition for the existence of the maximum likelihood estimate in high-dimensional logistic regression.” arXiv: Methodology.

Candès, Emmanuel, Yingying Fan, Lucas Janson and Jinchi Lv. 2018. “Panning for Gold: Model-X Knockoﬀs for High-dimensional Controlled Variable Selection.” Journal of the Royal Statistical Society: Series B 80:551–577.

Chernozhukov, Victor, Mert Demirer, Esther Duﬂo and Iv’an Fern’andez-Val. 2017. Generic Machine Learning Inference on Heterogenous Treatment Eﬀects in Randomized Experiments. Papers No. 1712.04802. arXiv.org. URL: https://ideas.repec.org/p/arx/papers/1712.04802.html

de la Cuesta, Brandon, Naoki Egami and Kosuke Imai. 2022. “Improving the External Validity of Conjoint Analysis: The Essential Role of Proﬁle Distribution.” Political Analysis 30:19–45.

Dezeure, Ruben, Peter Bühlmann, Lukas Meier and Nicolai Meinshausen. 2015. “HighDimensionalInference: ConﬁdenceIntervals, -ValuesandR-Softwarehdi.”Statist.Sci.30:533– 558. URL: https://doi.org/10.1214/15-STS527

Egami, Naoki and Kosuke Imai. 2019. “Causal Interaction in Factorial Experiments: Application

to Conjoint Analysis.” Journal of the American Statistical Association 114:529–540. Fisher, Ronald A. 1935. The Design of Experiments. London: Oliver and Boyd Chapter II. Goplerud, Max, Kosuke Imai and Nicole E. Pashley. 2022. Estimating Heterogeneous Causal

Eﬀects of High-Dimensional Treatments: Application to Conjoint Analysis. Technical Report. arxiv:2201.01357.

Green, Paul, Abba Krieger and Yoram Wind. 2001. “Thirty Years of Conjoint Analysis: Reﬂections and Prospects.” Interfaces 31:S56–S73.

Green, Paul E. and V. Srinivasan. 1990. “Conjoint Analysis in Marketing: New Developments with Implications for Research and Practice.” Journal of Marketing 54:3–19.

- Hainmueller, Jens and Daniel J. Hopkins. 2014. “Public Attitudes Toward Immigration.” Annual Review of Political Science 17:225–249.

- Hainmueller, Jens and Daniel J. Hopkins. 2015. “The Hidden American Immigration Consensus: A Conjoint Analysis of Attitudes toward Immigrants.” American Journal of Political Science.


Hainmueller, Jens, Daniel J. Hopkins and Teppei Yamamoto. 2014. “Causal Inference in Conjoint Analysis: Understanding Multidimensional Choices via Stated Preference Experiments.” Political Analysis 22:1–30.

Harking, Andrade. 2021. “Cherry-Picking, P-Hacking, Fishing Expeditions, and Data Dredging and Mining as Questionable Research Practices.” Frontiers in Psychology 16.

Hauber, A. Brett, Juan Marcos González, Catharina G.M. Groothuis-Oudshoorn, Thomas Prior, Deborah A. Marshall, Charles Cunningham, Maarten J. IJzerman and John F.P. Bridges. 2016. “Statistical Methods for the Analysis of Discrete Choice Experiments: A Report of the ISPOR Conjoint Analysis Good Research Practices Task Force.” Value in Health 19:300 – 315.

Imai, Kosuke and Michael Lingzhi Li. 2021. “Experimental Evaluation of Individualized Treatment Rules.” Journal of the American Statistical Association.

Imbens, Guido W. and Donald B. Rubin. 2015. Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction. Cambridge University Press.

Liu, Molei, Eugene Katsevich, Lucas Janson and Aaditya Ramdas. 2020. “Fast and Powerful Conditional Randomization Testing via Distillation.” arXiv preprint arXiv:2006.03980.

Luce, R.Duncan and John W. Tukey. 1964. “Simultaneous conjoint measurement: A new type of fundamental measurement.” Journal of Mathematical Psychology 1:1 – 27.

McFadden, Daniel. 1973. Frontiers of Econometrics (eds. P. Zarembka). New York: Academic Press Chapter Conditional Logit Analysis of Qualitative Choice Behavior, pp. 105–142.

Newman, Benjamin J. and Neil Malhotra. 2019. “Economic Reasoning with a Racial Hue: Is the Immigration Consensus Purely Race Neutral?” The Journal of Politics 81:153–166.

Ono, Yoshikuni and Barry C. Burden. 2018. “The Contingent Eﬀects of Candidate Sex on Voter Choice.” Political Behavior.

Popovic, Milena, Marija Kuzmanovic and Milan Martic. 2012. “Using Conjoint Analysis To Elicit Employers’ Preferences Toward Key Competencies For A Business Manager Position.” Management - Journal for theory and practice of management 17:17–26.

Raghavarao, D., J.B. Wiley and P. Chitturi. 2010. Choice-based conjoint analysis: Models and Designs. Chapman and Hall/CRC.

Rubin, Donald B. 1990. “Comments on “On the Application of Probability Theory to Agricultural Experiments. Essay on Principles. Section 9” by J. Splawa-Neyman translated from the Polish and edited by D. M. Dabrowska and T. P. Speed.” Statistical Science 5:472–480.

Szucs, Denes. 2016. “A Tutorial on Hunting Statistical Signiﬁcance by Chasing N.” Frontiers in Psychology 7:1444. URL: https://www.frontiersin.org/article/10.3389/fpsyg.2016.01444

Tansey, Wesley, Victor Veitch, Haoran Zhang, Raul Rabadan and David Blei. 2018. “The Holdout Randomization Test: Principled and Easy Black Box Feature Selection.”.

Teele, Dawn Langan, Joshua Kalla and Frances Rosenbluth. 2018. “The Ties That Double Bind: Social Roles and Women’s Underrepresentation in Politics.” American Political Science Review 112:525–541.

## A Proof of Theorem 3.1

Proof. We ﬁrst prove that if , then ( , ) = ( , ) for any , and . ( = ) = ( = , = )

= ( ( , )   = , = )

= ( ( , )   = )

= ( ( , )),

where the third and fourth equalities follow from the randomization of and that of , respectively. Similarly, we can show ( = ) = ( ( , )), thus we have shown ( ( , )) = ( ( , )) for any , and .

To the prove the other direction, we want to show that ( , ) = ( , ) implies , or equivalently ( = , = ) = ( = , = ) for any value of and any value of , .

( ( , )) = ( ( , )   = )

= ( ( , )   = , = )

= ( = , = ),

where the ﬁrst two equalities follow from the randomization of and that of , respectively. The same argument shows ( ( , )) = ( = , = ). Finally, because ( , ) = ( , ) we have that ( ( , )) = ( ( , )), implying ( = , = ) = ( = , = ) for any value of and any value of , .

| |
|---|


## B Relation to Finite-Population Inference

In Section 3, we introduced 0 under the super-population framework. Here, we consider the relationship between 0 and Fisher’s sharp null of no treatment eﬀect (Fisher, 1935). Under the ﬁnite-population framework where the potential outcomes are ﬁxed and the randomness comes only from the randomization of treatment assignment, if we assume no interference between units, 0 reduces to testing ( , ) = ( , ) for all  ,  and all possible values of , and

. Under the super-population framework, if we make the same no-interference assumption,

0 reduces to testing ( , ) = ( , ) for all  ,  and all possible values of , , , where the potential outcomes are assumed to be drawn from a population. These two null hypotheses are not equivalent even though the CRT can test 0 under both the ﬁnite-population and superpopulation frameworks (as proven in Theorem 3.1). This is because the distribution of ( , ) can still be equal to ( , ) even if ( , ) is diﬀerent than ( , ) for some  , .

## C Grouping Factor Levels

In this appendix, we further detail how to test 0 General when the analyst is interested in grouping multiple factor levels. For example, in the immigration conjoint application (Section 5.1), we

wish to test whether respondents diﬀerentiate immigrants from Mexico and those from Europe where there are three distinct levels for countries from Europe: Germany, France, and Poland. We now formally show how to group these levels up into one category Europe and test the hypothesis

0 .

General

We introduce a coarsening function that takes factors of interest as input and transforms them to a new set of grouped factors . Formally, this function is deﬁned as where represents the support of the grouped factors with . For the above example, we deﬁne the function on the “country of origin” factors such that the Mexico level takes one value whereas the France, Germany, and Poland levels all take another value: Europe . All other factor levels are mapped to diﬀerent values in .

Next, we deﬁne the outcome for each level of newly transformed factor levels. Given the coarsening function deﬁned above, we introduce the marginalized potential outcome variable ( , ), which averages over the distribution of original factor levels that are grouped. Formally, this new outcome variable has the following mixture structure,

( , ) =

{ ( ) = } ( , ) ( = = ) { ( ) = } ( = = )

, (11)

where , , and ( = = ) represents the conditional distribution of given

used in the experiment. For example, if we group three European countries—France, Germany, and Poland—and create one new factor level Europe, then its marginalized potential outcome will be a mixture distribution of the original potential outcomes for the three countries weighted by their known randomization probabilities conditional on the other factors.

Furthermore, the previously introduced coarsening function now takes the newly grouped up factor and maps it to the new coarsened factor, i.e., . Consequently, our updated generalized null hypothesis is,

General

0 ( , ) = ( , ) for all , , such that ( ) = ( ) and . (12) Finally, it can also be shown by applying the same argument as the one used to prove Theorem 3.1 that General0 is equivalent to the following conditional independence relation,

( ), . (13)

To test this null hypothesis, we keep the original test statistic HierNet shown in Equation (5) under the same symmetry constraints given in Equation (6) except that we use in place of to account for coarsening based on the function .

## D Data Description

Tables 2 and 3 present all the factors and their respective levels used in the immigration conjoint experiment (Section 2.1) and the gender candidate conjoint experiment (Section 2.2), respectively.

|Factor for Immigration Conjoint Experiment|Factor Levels|
|---|---|
|Education level<br><br>|No Formal Education, Fourth Grade, Eight Grade, High School, Two Years College, College Degree, Graduate Degree|
|Gender|Female, Male|
|Country of origin|Germany, France, Mexico, Philippines, Poland, India, China, Sudan, Somalia, Iraq|
|Language|Fluent English, Broken English, Tried to speak English but unable to, Spoke through an interpreter|
|Reason for application|Reunite with family members, Seek better job, Escape political/religious persecution|
|Profession|Gardener, Waiter, Nurse, Teacher, Child Care Provider, Janitor, Construction Worker, Financial Analyst, Research Scientist, Doctor, Computer Programmer|
|Job experience<br><br>|No job training or prior experience, One to two years, Three to ﬁve years, More than ﬁve years|
|Employment plan<br><br>|Has a contract with a U.S. employer, Does not have a contract with a U.S. employer, but has done job interviews, Will look for work after arriving in the U.S., Has no plans to look for work at this time|
|Prior trips to the U.S.<br><br>|Never been to the U.S., Entered the U.S. once before on a tourist visa, Entered the U.S. once before without legal authorization, Has visited the U.S. many times before on tourist visas, Spent six months with family members in the U.S.|


- Table 2: All nine randomized factors and their respective levels in the conjoint experiment used in Hainmueller and Hopkins (2015).


|Factor For Gender Conjoint Experiment|Factor Levels|
|---|---|
|Gender|Male, Female|
|Age|36, 44, 52, 60, 68, 76|
|Race/ethnicity|White, Black, Hispanic, Asian American|
|Family<br><br>|Single (never married), Single (divorced), Married (no child), Married (two children)|
|Experience in public oﬃce|12 years, 8 years, 4 years, No experience|
|Salient personal characteristics<br><br>|Strong leadership, Really cares about people like you, Honest, Knowledgeable, Compassionate, Intelligent|
|Party aﬃliation|Republican, Democrat|
|Policy area of expertise|Foreign policy, Public safety (crime), Economic policy, Health care, Education, Environmental issues|
|Position on national security|Cut military budget and keep U.S. out of war, Maintain strong defense and increase U.S. inﬂuence|
|Position on immigrants|Favors guest worker program, Opposes guest worker program|
|Position on abortion<br><br>|Pro-choice, Pro-life, Neutral|
|Position on government deﬁcit|Reduce through tax increase, Reduce through spending cuts, Does not want to reduce|
|Favorability rating among public<br><br>|34%, 43%, 52%, 61%, 70%|


- Table 3: All thirteen randomized factors and their respective levels in the conjoint experiment used in Ono and Burden


(2018).

## E Enforcing The No Proﬁle Order Eﬀect

We detail here a way to enforce the no proﬁle order eﬀect constraints in Equation (6) for general test statistics. We show through simulations that these constraints, when they hold, can substantially improve statistical power.

Under these constraints, switching the "left" and "right" proﬁle order does not change the value of the test statistic. We now formalize this intuition. First denote ×(2 + +1) as the regression data matrix composed of ( , , , ). Let ×(2 + +1) ×(2 + +1) denote a function that takes a data matrix as an input and swaps the “left” and “right” proﬁle order for rows of the data matrix, where {1,2,…,  }. For example, suppose we swap just the ﬁrst row and we

denote ( , , , ) as the columns for the output {1}( ). Then 11 = 11, 11 = 11, 11 = 11,

11 = 11, and 11 = 1 − 11 and all remaining rows remain identical as the original data . The function applies no swap to the respondent characteristic ( = ).

We introduce a new data matrix that appends the original data matrix with a data matrix that

swaps the proﬁle order for all rows. Formally, = [ ; {1,2,…,  }( )]. Table 4 shows an example of with as gender, as party aﬃliation, and as the respondent’s age. Conceptually,

aims to destroy all information about the proﬁle order since the “left” and “right” proﬁle are now indistinguishable, thus ensuring any test statistic that uses will respect the no proﬁle order eﬀect constraints. The following lemma formally states this result.

|Row Number|Gender|Gender<br><br>|Party|Party<br><br>|Respondent Age| |
|---|---|---|---|---|---|---|
|1|Male|Female<br><br>|Democrat|Republican<br><br>|27|1|
| | | | | | | |
|+ 1<br><br>|Female|Male|Republican<br><br>|Democrat|27<br><br>|0|
| | | | | | | |


- Table 4: Visual example of data matrix with as gender, as party aﬃliation, and as the respondent’s age. With a slight abuse of notation Gender denotes the left proﬁle’s gender values. Gender , Party , and Party are deﬁned similarly.


Lemma E.1. Let ( ) be a row invariant test statistic,14 then for any {1,2,…,  } we have that ( ) = ( ( ) ), where ( ) = [ ( ); 1,2,…,  ( ( ))]. Proof. The lemma holds because = ( ) up to row permutations. Using the assumption that

( ) is a row invariant test statistic we obtain the equality. Many algorithms like Random Forest have random initializations in the process so ( ) = ( ( ) ) may only hold up to distributional equality.

| |
|---|


Lemma E.1 states that the test statistic will remain invariant to any relabelling of “left” and “right” proﬁles as long the test statistic is a function of the data matrix. All regression based algorithms will respect exact row invariance. Lemma E.1 allows practitioners to build any test statistic, even ones that do not have natural “left” and “right” coeﬃcients, while still enforcing the no proﬁle order eﬀect. In particular, we enforce the constraints in Equation (6) by using as the input in HierNet.

Simulations. We now show that imposing the no proﬁle order eﬀect constraints in Equation (6) can substantially increase statistical power under the same simulation setup in Section 4 when the no proﬁle order eﬀect assumption is satisﬁed. To evaluate the power gain, we also ﬁt HierNet without imposing the constraints in Equation (6) by using the original data . We use HierNet( , , ) +

HierNet( , , ) as the test statistic, where HierNet( , , ) is the same as HierNet( , , ) in Equation (5) but all coeﬃcients correspond to their respective estimates for the left proﬁle. We similarly deﬁne HierNet( , , ) .

Figure 4 shows that imposing the no proﬁle order eﬀect constraints can signiﬁcantly increase power. For example, the power of HierNet without the constraints (purple squares) is roughly equal or smaller than that of even the AMCE (red circles) when the interaction eﬀect accounts for 20% of the variance or when there are as many interactions as twelve. Furthermore, we see the power of using HierNet that imposes the constraints (blue triangles) is consistently higher than that of the HierNet without the constraints.

Enforcing No Proﬁle Order Eﬀect in the Carryover Eﬀect Test Statistic. As mentioned in Section 3.5, we enforce the no proﬁle order eﬀect constraints when conducting the test of no carryover eﬀect. We detail here how to implement this.

14More formally we say ( ) is row invariant if ( ) = ( ( )) for any possible , where denotes a possible permutation of the rows of .

AMCE CRT Original CRT Unconstrained

1.00

1.00

0.75

0.75

Power

0.50

0.50

0.25

0.25

0.00

0.00

0 10 20 30 40

0 5 10 15

% Variance explained by interaction

##### Number of interactions

- Figure 4: This ﬁgure represents the power gain from imposing the no “Proﬁle Order Eﬀect” constraints in Equation (6) under the same simulation setup in Figure 3. We keep the AMCE and the original HierNet statistical power curves (red circles and blue triangles, respectively) and add the new unconstrained HierNet test statistic (purple squares).


Since represents the lag-1 proﬁle values, we do not expect alone (without interactions with ) to inﬂuence respondents’ choice of the left versus right proﬁle. Therefore, we force all main eﬀects and interactions among to be zero in the following way. Let 2× denote the columns of that correspond to the left proﬁle in . More formally, = [[( 1);( 1)] ; [( 3);( 3)] ;…;[(  , −1);(  , −1)] ]. If is not even, consider up to − 1 instead. We deﬁne , , similarly. We also deﬁne = [ 1 ;…; ] 2 × with , , , ,  deﬁned similarly. Then, we append copies of the following: [[( ) ;( ) ;( ) ;( ) ] ; [( ) ;( ) ;( ) ;( ) ] ;[( ) ;( ) ;( ) ;( ) ] to the original data matrix [( ) ;( ) ;( ) ;( ) ] , resulting in a total of 2 rows. Lastly, we also append copies of [ − ; − ; ] to the original response . Appending the ﬁrst copy of [( ) ;( ) ;( ) ; ( ) ] totheoriginaldatamatrixenforcesthefamiliarconstraintinEquation(6)usingLemmaE.1. The remaining copies force all the main eﬀects and interactions among to be zero by appealing to the same reasoning in Lemma E.1.

## F CRT Procedure for Testing Extensions

In this appendix, we describe in further detail how to carry out all the resampling procedures for the tests introduced in Sections 3.4 and 3.5.

### F.1 Testing 0 General

When testing 0 General, the resampling procedure is diﬀerent than Algorithm 1 because Equation (8) forces us to hold ( ( ), ) constant rather than holding only constant. The conditional distribu-

tion of ( ( ), ) constrains to be randomized only within the factor levels of interest. For

- Algorithm 2: Generalized 0: Testing 0 General Input: Data ( , , , ), test statistic ( , , , ), ( ), total number of re-samples ; for = 1,2,…,  do

Sample ( ) from the distribution of   ( ( ), , ) conditionally independently of and ;

Output: -value  = 1 +1 1 + =1 { ( ( ), , , ) ( , , , )}

concreteness, consider the immigration example in Section 5.1. In this case, ( ) groups levels Mexico and Europe to one output while keeping all the other countries of origin the same. Therefore, when obtaining the resamples for the “country of origin” factor, we keep all countries except Mexico and Europe constant, i.e., countries such as China do not get re-randomized. For the entries corresponding to Mexico and Europe, we resample values Mexico and Europe with probabilities (0.25,0.75), respectively (since 3 countries make up Europe). We present this resampling proce-

dure in Algorithm 2. Lastly, we remark that Algorithm 2 remains the same when testing General0 except we repalce with .

F.2 Testing the Regularity Assumptions

Proﬁle Order Eﬀect. We ﬁrst describe testing the assumption of no proﬁle order eﬀect without imposing SUTVA. For any {1,…,  }, let ( ) swap the left and right proﬁle values in rows

of while leaving the remaining rows unchanged. We similarly deﬁne ( ). Then, let ( )( , ) ﬂip the bits of (replace 1’s with 0’s and vice versa) the entries of ( , ) corresponding to indices in while leaving the remaining entries unchanged. For example, for simplicity, assume no while = 3, = {1}, = [( , );( , );( , )] (the left proﬁle values come ﬁrst), and

( ) = (1,0,1). Then ( ) = [( , );( , );( , )] and ( )( ) = (0,0,1). The observed ( ) is deﬁned similarly. We can formally state the null hypothesis of no proﬁle order eﬀect as follows:

Order

0 ( , ) = ( )( ( ), ( )) for all {1,…,  }, , and .

This null hypothesis states that for all possible reorderings of the left and right proﬁles there is no causal impact on which proﬁle is chosen. For the resampling procedure, we hold the realized values of all ( , ) constant while only resampling the subset , i.e., drawing independent Bernoulli coin ﬂips to determine which of the rows to include as part of as described above.

- Algorithm 3 details the procedure to calculate the CRT -value for testing 0 Order. Lastly, to not enforce Equation (6) in HierNet Order , we ﬁt HierNet on the original data matrix ( , , ) rather than .


Carryover Eﬀect. When testing the carryover eﬀect, we need to hold the even numbered tasks ﬁxed while resampling all odd numbered tasks . Therefore, we resample all factors ( , )

- for = 1,3,…,  − 1 from the experimental distribution for all the factors while holding ( , )
- for = 2,4,…,  constant. Algorithm 4 details the procedure to calculate the CRT -value for testing 0 Carryover.


- Algorithm 3: CRT: Proﬁle Order Eﬀect Input: Data ( , , ), test statistic ( , , ), total number of re-samples ; for = 1,2,…,  do

Sample independent Bernoulli(0.5) independently of ( , , ). is the index set corresponding to values of 1 in the Bernoulli’s;

Output: -value  = 1 +1 1 + =1 { ( ( ), ( ), ( )) ( , , )}

- Algorithm 4: CRT: Carryover Eﬀects


Input: Data ( , , ), test statistic ( , , ), total number of re-samples ; for = 1,2,…,  do

Sample ( , ) from the distribution of ( , ) independently of for

= 1,2,…,  and = 1,3,… − 1. Let ( ) = [[ 1; 1] ;[ 3; 3] ; …;[  , −1;  , −1] ] and ( ) = [( 1) ;( 2) ;…;( ) ];

Output: -value  = 1 +1 1 + =1 { (( ) , , ) ( , , )}

Fatigue Eﬀect. To carry out the CRT to test the fatigue eﬀect, we re-sample only the task evaluation order index for each respondent uniformly from the set of all permutations on {1,…, }, denoted as , while holding all the experimental factor values ﬁxed. Algorithm 5 details the

procedure to calculate the CRT -value for testing 0 Fatigue.

## G Details of the Simulation Setup

We provide here a detailed description of our simulation setup. For simplicity, we focus on the setting in which each respondent only has one evaluation, i.e., = 1. Appendix G.4 (see Figure 7) presents additional simulations that have multiple evaluations per respondent based on respondent random eﬀects. In the setting where each respondent evaluates only one task, we treat each response as an independent observation and drop subscript . We also assume that every factor ( , ) is uniformly and independently randomized, implying that all treatment combinations are equally likely. As before, represents the main factors of interest while denotes the other factors. For simplicity, we assume that all factors ( , ) are binary with their success probabilities equal to 0.5, and we have one factor of interest ( = 1).

### G.1 The Basic Setup

To clearly separate main and interaction eﬀects, we use the sum-to-zero constraint by coding each binary factor as (−0.5,0.5). Our data generating process uses the following logistic regression model under the forced-choice design,

Pr( = 1   , ) = logit−1 ( − ) + ( − )

+ 2 {( ) − ( )} + 2 {( ) − ( )} + 2 {( × ) − ( × )} ,

Algorithm 5: CRT: Fatigue Eﬀect Input: Data ( , , , ), test statistic ( , , , ), total number of re-samples ; for = 1,2,…,  do

Sample uniformly from the set of all permutations on {1,…, }; Output: -value  = 1 +1 1 + =1 { ( , , , ) ( , , , )}

where and represent the coeﬃcient vectors for the main eﬀects of and , respectively, and

and denote the coeﬃcient column vectors for the within-proﬁle and between-proﬁle interactions between and , respectively. For simplicity, we omit between-proﬁle interactions among and consider only within-proﬁle interactions among with eﬀect sizes . To facilitate interpretation, each interaction coeﬃcient is multiplied by 2 because our encoding of interaction eﬀects, e.g., {( ) − ( )}, results in three possible values (−0.5,0,0.5).

This data generating process also implies the absence of proﬁle order eﬀects. Lastly, we note that the logistic regression has a latent variable, , representation such that = 1 if > 0 and 0 otherwise, where we let follow a standard logistic distribution and

= ( − ) + ( − )

+ 2 {( ) − ( )} + 2 {( ) − ( )} + 2 {( × ) − ( × )} + .

We consider settings in which has one main eﬀect of = 0.1, which is ﬁxed for all simulations. In addition, consists of ten factors with four non-zero main eﬀects with a magnitude of 0.1 with alternating signs, which is ﬁxed for all simulations, i.e., = (0.1,−0.1,0.1,−0.1,0,…,0). Lastly, we ﬁx to have ﬁfteen non-zero entries of 0.05, where the non-zero interactions are randomly chosen from all possible within-proﬁle interactions among . The remaining entries are all zero.

The sample size is ﬁxed to = 3,000 throughout the simulations. For each simulation, we generate within-proﬁle and between-proﬁle interactions between and by randomly selecting the speciﬁed number of interactions from all possible interactions. The total number of non-zero interaction eﬀects between and varies from 0 to 18. The number of non-zero within-proﬁle interactions between and is kept identical to that of non-zero between-proﬁle interactions between

and . We make all non-zero within-proﬁle interactions positive and all non-zero between-proﬁle interactions negative while ﬁxing all non-zero interaction eﬀects between and to be equal in magnitude. We explore additional simulations in Appendix G.2 where there are heterogeneous interaction eﬀects. We set = 200 for all simulations presented in this paper.

We measure the total variance with respect to the latent representation of the logistic regression. Consequently, we deﬁne the variance explained by the interaction eﬀects between and and all other “remaining” eﬀects (main eﬀects of , , and interactions among ) as,

2

Interaction  = (2 {( ) − ( )} + 2 {( ) − ( )})

2

Remaining  = ( ( − ) + ( − ) + 2 {( × ) − ( × )}), where ( ) denotes the variance of the respective random variable. The total variance is deﬁned as

Interaction + Remaining 2 . Since ,  ,   are ﬁxed for all simulations, Remaining 2 is ﬁxed with a value of:

2

1 8

- 1

- 2


+15×4×0.052×

Remaining = 9×0.12×2 ( )+15×4×0.0522 ( ) = 9×0.12×

- 2


= 0.06375,

where the ﬁrst equality holds because all random variables ( ,  , , ) are independent, centered at zero, and identically distributed (element-wise identically distributed for the multivariate

and ). Furthermore, givenasignalsize andthenumberofinteractions ( denotesthetotalnumber

of within-proﬁle and between-proﬁle interactions), we have that:

2

Interaction = 8 2 ( ) =

2

.

2

Finally, since the left plot of Figure 3 contains six interactions ( = 6), the -axis is computed by

- 3 2+0.06375, where takes the following values (0,0.025, 0.05,0.075,0.1,0.125). To calculate the statistical power of each test, we compute a -value for each of 1,000 Monte


3 2

Carlo data sets. For the CRT, we use the HierNet test statistic given in Equation (5) and impose the constraints in Equation (6), whereas we use the -test based on the estimated regression coeﬃcient of for the AMCE-based test. The AMCE-based analysis assumes no proﬁle-order eﬀect. Therefore, as suggested by Hainmueller, Hopkins and Yamamoto (2014), we run the linear regression by stacking all the left and right proﬁles, resulting in 2 rows. More formally, we have the new

response AMCE = [ ; − ] regressed on AMCE = [ ; ], where = [ 1 ; 2 ;…; ] and is deﬁned similarly (note we have dropped the subscript since = 1). Finally, the stan-

dard errors are clustered by respondents as suggested by Hainmueller, Hopkins and Yamamoto. Since = 1 for our simulation, we cluster the standard errors on each evaluation task, i.e., each unique cluster consists of the left and right proﬁle for each task. We then compute the power as the proportion of -values that are less than = 0.05.

### G.2 Heterogeneous Interaction Size

As stated in Section 4, we ﬁx all interaction sizes to be equal for every simulation. Here, we examine if the simulation results presented in Figure 3 change if there are heterogeneous interaction eﬀects.

We compare the statistical power under two diﬀerent data generating processes using the CRT with test statistic in Equation (5). We denote the original data generating process as the “homogeneous” scenario since all interaction sizes are equal under this scenario. We create an additional “heterogeneous” scenario that contains two unique varying interaction eﬀects - one that is strong,

, and one that is weak . To facilitate a fair comparison between the “heterogeneous” and “homogeneous” scenario, we force the total variance explained by the interactions to be equal under both scenarios. We assign all strong interaction eﬀects to the within-proﬁle interaction and all weak interaction eﬀects to the between-proﬁle interaction. Suppose there are only two non-zero interactions between and . Since we impose Interaction 2 to be equal under both the “homogeneous” and “heterogeneous” scenario, we have the following equation:

2 + 2 = 2 2, where is the interaction size for the “homogeneous” scenario. The possible values of strong and weak eﬀects lie on the circle of radius 2 centered at the

origin. We pick ( ) = 43 and ( ) = 23 , i.e., the point corresponding to the thirty degree angle of the circle. The variance explained by the interaction is equal for both the “heterogeneous”

CRT Heterogeneous CRT Homogeneous

1.00

1.00

0.75

0.75

Power

0.50

0.50

0.25

0.25

0.00

0.00

0 10 20 30 40

0 5 10 15

% Variance explained by interaction

##### Number of interactions

- Figure 5: The ﬁgure shows the power of the “heterogeneous” (light green circles) and “homogeneous” (blue triangles) scenario in the same simulation setting as in Figure 3.


and “homogeneous” scenario when there are two non-zero interactions. To create a power curve for the “heterogeneous” scenario analogous to the left plot in Figure 3, we create three interactions of size ( ) for the within-proﬁle interaction and three interactions of size ( ) for the betweenproﬁle interaction. The two scenarios still maintain equal variance explained by the interaction eﬀects because all random variables are independent and centered at zero. For the analogue of the right plot of Figure 3, we similarly keep the relative proportion of ( ) and ( ) ﬁxed and increase the number of non-zero interactions to match the “homogeneous” scenario. For example, if there are twelve non-zero interaction eﬀects, then there are six within-proﬁle interactions of size

( ) and six between-proﬁle interactions of size ( ) for the “heterogeneous” scenario.

Figure 5 shows that the power of the “heterogeneous” and “homogeneous” scenario is indistinguishable under the same simulation setting in Figure 3. This shows that we lose no generality by considering only the simple “homogeneous” scenario in the main simulations in Figure 3.

### G.3 Additional AMCE Simulations

The AMCE computed in Figure 3 was based on a linear regression of on , without included among the predictors. Although this is valid and suﬃcient to compute the AMCE of , practitioners often compute the AMCE of all factors ( , ) simultaneously with a single linear regression of on all ( , ). We compute the power of the “long AMCE” that is based on the -test for the estimated regression coeﬃcient of obtained by regressing the response on all ( , ). Figure 6 shows that the power of the “long AMCE” (orange squares) is indistinguishable from that of the original AMCE presented in Figure 3 (red circles).

### G.4 Simulations with Multiple Tasks per Respondent

Appendix G.1 presents the simulation results where each respondent evaluates only one task ( = 1). Here, we consider a simulation setup where each respondent evaluates = 5 tasks while still

AMCE (X) AMCE (X, Z)

1.00

1.00

0.75

0.75

Power

0.50

0.50

0.25

0.25

0.00

0.00

0 10 20 30 40

0 5 10 15

% Variance explained by interaction

##### Number of interactions

- Figure 6: The ﬁgure shows the power of the “long AMCE” that uses all ( , ) in the linear regression ﬁt (orange squares) and the original AMCE that uses only in the linear regression ﬁt (red circles) in the same simulation setting as in Figure 3.


ﬁxing the total sample size = 3,000. We keep the same simulation setup as the one described in Appendix G.1 except that we allow each respondent to have a random eﬀect (0, 2 ). More formally, our new data generating process is,

Pr( = 1   , ) = logit−1 ( − ) + ( − )

+ 2 {( ) − ( )} + 2 {( ) − ( )} + 2 {( × ) − ( × )} + ,

where is the random eﬀect for each respondent . We keep all simulation parameters the same as that in Figure 3 except we use the above data generating process with = 5 evaluation tasks and random eﬀects with 2 = 0.1 to produce Figure 7.

Although the CRT HierNet test statistic does not change with the addition of multiple respondent evaluations, the AMCE estimate must properly account for the respondent eﬀect. As suggested by Hainmueller, Hopkins and Yamamoto (2014), we use the robust clustered standard errors clustered on respondents for the linear regression of on and use the -test based on the estimated regression coeﬃcient of to produce the power curve (red). Figure 7 shows the results are similar to those shown in Figure 3, suggesting that our results are not sensitive to the number of evaluations per respondent.

## H Leveraging Presidential Data in the Gender Application

We detail here how we leverage the Presidential candidate data to ﬁnd the strongest interaction, as mentioned in Section 5.2. Because we are only interested in whether the additional interactions are signiﬁcant, we run the Lasso logistic regression with main eﬀects of ( , , ) and one interaction between (“gender”) and one variable in ( , ), producing one CRT -value for each variable in ( , ). For example, when including an interaction between “gender” and “profession”, we include

AMCE CRT

1.00

1.00

0.75

0.75

Power

Power

0.50

0.50

0.25

0.25

0.00

0.00

0 10 20 30 40

0 5 10 15

% Variance explained by interaction

% Variance explained by interaction

- Figure 7: The ﬁgure shows the power of the AMCE (red circles) and the CRT (blue triangles) using the HierNet test statistic in Equation (5). We modify the simulation setting in Figure 3 by having each respondent evaluate = 5 tasks with a total of = 3,000 responses. Otherwise, the simulation setup remains identical to that in Figure 3. Each respondent has a random eﬀect of 2 = 0.1.


bothwithin-proﬁleandbetween-proﬁleinteractionsbetweenalllevelsof“gender”and“profession”. Consequently, the test statistic for testing the interaction between (“gender”) and factor of is:

( 1 − 1 )2. (14) The test statistic for testing the interaction between and factor of the respondent characteristic

Candidate Factor,

( 1 − 1 )2 +

Presidential =

=1 =1

=1 =1

is:

Respondent Characteristic,

( 1 − 1 )2, (15)

Presidential =

=1 =1

where all coeﬃcient estimates refer to the same corresponding estimatesin Equation (10)and = 2 refers to levels male and female. Lastly, when running the CRT we similarly enforce the constraints in Equation (6) (along with the constraints on the respondent characteristics) by ﬁtting the Lasso logistic regression on the appended data matrix.

Table 5 shows the resulting -value for each variable in ( , ). Many of the variables have

-values lower than 0.1. The variables such as “position on immigrants”, “position on abortion”, “position on government deﬁcit”, and “position on national security”, are all related to the disparate views Democratic and Republican candidates may have, in line with “party aﬃliation” being the most signiﬁcant. Even among the respondent characteristics, the respondent’s political ideology, a measure of how conservative or liberal the respondent is, is the most signiﬁcant variable. We conduct a robustness analysis by repeating the analysis of Section 5.2 but using the second most signiﬁcant variable, the “position on abortion” factor, to interact and include as the additional main eﬀect in HierNet, though we note that “position on abortion” is quite a bit less signiﬁcant than “party aﬃliation” with more than four times as large a -value. The resulting -value is 0.078. Although

Variable -value Age 0.060 Race 0.31 Family 0.22 Experience in public oﬃce 0.30 Salient personal characteristic 0.45 Party aﬃliation 0.0049 Policy area of expertise 0.25 Position on national security 0.067 Position on immigrants 0.067 Position on abortion 0.022 Position on government deﬁcit 0.032 Favorability rating among public 0.63 Respondent gender 1.00 Respondent education 1.00 Respondent age 1.00 Respondent class 0.41 Respondent region 1.00 Respondent race 1.00 Respondent partisanship 0.11 Respondent thought on Hillary Clinton 1.00 Respondent interest in politics 0.43 Respondent political ideology 0.042

- Table 5: Resulting -values using the CRT Lasso logistic regression with main eﬀects of ( , , ) and an additional interaction between and one variable in ( , ) from the Presidential candidate data. The test statistic captures the interaction terms with each variable in ( , ) as shown in Equation (14) and Equation (15), respectively. All respondent characteristic variables are labelled with “respondent”.


this is not as signiﬁcant as the main analysis, it still provides suggestive evidence that gender plays a role in voting for Congressional candidates.

## I Computational Details

The HierNet test statistic introduced in Equation (5) is powerful but can be computationally expensive because the CRT requires a total of + 1 cross-validated HierNet ﬁts. To address this problem, we speed up HierNet in three ways. First, we reduce the default convergence tolerance for the optimization algorithm in the HierNet package from 10−6 to 10−3. Second, following the “distillation” idea introduced in (Liu et al., 2020), we cross-validate the sparsity parameter lambda only through a HierNet ﬁt of on without involving any . Because ( , ) remains constant for all + 1 ﬁts, we only need one cross-validation ﬁt. Lastly, we initialize the starting parameters in the optimization algorithm with one HierNet ﬁt that is uniformly and randomly chosen from the

+ 1 HierNet ﬁts. Since we uniformly choose one out of + 1 HierNet ﬁts as the initialization, this procedure still satisﬁes the exchangeability needed for the CRT’s validity. Because many of the parameters estimated from the + 1 diﬀerent HierNet ﬁts will likely be similar to each other,

CRT CRT Slower

1.00

1.00

0.75

0.75

Power

0.50

0.50

0.25

0.25

0.00

0.00

0 10 20 30 40

0 5 10 15

% Variance explained by interaction

##### Number of interactions

- Figure 8: This ﬁgure represents the power of the original faster HierNet test statistic (blue triangles) with the three computational speedups and the slower HierNet test statistic (black squares) without the computational speedups in the same simulation setting as in Figure 3.


the initialization likely saves computation time.

Although the above procedure signiﬁcantly reduces computational complexity, practitioners may worry if there is a signiﬁcant loss of power from this simpliﬁcation. Consequently, we plot in

- Figure 8 the original HierNet power curve shown in Figure 3 that leverages the aforementioned three speed-ups (in blue) and the computationally slower HierNet power curve without the three speedups (in black). Figure 8 shows that the computational modiﬁcations have no signiﬁcant impact on power.


## J Inﬂated -values for Logistic Regression

Although the AMCE is popular in conjoint analysis, especially among political scientists, there also exist model-based approaches. Logistic regression remains a popular model-based approach to conjoint analysis (McFadden, 1973; Green and Srinivasan, 1990; Campbell, Mhlanga and Lesschaeve, 2013). We explore in this section how this modeling approach can lead to invalid inference in conjoint analysis. When testing 0, researchers may want to account for not only the main eﬀects of ( , ) but also all two-way interactions, as done similarly in HierNet, to reduce model misspeciﬁcation. Under this scenario, we show through simulations in Figure 9 that even reasonable sample sizes and dimensions of ( , ) can lead to invalid -values, i.e., the type 1 error is greater than the desired   [0,1].

We use a similar simulation setting as the one in Appendix G.1 but simplify it further. Since we are interested in showing how the -values obtained from a logistic regression may be invalid in general, we do not have “left” or “right” proﬁles but only one proﬁle, leading to the following data generating process,

Pr( = 1   , ) = logit−1 + + ( ) + ( × ) .

30

0.5

Proportion p−values < 0.05

0.4

20

Percentage

0.3

0.2

10

0.1

0.0

0

2.5 5.0 7.5 10.0 12.5

0.00 0.25 0.50 0.75 1.00

Number of Factors (Z)

Histogram of p−values

- Figure 9: Inﬂated -values from logistic regression. The left ﬁgure shows the proportion of -values, obtained through a -test from a logistic regression, less than = 0.05 when the number of other factors in is (3,5,10,11,12,13) and


0 is true. The red dotted line at = 0.05 represents the expected proportion of -values less than 0.05 if the -values are valid. The right ﬁgure shows the histogram of 1,000 Monte-Carlo -values when the number of other factors of is 12. The sample size is = 5,000 and each factor has four factor levels. All Monte Carlo standard errors are below 0.016.

All factors have four levels, and we similarly assume one factor of interest = 1 while varying the number of other factors. Since we are interested in the behavior of the -values under the null 0, we force all eﬀects of on the response to be zero, i.e., = = 0. For simplicity we also make all eﬀects of zero, i.e., = = 0 and ﬁx the sample size to = 5,000. To reﬂect the researcher’s desire to reduce model misspeciﬁcation by accounting for all two-way interactions as HierNet does, we ﬁt a logistic regression of on all main eﬀects and two-way interactions of ( , ). We then obtain a -value for testing 0 by an -test that tests = = 0. We obtain 1,000 Monte-Carlo

-values and plot the proportion of -values less than = 0.05 in the left plot of Figure 9. We also vary the number of factors of , which is shown in the -axis of the left plot. On the right plot of Figure 9, we plot the histogram of the 1,000 -values obtained when the number of factors of is 12.

Underthenullhypothesis, weexpectanyvalid -valuetohavetype1errorcontrol, i.e., ( -value

) for all   [0,1]. The left plot of Figure 9 shows that only ﬁve other factors of is enough to cause the proportion of -values less than = 0.05 to be noticeably inﬂated at 7%. The inﬂation becomes particularly apparent when there are twelve other factors of , which causes the proportion of -values less than 0.05 to be as high as 34%. The histogram on the right plot of Figure 9 visually shows how the -values are clearly far from the expected uniform distribution and have an undesirable peak at zero, resulting in poor type 1 error control. This phenomenon is studied in (Candès and Sur, 2018) and arises because the -values’ validity in a logistic regression depends on a low-dimensional asymptotic result. We note that a conjoint analysis has typically more than ten factors, where each factor usually has more than three levels. Therefore, Figure 9 shows the potential dangers of using a model-based approach like the logistic regression to ﬂexibly capture all interactions.

