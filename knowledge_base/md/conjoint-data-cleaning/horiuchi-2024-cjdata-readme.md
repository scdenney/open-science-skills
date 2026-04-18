# cjdata

<!-- badges: start -->
<!-- badges: end -->

**cjdata** is a small package for the first two steps necessary in conjoint analysis: read a CSV file downloaded from Qualtrics and make a long-format data frame. There exist other similarly-purported functions in the existing packages, such as <code>cj_tidy()</code> in the **cregg** package and <code>read.qualtrics()</code> in the **cjoint** package. For some researchers, however, these functions may be too "fancy" (or "complicated") for various reasons. They may want to do something much simpler -- just read a CSV file downloaded from Qualtrics and transform wide-format data into long-format data with minimum additional wrangling, which researchers can do *outside* the function. 

Some notes:

* Users should wrangle respondent-level data separately and merge them by each respondent's id.

* The current version assumes that the outcome variable is a binary choice.

* The outcome variables in the CSV file can be either a numerical variable (1 or 2) or a character variable ("Candidate 1", "Candidate 2"). In the latter case, the last character must be {"1", "2"} or {"A", "B"}. (Note: They can be in "zenkaku" in Japanese.)

## Installation

You can install the development version of cjdata from [GitHub](https://github.com/) with:

``` r
# install.packages("devtools")
devtools::install_github("yhoriuchi/cjdata")
```

## Example

This is a basic example which reshapes data (wide-form) for conjoint analysis. The original data set is from *Campus Diversity: The Hidden Consensus* by John Carey, Katie Clayton, and Yusaku Horiuchi (Cambridge University Press, 2020). The complete replication package is available at https://doi.org/10.7910/DVN/KMS5ZY. For more information about the book, see: https://horiuchi.org/diversity/.

```r
library(cjdata)
outcomes <- paste0("Q2.", seq(from = 4, to = 31, by = 3))
cjdata <- reshape_conjoint(exampleData, V1, outcomes)
```

To read the original Qualtrics data (with two rows being used for information about each column), use another function in this package, <code>read_Qualtrics()</code>. For example, 
```r
library(cjdata)
data <- read_Qualtrics("Campus_Diversity_Project__Dartmouth_Faculty_Recruitment.csv")
cjdata <- reshape_conjoint(data, V1, paste0("Q2.", seq(from = 4, to = 31, by = 3))
```
Note: "Campus_Diversity_Project__Dartmouth_Faculty_Recruitment.csv" is downloadable from the "data-raw" folder of this GitHub respository.

