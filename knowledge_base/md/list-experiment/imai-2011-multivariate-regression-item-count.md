## Kosuke IMAI

# Multivariate Regression Analysis for the Item Count Technique

The item count technique is a survey methodology that is designed to elicit respondents’ truthful answers to sensitive questions such as racial prejudice and drug use. The method is also known as the list experiment or the unmatched count technique and is an alternative to the commonly used randomized response method. In this article, I propose new nonlinear least squares and maximum likelihood estimators for efﬁcient multivariate regression analysis with the item count technique. The two-step estimation procedure and the Expectation Maximization algorithm are developed to facilitate the computation. Enabling multivariate regression analysis is essential because researchers are typically interested in knowing how the probability of answering the sensitive question afﬁrmatively varies as a function of respondents’ characteristics. As an empirical illustration, the proposed methodology is applied to the 1991 National Race and Politics survey where the investigators used the item count technique to measure the degree of racial hatred in the United States. Small-scale simulation studies suggest that the maximum likelihood estimator can be substantially more efﬁcient than alternative estimators. Statistical efﬁciency is an important concern for the item count technique because indirect questioning means loss of information. The open-source software is made available to implement the proposed methodology.

KEY WORDS: Indirect questioning; List experiments; Privacy protection; Sensitive questions; Survey methodology.

### 1. INTRODUCTION AND EXAMPLE

In survey research, an important methodological challenge has been the elicitation of truthful answers to sensitive questions. For a long time, the randomized response method introduced by Warner (1965) has been a dominant technique to address this problem, and many reﬁnements have been proposed. An alternative method that has recently begun to attract much attention of applied empirical researchers is the item count technique. This method was originally proposed by Miller (1984) and is also known as the list experiment or the unmatched count technique. A similar survey methodology was studied earlier by Raghavarao and Federer (1979) who called it the block total response method.

The item count technique has been used across a wide variety of disciplines. Applications include self-reports of racial prejudice (Kuklinski, Cobb, and Gilens 1997; Gilens, Sniderman, and Kuklinski 1998), attitudes towards immigration (Janus 2010), drug use (Droitcour et al. 1991), employee theft (Wimbush and Dalton 1997), and risky sexual behavior (LaBrie and Earleywine 2000). Although the validity of this method remains to be investigated more rigorously, some have reported promising initial results showing that the item count technique can successfully elicit truthful answers to sensitive questions (e.g., Tsuchiya, Hirai, and Ono 2007; Holbrook and Krosnick 2010; Coutts and Jann 2011).

Kosuke Imai is Assistant Professor, Department of Politics, Princeton University, Princeton NJ 08544 (E-mail: kimai@princeton.edu; url: http://imai. princeton.edu). Additional statistical methods useful for item count technique are developed in the companion article (Blair and Imai 2010b). The open-source software, list: Statistical Methods for the Item Count Technique and List Experiment, is available for download at the Comprehensive R Archive Network (http://cran.r-project.org/package=list). Previous versions of this article were ciculated under the title of “Statistical Inference for the Item Count Technique.” I thank Thomas Yee for his help in ﬁtting the Beta-Binomial model and useful comments. Thanks also to Graeme Blair, Patrick Brandt, and Adam Glynn for useful discussions. Detailed comments from the associate editor and anonymous referees signiﬁcantly improved the presentation and analysis of this article. The Institute for Quantitative Social Science at Harvard University provided the computational support for the simulation studies. Financial support from the NSF grant (SES–0849715) is acknowledged.

407

To illustrate the basic idea of the item count technique, consider the question of how to measure racial hatred against black people. Asking white respondents directly whether or not they dislike black people may be problematic because the respondents may give a “right” but untruthful answer. To avoid this possible social desirability bias, Sniderman, Tetlock, and Piazza (1992) employ the item count technique in the 1991 National Race and Politics Survey. Speciﬁcally, the respondents were randomly selected into the treatment and control groups. The control group was then presented with the following question:

Now I’m going to read you three things that sometimes make people angry or upset. After I read all three, just tell me HOW MANY of them upset you. (I don’t want to know which ones, just how many.)

- (1) “the federal government increasing the tax on gasoline;”
- (2) “professional athletes getting million-dollar-plus salaries;”
- (3) “large corporations polluting the environment.”


How many, if any, of these things upset you?

The treatment group was given the same question except that the sensitive item was added to the list used for the control group,

Now I’m going to read you four things that sometimes make people angry or upset. After I read all four, just tell me HOW MANY of them upset you. (I don’t want to know which ones, just how many.)

- (1) “the federal government increasing the tax on gasoline;”
- (2) “professional athletes getting million-dollar-plus salaries;”
- (3) “large corporations polluting the environment;”
- (4) “a black family moving next door to you.”


How many, if any, of these things upset you?

Note that for both treatment and control groups, the order of items on the lists can be randomized in order to mitigate the order effects. This indirect questioning technique attempts to provide a greater degree of privacy to respondents by asking only the total number of items that make them angry rather than having them answer each item separately. Moreover, because the treatment and control groups are randomly selected,

© 2011 American Statistical Association Journal of the American Statistical Association

June 2011, Vol. 106, No. 494, Applications and Case Studies DOI: 10.1198/jasa.2011.ap10415

the proportion of the respondents whose answer is afﬁrmative to the sensitive item can be estimated under certain assumptions by simply computing the difference in the mean response between those two groups.

Finally, although a detailed discussion is beyond the scope of this article, I emphasize that when applying the item count technique the control items (i.e., the items presented to the control group) must be carefully selected. In particular, the privacy is no longer protected if respondents in the treatment group wish to answer all sensitive and control questions either afﬁrmatively or negatively. If this problem occurs to many respondents, then the validity of the survey measurement may be compromised. Increasing the number of control items partially addresses this problem, but the resulting estimator will be statistically inefﬁcient. See Blair and Imai (2010b) for the discussion of statistical methods that address these and other failures of the item count technique.

Despite the growing use of the item count technique in applied research, there exist relatively few methodological research on the topic. The most commonly used method has been based on a simple difference-in-means estimator. Tsuchiya (2005) extends this method and considers an efﬁcient estimation in different subpopulations deﬁned by a discrete covariate. Chaudhuri and Christoﬁdes (2007) propose to improve the standard item count technique by slightly modifying the way the sensitive item is incorporated and derive a new estimator. Glynn (2010) suggests an adjustment to the difference-inmeans estimator, which yields greater efﬁciency at the cost of bias. Finally, Corstange (2009) proposes an approximate likelihood method, but his method is not applicable to the standard item count technique (see Blair and Imai 2010b, who propose the maximum likelihood estimator for this and other alternative designs based on the methodology proposed in this article).

In this article, new nonlinear least squares (NLS) and maximum likelihood (ML) estimators are developed for an efﬁcient multivariate analysis with the item count technique. Enabling a multivariate statistical analysis is essential because researchers are typically interested in knowing how the probability of answering the sensitive question afﬁrmatively varies as a function of respondents’ characteristics as well as estimating the population proportion of such respondents. For example, in their analysis of the 1991 National Race and Politics Survey introduced above, Kuklinski, Cobb, and Gilens (1997) were interested in estimating the difference between Southern and non-Southern whites with respect to the population proportion of those who answer the black family item afﬁrmatively while adjusting for certain demographic differences between them. Employing the difference-in-means estimator separately in each strata, as commonly done in applied research, is problematic especially when the number of strata is large.

To address this concern, I develop two new multivariate regression estimators. First, I consider the NLS estimator. For the NLS estimator, a computationally simple two-step estimation procedure is used to obtain consistent estimates. An advantage of the NLS estimator is that it provides a consistent estimate so long as the conditional mean functions are correctly speciﬁed. The NLS estimator also includes the conventional difference-in-means and the linear least squares estimators as special cases.

Second, the likelihood function is derived for the item count technique by regarding the answer to the sensitive question as

missing data. This formulation naturally leads to the use of the Expectation-Maximization algorithm for the reliable computation of the ML estimator. Finally, the proposed methodology is applied to the 1991 National Race and Politics survey question introduced above. In addition, small-scale simulation studies suggest that the ML estimator can be substantially more efﬁcient than other alternative estimators. The open-source software that implements the proposed estimators is available for download at the Comprehensive R Archive Network as Blair and Imai (2010a).

### 2. THE PROPOSED METHODOLOGY

In this section, the proposed methodology is described. First, the notation and the required identiﬁcation assumptions are introduced. I then develop two new estimators for the item count technique.

### 2.1 The Standard Design and Assumptions

Suppose that a simple random sample of N respondents is obtained from a population. I consider the standard design for the item count technique where there are J control items and one sensitive item. Let Ti represent the binary “treatment” status for respondent i; Ti = 0 means that the respondent is presented with the partial list of J control items whereas Ti = 1 indicates that the respondent is presented with the full list of J + 1 items including a sensitive question as well as control questions.

Next, suppose that each respondent possesses a latent potential response to each control item j = 1,...,J, which may depend on the respondent’s treatment status t. Using the potential outcomes notation (e.g., Holland 1986), I denote this variable by Zij(t), which is equal to 1 if the answer is afﬁrmative and equals 0 otherwise. For example, Zij(1) = 1 means that respondent i’s latent answer to the jth control item is afﬁrmative under the treatment condition. Furthermore, let Zi,J+1(1) denote respondent i’s latent answer to the sensitive question under the treatment condition. Recall that only the treatment group is presented with the sensitive item and so Zi,J+1(0) is not deﬁned.

Since respondents are instructed to give the total number of items on the list rather than answer each item separately, the potential responses can be deﬁned as Yi(1) = Jj=+11 Zij(1) and Yi(0) = Jj=1 Zij(0) where Yi(1) ∈ {0,...,J + 1} and Yi(0) ∈ {0,...,J}. Finally, the observed outcome is given by Yi = Yi(Ti) and a vector of pretreatment covariates is denoted by Xi where the support of Xi is given by X.

Under this setting, the identiﬁcation assumptions of the item count technique can be formally expressed as follows:

- Assumption 1 (Randomization of the Treatment). For any re-

spondent i = 1,...,N,

{Zij(0),Zij(1)}Jj=1,Zi,J+1(1) ⊥ Ti.

- Assumption 2 (No Design Effect). For any respondent i =

1,...,N,

J

j=1

Zij(0) =

J

j=1

Zij(1).

- Assumption 3 (No Liar). For any respondent i = 1,...,N,


Zi,J+1(1) represents a truthful response.

Note that Assumption 1 is guaranteed to hold because researchers conduct the randomization of respondents into the treatment and control groups. In contrast, Assumption 2 may be violated if respondents give different answers to control items depending on whether or not the sensitive item is included in the list. This type of design effect may occur if respondents evaluate items on the list relative to one another. Thus, this identifying assumption suggests that one must carefully choose control items in the item count technique. Finally, Assumption 3 implies that respondents give truthful answers about the sensitive item when asked indirectly about it using the item count technique. Note that we do not assume the answers to control items are truthful. For control items, we only need to assume that they are not affected by the addition of the sensitive item to the list.

In sum, Assumptions 2 and 3 together eliminate the possibility that the coexistence of the sensitive and control items in a single list inﬂuence responses in one way or another. In practice, however, these assumptions need to be made with care. For example, researchers are often concerned about the possibility that the location of the sensitive item in the treatment list may affect respondents’ answers. To minimize such potential order effects, they often randomize the order of items on the list. However, this may lead to the violation of the Stable Unit Treatment Value Assumption, which requires no multiple versions of treatment (Rubin 1990). Addressing these design effects is beyond the scope of this article, but interested readers may refer to Blair and Imai (2010b) who develop several methods to address these potential violations of the identiﬁcation assumptions (see also VanderWeele and Hernán 2010).

### 2.2 Identiﬁcation

Before describing the proposed estimators, I brieﬂy consider the issue of identiﬁcation. First, it is immediate that under Assumptions 1 and 2, we have

### Yi(1) − Yi(0) = Zi,J+1(1). (1)

This justiﬁes the following standard difference-in-means estimator that is commonly used to analyze the item count technique,

N

N

1 N1

1 N0

τˆ =

TiYi −

(1 − Ti)Yi, (2)

i=1

i=1

where N1 = Ni=1 Ti and N0 = N −N1. In particular, τˆ is an unbiased estimate of the population average response to the sensi-

tive item, that is, E(τ)ˆ = Pr(Zi,J+1(1) = 1).

Furthermore, as shown by Glynn (2010), it is important to note that under Assumptions 1 and 2 one can can identify the joint distribution Pr(Zi,J+1(1) = z,Yi(t) = y) for each t = 0,1 and z = 0,1. To see this formally, ﬁrst note that we have Pr(Yi(0) = y) = Pr(Yi | Ti = 0) for each y = 1,...,J by Assumption 1. Second, we have

Pr(Zi,J+1(1) = 1 | Yi(0) = y)

Pr(Yi(1) = y + 1,Yi(0) = y) Pr(Yi(0) = y | Ti = 0)

=

(3)

Pr(Yi ≤ y | Ti = 0) − Pr(Yi ≤ y | Ti = 1) Pr(Yi = y | Ti = 0)

=

, (4) where the second equality follows from Assumptions 1 and 2.

### 2.3 The Nonlinear Least Squares Estimator

Next, I consider the generalization of the standard differencein-means estimator in Equation (2) to a multivariate analysis based on the following additive nonlinear regression model,

Yi = f(Xi,γ) + Tig(Xi,δ) + i, (5)

where E( i | Xi,Ti) = 0 and (γ,δ) is a vector of unknown parameters. The model implies that f(x,γ) = E(Yi(0) | Xi = x) and g(x,δ) = Pr(Zi,J+1(1) = 1 | Xi = x) for x ∈ X. Typically, researchers are interested in estimating g(x,δ) so that they can determine the association between respondents’ characteristics, Xi, and their answer to the sensitive item, Zi,J+1(1).

To estimate (δ,γ), I propose the following computationally simple two-step procedure. First, obtain the NLS estimate of γ from the control group Ti = 0, and denote it by γˆNLS. Then, compute the NLS estimate of δ from the treatment group, δˆNLS, by setting γ equal to the estimate obtained from the ﬁrst step, γˆNLS.

Given this two-step procedure, when computing the standard error for δˆNLS, one must take into account for the fact that γ is estimated. In the Appendix, the asymptotic sampling distribution of this two-step NLS estimator is derived for a case of logistic models where it is assumed that f(Xi,γ) = J logit−1(X i γ) and g(Xi,δ) = logit−1(X i δ). The asymptotic sampling distribution for other parametric models such as probit links can be derived in a similar way.

The main advantage of the NLS estimator is that it provides a consistent estimator so long as the conditional mean functions, that is, f(x,γ) and g(x,δ), are correctly speciﬁed. The NLS estimator also includes two important estimators as special cases. First, when f(x,γ) = γ and g(x,δ) = δ, this procedure yields τˆ deﬁned in Equation (2), thereby generalizing the standard difference-in-means estimator. Next, if we assume linear functional form f(x,γ) = x γ and g(x,δ) = x δ, we have the following linear regression model with interaction terms:

Yi = X i γ + TiX i δ + i, (6)

where E( i | Xi,Ti) = 0. While it may not be appropriate for modeling discrete outcomes, this linear model can be easily estimated without the two-step procedure. Note that the heteroscedasticity-consistent robust standard errors must be computed for this model.

### 2.4 The Maximum Likelihood Estimator

The two-step NLS estimator is attractive in terms of its computational simplicity and connection to the difference-in-means and linear least squares estimators. However, one disadvantage is the potential loss of statistical efﬁciency. Also, it is not straightforward to extend this approach to more complex models such as hierarchical models. Therefore, I derive the maximum likelihood estimator by modeling the joint distribution of (Yi(0),Zi,J+1(1)), which is identiﬁable under Assumptions 1 and 2 as shown in Section 2.2.

To construct the likelihood function, notice that there exist the following four possible types of respondents according to their values of (Ti,Yi):

• (Ti,Yi) = (1,0): these respondents have (Yi(0), Zi,J+1(1)) = (0,0)

- • (Ti,Yi) = (1,J + 1): these respondents have (Yi(0), Zi,J+1(1)) = (J,1)
- • (Ti,Yi) = (0,y): these respondents have either (Yi(0), Zi,J+1(1)) = (y,1) or (y,0)
- • (Ti,Yi) = (1,y) where 0 < y < J + 1: these respondents have either (Yi(0),Zi,J+1(1)) = (y,0) or (y − 1,1).


Given this setup, if we let hz(y;x,ψz) = Pr(Yi(0) = y | Zi,J+1(1) = z,Xi = x) and g(x,δ) = Pr(Zi,J+1(1) = 1 | Xi = x), then the observed-data likelihood function can be written as

Lobs(ψ0,ψ1,δ;{Yi,Ti,Xi}Ni=1)

(1 − g(Xi,δ))h0(0;Xi,ψ0)

=

i∈J (1,0)

g(Xi,δ)h1(J;Xi,ψ1)

×

i∈J (1,J+1)

J

g(Xi,δ)h1(y − 1;Xi,ψ1)

×

y=1 i∈J (1,y)

+ (1 − g(Xi,δ))h0(y;Xi,ψ0)

J

g(Xi,δ)h1(y;Xi,ψ1)

×

y=0 i∈J (0,y)

+ (1 − g(Xi,δ))h0(y;Xi,ψ0) , (7)

where J (t,y) represents a set of respondents with (Ti,Yi) = (t,y). As mentioned before, researchers are typically interested in making inferences about the answers to the sensitive item, that is, g(x,δ), more than the control items.

The likelihood function in Equation (7) is potentially difﬁcult to optimize because it has two separate mixture components. Thus, I construct the Expectation-Maximization (EM) algorithm (Dempster, Laird, and Rubin 1977) by regarding Zi,J+1(1) as partially missing data. In this framework, given the complete data (Zi,J+1(1),Yi,Ti), the complete-data likelihood function can be written as

Lcom ψ0,ψ1,δ;{Zi,J+1(1),Yi,Ti,Xi}Ni=1

N

g(Xi,δ)h1(Yi − 1;Xi,ψ1)Ti

=

i=1

× h1(Yi;Xi,ψ1)1−Ti Zi,J+1(1) × (1 − g(Xi,δ))h0(Yi;Xi,ψ0) 1−Zi,J+1(1).

The E-step of the algorithm can then be derived by computing the following conditional expectation of the missing data,

wi = E(Zi,J+1(1) | Yi = y,Ti = t,Xi = x) = Pr(Zi,J+1(1) = 1 | Ti = t,Xi = x) × Pr(Yi = y | Zi,J+1(1) = 1,Ti = t,Xi = x) /Pr(Yi = y | Ti = t,Xi = x)

= Pr(Zi,J+1(1) = 1 | Xi = x) × Pr(Yi(0) = y − t | Zi,J+1(1) = 1,Ti = t,Xi = x) /Pr(Yi = y | Ti = t,Xi = x)

= Pr(Zi,J+1(1) = 1 | Xi = x) × Pr(Yi(0) = y − t | Zi,J+1(1) = 1,Xi = x) /Pr(Yi = y | Ti = t,Xi = x)

g(x,δ)h1(y − t;x,ψ1) g(x,δ)h1(y − t;x,ψ1) + (1 − g(x,δ))h0(y;x,ψ0)

=

, (8)

where the second, third, and fourth equalities follow from the Bayes’ rule, Assumption 2, and Assumption 1, respectively. Note that wi = 1 if Yi = J + 1 and Ti = 1 whereas wi = 0 if Yi = 0 and Ti = 1.

Then, the M-step will maximize the following objective function with respect to (ψ0,ψ1,δ) given the observed data {Yi,Ti,Xi}Ni=1 as well as {wi}Ni=1, which is evaluated at the current values of the parameters

Q(ψ0,ψ1,δ;{Yi,Ti,Xi,wi}Ni=1)

N

wi logg(Xi,δ)

=

i=1

+ Ti logh1(Yi − 1;Xi,ψ1) + (1 − Ti)logh1(Yi;Xi,ψ1)

+ (1 − wi) log(1 − g(Xi,δ)) + logh0(Yi;Xi,ψ0) .

The advantage of the EM algorithm is that in the M-step each of the three terms, g(x,δ), h0(y;x,ψ0), h1(y;x,ψ1), can be independently maximized based on their corresponding weighted log-likelihood functions. Thus, as I illustrate below with the beta-binomial model, the standard model ﬁtting routine can be used to implement the EM algorithm.

Finally, given the likelihood inference framework in Section 2.4, Bayesian inference can be conducted relatively easily. Naturally, the data augmentation algorithm can be used to exploit the missing data framework as done in the EM algorithm. In the context of the beta-binomial model, a Markov chain Monte Carlo (MCMC) algorithm can be constructed so that conditional on the model parameters, the missing data Zi,J+1(1) is sampled from the Bernoulli distribution with the probability wi given in Equation (8). Then, given this draw of Zi,J+1(1), the standard MCMC algorithms for the logistic and beta-binomial regression models can be used to update the model parameters.

### 2.5 The Beta-Binomial Model

To illustrate the above likelihood inference framework, I con-

sider the following model: Zi,J+1(1) | Xi = x indep∼ . Binom(1,logit−1(x δ)) Yi(0) | πi,Zi,J+1(1) = z,Xi = x indep∼ . Binom(J,πi) πi | Zi,J+1(1) = z,Xi = x

μz(x)(1 − ρz(x)) ρz(x)

(1 − μz(x))(1 − ρz(x)) ρz(x)

indep∼ . Beta

,

for z = 0,1 where 0 < μz(x) < 1 and 0 < ρz(x) < 1 for all x ∈ X, which is the support of Xi. This is the beta-binomial model with the mean E(Yi(0) | Zi,J+1(1) = z,Xi = x) = Jμz(x)

and the variance V(Yi(0) | Zi,J+1(1) = z,Xi = x) = Jμz(x)(1 − μz(x)){1 + ρz(x)(J − 1)}. For example, we can use the logistic model, that is, μz(x) = logit−1(x ψz). This parameterization was used by Lee and Sabavala (1987) and slightly differs from the standard parameterization (e.g., Grifﬁths 1973). The advantage of this alternative parameterization is the ease of interpretation. In particular, ρz(x) can be interpreted as the intrarespondent correlation across any two control questions among respondents who possess speciﬁc characteristics x and have response z to the sensitive question. Finally, μz(x) can be interpreted as the average response to J control items conditional on the response for the sensitive item.

The EM algorithm for this model is relatively straightforward. Speciﬁcally, the E-step requires the evaluation of the beta-binomial density function and the M-step consists of the ﬁtting of the weighted logistic regression [for g(x,δ)] and the weighted beta-binomial regression [for hz(y;x,ψz)]. For ﬁtting the weighted beta-binomial regression, I use the algorithm as implemented in the VGAM package (Yee and Hastie 2003; Yee 2010).

### 3. EMPIRICAL AND SIMULATIONS STUDIES

In this section, the methods developed in Section 2 are applied to the question from the 1991 National Race and Politics Survey that is described in Section 1. In addition, small scale simulation studies are conducted to compare the performance of the ML estimator with that of alternative estimators.

For the computation of all empirical and simulation results, the following strategy is employed. For the NLS estimator, the nls() function in R is used. For the ML estimation, I use the EM algorithm described in Section 2.4, and the asymptotic variance is calculated based on the numerical approximation via the optim() function in R.

### 3.1 Racial Prejudice and the “New South”

In their inﬂuential article, Kuklinski, Cobb, and Gilens (1997) analyze the question from the 1991 National Race and Politics Survey that is described in Section 1. The authors present the evidence against the prevalent notion of “New South,” which states that during the late 1970s and 1980s the South underwent the transformation where antiblack prejudice among Southern whites has declined to the level similar to the prejudice among non-Southern whites. (The deﬁnition of the South includes Alabama, Arkansas, Florida, Georgia, Louisiana, Mississippi, North Carolina, South Carolina, Texas, and Virginia).

Using the standard difference-in-means estimator, that is, τˆ in Equation (2), they ﬁnd that a large proportion of Southern whites answer afﬁrmatively to the question whether “a black family moving next door to you” will make them angry whereas very few non-Southern whites do so. This difference is statistically signiﬁcant and used as main evidence for the conclusion that there still exists a signiﬁcant amount of racial prejudice in the South.

After presenting the above evidence, Kuklinski, Cobb, and Gilens (1997, pp. 334–335) point out one possible objection to their analysis.

So far our discussion has implicitly assumed that the higher level of prejudice among white Southerners results from something uniquely ‘southern,’ what many would call southern culture. This assumption could be wrong. If white southerners were older, less educated, and the like—characteristics normally associated with greater prejudice—then demographics would explain the regional difference in racial attitudes, leaving culture as little more than a small and relatively insigniﬁcant residual.

To address this concern, the authors compare the marginal distributions of demographic variables between Southern and nonSouthern whites (table 3 on p. 337), and show that they are somewhat similar. This is then used as evidence to support their conclusion that demographic characteristics cannot explain the difference between the South and the non-South.

Here, I apply the proposed method and reexamine the question of whether there exists the difference between Southern and non-Southern whites even after taking into account other demographic characteristics. Speciﬁcally, in addition to the variable indicating whether a respondent lives in a Southern state, I include three demographic variables—age, education, and gender—that are used by the original authors (see table 4 on p. 339) as the pretreatment variables Xi. I follow the original coding where education is measured as a binary variable representing whether respondents attended college, although I do not dichotomize the age variable like the original analysis. The sample consists of 1213 white respondents, of which 285 are Southerners.

The linear and nonlinear least squares estimators as well as ML estimators are computed. For the ML estimation, the data shows little overdispersion and hence I use the binomial model, which is a limiting special case of the beta-binomial model described in Section 2.5. In addition, for the ML estimation, two models are ﬁtted, one with the constraint h0(y;x,ψ0) = h1(y;x,ψ1) and the other without it. Substantively, this constraint implies that a respondent’s answer to the sensitive item is not correlated with his/her answer to the control items after adjusting for the four pretreatment variables.

Table 1 presents the estimated coefﬁcients for all four models. Across all four models, the estimated coefﬁcient for the South variable (highlighted in gray) is positive in the model for the sensitive item. This estimated coefﬁcient is statistically signiﬁcantly different from zero at the conventional 5% level for the NLS and constrained ML estimators. The result implies that on average Southern whites are more likely to be angered by a black family moving next door than non-Southern whites even after adjusting for the demographic differences. In the models for the sensitive item, the standard errors for the constrained ML estimates are substantially smaller than those for the NLS estimates. Given the difﬁculty of directly interpreting these coefﬁcients (other than those from the linear least squares), a direct comparison across four models will be conducted when discussing Figure 1 below.

Furthermore, the assumption of the independence between the answer to the sensitive item and those to the control items can be statistically tested within the framework of the ML estimation. Speciﬁcally, the likelihood ratio test can be conducted to test the null hypothesis is that the constraint holds. The pvalue from this hypothesis test is 0.760, implying the failure to reject the null hypothesis. Thus, if I take the constrained model

Table 1. Estimated coefﬁcients from the item count technique regression models where the sensitive item is whether or not “a black family moving next door to you” will make (white) respondents angry. The key coefﬁcient of interest is the one for the variable South (highlighted in gray), which indicates whether or not a respondent lives in one of the Southern states. All the coefﬁcients except the linear least squares estimates are based on logistic regression models

Least squares estimator Maximum likelihood estimator

Linear Nonlinear Constrained model Unconstrained model Variables Est. SE Est. SE Est. SE Est. SE Est. SE Sensitive item

Intercept −0.434 0.160 −7.084 3.669 −5.508 1.021 −6.226 1.045

South 0.202 0.118 2.490 1.268 1.675 0.559 1.379 0.820 Age 0.007 0.003 0.026 0.031 0.064 0.016 0.065 0.021 Male 0.180 0.098 3.097 2.829 0.846 0.494 1.366 0.612 College 0.114 0.098 0.612 1.030 −0.315 0.474 −0.182 0.569

Control item h0(y;x,ψ0) h1(y;x,ψ1)

Intercept 2.406 0.105 1.388 0.187 1.191 0.144 1.156 0.156 3.781 2.159 South −0.180 0.074 −0.277 0.116 −0.292 0.097 −0.299 0.107 −0.270 0.590 Age 0.002 0.002 0.003 0.004 0.003 0.003 0.003 0.003 −0.013 0.016 Male −0.202 0.065 −0.332 0.107 −0.251 0.082 −0.218 0.086 −1.689 1.633 College −0.394 0.064 −0.662 0.113 −0.516 0.084 −0.488 0.087 −0.954 0.715

as the ﬁnal model, the result supports the conclusion of the original analysis that Southern whites are on average more likely to possess an anti-black sentiment than non-Southern counterparts, and this difference is statistically signiﬁcant even after adjusting for certain demographic differences.

Finally, based on the ﬁtted models listed in Table 1 as well as the models without covariates, Figure 1 presents the estimated proportions of Southern (squares) and non-Southern (circles) whites who are angered by “A black family moving next door to you.” For the NLS and ML estimators with covariates, the re-

sults are obtained by averaging over the sample distribution of covariates. The solid lines represent the 95% asymptotic conﬁdence intervals. The ML estimates are based on the constrained model. The results show that the ML estimators have substantially shorter conﬁdence intervals than the other estimators, illustrating the potential efﬁciency gain of a multivariate analysis. Indeed, unlike the other estimators, the asymptotic conﬁdence intervals for the ML estimator do not overlap with zero, which is consistent with the fact that the proportion is bounded below by zero (though of course this pattern does not generally hold).

| | |
|---|---|
| | |
| | |


| | |
|---|---|
| | |
| | |


| | |
|---|---|
| | |
| | |


| | |
|---|---|
| | |
| | |


| | |
|---|---|
| | |
| | |


- Figure 1. Estimated proportion of whites who are angered by “a black family moving next door to you” based on different estimation


methods. Each open square, open circle, and solid triangle represent the estimated proportion for Southern whites, that for non-Southern whites, and the difference between those two proportions, respectively. The solid lines represent the 95% asymptotic conﬁdence intervals. The maximum likelihood estimates are based on the binomial model without the constraint (those given in columns 5 and 6 of Table 1). For the models with covariates, the results are averaged over the sample distribution of covariates.

- Figure 2. Simulation results with no covariates. The data are generated according to the constrained binomial model without covariates for

the sample sizes of 500, 1000, and 2500. Plots represent bias, root mean square error, and the coverage of 90% conﬁdence interval for the estimated proportion of afﬁrmative answer to the sensitive item. The performance of the maximum likelihood (ML, solid circles) estimator is compared with that of the difference-in-means estimator (open circles). The results are based on 5000 Monte Carlo simulations.

- 3.2 Simulation Studies


to induce a moderate degree of positive correlation among control items. Finally, the outcome variable is sampled according to the beta-binomial model presented in Section 2.5 with the constraint h0(y;x,ψ0) = h1(y;x,ψ1).

I conduct two small-scale simulation studies to examine the relative performance of the ML estimator over the other alternatives. First, we compare the ML estimator with the differencein-means estimator, which is a special case of our NLS estimator when there exist no covariates. I sample the response variable using the ML estimates based on the constrained binomial model as the true values. For example, the true proportion of afﬁrmative answer to the sensitive item is set to 0.154. I generate the data according to this binomial model and compute bias, root mean square error (RMSE), and the coverage of 90% conﬁdence intervals using three different sample sizes, that is, 500, 1000, and 2500. In this setting, we expect both estimators to be unbiased but the ML estimator to have smaller variance than the difference-in-means estimator because the former incorporates the knowledge about the distribution of the response variable.

The sample sizes are set to 1000, 2500, and 5000. A total of 5000 Monte Carlo simulations are conducted for each sample size, and the bias, RMSE, and the coverage probability of the 90% asymptotic conﬁdence intervals are estimated for both the NLS and ML estimators. For the ML estimator, the constrained beta-binomial model is ﬁtted. Note that this data generating process is also consistent with the NLS model. The goal of this simulation study, therefore, is to assess the degree of relative efﬁciency loss the NLS estimator would incur by not incorporating the distributional assumption (in comparison with the ML estimator which is under this setting is known to be asymptotically the best unbiased estimator).

Figure 3 summarizes the simulation results for four coefﬁcients corresponding each of the covariates (rows). As expected, the ML estimator (solid circles) outperforms the NLS estimator in terms of bias and RMSE, and this difference can be substantial especially when the sample size is small. Across all coefﬁcients, the coverage of the 90% asymptotic conﬁdence intervals are reasonably close to its nominal coverage rate for both estimators even when the sample size is small. Overall, the simulation results suggest that the potential efﬁciency gain of the ML estimator is large if the distributional assumption of the model is correct.

Figure 2 presents the simulation results, which are based on 5000 independent Monte Carlo draws. As expected, both estimators exhibit little bias across sample sizes, whereas the ML estimator has smaller RMSE than the difference-in-means estimator. The conﬁdence intervals for the two estimators have appropriate coverage especially when the sample size is large. The result suggests that in the analysis of item count technique incorporating the knowledge of response distribution can lead to a substantial efﬁciency gain. This ﬁnding is consistent with the empirical example given above and is important because researchers must recoup the efﬁciency loss due to indirect questioning.

Finally, another small-scale simulation study is conducted to examine the relative efﬁciency of the ML estimator over the NLS estimator in the situations where covariates are available. To make the data generating process somewhat realistic, I take the survey data analyzed in Section 3.1 and sample covariates from the multivariate normal distribution whose mean vector and variance matrix are equal to the sample counterparts of the race data. For the true values of the coefﬁcients, the estimated coefﬁcients from the ML constrained binomial model in Table 1 are used. The overdispersion parameter ρ is set to 0.25

### 4. CONCLUDING REMARKS AND FUTURE RESEARCH

Eliciting truthful answers to sensitive questions has been one of the main challenges for survey research. Although statisticians have extensively studied the randomized response method, the item count technique has recently emerged as a viable alternative among applied empirical researchers across a number of disciplines. One important advantage of the item count technique over the randomized response method is that

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


Figure 3. Simulation results with covariates. The data are generated according to the constrained beta-binomial model for the sample sizes of 1000, 2500, and 5000. Each row represents the coefﬁcient for a speciﬁc covariate and the columns represent the statistics evaluating the performance of the nonlinear least squares (NLS, open circles) and maximum likelihood (ML, solid circles) estimators. The results are based on 5000 Monte Carlo simulations.

it does not require respondents to conduct randomization. This ease of implementation has allowed many applied researchers to use the item count technique when designing their own surveys. Another advantage is that respondents can easily understand why the item count technique provides privacy. Indeed, some scholars ﬁnd that the item count technique outperforms the randomized response method for various sensitive questions (Coutts and Jann 2011).

While the item count technique offers a promising method to ask sensitive survey questions, many methodological challenges remain. One major problem, which is addressed in this article, is the lack of efﬁcient multivariate regression technique applicable for this survey methodology. In this article, I develop the NLS and ML estimators to fulﬁll this gap. The empirical and simulation studies illustrate the potential efﬁciency gain of the proposed methods especially when the knowledge

of response distribution is incorporated. The likelihood inference framework developed in this article also will serve as the foundation for building more sophisticated modeling strategies such as Bayesian analysis and hierarchical modeling that may be required in more complex empirical applications.

Finally, future research should address potential failures of the item count technique. Speciﬁcally, statistical methods need to be developed for detecting and adjusting for the violations of the key identifying assumptions that underlie the item count technique (formalized as Assumptions 2 and 3 in this article) (see e.g., Blair and Imai 2010b; Glynn 2010). The development of such methods should shed light on effective ways in which applied researchers design and analyze survey questions based on the item count technique.

APPENDIX: THE ASYMPTOTIC SAMPLING DISTRIBUTION OF THE TWO–STEP NONLINEAR LEAST SQUARES ESTIMATOR FOR LOGISTIC MODELS

I follow the analytical strategy outlined in Newey and McFadden (1994, section 6) by treating the two-step estimator as a method of moments estimator which solves the following ﬁrst order conditions with probability approaching one,

N

exp(X i δ) 1 + exp(X i δ)

J exp(X i γ) 1 + exp(X i γ)

exp(X i δ) {1 + exp(X i δ)}2

1 N

##### Xi

= 0,

−

Ti Yi −

i=1

m1(Yi,Ti,Xi,δ,γ)

N

J exp(X i γ) 1 + exp(X i γ)

J exp(X i γ) {1 + exp(X i γ)}2

1 N

##### Xi

= 0.

(1 − Ti) Yi −

i=1

m0(Yi,Ti,Xi,γ)

Thus, under the standard regularity conditions (Hansen 1982), the two-step estimator is consistent. The asymptotic sampling distribution is given by

δ ˆNLS − δ γˆNLS − γ

√

−→ D N(0,V), where V = G−1F(G−1) .

N

The expressions for F and G are given below:

E(m1(Yi,Ti,Xi,δ,γ)m1(Yi,Ti,Xi,δ,γ) ) 0 0

F =

E(m0(Yi,Ti,Xi,γ)m0(Yi,Ti,Xi,γ) ) and

#### G−1 1 −G−1 1G2G−3 1

−1

G1 G2 0 G3

G−1 =

=

0 G−3 1 where the submatrices of G are given by

- G1 = E

∂m1(Yi,Ti,Xi,δ,γ) ∂δ

= −E

Ti exp(2X i δ) {1 + exp(X i δ)}4

XiX i ,

- G2 = E


∂m1(Yi,Ti,Xi,γ) ∂γ

= −E

JTi exp{X i (δ + γ)} {1 + exp(X i δ)}2{1 + exp(X i γ)}2

XiX i ,

G3 = E

∂m0(Yi,Ti,Xi,γ) ∂γ

J2(1 − Ti)exp(2X i γ) {1 + exp(X i γ)}4

#### XiX i .

= −E

[Received June 2010. Revised January 2011.]

### REFERENCES

Blair, G., and Imai, K. (2010a), “list: Statistical Methods for the Item Count Technique and List Experiment,” The Comprehensive R Archive Network (CRAN), available at http://CRAN.R-project.org/package=list. [408]

(2010b), “Statistical Analysis of List Experiments,” technical report, Dept. of Politics, Princeton University. Available at http://imai.princeton. edu/research/listP.html. [407-409,415]

Chaudhuri, A., and Christoﬁdes, T. C. (2007), “Item Count Technique in Estimating the Proportion of People With a Sensitive Feature,” Journal of Statistical Planning and Inference, 137, 589–593. [408]

Corstange, D. (2009), “Sensitive Questions, Truthful Answers?: Modeling the List Experiment With LISTIT,” Political Analysis, 17, 45–63. [408]

Coutts, E., and Jann, B. (2011), “Sensitive Questions in Online Surveys: Experimental Results for the Randomized Response Technique (RRT) and the Unmatched Count Technique (UCT),” Sociological Methods & Research, 40 (1), 169–193. [407,414]

Dempster, A. P., Laird, N. M., and Rubin, D. B. (1977), “Maximum Likelihood From Incomplete Data via the EM Algorithm” (with discussion), Journal of the Royal Statistical Society, Ser. B, 39, 1–37. [410]

Droitcour, J., Caspar, R. A., Hubbard, M. L., and Ezzati, T. M. (1991), “The Item Count Technique as a Method of Indirect Questioning: A Review of Its Development and a Case Study Application,” in Measurement Errors in Surveys, eds. P. P. Biemer, R. M. Groves, L. E. Lyberg, N. A. Mathiowetz, and S. Sudman, New York: Wiley, pp. 185–210. [407]

Gilens, M., Sniderman, P. M., and Kuklinski, J. H. (1998), “Afﬁrmative Action and the Politics of Realignment,” British Journal of Political Science, 28

(1), 159–183. [407]

Glynn, A. N. (2010), “What Can We Learn With Statistical Truth Serum?: Design and Analysis of the List Experiment,” technical report., Dept. of Government, Harvard University. [408,409,415]

Grifﬁths, D. A. (1973), “Maximum Likelihood Estimation for the BetaBinomial Distribution and an Application to the Household Distribution of the Total Number of Cases of a Disease,” Biometrics, 29 (4), 637–648. [411]

Hansen, L. P. (1982), “Large Sample Properties of Generalized Method of Moments Estimators,” Econometrica, 50 (4), 1029–1054. [415]

Holbrook, A. L., and Krosnick, J. A. (2010), “Social Desirability Bias in Voter Turnout Reports: Tests Using the Item Count Technique,” Public Opinion Quarterly, 74 (1), 37–67. [407]

Holland, P. W. (1986), “Statistics and Causal Inference” (with discussion),

Journal of the American Statistical Association, 81, 945–960. [408]

Janus, A. L. (2010), “The Inﬂuence of Social Desirability Pressures on Expressed Immigration Attitudes,” Social Science Quarterly, 91 (4), 928–946. [407]

Kuklinski, J. H., Cobb, M. D., and Gilens, M. (1997), “Racial Attitudes and the ‘New South’,” Journal of Politics, 59 (2), 323–349. [407,408,411]

LaBrie, J. W., and Earleywine, M. (2000), “Sexual Risk Behaviors and Alcohol: Higher Base Rates Revealed Using the Unmatched-Count Technique,” Journal of Sex Research, 37 (4), 321–326. [407]

Lee, J. C., and Sabavala, D. J. (1987), “Bayesian Estimation and Prediction for the Beta-Binomial Model,” Journal of Business & Economic Statistics, 5

(3), 357–367. [411] Miller, J. D. (1984), “A New Survey Technique for Studying Deviant Behavior,” Ph.D. thesis, The George Washington University. [407]

Newey, W., and McFadden, D. (1994), “Large Sample Estimation and Hypothesis Testing,” in Handbook of Econometrics, eds. R. F. Engle and D. L. McFadden, Vol. IV, Amsterdam: North Holland, pp. 2111–2245. [415] Raghavarao, D., and Federer, W. T. (1979), “Block Total Response as an Alternative to the Randomized Response Method in Surveys,” Journal of the Royal Statistical Society, Ser. B, 41 (1), 40–45. [407]

Rubin, D. B. (1990), Comment on “On the Application of Probability Theory to Agricultural Experiments. Essay on Principles. Section 9,” by J. SplawaNeyman (translated from the Polish and edited by D. M. Dabrowska and T. P. Speed), Statistical Science, 5, 472–480. [409]

Sniderman, P. M., Tetlock, P. E., and Piazza, T. (1992), “Codebook for the 1991 National Race and Politics Survey,” Survey Research Center, Berkeley, CA, available at http://sda.berkeley.edu/D3/Natlrace/Doc/nrac.htm. [407] Tsuchiya, T. (2005), “Domain Estimators for the Item Count Technique,” Sur-

vey Methodology, 31 (1), 41–51. [408]

Tsuchiya, T., Hirai, Y., and Ono, S. (2007), “A Study of the Properties of the Item Count Technique,” Public Opinon Quarterly, 71 (2), 253–272. [407]

VanderWeele, T. J., and Hernán, M. A. (2010), “Causal Inference Under Multiple Versions of Treatment,” technical report, Harvard School of Public Health. [409]

Warner, S. L. (1965), “Randomized Response: A Survey Technique for Eliminating Evasive Answer Bias,” Journal of the American Statistical Association, 60 (309), 63–69. [407]

Wimbush, J. C., and Dalton, D. R. (1997), “Base Rate for Employee Theft: Convergence of Multiple Methods,” Journal of Applied Psychology, 82 (5), 756–763. [407]

Yee, T. W. (2010), “The VGAM Package for Categorical Data Analysis,” Jour-

###### nal of Statistical Software, 32 (10), 1–34. [411]

Yee, T. W., and Hastie, T. J. (2003), “Reduced-Rank Vector Generalized Linear Models,” Statistical Modelling, 3, 15–41. [411]

