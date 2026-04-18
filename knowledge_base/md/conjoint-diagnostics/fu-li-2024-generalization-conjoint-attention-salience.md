### arXiv:2405.06779v4[econ.EM]14 Apr 2026

## A Formal Theory of Survey Experiment Generalizability: Attention and Salience*

Jiawei Fu† Xiaojun Li‡ April 15, 2026

Abstract

Survey experiments are widely used to identify causal effects in political science and the social sciences. Yet researchers are typically interested in more than the internal validity of an experimentally induced contrast. They also want to know whether the estimated effect corresponds to the effect in the real world. We develop a formal theory of survey experiment generalizability grounded in behavioral microfoundations. The theory highlights two mechanisms. First, the survey environment shapes attention: it determines which considerations enter the respondent’s active consideration set. Second, it shapes salience: conditional on consideration, it influences the relative weight assigned to those considerations. This framework yields two main results. Consideration-set compression generates amplification: survey-experimental effects can be larger in magnitude than their real-world counterparts, even for the same individuals, treatment content, and outcome. Context-dependent salience generates sign instability: the direction of the survey effect need not coincide with the direction of the corresponding realworld effect. The theory clarifies what survey experiments identify, when those effects are likely to generalize, and how survey designs can be modified to improve decision-environment transportability.

Keywords: Survey Experiment, External Validity, Generalizability, Attention, Salience.

*We thank Donald Green, Melody Huang, John Marshall, Cyrus Samii, Tara Slough, and Anton Strezhnev ; Participants at Experiment Conference at New York University, Center for Data Science of Renmin University of China, Polmeth and MPSA 2024. We also thank Raymond Liu for his excellent research assistance.

†Assistant Professor, Duke University jiawei.fu@duke.edu ‡Professor of Political Science, University of British Columbia xiaojun.li@ubc.ca

#### Introduction

Survey experiments are a core empirical tool in political science and the broader social sciences. Researchers use them to study candidate choice, policy support, accountability, punishment, among other outcomes (Eggers, Vivyan and Wagner, 2018; Carnes and Lupu, 2016; Sanbonmatsu, 2002). Because treatment is randomized, survey experiments are widely regarded as providing credible causal evidence. Between 2021 and 2025, a total of 204 survey experiments were published in leading political science journals, as shown in Table 1. Following the classification proposed by EGAP, we categorize these studies into five types: conjoint, endorsement, list, priming, and vignette/factorial.1 Figure 1 presents the distribution of these categories over time. Among them, vignette/factorial and conjoint designs are the two dominant approaches.

However, in most substantive applications, internal validity is not the end of the story. Researchers are often interested in a stronger claim: how the same information, attribute, or intervention would operate in real-world environments beyond the survey setting. For example, a candidate trait that shifts support in a conjoint experiment is often interpreted as evidence of how voters would weigh that trait in actual elections. Similarly, a corruption message that affects respondents’ evaluations in a vignette is often taken to reflect how such information would influence real-world political judgments. Survey experiments are often viewed as a powerful tool for learning about real-world effects (Gaines, Kuklinski and Quirk, 2007). Yet, under what conditions is such generalizability warranted? More fundamentally, what mechanisms determine whether findings from survey experiments successfully translate to real-world behavior, and when might they fail to do so?

In this study, we develop a formal framework that integrates a behavioral model with the potential outcomes framework to characterize two mechanisms that shape the generalizability of survey experiments. In the existing literature, generalizability and external validity are typically understood as the ability to make inferences about a broader population (Findley, Kikuta and Denly, 2021). By contrast, we take a more fundamental step by asking: even when we fix the same indi-

1https://egap.org/resource/10-things-to-know-about-survey-experiments/

![image 1](fu-li-2024-generalization-conjoint-attention-salience_images/imageFile1.png)

Figure 1: Distribution of Survey Experiments in AJPS, APSR, JOP, PA Table 1: Survey experiments by journal and subtype from 2012 to 2015

Journal Total Conjoint Endorsement List Priming Vignette/Factorial American Journal of Political Science 41 14 2 1 8 20 American Political Science Review 55 16 0 6 12 27 Political Analysis 9 8 0 1 1 0 The Journal of Politics 99 33 2 4 24 55 Total 204 71 4 12 45 102

Note: Subtype counts are not mutually exclusive because some papers have more than one survey experiment subtypes.

vidual, the same treatment, and the same outcome measure, does the effect estimated in a survey experiment inform the corresponding real-world effect? If the answer is negative, then concerns about generalizing survey experimental results to other populations become secondary.

More specifically, following Egami and Hartman (2023), we focus on two dimensions of generalizability: effect magnitude and effect sign. Effect magnitude generalization requires that the size of the estimated effect in the survey experiment corresponds to its magnitude in the real world. Effect sign generalization, by contrast, requires only that the direction (positive or negative) of the effect is preserved across settings. Importantly, an experiment need not satisfy both criteria simultaneously; the relevant notion of generalizability depends on the researcher’s objective. For example, policy evaluations often require accurate estimates of effect magnitudes to assess welfare

implications, and thus demand magnitude consistency. In contrast, when experiments are used to test predictions derived from formal theory, preserving the direction of the effect is often sufficient. In some cases, experimental designs may even deliberately amplify treatment variation to increase statistical power, making sign consistency the more appropriate benchmark.

Building on our model, we characterize two mechanisms that govern the generalizability of both effect magnitude and effect sign. These mechanisms rest on two behavioral microfoundations.

The first is limited attention. Conventional models of decision-making typically assume that individuals possess unlimited attention—that is, they account for all relevant attributes when making choices. While such assumptions yield tractable and often sharp theoretical predictions, they have been increasingly challenged by empirical anomalies. Classic examples include the paradoxes documented by Allais (1953) and Ellsberg (1961), which illustrate systematic violations of expected utility theory.2 In practice, individuals rarely process all potentially relevant considerations. Instead, they rely on a selective and context-dependent consideration set. This notion has long been recognized in the social sciences. For example, consumer choices may favor option y in the presence of x, yet this preference can reverse when x is not readily available (Masatlioglu, Nakajima and Ozbay, 2016). We incorporate this idea into the causal inference framework for survey experiments and show that differences in consideration sets across environments play a central role in shaping generalizability. In particular, the more restricted consideration sets typically induced by survey environments can mechanically amplify estimated effects relative to their real-world counterparts.

The second mechanism arises from salience. Even within a given consideration set, attributes are not weighted equally; some dimensions attract disproportionate attention. This phenomenon is well documented. For instance, Chetty, Looney and Kroft (2009) show that consumers underreact to taxes when tax-inclusive prices are not prominently displayed, but reduce demand by approximately eight percent when such prices are made salient. To formalize this mechanism, we draw on the psychologically grounded model of choice developed by Bordalo, Gennaioli and Shleifer

2The former shows that individuals frequently violate the independence axiom of expected utility theory, while the latter demonstrates ambiguity aversion inconsistent with subjective expected utility theory.

(2012, 2013), in which decision weights are distorted by the relative salience of attributes. We show that salience, when combined with limited attention, can generate failures of effect sign generalization. The key intuition is that salience distorts the relative weighting of attributes, effectively inducing correlations among them in the decision process. When consideration sets differ between survey and real-world environments, these salience-driven distortions operate on different subsets of attributes, potentially reversing the direction of the estimated effect.

Although the core components of our theory—consideration sets and salience—are not directly observable, we assess the empirical relevance of our framework by deriving a set of testable implications from the theoretical results. A central prediction is that the estimated effect attenuates, and may even reverse, as the number of attributes increases in some experiments. Intuitively, expanding the attribute space alters both the consideration set and the relative salience of each attribute, thereby changing the mapping from experimental effects to their real-world counterparts. We examine this prediction using data from multiple existing studies and supplement the analysis with additional pre-registered conjoint experiments.3 As the well-known adage suggests, “all models are wrong, but some are useful.” We do not claim that our framework exhausts all mechanisms underlying the empirical patterns we document. Rather, our goal is to isolate two theoretically grounded mechanisms—limited attention and salience—and to show that they generate distinctive, testable predictions.

Attention and salience have already emerged as important considerations in the study of conjoint experiments. For example, Jenke et al. (2021) and Bansak and Jenke (2025) employ eyetracking techniques to examine how respondents allocate attention across attributes. We build on this line of work by providing a formal framework that characterizes the conditions under which such patterns arise and how they affect causal interpretation. We emphasize that the definitions of attention and salience are quite versatile in the literature. Here, we define limited attention as a situation in which only a subset of attributes is under consideration, and we define salience as the extent to which the value of an attribute affects its importance. These definitions follow the

3The study is pre-registered and approved by the authors’ Institutional Review Board; further details are provided in the SI B.

framework of Bordalo, Gennaioli and Shleifer (2012). This idea is closely related to the concept of extremity (Liu and Latan´e, 1998; Abelson, 2014; Krosnick and Abelson, 1992).

More broadly, our results suggest that, among survey-based designs, well-constructed conjoint experiments may offer advantages for generalizability. By presenting multiple attributes simultaneously, conjoint designs encourage respondents to consider a richer set of factors, thereby mitigating distortions induced by limited attention and salience. When the set of attributes included in the experiment sufficiently captures the core and relevant dimensions of real-world decision-making, concerns about generalizability are correspondingly reduced. This perspective helps rationalize prior empirical findings documenting the robustness of conjoint experiments (Jenke et al., 2021; Hainmueller, Hangartner and Yamamoto, 2015; Bansak et al., 2018, 2021), and provides a microfoundation for understanding when such robustness should be expected.

Our research intersects with and contributes to several important strands of literature. At its core, our study engages with a central question in the literature on external validity (Barabas and Jerit 2010; List and Levitt 2005; Gaines, Kuklinski and Quirk 2007), particularly the external validity of survey experiments. Slough and Tyson (2023, 2024) develop a formal framework to clarify external validity by identifying conditions under which different studies are target-equivalent and target-congruent. Their framework emphasizes the importance of harmonizing studies along key dimensions, including treatment, control, and outcome measurement. Similarly, Egami and Hartman (2023) propose a unified framework encompassing multiple dimensions of external validity—population, context, treatment, and outcome—building on the typology of Cook, Campbell and Shadish (2002). They further develop estimators for both effect magnitude and sign generalization. We complement this literature by providing a behavioral foundation for understanding when and why effect magnitude and sign generalization succeed or fail.

Much of this literature focuses on generalizing results to new populations (Mullinix et al. 2015; Huang 2022). By contrast, our paper examines a more fundamental form of external validity: the consistency between experimental effects and real-world effects, even when holding fixed the same individuals, treatments, and outcomes. A variety of factors may undermine such consistency,

including well-known phenomena such as the Hawthorne effect (Adair, 1984). We contribute to this literature by providing a new explanation tailored to settings involving multidimensional decision-making.

More specifically, concerns about the generalizability of survey experiments have been widely documented, with mixed empirical evidence (Barabas and Jerit, 2010; Findley et al., 2017; Hainmueller, Hangartner and Yamamoto, 2014). Existing explanations for threats to external validity include features of experimental design (De Mesquita and Tyson, 2020) and information (non)equivalence across settings (Dafoe, Zhang and Caughey, 2018). Departing from purely statistical approaches, we develop a behavioral framework that highlights the roles of limited attention and salience as key mechanisms underlying these discrepancies.

Our work also contributes to the emerging literature on the Theoretical Implications of Empirical Methods (TIEM) (Fu and Slough, 2026; Slough and Tyson, 2023; De Mesquita and Tyson, 2020; Slough, 2023), which evaluates empirical methodologies through the lens of formal theory. In contrast to the Empirical Implications of Theoretical Models (EITM) approach, TIEM emphasizes how methodological choices themselves embed implicit theoretical assumptions. Within this perspective, our application of decision theory and behavioral economics to survey experiments reveals systematic discrepancies between experimental estimates and real-world effects, extending beyond the aggregate-level inconsistencies documented by Abramson, Ko¸cak and Magazinnik (2019).

Finally, we contribute to the literature on salience in political economy. While salience theory has been widely applied to topics such as electoral behavior, party competition, agenda setting, and judicial decision-making (Moniz and Wlezien, 2020; Dragu and Fan, 2016; Riker, Riker and Riker, 1986; Ascencio and Gibilisco, 2015; Guthrie, Rachlinski and Wistrich, 2000; Viscusi, 2001; Bartels, 1986; Niemi and Bartels, 1985; RePass, 1929), its implications for research design have received less attention. By incorporating the framework developed by Bordalo, Gennaioli and Shleifer (2012, 2013, 2016) into the study of survey experiments, we highlight salience as a central consideration in experimental methodology, thereby extending its scope and applicability.

#### 1 Model of Survey Experiments

Causal effects are typically formalized within the potential outcomes framework. To illustrate the mechanisms underlying generalizability, we develop a model that integrates behavioral microfoundations of attention and salience with the potential outcomes framework. We explicitly incorporate environmental features into the potential outcomes and emphasize that the target estimand in a survey experiment depends on the consideration set and the salience of attributes.

##### 1.1 Attention and Salience

Consider a survey experiment conducted in a survey environment. Let Es denote the survey environment, and Er denote the target real-world environment. Let the informational content available to respondent i be summarized by an attribute vector Xi = (Xi1,...,XiK) ∈ X. The components of Xi can be interpreted broadly. In a conjoint experiment, they correspond to profile attributes. In a vignette experiment, they represent features of a scenario. In an informational treatment, they capture the arguments, facts, or cues embedded in the message. In candidate or policy evaluation tasks, they describe the characteristics of the object being evaluated. Throughout the paper, we refer to Xik as attribute, and to its specific realization xik as the value of the attribute.

Individuals have limited attention. A large body of research shows that, when making decisions—such as purchasing a computer—individuals do not evaluate the full set of available options or attributes (Hausman, 2008). Instead, they focus on a subset of relevant information. In the literature, the subset of attributes or alternatives that a respondent attends to when making a decision is referred to as the consideration set (Hausman, 2008; Wright and Barbour, 1977). It is well established that, due to cognitive constraints, individuals cannot allocate sufficient attention to all potentially relevant attributes (Stigler, 1961; Jones and Baumgartner, 2005; Chetty, Looney and Kroft, 2009). As a result, the consideration set is typically a strict subset of the full attribute

space that may, in principle, influence a decision. Formally, let

###### Ci(E) ⊆ {1,...,K}

denote respondent i’s active consideration set under environment E ∈ {Er,Es}. If k ∈/ Ci(E), then attribute k does not enter the active evaluation in environment E.

Following the salience model (Bordalo, Gennaioli and Shleifer, 2012, 2013), given an attribute vector Xi, respondent i evaluates it in environment E as:

Vi(Xi,E) =

K

αik(Xi,E)uik(Xik) =

αik(Xi,E)uik(Xik)

k=1

k∈Ci(E)

where αik(Xi,E) > 0 denotes the salience weight assigned to attribute k, satisfying Kk=1 αik(Xi,E) =

- 1. The function uik(Xik) represents the utility contribution of attribute k. We assume that the baseline utility component uik is invariant across environments. This restriction allows us to isolate the role of attention and salience—captured by Ci(E) and αik(Xi,E)—in shaping differences between the survey and real-world evaluations. It is worth noting that the environment E may influence many aspects of the decision-making process. In this study, however, we focus exclusively on the roles of attention and salience.


The key idea is that salience αik(Xi,E) need not be fixed. As emphasized by Taylor and Thompson (1982), ”salience refers to the phenomenon that when one’s attention is differentially directed to one portion on the environment rather than to others, the information contained in that portion will receive disproportionate weighing in subsequent judgment.” This idea is formalized by a salience function σ(xk,Xk), where xk denotes the realized value of attribute Xk, and Xk is a reference point. The reference may be individual-specific or determined by the experimental context. For example, in a vignette experiment where the attribute is the level of corruption, each respondent i may have a baseline perception of the typical level of corruption among politicians. In a conjoint experiment, where respondents evaluate two hypothetical politicians, a natural reference

point is the average level of corruption across the two profiles.

The salience function captures the “distance” between an attribute value and its reference point. Intuitively, attributes that deviate more from the reference point receive greater salience. A more formal treatment is provided in Bordalo, Gennaioli and Shleifer (2012). The salience function is typically assumed to satisfy several axiomatic properties. First, for any two intervals [x,y] and [x′,y′], with [x,y] fully contained within [x′,y′], it holds that σ(x,y) < σ(x′,y′). This reflects the psychological principle that larger contrasts are more perceptually salient. Second, the function satisfies homogeneity of degree zero: σ(bx,by) = σ(x,y) for any positive scalar b. A commonly used functional form that satisfies these properties is σ(x,y) = |x−yy|.

Now we introduce how salience operates. Let rik(Xi,E) ∈ {1,...,|Ci(E)|} denote the salience rank of attribute k among the active considerations in environment E, where smaller values indicate greater salience. The effective salience weight αik takes the form

ik(Xi,E)−1

α¯ik δr

###### j∈Ci(E) α¯ij δrij(Xi,E)−1, k ∈ Ci(E), (1)

αik(Xi,E) =

where δ ∈ (0,1] indexes the strength of salience, and α¯ik denotes the baseline salience. When attribute j is more salient than attribute k, as determined by the salience function, i.e., σ(xij,Xij) > σ(xik,Xik), it follows that rij < rik. Consequently, under the effective salience weights, attribute Xk is more heavily discounted, since δr

ij−1. To illustrate the mechanism, consider a simple example. For ease of exposition, we suppress the individual subscript i. Suppose a candidate-choice conjoint experiment with two attributes: age X1 and gender X2. Let α1 and α2 denote the baseline salience weights, reflecting the importance of age and gender in candidate evaluation. When respondents observe two hypothetical candidates, salience is determined by how each attribute value deviates from its reference point. Without loss of generality, suppose that in the conjoint setting the reference for each attribute is given by the average across the two candidates Xj = x

ik−1 < δr

2 . If, for a given comparison, gender is more salient than age, i.e., σ(x1,X1) < σ(x2,X2), then r1 = 2 and r2 = 1. The resulting evaluation

1+x2

V (X1,X2,Es) with effective salience is



α1+δα2u2(x2) if σ(x1,x1) > σ(x2,x2)

α1+δα2u1(x1) + δα

α1

2



(2)

V (X1,X2,Es) =

δα1+α2u2(x2,) if σ(x1,x1) < σ(x2,x2) α1u1(x1) + α2u2(x2) if σ(x1,x1) = σ(x2,x2)

δα1+α2u1(x1) + α

δα1

2



Accordingly, when an attribute, such as x1, is relatively more salient, its weight in the utility function (α1) is effectively increased to α1

α1+δα2, while the weight on the less salient attribute, α2, is reduced to δα2

α1+δα2.The denominator ensures that the salience weights sum to one. The parameter δ governs the strength of the salience effect. When δ = 1, there is no salience distortion, and attributes are weighted according to their baseline importance. As δ decreases below one, relatively more salient attributes receive disproportionately greater weight, while less salient attributes are increasingly discounted.

##### 1.2 Causal Effects

We use Zi to denote treatment. In survey experiments, the treatment typically determines the values of the attributes that respondents observe. Accordingly, the attribute vector Xi(Zi) can be viewed as a function of Zi. The individual causal effect on utility, comparing Zi = z and Zi = z′ in environment E, is defined as

###### ICEi(E) = Vi(Xi(z);E) − Vi(Xi(z′);E).

where = Vi(Xi(z);E) denotes the potential utility under treatment z.4

The outcome variable need not directly measure this latent evaluation. Instead, it is generally a function of the observed response, given by Yi = gi(Vi(Xi;E)). This formulation nests several commonly used outcomes: forced-choice decisions, where gi(v) = 1{v ≥ 0}; ratings or ther-

4For conjoint experiments, please see SI A. For factorial designs, the framework can be readily extended to accommodate multiple treatments.

mometer scales, where gi is the identity or a discretized monotone transformation; and approval or support indicators, where gi follows a threshold rule. Because gi is typically weakly increasing, the latent comparison in Vi remains the central theoretical object. Our results extend to any monotone transformation of Vi.

As discussed in the introduction, we examine whether causal effects identified in the survey environment generalize to the real-world environment while holding fixed the individuals, treatments, and outcome mappings. This constitutes a necessary precondition for any subsequent discussion of generalizability to a broader population. Following Egami and Hartman (2023), we focus on two key dimensions of generalizability: effect magnitude and effect sign.

- Definition 1 (Effect Magnitude Equivalence). ICEi(z,z′;Es) = ICEi(z,z′;Er)
- Definition 2 (Effect Sign Congruence). sign[ICEi(z,z′;Es)] = sign[ICEi(z,z′;Er)]


Generalizability of average effects follows naturally once we aggregate individual-level causal effects across the population. We focus on ICE because it provides a clear way to illustrate the mechanism at the individual level and, as discussed earlier, because our notion of weaker generalizability involves holding individuals, treatments, and outcome mappings fixed.

#### 2 Limited Attention and Survey Experiment Generalizability

This section studies how attention mechanisms affect generalizability, with a particular focus on the equivalence of effect magnitudes. To isolate the role of attention, we first suppress salience distortions and examine how generalizability is affected when the survey environment alters only the active consideration set. Accordingly, as a benchmark, we assume δ = 1 throughout this section. The evaluation function then simplifies to Vi(Xi,E) = h∈C

i(E) αikuik(Xik), where the (effective) salience αik are invariant to attribute values.

Individuals have limited attention. In most decision-making contexts, it is unrealistic for individuals to consider all potentially relevant features. Instead, decisions are based only on attributes

that enter the active consideration set. A defining feature of the survey environment is that respondents’ attention is strongly shaped by the information explicitly provided in the experimental design. For example, in a candidate-choice experiment where only age and gender are presented, respondents are likely to focus primarily, if not exclusively, on these attributes. Ensuring that respondents attend to the provided information, rather than skim past it, is therefore a central concern in survey experiments, motivating the widespread use of attention checks to detect inattentive respondents.

By contrast, in the real-world environment, individuals are not constrained by the limited set of attributes specified by the researcher. When making analogous decisions outside the survey context, respondents may attend to a broader and potentially different set of features. To formalize this distinction, we analyze the attention mechanism under the following limited-attention assumption.

- Assumption 1 (Limited Attention). Ci(Es) ⊂ Ci(Er).


The consideration set in survey experiments is often a subset of the real-world consideration set for several reasons. In many applications, this provides a natural benchmark. First, survey experiments are designed to address specific research questions. As a result, researchers typically include a selected set of substantively relevant attributes, along with additional attributes serving as controls. These attributes are therefore best understood as a subset of the real-world consideration set Ci(Er). Second, researchers rarely possess complete knowledge of all attributes that respondents consider in real-world decision-making. Even if such knowledge were available, it would generally be infeasible to present the full set of relevant attributes within the constraints of a single survey instrument.

Ideally, respondents attend primarily to the attributes presented in the survey experiment, as these are the sources of randomized variation. However, in practice, respondents may also infer unlisted characteristics or rely on prior beliefs (Dafoe, Zhang and Caughey, 2018). A more general formulation therefore allows for Ci(Es) ̸= Ci(Er). In some special cases, it is even possible that Ci(Es) ⊃ Ci(Er). Under such scenarios, our results continue to hold qualitatively, although the implications shift—from amplified effect magnitudes to potentially attenuated or unequal effects.

Empirically, however, available evidence is more consistent with the limited-attention benchmark, although direct evidence remains limited.

Without loss of generality, we assume that the real-world consideration set is CIr = {X1,X2,...,Xm},

with associated baseline salience weights denoted by αr = (αi1,...,αim). The experimental consideration set is given by Cis = {X1,X2,...,Xk}, with corresponding baseline salience αs = (αi′1,...,αik′ ). We assume the cardinality of the real-world consideration set, m = |Cir|, exceeds that of the experimental consideration set, k = |Cis|. In other words, the experimental consideration set consists of only the first k attributes from the real-world consideration set.

Now, we provide intuition for how limited attention affects the magnitude of causal effects. For ease of exposition, suppose the treatment in the survey experiment changes only the first attribute Xi1(Zi), from xi1 to x′i1. Then, the utility changes from Vi(xi1,xi−1,Es) = αi1ui1(xi1) +

m j=2 αjuij(xij) to Vi(x′i1,,xi−1,Es) = αi1ui1(x′i1) + mj=2 αjuij(xij). Therefore, the ICE in the survey experiment is ICEI(ES) = Vi(xi1,xi−1,Es)−Vi(x′i1,xi−1,Es) = αi1[ui1(xi1)−ui1(x′i1)]. Similarly, in the real-world environment, the ICE is αi′1[ui1(xi1) − ui1(x′i1)]. Unless the baseline salience weights coincide, the two effects will generally differ. Under limited attention, the survey consideration set contains fewer attributes than the real-world consideration set (Ci(Es) ⊂ Ci(Er)). As a result, each attribute in the smaller consideration set Ci(Es) tends to receive relatively greater weight than in Ci(Er). Consequently, it is unlikely that αi1 = αi′1. Instead, it is more plausible that αi1 > αi′1, implying that the causal effect is amplified in the survey environment, ICE(Es) > ICE(Er).

Formally establishing this amplification result requires additional assumptions. In particular, when the real-world consideration set includes additional attributes, these attributes may be correlated with existing ones—especially the focal attribute Xi1-which can alter baseline salience weights and potentially attenuate or even reverse the effect. Although such scenarios are possible, our focus is on isolating the limited-attention mechanism. Moreover, well-designed survey experiments rarely omit attributes that are highly correlated with the focal attribute, as doing so would undermine the internal validity of the design. To formalize this idea, we impose that the relative

importance of attributes is preserved even when additional attributes are introduced.

- Assumption 2. For two consideration set Ci1 and Ci2, and any j,k ∈ Ci1 ∩ Ci2,


αij′ α′

αij αik

=

ik

Specifically, if a respondent perceives attribute X1 to be more important than attribute X2 in one setting, then in a comparable setting with an expanded consideration set, the respondent continues to rank X1 as more important than X2. This assumption is more likely to hold in well-designed experiments that explicitly incorporate attributes highly correlated with the focal dimensions of interest, thereby ensuring that any additional attributes in the real-world consideration set are not strongly correlated with those included in the experimental design.

The following results hold for general treatment.Let Di = {j ∈ {1,...,k}|uij(Xij(z)) ̸= uij(Xij(z′))} denote the set of attribute indices for which the treatment affects individual i.

- Proposition 1 (Effect Magnitude Non-Generalizability). Given treatment assignment Z = z and Z = z′, suppose the limited attention assumption 1 hold, and Di ̸= ∅.


(1) The causal effects in the survey experiment and the real world differ almost surely:

ICE(Es) ̸= ICE(Es)

if αij ̸= αij′ for some j ∈ Csr and uij(Xij(z)) ̸= uij(Xij(z′)).

(2) Moreover, if the assumption 2 also holds, then the causal effect in the survey experiment are amplified relative to those in the real-world environment by a factor δ = α′ 1

1+α′2+...+α′k > 1. Proof. All proofs are in the SI.

| |
|---|


The first result follows directly. When baseline salience differs between the survey and realworld environments due to limited attention, the magnitude of causal effects estimated in the experimental setting will, in general, not be externally valid.

Under the additional stable salience assumption, we obtain a sharper result. If the inclusion of additional attributes in the real-world environment does not distort the relative importance of the attributes already present in the experiment, then the experimental causal effect is systematically amplified relative to the real-world effect. This condition is more likely to hold when the experimental design incorporates the most substantively important attributes—particularly those that are highly correlated with other relevant dimensions—so that omitted attributes do not substantially alter relative salience rankings.

The amplification factor δ depends on the total salience of the attributes included in the survey experiment, as measured by their real-world salience weights α. When respondents place substantial weight on attributes that are omitted from the experimental design, the share of total salience allocated to the included attributes is correspondingly reduced in the real world. As a result, the experimental estimate which implicitly redistributes attention over a smaller set of attributes can substantially overstate the true causal effect.

###### Empirical Evidence

The formal model and Proposition 1 illustrate the mechanism through which limited attention distorts the magnitude of experimental causal effects. We now turn to empirical evidence. Our goal is not to “prove” the model—no formal model can be proven in that sense. The value of the model here lies in its ability to clarify and organize an empirically relevant phenomenon.

One implication of Proposition 1 is that amplification bias should decline as more attributes are included in the consideration set. Of course, neither the true consideration set nor the realworld causal effect is directly observable. What researchers can manipulate, however, is the set of attributes presented in the survey experiment. When respondents attend to the experimental task, their attention is likely to be concentrated primarily on the attributes explicitly provided by the researcher. This is particularly true for conjoint experiments compared to other types of survey experiments. We therefore focus primarily on conjoint experiments. We argue that the attributes included in the experiment largely determine, or at least dominate, the active consideration set.

To examine this implication, we first study the 67 candidate-choice conjoint and vignette experiments compiled by Schwarz and Coppock (2022). In these experiments, a gender attribute is randomly assigned, and the outcome measures are comparable or can be consistently recoded across studies. This common structure allows us to isolate and compare the average causal effect of the gender attribute across studies. In addition, we collected information on the number of nongender attributes presented in each experiment. Notably, in some studies, the number of attributes provided is as small as two.

To investigate the hypothesized relationship between the number of attributes and the AMCE of gender across these experiments, we conduct a meta-analysis. Figure 2 presents the metaregression results based on a random-effects model, both for the full sample of countries and for the United States subsample, given that the majority of experiments were conducted in the United States. The vertical axis reports the absolute value of the estimated effect, recognizing that the causal effect of gender may be negative in some studies.5 Across both specifications, we find a statistically significant negative relationship between the number of attributes and the experimental causal effect of gender, consistent with our theoretical predictions. The results are robust to excluding experiments with a small number of negative estimates as well as potential outliers.

To address cross-study heterogeneity and more directly test our hypothesis regarding the influence of the number of attributes on experimental effects, we designed and conducted an original candidate-choice experiment with a controlled and consistent attribute set. The experiment was fielded to 1,200 respondents in the United States via Lucid in September 2023. Lucid employs a quota sampling strategy to align participant demographics with those of the U.S. Census. Prior research by Coppock and McClellan (2019) shows that Lucid samples yield behavioral patterns comparable to those observed in nationally representative benchmark experiments.

Additional details on the experimental design are provided in SI B. Respondents were randomly

5Consistent with our theoretical framework, a true positive effect is expected to diminish as the number of attributes increases, whereas a true negative effect should move toward zero in magnitude (i.e., its absolute value decreases).

All

USA

| | | | | | | | |
|---|---|---|---|---|---|---|---|
|USA| | | | | | | |
| |USA| | | | | | |
|US<br><br>USA|A<br><br>USA<br><br>Afghan|istan| | | | | |
|USA<br><br>US|Malawi<br><br>India A|Bra Norway<br><br>USA|zil Brazil Norwa|y| | | |
|U<br><br>US|K Arge<br><br>USA US A USA|ntina<br><br>A<br><br>USA<br><br>Jap<br><br>USA|an<br><br>USA<br><br>Japan| | | | |
|UK<br><br>USA|UK<br><br>U<br><br>UK USA<br><br>UK|T SA<br><br>USA<br><br>UK|unisia Zambia| |= 0.001|1| |
|USA|UK<br><br>UK<br><br>C UK|Tunisia<br><br>USA hile|USA USA<br><br>U|US<br><br>SA|A|USA| |
| |U|SA USA|Malawi| | |USA| |


| | | | | | | | |
|---|---|---|---|---|---|---|---|
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | |P = 0.00|04| | |
| | | | | | | | |
| | | | | | | | |


0.09

0.09

Estimate

Estimate

0.06

0.06

0.03

0.03

0.00

0.00

5 10 15

5 10 15

Number of Attributes

Number of Attributes

- Figure 2: Test of the amplification hypothesis using meta-regression. Each point represents the estimated effect of gender from a conjoint experiment conducted in a given country, with point size proportional to the inverse of the estimate’s variance. The fitted meta-regression line indicates that the treatment effect decreases as the number of attributes increases. Full results are reported in Table A.3, Columns 1–2.


assigned to one of five groups. Within each group, participants completed six paired candidatechoice tasks. The groups differed in the number of attributes presented, while holding the specific attribute set fixed within each group.

|- Group 1 was presented with only two attributes: gender and age.<br>- Group 2 included the previous attributes plus education and tax policy, totaling four attributes.<br>- Group 3 added race and income to the attributes in Group 2, resulting in six attributes.<br>- Group 4 included military service and religious beliefs, bringing the total to eight attributes.<br>- Group 5 encompassed ten attributes by adding children and marital status to those in Group 4.<br>|
|---|


Consistent with our meta-analytic focus, we examine the effect of gender across these groups. The results, presented in Figure 3, reveal a statistically significant negative relationship between the number of attributes and the magnitude of the experimental gender effect, despite the limited number of observations (five groups). This pattern provides supporting evidence for our theory,

which predicts that effect sizes diminish as the number of attributes increases.

An exception arises in Group 4 (with eight attributes), where the estimated gender effect is larger than expected. While this deviation may reflect sampling variability, an alternative explanation is that salience effects may be at play—a possibility we explore in subsequent sections.

Gender Effects

0.16

| | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | |P = 0|.07| |
| | | | | | | | | | |
| | | | | | | | | | |
| | | | | | | | | | |
| | | | | | | | | | |
| | | | | | | | | | |
| | | | | | | | | | |


0.12

Estimate

0.08

0.04

2 4 6 8 10

Number of Attributes

- Figure 3: Test of the amplification hypothesis using a single conjoint experiment. Each point represents the estimated AMCE of the gender attribute under a given number of attributes, with point size proportional to the inverse of the estimate’s variance. The fitted line is obtained from a meta-regression. Full results are reported in Table A.3, Column 3, and Table A.4.


#### 3 Salience and Survey Experiment Generalizability

In this section, we incorporate the role of salience. Building on the framework developed by Bordalo, Gennaioli and Shleifer (2012), we examine how salience, in conjunction with limited attention, further shapes the generalizability of survey experiments. In particular, we focus on the possibility of effect sign reversal across environments.

Not all attributes are equally important in decision-making. Evidence from survey experiments, including studies using eye-tracking techniques, shows that respondents process information selec-

tively, focusing on attributes they perceive as important while ignoring less relevant ones as task complexity increases. For example, Jenke et al. (2021) demonstrate that respondents in conjoint experiments allocate attention unevenly across attributes. In salience theory, attention is differentially allocated to attributes that stand out relative to a reference point, as captured by the salience function σ(xij,Xij). To operationalize this idea, we rank attributes by salience, where a smaller rank r indicates greater salience. The resulting mechanism is summarized by equation 1, which we reproduce here for convenience:

ik(Xi,E)−1

α¯ik δr

αik(Xi,E) =

j∈Ci(E) α¯ij δrij(Xi,E)−1

Therefore, if an attribute lies close to its reference point, its salience is substantially discounted; conversely, attributes that deviate markedly from the reference receive relatively greater salience. The parameter δ governs the strength of this effect. To capture the possibility that perceived attribute salience varies across decision contexts, we introduce the following assumption:

Assumption 3 (Salience Effect). δ < 1.

The salience model emphasizes that the weight assigned to each attribute depends on the extent to which its realized value deviates from a reference point or prevailing expectation. Throughout this section, we maintain the assumption 2. Absent this condition, changes in the attribute set could alter relative salience rankings in ways that confound the mechanism of interest, making it difficult to disentangle salience-driven distortions from broader shifts in underlying preferences.

##### 3.1 Effect Sign Reversal

In the previous section, we showed that experimental estimates can be distorted by limited attention, leading to systematically amplified causal effects. Such amplification may, in some cases, be advantageous for researchers seeking to detect the direction of an effect, as it can reduce the sample size required to achieve a given level of statistical power.

A more conservative—and ultimately more fundamental—requirement for experimental evidence to meaningfully validate theoretical predictions is effect sign congruence: the experimental causal effect should have the same direction as the corresponding real-world effect (Slough and Tyson, 2024). However, once salience effects are introduced, this requirement may fail. In particular, salience-induced reweighting of attributes can generate effect sign reversal, thereby undermining the reliability of experimental findings as indicators of underlying causal relationships.

As is evident from equation 1, salience depends on the realized attribute levels. Accordingly, the salience rank for attribute k can be expressed as a function of the treatment, rk(Zi). The following proposition provides a sufficient condition under which effect sign reversal may occur.

- Proposition 2 (Effect Sign Reversal). Suppose that assumptions 2 and 3 hold. The direction of the experimental effects may differ from their real-world counterparts if there exists an attribute k such that rk(zi) ̸= rk(zi′).


The key condition in this proposition – that there exists an attribute k such that the salience ranking changes across treatment states – captures a scenario in which a change in the treatment alters the relative salience of at least one attribute. As shown in the proof, such a reversal can arise regardless of the utility magnitudes associated with excluded attributes or the baseline salience of the treatment attribute itself.

To build intuition for the phenomenon of effect sign reversal, consider again a survey experiment in which the treatment affects only the first attribute. As illustrated in the left panel of Table

- 2, under the control condition, the attribute values are (x1,x2) with corresponding salience weights (α1,α2). The treatment changes only x1 to x˜1, leading to updated salience weights (α1′ ,α2′ ). In the real-world environment, suppose there is an additional attribute X3 in the consideration set, as shown in the right panel of the table 2. Under the same experiment, only the first attribute is affected. The individual causal effect in the survey environment is given by


ICE(Es) =

2

αikuik(xk) − αikuik(˜xk)

k=1

where x˜2 = x2 since the treatment only affects the first attribute. In contrast, in the real-world environment, the individual causal effect is

ICE(Er) =

2

βikuik(xk) − βikuik(˜xk) + [β3uik(x3) − β˜3uik(˜x3)].

k=1

We observe that salience affects the individual causal effect through two distinct channels. First, changes in salience weights imply that, even when the treatment does not alter the values of other attributes, those attributes still contribute to the treatment effect via reweighting. In particular, because the real-world environment includes an additional attribute, the salience weights assigned to the first two attributes (β) differ from those in the survey environment (α). This reallocation of attention can lead to differences in effect magnitude and, potentially, in effect sign across environments. Second, in the real-world environment, ICE(Er) includes an additional term arising from the third attribute, [β3uik(x3) − β˜3uik(˜x3)]. This additional component can be sufficiently large to overturn the direction of the treatment effect, thereby inducing effect sign reversal.

Survey Experiment Environment Real-world Environment Control Status Treatment Status Control Status Treatment Status

|Attribute Salience|Attribute Salience<br><br>|Attribute Salience|Attribute Salience|
|---|---|---|---|
||x1|
|---|
<br><br>α1 x2 α2<br><br>||x˜1|
|---|
<br><br>α1′ x2 α2′<br><br>||x1|
|---|
<br><br>β1 x2 β2 x3 β3<br><br>||x˜1|
|---|
<br><br>β1′ x2 β2′ x3 β3′|


Table 2: Illustration of Salience Effect.

It is immediate that if there exist parameter configurations under which a positive effect can be reversed to a negative one, then it is even more likely that configurations exist under which the effect is attenuated to zero. We formalize this observation in the following corollary:

Corollary 1. Suppose assumptions 2 and 3 hold. If there exists j and k, such that rj(zi) ̸= rk(zi′), then the experimental treatment effect may become null in the real-world environment, and vice versa.

It is important to emphasize that our results are existence results; they do not imply that effect

sign reversal or attenuation must occur in practice. For example, if a particular attribute—or its associated salience—dominates the evaluation process, then reversal is unlikely. The intuition is straightforward. Suppose attribute X1 is substantially more important than all other attributes. In that case, it yield a large utility contribution u(X1). Consequently, in the overall evaluation V , the term α1u(X1) dominates. Even if salience rankings shift, this dominant component is unlikely to be offset by changes in other attributes. As a result, the sign of V , and hence of the individual causal effect, will largely be determined by X1, making sign reversal unlikely in such settings.

Another scenario that precludes effect sign reversal or attenuation arises when the rank-change condition is not satisfied. As emphasized in Proposition 1, variation in salience rankings across treatment states is essential for generating sign reversal. The following proposition formalizes that, in the absence of such rank changes, effect sign reversal cannot occur.

- Proposition 3. Assuming conditions 2 and 3 hold. If the relative salience rankings satisfy rk(z) = rk(z′) for all k, then the effect sign reversal cannot occur.


##### 3.2 Empirical Evidence

The preceding propositions illustrate how salience can generate effect sign reversal or effect attenuation. We cannot directly test the theory, because neither the real-world consideration set nor the exact salience weights are observed or experimentally controlled. What we can do, instead, is derive testable implications. As before, our goal is not to “prove” the model.

Although we cannot manipulate the real-world consideration set, we do expect to substantially influence the consideration set in the survey environment. Building on Proposition 2 and Corollary 1, we therefore derive the following testable implications:

- Implication 1. The sign of the effect in a conjoint experiment may reverse or attenuate to null as the number of attributes increases.


The proposition also highlights that changes in salience rankings are necessary for this phenomenon to arise. This raises the question: under what conditions can we expect salience rank-

ings to remain unchanged, as assumed in the preceding proposition? The mechanism underlying salience implies that rankings are determined by the salience function σ(xk,Xk). If the treatmentinduced change in the attribute X1 is not sufficiently large to meaningfully alter the reference point Xk, then σ(xk,Xk) will be close to σ(˜xk,Xk). In such cases, the change in salience is too small to affect the relative ranking of attributes. Motivated by this intuition, we propose the following implication:

- Implication 2. Attribute effect sign reversal or attenuation is less likely when changes in attribute levels are marginal.


We draw on data from a conjoint experiment on hotel rooms conducted by Bansak et al. (2021). The study identifies four core attributes of hotel rooms: “view from the room (ocean or mountain view), floor (top, club lounge, or gym and spa floor), bedroom furniture (1 king bed and 1 small couch or 1 queen bed and 1 large couch), and the type of in-room wireless internet (free standard or paid high-bandwidth wireless).” In addition to these core attributes, the authors include 18 supplementary attributes that are largely unrelated to the core set.

Respondents were asked to choose their preferred hotel room from 15 paired comparisons, where each profile included the four core attributes along with a randomly selected subset of additional attributes. As a result, respondents were randomly assigned to one of 11 experimental conditions, with profiles containing 4, 5, 6, 7, 8, 9, 10, 12, 14, 18, or up to 22 attributes.

Figure 4 presents a heatmap of the results.6 The horizontal axis indicates the number of attributes, while the vertical axis corresponds to attribute levels. Darker colors denote negative AMCEs, whereas lighter colors indicate positive AMCEs. The results provide support for our hypothesis on effect sign reversal (implication 1). In particular, the estimated effects of some attributes—such as menu, bar, closet, and pillow—exhibit substantial instability across conditions. By contrast, other attributes, including View, Towels, and Internet, display considerable stability.

6Figure A.4 in the SI reports statistical significance. Due to limited statistical power, relatively few estimates are statistically significant. As the sample size increases, confidence intervals would be expected to narrow, potentially revealing additional cases of statistically significant effect reversals. At the same time, null effects are also consistent with our theoretical predictions and align with implication 1.

This pattern is consistent with our theoretical framework: these attributes likely carry high baseline salience and utility, allowing them to dominate the evaluation process and remain robust to changes in the attribute set. This evidence also reinforces the classification of View and Internet as core attributes, as emphasized by Bansak et al. (2021).

To test implication 2, we adapted our candidate-choice experimental design. To better control for salience, rather than randomly assigning attribute levels across profiles, we constrained level differences to be minimal. For example, for the age attribute with five levels (40, 52, 60, 68, 75), only adjacent values were allowed to appear in a comparison. Thus, if one profile was assigned age 52, the other profile could only take values 40 or 60.

As in the previous experiment, this study was fielded to 1,200 U.S. respondents via Lucid in November 2023. Each respondent completed five paired choice tasks. Table 3 reports the AMCEs for gender under both the original design and the modified, reduced-salience design. When attribute levels were assigned randomly—without controlling for salience—the corresponding AMCEs (Column 2) exhibit a sign reversal as the number of attributes increases from six to eight. By contrast, Column 3 presents results from the reduced-salience design. A key observation is the absence of a clear effect sign reversal under this specification. We emphasize that this finding does not imply that researchers should universally restrict conjoint designs to adjacent attribute levels. Rather, this design choice is intended as a targeted test of the theoretical mechanism.

Num Salience Effect Reduced Salience

2 0.15 0.45 4 0.10 0.10 6 0.03 0.15 8

|-0.08|
|---|


0.10 10

|-0.02|
|---|


0.27 Table 3: Gender Effect. Full results are in the Table A.4 and A.5

We emphasize again that our results are not claims about inevitability or frequency. We do not assert that such inconsistencies must occur, nor do we quantify how often they arise in practice. Rather, our goal is to illustrate a plausible mechanism. Other mechanisms—and potentially

| | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |


View

- Towels1
- Towels2


Thermon3

- Thermo1
- Thermo2


Sink

- Service1
- Service2
- Service3


- Pillow1
- Pillow2
- Pillow3


Office

Menu

- Linens1
- Linens2


- Lamps1
- Lamps2


Treatment

- Kitchen1
- Kitchen2


Internet

- Hallway1
- Hallway2


Furniture

- Floor1
- Floor2


Fan

Elevators

Closet

- Chocolate1
- Chocolate2
- Chocolate3


- Channels1
- Channels2


Call

- Bar1
- Bar2


4 5 6 7 8 9 10 12 14 18 22

Number of Attributes

Treatment Effect Negative Positive NA

- Figure 4: Testing the implication of effect sign reversal. The horizontal axis denotes the number of attributes, and each row represents the effect sign for a given attribute. Dark colors indicate negative effects, while light colors indicate positive effects. The 385 estimates are obtained from the same model specification as in Bansak et al. (2021).


offsetting countervailing forces—may also be at work.

Indeed, based on our theory, relative to other types of survey experiments, well-designed conjoint experiments may be less susceptible to generalizability concerns. Because they incorporate multiple attributes within a single design, they substantially reduce the likelihood of omitting attributes that are important in real-world decision-making. The robustness of conjoint experiments has been widely discussed in the literature (Jenke et al., 2021; Hainmueller, Hangartner and Yamamoto, 2015).

#### 4 Discussion and Concluding Remarks

An increasing number of studies in the social sciences employ experiments to identify causal effects (Druckman et al. 2006). While such designs provide strong internal validity, external validity remains a longstanding concern. This paper develops a formal framework to explain why survey experiments may fail to satisfy this stronger notion of generalizability, even when treatment is randomized and even when the same individuals, treatment content, and outcome measures are held fixed. This limitation raises important concerns about the extent to which experimental findings can be extrapolated to real-world settings. For example, Boas, Hidalgo and Melo (2019) show that although voters appear to sanction corruption information in survey experiments, they do not take action when presented with similar information about their own mayor in a field setting.

We provide both theoretical and empirical evidence demonstrating how two mechanisms—limited

attention and salience effects—can undermine the generalizability of survey experiments. In particular, we show that experimental effects may be systematically amplified in magnitude and, in some cases, may even diverge in direction from their real-world counterparts.

A caveat to our findings is that we do not claim that non-generalizability is inevitable in survey experiments. Many studies—for example, Jenke et al. (2021)—as well as empirical evidence presented in this paper, suggest that certain attributes exhibit stability across contexts in conjoint experiments. Our theoretical framework also highlights that conjoint experiments possess particu-

lar advantages for achieving high levels of generalizability.

It is important to emphasize that salience effects are not inherently detrimental to experimental design. Whether individuals make decisions in real-world contexts or within experimental settings, salience is an integral component of multi-dimensional decision-making. Accordingly, the goal should not be to eliminate salience effects altogether. Rather, the objective is to ensure that the salience patterns induced in the experiment closely mirror those that arise in real-world environments. It is the artificially induced salience distortions—those that diverge from real-world conditions—that are most problematic.

Notably, in the absence of attention distortions—i.e., if the experimental environment perfectly replicates the real-world decision context—experimental ICEs would coincide with their real-world counterparts, precisely because salience patterns would align across environments. The challenge, of course, is that achieving such equivalence is rarely feasible in practice.

A more practical approach is to design attribute levels and profile combinations that closely approximate real-world scenarios. This calls for a phased research design that emphasizes realism, relevance, and precision. A natural starting point is a comprehensive review of the existing literature and available data on the decision-making context of interest. This preliminary step should be complemented by exploratory interviews or pilot surveys with individuals who engage in similar decisions in real-world settings. Such qualitative and descriptive evidence is essential for identifying the attributes and attribute levels that are most salient and substantively relevant to the decision-making process.

#### References

Abelson, Robert P. 2014. Attitude extremity. In Attitude strength. Psychology Press pp. 25–41. Abramson, Scott F, Korhan Koc¸ak and Asya Magazinnik. 2019. “What do we learn about voter

preferences from conjoint experiments.” Unpublished Working Paper . Abramson, Scott F, Korhan Kocak, Asya Magazinnik and Anton Strezhnev. 2023. “Detecting Preference Cycles in Forced-Choice Conjoint Experiments.”. Adair, John G. 1984. “The Hawthorne effect: a reconsideration of the methodological artifact.” Journal of applied psychology 69(2):334.

Allais, Maurice. 1953. “Le comportement de l’homme rationnel devant le risque: critique des postulats et axiomes de l’´ecole am´ericaine.” Econometrica: Journal of the Econometric Society pp. 503–546.

Ascencio, Sergio and Michael B Gibilisco. 2015. “Endogenous Issue Salience in an Ownership Model of Elections.”.

Bansak, Kirk, Jens Hainmueller, Daniel J Hopkins and Teppei Yamamoto. 2018. “The number of choice tasks and survey satisficing in conjoint experiments.” Political Analysis 26(1):112–119.

Bansak, Kirk, Jens Hainmueller, Daniel J Hopkins and Teppei Yamamoto. 2021. “Beyond the breaking point? Survey satisficing in conjoint experiments.” Political Science Research and Methods 9(1):53–71.

Bansak, Kirk and Libby Jenke. 2025. “Odd profiles in conjoint experimental designs: Effects on survey-taking attention and behavior.” Political Analysis 33(4):315–338.

Barabas, Jason and Jennifer Jerit. 2010. “Are survey experiments externally valid?” American Political Science Review 104(2):226–242.

Bartels, Larry M. 1986. “Issue voting under uncertainty: An empirical test.” American Journal of Political Science pp. 709–728.

Boas, Taylor C, F Daniel Hidalgo and Marcus Andr´e Melo. 2019. “Norms versus action: Why voters fail to sanction malfeasance in Brazil.” American Journal of Political Science 63(2):385– 400.

- Bordalo, Pedro, Nicola Gennaioli and Andrei Shleifer. 2012. “Salience theory of choice under risk.” The Quarterly journal of economics 127(3):1243–1285.
- Bordalo, Pedro, Nicola Gennaioli and Andrei Shleifer. 2013. “Salience and consumer choice.” Journal of Political Economy 121(5):803–843.


Bordalo, Pedro, Nicola Gennaioli and Andrei Shleifer. 2016. “Competition for attention.” The Review of Economic Studies 83(2):481–513.

Carnes, Nicholas and Noam Lupu. 2016. “Do voters dislike working-class candidates? Voter biases and the descriptive underrepresentation of the working class.” American Political Science Review 110(4):832–844.

Chetty, Raj, Adam Looney and Kory Kroft. 2009. “Salience and taxation: Theory and evidence.” American economic review 99(4):1145–77.

Cook, Thomas D, Donald Thomas Campbell and William Shadish. 2002. Experimental and quasiexperimental designs for generalized causal inference. Vol. 1195 Houghton Mifflin Boston, MA.

Coppock, Alexander and Oliver A McClellan. 2019. “Validating the demographic, political, psychological, and experimental results obtained from a new source of online survey respondents.” Research & Politics 6(1):2053168018822174.

Dafoe, Allan, Baobao Zhang and Devin Caughey. 2018. “Information equivalence in survey experiments.” Political Analysis 26(4):399–416.

De Mesquita, Ethan Bueno and Scott A Tyson. 2020. “The commensurability problem: Conceptual difficulties in estimating the effect of behavior on behavior.” American Political Science Review 114(2):375–391.

Dragu, Tiberiu and Xiaochen Fan. 2016. “An agenda-setting theory of electoral competition.” The Journal of Politics 78(4):1170–1183.

Druckman, James N, Donald P Green, James H Kuklinski and Arthur Lupia. 2006. “The growth and development of experimental research in political science.” American Political Science Review 100(4):627–635.

Egami, Naoki and Erin Hartman. 2023. “Elements of external validity: Framework, design, and analysis.” American Political Science Review 117(3):1070–1088.

Eggers, Andrew C, Nick Vivyan and Markus Wagner. 2018. “Corruption, accountability, and gender: Do female politicians face higher standards in public life?” The Journal of Politics 80(1):321–326.

Ellsberg, Daniel. 1961. “Risk, ambiguity, and the Savage axioms.” The quarterly journal of economics 75(4):643–669.

Findley, Michael G, Brock Laney, Daniel L Nielson and Jason C Sharman. 2017. “External validity in parallel global field and survey experiments on anonymous incorporation.” The Journal of Politics 79(3):856–872.

Findley, Michael G, Kyosuke Kikuta and Michael Denly. 2021. “External validity.” Annual review of political science 24(1):365–393.

Fu, Jiawei and Tara Slough. 2026. “Heterogeneous Treatment Effects and Causal Mechanisms.” American Political Science Review p. 1–18.

Gaines, Brian J, James H Kuklinski and Paul J Quirk. 2007. “The logic of the survey experiment reexamined.” Political Analysis 15(1):1–20.

Guthrie, Chris, Jeffrey J Rachlinski and Andrew J Wistrich. 2000. “Inside the judicial mind.” Cornell L. Rev. 86:777.

- Hainmueller, Jens, Dominik Hangartner and Teppei Yamamoto. 2014. “Do survey experiments capture real-world behavior? External validation of conjoint and vignette analyses with a natural experiment.” Proceedings of the National Academy of Sciences 112(8):2395–2400.
- Hainmueller, Jens, Dominik Hangartner and Teppei Yamamoto. 2015. “Validating vignette and conjoint survey experiments against real-world behavior.” Proceedings of the National Academy of Sciences 112(8):2395–2400.


Hausman, Daniel. 2008. “Mindless or mindful economics: A methodological evaluation.” The foundations of positive and normative economics: A handbook pp. 125–55.

Huang, Melody. 2022. “Sensitivity analysis in the generalization of experimental results.” arXiv preprint arXiv:2202.03408 .

Jenke, Libby, Kirk Bansak, Jens Hainmueller and Dominik Hangartner. 2021. “Using eye-tracking to understand decision-making in conjoint experiments.” Political Analysis 29(1):75–101.

Jones, Bryan D and Frank R Baumgartner. 2005. The politics of attention: How government prioritizes problems. University of Chicago Press.

Krosnick, Jon A and Robert P Abelson. 1992. “The case for measuring attitude strength in surveys.”.

List, John A and Steven D Levitt. 2005. “What do laboratory experiments tell us about the real world.” NBER working paper pp. 14–20.

Liu, James H and Bibb Latan´e. 1998. “The catastrophic link between the importance and extremity of political attitudes.” Political Behavior 20(2):105–126.

Masatlioglu, Yusufcan, Daisuke Nakajima and Erkut Y Ozbay. 2016. Revealed attention. In Behavioral Economics of Preferences, Choices, and Happiness. Springer pp. 495–522.

Moniz, Philip and Christopher Wlezien. 2020. Issue salience and political decisions. In Oxford research encyclopedia of politics.

Mullinix, Kevin J, Thomas J Leeper, James N Druckman and Jeremy Freese. 2015. “The generalizability of survey experiments.” Journal of Experimental Political Science 2(2):109–138.

Niemi, Richard G and Larry M Bartels. 1985. “New measures of issue salience: An evaluation.” The Journal of Politics 47(4):1212–1220.

RePass, David E. 1929. “Issue salience and party choice.” American Political Science Review 65(2):389–400.

Riker, William H, William H Riker and William H Riker. 1986. The art of political manipulation. Vol. 587 Yale University Press.

Sanbonmatsu, Kira. 2002. “Gender stereotypes and vote choice.” american Journal of political Science pp. 20–34.

Schwarz, Susanne and Alexander Coppock. 2022. “What Have We Learned about Gender from Candidate Choice Experiments? A Meta-Analysis of Sixty-Seven Factorial Survey Experiments.” The Journal of Politics 84(2):655–668.

Slough, Tara. 2023. “Phantom counterfactuals.” American Journal of Political Science 67(1):137– 153.

- Slough, Tara and Scott A Tyson. 2023. “External Validity and Meta-Analysis.” American Journal of Political Science 67(2):440–455.
- Slough, Tara and Scott A Tyson. 2024. “Sign-Congruence, External Validity, and Replication.”.


Stigler, George J. 1961. “The economics of information.” Journal of political economy 69(3):213– 225.

Taylor, Shelley E and Suzanne C Thompson. 1982. “Stalking the elusive” vividness” effect.” Psychological review 89(2):155.

Viscusi, W Kip. 2001. “Jurors, Judges, and the Mistreatment of Risk by the Courts.” The Journal of Legal Studies 30(1):107–142.

Wright, Peter and Fredrick Barbour. 1977. Phased decision strategies: Sequels to an initial screening. Graduate School of Business, Stanford University.

# Supplementary Information

- A Formal Definition of Causal Targets of Conjoint Experiment 2
- B Design of Candidate-Choice Experiment 6

- B.1 Principles for Human Subjects Research . . . . . . . . . . . . . . . . . . . . . . 6
- B.2 Pre-registered Design . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7


- C Proof of Proposition 1 10
- D Proof of Proposition 2 12
- E Proof of Proposition 3 13
- F Tables 14
- G Figures 17


#### A Formal Definition of Causal Targets of Conjoint Experiment

Consistent with standard practice, the causal effects are understood in terms of potential outcomes in a hypothetical scenario. We use Table A.1 to illustrate the concept. Suppose we aim to define the ICE for attribute X1 when it changes from x1 to x˜1, while holding the other attributes constant. This involves considering two hypothetical scenarios.

World2 A˜1 A2

World1 A1 A2

x′1 X2 x2 x′2 X3 x3 x′3

|x˜1|
|---|


x′1 x2 x′2 x3 x′3

X1

|x1|
|---|


- Table A.1: Illustration of Multi-dimensional Decisions. Aj is the alternatives and Xk is the attribute.


In the first scenario (World 1), decision makers (DMs) are presented with a choice between two candidates, A1 and A2. Each candidate is characterized by three attributes: X1,X2, and X3. The realized values of these attributes for A1 and A2 are the vectors (x1,x2,x3) and (x′1,x′2,x′3), respectively. For example, if X1 represents gender, with x1 indicating female and x′1 indicating male, the evaluations for the two candidates in World 1 are Vi(A1) and Vi(A2).

In the second scenario (World 2), the DM is presented with the same A2, but for A1, the attribute X1 is realized as x˜1 instead. In other words, all attribute realizations remain the same except for X1. We thus use A˜1 to differentiate this modified version of A1 from its original. The potential evaluations in World 2 become: Vi(A˜1) and Vi(A2).

In practice, most conjoint experiments measure the forced choice outcome Y ; that is, whether

- a candidate is chosen or not, denoted by 1 or 0. Theoretically, the DM chooses candidate A1 over


- A2 because the DM has a higher evaluation for the former. Because the utility difference drives the potential outcome we observe, without loss of generality, throughout the main text, we focus on V rather than Y 7. Therefore, Y is a function of the utility difference. The corresponding utility


7It is evident that the binary choice potential outcome can be defined as Yij = [Vij ≥ 0], where j = 1,2. For outcomes that are preference scores, our results also hold because the score is also a function of the evaluation. In some survey experiments, the DM may only observe one alternative. In such cases, we can simply set Vi(A2) = 0.

differences in World 1 are Vi1 = Vi(A1) − Vi(A2), and in World 2, they are Vi2 = Vi(A˜1) − Vi(A2) 8. Consequently, the individual causal effect for attribute X1 when it changes from x1 to x˜1, given the other attributes remain constant, is defined as the difference-in-differences Vi1 − Vi2.

Our previous difference-in-differences Vi1−Vi2 corresponds to the individual component effect used in the conjoint experiment literature. See Abramson et al. (2023) for details.

To gain intuition regarding the phenomenon of Effect Sign Reversal, consider two hypothetical worlds, as depicted in the left panel of Table A.2. In Experiment 1, we compare B1 and B2, each with three attributes. In Experiment 2, the comparison involves two-attribute profiles A1 and A2. We are particularly interested in the treatment effect of attribute X1 as it changes from x1 to x˜1. Consequently, B2 (and A2), serving as the controlled profiles, are fixed at Xc = (x′1,x′2,x′3) (and (x′1,x′2)) respectively.

We use βk (αk) to denote the salience of each attribute xk when the DM evaluates these alternatives. The corresponding sets of salience are illustrated in the right panel of Table A.2. Assume the existence of prior salience for each attribute, denoted by β = (β10,β20,β30) and α = (α10,α20). Consider how salience is formed and evolves as the DM observes the realized attributes during comparison. When an individual compares two profiles, differing levels of each attribute will “distort” the original salience based on the rule previously mentioned. Specifically, in World 1, when comparing B1 = (x1,x2,x3) to B2 = (x′1,x′2,x′3), for each attribute j, we compute the salience function σk(·, xk+x

′ k

k−1, where rk represents the relative salience rank introduced earlier. We assume that the updated salience attached to B1 follows β1 > β2 > β3 and the salience attached to B2 follows β1′ > β2′ > β3′.

2 ). The original salience β0 is then discounted by δr

In the hypothetical World 2, only the level of attribute 1 in the treatment group is altered, from x1 to x˜1. This modification affects the reference level for attribute X1 and, consequently, the value of the salience function σ1 for attribute 1. For instance, the updated salience attached to B˜1 is now β˜2 > β˜1 > β˜3; in other words, the salience of attribute 1 is now less than that of attribute 2. For simplicity, we assume that the salience values for the controlled profile remain the same as in the

8Note that Vi(A2) in the two hypothetical worlds may differ due to the salience effect, which we will discuss in Section 3.

- Experiment 1

World 1 World 2

|B1 B2<br><br>|B˜1 B2|
|---|---|
||x1|
|---|
<br><br>x′1 x2 x′2 x3 x′3<br><br>||x˜1|
|---|
<br><br>x′1<br><br>xt2 x′2<br>xt3 x′3<br>|


Experiment 1 World 1 World 2

|β1 β2<br><br>|β˜1 β2|
|---|---|
|β1 β1′<br>β2 β2′<br>β3 β3′<br>|β˜1 β1′<br><br>β˜2 β2′<br><br>β˜3 β3′<br>|


- Experiment 2


Experiment 2 World 1 World 2

World 1 World 2

|A1 A2<br><br>|A˜1 A2|
|---|---|
||x1|
|---|
<br><br>x′1 x2 x′2<br><br>||x˜1|
|---|
<br><br>x′1 xt2 x′2|


|α1 α2<br><br>|α˜1 α2|
|---|---|
|α1 α1′<br><br>α2 α2′<br><br><br>|α˜1 α1′<br>α˜2 α2′<br>|


- Table A.2: Illustration of Salience Effect. Aj and Bj are alternatives, xk denotes the attribute, and αk and βk denotes thesalience.


first comparison.

For Experiment 1, the utility differences in hypothetical World 1 are given by k βkuk(xk) − k βk′ uk(x′k), and in hypothetical World 2, they are j β˜kuk(˜xk) − k βk′ uk(x′k), where x˜2 = x2

and x˜3 = x3. Consequently, the individual treatment effect of attribute X1 can be expressed as:

ICE3 =

=

3

[βkuk(xk) − β˜kuk(˜xk)]

k=1

2

[βkuk(xk) − β˜kuk(˜xk)] + [β3u3(x3) − β˜3u3(˜x3)]

k=1

where the subscript 3 indicates that a total of three attributes are considered in Experiment 1. Similarly, the individual treatment effect for Experiment 2 is

ICE2 =

2

[αkuk(xk) − α˜kuk(˜xk)]

k=1

It is evident that ICE3 includes an additional term [β3u3(x3) − β˜3u3(˜x3)] compared to ICE2. Furthermore, the salience values denoted by β in ICE3 differ from those denoted by α in ICE2. These two factors could lead to ICE3 and ICE2 having different signs.

| | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |


View

- Towels1
- Towels2


Thermon3

- Thermo1
- Thermo2


Sink

- Service1
- Service2
- Service3


- Pillow1
- Pillow2
- Pillow3


Office

Menu

- Linens1
- Linens2


- Lamps1
- Lamps2


Treatment

- Kitchen1
- Kitchen2


Internet

- Hallway1
- Hallway2


Furniture

- Floor1
- Floor2


Fan

Elevators

Closet

- Chocolate1
- Chocolate2
- Chocolate3


- Channels1
- Channels2


Call

- Bar1
- Bar2


4 5 6 7 8 9 10 12 14 18 22

Number of Attributes

Importance 10 20 30

Figure A.1: Testing Hypothesis of Importance Reversal. The horizontal line denotes the number of attributes and each row illustrates the relative importance of each attribute. The darker color represents less importance. The total 385 estimates are from the same model in Bansak et al. (2021).

#### B Design of Candidate-Choice Experiment

This study is pre-registered with the center for Open Science Framework (OSF). An anonymized version along with the questionnaire can be found at the OSF. The survey experiment received full Institutional Review Board (IRB) approval in Study ID [details removed for anonymous peer review] from the authors’ institutions.

##### B.1 Principles for Human Subjects Research

We recruit subjects using the online survey platform, Lucid Theorem, which manages relationships with suppliers who handle incentives to participants directly. Researchers pay Lucid a cost per (currently at $1.50 for a 10–15 minute survey) for a completed interview (CPI) and Lucid pays suppliers who then provide a portion of those earnings to participants in the form of cash, gift cards, or loyalty reward points. Lucid Theorem uses a proportional sampling method to provide nationally representative samples, balancing participants based on age, gender, ethnicity, and region.

Each solicited respondent received a link from the company that redirected them to the actual survey and the consent information, hosted on a server maintained by Qualtrics. Upon completing the survey, respondents are immediately redirected back to the company’s website to claim their reward. All participants received compensation after completing the questionnaires.

In the beginning of the survey, we provided a consent form that laid out clear and comprehensive information about the project, including how data will be collected, used, and stored, the costs and benefits of participation, and contact information for the lead researcher and university IRB. Respondents were also informed that no identifying information would be collected, and that they were able to opt out of the research at any time. Each participant was required to read the consent form before proceeding with the survey (at which point consent was assumed to be granted).

The project did not involve any deception, nor did we intervene in any political processes. The data were obtained in compliance with all relevant regulations and ethical guidelines. The raw data is handled exclusively by the authors, following strict protocols to ensure confidentiality and data

security.

##### B.2 Pre-registered Design

The online anonymized version along with the questionnaire can be found at the OSF.

This study explores how the causal effects derived from conjoint experiments can be inconsistent with the real-world effect due to attention and salience biases. Using a series of candidate choice conjoint experiments, we will randomly vary the numbers of attributes (attention bias) and their levels (salience bias) presented to the respondents and examine the differences in the average marginal component effects (AMCEs) of two key features–gender and age–common across all experimental groups. We expect that the AMCEs will be smaller the more number of attributes are included and larger when the levels of the attributes are more salient.

We conduct two candidate-choice experiment to test hypotheses outlined in the main text. The

sample sizes for both experiments were 1,200, which is determined by our research budget. Study Information Hypotheses

- H1: The AMCEs of a common attribute will be smaller the more number of attributes are

included in the conjoint experiment

- H2: The AMCEs of a common attribute will be larger when the levels of the attributes are more


salient in the conjoint experiment. Part 1: In the firs experiment, respondents see a conjoint table with a hypothetical candidate that is

described by K (=2,4,6,8,10) attributes as shown in the example table below:

We randomly assign participants into one of five groups. For each attribute, levels are also randomly assigned. Each participant completed six rounds of the candidate choice experiment.

- • Group 1: each hypothetical candidate has K=2 attributes including Gender and Age; there are total of 6 rounds for each participant


![image 2](fu-li-2024-generalization-conjoint-attention-salience_images/imageFile2.png)

![image 3](fu-li-2024-generalization-conjoint-attention-salience_images/imageFile3.png)

![image 4](fu-li-2024-generalization-conjoint-attention-salience_images/imageFile4.png)

8

Figure A.2: Caption

![image 5](fu-li-2024-generalization-conjoint-attention-salience_images/imageFile5.png)

Figure A.3: Attribute Table

- • Group 2: each hypothetical candidate has K=4 attributes including Gender, Age, Education, and Tax; there are total of 6 rounds for each participant
- • Group 3: each hypothetical candidate has K=6 attributes including Gender, Age, Education, Tax, Race, and Income; there are total of 6 rounds for each participant
- • Group 4: each hypothetical candidate has K=8 attributes including Gender, Age, Education, Tax, Race, Income, Religion, and Military service; there are total of 6 rounds for each participant
- • Group 5: each hypothetical candidate has K=10 attributes including Gender, Age, Education, Tax, Race, Income, Religion, Military service, Gay Marriage, and Children; there are total of 6 rounds for each participant


Attribute level: Part 2: In the second experiment, respondents are required to complete 5 rounds of candidate choice

experiment similar to the first experiment. However, we control attribute salience in each pair. In

particular, we let some attributes be randomly chosen so that their levels are close to each other. For example, for attribute age = [40,52,60,68,75], only levels (40,52) , (52,60), (60,68), and (68,75) will be randomly chosen. Those levels are age, income, same sex marriage, tax, education, and children.

- • If K=2, attributes are Gender and Age
- • If K=4, attributes are Gender, Age, Tax, and Education.
- • If K=6, attributes are Gender, Age, Tax, Education, Race, and Income.
- • If K=8, attributes are Gender, Age, Tax, Education, Race, Income, Military, and Religion.
- • If K=10, attributes are Gender, Age, Tax, Education, Race, Income, Military, Religion, Same Sex Marriage, and Children.


###### Analysis:

- (1) We will calculate the average marginal component effect (binary and 10-point rate), and

R2 for each attribute in each K group. We also present both results with and without covariate adjustment.

- (2) Check the relationship between AMCE and the number of attributes K by linear regression

and meta-regression.

- (3) Check the relationship between the treatment effect direction (positive, negative) and the

number of attributes K by drawing a heatmap.

- (4) Check the relationship between the treatment effect direction and the number of attributes


K conditional on whether levels are salient or not.

#### C Proof of Proposition 1

Proof. Recall, without loss of generality, we assume that the real-world consideration set is CIr = {X1,X2,...,Xm}, the associated baseline salience is denoted as (αi1,...,αim). The experimental

consideration set is Cis = {X1,X2,...,Xk} and baseline salience is (αi′1,...,αik′ ). We assume the cardinality of Xr, denoted by m, is greater than that of Xe, denoted by k (|Cir| = m > |Cis| = k).

Recall, Di = {j ∈ [1,k]|uij(Xij(z)) ̸= uij(Xij(z′))} ≠ ∅ is the set of attribute index that treatment has effects on individual i.

i∩Di αijuij(Xij(Z)). Therefore, the ICE in the survey experiment is

Under treatment Z, the outcome is Vi(z,E) = j∈C

ICE(z,z′;Es) =

αij(uij(Xij(z)) − uij(Xij(z′))).

j∈Cis∩Di

Note that treatment cannot affect the attributes that are not in the Cis. By assumption 1, Cir ∩ Cis = ∩Cis. Therefore, the ICE in the real world is

αij′ (uij(Xij(z)) − uij(Xij(z′))).

ICE(z,z′;Er) =

j∈Cis∩Di

i∩Di, where some αij ̸= αij′ for some j ∈ Ci∩Di. Because uij(Xij(z)) − uij(Xij(z′)) are not constrained, we treat them as a random draw from an closed interval, and thus the first result holds.

Fix vectors (αij)j∈C

###### i∩Di and (αij′ )∈C

′ ik

αij = α

Under assumption 3, fixing a j ∈ {Ci ∩ Di}, denote δjk = α

α′ij for any k ∈ {Ci ∩ Di}. Therefore,

ik

and

ICE(z,z′;Es) = αij

###### δjk∆uik

k∈Cis∩Di

ICE(z,z′;Er) = αij′

###### δjk∆uik

k∈Cis∩Di

where we use ∆uik to denote uij(Xij(z)) − uij(Xij(z′)). By assumption 3 again, αij′ = αij(1 − mj=k+1 αij′ ). Therefore,

ICE(z,z′;Es) ICE(z,z′;Er)

=

1

k

j=1 α′

ij

Now, we have shown results based on ICE. ACE holds because it is a weighted average of ICE.

| |
|---|


#### D Proof of Proposition 2

Proof. We show existence for the case in which |Cis| = 2 and |Cir| = 3. The general case follows the same logic. Suppose there are two attributes in the consideration set of the survey experiment. Under treatment status Zi = z, we denote the vector by x1 = (ui1(Xi1(z)),ui2(Xi2(z)),0), and the corresponding salience is a = (αi1,αi2,0). Under treatment Zi = z′, we write x′1 = (ui1(Xi1(z′)),ui2(Xi2(z′)),0), with corresponding salience a′ = (αi′1,αi′2,0). Under the assumption, r1(zi) ̸= r1(zi′), and therefore a ̸= a′. Without loss of generality, we assume that the ICE is positive:

ICE(Es) = a · x1 − a′ · x′i > 0 (3)

Similarly, suppose there are three attributes in the consideration set of the real-world experiment. We define x2 = (ui1(Xi1(z)),ui2(Xi2(z)),ui3(Xi3(z))), with corresponding salience

- b = (βi1,βi2,βi3). We define x′2 and b′ analogously. Therefore, we want to show that


###### ICE(Er) = b · x2 − b′ · x′2 < 0 (4)

Note that x2 = x1 + u3 and x′2 = x′1 + u3, where u3 = (0,0,ui3(xi3)). By stable salience, we define k = β

′ i1

αi1 and k′ = β

α′i1. Suppose that k > k′. Then we can write

i1

###### b = ka + b3 and b′ = k′a′ + b′3

where b3 = (0,0,βi3) and b′3 = (0,0,βi′3). Substituting these into equation (4), we obtain

(ka + b3) · (x1 + u3) − (k′a′ + b′3) · (x′1 + u3) < 0 ka · x1 − k′a′ · x′1 + (βi3 − βi′3) · ui3(xi3) < 0

Note that, by stable salience, we have βi3 = 1 − k and βi′3 = 1 − k′. Substituting these into the inequality above, we obtain

###### k(a · x1 − ui3(xi3)) < k′(a′ · x′1 − ui3(xi3))

Also, combining this with equation (3), we conclude that any ui3(xi3) satisfying

a′ · x′1 < a · x1 < ui3(xi3)

a′1 · x′1 − ui3(xi3) a1 · x1 − ui3(xi3)

> 1

can produce effect sign reversal. For k < k′, we simply reverse the inequality sign.

As demonstrated in the proof, we have more “parameters” than constraints, and thus there is considerable flexibility in achieving the desired outcome. Identifying even a single scenario that aligns with our hypothesis is sufficient.

| |
|---|


#### E Proof of Proposition 3

Proof. Following the proof of Proposition 1, we have

ICE(z,z′;Es) ICE(z,z′;Er)

=

1

k

j=1 α′

ij

###### Because kj=1 αij′ > 0, we have sign(ICE(z,z′;Es)) = sign(ICE(z,z′;Er)).

| |
|---|


#### F Tables

Table A.3: Gender Effects Meta-regression

All USA Own

(1) (2) (3) Number −0.0029∗∗∗ −0.0037∗∗∗ −0.0148∗

(0.0009) (0.0037) (0.0054) Intercept 0.0459∗∗∗ 0.0549∗∗∗ 0.1653∗∗ (0.0059) (0.0071) (0.0352)

R2 0.21 0.43 0 τ2 0.0003 0.0003 0

Notes: R2 denotes the amount of heterogeneity accounted for and τ2 is the estimated amount of residual heterogeneity. ∗p<0.1; ∗∗p<0.05; ∗∗∗p<0.01.

Dependent Variable: Preference Score (1) (2) (3) (4) (5)

GenderMale 0.154∗∗ 0.098 0.031 −0.081 −0.018 (0.063) (0.068) (0.067) (0.071) (0.069)

Age52 0.119 −0.041 0.032 0.004 −0.131 (0.099) (0.107) (0.107) (0.112) (0.108)

Age60 −0.162 −0.119 −0.194∗ −0.048 −0.110

- (0.101) (0.107) (0.106) (0.111) (0.109)

Age68 −0.425∗∗∗ −0.331∗∗∗ −0.273∗∗ −0.145 −0.253∗∗

- (0.101) (0.107) (0.107) (0.112) (0.108)


Age75 −1.340∗∗∗ −0.830∗∗∗ −0.566∗∗∗ −0.551∗∗∗ −0.394∗∗∗

(0.101) (0.107) (0.107) (0.112) (0.110) EducationBA from Ivy League University 0.048 −0.027 −0.042 0.045

(0.083) (0.082) (0.087) (0.084) EducationBA from State University 0.076 0.001 −0.036 0.026

- (0.083) (0.081) (0.087) (0.085)

TaxOppose −0.327∗∗∗ −0.374∗∗∗ −0.209∗∗ −0.094

- (0.083) (0.082) (0.087) (0.085)


TaxSupport 0.828∗∗∗ 0.401∗∗∗ 0.213∗∗ 0.327∗∗∗

(0.083) (0.081) (0.087) (0.084) RaceBlack 0.137∗ 0.116 0.037

(0.082) (0.087) (0.084) RaceWhite 0.066 0.163∗ 0.078

(0.082) (0.087) (0.084) Income32,000 −0.080 0.009 −0.159 (0.117) (0.123) (0.119) Income5.1 million −0.347∗∗∗ −0.085 −0.179

(0.116) (0.124) (0.120) Income54,000 −0.030 0.089 0.075

(0.116) (0.123) (0.119) Income65,000 −0.068 0.252∗∗ 0.007

- (0.116) (0.123) (0.119)

Income92,000 −0.051 0.095 −0.030

- (0.117) (0.123) (0.120)


MilitaryServed 0.209∗∗∗ 0.134∗ (0.071) (0.069)

ReligionMormon −0.429∗∗∗ −0.173∗∗

(0.087) (0.084) ReligionProtestant −0.024 0.040

(0.087) (0.084)

- Children1 0.073 (0.107)
- Children2 0.159 (0.110)
- Children3 0.138 (0.107)
- Children4 0.158 (0.109)


MarriageOppose −0.481∗∗∗

- (0.084)

MarriageSupport 0.010

- (0.085)


Constant 6.240∗∗∗ 5.540∗∗∗ 5.813∗∗∗ 5.697∗∗∗ 5.375∗∗∗ (0.078) (0.108) (0.139) (0.161) (0.175)

Observations 6,300 6,187 5,825 5,713 6,180 R2 0.042 0.046 0.025 0.019 0.018 Adjusted R2 0.041 0.044 0.022 0.016 0.014 Residual Std. Error 2.513 (df = 6294) 2.668 (df = 6177) 2.548 (df = 5808) 2.680 (df = 5693) 2.702 (df = 6154) F Statistic 55.115∗∗∗ (df = 5; 6294) 32.840∗∗∗ (df = 9; 6177) 9.211∗∗∗ (df = 16; 5808) 5.947∗∗∗ (df = 19; 5693) 4.481∗∗∗ (df = 25; 6154) Note: ∗p<0.1; ∗∗p<0.05; ∗∗∗p<0.01

###### Table A.4: Full Results for Candidate-Choice Conjoint Experiments

Dependent Variable: Preference Score (1) (2) (3) (4) (5)

genderMale 0.453∗∗∗ 0.098 0.153 0.103 0.272∗∗

(0.101) (0.099) (0.107) (0.097) (0.109) age52 0.088 0.028 −0.398∗∗ −0.151 0.200

(0.173) (0.174) (0.184) (0.174) (0.193) age60 −0.079 0.157 −0.505∗∗∗ −0.001 0.347∗

(0.173) (0.173) (0.184) (0.174) (0.193) age68 −0.366∗∗ 0.128 −0.575∗∗∗ −0.039 0.383∗∗ (0.174) (0.173) (0.186) (0.174) (0.193) age75 −0.855∗∗∗ −0.318 −1.019∗∗∗ −0.385∗ −0.102

(0.205) (0.214) (0.234) (0.212) (0.239) eduBA from Ivy League University −0.792∗∗∗ −0.427∗∗ −0.287∗ 0.096

(0.162) (0.179) (0.163) (0.192) eduBA from State University −0.281∗∗ −0.048 −0.268∗∗ 0.132

(0.126) (0.137) (0.124) (0.143) taxOpposite −0.184 −0.372∗∗∗ −0.483∗∗∗ −0.170

(0.129) (0.140) (0.125) (0.145) taxSupport 1.034∗∗∗ 0.498∗∗∗ 0.342∗∗∗ 0.271∗

(0.126) (0.138) (0.125) (0.143) raceWhite 0.056 0.095 −0.010

(0.108) (0.103) (0.116) income32,000 −0.045 −0.338∗ 0.021

- (0.211) (0.186) (0.214)

income5.1 million −0.260 −0.774∗∗∗ 0.058

- (0.212) (0.189) (0.217)


income54,000 −0.238 −0.344∗∗ 0.024

(0.167) (0.150) (0.171) income65,000 −0.079 0.013 0.078

(0.166) (0.151) (0.170) income92,000 −0.047 −0.250∗ 0.172

(0.165) (0.151) (0.171) miliServed 0.088 0.069

(0.101) (0.114) reliProtestant 0.116 −0.041

(0.110) (0.126) child1 0.320∗

(0.193) child2 0.044

(0.192) child3 0.158

(0.191) child4 −0.285 (0.239)

gayOpposite −0.453∗∗∗

(0.145) gaySupport 0.599∗∗∗ (0.143) Constant 5.707∗∗∗ 5.664∗∗∗ 6.406∗∗∗ 6.071∗∗∗ 4.829∗∗∗ (0.154) (0.180) (0.222) (0.234) (0.300)

Observations 2,373 2,359 2,420 2,775 2,520 R2 0.024 0.086 0.052 0.045 0.046 Adjusted R2 0.022 0.082 0.046 0.039 0.037 Residual Std. Error 2.456 (df = 2367) 2.353 (df = 2349) 2.599 (df = 2404) 2.493 (df = 2757) 2.687 (df = 2496)

- F Statistic 11.462∗∗∗ (df = 5; 2367) 24.485∗∗∗ (df = 9; 2349) 8.762∗∗∗ (df = 15; 2404) 7.611∗∗∗ (df = 17; 2757) 5.228∗∗∗ (df = 23; 2496) Note: ∗p<0.1; ∗∗p<0.05; ∗∗∗p<0.01


###### Table A.5: Full Results for Candidate-Choice Conjoint Experiments (Control Salience)

#### G Figures

![image 6](fu-li-2024-generalization-conjoint-attention-salience_images/imageFile6.png)

![image 7](fu-li-2024-generalization-conjoint-attention-salience_images/imageFile7.png)

![image 8](fu-li-2024-generalization-conjoint-attention-salience_images/imageFile8.png)

| | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|
|0|0|0|0|0|0|0|0|0|0|0| |
| |0.0|3 0|0|0.0|1 0|0|0|0|0|0| |
| |0|0|0|0|0|0|0|0|0|0| |
| | | | | | |0.0|2| |0.0|1 0.0|1|
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | |0.0|7| | | | | | | | |
| |0.0|1 0|0|0|0|0|0|0|0|0| |
| | | | | | |0| | |0.0|9| |
| | | |0.0|1 0.0|3|0.0|1| | |0.0|5|
| | | | | | | | |0.0|8| | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |
| | | | | | | |0.0|4| | | |
| |0.0|5 0|0|0|0|0|0|0|0.0|2 0| |
| | |0.0|2 0|0|0|0|0|0|0|0| |
| | | |0| | | | | | | | |
| |0| |0.0|1| | | |0.|1 0.0|9| |
| |0.0|2 0|0|0|0|0|0|0.0|2 0|0| |
| | |0.0|4|0.|1 0.0|2|0.0|2 0|0|0.0|5|
|0|0|0|0|0|0|0|0|0|0|0| |
| | |0.0|4 0.0|7 0.0|8 0.0|9| | | | | |
| | | | | | | | |0.0|1| | |
|0|0|0|0|0|0|0|0|0|0|0| |
|0.0|3| |0.|1|0.0|1| |0.0|1| | |
| | |0.|1|0| | | | | | | |
| |0.0|1 0.0|4| |0.0|1| | | | | |
| | | |0|0|0.0|1 0|0.|1 0.0|1| | |
| | |0.0|8| | | |0.0|4| | | |
| | | | | | |0.0|1| | | | |
| | | | | | | |0.0|8| | | |
| |0.0|9| | | | | | | | | |
| | | |0.0|5 0.0|4 0|0.0|4 0|0|0|0.0|3|
| | |0.0|6| |0| | | | | | |
| | | | | | |0.0|9 0.0|7| | | |
| | | |0| |0| | |0.0|3|0| |
| | | | | | | |0.0|5| | | |


View

- Towels1
- Towels2


Thermon3

- Thermo1
- Thermo2


Sink

- Service1
- Service2
- Service3


- Pillow1
- Pillow2
- Pillow3


Office

Menu

- Linens1
- Linens2


- Lamps1
- Lamps2


Treatment

- Kitchen1
- Kitchen2


Internet

- Hallway1
- Hallway2


Furniture

- Floor1
- Floor2


Fan

Elevators

Closet

- Chocolate1
- Chocolate2
- Chocolate3


- Channels1
- Channels2


Call

- Bar1
- Bar2


4 5 6 7 8 9 10 12 14 18 22

Number of Attributes

Treatment Effect Negative Positive NA

###### Figure A.4: Testing Hypothesis of Effect Reversal with P-value < 0.1

