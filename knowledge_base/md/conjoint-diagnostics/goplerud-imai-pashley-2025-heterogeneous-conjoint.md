# Estimating Heterogeneous Causal Eﬀects of High-Dimensional Treatments Using Interpretable Machine Learning: Application to Conjoint Analysis∗

Max Goplerud† Kosuke Imai‡ Nicole E. Pashley§ August 5, 2021

Abstract

Estimation of heterogeneous treatment eﬀects is an active area of research in causal inference. Most of the existing methods, however, focus on estimating the conditional average treatment eﬀects of a single, binary treatment given a set of pre-treatment covariates. Indeed, there exists little research that models heterogeneous eﬀects of high-dimensional treatments, which pose unique challenges in terms of computation and interpretation. In this paper, we propose a method to estimate the heterogeneous causal eﬀects of high-dimensional treatments using interpretable machine learning. The proposed approach is based on a Bayesian mixture of regularized regressions to identify groups of units who exhibit similar patterns of treatment eﬀects. By directly modeling cluster membership with covariates, the proposed methodology allows one to explore the unit characteristics that are associated with diﬀerent patterns of treatment eﬀects. Our motivating application is conjoint analysis, which is a popular survey experiment in social science and marketing research and is based on a high-dimensional factorial design. We apply the proposed methodology to the conjoint data, where survey respondents are asked to select one of two immigrant proﬁles with randomly selected attributes. We ﬁnd that a group of respondents with a relatively high degree of prejudice appears to discriminate against immigrants from non-European countries like Iraq and those who cannot speak English ﬂuently. An open-source software package is available for implementing the proposed methodology.

Key words: causal inference, factorial design, mixture model, randomized experiment, regularized regression

∗Imai thanks the Alfred P. Sloan Foundation (Grant number 2020–13946) for partial support. Pashley was partially supported by the National Science Foundation Graduate Research Fellowship while working on this project under Grant No. DGE1745303. Any opinion, ﬁndings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reﬂect the views of the National Science Foundation.

†Assistant Professor, Department of Political Science, University of Pittsburgh. 4600 Wesley W. Posvar Hall, Pittsburgh, PA 15260. Email: mgoplerud@pitt.edu. URL: https://mgoplerud.com

‡Professor, Department of Government and Department of Statistics, Harvard University. 1737 Cambridge Street, Institute for Quantitative Social Science, Cambridge MA 02138. Email: imai@harvard.edu URL: https://imai.fas.harvard.edu

§Assistant Professor, Department of Statistics, Rutgers University. 501 Hill Center, 110 Frelinghuysen Road, Piscataway, NJ 08854. Email: nicole.pashley@rutgers.edu

## 1 Introduction

Over the past decade, a number of researchers have exploited modern machine learning algorithms and proposed new methods to estimate heterogeneous treatment eﬀects using experimental data. They include tree-based methods (e.g., Imai and Strauss, 2011; Athey and Imbens, 2016; Wager and Athey, 2018; Hahn, Murray and Carvalho, 2020), regularized regressions (e.g., Imai and Ratkovic, 2013; Tian et al., 2014; Ku¨nzel et al., 2018), ensemble methods (e.g., van der Laan and Rose, 2011; Grimmer, Messing and Westwood, 2017), and frameworks that allow for the use of generic machine learning methods (e.g., Chernozhukov et al., 2019; Imai and Li, 2021). This methodological development, however, has largely been conﬁned to settings with a single, binary treatment variable. Indeed, there exists little prior research that models heterogeneous eﬀects of high-dimensional treatments, which pose unique challenges in terms of computation and interpretation.

In this paper, we consider the estimation of heterogeneous causal eﬀects based on the data from a randomized experiment, in which the treatments of interest are high-dimensional with the number of possible treatment combinations exceeding the sample size. We address the challenge of eﬀectively summarizing the complex patterns of heterogeneous treatment eﬀects that are induced by the interactions among the treatments themselves as well as the interactions between the treatments and unit characteristics. We use an interpretable machine learning algorithm based on a ﬁnite mixture of regularized regressions to identify groups of units who exhibit similar patterns of treatment eﬀects. To further facilitate the interpretation of the results, we directly model cluster membership using unit characteristics. Thus, the proposed methodology allows one to explore the unit characteristics that are associated with diﬀerent patterns of treatment eﬀects.

Our motivating application is conjoint analysis, which is a popular survey experimental methodology in social sciences and marketing research (e.g., Hainmueller, Hopkins and Yamamoto, 2014; Rao, 2014). Conjoint analysis is a variant of factorial designs with a large number of factorial treatments (Dasgupta, Pillai and Rubin, 2015). Under the most commonly used “forced-choice” design, respondents are asked to evaluate a pair of proﬁles whose attributes are randomly selected based on factorial variables with several levels. In the speciﬁc experiment we reanalyze, for example, the original authors used a conjoint analysis to measure immigration preferences by presenting each survey respondent with several pairs of immigrant proﬁles with varying attributes including education, country of origin, and job experience (Hainmueller and Hopkins, 2015). For each pair, the respondent was asked to choose one proﬁle they prefer. The authors then analyzed the resulting response patterns to understand which immigrant characteristics play a critical role in forming the immigration preferences of American citizens.

In the methodological literature on factorial designs and conjoint analysis, researchers have almost exclusively focused upon the estimation of marginal eﬀects, which represent the average eﬀect of one factor level relative to another level of the same factor averaging over the randomization distribution of the remaining factors (Hainmueller, Hopkins and Yamamoto, 2014; Dasgupta, Pillai and Rubin, 2015). Although some have explored the estimation of interaction eﬀects among the factorial treatments (e.g., Dasgupta, Pillai and Rubin, 2015; Egami and Imai, 2019), there exists little methodological research that investigates how to estimate heterogeneous treatment eﬀects of highdimensional treatments. As a result, in conjoint analysis, a dominant approach to the estimation of heterogeneous treatment eﬀects is based on subgroup analysis, in which researchers estimate the marginal eﬀects of interest using a particular subset of respondents (e.g., Hainmueller and Hopkins, 2015; Newman and Malhotra, 2019). Unfortunately, this approach often results in low statistical power and may suﬀer from multiple testing problems. In addition, subgroup analysis that focuses on marginal eﬀects fails to capture complex patterns of treatment eﬀects based on interactions that may be of scientiﬁc interest.

To overcome this challenge, we propose an interpretable machine learning algorithm based on a Bayesian ﬁnite mixture of regularized regressions. We build a model that draws together two distinct strands of methodological research. First, a number of scholars have developed a ﬁnite mixture of regularized regressions (e.g., Khalili and Chen, 2007; St¨dler, Bu¨hlmann and Van De Geer, 2010), with some allowing covariates to predict cluster membership under a mixture-of-experts framework (Khalili, 2010). The marketing literature using conjoint analysis has long applied similar mixture models to analyzing heterogeneity (e.g., Gupta and Chintagunta, 1994; Andrews, Ainslie and Currim, 2002), although their treatments are typically low dimensional and do not require regularization. Using a mixture-of-experts gives a small number of treatment eﬀect patterns that can be easily interpreted while also incorporating a rich set of moderators to characterize how they relate to diﬀerent patterns of treatment eﬀects.

Second, to analyze the data from a high-dimensional factorial experiment, we draw on a growing literature that shows how to regularize factor variables by grouping and fusing levels together rather than shrinking levels to zero (e.g., Bondell and Reich, 2009; Post and Bondell, 2013; Stokell, Shah and Tibshirani, 2021). This facilitates the interpretation of empirical ﬁndings by identifying a set of factor levels that characterize treatment eﬀect heterogeneity. Our proposed model accommodates interactions, respecting a hierarchical structure where the main eﬀects may be fused only if the interactions themselves are also fused (Yan and Bien, 2017). For regularization, we use an 2 norm for computational tractability although existing work has relied on a ∞ norm penalty to induce

sparsity (Post and Bondell, 2013; Egami and Imai, 2019).

To ﬁt this model, we use a Bayesian approach and apply an Expectation-Maximization (EM) algorithm through data augmentation to ﬁnd the posterior mode (Dempster, Laird and Rubin, 1977; Meng and van Dyk, 1997). We exploit the representation of 1 and 2 penalties as a mixture of Gaussians and derive a tractable, closed-form, EM algorithm (see, e.g., Figueiredo 2003; Polson and Scott 2011; Ratkovic and Tingley 2017; Goplerud 2021, for some uses of EM algorithm for sparse models). This formulation allows for commonly available methods to accelerate EM algorithms while maintaining monotonic convergence such as SQUAREM (Varadhan and Roland, 2008).

The rest of the paper is organized as follows. In Section 2, we discuss the motivating application, which is a conjoint analysis of American citizens’ preferences regarding immigrant features. We also brieﬂy describe a methodological challenge to be addressed. In Section 3 , we present our proposed methodology. In Section 4, we apply this methodology and reanalyze the data from the motivating conjoint analysis. Section 5 concludes with a discussion.

## 2 Motivating Application: Conjoint Analysis of Immigration Pref-erences

Our motivating application is a conjoint analysis of American immigration preferences. In this section, we introduce the experimental design and discuss the results of previous analyses that motivate our methodology for estimating heterogeneous treatment eﬀects.

### 2.1 The Experimental Design

In an inﬂuential study, Hainmueller and Hopkins (2015) use conjoint analysis to estimate the eﬀect of immigrant attributes on preferences for admission to the United States. The authors conduct an online survey experiment using a sample of 1,407 American adults. Each survey respondent assessed ﬁve pairs of immigrant proﬁles with randomly selected attributes. For each pair, a respondent was asked to choose one of the two immigrant proﬁles they preferred to admit to the United States.

The attributes of immigrant proﬁles used in this factorial experiment are gender, education, employment plans, job experience, profession, language skills, country of origin, reasons for applying, and prior trips to the United States. For completeness, these factors and their levels are reproduced as Table 1 in Section A of the Supplementary Appendix. In total, there exist 7 × 2 × 10 × 4 × 3 × 11 × 4 × 4 × 5 = 1,478,400 possible proﬁles, implying that there are more than 2 × 1012 possible comparisons that can be made. It is clear that with 1,407 respondents, even though each respondent performs ﬁve comparisons, not all possible proﬁles can be included.

The levels of each factor variable were independently randomized to yield one immigration proﬁle.

Overall High Prejudice Low Prejudice

Iraq

Somalia

Sudan

Country of Origin

China

India

Poland

Philippines

Mexico

France

Germany

−0.2 0.0 0.2 −0.2 0.0 0.2 −0.2 0.0 0.2

Effect

- Figure 1: Estimated average marginal component eﬀects (AMCEs) of country of origin where the baseline is Germany. The“Overall” plot presents the overall eﬀects, as given in the original analysis of Hainmueller and Hopkins (2015), whereas the right two plots present the results of a subgroup analysis based on the level of respondent’s hispanic prejudice score.


Randomization was subject to some restrictions such that profession and education factors result in sensible pairings (e.g., ruling out doctors with with less than two-years of college education) and immigrants whose reason for applying is persecution are from Iraq, Sudan, or Somalia. The ordering of the attributes was also randomized for each respondent. The experiment additionally collected data on the respondents, including various demographic information, partisanship, attitudes towards immigration, and ethnocentrism. A rating for each immigrant proﬁle was also recorded, but that metric is not the focus of our analysis.

### 2.2 Heterogeneous Treatment Eﬀects

In the original article, Hainmueller and Hopkins (2015) conducted their primary analysis based on linear regression model where the unit of analysis is an immigrant proﬁle (rather than a pair) and the outcome variable is an indicator for whether a given proﬁle was chosen. The predictors of the model include the indicator variable for each immigrant attribute. The model also includes the interactions between education and profession, as well as between country of origin and reasons for applying, in order to account for the restricted randomization scheme mentioned above. Finally, the standard errors are clustered by respondent.

As formalized in Hainmueller, Hopkins and Yamamoto (2014), the regression coeﬃcient repre-

sents the average marginal component eﬀect (AMCE) of each attribute averaging over all the other attributes including those of the other proﬁle in a given pair. The left plot of Figure 1 reproduces the estimated overall AMCEs of country of origin where the baseline category is India. There is little country eﬀect with the exception of Iraq, which negatively aﬀects the likelihood of being preferred by a respondent.

Beyond the AMCEs, these authors and others including Newman and Malhotra (2019) have explored the heterogeneous treatment eﬀects among respondents by conducting many sub-group analyses for respondent characteristics including partisanship and level of education. Here, we follow Newman and Malhotra (2019) and focus on a measure of ethnic and racial prejudice by utilizing the hispanic prejudice score, which represents a 0–100 point feeling thermometer towards hispanics. We dichotomize this score in the same way as Newman and Malhotra (2019), labeling those with score below 50 as “high prejudice,” and all others as “low prejudice.”

The results for high and low prejudice groups are shown in the right two plots of Figure 1. The estimated AMCEs appear to suggest that respondents with low prejudice give similar preference to immigrants from most countries, except for Iraq and Somalia which are not preferred. Respondents with high prejudice give stronger preference to immigrants from Germany, France, Poland, and the Phillipines. However, the estimates are noisy as demonstrated by wide conﬁdence intervals.

Although these results suggest possible existence of heterogeneous treatment eﬀects, there is a room for improved analysis. First, it may be desirable to avoid dichotomization of moderator. Second, we may wish to add other moderators of interest to our analysis rather than conducting separate subgroup analyses as done in the conjoint analysis literature. When analyzing highdimensional treatments, it is especially important to use a principled method for the estimation of heterogeneous treatment eﬀects. Researchers must parsimoniously characterize how a large number of possible treatment combinations interact with several key moderators of interest. We now turn to our methodology which is designed to address this challenge.

## 3 The Proposed Methodology

In this section, we describe the proposed methodology for estimating heterogeneous eﬀects of highdimensional treatments. To simplify the exposition and notation, we focus on a general factorial design. This design corresponds to conjoint analysis with a single task per person and the complete and independent randomization of all levels within each factor. The extensions to more realistic conjoint analyses are immediate and will be discussed and applied in Section 4.

- 3.1 Set Up Suppose that we have a simple random sample of N units. Consider a factorial design with J factors where each factor j ∈ {1,··· ,J} has Lj ≥ 2 levels. The treatment variable for unit i, denoted by Ti, is a J-dimensional vector of random variables, each of which represents the assigned level of the corresponding factor variable. For example, the jth element of this random vector Tij ∈ {0,1,2,...,Lj − 1} represents the level of factor j. Following Dasgupta, Pillai and Rubin

(2015), we deﬁne the potential outcome as Yi(t) where t ∈ T represents the realized treatment with T representing the support of the randomization distribution for Ti. Then, the observed outcome is given by Yi = Yi(Ti). The notation implicitly assumes no interference between units (Rubin, 1980). In this paper, for the sake of concreteness, we focus on the binary outcome Yi ∈ {0,1}. Extensions to non-binary outcomes are straightforward. Lastly, we observe a vector of M pre-treatment covariates for each unit i and denote it by Xi.

The randomization of treatment assignment implies,

{Yi(t)}t∈T ⊥⊥ Ti (1)

for each i. In many practical applications of conjoint analysis, researchers independently and uniformly randomize each factor. However, in some cases including our application, researchers may exclude certain unrealistic combinations of factor levels (e.g., doctor without a college degree), leading to the dependence between factors. In all cases, researchers have complete knowledge of the randomization distribution of the factorial treatment variables.

- 3.2 Modeling Heterogeneous Treatment Eﬀects


The most basic causal quantity of interest is the average marginal component eﬀect (AMCE; Hainmueller, Hopkins and Yamamoto, 2014), which is deﬁned for any given factor j as,

δj(l,l ) = E{Yi(Tij = l,Ti,−j) − Yi(Tij = l ,Ti,−j)}, (2)

where l = l ∈ Tj with Tj representing the support of the randomization distribution for Tj. The expectation in Equation (2) is taken over the distribution of the other factors Ti,−j as well as the random sampling of units from the population. Thus, the AMCE averages over two sources of causal heterogeneity — heterogeneity across treatment combinations and across units. Diﬀerent treatment combinations may have distinct impacts on units with varying characteristics. Our goal is to model these potentially complex heterogeneous treatment eﬀects using an interpretable machine learning algorithm.

We propose to use a mixture of experts based on a small number of regularized logistic regressions (see Gormley and Fr¨uhwirth-Schnatter, 2019, for a recent review). The model consists of two parts. First, for each cluster, a regularized logistic regression is used to model the outcome variable as a function of treatments Ti where an ANOVA-style sum-to-zero constraint is imposed separately for each factor. Regularization is used to facilitate merging of diﬀerent levels within each factor. This modeling strategy identiﬁes a relatively small number of treatment combinations while avoiding the speciﬁcation of a baseline level for each factor (Egami and Imai, 2019). Second, we model the probability of unit i’s assignment to each cluster using a set of px unit characteristics Xi, which we refer to as “moderators.” These moderators describe the characteristics of units that belong to each cluster. All together, the proposed modeling strategy allows researchers to identify interpretable patterns of heterogeneous eﬀects across treatment combinations and units.

Formally, let K be the number of clusters. Then, the model is deﬁned as follows,

Pr(Yi = 1 | Ti,Xi) =

K

πk(Xi)ζk(Ti) (3)

k=1

where i = 1,2,...,N and for k = 1,2,...,K, we use the logistic regression to model the outcome variable and the multinomial logit model for the cluster membership,

ζk(Ti) =

exp(ψk(Ti)) 1 + exp(ψk(Ti))

exp(X i φk)

, and πk(Xi) =

. (4)

K k =1 exp(X i φk )

For identiﬁcation, we set φ1 = 0.

We use the following linear equation for ψk(Ti) where we include both main eﬀects and two-way interaction eﬀects with a common intercept µ shared across all clusters,

J

ψk(Ti) = µ +

j=1

Lj−1

J−1

1{Tij = l}βklj +

j=1 j >j

l=0

Lj −1

Lj−1

1{Tij = l,Tij = l }β klljj , (5)

l=0

l =0

for each k = 1,2,...,K where we use the following ANOVA-type sum-to-zero constraints,

Lj−1

βklj = 0, and

l=0

Lj−1

β klljj = 0, (6)

l=0

for each j,j = 1,2,...,J with j > j, and l = 0,1,...,Lj . We write these constraints compactly as,

C βk = 0 (7)

where βk is a stacked column vector containing all coeﬃcients for cluster k. Each row of C βk corresponds to one of the sum-to-zero constraints given in Equation (6). For example, in a model

without interactions, C takes the following J × Jj=1 Lj matrix,





1L1 0L2 ··· 0LJ 0L1 1L2 ··· 0Lj

, (8)

C =

... .

 

 

. .

0L1 0L2 ··· 1LJ

where 0p and 1p denote the column vectors of zeros and ones, respectively, with length p.

Given the high dimensionality of this model, we apply a sparsity-inducing penalty. In factorial experiments, it is desirable to regularize the model such that certain levels of each factor are fused together when their main eﬀects and all interactions are similar (Post and Bondell, 2013; Egami and Imai, 2019). For example, we would like to fuse levels l1 and l2 of factor j if βlj

≈ βlj

and β ljj

1

2

1l ≈ β ljj

2l for all j and l . We encourage this fusion by applying a structured sparsity approach (Goplerud, 2021) that generalizes the group and overlapping group LASSO (e.g., Yuan and Lin, 2006; Yan and Bien, 2017) by allowing positive semi-deﬁnite constraint matrices. For computational tractability, we use 2 norm instead of the ∞ norm as done in GASH-ANOVA (Post and Bondell, 2013).

To build an intuition, consider a simple example with a single cluster and two factors—factor

one has three levels and factor two has two levels. In this case, our penalty contains four terms, (β01 − β11)2 + (β0012 − β1012)2 + (β0112 − β1112)2 + (β01 − β21)2 + (β0012 − β2012)2 + (β0112 − β2112)2 + (β11 − β21)2 + (β1012 − β2012)2 + (β1112 − β2112)2 + (β02 − β12)2 + (β0012 − β0112)2 + (β1012 − β1112)2 + (β2012 − β2112)2.

(9) The ﬁrst three terms encourages the pairwise fusion of the levels of factor one whereas the fourth encourages the fusion of the levels of factor two. For compact notation, the penalty can also be written using the sum of Euclidean norms of quadratic forms where F1,F2,F3 are appropriate positive semi-deﬁnite matrices to encourage the fusion of the pairs of levels in factor one and F4 encourages the fusion of the two factors in factor two.

||β F1β||2 + ||β F2β||2 + ||β F2β||3 + ||β F2β||4, (10) where β = [β01 β11 β21 β02 β12 β0012 β1012 β2012 β0112 β1112 β2112] .

We generalize this formulation to an arbitrary number of factors and factor levels. For each factor that contains Lj levels, we have L2j penalty matrices to encourage pairwise fusion. Imposing additional constraints, e.g. for ordered factors, is a simple extension. Let G = Jj=1 L2j represent the total number of penalty matrices. For g = 1,2,...,G, we use Fg to denote a penalty matrix

such that β Fgβ is equivalent to the 2 norm on the vector of diﬀerences between all main eﬀects and interactions containing a main eﬀect.

We cast this penalty as the following Bayesian prior distribution so that our inference is based on the posterior distribution given the conditional prior on βk,

 −λπ¯kγ

 , (11)

G

p βk|{φk}Kk=2 ∝ λπ¯kγ m exp

β k Fgβk

g=1

where π¯k = Ni=1 πk(Xi)/N and m = rank([F1,··· ,FG]). Following Zahid and Tutz (2013), we use a normal prior distribution for the coeﬃcients for the moderators. The resulting regularization is invariant to the choice of baseline category φ1 = 0, which is the ﬁrst row of the K × px coeﬃcient matrix φ. The prior distribution is given by,

σφ2 2

p({φk}Kk=2) ∝ exp −

px

[φ2l,··· ,φKl] T[φ2l,··· ,φKl] , (12)

l=1

where T is a (K −1)×(K −1) matrix with Tkk = (K −1)/K if k = k and Tkk = −1/K otherwise. We set σφ2 to 1/4 for a relatively diﬀuse prior.

### 3.3 Estimation and Inference

We use the the Expectation-Maximization algorithm to maximize the log posterior density (Dempster, Laird and Rubin, 1977). We derive an AECM algorithm (Meng and van Dyk, 1997) based on a data augmentation scheme that reduces the M-Step for the treatment eﬀects to a ridge regression after using Polya-Gamma augmentation (Polson, Scott and Windle, 2013) and data augmentation on the sparsity-inducing penalty (e.g., Figueiredo, 2003; Polson and Scott, 2011; Ratkovic and Tingley, 2017; Goplerud, 2021).

Speciﬁcally, if we let Zi denote the cluster membership of unit i, we can write both the likelihood and prior as mixtures of multivariate normal distributions,

- 1

- 2


ωi 2

- 1

- 2


ψZi(Ti)2 fPG(ωi | 1,0), (13)

exp Yi −

ψZi(Ti) −

p(Yi,ωi | Zi) ∝

 

 

 

 βk

G

G

(λπ¯k)2

Fg τgk2

- 1

- 2


τgk−1 exp −

2 · τgk2 , (14) where fPG(· | b,c) represents the Polya-Gamma distribution with parameters (b,c) and Zi ∼ Multinomial(1,πi) with the kth element of π equal to πk(Xi). The linear constraints on βk given in Equation (7) still hold but are suppressed for notational simplicity. We note that the joint prior on p(βk,{τgk2 }) is guaranteed to be proper when all pairwise fusions are encouraged by {Fg}Gg=1, although in other circumstances it may be improper (Goplerud, 2021). Appendix D provides additional details.

p(βk,{τgk2 }Gg=1 | λ,{φk}) ∝ exp

−

β k





g=1

g=1

Given the above set-up, we derive the closed-form expressions for the required expectations of

1/τgk2 , ωi and Zi for the EM algorithm (see Appendix E). One challenge is the question of how to incorporate the equality constraint given in Equation (7). We resolve this by recognizing that the

constraint implies βk belongs to the null space of C. Let BC represent a basis of the null space of C . Rather than performing inference directly on βk in the constrained space, we consider unconstrained inference on the transformed parameter β˜k ∈ Rrank(C ) where β˜k = B C BC

−1 B C βk. Similarly, we re-deﬁne Fg as B C FgBC . Once we obtain an update of β˜k for each k, then we compute βk as βk = BC β ˜k.

To update the moderator parameters {φk}Kk=2, we augment the original model deﬁned in Equations (3) and (11) with the latent cluster membership Zi and apply a standard optimizer (e.g., L-BFGS-B) to the following objective function after taking its expectation with respect to Zi conditional on all observed data and the current parameter values,

  + p({φk}Kk=2) (15)

 mγ ln(¯πk) − λπ¯kγ

K

N

K

G

1{Zi = k}ln(πk(Xi)) +

β k Fgβk

g=1

i=1

k=1

k=1

where πk(Xi) and π¯k = Ni=1 πk(Xi)/N are functions of φk. Note that if γ = 0, this simpliﬁes to a (weighted) multinomial regression with E(zik) as the outcome.

Appendix E also discusses some additional details on our EM algorithm including initialization and techniques to accelerate convergence. For our empirical application, we extend the above model and estimation algorithm to accommodate (1) repeated observations for each individual respondent, (2) a forced choice conjoint design, (3) survey weights, and (4) adaptive weights for the sparsityinducing penalty. Appendix F gives details of these extensions. Lastly, our experience suggests that our penalty function, which consists of overlapping groups, often ﬁnds highly sparse solutions. To address this problem, Appendix F shows how to integrate the latent overlapping group formulation of Yan and Bien (2017) into our framework so that the main eﬀects are duplicated and then penalized without the interactions.

Fitting the proposed model is computationally expensive, so we use an information criterion approach, rather than cross validation, to select the value of the regularization parameter λ (Khalili and Chen, 2007; Khalili, 2010; Chamroukhi and Huynh, 2019). Appendix E presents the details of our degrees-of-freedom estimation, and here we provide a brief overview. We proceed using a two-step process. First, for any two factor levels that are suﬃciently close (e.g. β k Fgβk < 10−4), we assume they are fused together and consider it as an additional linear constraint on the parameter vector βk. Second, given that assumed fusion, we calculate the degrees of freedom on the unconstrained parameters {µ,{β˜k}Kk=1} by noting that each M-step of the EM update for these parameters is a

ridge regression given expected cluster memberships and Polya-Gamma weights. Thus, following the idea of Oelker and Tutz (2017), we compute the implied hat matrix from this update and use its trace as the degrees of freedom. We ﬁnally adjust upwards the degrees of freedom by the number of moderator coeﬃcients (e.g., Khalili 2010; Chamroukhi and Huynh 2019). We use this to calculate the BIC of the model given the value of the regularization parameter (λ) obtained based on Bayesian model-based optimization (mlrMBO; Bischl et al. 2018).

Finally, to quantify the uncertainty in the parameter estimates, we rely on a quadratic approximation to the log posterior distribution. To ensure its diﬀerentiability, we follow a standard approach of regularized regression (e.g., Fan and Li, 2001) and again fuse pairwise factor levels that are suﬃciently close together. We assume these restrictions are binding and conduct inference on the transformed parameters in the constrained space and estimate their variance-covariate matrix. The Hessian of the log posterior distribution can be computed in closed form using the method of Louis (1982) as shown in Appendix G. Given these results, the Delta method can be used to derive the standard errors for various quantities of interest.

## 4 Empirical Analysis

In this section, we re-analyze data from Hainmueller and Hopkins (2015) using our methodology. We ﬁnd evidence of eﬀect heterogeneity for immigrant choice based on respondents traits. In particular, we consistently ﬁnd that the immigrant’s country of origin plays a greater role in forming the immigration preference of respondents with increased prejudice, as measured by a hispanic prejudice score. However, outside of this cluster, which accounts for about one third or more of the respondents, the country of origin factor plays a much smaller role. In addition, we ﬁnd some interaction eﬀects among factors but their magnitude is too small to be meaningful.

### 4.1 Data and Model

Following the original analysis, in addition to dummy variables for each factor, we also include interactions between country and reason of application factors as well as education and job factors to account for the restricted randomization based on those factors. We additionally include interactions between country and job as well as those between country and education, in accordance with the skill premium theory of Newman and Malhotra (2019), which hypothesizes that prejudiced individuals prefer highly skilled immigrants only for certain immigrant countries. This results in a total of 41 main eﬀect and 222 interaction eﬀect coeﬃcients for each cluster.

For modeling cluster membership, we include the respondents’ political party, education, demographics of their ZIP code (we follow the original analysis and include the variables indicating

whether respondents’ ZIP code had few immigrants (< 5%) and for those from ZIPs with > 5% foreign-born, and whether the majority were from Latin America), and Hispanic prejudice score. The Hispanic prejudice score was used by Newman and Malhotra (2019), though we negate it to make lower values correspond to lower prejudice. The score is based on a standardized (and negated) feeling thermometer for Hispanics. The score ranges from −1.62 to 2.11 for our sample, where higher scores indicate higher levels of prejudice.

We analyze the subset of the data that contain only white respondents. After removing entries with missing data, we have the sample of 888 respondents. Most respondents evaluated ﬁve pairs of proﬁles, though four respondents have fewer responses in the data set used. The total number of observations is 8,866 or 4,433 pairs of proﬁles. We incorporate the survey weights into our analysis.

The original conjoint experiment was conducted using the forced choice design, in which a pair of immigrant proﬁles are presented and a respondent is asked to choose one of them. To accommodate this design, we follow Egami and Imai (2019) and slightly modify the model speciﬁcation. In particular, we model the choice as a function of diﬀerences in treatments as follows,

J

βklj 1 TijL = l − 1 TijR = l

ψk(TiL,TiR) = µ +

j=1 l∈Lj

J−1

β klljj 1 TijL = l,TijL = l − 1 TijR = l,TijR = l ,

+

j=1 j >j l∈Lj l ∈Lj

(16)

where TiL and TiR represent the factors for the left and right proﬁles. The outcome variable Yi is equal to 1 if the left proﬁle is selected and is equal to 0 if the right proﬁle is chosen. With this new linear predictor formulation, the estimation and inference proceed as explained in Section 3.

We conduct the two analyses, one with two clusters and the other with three clusters. These two models perform equally well in terms of out-of-sample classiﬁcation. Using more than three clusters does not appear to give signiﬁcantly improved substantive insights or provide any improvement in model performance. For each analysis, we use Bayesian information criterion (BIC) to choose the value of regularization parameter λ.

### 4.2 Findings

We focus on the AMCE for each factor as the primary quantity of interest and separately estimate it for each cluster. Under our modeling strategy for the forced choice design, the AMCE of level l versus level l of factor j within cluster k can be written as,

δjk(l,l ) =

- 1

- 2


E Pr Yi = 1 | Zi = k,TijL = l,Ti,L−j,TiR − Pr Yi = 1 | Zi = k,TijL = l ,Ti,L−j,TiR

+ Pr Yi = 0 | Zi = k,TijR = l,Ti,R−j,TiL − Pr Yi = 0 | Zi = k,TijR = l ,Ti,R−j,TiL .

Cluster 1: 50.3% Cluster 2: 49.7%

Cluster 1: 33.7% Cluster 2: 32.3% Cluster 3: 34%

| | | | |
|---|---|---|---|
| | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |


| | | | | |
|---|---|---|---|---|
| | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


Iraq

Iraq

Somalia

Somalia

Sudan

Sudan

China

China

India

India

Country

Country

Poland

Poland

Philippines

Philippines

Mexico

Mexico

France

France

Germany

Germany

| | | | | | |
|---|---|---|---|---|---|
| | | | | | |


| | | | | |
|---|---|---|---|---|
| | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | |
|---|---|---|---|---|---|
| | | | | | |


Grad degree

Grad degree

College

College

2 year college

2 year college

Education

High school

Education

High school

Grade 8

Grade 8

Grade 4

Grade 4

No formal

No formal

| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


Male

Male

Gender

Gender

Female

Female

| | | | | |
|---|---|---|---|---|
| | | | | |


| | | | | | |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |


| | | | |
|---|---|---|---|
| | | | |


| | | | | | |
|---|---|---|---|---|---|
| | | | | | |


Doctor

Doctor

Research scientist

Research scientist

Nurse

Nurse

Computer programmer

Computer programmer

Teacher

Teacher

Factor

Factor

Job

Construction worker

Job

Construction worker

Financial analyst

Financial analyst

Gardener

Gardener

Child care provider

Child care provider

Waiter

Waiter

Janitor

Janitor

| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | |
|---|---|---|---|---|---|
| | | | | | |


>5 years

>5 years

3−5 years

3−5 years

Job exp

Job exp

1−2 years

1−2 years

None

None

| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | |
|---|---|---|---|---|
| | | | | |


| | | | | | |
|---|---|---|---|---|---|
| | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


Interpreter

Interpreter

Unable

Unable

Language

Language

Broken

Broken

Fluent

Fluent

| | | | | | |
|---|---|---|---|---|---|
| | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | |
|---|---|---|---|---|---|
| | | | | | |


No plans

No plans

Will look after arrival

Will look after arrival

Plans

Plans

No contract, had interviews

No contract, had interviews

Has contract

Has contract

| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |


Persecution

Persecution

Reason

Job

Reason

Job

Family

Family

| | | | | | |
|---|---|---|---|---|---|
| | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |


Entered illegally once

Entered illegally once

6 months with family

6 months with family

Trips

Multiple times with visa

Trips

Multiple times with visa

Once with visa

Once with visa

Never been

Never been

−0.4−0.2 0.0 0.2 −0.4−0.2 0.0 0.2

−0.4−0.2 0.0 0.2 −0.4−0.2 0.0 0.2 −0.4−0.2 0.0 0.2

Effect

Effect

- Figure 2: Estimated average marginal component eﬀects using a two-cluster (left) and three-cluster (right) analysis. The point estimates and 95% conﬁdence intervals are shown. A solid circle represents the baseline level of each factor. Number after colon give posterior predictive probability for each cluster, over normalized survey weights.


That is, we compute the AMCE separately for the left and right proﬁles and then average them to obtain the overall AMCE. We estimate this quantity using the ﬁtted model and averaging over the empirical distribution of the factorial treatments.

Figure 2 presents the estimated AMCEs and their 95% conﬁdence intervals for the two-cluster and three-cluster analyses in the left and right panels, respectively. In both analyses, Cluster 1 displays stronger impacts of country of origin than the other clusters. The respondents in Cluster 1 give the most preference to immigrants from Germany and the least preference to immigrants from Iraq (followed by Somalia and Sudan). The patterns we observe for the other factors are also similar for Cluster 1 between the two analyses. The respondents in Cluster 1 prefer educated, experienced, and skilled immigrants.

Language ability also has particularly strong eﬀects in Cluster 1 of both analyses, with ﬂuent immigrants being most preferred and those who need an interpreter or are unable to speak English

2 cluster analysis 3 cluster analysis

| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |


2 cluster analysis 3 cluster analysis

Few immigrants

ZIP diversityParty IDEducation

Many immigrants, majority Hisp

1

Many immigrants, majority not Hisp

Respondent characteristics

| | | | | |
|---|---|---|---|---|


Strong Democrat

Cluster number

Not strong Democrat

Cluster number

Leans Democrat

- 1
- 2
- 3


Undecided/Indep/Other

2

Leans Republican

Not strong Republican

Strong Republican

| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |


Bachelor's or higher

Some college

3

High school

< High school

−1 0 1 2 −1 0 1 2

0.0 0.2 0.4 0.6 0.0 0.2 0.4 0.6

Hispanic prejudice score

Proportion

- Figure 3: Distribution of respondent characteristics for each cluster. Left set of plots show weighted box plot showing distribution of the hispanic prejudice moderator within each cluster over the posterior predictive distribution and survey weight distribution using a two-cluster (left) and threecluster (right) analysis. Right set of plots show the distribution of categorical moderators within each cluster over the posterior predictive distribution and survey weight distribution using a twocluster (left) and three-cluster (right) analysis.


being least preferred. In addition, these respondents prefer immigrants who already have contracts over those who have no contracts or plans. One diﬀerence between the two analyses is that a strong negative eﬀect of illegal immigration appears in Cluster 1 for the two-cluster analysis, but no such eﬀect is present for Cluster 1 of the three-cluster analysis. Instead, both Clusters 2 and 3 exhibit a strong negative eﬀect of illegal immigration.

For the two-cluster analysis, the respondents in Cluster 2 do not care much about immigrant’s country of origin. Instead, they place a greater emphasis on education, reason for immigration, and legality when compared to those in Cluster 1. Preferences towards immigrants with job experience, language ﬂuency, and work plans are similar between the two clusters. For the three-cluster analysis, Clusters 2 and 3 together correspond roughly to Cluster 2 of the two-cluster analysis. In fact, more than 85% of the respondents who belong to Cluster 2 of the two-cluster analysis are the members of either Cluster 2 or 3 in the three-cluster analysis. The diﬀerences between Clusters 2 and 3 are substantively small, but those in Cluster 3 appear to place more emphasis on job experiences.

Who belongs to each cluster? The left panel of Figure 3 shows the distribution of hispanic prejudice score for each cluster weighted by the corresponding posterior cluster membership probability

and the survey weight for each individual respondent. The plot shows that for both two-cluster and three-cluster analyses, those with high prejudice score are much more likely to be part of Cluster 1. This is consistent with the ﬁnding above that the respondents in Cluster 1 tend to put more emphasis on immigrant’s country of origin. The right panel of the ﬁgure shows the distribution of other respondent characteristics. In general, Cluster 1 consists of those who live in ZIP code with few immigrants, are Republicans, and are less educated. For the three-cluster analysis, those in Cluster 3 are similar in their characteristics to those in Cluster 1 except that the latter are much more prejudiced than the former.

What respondent characteristics are predictive of the cluster membership? We examine how the predicted probabilities of cluster memberships change across respondents with diﬀerent characteristics. Speciﬁcally, we estimate

E[πk(Xij = x1,Xi,−j) − πk(Xij = x0,Xi,−j)] (17)

where x0 and x1 are diﬀerent values of covariate of interest Xij. If Xij is a categorical variable, we set x0 to the baseline level and x1 to the level indicated on the vertical axis. If Xij is a continuous variable as in the case of the hispanic prejudice score, then x0 and x1 represent the 25th and 75th percentile values. The solid arrows represent whether the corresponding 95% conﬁdence interval covers zero or not.

Consistent with the earlier ﬁndings, Figure 4 shows that those with high hispanic prejudice scores are predicted to belong to Cluster 1 even after controlling for other factors. These respondents are also less likely to belong to Cluster 2 in the three-cluster analysis. For the two-cluster analysis, party ID appears to play a statistically signiﬁcant role with Republicans having a tendency to belong to Cluster 1. The three-cluster analysis, however, suggests that the diﬀerences between Clusters 2 and

- 3 can be explained by partisanship and education. Cluster 2 tend to have highly educated and Democratic respondents when compared to those who belong to Cluster 3.


Finally, we estimate the average marginal interaction eﬀects (AMIE) between two factors (Egami and Imai, 2019), which can be computed by subtracting the two AMCEs from the average eﬀect of changing the two factors of interest at the same time. Thus, the AMIE represents the additional eﬀect of changing the two factors beyond the sum of the average eﬀects of changing one of the factors alone. Formally, we can deﬁne the AMIE of changing factors j and j from levels lj and lj to levels l j and l j , respectively, as follows,

E{Yi(Tij = lj,Tij = lj ,Ti,−j,−j ) − Yi(Tij = l j,Tij = l j ,Ti,−j,−j )} − δj(lj,l j) − δj (lj ,l j ). As shown in Figure 5, we ﬁnd interaction eﬀects between country and job for Cluster 1 in both

2 clusters Cluster 1

2 clusters Cluster 2

3 clusters Cluster 1

3 clusters Cluster 2

3 clusters Cluster 3

| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |


| | | | | | | | |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |


| | | | | | |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |


| | | | | | | |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |
| | | | | | | |


| | | | | | | | |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |


Hispanic prejudice scale

ZIP(Few immigrants)

ZIP(Many immigrants, majority Hisp)

Ed(Bachelor's or higher)

Ed(Some college)

Covariate

Ed(High school)

Party ID(Strong Democrat)

Party ID(Not strong Democrat)

Party ID(Leans Democrat)

Party ID(Undecided/Indep/Other)

Party ID(Leans Republican)

Party ID(Not strong Republican)

0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8 0.2 0.4 0.6 0.8

Posterior Predictive Probability of Cluster Membership

- Figure 4: The impact of moderator values on likelihood of being assigned to clusters, for two-cluster (left two plots) and three-cluster (right three plots) analysis.

analyses. The eﬀect sizes are quite small, but the estimated eﬀects are consistent with the skill premium hypothesis of Newman and Malhotra (2019). In particular, it appears that individuals who hold higher prejudice (those in Cluster 1), do enforce a skill premium for individuals from Iraq in terms of job, slightly preferring Iraqi immigrants with high skilled jobs, whereas immigrants from Germany show lower preference for high-skilled jobs such as doctor. Interactions among other factors were found to be even smaller in magnitude, and therefore are not displayed.

- 5 Concluding Remarks


We have shown that a mixture of regularized regressions can be eﬀectively used to estimate heterogeneous treatment eﬀects of high-dimensional treatments. The proposed approach yields interpretable results, illuminating how diﬀerent sets of treatments have heterogeneous impacts on distinct groups of units. We applied our methodology to conjoint analysis, which is a popular survey experiment in marketing and social sciences. Our analysis shows that individuals with high prejudice score tend

Cluster 1 Cluster 2

Cluster 1 Cluster 2 Cluster 3

| |
|---|


| |
|---|


Doctor

Doctor

Research scientist

Research scientist

Nurse

Nurse

AMIE

Computer programmer

Computer programmer

![image 1](goplerud-imai-pashley-2025-heterogeneous-conjoint_images/imageFile1.png)

Teacher

Teacher

0.000

Job

Job

−0.005

Construction worker

Construction worker

−0.010

Financial analyst

Financial analyst

−0.015

Gardener

Gardener

−0.020

Child care provider

Child care provider

Waiter

Waiter

Janitor

Janitor

Poland

Iraq

Poland

Iraq

Poland

Iraq

Poland

Iraq

Poland

Iraq

Philippines

Philippines

Philippines

Philippines

Philippines

Mexico

Mexico

Mexico

Mexico

Mexico

India

India

India

India

India

Sudan

Sudan

Sudan

Sudan

Sudan

Germany

France

China

Somalia

Germany

France

China

Somalia

Germany

France

China

Somalia

Germany

France

China

Somalia

Germany

France

China

Somalia

Country

Country

Figure 5: Estimated average marginal interaction eﬀects (AMIEs) for the two-cluster (right) and three cluster (left) analysis between country and job. The interaction eﬀects are detected only for Cluster 1 of both analyses, but their magnitude is small.

to discriminate against immigrants from certain non-European countries. These individuals tend to be Republicans, less educated, and live in areas with few immigrants. Future research should consider the derivation of optimal treatment rules in this setting as well as the empirical evaluation of such rules. Another important research agenda is the estimation of heterogeneous eﬀects of high-dimensional treatments in observational studies.

## References

Andrews, Rick L, Andrew Ainslie and Imran S Currim. 2002. “An empirical comparison of logit choice models with discrete versus continuous representations of heterogeneity.” Journal of Marketing Research 39:479–487.

Athey, Susan and Guido Imbens. 2016. “Recursive Partitioning for Heterogeneous Causal Eﬀects.” Proceedings of the National Academy of Sciences 113:7353–7360.

Bischl, Bernd, Jakob Richter, Jakob Bossek, Daniel Horn, Janek Thomas and Michel Lang. 2018. “mlrMBO: A Modular Framework for Model-Based Optimization of Expensive Black-Box Functions.”.

Bondell, Howard D. and Brian J. Reich. 2009. “Simultaneous Factor Selection and Collapsing Levels in ANOVA.” Biometrics 65:169–177.

Chamroukhi, Faicel and Bao-Tuyen Huynh. 2019. “Regularized maximum likelihood estimation and feature selection in mixtures-of-experts models.” Journal de la soci´et´e fran¸aise de statistique 160:57–85.

Chernozhukov, Victor, Mert Demirer, Esther Duﬂo and Ivan Fernandez-Val. 2019. Generic Machine Learning Inference on Heterogeneous Treatment Eﬀects in Randomized Experiments. Technical Report. arXiv:1712.04802.

Dasgupta, Tirthankar, Natesh S. Pillai and Donald B. Rubin. 2015. “Causal inference from 2K factorial designs by using potential outcomes.” Journal of the Royal Statistical Society. Series B (Statistical Methodology) 77:727–753.

Dempster, Arthur P., Nan M. Laird and Donald B. Rubin. 1977. “Maximum Likelihood from Incomplete Data Via the EM Algorithm (with Discussion).” Journal of the Royal Statistical Society, Series B, Methodological 39:1–37.

Egami, Naoki and Kosuke Imai. 2019. “Causal Interaction in Factorial Experiments: Application to Conjoint Analysis.” Journal of the American Statistical Association 114:529–540.

Fan, Jianqing and Runze Li. 2001. “Variable selection via nonconcave penalized likelihood and its oracle properties.” Journal of the American statistical Association 96:1348–1360.

Figueiredo, M´rio A.T. 2003. “Adaptive Sparseness for Supervised Learning.” IEEE Transactions on Pattern Analysis and Machine Intelligence 25:1150–1159.

Goplerud, Max. 2021. “Modelling Heterogeneity Using Bayesian Structured Sparsity.” arxiv preprint 2103.15919.

Gormley, Isobel Claire and Sylvia Fru¨hwirth-Schnatter. 2019. “Mixture of experts models.” In Handbook of Mixture Analysis, ed. Sylvia Fru¨hwirth-Schnatter, Gilles Celeux and Christian P. Robert. Chapman and Hall/CRC pp. 271–307.

Grimmer, Justin, Solomon Messing and Sean J. Westwood. 2017. “Estimating Heterogeneous Treatment Eﬀects and the Eﬀects of Heterogeneous Treatments with Ensemble Methods.” Political Analysis 25:413–434.

Gupta, Sachin and Pradeep K Chintagunta. 1994. “On using demographic variables to determine segment membership in logit mixture models.” Journal of Marketing Research 31:128–136.

Hahn, P. Richard, Jared S. Murray and Carlos M. Carvalho. 2020. “Bayesian regression tree models for causal inference: regularization, confounding, and heterogeneous eﬀects.” Bayesian Analysis 15:965–1056.

Hainmueller, Jens and Daniel J Hopkins. 2015. “The hidden American immigration consensus: A conjoint analysis of attitudes toward immigrants.” American Journal of Political Science 59:529– 548.

Hainmueller, Jens, Daniel J Hopkins and Teppei Yamamoto. 2014. “Causal inference in conjoint analysis: Understanding multidimensional choices via stated preference experiments.” Political analysis 22:1–30.

Imai, Kosuke and Aaron Strauss. 2011. “Estimation of Heterogeneous Treatment Eﬀects from Randomized Experiments, with Application to the Optimal Planning of the Get-out-the-vote Campaign.” Political Analysis 19:1–19.

Imai, Kosuke and Marc Ratkovic. 2013. “Estimating Treatment Eﬀect Heterogeneity in Randomized Program Evaluation.” Annals of Applied Statistics 7:443–470.

Imai, Kosuke and Michael Lingzhi Li. 2021. “Experimental Evaluation of Individualized Treatment Rules.” Journal of the American Statistical Association.

Khalili, Abbas. 2010. “New estimation and feature selection methods in mixture-of-experts models.” Canadian Journal of Statistics 38:519–539.

Khalili, Abbas and Jiahua Chen. 2007. “Variable Selection in Finite Mixture of Regression Models.” Journal of the American Statistical Association 102:1025–1038.

Ku¨nzel, S¨ren R., Jasjeet S. Sekhon, Peter J. Bickel and Bin Yu. 2018. Meta-learners for Estimating Heterogeneous Treatment Eﬀects using Machine Learning. Technical Report. arXiv:1706.03461.

Louis, Thomas A. 1982. “Finding the Observed Information Matrix When Using the EM Algorithm.” Journal of the Royal Statistical Society, Series B, Methodological 44:226–233.

Meng, Xiao-Li and David A. van Dyk. 1997. “The EM Algorithm – an Old Folk Song Sung to a Fast New Tune (with Discussion).” Journal of the Royal Statistical Society, Series B, Methodological 59:511–567.

Newman, Benjamin J and Neil Malhotra. 2019. “Economic reasoning with a racial hue: Is the immigration consensus purely race neutral?” The Journal of Politics 81:153–166.

Oelker, Margret-Ruth and Gerhard Tutz. 2017. “A uniform framework for the combination of penalties in generalized structured models.” Advances in Data Analysis and Classiﬁcation 11:97– 120.

Polson, Nicholas G., James G. Scott and Jesse Windle. 2013. “Bayesian Inference for Logistic Models Using P´lya–Gamma Latent Variables.” Journal of the American Statistical Association 108:1339–1349.

Polson, Nicholas G. and Steve L. Scott. 2011. “Data Augmentation for Support Vector Machines.” Bayesian Analysis 6:1–24.

Post, Justin B. and Howard D. Bondell. 2013. “Factor Selection and Structural Identiﬁcation in the Interaction ANOVA Model.” Biometrics 69:70–79.

Rao, Vithala R. 2014. Applied Conjoint Analysis. Berlin Heidelberg: Springer.

Ratkovic, Marc and Dustin Tingley. 2017. “Sparse Estimation and Uncertainty with Application to Subgroup Analysis.” Political Analysis 25:1–40.

Rubin, Donald B. 1980. “Randomization Analysis of Experimental Data: The Fisher Randomization Test Comment.” Journal of the American Statistical Association 75:591–593.

Sta¨dler, Nicolas, Peter Bu¨hlmann and Sara Van De Geer. 2010. “ -1-penalization for mixture regression models.” Test 19:209–256.

Stokell, Benjamin G., Rajen D. Shah and Ryan J. Tibshirani. 2021. “Modelling High-Dimensional Categorical Data Using Nonconvex Fusion Penalties.”.

Tian, Lu, Ash A. Slizadeh, Andrew J. Gentles and Robert Tibshirani. 2014. “A Simple Method for Estimating Interactions Between a Treatment and a Large Number of Covariates.” Journal of the American Statistical Association 109:1517–1532.

van der Laan, Mark J. and Sheri Rose. 2011. Targeted Learning: Causal Inference for Observational and Experimental Data. Springer.

Varadhan, Ravi and Christophe Roland. 2008. “Simple and globally convergent methods for accelerating the convergence of any EM algorithm.” Scandinavian Journal of Statistics 35:335–353.

Wager, Stefan and Susan Athey. 2018. “Estimation and Inference of Heterogeneous Treatment Eﬀects using Random Forests.” Journal of the American Statistical Association 113:1228–1242.

Yan, Xiaohan and Jacob Bien. 2017. “Hierarchical sparse modeling: A choice of two group lasso formulations.” Statistical Science 32:531–560.

Yuan, Ming and Yi Lin. 2006. “Model selection and estimation in regression with grouped variables.” Journal of the Royal Statistical Society: Series B (Statistical Methodology) 68:49–67.

Zahid, Faisal Maqbool and Gerhard Tutz. 2013. “Ridge estimation for multinomial logit models with symmetric side constraints.” Computational Statistics 28:1017–1034.

