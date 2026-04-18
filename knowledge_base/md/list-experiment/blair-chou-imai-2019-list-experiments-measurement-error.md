.

https://www.cambridge.org/core/terms

, subject to the Cambridge Core terms of use, available at

09 Oct 2019 at 19:44:36

, on

Harvard-Smithsonian Centerfor Astrophysics

.

https://www.cambridge.org/core

Downloaded from

Political Analysis (    ) vol.   :   –    DOI:   .    /pan.    .   Published    May      Corresponding author Kosuke Imai Edited by Je  Gill

c The Author(s)     . Published by Cambridge University Press on behalf of the Society for Political Methodology.

# List Experiments with Measurement Error

## Graeme Blair , Winston Chou and Kosuke Imai

![image 1](blair-chou-imai-2019-list-experiments-measurement-error_images/imageFile1.png)

Assistant Professor of Political Science, UCLA, USA. Email: graeme.blair@ucla.edu, URL: https://graemeblair.com Ph.D. Candidate, Department of Politics, Princeton University, Princeton NJ      , USA. Email: wchou@princeton.edu, URL: http://princeton.edu/∼wchou Professor of Government and of Statistics, Harvard University,      Cambridge Street, Institute for Quantitative Social Science, Cambridge MA      , USA. Email: Imai@Harvard.Edu, URL: https://imai.fas.harvard.edu

### Abstract

Measurement error threatens the validity of survey research, especially when studying sensitive questions. Although list experiments can help discourage deliberate misreporting, they may also su er from nonstrategic measurement error due to flawed implementation and respondents’ inattention. Such error runs against the assumptions of the standard maximum likelihood regression (MLreg) estimator for list experiments and can result in misleading inferences, especially when the underlying sensitive trait is rare. We address this problem by providing new tools for diagnosing and mitigating measurement error in list experiments. First, we demonstrate that the nonlinear least squares regression (NLSreg) estimator proposed in Imai ( ) is robust to nonstrategic measurement error. Second, we o er a general model misspecification test to gauge the divergence of the MLreg and NLSreg estimates. Third, we show how to modelmeasurementerrordirectly,proposingnewestimatorsthatpreservethestatisticale iciencyof MLreg while improving robustness. Last, we revisit empirical studies shown to exhibit nonstrategic measurement error, and demonstrate that our tools readily diagnose and mitigate the bias. We conclude this article with a number of practical recommendations for applied researchers. The proposed methods are implemented through an open-source so ware package.

Keywords: auxiliary information, indirect questioning, item count technique, misspecification test, sensitive survey questions, unmatched count technique

### Introduction

Measurement error poses a serious threat to the validity of survey research. This is especially true when studying sensitive questions, which present respondents with strong incentives to disguise the truth. Along with other methods such as the randomized response and endorsement experiments (e.g., Gingerich ; Bullock, Imai, and Shapiro ; Blair, Imai, and Zhou ), the list experiment (a.k.a. the item count technique and the unmatched count technique) is an indirect questioning method that, by veiling individual responses, seeks to mitigate potential social desirability and nonresponse biases (Miller ; Corstange ; Imai ; Blair and Imai

; Glynn ). While some studies have shown that list experiments can be e ective for reducingbias,awell-knownlimitationofthemethodisthattheextremevalueresponsesperfectly reveal the sensitive trait, meaning that some respondents are still incentivized to disguise the truth.BlairandImai( )showhowtoaddresssuch“floorandceilinge ects”withinaregression framework.

While the literature has since provided additional tools for alleviating strategic measurement error in list experiments (e.g., Blair, Imai, and Lyall ; Aronow et al. ), it has not yet addressed the consequences of nonstrategic measurement error, arising for example from “the usual problems of miscoding by administrators or enumerators as well as respondents

Authors’ note: All the proposed methods presented in this paper are implemented as part of the R package, list: Statistical Methods for the Item Count Technique and List Experiment, which is freely available for download at http://cran.r-project.org/package=list (Blair, Chou, and Imai ). The replication materials are available as Blair, Chou, and Imai ( ).

misunderstanding or rushing through surveys” (Ahlquist ). Like floor and ceiling e ects, these behaviors run against the assumptions of the standard maximum likelihood model (MLreg) for list experiments (Blair and Imai ), and can induce severe model misspecification biases, especially when the underlying trait is rare (Ahlquist ). Of course, all forms of nonstrategic measurementerrorarebestavoidedthroughcarefulinterviewertraining,pilotsurveys,andother best practices of survey research. Still, for some list experiments, a certain degree of careless responding and administrative errors may be unavoidable. We do not yet have the necessary tools for addressing nonstrategic measurement error in list experiments.

.

https://www.cambridge.org/core/terms

In this paper, we take up the challenge of providing new statistical methods for detecting such errorandalleviatingtheresultingmodelmisspecificationbias.Forconcreteness,weconsidertwo specific measurement error mechanisms, originally proposed in Ahlquist ( ). First, top-biased error occurs when a random subset of respondents chooses the maximal (ceiling) response value, regardless of their truthful response. Such error can greatly bias MLreg, which achieves statistical e iciency by modeling each level of the response variable. However, as we argue in Section  . , top-biased error is also unlikely to be common for truly sensitive questions (unless respondents are not paying attention or survey implementation is poor), since choosing the ceiling response amountstoaconfessionthatonepossessesthesupposedlysensitivetrait.Forthisreason,wealso consider a second, more plausible nonstrategic measurement error mechanism, uniform error, which occurs when a subset of respondents chooses their responses at random.

, subject to the Cambridge Core terms of use, available at

As a point of reference, we begin by showing that existing methods, in particular the standard di erence-in-means (DiM) and nonlinear least squares regression (NLSreg) estimator, are more robust than MLreg to these measurement error mechanisms. Leveraging this fact, we propose a simple statistical test that gauges the di erence between NLSreg and MLreg. Our test provides a principled approach to determining when the additional assumptions required by MLreg are justified. It can also be viewed as the formal and multivariate version of Ahlquist’s recommendation to compare the sensitive item prevalence estimated by DiM and MLreg, as NLSreg is a generalization of DiM.

09 Oct 2019 at 19:44:36

Next, we show how to detect and adjust for top-biased and uniform error in a regression modeling framework (Section ). Our new regression models occupy a valuable middle ground between existing approaches. On the one hand, they preserve the greater e iciency of MLreg, which can be invaluable when analyzing noisy methods such as the list experiment. On the other hand, they also contain the model without measurement error as a limiting case, thus improving robustnessandprovidinganotherstatisticaltest.Weproposeanadditionalmethodforimproving the robustness of the standard regression estimators using the auxiliary information strategy of Chou, Imai, and Rosenfeld ( ). All of our proposed methods are implemented via the opensource R package list (Blair, Chou, and Imai ).

, on

Harvard-Smithsonian Centerfor Astrophysics

We examine the performance of the proposed methodology through small scale simulation studies, which build on the simulations in Ahlquist ( ) (Section ). We show that our proposed test detects deviations from the modeling assumptions at a high rate. We also confirm the theoretical expectation that NLSreg is robust to nonstrategic measurement error and the forms of model misspecification contemplated in Ahlquist ( ). Turning to uniform response error, we find that MLreg performs reasonably well despite this misspecification. Nevertheless, we show thattherobustestimatorsproposedhereandinChou,Imai,andRosenfeld( )canimprovethe performance of list experiment regression in the presence of both types of measurement error.

.

https://www.cambridge.org/core

Finally,weapplytheproposedmethodologytotheempiricalstudypresentedinAhlquist( ) (Section ). When analyzed via MLreg, the study shows that unrealistically large proportions of Americans engage in voter fraud and/or were abducted by aliens. By contrast, a list experiment on texting while driving did not reveal such problems. The most straightforward analysis of these datayieldsanegativeestimate(apositiveestimatethatisstatisticallyindistinguishablefromzero)

for the proportion of those who engage in voter fraud (were abducted by aliens). We caution that multivariate analysis of such list experiments is bound to be unreliable, as a trait needs to exist for it to covary with respondent characteristics. Nevertheless, we show that our methods yield more sensible estimates of the prevalence of these traits than MLreg. In particular, our uniform error model yields estimates of voter fraud and alien abduction that are statistically indistinguishable from zero with the narrowest confidence intervals among the estimators we consider.

We further demonstrate that for the list experiment on texting while driving, which is not an extremely rare event, MLreg yields reasonable results that agree with those of the other methods. Given that all three list experiments were conducted in the same survey on the same respondents,andsowerelikelysubjecttothesameformsofnonstrategicmeasurementerror,this finding indicates that researchers should primarily be concerned with the rarity of the sensitive traits when deciding whether multivariate regression analyses are appropriate. Building on this observation, we conclude this article by o ering a set of practical recommendations for applied researchers conducting list experiments (Section ).

.

https://www.cambridge.org/core/terms

### The Proposed Methodology

, subject to the Cambridge Core terms of use, available at

In this section, we propose statistical methods for analyzing list experiments with measurement error. We begin by reviewing MLreg and NLSreg, introduced in Imai ( ) and extended in Blair and Imai ( ). We then propose a statistical test of model misspecification for detecting measurement error. Next, following Blair and Imai ( ), we show how to directly model measurement error mechanisms and apply this strategy to the top-biased and uniform error processes introduced in Ahlquist ( ). Finally, we adopt another modeling strategy developed in Chou, Imai, and Rosenfeld ( ) to further improve the robustness of multivariate regression models.

 .  Multivariate Regression Models: A Review

Suppose that we have a simple random sample of N respondents from a population. In standard list experiments, we have a total of J binary control questions and one binary sensitive question. LetTi betherandomizedtreatmentassignmentindicator.Thatis,Ti = 1indicatesthatrespondent i is assigned to the treatment group and is asked to report the total number of a irmative responses to the J + 1 items (J control items plus one sensitive item). In contrast,Ti = 0 implies that the respondent is assigned to the control group and is asked to report the total number of a irmative answers to J control questions. We use Xi to represent the set of K pretreatment covariates (including an intercept).

09 Oct 2019 at 19:44:36

, on

Harvard-Smithsonian Centerfor Astrophysics

Let Yi denote the observed response. If respondent i belongs to the treatment group, this variable can take any nonnegative integer less than or equal to J + 1, i.e.,Yi ∈ {0, 1, . . ., J + 1}. On the other hand, if the respondent is assigned to the control group, the maximal value is J, i.e., Yi ∈ {0, 1, . . ., J}. Furthermore, let Zi represent the latent binary variable indicating the a irmative answer to the sensitive question. If we use Yi∗ to represent the total number of a irmative answers to the J control questions, the observed response can be written as,

##### Yi = Ti Zi +Yi∗. ( )

.

https://www.cambridge.org/core

Intheearlyliteratureonlistexperiments,researchersestimatedtheproportionofrespondents with the a irmative answer to the sensitive item using DiM, but could not characterize the respondents most likely to have the a irmative response. To overcome this challenge, Imai ( ) considers the following multivariate regression model,

(Yi Ti, Xi) = Ti (Zi Xi) +  (Yi∗ Xi) ( )

where the randomization of treatment assignment guarantees the following statistical independence relationships:Ti ⊥⊥ Zi Xi andTi ⊥⊥ Yi∗ Xi.

Althoughthisformulationcanaccommodatevariousregressionmodels,onesimpleparametric model, considered in Imai ( ), is the following binomial logistic regression model,

Zi Xi indep∼ . Binom(1, g(Xi;β)) ( ) Yi∗ Xi indep∼ . Binom(J,f (Xi;γ)) ( )

.

https://www.cambridge.org/core/terms

where f (Xi;γ) = logit−1(X i γ) and g(Xi;β) = logit−1(X i β), implying the following regression functions, (Yi∗ Xi) = J · f (Xi;γ) and (Zi Xi) = g(Xi;β). Note that β and γ represent vectors of regression coe icients.

Imai ( ) proposes two ways to estimate this multivariate regression model: nonlinear least squares (NLSreg) and maximum likelihood (MLreg) estimation. NLSreg is obtained by minimizing the sum of squared residuals based on equation ( ).

N

, subject to the Cambridge Core terms of use, available at

(βˆNLS,γˆNLS) = argmin

{Yi −Ti · g(Xi;β) − f (Xi;γ)}2 ( )

(β,γ)

i=1

where βˆNLS and γˆNLS are the nonlinear least squares (NLS) estimates of the coe icients. NLSreg is consistent so long as the regression functions are correctly specified and does not require the distributions to be binomial. One can obtain more e icient estimates by relying on distributional assumptions.Inparticular,MLregisobtainedbymaximizingthefollowinglog-likelihoodfunction,

(βˆML,γˆML) = argmax

[log{1 − g(Xi;β)} + J · log{1 − f (Xi;γ)}]

(β,γ) i ∈J(1,0)

J

y logf (Xi;γ) + (J − y)log{1 − f (Xi;γ)}

+

09 Oct 2019 at 19:44:36

y=0 i ∈J(0,y)

{logg(Xi;β) + J logf (Xi;γ)}

+

i ∈J(1,J+1)

J

J y − 1

f (Xi;γ)y−1{1 − f (Xi;γ)}J−y+1

log g(Xi;β)

+

, on

y=1 i ∈J(1,y)

Harvard-Smithsonian Centerfor Astrophysics

J y

f (Xi;γ)y{1 − f (Xi;γ)}J−y ( )

+{1 − g(Xi;β)}

where βˆML and γˆML are the maximum likelihood (ML) estimates of the coe icients and J(t, y) represents the set of respondents who haveTi = t andYi = y.

The choice between NLSreg and MLreg involves a fundamental tradeo  between bias and variance. MLreg is more e icient than NLSreg because the former makes additional distributional assumptions. In particular, MLreg models each cell of the observed response, including theYi = J+1andYi = 0cellsinthetreatmentgroup,whichcangreatlya ectparameterestimates(Ahlquist

). In contrast, NLSreg only makes an assumption about the conditional mean functions and hence is more robust to measurement errors in specific cells. In line with these theoretical expectations, simulations in Ahlquist ( ) report that DiM, which is a special case of NLSreg without covariates, is more robust for estimating the proportion of the sensitive trait than MLreg.

.

https://www.cambridge.org/core

Two identification assumptions are required for DiM, NLSreg, and MLreg. First, respondents in the treatment group are assumed not to lie about the sensitive item, i.e., no liars. Any other behavior implies misreporting, and any estimator based on mismeasured responses is likely to be biased. The second assumption is that respondents’ answers to the control items are not a ected

by the treatment, i.e., no design e ect. Because list experiments rely upon the comparison of responsesbetweenthetreatmentandcontrolgroups,responsestothecontrolitemsmustremain identical in expectation between the two groups. The violation of this assumption also leads to mismeasured responses, yielding biased estimates. We emphasize that DiM is a special case of NLSreg and is not exempt from these assumptions. In Appendix A, we prove that DiM is biased under top-biased and uniform error. The bias is large when the prevalence of the sensitive trait is small. NLSreg adds an assumption about the correctly specified regression function and MLreg imposes an additional distributional assumption.

.

https://www.cambridge.org/core/terms

The main di iculty of multivariate regression analysis for list experiments stems from the fact that the response to the sensitive item is not observed except for the respondents in the treatment group who choose the maximal or minimal response. Regression analysis under this circumstance is more challenging than when the outcome is directly observed. If the sensitive trait of interest is a rare event, then MLreg is likely to su er from bias. Such bias is known to exist even whentheoutcomevariable is observed (Kingand Zeng ), and islikelytobeamplifiedfor list experiments. In addition, dealing with measurement error will also be more di icult when the outcome variable is not directly observed. Below, we consider several methodological strategies for addressing this issue.

, subject to the Cambridge Core terms of use, available at

 .  Strategic and Nonstrategic Measurement Errors

Researchers most o en use indirect questioning techniques to study sensitive topics, which present respondents with strong incentives to disguise the truth. For this reason, much of the existing literature on list experiments has been rightly concerned with mitigating strategic measurement error, particularly floor and ceiling e ects (e.g., Blair and Imai ; Glynn ). These errors arise because the list experiment fails to mask the sensitive trait for respondents whose truthful response under treatment occupies the floor or ceiling cells.

Although the literature has provided many tools for ameliorating such bias, much less attention has been paid to nonstrategic measurement error, arising for example from poor survey implementation or respondent inattention. Because these behaviors run against the assumptions of the estimators described in Section  . , it is no surprise that they can induce similar forms of bias. Illustrating this point, Ahlquist ( ) examines a specific nonstrategic error mechanism—called top-biased error, where a random fraction of respondents provide the maximal response value regardless of their truthful answer to the sensitive question—and demonstrates that MLreg can be severely biased under this error mechanism.

09 Oct 2019 at 19:44:36

, on

Harvard-Smithsonian Centerfor Astrophysics

Although we provide the tools to diagnose and correct this and other nonstrategic measurement error mechanisms below, we are skeptical that top-biased error is common in practice, at least for truly sensitive questions. The reason is that under the treatment condition, givingthemaximalvaluerevealsthattherespondentanswersthesensitivequestiona irmatively. This implies, for example, that respondents are willing to admit engaging in such sensitive behaviors as drug use and tax evasion or having socially undesirable attitudes such as gender and racial prejudice. This scenario is unlikely so long as the behavior or attitudes researchers are trying to measure are actually sensitive.

In our experience, when answering truly sensitive questions, respondents typically avoid reporting the extreme values (rather than gravitating toward them as assumed under the topbiased error mechanism). As an example of this phenomenon, we present a list experiment conducted by Lyall, Blair, and Imai ( ) in the violent heart of Taliban-controlled Afghanistan, which was designed for estimating the level of support for the Taliban. The control group was given the following script (J = 3):

.

https://www.cambridge.org/core

I’m going to read you a list with the names of different groups and individuals on it. After I read the entire list, I’d like you to tell me how many of these groups and individuals you broadly support, meaning that you generally agree with the goals and policies of the group or individual. Please don’t tell me which ones you generally agree with; only tell me how many groups or individuals you broadly support. Karzai Government; National Solidarity Program; Local Farmers

.

https://www.cambridge.org/core/terms

For the treatment group, the sensitive actor, i.e., the Taliban, is added.

##### Karzai Government; National Solidarity Program; Local Farmers; Taliban

Table presentsdescriptiveinformation,whichshowsclearevidenceoffloorandceilinge ects. Indeed, no respondent gave an answer of   or  . By avoiding the extreme responses of   and  , respondents in the treatment group are able to remain ambiguous as to whether they support or oppose the Taliban. This strategic measurement error may have arisen in part because of the public nature of interview. As explained in Lyall, Blair, and Imai ( ), interviewers are required to ask survey questions to respondents in public while village elders watch and listen. Under this circumstance, it is no surprise that respondents try to conceal their truthful answers. Because of this sensitivity, the authors of the original study used endorsement experiments (Bullock, Imai, and Shapiro ), which represent a more indirect questioning technique, in order to measure the level of support for the Taliban. On the other hand, Blair, Imai, and Lyall ( ) find that in the same survey the list experiment works well for measuring the level of support for the coalition International Security Assistance Force, which is a less sensitive actor to admit support or lack thereof for than is the Taliban.

, subject to the Cambridge Core terms of use, available at

 .  Detecting Measurement Error

Althoughresearchersareunlikelytoknowthemagnitudeofmeasurementerror,whetherstrategic or not, we can sometimes detect measurement error from data. In addition to the tests developed by Blair and Imai ( ) and Aronow et al. ( ), we extend and formalize the recommendation by Ahlquist ( ) to compare the results of multiple models to assess their robustness to measurement error. We focus on comparisons between MLreg and NLSreg, in order to focus on comparisons of the quantity of interest most commonly used by applied researchers.

09 Oct 2019 at 19:44:36

, on

We employ a general specification test due to Hausman ( ) as a formal means of comparison between MLreg and NLSreg, both of which are designed to examine the multivariate relationships between the sensitive trait and respondents’ characteristics. The idea is that if the regression modeling assumptions are correct, then NLSreg and MLreg should yield statistically indistinguishableresults.Iftheirdi erencesaresignificant,werejectthenullhypothesisofcorrect specification. Note that model misspecification can arise for various reasons, with measurement error being one possibility. Furthermore, the test assumes the linear regression specification shared across NLSreg and MLreg. Then the test statistic and its asymptotic distribution are given by,

Harvard-Smithsonian Centerfor Astrophysics

.

https://www.cambridge.org/core

(θˆML − θˆNLS) ( (θˆNLS) − (θˆML))−1(θˆML − θˆNLS) approx∼ . χdim(2 β)+dim(γ) ( )

whereθˆNLS = (βˆNLS,γˆNLS)andθˆML = (βˆML,γˆML)aretheNLSandMLestimatorsand (θˆNLS)and (θˆML) aretheirestimatedasymptoticvariances.Weviewthistestasalogicalextensionandformalization of the recommendation in Ahlquist ( ) to compare the results from DiM and MLreg.

Table  . An Example of Floor and Ceiling E ects from the List Experiment in Afghanistan Reported in Lyall, Blair, and Imai ( ). No respondent in the treatment group gave an answer of   or  , suggesting that the respondents were avoiding revealing whether they support the Taliban.

Control group Treatment group Response Counts Percentage Counts Percentage

.

https://www.cambridge.org/core/terms

 .  Modeling Measurement Error Mechanisms

One advantage of the multivariate regression framework proposed in Imai ( ) is its ability to directly model measurement error mechanisms, an approach which has demonstrated its value in a variety of contexts (see e.g., Carroll et al. ), including list experiments (Blair and Imai

, subject to the Cambridge Core terms of use, available at

; Chou ). Measurement error models strike a valuable middle ground between MLreg and NLSreg. First, these models include the model without measurement error as their limiting case, requiring fewer and weaker assumptions than standard models. As a result, we can apply the specification test as shown for NLSreg and MLreg above. Second, these models can be used to check the robustness of empirical results to measurement error. Third, researchers can use these models to test the mechanisms of survey misreporting in order to understand when list experiments do and do not work.

Although we believe that top-biased error is unlikely to obtain in applied settings, we show how to model this error process as an illustration of how our modeling framework can flexibly incorporatevariousmeasurementerrormechanisms.Wethenshowhowtomodeluniformerrorin which “a respondent’s truthful response is replaced by a random uniform draw from the possible answers available to her, which in turn depends on her treatment status” (Ahlquist , p.  ). We think that this uniform response error process is more realistic and hence the proposed uniform error model will be useful for applied researchers. As shown in Appendix A, DiM is biased under these error processes.

09 Oct 2019 at 19:44:36

Top-biased error. Under top-biased error, for the NLS estimation, equation ( ) becomes,

, on

Harvard-Smithsonian Centerfor Astrophysics

(Yi Ti, Xi) = pJ +Ti{p + (1 − p) (Zi Xi)} + (1 − p) (Yi∗ Xi) ( )

where p is the additional parameter representing the population proportion of respondents who give the maximal value as their answer. When p = 0 the model reduces to the standard model given in equation ( ). The NLS estimator is obtained by minimizing the sum of squared error,

N

[Yi − pJ −Ti{p + (1 − p) (Zi Xi)} − (1 − p) (Yi∗ Xi)]2. ( )

(βˆNLS,γˆNLS) = argmin

(β,γ,p)

i=1

.

https://www.cambridge.org/core

We can also model top-biased error using the following likelihood function,

[g(Xi;β)f (Xi;γ)J + p{1 − g(Xi;β)f (Xi;γ)J}]

[f (Xi;γ)J + p{1 − f (Xi;γ)J}]

i ∈J(1,J+1)

i ∈J(0,J)

J−1

J y

f (Xi;γ)y{1 − f (Xi;γ)}J−y

(1 − p){1 − g(Xi;β)}{1 − f (Xi;γ)}J

(1 − p)

i ∈J(1,0)

y=0 i ∈J(0,y)

J

J y − 1

f (Xi;γ)y−1{1 − f (Xi;γ)}J−y+1

(1 − p) g(Xi;β)

y=1 i ∈J(1,y)

J y

f (Xi;γ)y{1 − f (Xi;γ)}J−y . (  )

+{1 − g(Xi;β)}

Again,whenp = 0,thislikelihoodfunctionreducestothelikelihoodfunctionoftheoriginalmodel, whichisgivenonthelogarithmicscaleinequation( ).Whilethislikelihoodfunctionistoocomplex tooptimize,wecanusetheexpectation–maximization(EM)algorithm(Dempster,Laird,andRubin

.

https://www.cambridge.org/core/terms

) to maximize it. The details of this algorithm are given in Appendix B. .

Uniform error. Under the uniform error mechanism, we modify the regression model given in equation ( ) to the following,

p0(1 −Ti)J 2

p1(J + 1) 2

(Yi Ti, Xi) =

+ (1 − p1) (Zi Xi)

+Ti

+{(1 −Ti)(1 − p0) +Ti(1 − p1)} (Yi∗ Xi) (  )

, subject to the Cambridge Core terms of use, available at

where pt = Pr(Si Ti = t) represents the proportion of misreporting individuals under the treatment condition Ti = t. Again, when p0 = p1 = 0, this model reduces to the original model without measurement error. As before, we can obtain the NLS estimator by minimizing the sum of squared error. We can also formulate the ML estimator using the following likelihood function,

p1 J + 2

(1 − p1)g(Xi;β)f (Xi;γ)J +

i ∈J(1,J+1)

p1 J + 2

(1 − p1){1 − g(Xi;β)}{1 − f (Xi;γ)}J +

i ∈J(1,0)

J

- y=0 i ∈J(0,y)

(1 − p0)

J y

f (Xi;γ)y {1 − f (Xi;γ)}J−y +

p0 J + 1

J

- y=1 i ∈J(1,y)


09 Oct 2019 at 19:44:36

J y − 1

f (Xi;γ)y−1 {1 − f (Xi;γ)}J−y+1

(1 − p1) g(Xi;β)

J y

p1 J + 2

f (Xi;γ)y {1 − f (Xi;γ)}J−y +

+{1 − g(Xi;β)}

. (  )

, on

Harvard-Smithsonian Centerfor Astrophysics

As shown in Appendix B. , the EM algorithm can be used to obtain the ML estimator.

 .  Robust Multivariate Regression Models

As another approach, we also show how to conduct multivariate regression analysis while ensuring that the estimated proportion of the sensitive trait is close to DiM. To do this, we follow Chou, Imai, and Rosenfeld ( ), who show how to incorporate available auxiliary information such as the aggregate prevalence of sensitive traits when fitting regression models. The authors find that supplying aggregate truths significantly improves the accuracy of list experiment regression models. Adopting this strategy, we fit the multivariate regression models such that they give an overall prediction of sensitive trait prevalence consistent with DiM. To the extent that DiM rests on weaker assumptions, this modeling strategy may improve the robustness of the multivariate regression models.

.

https://www.cambridge.org/core

Specifically, we use the following additional moment condition,

   

 {g(Xi;β)} =      

N i=1(1 −Ti)Yi

N i=1TiYi

. (  )

−

N i=1(1 −Ti)

N i=1Ti

.

https://www.cambridge.org/core/terms

, subject to the Cambridge Core terms of use, available at

09 Oct 2019 at 19:44:36

, on

Harvard-Smithsonian Centerfor Astrophysics

.

https://www.cambridge.org/core

Downloaded from

For the NLS estimation, we combine this moment condition with the following first order conditions from the two-step NLS estimation.

Ti{Yi − f (Xi;γ) − g(Xi;β)}g (Xi;β) = 0 (  ) (1 −Ti){Yi − f (Xi;γ)}f (Xi;γ) = 0 (  )

where f (Xi;γ) and g (Xi;β) are the gradient vectors with respect to γ and β, respectively. Altogether, the moments form a generalized method of moments (GMM) estimator. In fact, we can use the same exact setup Chou, Imai, and Rosenfeld ( ) and use their code in the list package inRtoobtaintheNLSestimatorwiththisadditionalconstraint,althoughthestandarderrorsmust be adjusted as the auxiliary constraint does not provide additional information.

We can also incorporate the constraint in equation ( ) in the ML framework. To do this, we combine the score conditions obtained from the log-likelihood function with this additional momentcondition.Then,theGMMestimatorcanbeconstructedusingallthemomentconditions. The details of this approach are given in Appendix B. .

### Simulation Studies

How do the methods we introduce above fare in estimating common quantities of interest for the list experiment in the presence of measurement error? In this section, we build on the simulation study presented in Ahlquist ( ) and examine the performance of the DiM and MLreg but also the NLSreg introduced in Imai ( ) and the robust models introduced in Section . We examine the performance for two common estimands: the sensitive item proportion, which on theoretical grounds we recommend be primarily estimated using the DiM; and the relationship between the sensitive item and covariates. For comparability, we rely on the simulation settings in Ahlquist ( ) and examine whether the theoretical properties of the estimators hold in the presence of top-biased error and uniform error.

Ahlquist ( ) finds that MLreg is more sensitive to top-biased error than DiM. The paper also reports that the degree of sensitivity increases when the prevalence of the sensitive trait is low and the control items are negatively correlated with each other. Below, we show that our statistical test, developed in Section  . , can detect the misspecified data-generating process used in Ahlquist ( ). We show that NLSreg is robust to these types of model misspecification. Although we confirm that MLreg is sensitive to top-biased error, we find that it is more robust to uniform error. Finally, we find that the new ML estimators proposed above perform reasonably well in the presence of response errors, especially when the sensitive trait is su iciently common.

 .  Simulation Settings

We begin by replicating the “designed list” simulation scenario, which Ahlquist ( ) found to be most problematic for MLreg. In addition to the introduction of top-biased error, this simulation scenario violates the assumptions of MLreg in two ways. First, Ahlquist follows the advice of Glynn ( ) and generates a negative correlation among the control items. By contrast, MLreg assumes conditionalindependenceofthecontrolitems.Second,controlitemsaregeneratedwithdi erent marginal probabilities, which is also inconsistent with the binomial distribution.

Thedata-generatingprocessfortheseproblematic“designed”listsisasfollows.Forthecontrol

outcomeYi∗, the marginal probabilities are fixed for each control item. For the simulations with J = 3 control items, the probabilities of latent binary responses are specified to be (0.5, 0.5, 0.15),

Wedonotstudythe“Blair–Imailist”simulationscenarioinAhlquist( ),whichdoesnotfollowthebinomialdistribution assumed for MLreg of Blair and Imai ( ), making it impossible to isolate the e ects of measurement error. Blair and Imai ( ) show how to model this data-generating process using the Poisson binomial distribution. Another possibility is to model the joint distribution of control items by using the information from another survey, in which each item is asked separately.

whereas in the simulations with J = 4, the study uses (0.5, 0.5, 0.15, 0.85). The rmvbin() function in the R package bindata is used to generate the latent responses to the control items such that thecorrelationbetweenthefirsttwoitemsisnegative . .Togeneratethesensitivetrait, Zi,firsta single covariate, Xi, is sampled independently from the uniform distribution for each observation i = 1, 2, . . ., N. Together with an intercept, we form the model matrix Xi = (1, Xi). The sensitive trait is then drawn according to the logistic regression given in equation ( ). The coe icients are set to β = (0, −4) corresponding to the prevalence of the sensitive trait approximately equal to 0.12. Finally, we assign the half of the sample to the treatment group (Ti = 1) and the other half to the control group (Ti = 0). The outcome variable then is generated according to equation ( ). We conduct  ,    simulations with these parameters.

.

https://www.cambridge.org/core/terms

To introduce top-biased error, Ahlquist ( ) uses complete randomization to select  % of the sampleandchangestheoutcomevariableYi to J +1(J)ifobservationisassignedtothetreatment (control) group, independently of the values of Xi,Yi∗, and Zi. To generate uniform error,  % of the observations are similarly sampled, but are assigned their outcome variable with uniform probability to one of the J + 2 (J + 1) possible values, depending on their treatment status. We follow these procedures in our simulations.

, subject to the Cambridge Core terms of use, available at

 .  Detecting Model Misspecification

Giventhediscrepanciesbetweenthisdata-generatingprocessandtheprocessassumedbyMLreg, MLreg is shown to be severely biased by these procedures (Ahlquist ). However, as explained in Section  . , NLSreg should be more robust than MLreg, though it is less e icient. This biasvariancetradeo arisesbecauseNLSregdoesnotassumethebinomialdistributionforthecontrol items. Under the assumptions of NLSreg, the control items can be arbitrarily correlated and have di erent marginal probabilities (although a specific functional form—here, the logistic functionisassumedfortheconditionalexpectation).ThisimpliesthatNLSregshouldonlybesubjecttothe potential bias from response error.

This theoretical expectation suggests that the Hausman test proposed in Section  .  may be able to detect departures from the modeling assumptions. We find that this is indeed the case. Table shows that our test diagnoses the inconsistency of MLreg in the presence of such severe model misspecification. The table presents the rejection rate for our simulations at di erent combinations of J and N with a p-value of  .  as the threshold. As the “p-value” columns show, we find su iciently large (and positive) test statistics to reject the null hypothesis of no misspecification in a large proportion of trials, especially when there is no response error. The finding is consistent with substantial model misspecification, in excess of response error, introduced by the designed list procedure in Ahlquist ( ). Interestingly, the top-biased error appears to mask this misspecification.

09 Oct 2019 at 19:44:36

, on

Harvard-Smithsonian Centerfor Astrophysics

Importantly, we discovered that in all cases a large proportion of the trials yielded a negative valueoftheteststatistic,whichcorrespondstoextremelypoorfitof MLregrelativetoNLSreg.Such values are only consistent with model misspecification so long as the test is su iciently powered (Schreiber ). While the test statistic can by chance take a negative value in a finite sample, in our simulations such statistics are strikingly prevalent. As shown in the “p-value & negative” columnsofthetable,byusinganegativeorlargepositiveteststatisticasthecriterionforrejection, we obtain a much more powerful test for misspecification even in the case of top-biased error. Although this test may be conservative, leading to overrejection of the null hypothesis, the fact that these rejection rates are large even when the sample size is moderate suggests that the test is well powered in this simulation study.

.

https://www.cambridge.org/core

In sum, the proposed model misspecification test readily diagnoses the designed list misspecification studied in Ahlquist ( ). Although the test may not work in all settings, we find here that it detects the significant problems in the designed lists simulations at a high rate.

.

https://www.cambridge.org/core/terms

, subject to the Cambridge Core terms of use, available at

09 Oct 2019 at 19:44:36

, on

Harvard-Smithsonian Centerfor Astrophysics

.

https://www.cambridge.org/core

Downloaded from

Table  . Results of the Model Misspecification Test for the Designed List Simulations. The proportions rejecting the null hypothesis of no model misspecification are shown. The “p-value” column is based on the standard Hausman test with a p-value of  .  as the threshold, while the “p-value & negative” column is based onthecombinedrejectioncriteriawherewerejectthenullhypothesisifthep-valueislessthan . orthetest statistic takes a negative value.

No response error Top-biased error Uniform error

Number of Sample p-value & p-value & p-value & control items size p-value negative p-value negative p-value negative

 .    .    .    .    .    .    .    .    .    .    .    .    .    .    .    .    .    .  

##### J = 3

 .    .    .    .    .    .    .    .    .    .    .    .    .    .    .    .    .    .  

##### J = 4

 .  Robustness of the Nonlinear Least Squares Regression Estimator

Our second main finding is that NLSreg is robust to these misspecifications. This fortifies our previous result that the model misspecification test, which is based on the divergence between NLSreg and MLreg, is e ective for diagnosing model misspecification. To illustrate the robustness of NLSreg, in Figure , we present the bias, root-mean-squared error (RMSE), and the coverage of   % confidence intervals of our estimates of the population prevalence of the sensitive trait. We also present results for MLreg, filtered using the p-value plus negative value criterion for rejection describedabove. Last,giventhegoalsofmultivariateregression,wealsocomputethesestatistics for the estimated coe icients.

Figure shows the results for J = 3 control items for top-biased error (le  three columns) and uniform error (right three columns). Given space limitations, the analogous figure for J = 4 control items is shown in Figure   in the Supplementary Appendix. We include the two estimators considered in Ahlquist ( ): DiM and MLreg (solid square with solid line), as well as the NLSreg estimator proposed in Imai ( ) (solid triangle with dashed line). Our main finding here is that NLSreg is robust to all of these model misspecifications, doing as well as DiM. This is consistent with our prior expectation: DiM is a special case of NLSreg.

Although filtering based on the model misspecification test addresses the overestimation of thesensitivetraitundertop-biasederrorobserved inAhlquist ( ),wenotethatMLregdoesnot performwellfortheestimationofthecoe icients,nordoesitimproveinferencefortheprevalence of the sensitive trait under uniform error. However, as Table showed, these results are based on the small fraction of trials that did not result in a negative or large positive test statistic. In such trials, the NLS estimates were also inaccurate due to sampling error. This suggests that, while our proposed statistical test will o en be able to detect misspecification in practice, in the instances where it does not, NLSreg (and, by extension, DiM) will also be biased.

The results confirm our theoretical expectation that NLSreg is robust to various types of misspecification. As a final point, we note that our simulation results, based on the grossly misspecified data-generating process described above, do not necessarily imply that MLreg will perform badly for designed lists. The simulation settings we adapted from Ahlquist ( ) are not realistic. They imply, for example, that the individual covariates have no predictive power for

For the purpose of presentation, we adopt the Bayesian approach suggested by Blair and Imai ( ), which is based on weakly informative priors for logistic regression. Although the use of such prior distribution typically yields estimates that are similar to those of MLreg, it acts as regularization and avoids complete separation of covariates in a small number of simulations when the model is misspecified. We follow Gelman et al. ( ) and use their default recommendation of a Cauchy prior with center parameter set to 0 and scale set to  .  (  ) for the coe icients (intercept). Note that fewer than  % of simulations are a ected by separation issues.

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |


.

https://www.cambridge.org/core/terms

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


, subject to the Cambridge Core terms of use, available at

Figure  . Robustness of the Nonlinear Least Squares Regression Estimator in the Presence of Several Model Misspecifications Considered in Ahlquist ( ). We consider the three estimators of the prevalence of the sensitive trait: the DiM estimator (open circle with dotted line), the ML regression estimator (solid square withsolidline;filteredbythemodelmisspecificationtestusingthecombinedcriteria),andtheNLSestimator (solid triangle with dashed line). The result shows that the NLS regression estimator is as robust as the DiM estimator.

responses to the control items. Furthermore, our model misspecification test is able to detect the distributional misspecification in these simulations. Thus, in practice, such a misspecification will o en be apparent from the divergence of the NLSreg and MLreg results.

 .  Addressing Response Error

The simulation settings adopted above include several violations of the modeling assumptions, including correlation between control items, varying control item propensities, model misspecification, and measurement error. As such, it is di icult to disentangle which model misspecifications, or combination of them, are a ecting the performance of di erent methods. In this section, we focus on assessing the impacts of top-biased and uniform error processes and examine how the multivariate models proposed in Section can address them. To be sure, applied researchers will rarely know which (if any) of these mechanisms characterize their data. Nevertheless, we show here that these methods can eliminate these errors when they arise, and illustrate in Section how they can be used to assess the robustness of empirical results.

09 Oct 2019 at 19:44:36

, on

Harvard-Smithsonian Centerfor Astrophysics

To isolate the e ects of measurement errors, we develop a data-generating process that assumes no other model misspecification. First, we draw the latent response to the sensitive item Zi and the control items Yi∗ according to the model defined in equations ( ) and ( ). Following Ahlquist ( ), we set the true values of the coe icients for the control items to γ to (0, 1), corresponding to a conditional mean of observed response about J × 0.62, whereas the coe icients for the sensitive item are set to β = (0, −4), generating a low propensity of approximately 0.12. In the Supplementary Appendix, we present a high propensity scenario of about  .  . Last, we introduce each response error using the same procedure described earlier. We conduct  ,    simulations with these parameters.

.

https://www.cambridge.org/core

Figure presentsthefindingsforJ = 3,whereasFigure oftheSupplementaryAppendixshows the results for J = 4. In the le -hand columns, we show the top-biased error simulation with the standard ML estimator (solid square with solid line), the constrained ML estimator (solid triangle with dot-dash line), the top-biased ML model (open circle with dash line), and the uniform ML

| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |


.

https://www.cambridge.org/core/terms

| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |


| | |
|---|---|
| | |
| | |
| | |
| | |
| | |


, subject to the Cambridge Core terms of use, available at

Figure  . Robustness of the Constrained and Measurement Error Maximum Likelihood Estimators in the Presence of Response Errors when the Propensity of Sensitive Trait is Low. We consider four estimators of the prevalence of the sensitive trait and slope and intercept regression coe icients: the standard ML estimator (solid square with solid line), the constrained ML estimator (solid triangle with dot-dash line), the ML estimators adjusting for top-biased response error (open circle with dashed lines) and uniform response errors (open diamond with dot-long-dash line). The result shows that both the constrained ML estimator and the models adjusting for response error are an improvement over the performance of the ML estimator.

model (open diamond with dot-long-dash line) introduced in Section . The right-hand columns present the uniform error simulation results. As before, we show the bias, RMSE, and coverage of   % confidence intervals.

As the upper le -hand corner plot shows, we replicate the main finding in Ahlquist ( ) that a small amount of top-biased error is enough to significantly bias the standard ML estimator. Looking at the regression coe icients, we find that this positive bias follows from the bias in the estimated slope. Our proposed methods appear to address this issue e ectively. The constrained estimator slashes the bias of the overall prevalence by almost   %. This is unsurprising, as it constrainstheregression-basedpredictiontotheDiMestimate.However,becausetheconstrained ML does not model the error mechanism directly, it does not improve the bias of the estimated regression coe icients. Indeed, the dashed lines show, the constrained model reduces the bias by decreasing the intercept rather than the slope, which does not help in this particular simulation setting where the bias for the intercept is small to begin with. As a result, the coverage of the confidence interval for the slope is only slightly improved.

09 Oct 2019 at 19:44:36

, on

Harvard-Smithsonian Centerfor Astrophysics

As expected, the top-biased error model most e ectively addresses this measurement error mechanism, eliminating the bias of the three quantities of interest almost entirely. Likewise, coverage is at the nominal rate for all three quantities of interest. We find that the uniform error model, which models a di erent error process to the one assumed, nevertheless is no worse than the standard ML model. Indeed, it exhibits less bias, better coverage, and lower RMSE than MLreg. In both cases, there is a small finite-sample bias that reduces as sample size increases.

.

https://www.cambridge.org/core

The right-hand columns of Figure examine the performance of the same four estimators under uniform error. We find several interesting results. Most importantly, we find that MLreg is significantly less biased under this measurement error mechanism than under the top-biased error process. Given the greater plausibility of uniform error relative to top-biased error, this finding suggests that MLreg may be more robust to nonstrategic measurement error than the simulations of Ahlquist ( ) suggest.

We find that the uniform error model leads to some underestimation of the sensitive trait prevalence. While no estimator is unbiased for estimating the intercept, the uniform error model yields a large finite-sample bias for the estimation of the slope coe icient. However, these biases are small relative to the standard error as shown by the proper coverage of the corresponding confidence intervals, and they go to zero as the sample size increases. In contrast, the constrained ML estimator appears to perform well with small bias and RMSE as well as proper coverage of confidence intervals. We also note that the top-biased error model, which assumes a di erent error process than the simulation DGP, performs well under uniform error, exhibiting low bias, RMSE, and nominal coverage.

.

https://www.cambridge.org/core/terms

### Empirical Applications

In this section, we illustrate our methods in application to a set of list experiments, which Ahlquist ( ) found to su er from measurement error. These experiments were originally conducted by Ahlquist,Mayer,andJackman( )forthepurposeofmeasuringvoterimpersonationinthe     US election—a phenomenon that many scholars of American politics consider to be exceedingly rare (see, e.g., Sobel , and references therein). While the DiM estimate from the voter fraud experiment, negative  . %, confirms this expectation, Ahlquist ( ) finds that the multivariate regression model significantly overestimates voter fraud. Ahlquist, Mayer, and Jackman ( ) also conducted two additional list experiments, one on alien abduction and the other on texting while driving. Ahlquist ( ) finds that MLreg similarly overestimates the prevalence of alien abduction, while no such problem is found for the texting-while-driving list.

, subject to the Cambridge Core terms of use, available at

Below, we reanalyze these list experiments using the proposed methodology. As a preliminary point, we note that a simple descriptive analysis of these list experiments demonstrates the impracticality of multivariate regression models for the voter fraud and alien abduction lists. Our analysis—as basic as taking the DiM—confirms that these are extremely rare or nonexistent events, and consequently there is no association that exists to be studied. Nevertheless, our new methodsyieldmuchmoresensibleestimatesoftheprevalenceofvoterfraudandalienabduction. In particular, when accounting for uniform error, the estimated prevalence of these events is precisely zero. Finally, we analyze the texting-while-driving list, which measures a much more common event, and show that the proposed methods as well as the standard ML estimator yield reasonable results, indicating that rarity, rather than nonstrategic measurement error, was chiefly responsible for the problems with these lists.

09 Oct 2019 at 19:44:36

, on

Harvard-Smithsonian Centerfor Astrophysics

 .  Extremely Rare Sensitive Traits and Multivariate Regression Analysis

As a general rule of thumb, we caution against the use of multivariate regression models when studying extremely rare or even nonexistent sensitive traits. The reason is simple. The goal of multivariate regression analysis is to measure the association between sensitive traits and respondent characteristics. If almost all respondents do not possess such traits, then multivariate regression analysis is likely to be unreliable because no association exists in the first place (and anyexistingassociationislikelytobeduetonoise).Inlinewiththeseexpectations,Ahlquist( ) findstheMLregressionestimatortobemisleadingforthelistexperimentsonvoterfraudandalien abduction but unproblematic for the list experiment on texting while driving, the more common phenomenon by far.

.

https://www.cambridge.org/core

Indeed, we find that the voter fraud and alien abduction list experiments elicit extremely small proportions of the a irmative answer. As discussed in Section  .  and recommended in Blair and Imai ( ), Table presents the estimated proportion of each respondent J(y, z) type defined by two latent variables, i.e., the total number of a irmative answers to the control itemsYi∗ = y and the answer to the sensitive item Zi = z. We also present the DiM for each list experiment. The list experiment on voter fraud is most problematic, yielding an overall negative estimate and

Table . EstimatedProportionofRespondentTypesbytheNumberofA irmativeAnswerstotheControland Sensitive Items. The table shows the estimated proportion of respondent type J(y, z), where y ∈ {0, . . ., J} denotes the number of a irmative answers to the control items and z ∈ {0, 1} denotes whether respondents would answer yes to the sensitive item. In the last row, we also present the DiM estimator for the estimated proportion of those who would a irmatively answer the sensitive item. The voter fraud and alien abduction list experiments have an extremely small proportion of those who would answer yes to the sensitive item, and for voter fraud some proportions are estimated negative, suggesting the problem of list experiment.

Texting while Voter fraud Alien abduction driving

.

https://www.cambridge.org/core/terms

est. s.e. est. s.e. est. s.e.

J( ,  ) − .     .     .     .     .     .    J( ,  ) − .     .     .     .     .     .    J( ,  ) − .     .     .     .     .     .    J( ,  )  .     .     .     .     .     .    J( ,  )  .     .     .     .     .     .    J( ,  )  .     .     .     .     .     .    J( ,  )  .     .     .     .     .     .    J( ,  )  .     .     .     .     .     .    J( ,  )  .     .     .     .     .     .    J( ,  )  .     .     .     .     .     .    Di .-in-means − .     .     .     .     .     .   

, subject to the Cambridge Core terms of use, available at

exhibiting three negative estimates for respondent types who would answer the sensitive item a irmatively.

Althoughthesenegativeestimatesarenotstatisticallysignificant,thissimplediagnosticshows that the list experiment on voter fraud su ers from either the violation of assumptions or an exceedingly small number of respondents with the sensitive trait or both. The descriptive informationclearlysuggeststhatmultivariateregressionanalysiscannotbeinformativeforthelist experiments on voter fraud and alien abduction. Virtually no respondent would truthfully answer yes to these questions; thus, there is no association to be studied.

09 Oct 2019 at 19:44:36

The application of the multivariate ML regression model to the alien abduction and voter fraud lists compounds the weakness of indirect questioning methods, which are ill-suited to studying extremely rare sensitive traits. Although indirect questioning methods seek to reduce bias from social desirability and nonresponse by partially protecting the privacy of respondents, they are muchlesse icientthandirectquestioning.Asaconsequence,theestimateswilllackthestatistical precisionrequiredformeasurementandanalysisofextremelyraretraits.Indirectmethodsfurther amplify the finite-sample bias associated with rare events (King and Zeng ).

, on

Harvard-Smithsonian Centerfor Astrophysics

Given these tradeo s, we recommend that list experiments be used only when studying truly sensitive topics. The increased cognitive burden on respondents and the loss of statistical e iciency are too great for this survey methodology to be helpful for nonsensitive traits. Among the three list experiments, the one on alien abduction provides the least insight into the e icacy of list experiments. In fact, such questions may themselves increase measurement error if they prompt respondents to stop taking the survey seriously. Better designed validation studies are needed to evaluate the e ectiveness of list experiments and their statistical methods (see e.g., Rosenfeld, Imai, and Shapiro ).

.

https://www.cambridge.org/core

Despite our reservations about the application of the multivariate regression models to two of the three list experiments, we now examine whether the methods proposed in Section can detect and adjust for measurement error by applying them to these list experiments.

| | | | |
|---|---|---|---|
| | | | |


.

https://www.cambridge.org/core/terms

Figure  . The Estimated Prevalence of Voter Fraud, Alien Abduction, and Texting while Driving. Along with the DiM estimator, we present the estimates based on various multivariate regression analyses including the maximum likelihood and nonlinear least squares regression estimators and estimates are much more stable. The results based on the two measurement error models, i.e., top-biased and uniform errors, are also presented.

Table . ResultsoftheProposedSpecificationTests.Thep-valuesarebasedontheabsolutevalueofthetest statistic. The results show that for the list experiments based on voter fraud and alien abduction we detect model misspecification. For the list experiment on texting while driving, we fail to reject the null hypothesis.

, subject to the Cambridge Core terms of use, available at

Degrees of freedom Test statistic p-value

#### Voter fraud

Without covariates − .     .   With covariates −  .    < .  

#### Alien abduction

Without covariates −  .    < .   With covariates   .     .  

#### Texting while driving

Without covariates  .     .   With covariates  .     .  

09 Oct 2019 at 19:44:36

 .  Comparison Between the ML and NLS Regression Estimators

Weconducttwotypesofanalyses.First,wefitthemultivariateregressionmodelwithage,gender, andraceascovariatesusingtheMLandNLSestimationmethods.WeshowthattheNLSregression estimator does not overestimate the incidence of voter fraud and abduction. Next, we implement the test outlined in Section  . , and show that the di erence between MLreg and NLSreg clearly indicates model misspecification.

, on

Harvard-Smithsonian Centerfor Astrophysics

We begin by showing that NLSreg does not overestimate the prevalence of voter fraud and alien abduction. Figure presents the estimated proportion of the sensitive trait based on DiM, NLSreg, and MLreg as well as two other estimators that will be described later. We find that the NLS regression estimates closely track the DiM estimates. Indeed, the NLS estimate is statistically indistinguishable from the DiM estimate in all three cases. In the case of voter fraud, the NLS estimate—around . %andstatisticallyindistinguishablefromzero—exceedstheDiMestimateby 2.59 percentage points, with a   % bootstrap confidence interval equal to [−3.74, 9.30]. For the alien abduction list experiment, the NLS estimate exceeds the DiM estimate by 1.70 percentage points, also an insignificant di erence (  % CI: [−0.60, 5.90]). Last, for the texting-while-driving list experiment, the di erence is 1.10 percentage points (  % CI: [−1.40, 2.60].)

.

https://www.cambridge.org/core

HavingshownthatNLSregdoesnotyieldmeaningfullylargerestimatesthanDiM,wenowapply thestatisticaltestdevelopedinSection . totheselistexperiments.Table presentstheresultsof thisproposedspecificationtest.Forthelistexperimentsonvoterfraudandalienabduction,which our earlier analysis found most problematic, we obtain negative and large, positive values of the

Hausman test statistic. For the negative test statistic, we compute p-values based on the absolute value.Theresultsofthestatisticalhypothesistestsstronglysuggestthatthemodelismisspecified for the voter fraud and alien abduction experiments. In contrast, for the list experiment on texting while driving, we fail to reject the null hypothesis of correct model specification.

In sum, the proposed model specification test reaches the same conclusion as the descriptive analysis presented above: multivariate regression models should not be applied to list experiments with extremely rare sensitive traits. For the list experiments on voter fraud and alien abduction, we find strong evidence for model misspecification, suggesting the unreliability of multivariateregressionanalysisfortheselistexperiments.Incontrast,wefailtofindsuchevidence for the list experiment on texting while driving, for which the proportion of a irmative answers is relatively high.

.

https://www.cambridge.org/core/terms

 .  Modeling Response Error

Next, we apply the nonstrategic measurement error models developed in Section  .  to these dataandexaminewhethertheyyielddi erentresults.Earlier,wearguedthatthetop-biasederror processiso enimplausible,asitimpliesthatrespondentsarewillingtorevealsensitivetraits.We would expect top-biased error to be most unlikely for the list experiment on voter fraud, as this is the most unambiguously stigmatized trait. On the other hand, uniform error may be the more plausible measurement error mechanism, for example due to satisficing.

, subject to the Cambridge Core terms of use, available at

AsshowninFigure ,theresultsbasedonthesemeasurementerrormodelsareconsistentwith our arguments. For the list experiment on voter fraud, the top-biased error gives a relatively large estimate that is statistically indistinguishable from the ML estimate. In contrast, the uniform error model provides an estimate that is indistinguishable from zero with a   % confidence interval that is narrower than any other estimator. The list experiment on alien abduction yields a similar result. Like all other models, the top-biased error model gives an estimate that is statistically distinguishable from zero, suggesting that percent of respondents were abducted by aliens (even the DiM estimate is barely statistically insignificant). On the other hand, the prevalence estimate based on the uniform error process model has the narrowest   % confidence interval that contains zero, suggesting a superior model fit. The results indicate that the uniform error model is more e ective for mitigating nonstrategic respondent error in these data than the topbiased error model.

09 Oct 2019 at 19:44:36

Finally, the results for the list experiment on texting while driving show that the top-biased and uniform measurement error models yield estimates that are much more consistent with the other models. Although the estimate based on the uniform error model is smaller, it has a wider confidence interval than other estimates, suggesting a possibly poor model fit. Together with the other results shown in this section, this finding implies that only the estimates based on the list experiment on texting while driving are robust to various model specification and measurement errors, whereas the estimates for voter fraud and alien abduction are quite sensitive.

, on

Harvard-Smithsonian Centerfor Astrophysics

Our statistical analysis suggests that the problems described in Ahlquist ( ) arise mainly from the fact that voter fraud in the US and alien abduction are rare to nonexistent events. Given all three lists were implemented in the same survey on the same sample, and were consequently subject to the same nonstrategic measurement error, the robustness of the texting-while-driving lists indicates that researchers should be concerned more with the rarity of the traits under study than with nonstrategic measurement error per se. We provide additional evidence for this statement below by showing that accounting for measurement error does not alter any of the multivariate inferences that one would draw from the texting-while-driving list experiment.

.

https://www.cambridge.org/core

Table  . Multivariate Regression Analysis of the Texting-While-Driving List. This table shows the estimated coe icients from the baseline NLS and ML multivariate regression models, as well as the proposed robust ML, top-biased, and uniform measurement error models. Younger respondents are more likely to text while driving. We also find suggestive evidence that male respondents are more likely to text while driving.

NLS ML Robust ML Top-biased Uniform est. se. est. se. est. se. est. se. est. se.

Sensitive Trait

(Intercept)  .     .    − .     .    − .     .    − .     .    − .     .    Age − .     .    − .     .    − .     .    − .     .    − .     .    White − .     .    − .     .    − .     .    − .     .     .     .    Female − .     .    − .     .    − .     .    − .     .    − .     .   

.

https://www.cambridge.org/core/terms

Control Items

(Intercept) − .     .    − .     .    − .     .    − .     .    − .     .    Age − .     .    − .     .    − .     .    − .     .    − .     .    White − .     .    − .     .    − .     .    − .     .    − .     .    Female  .     .    − .     .    − .     .     .     .     .     .   

, subject to the Cambridge Core terms of use, available at

 .  Multivariate Regression Analysis of Texting While Driving

Recall that the goal of multivariate regression models for list experiments is to measure the association between the sensitive trait and respondent characteristics. We reiterate that voter fraud and alien abduction are so rare that multivariate analysis of these traits is likely to be unreliable. By contrast, the texting-while-driving list o ers a unique opportunity to examine how accounting for measurement error a ects the estimated regression parameters. Studies commonly assume that younger drivers are especially likely to text while driving. However, frequently used methods, such as analysis of tra ic accidents, are unable to measure this association directly (e.g., Delgado, Wanner, and McDonald ). Clearly, DiM also fails to shed light on this relationship.

09 Oct 2019 at 19:44:36

Figure and Table present the results from our multivariate analysis of the texting-whiledriving list. In Figure , we present predicted values for the di erent subgroups defined by the three covariates. These values are calculated by changing the variable of interest while fixing the other variables to their observed values. The highlighted comparisons correspond to statistically significant coe icients at the α = 0.10 level (see Table ). As the bottom-le  panel of the figure shows, we find a consistent association between age and texting while driving. In all models younger respondents are more likely to text while driving than older respondents. We find some evidenceofgenderdi erentiationaswell;malerespondentsappeartobeconsistentlymorelikely totextwhiledrivingthanfemalerespondents,althoughthisdi erenceisnotgenerallystatistically significant.

, on

Harvard-Smithsonian Centerfor Astrophysics

The overall conclusion is that accounting for uniform error does not have a substantial e ect on the conclusions that one would draw from the standard ML or NLS models. Moreover, the results illustrate the primary advantage of multivariate regression modeling, which is to assess the relationship between the sensitive trait and covariates.

.

### Concluding Recommendations

https://www.cambridge.org/core

In this paper, we develop statistical tools that researchers can use to detect and ameliorate nonstrategic measurement error in list experiments, arising for instance from enumerator or respondent noncompliance. Of course, our view is that the best cure for nonstrategic measurement error is to minimize it at the design and administration stages of surveys, and consequently that the presence of such error signals more fundamental flaws in the survey implementation. For example, because the top-biased error process runs directly against

.

https://www.cambridge.org/core/terms

Figure  . Multivariate Regression Analysis of the Texting-While-Driving List. This figure shows the estimated prevalence of texting while driving based on the di erent values of the predictor variables. Highlighted estimates correspond to significant coe icients at the α = 0.10 level. Accounting for measurement error, we find that younger respondents are significantly more likely to report texting while driving. We also find that male respondents are more likely to report texting while driving, though the di erences are generally insignificant.

, subject to the Cambridge Core terms of use, available at

respondents’ incentives to conceal sensitive traits, its presence suggests that they do not actually consider the topic to be sensitive in the first place. We would advise against the use of indirect questioning for such topics. The increased cognitive burden and variance of indirect questioning are too great to be used for nonsensitive traits. By extension, we also discourage the use of list experiments for topics like alien abduction, as this can prevent serious engagement with the survey and increase measurement error as a result.

Weconcludethispaperbyo eringsevenrecommendationsonhowtoanalyzelistexperiments with measurement error:

( ) Ifthegoalistoestimatetheprevalenceofthesensitivetrait,researchersshouldusetheDiM estimatorastheprimaryestimatorforitssimplicityandrobustness.Multivariateregression models should be used mainly when inferring the association between the sensitive trait and respondent characteristics.

09 Oct 2019 at 19:44:36

( ) Multivariate regression models should not be used if the DiM estimator yields a small or negativeestimateoftheprevalence.Asensitivetraitmustexistforittovarywithrespondent characteristics. In general, list experiments are not suitable for studying rare sensitive traits because they lack statistical power.

, on

Harvard-Smithsonian Centerfor Astrophysics

( ) It is important to first conduct a descriptive analysis as shown in Table . In particular, negative estimates of respondent type proportions would suggest that at least one of the identification assumptions of list experiments may have been violated (related statistical tests are described in Blair and Imai ( ) and Aronow et al. ( )).

( ) Researchers should compare the NLS and ML regression estimates. NLSreg relies on weaker assumptions than MLreg, and as a result the former is more robust (though less e icient) than the latter. Despite the greater fragility of MLreg, its reduced variance can matter when analyzing list experiments, an underpowered questioning mode. To help researchers adjudicate this bias-variance tradeo , we provide a model misspecification test predicated on the di erence between MLreg and NLSreg.

.

https://www.cambridge.org/core

( ) Multivariate regression models can be extended to model strategic and nonstrategic measurement error processes. These models can be used as robustness checks. Although practical steps can be taken to address nonstrategic error, even perfectly administered surveys are subject to strategic measurement error.

( ) ItispossibletomaketheNLSandMLestimatorsmorerobustbyusingauxiliaryinformation whenever available. In particular, aggregate truths will be helpful. Even when such information is not available, one can ensure that the NLS and ML regression estimators give results consistent with the DiM estimator.

( ) When possible, it is helpful to combine list experiments with direct questioning and other indirectquestioningtechniques.ThemethodsdevelopedbyBlair,Imai,andLyall( )and Aronow et al. ( ) can be used to conduct more credible analyses by combining the data from di erent survey methods.

.

https://www.cambridge.org/core/terms

- Appendix A. The Bias of the Di erence-in-Means Estimator under Nonstrategic Measurement Error In this appendix, we show that the DiM estimator is generally biased under the top-biased and uniform error processes. In both cases, the DiM estimator is generally biased because the range of the response variable (and therefore the magnitude of the measurement error bias) is correlated withthetreatmentstatus.Inparticular,biasislargewhentheprevalenceofsensitivetraitissmall.

First, under the top-biased error process, the bias of the DiM estimator is given by:

{ [(1 − p)(Yi∗ + Zi) + p(J + 1)] −  [(1 − p)Yi∗ + pJ]} − τ = (1 − p)τ + p − τ = p(1 − τ)

where τ = Pr(Zi = 1) is the proportion of those with a sensitive trait, p is the proportion of those who answer J +1 regardless of truthful response. The result shows that the bias is zero only when τ = 1, i.e., everyone has a sensitive trait. The bias increases as the prevalence of the sensitive trait decreases. Similarly, under the uniform measurement error mechanism, the bias is given by,

(1 − p)(Yi∗ + Zi) + p

J + 1 2 − (1 − p)Yi∗ + p

J 2 − τ = (1 − p)τ +

p 2 − τ = p

- 1

- 2 − τ .


Thus, in this case, the bias disappears only when the proportion of those with a sensitive trait exactly equals  . . Again, the bias is large when the prevalence of the sensitive trait is small.

- Appendix B. Computational Details for Measurement Error Models


, subject to the Cambridge Core terms of use, available at

09 Oct 2019 at 19:44:36

B.  The EM Algorithm For the Model of Top-Biased Error

We treat (Si, Zi,Yi∗) as (partially) missing data to form the following complete-data likelihood function,

, on

Harvard-Smithsonian Centerfor Astrophysics

N

J Yi∗

f (Xi;γ)Yi∗{1 − f (Xi;γ)}J−Yi∗. (B )

pSi (1 − p)1−Si g(Xi;β)TiZi {1 − g(Xi;β)}Ti(1−Zi)

i=1

With this much simpler form, we can use the EM algorithm, which consists of a series of weighted regressions, to obtain the ML estimator.

We first derive the E-step. For the latent variable of misreporting, we have,

   

p

p{1−g(Xi;β)f (Xi;γ)J}+g(Xi;β)f (Xi;γ)J if i ∈ J(1, J + 1)

.

https://www.cambridge.org/core

ξ(Xi,Ti,Yi) =  (Si Xi,Ti,Yi) =

p p{1−f (Xi;γ)J}+f (Xi;γ)J if i ∈ J(0, J) 0 otherwise.

The E-step for the latent variable of truthful response to the sensitive item is given by,

η(Xi, 1,Yi) =  (Zi Xi,Ti = 1,Yi)



0 if i ∈ J(1, 0)



(1−p)g(Xi ;β)f (Xi ;γ)J+p·g(Xi ;β)

p{1−g(Xi;β)f (Xi;γ)J}+g(Xi;β)f (Xi;γ)J if i ∈ J(1, J + 1)

=

g(Xi;β)(YiJ−1)f (Xi;γ)Yi−1{1−f (Xi;γ)}J−Yi+1 g(Xi;β)(YiJ−1)f (Xi;γ)Yi−1{1−f (Xi;γ)}J−Yi+1+{1−g(Xi;β)}(YJi)f (Xi;γ)Yi {1−f (Xi;γ)}J−Yi

 

.

otherwise.

https://www.cambridge.org/core/terms

Finally,theE-stepforthelatentvariablerepresentingtheresponsetothecontrolitemshasseveral di erent expressions depending on the values of observed variables. We begin with the control group,

ζJ(Xi, 0,Yi) = Pr(Yi∗ = J Xi,Ti = 0,Yi) =    

f (Xi ;γ)J p{1−f (Xi;γ)J}+f (Xi;γ)J if i ∈ J(0, J) 0 otherwise

, subject to the Cambridge Core terms of use, available at

and for 0 y < J,

   

p(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y

p{1−f (Xi;γ)J}+f (Xi;γ)J if i ∈ J(0, J) 1 ifYi = y 0 otherwise.

ζy(Xi, 0,Yi) = Pr(Yi∗ = y Xi,Ti = 0,Yi) =

For the treatment group, we have,

ζJ(Xi, 1,Yi) = Pr(Yi∗ = J Xi,Ti = 1,Yi)



(1−p)g(Xi ;β)f (Xi ;γ)J+p·f (Xi ;γ)J

p+(1−p)g(Xi;β)f (Xi;γ)J if i ∈ J(1, J + 1)

09 Oct 2019 at 19:44:36



{1−g(Xi ;β)}f (Xi ;γ)J {1−g(Xi;β)}f (Xi;γ)J+g(Xi;β)·J·f (Xi;γ)J−1{1−f (Xi;γ)} if i ∈ J(1, J) 0 otherwise

=

 

, on

ζ0(Xi, 1,Yi) = Pr(Yi∗ = 0   Xi,Ti = 1,Yi)

Harvard-Smithsonian Centerfor Astrophysics

   

p{1−f (Xi ;γ)}J p+(1−p)g(Xi;β)f (Xi;γ)J if i ∈ J(1, J + 1) 1 if i ∈ J(1, 0) 0 otherwise

=

and for 0 < y < J,

ζy(Xi, 1,Yi) = Pr(Yi∗ = y Xi,Ti = 1,Yi)



p(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y p+(1−p)g(Xi;β)f (Xi;γ)J if i ∈ J(1, J + 1)

.

https://www.cambridge.org/core

g(Xi;β)(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y g(Xi;β)(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y+{1−g(Xi;β)}(yJ+1)f (Xi;γ)y+1{1−f (Xi;γ)}J−y−1 } if i ∈ J(1, y + 1)



=

{1−g(Xi;β)}(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y {1−g(Xi;β)}(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y+g(Xi;β)(yJ−1)f (Xi;γ)y−1{1−f (Xi;γ)}J−y+1 if i ∈ J(1, y) 0 otherwise.

 

Finally, the Q-function is given by,

N

ξ(Xi,Ti,Yi)logp + {1 − ξ(Xi,Ti,Yi)}log(1 − p)

i=1

N

Ti [η(Xi, 1,Yi)logg(Xi;β) + {1 − η(Xi, 1,Yi)}log{1 − g(Xi;β)}]

+

i=1

y · ζy(Xi,Ti,Yi)   

logf (Xi;γ) +    

y · ζy(Xi,Ti,Yi)   

   

.

J

J

N

https://www.cambridge.org/core/terms

log{1 − f (Xi;γ)}.

J −

+

y=1

y=1

i=1

Thus, the M-step for p is,

N

1 N

ξ(Xi,Ti,Yi). (B )

p =

i=1

, subject to the Cambridge Core terms of use, available at

The M-steps for β and γ consist of a series of weighted logistic regressions.

B.  The EM Algorithm For the Model of Uniform Error

The complete-data likelihood is given by,

n

{p1Si (1 − p1)1−Si }Ti {p0Si (1 − p0)1−Si }1−Ti

i=1

J Yi∗

f (Xi;γ)Yi∗{1 − f (Xi;γ)}J−Yi∗. (B )

×g(Xi;β)TiZi {1 − g(Xi;β)}Ti(1−Zi)

Then, the EM algorithm, which consists of a series of weighted regressions, is used to obtain the ML estimator.

The E-steps for the latent variables of misreporting and truthful answer to the sensitive item are given by,

09 Oct 2019 at 19:44:36

ξ(Xi,Ti,Yi) =  (Si Xi,Ti,Yi) = Pr(Si = 1   Xi,Ti,Yi)



p1 J+2 p1

J+2+(1−p1)g(Xi;β)f (Xi;γ)J if i ∈ J(1, J + 1)

, on

p1 J+2 p1

##### J+2+(1−p1){1−g(Xi;β)}{1−f (Xi;γ)}J if i ∈ J(1, 0)

Harvard-Smithsonian Centerfor Astrophysics



=

p0 J+1

- p0

- J+1+(1−p0)(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y if i ∈ J(0, y)

p1 J+2 p1

- J+2+(1−p1) g(Xi;β)(YiJ−1)f (Xi;γ)Yi−1{1−f (Xi;γ)}J−Yi+1+{1−g(Xi;β)}(YJi)f (Xi;γ)Yi {1−f (Xi;γ)}J−Yi




 

otherwise

η(Xi,Ti = 1,Yi) = (Zi Xi,Ti = 1,Yi)



p1 J+2g(Xi ;β)+(1−p1)g(Xi ;β)f (Xi ;γ)J

(1−p1)g(Xi;β)f (Xi;γ)J+Jp+21 if i ∈ J(1, J + 1)

p1 J+2g(Xi ;β)



(1−p1){1−g(Xi;β)}{1−f (Xi;γ)}J+Jp+21 if i ∈ J(1, 0)

=

.

https://www.cambridge.org/core

J+2+(1−p1)(YiJ−1)f (Xi;γ)Yi−1{1−f (Xi;γ)}J−Yi+1 g(Xi;β)

p1

 

otherwise.

J+2+(1−p1) g(Xi;β)(YiJ−1)f (Xi;γ)Yi−1{1−f (Xi;γ)}J−Yi+1+{1−g(Xi;β)}(YJi)f (Xi;γ)Yi {1−f (Xi;γ)}J−Yi

p1

For the latent variable of response to the control items, we obtain the E-steps separately for di erent sets of observations. For the control group, we have

   

J+1+(1−p0) (yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y

p0

J+1+(1−p0)(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y if i ∈ J(0, y)

p0

ζy(Xi, 0,Yi) = Pr(Yi∗ = y Xi,Ti = 0,Yi) =

J+1(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y

p0

otherwise

J+1+(1−p0)(YJi)f (Xi;γ)Yi {1−f (Xi;γ)}J−Yi

p0

.

https://www.cambridge.org/core/terms

where y = 0, 1, . . ., J. For the treatment group, the E-step is more complex,

ζJ(Xi, 1,Yi) = Pr(Yi∗ = J Xi,Ti = 1,Yi)



{(1−p1)g(Xi;β)+Jp+21 }f (Xi;γ)J

J+2+(1−p1)g(Xi;β)f (Xi;γ)J if i ∈ J(1, J + 1) [(1−p1){1−g(Xi;β)}+Jp+21 ]f (Xi;γ)J

p1

(1−p1)[{1−g(Xi;β)}f (Xi;γ)J+g(Xi;β)Jf (Xi;γ)J−1{1−f (Xi;γ)}]+Jp+21 if i ∈ J(1, J)



=

p1 J+2f (Xi ;γ)J

J+2+(1−p1){1−g(Xi;β)}{1−f (Xi;γ)}J if i ∈ J(1, 0) p1 J+2f (Xi ;γ)J

, subject to the Cambridge Core terms of use, available at

p1

 

otherwise

(1−p1) {1−g(Xi;β)}(YJi)f (Xi;γ)Yi {1−f (Xi;γ)}J−Yi +g(Xi;β)(YiJ−1)f (Xi;γ)Yi−1{1−f (Xi;γ)}J−Yi+1 +Jp+21

ζ0(Xi, 1,Yi) = Pr(Yi∗ = 0   Xi,Ti = 1,Yi)



p1 J+2{1−f (Xi ;γ)}J

p1 J+2+(1−p1)g(Xi;β)f (Xi;γ)J if i ∈ J(1, J + 1) [Jp+21 +(1−p1){1−g(Xi;β)}]{1−f (Xi;γ)}J



J+2+(1−p1){1−g(Xi;β)}{1−f (Xi;γ)}J if i ∈ J(1, 0)

=

p1

[(1−p1){1−g(Xi;β)}+Jp+21 ]{1−f (Xi;γ)}J (1−p1) {1−g(Xi;β)}(YJi)f (Xi;γ)Yi {1−f (Xi;γ)}J−Yi +g(Xi;β)(YiJ−1)f (Xi;γ)Yi−1{1−f (Xi;γ)}J−Yi+1 +Jp+21

 

otherwise

and for 0 < y < J, we have,

09 Oct 2019 at 19:44:36

ζy(Xi, 1,Yi) = Pr(Yi∗ = y Xi,Ti = 1,Yi)



{Jp+21 +(1−p1)g(Xi;β)}(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y

J+2+(1−p1) g(Xi;β)(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y+{1−g(Xi;β)}(yJ+1)f (Xi;γ)y+1{1−f (Xi;γ)}J−y−1 if i ∈ J(1, y + 1) [Jp+21 +(1−p1){1−g(Xi;β)}](yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y

p1

J+2+(1−p1) g(Xi;β)(yJ−1)f (Xi;γ)y−1{1−f (Xi;γ)}J−y+1+{1−g(Xi;β)}(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y if i ∈ J(1, y)



p1

, on

=

Harvard-Smithsonian Centerfor Astrophysics

J+2(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y

p1

##### J+2+(1−p1){1−g(Xi;β)}{1−f (Xi;γ)}J if i ∈ J(1, 0)

p1

J+2(yJ)f (Xi;γ)y{1−f (Xi;γ)}J−y

p1

 

otherwise.

J+2+(1−p1) {1−g(Xi;β)}(YJi)f (Xi;γ)Yi {1−f (Xi;γ)}J−Yi +g(Xi;β)(YiJ−1)f (Xi;γ)Yi−1{1−f (Xi;γ)}J−Yi+1

p1

Finally, the Q-function is given by,

n

(Si Xi,Ti = 1,Yi)logp1 + {1 − (Si Xi,Ti = 1,Yi)}log(1 − p1)

i=1

+ (Si Xi,Ti = 0,Yi)logp0 + {1 − (Si Xi,Ti = 0,Yi)}log(1 − p0)

.

https://www.cambridge.org/core

(Zi Xi,Ti = 1,Yi)logg(Xi;β) + {1 − (Zi Xi,Ti = 1,Yi)}log{1 − g(Xi;β)}

+ (Yi∗ Xi,Ti,Yi)logf (Xi;γ) + {J − (Yi∗ Xi,Ti,Yi)}log{1 − f (Xi;γ)}. (B )

Hence, the M-steps for p0 and p1 are immediate. The M-steps for β and γ consist of a series of weighted logistic regressions.

B.  Details of the Robust Maximum Likelihood Multivariate Regression Estimator

We focus on the logistic regression model whose log-likelihood function is given as,

N

(X i β + JX i γ)

##### [J log{1 + exp(X i γ)} + log{1 + exp(X i β)}] +

−

i ∈J(1,J+1)

i=1

J

[yX i γ + log{1 + exp(X i β)}]

+

.

https://www.cambridge.org/core/terms

y=0 i ∈J(0,y)

J

J y − 1

J y

(y − 1)X i γ + log

exp(X i β) +

exp(X i γ) + constant. (B )

+

y=1 i ∈J(1,y)

Let Li(β,γ; Xi,Yi) represent the log-likelihood function for observation i. Then, the first order condition for each observation is given by,

∂ ∂β Li(β,γ; Xi,Yi)

, subject to the Cambridge Core terms of use, available at



exp(X i β) 1 + exp(X i β)

+ {i ∈ J(1, J + 1)}

−

=





J

y−1 exp(X i β) J

J

J

exp(X i β) 1 + exp(X i β)

{i ∈ J(0, y)}

{i ∈ J(1, y)}

+

+

##### Xi



y−1 exp(X i β) + y J exp(X i γ)

y=0

y=1

(B ) ∂

∂γ Li(β,γ; Xi,Yi)



J exp(X i γ) 1 + exp(X i γ)

+ J {i ∈ J(1, J + 1)}

−

=





J y exp(X i γ)

09 Oct 2019 at 19:44:36

J

J

y {i ∈ J(0, y)} +

{i ∈ J(1, y)} (y − 1) +

+

Xi . (B )



J

y−1 exp(X i β) + y J exp(X i γ)

y=0

y=1

The sample analogue of the moment condition given in equation ( ) can be written as,

, on

Harvard-Smithsonian Centerfor Astrophysics

N

N

exp(X i β)

1 N

1 N

1 + exp(X i β) − τˆ = 0 (B ) where τˆ is the DiM estimator. We can also express this condition as

Mi(β; Xi,Yi) =

i=1

i=1

N

N

exp(X i β)

exp(X i β) 1 + exp(X i β)

1 N

1 N

N N1

N N0

Mi(β; Xi,Yi) =

Yi + (1 −Ti)

1 + exp(X i β) −

+

Ti

Yi ,

i=1

i=1

(B ) in order to account for the correlation between this moment and the score function.

.

https://www.cambridge.org/core

Putting together all these moment conditions, the e icient GMM estimator is given by,

G(β,γ) W(β,γ)−1G(β,γ) (B  )

(βˆGMM,γˆGMM) = argmin

(β,γ)

where

N

N

1 N

1 N

∂ ∂β Li(β,γ; Xi,Yi)

∂ ∂γ Li(β,γ; Xi,Yi) Mi(β; Xi,Yi)

G(β,γ) =

Gi(β,γ) =

i=1

i=1

(B  ) W(β,γ) =

N

1 N

Gi(β,γ)Gi(β,γ) . (B  )

i=1

.

https://www.cambridge.org/core/terms

The asymptotic distribution of this estimator is given by:

−1

√

β ˆ γˆ

∂Gi(β,γ) ∂(β γ )

∂Gi(β,γ) ∂(β γ )

β γ

Ω(β,γ)−1

(B  )

−

N 0,

N

where

∂2

∂β∂β Li(β,γ; Xi,Yi) ∂β∂γ∂2 Li(β,γ; Xi,Yi)

, subject to the Cambridge Core terms of use, available at

∂Gi(β,γ) ∂(β γ )

(B  )

∂γ∂β Li(β,γ; Xi,Yi) ∂γ∂γ∂2 Li(β,γ; Xi,Yi)

∂2

=  

∂β Mi(β; Xi,Yi) 0

∂

and

∂Gi(β,γ) ∂(β γ )

∂Gi(β,γ) ∂(β γ )

Ω(β,γ) =  

. (B  )

Note that the second derivatives are given by,

∂2 ∂β∂β Li(β,γ; Xi,Yi)



09 Oct 2019 at 19:44:36

J

exp(X i β) {1 + exp(X i β)}2

exp(X i β) {1 + exp(X i β)}2

{i ∈ J(0, y)}

−

=

+



y=0



exp y J−1 y J X i (γ + β) J

J

{i ∈ J(1, y)}

XiX i (B  )

+



y−1 exp(X i β) + y J exp(X i γ) 2

, on

y=1

Harvard-Smithsonian Centerfor Astrophysics

∂2 ∂γ∂γ Li(β,γ; Xi,Yi)





exp y J−1 y J X i (γ + β) J

J

J exp(X i γ) {1 + exp(X i γ)}2

{i ∈ J(1, y)}

−

=

+

XiX i





y−1 exp(X i β) + y J exp(X i γ) 2

y=1

(B  ) ∂2

∂β∂γ Li(β,γ; Xi,Yi)





exp y J−1 y J X i (γ + β) J

J

.

XiX i . (B  )

{i ∈ J(1, y)}

https://www.cambridge.org/core

= −





y−1 exp(X i β) + y J exp(X i γ) 2

y=1

### Supplementary material

For supplementary material accompanying this paper, please visit https://doi.org/  .    /pan.    .  .

### References

Ahlquist, John S.     . “List experiment design, non-strategic respondent error, and item count technique estimators.” Political Analysis   :  –  .

Ahlquist, John S., Kenneth R. Mayer, and Simon Jackman.     . “Alien abduction and voter impersonation in the      U.S. General Election: Evidence from a survey list experiment.” Election Law Journal   :   –   .

Aronow, Peter M., Alexander Coppock, Forrest W. Crawford, and Donald P. Green.     . “Combining list experiment and direct question estimates of sensitive behavior prevalence.” Journal of Survey Statistics and Methodology  :  –  .

.

Blair, Graeme, and Kosuke Imai.     . “Statistical analysis of list experiments.” Political Analysis   :  –  . Blair, Graeme, Kosuke Imai, and Jason Lyall.     . “Comparing and combining list and endorsement

https://www.cambridge.org/core/terms

experiments: Evidence from Afghanistan.” American Journal of Political Science   :    –    . Blair, Graeme, Kosuke Imai, and Yang-Yang Zhou.     . “Design and analysis of randomized response technique.” Journal of the American Statistical Association    :    –    .

Blair, Graeme, Winston Chou, and Kosuke Imai.      list: Statistical methods for the item count technique and list experiment. Available at the Comprehensive R Archive Network (CRAN). https://CRAN.R-project.org/package=list.

Blair, Graeme, Winston Chou, and Kosuke Imai.      “Replication data for: List experiments with measurement error.” https://doi.org/  .    /DVN/L GWNP, Harvard Dataverse. Bullock, Will, Kosuke Imai, and Jacob N. Shapiro.     . “Statistical analysis of endorsement experiments: Measuring support for militant groups in Pakistan.” Political Analysis   :   –   . Carroll, Raymond J., David Ruppert, Leonard A. Stefanski, and Ciprian M. Crainiceanu.     . Measurement error in nonlinear models: A modern perspective.  nd ed. London: Chapman & Hall. Chou, Winston.     . Lying on surveys: Methods for list experiments with direct questioning. Technical report, Princeton University. Chou, Winston, Kosuke Imai, and Bryn Rosenfeld.     . “Sensitive survey questions with auxiliary information.” Sociological Methods & Research, doi:  /    /                . Corstange, Daniel.     . “Sensitive questions, truthful answers?: Modeling the list experiment with LISTIT.” Political Analysis   :  –  .

, subject to the Cambridge Core terms of use, available at

Delgado, M. Kit, Kathryn J. Wanner, and Catherine McDonald.     . “Adolescent cellphone use while driving: An overview of the literature and promising future directions for prevention.” Media and Communication  :  –  .

Dempster, Arthur P., Nan M. Laird, and Donald B. Rubin.     . “Maximum likelihood from incomplete data via the EM algorithm (with discussion).” Journal of the Royal Statistical Society, Series B, Methodological   : –  .

09 Oct 2019 at 19:44:36

Gelman, Andrew, Aleks Jakulin, Maria Grazia Pittau, and Yu-Sung Su.     . “A weakly informative default prior distribution for logistic and other regression models.” Annals of Applied Statistics  :    –    . Gingerich, Daniel W.     . “Understanding o -the-books politics: Conducting inference on the

determinants of sensitive behavior with randomized response surveys.” Political Analysis   :   –   . Glynn, Adam N.     . “What can we learn with statistical truth serum?: Design and analysis of the list

experiment.” Public Opinion Quarterly   :   –   . Hausman, Jerry A.     . “Specification tests in econometrics.” Econometrica   :    –    . Imai, Kosuke.     . “Multivariate regression analysis for the item count technique.” Journal of the American

, on

Harvard-Smithsonian Centerfor Astrophysics

Statistical Association    :   –   .

King, Gary, and Langche Zeng.     . “Logistic regression in rare events data.” Political Analysis  :   –   . Lyall, Jason, Graeme Blair, and Kosuke Imai.     . “Explaining support for combatants during wartime: A

survey experiment in Afghanistan.” American Political Science Review    :   –   . Miller, J. D.      The item-count/paired lists technique: An indirect method of surveying deviant behavior. PhD thesis, George Washington University. Rosenfeld, Bryn, Kosuke Imai, and Jacob Shapiro.     . “An empirical validation study of popular survey methodologies for sensitive questions.” American Journal of Political Science   :   –   . Schreiber, Sven.     . “The Hausman test statistic can be negative, even asymptotically.” Jahrbücher für Nationalökonomie und Statistik    :   –   . Sobel, Richard.     . “Voter-ID Issues in Politics and Political Science: Editor’s Introduction.” PS: Political Science & Politics   :  –  .

.

https://www.cambridge.org/core

