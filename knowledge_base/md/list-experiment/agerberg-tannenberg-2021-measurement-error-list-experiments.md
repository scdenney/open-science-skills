###### 1013154RAP0010.1177/20531680211013154Research & PoliticsAgerberg and Tannenberg

![image 1](agerberg-tannenberg-2021-measurement-error-list-experiments_images/imageFile1.png)

research-article20212021

###### Research Article

# Dealing with measurement error in list experiments: Choosing the right control list design

Research and Politics April-June 2021: 1–8 © The Author(s) 2021 Article reuse guidelines: sagepub.com/journals-permissions DOI: 10.1177/20531680211013154 journals.sagepub.com/home/rap

https://doi.org/10.1177/20531680211013154

## Mattias Agerberg and Marcus Tannenberg

##### Abstract

List experiments are widely used in the social sciences to elicit truthful responses to sensitive questions. Yet, the research design commonly suffers from the problem of measurement error in the form of non-strategic respondent error, where some inattentive participants might provide random responses. This type of error can result in severely biased estimates. A recently proposed solution is the use of a necessarily false placebo item to equalize the length of the treatment and control lists in order to alleviate concerns about respondent error. In this paper we show theoretically that placebo items do not in general eliminate bias caused by non-strategic respondent error. We introduce a new option, the mixed control list, and show how researchers can choose between different control list designs to minimize the problems caused by inattentive respondents. We provide researchers with practical guidance to think carefully about the bias that inattentive respondents might cause in a given application of the list experiment. We also report results from a large novel list experiment fielded to over 4900 respondents, specifically designed to illustrate our theoretical argument and recommendations.

Keywords List experiment, non-strategic respondent error, placebo item, sensitive questions, control list design

## Introduction

While list experiments remain popular in the social sciences, several studies have highlighted the problem of measurement error in the form of non-strategic respondent error, where some inattentive subjects might provide random responses to the list (Ahlquist, 2018; Alvarez et al., 2019; Blair et al., 2019; Kramon and Weghorst, 2019). Given that the length of the treatment and control list differs, this type of error can result in heavily biased estimates. To address this issue, a recent study recommends the use of a necessarily false placebo item1 in order to equalize the length of the treatment and control lists and, in turn, alleviate concerns about respondent error (Riambau and Ostwald, 2020) (see also Ahlquist et al. (2014) and De Jonge and Nickerson (2014)).

In this paper we show that placebo items are not a straightforward universal solution to the problem of nonstrategic respondent error in list experiments and that their inclusion can even increase bias in many cases. In

general, modifying the length of the control list will not eliminate bias caused by inattentive respondents. However, we show that researchers, by carefully considering the expected bias associated with a specific control list design, can choose a design that minimizes the problems caused by non-strategic respondent error. In addition to the conventional and placebo control list, we introduce a novel third alternative, the mixed control list, that combines the two former designs. We calculate the expected bias associated with each control list design and

University of Gothenburg, Sweden Corresponding author: Mattias Agerberg, University of Gothenburg, Sprängkullsgatan 19, Göteborg, 41123, Sweden. Email: mattias.agerberg@gu.se

Correction (June 2025): The article has been updated with correct dataverse link in the supplementary material section. For more details, please see the correction notice 10.1177/20531680251326800.

![image 2](agerberg-tannenberg-2021-measurement-error-list-experiments_images/imageFile2.png)

Creative Commons Non Commercial CC BY-NC: This article is distributed under the terms of the Creative Commons Attribution-NonCommercial 4.0 License (https://creativecommons.org/licenses/by-nc/4.0/) which permits non-commercial use,

reproduction and distribution of the work without further permission provided the original work is attributed as specified on the SAGE and Open Access pages (https://us.sagepub.com/en-us/nam/open-access-at-sage).

provide concrete recommendations for researchers for choosing between them in different situations. Using data from a recent meta analysis (Blair et al., 2020), we show that a clear majority of existing studies using list experiments might have benefited from a non-conventional control list design. We also report results from from a large list experiment fielded in China to over 4900 respondents, designed to test our theoretical predictions. The study includes a novel approach to designing placebo items that we recommend researchers to use whenever the inclusion of such an item is warranted. We conclude by discussing the general implications of our results and summarize our overall recommendations for researchers using the list experiment.

## Setup

The list experiment works by aggregating a sensitive item of interest with a list of control items to protect respondents’ integrity (Glynn, 2013). We adopt the notation in Blair and Imai (2012) and consider a list experiment with J binary control items and one binary sensitive item denoted Zi,J+1 . Respondents are randomly assigned to either a control group (Ti = 0 ) and given the list with J control items, or to a treatment group (Ti =1 ), given the list with with J control items and the sensitive item Zi,J+1 . The total number of items in the treatment group is thus J +1. Yi denotes the observed response to the list experiment for respondent i (the total number of items answered affirmatively). If we denote the total number of affirmative answers to J

control items with Yi* , the process generating the observed response can be written as:

Yi = TiZi,J+1 +Yi*

(1)

Blair and Imai (2012) show that if we assume that the responses to the sensitive item are truthful (“no liars”) and that the addition of the sensitive item does not alter responses to the control items (“no design effects”), the proportion of affirmative answers to the sensitive item, denoted τ, can be estimated by taking the difference between the average response among the treatment group and the average response among the control group, that is, a difference-in-means (DiM) estimator. The DiM estimator can be written as:

N

N

1 1

 =

i i (2)

T Y

(1 ) N1 =1 0 =1

TY

i i

N

i

i

where τ is the estimated proportion affirmative answers to the sensitive item, N1 = Ti is the size of the treatment group and N0 = N − N1 is the size of the control group.

#### ∑N

i=1

When assignment to the treatment group is random and we invoke the two assumptions above, the DiM estimator is unbiased: E[Yi |Ti =1] E[Yi |Ti = 0] = 0 (Blair et al., 2019).

## Non-strategic respondent error and bias

### Modeling inattentive respondents

Strategic respondent error in list experiments, where the respondent for instance might avoid selecting the maximum or minimum number of items, can generally be minimized by choosing control items (non-sensitive items) in a well-thought-out manner (Glynn, 2013). Non-strategic respondent error, on the other hand, arises when respondents provide a random response to the list experiment. This type of respondent error is likely to be prevalent when respondents do not pay enough attention to the survey (Berinsky et al., 2014) or when respondents resort to satisficing (Krosnick, 1991). Given that the list lengths differ between the treatment and control group, this type of error will often be correlated with treatment assignment and can hence dramatically increase both bias and variance in the estimate of interest (Ahlquist, 2018; Blair et al., 2019).

We refer to respondents providing random responses as inattentive2 and let Wi =1 if a respondent is inattentive (Wi = 0 otherwise). Blair et al. (2019) model inattentives as providing responses to the list experiment according to a discrete uniform distribution U{0, J}, that is, by randomly picking a number between 0 and J ( J +1 in the treatment group). We refer to this as the uniform error model. The process generating the observed response under this model can be written as:

*

Y W T Z Y W TU T U

= (1 )( ) ( (1 ) )

i i i i J i i i J

, 1

{0, 1}

i J

{0, }

(3)

The consequences of this error process in terms of bias in the estimate of τ (see below) are identical to several other plausible error processes. We discuss this further in Appendix A.

Let s denote the share of inattentive respondents. As shown by Blair et al. (2019) [appendix A], under the uniform error model, the bias of the difference-in-means estimator (E[Yi |Ti =1] E[Yi |Ti = 0] ) amounts to:

J

- 1
- 2


*

{ (1 )( )

E

s Y Z s

, 1

i i J

J

*

E

(1 )

s Y s

}

i

2

J J ) s

- 1
- 2 2


- 1
- 2


ss s

= (1

=

(4)

This follows from the fact that the expected value of a (discrete) uniform distribution is a +b

, where the interval

2

≠

[a,b] denotes the support of the distribution. The expected difference between the treatment and control group for inattentive respondents is thus:

##### E E E

[ | =1] = [ | =1, =1] [ | = 0, =1] =

W Y T W Y T W

i i i i

J J

- 1
- 2 2


- 1
- 2


=

i i i

(5)

The amount of bias will hence be larger when τ is further away from

- 1
- 2


and the estimate will be “pulled” toward as s increases. What is sometimes referred to as “artifi-

- 1
- 2


cial inflation” (De Jonge and Nickerson, 2014; Riambau and Ostwald, 2020) is simply what we would expect under

- 1
- 2


this error process, as long as τ<

.

### Introducing a placebo item

How is the amount of bias affected by the introduction of a placebo item? When adding a placebo item (with expected value equal to 0) to the control list, the bias under this error model3 instead becomes:

J

- 1
- 2


*

{ (1 )( )

E

s Y Z s

, 1

i i J

J

- 1
- 2


*

E

(1 )

s Y s

}

i

J J

- 1
- 2


- 1
- 2


11 )

s s =

=(

s

(6)

Hence, without a placebo item the bias will be 0 only when τ=

- 1
- 2


, and with a placebo item the bias will be 0 only

when τ= 0 (assuming s is fixed and positive). The addition of the placebo item will thus in general cause negative bias ( s ) under the uniform-error model. This is because the expected estimated prevalence of the sensitive item in the inattentive group is 0: E[(J 1) / 2 (J 1) / 2] .

When does the addition of a placebo item decrease the absolute amount of bias? This happens when

1 4

- 1
- 2


. The addition of a placebo item will thus only decrease the absolute amount of bias when the true prevalence of Zi,J+1 is below 1

s s

> <

.

4

### The mixed control list

We also consider a third option for constructing a control list: allocating respondents in the control group to either the placebo or conventional control list. We focus on a design where respondents are allocated to the two groups with p* = 0.5

(conditional on being assigned to the control group). It is also possible to assign respondents to the different control lists with unequal probability ( p* and 1− p*, with p 0.5*), however we focus on the equal probability scenario since this is the easiest to implement.4 Under the mixed design, the bias under the uniform error model becomes:

E

J

- 1
- 2


*

{ (1 )( )

E

s Y Z s

, 1

i i J

J

J

- 1
- 2


* * *

i } =

(1 )

s Y s p

(1 )

p

2

J

- 1
- 2 2


J

J

- 1
- 2


s s * *

(1 )

p

p

(1 )

=

s

*

p

2

(7)

With p* = 0.5 (the equal probability scenario), the bias is hence 0 when τ=

1 4

.

### Which control list design should you choose?

In summary, adding a placebo item might decrease bias but should not in general be considered a silver bullet solution to the problem of non-strategic respondent error; in many cases it might even increase bias if not implemented carefully. It is clear that this type of bias varies considerably between different designs and that it has the potential to strongly influence the resulting estimate. Unfortunately, the bias caused by inattentive respondents can not be easily eliminated by modifying the control list. However, by making an informed choice regarding the control list design, the problem can be mitigated.

As the sections above show, the bias under the different control list designs – conventional, placebo, and mixed – will depend on τ (when s > 0 ). Researchers thus need to make an informed guess about the true prevalence rate to choose the best control list design in a given situation. We call this guess the predicted prevalence rate and denote it by τ* . To set τ*, researchers should rely on previous research, including other list experiments. If previous evidence is insufficient, an alternative is to run a pilot study with a few hundred respondents to estimate agreement with the direct question. Based on this estimate, τ can be approximated by making assumptions about the degree of sensitivity bias. As a starting point, Blair et al. (2020) find that sensitivity biases are typically smaller than 10 percentage points. The authors also provide a discussion of sensitivity bias in different literatures.

Which control list design to choose in a specific study depends mainly on two considerations: τ* and the specific goal of the study (e.g., what is the estimand?). If the goal of the study is to use a list experiment to get a good descriptive estimate of τ, we advocate choosing the control list design that minimizes the absolute expected bias. This amount is

Table 1. Control lists yielding (mostly) conservative estimates when testing for sensitivity bias. Predicted prevalence Hypothesized sensitivity bias Control list design Estimate

0 < * 0.25 Underreporting Placebo Conservative (pulled toward 0) 0.25 < * 0.5 Underreporting Mixed Conservative (pulled toward 0.25) 0.5 < * 1 Underreporting Conventional Conservative (pulled toward 0.5) 0 < * 0.25 Overreporting Mixed Conservative (pulled toward 0.25) 0.25 < * 0.5 Overreporting Conventional Conservative (pulled toward 0.5) 0.5 < * 1 Overreporting Conventional Non-conservative (pulled toward 0.5)

calculated by plugging in a value for τ* in equation (4), (6), and (7) and comparing the absolute value of each result.

If the goal of the study is to estimate the amount of sensitivity bias, we advocate an approach that likely will lead to a conservative estimate. Typically, researchers do not reflect upon how non-strategic respondent error may influence their list experiment estimate. In many cases this bias works in favor of the tested hypothesis: when τ is below 0.5 and the researcher wants to test if the quantity is underreported (when measured with a direct question), a list experiment with a conventional control list will pull the estimate toward 0.5 due to non-strategic respondent error. This may thus inflate the type 1 error rate – e.g., concluding that underreporting is prevalent when it is in fact negligible. Instead, we advocate choosing a control list design where potential bias due to respondent error works against the tested hypothesis. This approach is described in Table 1.

To illustrate, when τ* is assumed to be approximately 0.35 and hypothesized to be underreported, the researcher should choose the mixed design. This will pull the estimate from the list experiment toward 0.25 (the expected bias among inattentives under the mixed design) and hence yield a conservative estimate of the degree of underreporting when comparing the list estimate to a direct estimate. Note that when 0.5 < * 1 and the researcher predicts overreporting, there is no design that yields a conservative

estimate. The conventional design is still the “least bad” in this case.

To what extent are our design recommendations relevant for researchers using list experiments? To take the 264 list experiments included in Blair et al.’s (2020) meta analysis as an indication: only 36 percent of the studies have an estimated prevalence and hypothesized sensitivity bias for which the conventional control list is expected to yield the smallest bias granted a preference for a conservative estimate.5 For 37 percent, the placebo control list would have been recommended. The remaining 27 percent of the list experiments would have benefited from our proposed mixed control list design (see Figure 1). In summary, assuming a non-negligible share of inattentive respondents, the vast majority of existing studies using list experiments have used a sub-optimal control list design, among which we are more likely to find type 1 errors.

This concerns some sub-fields more than others. For example, studies of relatively low prevalence behaviors, with a hypothesized underreporting, such as vote buying (Gonzalez-Ocantos et al., 2012), clientelism (Corstange, 2018), and corruption (Agerberg, 2020; Tang, 2016) would often be recommended to choose the placebo or mixed control list in order to guard against type 1 errors. In contrast, studies of voter turnout (Holbrook and Krosnick, 2010) and support in authoritarian regimes

|![image 3](agerberg-tannenberg-2021-measurement-error-list-experiments_images/imageFile3.png)<br><br>Recommended control list: Conventional Placebo Mixed<br><br>Under− reporting<br><br>Over− reporting<br><br>0.00 0.25 0.50 0.75 1.00<br><br>Estimated prevalence|
|---|


- Figure 1. Distribution of estimated prevalence by hypothesized sensitivity bias from list experiments included in Blair et al.’s


(2020) meta analysis. Recommendations are based on a preference for a conservative estimate (see Table 1).

(Frye et al., 2017; Robinson and Tannenberg, 2019), where the hypothesized sensitivity bias concerns overreporting, are more often in the predicted prevalence range where the conventional control list is the best choice. It should be noted that several of the latter studies are in a range, ( 0.5 < * 1 ), where it is not possible to obtain conservative estimates (see bottom right of Figure 1).

## An empirical illustration

To empirically demonstrate the consequences of the different control list designs we designed a list experiment that was fielded online in China to 4973 respondents, in collaboration with the survey research company Lucid. In the experiment, one-third of respondents were assigned to a conventional control list with four items, another third to a placebo list with the same four control items plus a placebo item, and the remaining third were assigned to a treatment list with the four control items plus an additional “item of interest” (corresponding to the “sensitive item” in regular designs). By sampling from the conventional and the placebo control list with p* = 0.5 (the equal probability scenario), we create the third control group representing the mixed design.

The four items on the control list were presented in random order and two of the items were chosen to be negatively correlated, following best practice (Glynn, 2013) (see Appendix B, Table 2). The placebo list added a fifth item to match the length of the treatment list. The order of the items was randomized. The placebo item was designed to have a true expected prevalence for each respondent of 0 (see section How to choose good placebo items below for further details).

The treatment group was given the control list plus an additional item of interest. We designed the experiment so that the item of interest had the following three specific properties: (1) the true quantity of the item was known, (2) the item was independent of all items on the control list, (3) the item was independent of all (observed and unobserved) respondent characteristics. Given the focus of our study, we also wanted an item that was not sensitive, to avoid mixing strategic and non-strategic respondent error. We constructed an item of interest that met these criteria by randomly selecting one item from a separate set of items for each individual respondent in the treatment group. This set contained items regarding one’s zodiac animal, for example, “I was born in the year of the Dog or in the year of the Pig.” In China, respondents’ knowledge of their zodiac animal is safe to assume. Each given year is associated with one animal of which there are 12 in total. The specific animal combination presented to each respondent was randomly drawn with uniform probability from a set of 6 different combinations (including all 12 animals) and piped into the treatment list (see Appendix B Table 2 for the 6 zodiac statements).

Hence, agreement with the proposed item (τ) was exactly 1/ 6 in expectation for each respondent by construction. Since it is was randomly determined whether any specific respondent would agree with the item, it also had property (2) and (3).

The design allows us to estimate a known quantity (τ=1/ 6 ) using the conventional control list, the placebo list, and the mixed control list design. At this prevalence, we expect the conventional control list design to be the most biased (estimate pulled toward 0.5), the placebo design to be moderately biased (estimate pulled toward 0), and the mixed design to yield the smallest absolute bias (estimate pulled toward 0.25). This follows from equation (4), (6), and (7) (see Table 1 for a quick overview). Since this is an application where we are simply trying to estimate the prevalence of the item of interest, our recommendations suggest that we should choose the mixed control list design since this is expected to minimize the absolute bias, assuming that we set τ* to approximately 1/ 6 .

### How to choose good placebo items: the piped-in approach

Designing a good placebo item is not as easy as it may first appear. Ideally, a placebo item should be plausible for all respondents, yet by design necessarily false for any one given respondent. We propose a novel design for assigning a placebo item that can be implemented in any programmed survey, such as web-administrated or tabletadministrated surveys, where it is possible to pipe in an item utilizing information gained earlier in the survey or collected beforehand. This can be done in a number of different ways. In our application we gave survey respondents who indicated earlier in the survey that they were below 30 years of age the statement “I was born in the 70s,” and respondents who indicated that they were 30 or above the placebo statement “I was born in the 2000s.” Depending on the other items on the list, it may for example fit better to construct a contextually adjusted placebo item such as, “I was born after the September 11 attacks” for the US, or another well-known national event, by using prior data on respondents’ date of birth. Theoretically the pipe-in approach has one clear benefit vis-á-vis existing approaches. For example, in the Singaporean setting Riambau and Ostwald (2020) use “I have been invited to have dinner with PM Lee at Sri Temasek [the Prime Minister of Singapore’s residence] next week,” which they suggest is “plausible but false” for all respondents. The authors caution against using ridiculous items (such as having the ability to teleport oneself) so as not to risk compromising the perceived seriousness of the survey. We take this one step further and suggest that there is a benefit to having a placebo item that is truly plausible to signal seriousness. Using an item that is necessary true or necessary false due to implausibility, even if not

|Conventional N = 3284<br><br>Placebo N = 3310<br><br>Mixed N = 3317<br><br>0.1 0.2 0.3<br><br>Estimated prevalence|
|---|


Figure 2. DiM estimates of the item of interest using

conventional, placebo, and mixed control groups. The dotted line at τ=1/ 6 marks the true prevalence of the item being estimated.

impossible, risks signaling to the respondent that their responses are not important or valuable to the researchers, which could result in lower attentiveness.

### Results

- Figure 2 shows the estimated prevalence of the item of interest using the DiM estimator with the conventional control group (point with solid line); the placebo control group (triangle with short dotted line); and the mixed control group (square with long dotted line). The vertical dotted line notes the true prevalence of the item being estimated (τ=1/ 6 ). Notably, the true prevalence falls outside of the associated confidence intervals when using both the conventional and the placebo control group (see Appendix B, Table 4 for additional details). While the former results in an overestimation of the item by 7.6 percentage points, the latter results in an underestimation of the true prevalence by 7.9 percentage points. In this particular empirical application, it is clear that including a placebo item on the control list is no remedy, as both the conventional and placebo approaches results in similarly and severely biased estimates. It should be noted that in an application where the true prevalence of the item of interest is less than one quar-


1 4

ter (τ<

), we expect the placebo approach to yield a

smaller bias than the conventional approach (see equation 7). The observed discrepancy is likely due to standard sampling variability, which is known to be large in list experiments (Blair et al., 2020), and we can conclude that neither approach is particularly precise. The mixed design, where respondents in the control group receive (in this application were sampled from) the conventional list or the placebo list with equal probability, yields an estimate shy of the true prevalence by just 0.3 percentage points.

## Conclusions

Respondents’ lack of attention is a core threat to obtaining unbiased estimates through list experiments.

Unfortunately, this threat is not easily averted by modifying the length of the control list. The inclusion of placebo items in list experiments should hence not in general be regarded as costless and is not a universal solution to the problem of non-strategic respond errors. Rather, by modeling the error process, we show that different control list designs are associated with different kinds of bias. We focus on two control list designs from previous research, the conventional and the placebo design, and introduce a third, the mixed design.

Our first recommendation for researchers is therefore to focus on eliminating s – the share of inattentive respondents. This is the only reliable way of minimizing non-strategic respond error. Reducing the share of inattentive respondents is arguably more important in list experiments than in many other designs: The resulting measurement error not only results in noisier estimates, but is also associated with specific forms of bias, as shown in this paper. The share of inattentives in the sample can be minimized by excluding respondents who fail instructional manipulation checks or similar control questions (Berinsky et al., 2014), or by trying to increase the effort and attention among respondents in the study (see Clifford and Jerit (2015)). However, all these methods involve trade-offs. Excluding some respondents might, for instance, decrease the representativeness of the sample if attentiveness is correlated with certain respondent characteristics (Alvarez et al., 2019; Berinsky et al., 2014). How to best reduce s in the context of the list experiment is clearly an important area for future research.

Our second recommendation is to encourage researchers to think carefully about the specific bias that inattentive respondents might cause in a given study and adjust their control list design based on this. The share of inattentive respondents is often large (Alvarez et al., 2019; Berinsky et al., 2014) and it is unlikely that researchers will be able to eliminate s entirely ( s is of course in general not known). We argue that a major problem in previous studies is that the expected bias often works in favor of the researcher’s hypothesis. When estimating the prevalence of phenomena that are relatively uncommon (for instance vote buying), the list experiment might provide evidence of “underreporting” when compared with a direct question simply because the list estimate is pulled toward 0.5 by inattentive respondents under the conventional design.

We advocate the following approach for choosing and designing control lists. First, the researcher should provide a best guess regarding the true prevalence rate of the item of interest (τ* ). This guess should be guided by previous research or, potentially, by a pilot study estimating agreement with the direct question. Second, the researcher should decide on a control list design (conventional, placebo, or mixed) based on τ* and the specific goal of the study. When the goal is to simply estimate the prevalence

of the item of interest, the researcher should choose the design that minimizes the expected absolute bias. This is done by plugging τ* into equation (4), (6), and (7), and taking the absolute value. When the goal is to test for the existence of hypothesized under- or overreporting, the researcher should choose a control list design according to Table 1. This way, the bias caused by inattentive respondents will (in most cases) result in a conservative estimate that works against the tested hypothesis. There are opportunities for improvement: Using data from a Blair et al.’s (2020) meta analysis, we show that a majority of existing studies using list experiments likely would have benefited from choosing a different control list design.

Our third recommendation is for researchers to always (when possible) use our proposed piped-in approach to construct plausible placebo items, utilizing information collected previously. We view this as a distinct improvement over previous methods that is flexible and avoids undermining the credibility of the experiment by including implausible items.

We provide an empirical illustration in which we fielded a list experiment with known prevalence rate, and where one-third of respondents received the treatment list, another a conventional control list, and the remaining third a placebo list. We also constructed a mixed list from the two other control lists. The empirical study confirms many of our theoretical results: We find that the prevalence is overestimated when we use the conventional control list, but underestimated when using the placebo list. In line with our recommendations applied to the specific case, we find that the mixed list yields the estimate with lowest bias.

As our paper shows, there is no simple solution to the issue of non-strategic respondent error in list experiments without decreasing the share of inattentive respondents in the sample. However, by thinking more carefully about the expected bias in a specific application, researchers can substantially mitigate the problem.

##### Acknowledgements

We thank Adam Glynn, Jacob Sohlberg, and Kyle Marquardt for their helpful comments at the early stage of this project. We would also like to thank Eddie Yang and Shane Xuan for generous help with fine-tuning the Chinese question wording. Finally, we thank the editor at R&P and the anonymous reviewers whose comments and insightful input helped us in making the paper stronger.

##### Declaration of conflicting interests

The author(s) declared no potential conflicts of interest with respect to the research, authorship, and/or publication of this article.

##### Funding

The author(s) disclosed the following financial support for the research, authorship, and/or publication of this article: We are

grateful to Helge Ax:son Johnssons Stiftelse and Lundgrens Vetenskapsfond for financial support for data collection.

##### ORCID iDs

Mattias Agerberg https://orcid.org/0000-0001-7813-6109 Marcus Tannenberg https://orcid.org/0000-0003-0077-4711

##### Supplementary materials

The supplementary files are available at http://journals. sagepub.com/doi/suppl/10.1177/20531680211013154. The replication files can be found at https://dataverse.harvard.edu/dataset. x h t m l ? p e r s i s t e n t I d = d o i : 1 0 . 7 9 1 0 / D V N / DNHS7F&version=DRAFT

##### Notes

- 1. Riambau and Ostwald (2020) refer to this as a “placebo statement.” We define a placebo item as an item that is added to the control list in addition to the regular items but that is necessarily false for each respondent (the expected prevalence of the item is 0).
- 2. We use “inattentive” in a broad sense to also include response patterns often described as “satisficing” (Krosnick, 1991).
- 3. In Appendix A we show that the consequences of adding a placebo item are identical under at least two other plausible error models: a binomial model where each respondent agrees with each item with p = 0.5 and a model where inattentive respondents select the middle response. This also implies that any weighted average of these three error models will exhibit the same pattern of bias.
- 4. As long as τ is between 0 and 0.5, the researcher can choose to allocate respondents “optimally” (in the sense of minimizing absolute bias) between the two control groups by simply solving p*

2

=τ for p* , where τ is set by the researcher

(see equation (7) and the discussion below). However, since this type of unequal randomization is much trickier to implement on most platforms, we focus on the equal probability scenario.

- 5. Assuming each study’s estimated prevalence is our best guess for τ* .


##### Carnegie Corporation of New York Grant

This publication was made possible (in part) by a grant from the Carnegie Corporation of New York. The statements made and views expressed are solely the responsibility of the author

##### References

Agerberg M (2020) Corrupted estimates? Response bias in citizen surveys on corruption. Political Behavior 1–26.

Ahlquist JS (2018) List experiment design, non-strategic respondent error, and item count technique estimators. Political Analysis 26(1): 34–53.

Ahlquist JS, Mayer KR and Jackman S (2014) Alien abduction and voter impersonation in the 2012 U.S. general election: Evidence from a survey list experiment. Election Law Journal 13(4): 46–475.

Alvarez RM, et al. (2019) Paying attention to inattentive survey respondents. Political Analysis 27(2): 1–18.

Berinsky AJ, Margolis MF and Sances MW (2014) Separating the shirkers from the workers? Making sure respondents pay attention on self-administered surveys. American Journal of Political Science 58(3): 739–753.

Blair G and Imai K (2012) Statistical analysis of list experiments. Political Analysis 20(1): 47–77. Blair G, Chou W and Imai K (2019) List experiments with measurement error. Political Analysis 27(4): 455–480.

Blair G, Coppock A and Moor M (2020) When to worry about sensitivity bias: A social reference theory and evidence from 30 years of list experiments. American Political Science Review 114(4): 1297–1315.

Clifford S and Jerit J (2015) Do attempts to improve respondent attention increase social desirability bias? Public Opinion Quarterly 79(3): 790–802.

Corstange D (2018) Clientelism in competitive and uncompetitive elections. Comparative Political Studies 51(1): 76–104. De Jonge CPK and Nickerson DW (2014) Artificial inflation or deflation? Assessing the item count technique in comparative surveys. Political Behavior 36(3): 659–682.

Frye T, et al. (2017) Is Putin’s popularity real? Post-Soviet Affairs 33(1): 1–15.

Glynn AN (2013) What can we learn with statistical truth serum? Design and analysis of the list experiment. Public Opinion Quarterly 77(S1): 159–172.

Gonzalez-Ocantos E, et al. (2012) Vote buying and social desirability bias: Experimental evidence from Nicaragua. American Journal of Political Science 56(1): 202–217. Holbrook AL and Krosnick JA (2010) Social desirability bias in

voter turnout reports. Public Opinion Quarterly 74(1): 37–67.

Kramon E and Weghorst K (2019) (Mis)Measuring sensitive attitudes with the list experiment: Solutions to list experiment breakdown in Kenya. Public Opinion Quarterly 83(S1): 236–263.

Krosnick JA (1991) Response strategies for coping with the cognitive demands of attitude measures in surveys. Applied Cognitive Psychology 5(3): 213–236.

Riambau G and Ostwald K (2020) Placebo statements in list experiments: Evidence from a face-to-face survey in Singapore. Political Science Research and Methods: 1–8.

Robinson D and Tannenberg M (2019) Self-censorship of regime support in authoritarian states: Evidence from list experiments in China. Research & Politics 6(3). doi: 10.1177/2053168019856449.

Tang W (2016) Populist Authoritarianism: Chinese political culture and regime sustainability. Oxford: Oxford University Press.

