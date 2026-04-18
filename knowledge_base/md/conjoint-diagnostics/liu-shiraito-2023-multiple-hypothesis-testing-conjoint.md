# Multiple Hypothesis Testing in Conjoint Analysis∗

#### Guoer Liu† Yuki Shiraito‡ First draft: January 5, 2021 Submitted for publication: October 9, 2022

###### Abstract

Conjoint analysis is widely used for estimating the eﬀects of a large number of treatments on multidimensional decision making. However, it is this substantive advantage that leads to a statistically undesirable property, multiple hypothesis testing. Existing applications of conjoint analysis except for a few do not correct for the number of hypotheses to be tested, and empirical guidance on the choice of multiple testing correction methods has not been provided. This paper ﬁrst shows that even when none of the treatments has any eﬀect, the standard analysis pipeline produces at least one statistically signiﬁcant estimate of average marginal component eﬀects in more than 90% of experimental trials. Then, we conduct a simulation study to compare three well-known methods for multiple testing correction, the Bonferroni correction, the Benjamini-Hochberg procedure, and the adaptive shrinkage. All three methods are more accurate in recovering the truth than the conventional analysis without correction. Moreover, the adaptive shrinkage method outperforms in avoiding false negatives, while reducing false positives similarly to the other methods. Finally, we show how conclusions drawn from empirical analysis may diﬀer with and without correction by reanalyzing applications on public attitudes toward immigration and partner countries of trade agreements.

∗The authors thank Scott Abramson, Nahomi Ichino, Yusaku Horiuchi, Naijia Liu, Tom Pepinsky, Kevin Quinn, Teppei Yamamoto, Arthur Yu, Jerry Yu, participants at the Joint Conference of Asian Political Methodology Meeting VIII and Australian Society for Quantitative Political Science Meeting IX, attendees at the “Politics, Sandwiches, and Comments” workshop of the Cornell Department of Government and the University of Michigan Interdisciplinary Seminar in Social Science Methodology, members of the Ichino lab, the Quinn research group, and the Shiraito research group, and two anonymous reviewers for helpful comments and discussions on earlier drafts.

†Ph.D. Candidate, Department of Political Science, University of Michigan. Email: guoerliu@umich.edu.

‡Assistant Professor, Department of Political Science, University of Michigan. Center for Political Studies, 4259 Institute for Social Research, 426 Thompson Street, Ann Arbor, MI 48104-2321. Phone: 734-615-5165, Email: shiraito@umich.edu, URL: shiraito.github.io.

## 1 Introduction

Conjoint analysis has been one of the most widely used survey experimental designs in political science, since Hainmueller, Hopkins and Yamamoto (2014) deﬁned the average marginal component eﬀect (AMCE) as an estimand in conjoint designs and developed a simple estimator. In a typical conjoint experiment, respondents are asked to assess pairs of proﬁles and choose a preferred one in each paired comparison. The proﬁles consist of theoretically relevant attributes that reﬂect multiple dimensions of respondents’ preferences, and the attributes are independently randomized across the proﬁles. For instance, Hainmueller and Hopkins (2015) examined individual-level attributes of a hypothetical immigrant such as gender, education, occupation, and the country of origin. Using a conjoint experiment, the authors estimated the AMCEs of those attributes on the probability that the immigrant’s admission is preferred. After this canonical study, conjoint designs are used to study voting (e.g., Carnes and Lupu, 2016; Teele, Kalla and Rosenbluth, 2018; Ono and Burden, 2019; Incerti, 2020), bureaucratic selection (e.g., Liu, 2019; Oliveros and Schuster, 2018), and other types of multi-dimensional decision making (e.g., Sen, 2017; Fournier, Soroka and Nir, 2020; Shafranek, 2021).1

Conjoint analysis “enables researchers to estimate the causal eﬀect of multiple treatment components and assess several causal hypotheses simultaneously” (Hainmueller, Hopkins and Yamamoto, 2014, p.1). This property is extremely valuable substantively. Since a number of factors contribute to decisions, isolating the causal eﬀect of each factor under all combinations of the others would require impractically many experimental conditions. Conjoint analysis overcomes this diﬃculty by identifying the AMCEs of multiple attributes at once. AMCE is the causal eﬀect of an attribute averaged over all proﬁles of the other attributes, and it has an intuitive interpretation (Bansak et al., 2022). The combination of conjoint designs and AMCE enables researchers to estimate the eﬀects of multiple features simultaneously.

Despite this substantive advantage, producing many estimates leads to a statistically undesirable property, multiple hypothesis testing. Testing multiple hypotheses in statistical inference is problematic because the more null hypotheses are tested, the more likely at least one of them is to be rejected, even if all of them are true. The prespeciﬁed critical value, conventionally set at .05, represents the probability of falsely rejecting the null hypothesis assuming that only one is tested. When several hypotheses are tested simultaneously, the test procedure needs to be modiﬁed. In political science, multiple testing has not been considered

- as a common concern because studies usually intend to examine only a few hypotheses.2


- 1For a more comprehensive list of conjoint experiment papers, see de la Cuesta, Egami and Imai (2022). 2Recently, however, multiple testing correction is used more often as robustness checks than before. We


However, since conjoint analysis is designed exactly for estimating multiple eﬀects, it cannot avoid multiple statistical tests. The immigration application in Hainmueller, Hopkins and

- Yamamoto (2014), for example, involves 41 hypothesis tests in total. Theoretically, even if all 41 AMCEs are zero in truth, estimates of two AMCEs will be statistically distinguishable from zero on average across experimental trials. The promise of conjoint analysis implies many statistical tests, and false-positive conclusions may follow as a result.

To our knowledge, existing studies in political science using conjoint analysis do not correct for multiple testing in their main analysis except for Hainmueller, Hangartner and

- Yamamoto (2015), which use the Bonferroni correction. A few others, for example Clayton, Ferwerda and Horiuchi (2021), conﬁrm their results with corrections as robustness checks. In fact, researchers are aware that multiple hypothesis testing is an inherent problem with conjoint designs. Bansak et al. (2021b, p.28) point out that the concerns about multiple comparisons make pre-registration and pre-analysis plans especially valuable. However, no systematic assessments have been done on the severity of the problem in the literature. Moreover, to avoid haphazard selection, applied researchers need guidance on which correction method among several well-known ones is appropriate under their circumstances.


In this paper, we quantify the multiple testing problem in conjoint designs and assess easy-to-implement correction strategies. First, we show that under a classic conjoint setup the standard analysis pipeline produces at least one statistically signiﬁcant AMCE estimate in more than 90% of experimental trials even when all AMCEs are zero.

Second, we compare the strengths and limitations of two well-known correction methods, the Bonferroni correction (Dunn, 1961; Bland and Altman, 1995) and the BenjaminiHochberg procedure (Benjamini and Hochberg, 1995). In addition, we introduce a recently developed correction method, adaptive shrinkage (Stephens, 2017; Gerard and Stephens, 2018). While none of the methods completely resolves the problem, all of them are better than the standard practice. Among the three methods, the Bonferroni correction guards against false-positive conclusions, but the cost of false-negative conclusions can be signiﬁcant. On the other hand, the Benjamini-Hochberg is the least susceptible to false-negative conclusions, but it is most lenient with false positives. The adaptive shrinkage takes a middle ground.

To illustrate how diﬀerent correction methods perform in real data, we reanalyze two conjoint design applications. The ﬁrst application using the data set of Hainmueller, Hopkins and Yamamoto (2014) demonstrates that results corrected by the adaptive shrinkage are more consistent with the original authors’ argument than other methods. Second, reanalysis of an experiment in Vietnam about the selection of trade agreement partners (Spilker,

thank Yusaku Horiuchi for pointing this out.

Bernauer and Uman˜a, 2016) shows that corrected methods remove the statistical signiﬁcance on an attribute that is hard to interpret given Vietnam’s security policy.

Compared to other studies that propose improvements on conjoint survey designs, this paper exclusively focuses on statistical inference. Existing studies have examined estimands and interpretation (Egami and Imai, 2019; de la Cuesta, Egami and Imai, 2022; Ganter, 2021; Abramson, Ko¸cak and Magazinnik, 2022; Abramson et al., 2020; Bansak et al., 2022), implementation (Bansak et al., 2018, 2021a), social desirability bias (Horiuchi, Markovich and Yamamoto, 2020), and subgroup analysis (Leeper, Hobolt and Tilley, 2020; Clayton, Ferwerda and Horiuchi, 2021). While this paper does not directly engage with any of these, the issue of multiple testing is relevant to any statistical inference with conjoint analysis due to its multiple comparison feature, unless the purpose of the analysis is exclusively exploration of higher-order interaction eﬀects (Egami and Imai, 2019).

The paper proceeds in four sections. First, we discuss why multiple testing is a problem in conjoint designs and quantify the problem. Then, we examine three correction methods and compare their performance in a simulation study. Third, we apply the correction methods to two conjoint experiment data sets. Finally, we summarize the paper and discuss suggested analysis pipelines for conjoint designs in the concluding section.

## 2 False-Positive Findings in Conjoint Analysis

When a large number of hypothesis tests are conducted, some reject null hypotheses purely by chance. With the conventional signiﬁcance level of .05, a test rejects a true null hypothesis with probability .05. That is, the test tolerates ﬁve false positives out of 100 experimental trials on average. However, the probability that at least one of multiple tests rejects its null hypothesis can be much larger depending on the number of hypotheses. When ten hypotheses are tested, this probability, known as the familywise error rate (FWER), is 1 − Pr(None of the ten tests rejects the null) = 1 − (1 − .05)10 = .401. If the number of tests is 20, the FWER increases to .642. (See Supplementary Information (SI) A.) Since the number of hypotheses is greater than 20 in most conjoint experiments, the problem is even more severe—in fact, it is almost guaranteed that at least one AMCE will be deemed statistically distinguishable from zero in any conjoint experiment, even if all AMCEs are zero in truth.

To illustrate how likely conjoint experiments may produce false-positive ﬁndings, we conducted a simulation study. Simulated data sets are generated from the conjoint design of Hainmueller, Hopkins and Yamamoto (2014). The design consists of nine attributes with total 50 levels, and therefore requires 41 comparisons excluding a reference level in each attribute. The forced-choice design is simulated by coarsening linear continuous responses

| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | |


250

200

Number of data sets

150

100

50

0

0 1 2 3 4 5 6 7 8 9 10 11 12

Number of significant coefficients

- Figure 1: False-positive Results of Estimated AMCEs when All Null Hypotheses are True. Each bar presents the number of data sets (y-axis) for each number of statistically signiﬁcant estimates (x-axis), with the truth (no signiﬁcant ﬁndings) shaded by gray.


into a binary choice in each pair of proﬁles. 1,000 simulation data sets are generated under the scenario that the true AMCEs of all attributes are zero. In particular, the individual marginal component eﬀect (MCE) is generated from N(.06,.0152) for a half of the respondents and from N(−.06,.0152) for the other half. We estimate AMCEs for each simulated data set following the standard analysis pipeline for conjoint analysis and test the null hypothesis that each AMCE is zero.3

Figure 1 shows that only less than 75 out of 1,000 experimental trials correctly conclude that none of the attribute levels has any average eﬀect. In other words, more than 90% of experiments may produce false-positive ﬁndings. Although we observe that the rate of false-positive ﬁndings is a little lower (around 80%) under some other simulation settings (SI B), the high false positive rate is concerning for applied research.

## 3 Multiple Testing Correction Methods

This section brieﬂy introduces two popular methods, Bonferroni Correction and BenjaminiHochberg Procedure, and a recently developed method, adaptive shrinkage. Then, The respective advantages and limitations of these methods will be illustrated by Monte Carlo simulations.

3For greater details of the simulation settings, see SI B.

### 3.1 Bonferroni Correction

The Bonferroni correction (Dunn, 1961; Bland and Altman, 1995, henceforth BC) reduces the FWER by using a more stringent threshold as the number of tests increases. To control the FWER below α, the BC tests each hypothesis at the signiﬁcance level α/(# of tests). Therefore, when ﬁve hypotheses are tested at the conventional 5% level, each test is conducted at the 1% level. The BC is easiest to implement among the methods to control the FWER, since researchers only need to implement the standard test procedure and construct conﬁdence intervals with a new signiﬁcance level.

One caveat is that the BC can be overly conservative. In many applications, the BC reduces the FWER substantially lower than the level set by the user. Hence, the BC may suﬀer low statistical power and false-negative ﬁndings. We illustrate this point later in our simulation study.

Another critique of the BC is that the total number of tests in a “family” cannot be unambiguously deﬁned and tracked (Sj¨olander and Vansteelandt, 2019). Hochberg and Tamhane deﬁne family as “[a]ny collection of inferences for which it is meaningful to take into account some combined measure of errors” (1987, p.5). While conjoint designs clearly pre-specify the number of attribute levels, researchers often conduct many tests to ensure survey quality such as balance and attention checks. Moreover, many applications include subgroup comparisons (Leeper, Hobolt and Tilley, 2020). It may not be obvious which tests should be included in the “family” when using the BC.

While the decision on the number of tests may increase the researchers’ degree of freedom, this problem should be ameliorated by pre-registration, as Bansak et al. (2021b) suggest for conjoint experiments in general. What constitutes a family depends on whether the type of research is exploratory or conﬁrmatory. “In purely exploratory research the question of interest (or lines of inquiry) are generated by data-snooping. In purely conﬁrmatory research they are stated in advance. Most empirical studies combine aspects of both types of research” (Hochberg and Tamhane, 1987, p.5). Discussing this issue in greater detail is beyond the scope of this paper, but pre-registration will ameliorate this ambiguity to some extent. In the conclusion section, we provide a recommendation checklist for conjoint users.

### 3.2 Benjamini-Hochberg Procedure

The Benjamini-Hochberg procedure (Benjamini and Hochberg, 1995, henceforth BH) controls another measure of false-positive ﬁndings, the false discovery rate (FDR), which is deﬁned as

# false discoveries # total discoveries

FDR ≡ E

.

The FDR indicates the average proportion of false positives among all statistical ﬁndings. Therefore, lowering the FDR implies that researchers can be more conﬁdent in their ﬁndings. The BH is a method for containing the FDR under a pre-set level α. The value of α is commonly set to .05, i.e., 5% of null hypothesis rejections are false positives on average. The key idea of the BH is to remove some ﬁndings after conducting standard hypothesis tests. In other words, it prunes signiﬁcant estimates so that researchers obtain fewer false ﬁndings.

The BH is a rank-based method with four steps. 1) For m hypotheses, a m-vector of p-values is produced. 2) Rank the p-values in the ascending order and index by i. 3) Deﬁne k ≡ max{i : pi ≤ α×i/m,0 ≤ i ≤ m}. 4) Reject null hypotheses Hi for i = 1,2,...,k, whose p-values are smaller than or equal to pk, or reject none if k does not exist.

Although discussing theoretical properties of the BH (e.g., Benjamini and Hochberg, 1995; Benjamini and Yekutieli, 2001) is beyond the scope of this paper, the BH is less susceptible to false-negative conclusions than the BC, because it accepts all statistically signiﬁcant ﬁndings in its ﬁrst step. However, the BH eliminates fewer false-positive ﬁndings. Moreover, the BH does not oﬀer conﬁdence intervals because it uses the p-values. We illustrate these limitations below by simulations and applications.

### 3.3 Adaptive Shrinkage

The adaptive shrinkage (Ash) is a recently-proposed, empirical Bayes approach to controlling the FDR developed by Stephens (2017) and Gerard and Stephens (2018). Applied researchers can easily incorporate the Ash in conjoint analysis routine using the ashr package in R (Stephens et al., 2020).

The basic idea of the Ash is post-hoc regularization of estimated coeﬃcients using a spikeand-slab prior (see Figure 2). Regularization, in general, decreases the sampling variance of an estimator by introducing additional information into estimation. For the Ash, the spike-and-slab prior is such auxiliary information. On the one hand, the spike part reﬂects the fact that some estimates are false positives, inducing estimates to be zero with a certain probability. On the other hand, the slab part allows estimates to be non-zero with the remaining probability. As a result, the Ash shrinks estimated coeﬃcients and produces narrower conﬁdence intervals and smaller mean squared error. As shown in Section 5, the Ash moves point estimates of small absolute values toward zero and removes their statistical signiﬁcance. By contrast, large point estimates are preserved and their conﬁdence intervals are shortened.

Formally, let β = (β1,...,βJ) denote estimates for J attribute levels, βˆ = (βˆ1,...,βˆJ) denote point estimates of β, and sˆ = (ˆs1,...,sˆJ) be the standard errors of βˆ. Consider the

| | | | | | |
|---|---|---|---|---|---|
| | | | | | |


−0.4 −0.2 0 0.2 0.4

Prior for

- Figure 2: Example of the Spike-and-slap Prior Distribution. The spike (point mass) is at zero, and the slap (grey curve) follows a normal distribution.


posterior distribution of β given βˆ and sˆ:

p(β|βˆ,sˆ) ∝ p(βˆ|β,sˆ)p(β|sˆ). (1)

The likelihood in Equation 1 is the sampling distribution of βˆ approximated by the normal distribution with mean β and variance sˆ2. To regularize a large number of estimates, independent spike-and-slab prior distributions are placed. Since the Ash is an empirical Bayes method, the mixture probabilities of the spike-and-slab prior are estimated by maximizing the penalized likelihood and then the posterior parameters are estimated using the prior parameter estimates. The conﬁdence intervals are constructed based on the posterior distribution of β. SI C.1 provides a greater detail of the model and estimation.

The Ash delivers an additional beneﬁt because of the shrinkage property. Its regularization leads to smaller mean squared errors of the point estimates. This is attractive because in many social science applications, researchers are interested not only in “whether factor X aﬀect respondents’ choice,” but also in “to what extent.” The classic immigrant conjoint experiment, for instance, found a bonus for some education relative to no formal education.

When researchers would like to estimate the amount of the education bonus, the other correction methods do not reduce the sampling error of point estimates. The Ash, however, enables us to get more precise estimates in a principled manner. SI C.2 illustrates this point by simulations.

## 4 Comparing Correction Methods

This section examines the performance of the three methods by a series of simulations. In all simulations, we generate 1,000 samples from simulation experiment using the immigrant proﬁle data of Hainmueller, Hopkins and Yamamoto (2014), and conduct hypothesis tests

- at the conventional signiﬁcance level of .05. The total number of tests for the BC is set to the total number of comparisons of attribute levels and a reference category. First, we apply the correction methods to the case where the true AMCE is zero for all attributes (identical to Section 2). Second, we compare the correction performance in more realistic cases where some attributes have non-zero AMCEs.


### 4.1 Zero AMCEs

The results are summarized in Figure 3. As in Figure 1, the bars represents the number of data sets for each number of statistically signiﬁcant estimates. Note that the black bars are identical to Figure 1. Figure 3 also shows the results of the BC, BH, and Ash with a mixture of uniform components and with a mixture of normal components.

All three correction methods dramatically reduce the probability of false ﬁndings. Because all null hypotheses are true, all simulations should result in zero signiﬁcant coeﬃcients. As we discussed in Section 2, more than 90% experimental trials would produce at least one signiﬁcant estimate without correction. By contrast, both the BC and BH remove false ﬁndings in more than 90% of simulation data sets. The Ash performs even better. It eliminates almost all false-positive ﬁndings.

### 4.2 Non-zero AMCEs

It is perhaps rare that all AMCEs are zero in applications, because attributes are designed to capture promising theoretical hypotheses. We consider two sets of more realistic simulations where some AMCEs are not zero to see how the correction methods perform in such settings.

In the ﬁrst scenario, one binary attribute has a non-zero AMCE, and the results are shown in Table 1. In the original proﬁle data, this attribute corresponds to Gender. We vary the noise in simulations by changing the heterogeneity of AMCEs and the error variance of the regression model for latent responses. Since only Gender has an eﬀect, the shaded cells are the target we would like to hit: tests identify only one true-positive ﬁnding and no false

| | | | | | | | | | | | | | | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | |


1000

750

Number of data sets

500

250

0

0 1 2 3 4 5 6 7 8 9 10 11 12

Number of significant coefficients

No corr. Bonf corr. FDR corr. ashUnif corr. ashNorm corr.

- Figure 3: False-positive AMCE Estimates when All Null Hypotheses are True with Correction Methods. While the standard analysis pipeline correctly accepts all null hypotheses in fewer than 80 data sets, the BC, BH, and Ash all correct multiple testing in more than 900 experimental trials with the Ash performing the best.


ﬁndings. The pattern is quite consistent with the simulation results shown in Section 4.1. Without correction, about 80% of experimental trials produce at least one false-positive ﬁnding. All correction methods improve the situation remarkably, with the Ash has the best performance in all circumstances.

In the second scenario, all levels of the attributes that correspond to Gender, Education, and English in the original data have non-zero AMCEs, whereas the AMCEs of the others are zero.4 Table 2 presents the results. Because ten levels have non-zero AMCEs, the shaded cells indicate the number of data sets in which hypothesis tests are perfectly accurate. All cells to the right (above) are the number of samples where some false positives (negatives) are produced. For example, without correction, 248 experimental trials successfully detect exactly the true non-zero AMCEs; 314 detect those AMCEs, plus one false-positive result; three experiments do not yield any false-positive ﬁndings, but missed one non-zero eﬀect.

Table 2 shows the trade-oﬀ in using correction methods. On the one hand, the use of a correction method dramatically improves the number in the shaded cells. In contrast to 248 without correction, almost all correction methods ﬁnd the truth in more than 600 samples. On the other hand, as the Sum column indicates, all correction methods produce false negatives more often than the standard approach. Reducing the number of false positives

4SI B.2 describes simulation parameters.

##### No. of False Positives 0 1 2 3 4 5 6 7 8

##### No corr. 1 230 290 215 123 69 42 19 9 3 Bonf. corr. 1 966 32 2 BH corr. 1 931 61 7 1 ashUnif corr. 1 996 4 ashNorm corr. 1 998 2

##### No. of True Positives

###### (a) Baseline

No. of False Positives 0 1 2 3 4 5 6 7 8 9 10 11 12

No corr. 1 237 253 223 134 83 38 17 6 2 6 1 Bonf. corr. 1 962 37 1 BH corr. 1 930 55 7 5 1 1 1 ashUnif corr. 1 984 14 2 ashNorm corr. 1 987 12 1

No. of True Positives

(b) Larger Error Variance

No. of False Positives 0 1 2 3 4 5 6 7 8 9 10

No corr. 1 191 288 228 125 79 42 30 9 3 2 3 Bonf. corr. 1 951 43 6 BH corr. 1 902 83 12 3 ashUnif corr. 1 982 15 3 ashNorm corr. 1 985 13 2

No. of True Positives

(c) Larger Heterogeneous AMCE and Error Variance

- Table 1: Number of Data Sets for Each Number of True- and False-positive Findings when the AMCE of Gender is Non-zero. (a) The eﬀect of male is −.06 and the eﬀects of female and all other attributes are drawn independently from N(0,.0152). The error variance of the regression model for continuous responses is .012. (b) AMCEs are identical to Table 1a, but the error variance of the regression model is .12. (c) The eﬀect of male and the other attributes and the error variance are identical to Table 1b, but the eﬀect of female is independently drawn from N(0,.122). Empty cells indicate zero.


No. of False Positives 0 1 2 3 4 5 6 7 8 9 10 Sum

- 9 3 2 1 2 2 10

- 10 248 314 195 116 56 33 14 9 2 2 1 990


No corr.

- 8 35 3 38

- 9 289 13 1 303

- 10 625 33 1 659


Bonf corr.

No. of True Positives

- 8 1 1

- 9 45 17 6 2 70

- 10 589 253 57 16 9 4 1 929


BH corr.

- 8 18 1 19

- 9 151 18 4 3 176

- 10 620 151 26 3 4 1 805


ashUnif corr.

- 8 15 2 17

- 9 178 23 6 1 208

- 10 645 106 18 3 2 1 775


ashNorm corr.

###### Table 2: Number of Data Sets for Each Number of True- and False-positiveFindings when the True AMCEs of All levels in Gender, Education, and Englishare Non-zero. Obtaining ten true positives and zero false positives (shaded) is the groundtruth. Empty cells indicate zero.

###### comes at a cost of increasing the number of false negatives. Moreover, the trade-oﬀ exists among the correction methods, too. As the most conservative correction method, the BC produces false negatives in about 30% of experimental trials. The BH is least likely to miss the true AMCEs, but it produces more false-positive conclusions than the other two. The Ash takes the middle ground: it produces false-negative ﬁndings less likely than the BC, and false-positive results less likely than the BH.

###### Given this trade-oﬀ, should researchers use a correction method? In Figure 3 and Table 1, the answer is clear: any correction method dominates non-correction. When only zero or one attribute level has AMCE, the use of correction methods reduces the risk of false-positive ﬁndings at no cost since there is nothing to be missed. However, if many levels have AMCEs

###### as in Table 2, correction methods decrease the number of false positives in exchange for anincrease of the number of false negatives. Hence, correction methods may not be uniformlybetter than not correcting.

###### Figure 4 presents a measure to evaluate this trade-oﬀ. It shows the distribution of the True Positive Rate (TPR) minus the False Positive Rate (FPR) across samples in the same

###### No Correction

Density

051015202530

0.70 0.75 0.80 0.85 0.90 0.95 1.00

TPR − FPR

###### Bonferroni Correction

Density

051015202530

0.70 0.75 0.80 0.85 0.90 0.95 1.00

TPR − FPR

###### Benjamini−Hochberg

Density

051015202530

0.70 0.75 0.80 0.85 0.90 0.95 1.00

TPR − FPR

###### Ash Uniform Mixture

Density

051015202530

0.70 0.75 0.80 0.85 0.90 0.95 1.00

TPR − FPR

Density

###### Ash Normal Mixture

051015202530

0.70 0.75 0.80 0.85 0.90 0.95 1.00

TPR − FPR

TPR = True Positive / Total Positive FPR = False Positive / Total Negative

###### Figure 4: Density Histograms of the Diﬀerence between True Positive Rate (TPR)and False Positive Rate (FPR). A larger value on the x-axis indicates better performence.The ﬁgure is based on the same simulations as Table 2.

simulations as Table 2. The TPR is the number of true positives divided by the number of true non-zero AMCEs while the FPR is the number of false positives divided by the number of true zero AMCEs. If a test is perfect, its TPR is one and FPR is zero, because the ideal test ﬁnds all non-zero AMCEs and does not falsely reject the null on any zero AMCEs. Therefore, the higher density is concentrated on the right in Figure 4, the better. The ﬁgure shows that the BH and the Ash achieve a value larger than .85 in almost all simulated samples while the distribution without correction has a longer tail on the left. The ﬁgure indicates that researchers are more likely to get the ideal outcome with a correction method than without any.

These simulations demonstrate the promise and pitfalls of multiple testing correction methods. First, researchers should always use some correction method when conducting conjoint survey experiments. Since conjoint analysis inherently requires a large number of hypothesis tests, some, if not all, statistically signiﬁcant ﬁndings are likely to be false positives. Second, the risk of false-positive ﬁndings cannot be entirely eliminated, and correction methods diﬀer across the ability and cost of reducing the number of false positives. The BC is most aggressive in avoiding false positives, but its cost of missing true ﬁndings may be substantial. The BH is the opposite, and the Ash is in between the two. Although none

provides the perfect solution, researchers should choose a correction method that best suits their needs. In particular, the choice should be based on a careful assessment on the relative tolerance of false positives and false negatives.5 We provide a checklist as an additional guidance in concluding remarks.

## 5 Reanalysis

To illustrate how the use of the correction methods may change empirical conclusions, we apply the correction methods to two published applications of conjoint experiment.6 Overall, the pattern we observe in the reanalysis is consistent with the simulations. The BC reduces the number of ﬁndings the most, and some of the results that are changed to null are substantively questionable. On the other hand, the BH does not eliminate any ﬁndings of the original papers. The Ash corrects fewer ﬁndings away than the BC, but its results seem to make the most substantive sense.

### 5.1 Selecting Immigrants in the US

In the seminal paper on conjoint designs for causal inference, Hainmueller, Hopkins and Yamamoto (2014) employs the conjoint design to explore the AMCEs of immigrants’ attributes on preference for admission to the United States. There are nine attributes: Gender, Education, Language, Origin, Profession, Job experience, Job plans, Application reasons, and Prior trips to U.S.. To exclude unrealistic attributes combinations, the randomization for Education, Profession, Country of Origin, and Application reasons are conditionally independent given some constraints, and the randomization for the other ﬁve attributes are completely independent. The outcome variable is whether a respondent prefers a given proﬁle in a paired comparison.

We focus on two attributes, Country of origin and Profession, shown in Figure 5.7 The left panel of Figure 5 shows the estimates of the AMCE of each country of origin relative to India, with no correction, the BC, the BH, and the Ash. The most noticeable pattern is that the BC eliminates the statistical signiﬁcance of all estimates except for the eﬀect of Iraq. If we believe the BC results, respondents in their survey did not distinguish immigrants from India, Mexico, France, Germany, Sudan, and Somalia. On the other hand, coeﬃcients adjusted by the BH and the Ash largely preserve the original paper’s conclusion that immigrants from Sudan, Somalia, and Iraq are less preferred than those from India.

The right panel of Figure 5 presents the results on the Profession attribute. Janitor is the reference category. The original results suggest that there is a bonus for ﬁnancial

5Additional simulation results with more noisy data are shown in SI B.3 6SI D.3 shows the reanalysis of another paper in comparative politics. 7For the entire replication results, see SI Figure D.1.

Computer programmer

Construction worker

Child care provider

Research scientist

Financial analyst

Gardener

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

Teacher

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

Doctor

Waiter

Nurse

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

−0.2−0.100.10.2

BH

BH

BH

BH

BH

BH

BH

Janitor

Janitor

Janitor

Janitor

Janitor

Janitor

Janitor

Janitor

Janitor

Janitor

Philippines

Germany

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

ash.Norm

Somalia

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

ash.Unif

Mexico

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

no Corr.

Poland

France

Sudan

China

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Bonf.

Iraq

−0.2−0.100.10.2

BH

BH

BH

BH

India

India

India

India

India

India

India

India

India

###### Figure5:EﬀectsoftheImmigrant’sCountryofOrigin(left)AndProfession(right)ontheProbabilityofBeing

onregressionestimatorswithclusteredstandarderrorsatrespondentlevel;barsrepresent95%conﬁdenceintervals.Barswith

PreferredforAdmissiontotheUnitedStates.For,thereferencecategoryisIndia;for,countryoforiginprofession

solidcirclesareestimateswithnocorrection,whichreplicatecorrespondingattributesinFigure3ofHainmueller,Hopkinsand

the reference category is janitor.The plot shows estimates with no correction,the BC (),the Ash with a mixture of normalBonf

nexttopointestimatesindicatesBHcorrectedcoeﬃcientissigniﬁcantforthatspeciﬁcattributelevel.Estimatesarebased

components(),andtheAshwithamixtureofuniformcomponents()foreachpairofcomparison.ash.Normash.UnifBH

Yamamoto(2014,p.21).

analysts, construction workers, teachers, computer programmers, nurses, research scientists, and doctors. Again, the BC renders more coeﬃcients insigniﬁcant: ﬁnancial analysts and computer programmers are indistinguishable from janitors. While the BH preserves all the original ﬁndings, the Ash changes the results for construction workers—the bonus for construction workers is indistinguishable from zero. The Ash result is in fact consistent with the argument of the original paper that high-skilled immigrants are preferred to low-skilled workers.

While we cannot adjudicate on the diﬀerences with certainty because the true value is unknown, some correction methods lead to more substantively understandable results over the others. The BC seems overly conservative, and its null ﬁndings may require further theoretical justiﬁcation. The BH results agree with most non-corrected results, including some unexpected signiﬁcant estimates. The Ash corrects some ﬁndings away but not as aggressively as the BC does, and it leads to conclusions that make most substantive sense in this application.

### 5.2 Selecting Trading Partners in Vietnam

Conjoint experiment is also useful in examining attributes of units other than individuals. Spilker, Bernauer and Uman˜a (2016) explores what types of countries are preferred partners for Preferential Trade Agreements (PTAs) by conducting conjoint surveys in Costa Rica, Nicaragua, and Vietnam. They include eight attributes in their design: Distance from the partner country’s capital with three levels; Size of the economy with three levels; Culture, a binary variable indicating similarity in tradition and language of the partner country; Religion, which contains three religions for Costa Rica and Nicaragua and four religions for Vietnam; Political system, three levels of the extent to which citizens democratically elect political leaders; Military ally, a binary variable indicates whether the partner country has a security alliance with respondents’ home country; Environmental protection standards and Worker rights protection standards, each takes three levels. All these attributes are completely randomized and no proﬁle is excluded in the original surveys. The outcome is binary, whether respondents choose a country proﬁle in a paired comparison.

Figure 6 focuses on the eﬀect of two attributes Military ally and Environmental protection standards on the respondents in Vietnam.8 Among the three countries, Vietnam is the only one where non-military allies are punished relative to military allies. The original paper justiﬁes the ﬁnding by its geopolitical location and military-security rivalries in the region (Spilker, Bernauer and Uman˜a, 2016, p.710,714). However, Vietnam has a “Three Nos” defense policy since 1998: no military alliance, no aligning with one country against another,

8The complete replication results can be found in Figure D.2 of Supplementary Appendices.

Military (Ally) no Corr.

BH

Bonf.

ash.Unif

ash.Norm

Envir. std. (Lower)

BH

no Corr.

Bonf.

ash.Unif

ash.Norm

Envir. std. (Lower)

BH

no Corr.

Bonf.

ash.Unif

ash.Norm

0.1 0 0.1

Change in Pr(Country preferred as partner)

Not Ally

Higher std.

Similar std.

- Figure 6: Eﬀects of Military Ally (Top) and Environmental Protection Standards (bottom) on the Probability of Being Preferred as Trading Partners in Vietnam. For Military ally, the reference category is allied; for Environmental Protection Standards, the reference category is lower standards. The plot shows estimates with no correction, the BC (Bonf), the Ash with a mixture of normal components (ash.Norm), and the Ash with a mixture of uniform components (ash.Unif) for each pair of comparison. BH next to point estimates indicates the BH corrected coeﬃcient is signiﬁcant for that speciﬁc attribute level. Estimates are based on regression estimators with clustered standard errors


- at respondent level; bars represent 95% conﬁdence intervals. Bars with solid circles are estimates with no correction, which replicate corresponding attributes in Figure 1.3 in Spilker, Bernauer and Uman˜a (2016, p.715).


and no foreign military bases on Vietnamese soil.9 The context makes it diﬃcult to interpret the signiﬁcant result, because it is unclear what military allies mean to Vietnam given this defense policy. While the BH preserves the original ﬁnding, the BC and the Ash correct it away.

For environmental standards, while the preference for higher standards relative to lower standards is robust to diﬀerent correction results, the bonus for countries with similar standards is not. Again, the BC and the Ash render it a false positive conclusion. The BH agrees completely with the original conclusion, but we cannot rule out the possibility that this is

9Socialist Republic of Vietnam Ministry of National Defence, 2009.

guaranteed by the design of BH: there are not enough signiﬁcant discoveries to begin with to control for FDR. A lower FDR may be needed to accommodate the smaller number of signiﬁcant ﬁndings in social science researches.

The replication exercise demonstrates the usefulness of applying correction methods in conjoint design from a substantive perspective. Correction methods could raise alarms of potential limitations in the proﬁle design. Such warnings would be valuable especially in the phase of pilot research or pretesting. Moreover, results that stand the test of correction would help authors make more convincing arguments. In this application, the authors of the original paper needed to justify their ﬁnding on the preference for military allies only in Vietnam, but it is diﬃcult to interpret this ﬁnding given the fact that Vietnam has not have military allies for a while and will not for the foreseeable future. The authors could have avoided interpreting this result by using the BC or the Ash, even though they included the Military ally attribute, which should have been excluded from the design.

## 6 Concluding Remarks

Conjoint analysis is widely used in political science because it allows researchers to estimate the eﬀects of many variables on preference formation. Unfortunately, exactly because it is designed for estimating multiple eﬀects, statistical inference on estimates in conjoint designs suﬀers from the multiple testing problem. However, few systematic assessments on the severity of the problem and little empirical guidance on the choice of correction methods have been provided. In a series of simulations and applications to published data, we examined the probability of getting false positive conclusions from a typical conjoint survey experiment, and compared the performance of three oﬀ-the-shelf multiple testing correction methods.

Although some correction is always better than no corrections, none of the methods provides the perfect solution to the problem. The Bonferroni correction is most conservative. Therefore, it is least likely to mislead researchers to false positive conclusions while it is most likely to mislead researchers to false negative conclusions. The Benjamini-Hochberg procedure is the opposite. We even found that the Benjamini-Hochberg procedure does not change the statistical signiﬁcance of any estimates in some applications. The adaptive shrinkage method takes a middle ground between the two. While it reduces the probability of false positives than the Benjamini-Hochberg, it avoids false negatives better than the Bonferroni correction.

Whether being conservative (or lenient) is a virtue rather than a vice depends on the purpose of researchers. We believe that the adaptive shrinkage method should be recommended when researchers do not have much prior knowledge on the existence of AMCEs, because it is unclear which of false positives or false negatives the researchers need to avoid more.

Design

Pre-registration Analysis

###### Step 1: Research Goal

Step 2: Methods& Set Parameters

###### Step 3: Report & Discuss

? Report

? Bonferroni (Bonf.) The total number of testsis______

? Confirmatory

Both the uncorrected and corrected estimates

E.g., Existing studies have used similar attributes to answer similar questions.

? Justify

? Adaptive Shrinkage (Ash)

The choice correction methods E.g., False-positive versus False-negative tradeoff

M ixture distribution ______

? Exploratory

E.g., Uniform, Normal, etc.

E.g., There is no known research that 1) uses similar attributes, 2) answers similar research questions, or 3) both.

? Benjemini-Hochberg (BH )

? Elaborate

FDR tolerance level ______

E.g., If the corrected estimates and uncorrected estimates disagree

E.g., FDR equals 0.05 means that 5% of "declared" positives are false positives.

? Others_____________

###### Figure 7: Checklist for Multiple Hypothesis Testing in Conjoint Analysis.

However, the Benjamini-Hochberg procedure might be preferred if previous studies strongly suggest the existence of AMCEs, whereas the Bonferroni correction should be recommended for AMCEs whose existence is considered unlikely. In the former, although the rejection of the null is not surprising, researchers can cast more doubt on the prior knowledge if the null is accepted. In the latter case, passing a more conservative test is valuable information because it is more likely to be a new ﬁnding. The comparison in our paper provides a guide in selecting the correction method that suits a particular application.

Figure 7 summarizes our recommendations on the use of multiple testing correction methods in conjoint analysis. It helps researchers reduce missing steps and ensures consistency and completeness. Importantly for our purpose, it guides researchers to contemplate a series of questions related to multiple hypothesis testing at diﬀerent stages of the study. The checklist is divided into three sections, design, pre-registration, and analysis.

During the design phase, scholars determine their research objective, whether the conjoint experiment is to conﬁrm ﬁndings in existing studies or it is exploratory in nature. The distinction between the two types of research is fuzzy in many empirical studies. This item is not designed to force researchers to choose one or the other, but rather it reminds them to be more precise, and their inclination will provide a direction for the pre-registration stage.

As discussed above, if the research objective is conﬁrmatory, we recommend that researchers use the more stringent Bonferroni correction and specify the number of tests they

plan to conduct in the pre-registration. The number of tests is the collection of meaningful inferences from a substantive perspective, deﬁned by the researchers. Usually, the bare minimum includes all the possible attribute-level combinations10. It should also include all the subgroup analysis, balancing checks, and other quality check tests that researchers usually perform.11 On the contrary, we recommend the more lenient Benjamini-Hochberg method if the research is primarily exploratory. Here researchers need to specify the FDR. For instance, the default FDR in many R packages is set at 0.05, meaning that 5% of the “declared” positive ﬁndings will be purged as false positives. For the remaining types, we recommend Ash. Researchers need to specify the mixture distribution they are going to use.12 Setting the mixture distribution requires some prior knowledge of the subject matter. However, because the number of hypothesis testing in most social science applications is not so large, the corrected results do not diverge drastically when diﬀerent mixture distributions are used, as our simulation studies demonstrate.

In the analysis and writeup stage, uncorrected and corrected data should be included in the paper regardless of the chosen method. Researchers should consider the false-positive and the false-negative tradeoﬀ in this particular application and justify the method of choice. If any of the corrected and uncorrected results diﬀer, the discrepancy should be described and discussed explicitly. In summary, the steps in the checklist are intended to reduce the researchers’ degrees of freedom when selecting diﬀerent methods. Furthermore, it aids researchers in incorporating multiple testing correction into the conjoint analysis routine in a principled and transparent manner.

Multiple hypothesis testing may also be a problem with empirical studies using other methods than conjoint designs. In fact, one of the major sources of publication bias is the property of the frequentist hypothesis testing that the probability of false ﬁndings is controlled. We focused on conjoint analysis in this paper because the number of hypotheses

- 10 Cross-attribute constraints will reduce the total number of tests. For example, the impossible combina-

tion of someone whose occupation is a doctor and education level is no formal education school should not be included in the total number when determining the new signiﬁcance level α˜ in Bonferroni correction.

- 11 A reviewer pointed out that some attributes or levels may be included in a conjoint design only to make


its proﬁles look real and therefore it may be more appropriate that estimates for such attributes/levels are not counted as hypotheses to be tested. On the one hand, we agree that, if an attribute is used only for that purpose and not in the study’s interest, the number of levels of the attribute can be excluded from the number of hypotheses to be tested. On the other hand, we note that estimates for all levels of all attributes are reported in most previous studies using conjoint surveys. If one excludes some attributes or levels from hypotheses, statistical estimation of the marginal means or AMCEs should ignore those attributes or levels entirely and the analysis is preregistered as such. Researchers also need to be cautious when including attributes or levels that are not interested, because the estimates of the researchers’ interest depend on the distribution of those non-interested attributes or levels (de la Cuesta, Egami and Imai, 2022).

12The ash function in the ashr package (version 2.2-47) supports uniform, normal, halfuniform, +uniform,

-uniform, and halfnormal distributions. For more information, see Stephens et al. (2020).

to be tested is relatively unambiguous. Applying the correction methods we discussed to studies where the number of statistical hypotheses varies over the stages of research, e.g., adding robustness checks to address reviewers’ comments, is much harder than to conjoint designs. More research on multiple testing correction in the other contexts is warranted.

## References

Abramson, Scott F, Korhan Ko¸cak and Asya Magazinnik. 2022. “What Do We Learn About Voter Preferences From Conjoint Experiments?” American Journal of Political Science (forthcoming).

Abramson, Scott, Korhan Kocak, Asya Magazinnik and Anton Strezhnev. 2020. “Improving Preference Elicitation in Conjoint Designs using Machine Learning for Heterogeneous Eﬀects.”.

Bansak, Kirk, Jens Hainmueller, Daniel J Hopkins and Teppei Yamamoto. 2018. “The Number of Choice Tasks and Survey Satisﬁcing in Conjoint Experiments.” Political Analysis 26:112–119.

Bansak, Kirk, Jens Hainmueller, Daniel J. Hopkins and Teppei Yamamoto. 2021a. “Beyond the breaking point? Survey satisﬁcing in conjoint experiments.” Political Science Research and Methods 9:53–71.

- Bansak, Kirk, Jens Hainmueller, Daniel J Hopkins and Teppei Yamamoto. 2021b. “Conjoint Survey Experiments.” In Advances in Experimental Political Science, ed. James Druckman and Donald P. Green. Cambridge University Press.
- Bansak, Kirk, Jens Hainmueller, Daniel J Hopkins and Teppei Yamamoto. 2022. “Using Conjoint Experiments to Analyze Elections: The Essential Role of the Average Marginal Component Eﬀect (AMCE).” Political Analysis First View:1–19.


Benjamini, Yoav and Daniel Yekutieli. 2001. “The Control of the False Discovery Rate in Multiple Testing under Dependency.” The Annals of Statistics 29:1165–1188.

Benjamini, Yoav and Yosef Hochberg. 1995. “Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing.” Journal of the Royal Statistical Society: Series B (Methodological) 57:289–300.

Bland, J. Martin and Douglas G. Altman. 1995. “Multiple Signiﬁcance Tests: The Bonferroni Method.” BMJ 310:170.

Carnes, Nicholas and Noam Lupu. 2016. “Do Voters Dislike Working-Class Candidates? Voter Biases and the Descriptive Underrepresentation of the Working Class.” American Political Science Review 110:832–844.

Clayton, Katherine, Jeremy Ferwerda and Yusaku Horiuchi. 2021. “Exposure to Immigration and Admission Preferences: Evidence from France.” Political Behavior 43:175–200.

de la Cuesta, Brandon, Naoki Egami and Kosuke Imai. 2022. “Improving the External Validity of Conjoint Analysis: The Essential Role of Proﬁle Distribution.” Political Analysis 30:19–45.

Dunn, Olive Jean. 1961. “Multiple Comparisons among Means.” Journal of the American Statistical Association 56:52 – 64.

Egami, Naoki and Kosuke Imai. 2019. “Causal Interaction in Factorial Experiments: Application to Conjoint Analysis.” Journal of the American Statistical Association 114:529–540.

Fournier, Patrick, Stuart Soroka and Lilach Nir. 2020. “Negativity Biases and Political Ideology: A Comparative Test across 17 Countries.” American Political Science Review 114:775–791.

Ganter, Flavien. 2021. “Identiﬁcation of Preferences in Forced-Choice Conjoint Experiments: Reassessing the Quantity of Interest.” Political Analysis First View:1–15.

Gerard, David and Matthew Stephens. 2018. “Empirical Bayes Shrinkage and False Discovery Rate Estimation, Allowing For Unwanted Variation.” Biostatistics.

Hainmueller, Jens and Daniel J. Hopkins. 2015. “The Hidden American Immigration Consensus: A Conjoint Analysis of Attitudes toward Immigrants.” American Journal of Political Science 59:529–548.

Hainmueller, Jens, Daniel J. Hopkins and Teppei Yamamoto. 2014. “Causal Inference in Conjoint Analysis: Understanding Multidimensional Choices via Stated Preference Experiments.” Political Analysis 22:1–30.

Hainmueller, Jens, Dominik Hangartner and Teppei Yamamoto. 2015. “Validating Vignette and Conjoint Survey Experiments Against Real-world Behavior.” Proceedings of the National Academy of Sciences 112:2395–2400.

Hochberg, Yosef and Ajit C Tamhane. 1987. Multiple comparison procedures. John Wiley & Sons, Inc.

Horiuchi, Yusaku, Zachary D. Markovich and Teppei Yamamoto. 2020. “Does Conjoint Analysis Mitigate Social Desirability Bias?” Political Analysis 30:535–549.

Incerti, Trevor. 2020. “Corruption Information and Vote Share: A Meta-Analysis and Lessons for Experimental Design.” American Political Science Review 114:761–774.

Leeper, Thomas J., Sara B. Hobolt and James Tilley. 2020. “Measuring Subgroup Preferences in Conjoint Experiments.” Political Analysis 28:207–221.

Liu, Hanzhang. 2019. “The Logic of Authoritarian Political Selection: Evidence from a Conjoint Experiment in China.” Political Science Research and Methods 7:853–870.

Oliveros, Virginia and Christian Schuster. 2018. “Merit, Tenure, and Bureaucratic Behavior: Evidence From a Conjoint Experiment in the Dominican Republic.” Comparative Political Studies 51:759–792.

Ono, Yoshikuni and Barry C. Burden. 2019. “The Contingent Eﬀects of Candidate Sex on Voter Choice.” Political Behavior 41:583–607.

Sen, Maya. 2017. “How Political Signals Aﬀect Public Support for Judicial Nominations: Evidence from a Conjoint Experiment.” Political Research Quarterly 70:374–393.

Shafranek, Richard M. 2021. “Political Considerations in Nonpolitical Decisions: A Conjoint Analysis of Roommate Choice.” Political Behavior 43:271–300.

Sjo¨lander, Arvid and Stijn Vansteelandt. 2019. “Frequentist versus Bayesian Approaches to Multiple Testing.” European Journal of Epidemiology 34:809–821.

Spilker, Gabriele, Thomas Bernauer and V´ıctor Uman˜a. 2016. “Selecting Partner Countries for Preferential Trade Agreements: Experimental Evidence From Costa Rica, Nicaragua, and Vietnam.” International Studies Quarterly 60:706–718.

Stephens, Matthew. 2017. “False Discovery Rates: A New Deal.” Biostatistics 18:275–294. Stephens, Matthew, Peter Carbonetto, David Gerard, Mengyin Lu, Lei Sun, Jason Willwer-

scheid and Nan Xiao. 2020. ashr: Methods for Adaptive Shrinkage, using Empirical Bayes. URL: https://CRAN.R-project.org/package=ashr

Teele, Dawn Langan, Joshua Kalla and Frances Rosenbluth. 2018. “The Ties That Double Bind: Social Roles and Women’s Underrepresentation in Politics.” American Political Science Review 112:525–541.

