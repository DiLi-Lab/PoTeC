#!/usr/bin/env Rscript
library(boot)
library(readr)
library(tidyr)
library(dplyr)
library(stringr)
library(lme4)
library(MASS)
library(brms)
library(ggplot2)
library(lme4)
library(lmerTest)
library(argparse)

rm(list = ls())
# detect all files
files <- list.files(
    pattern = "*tsv",
    path = "eyetracking_data/reading_measures_merged",
    full.names = TRUE
)

#  load all files into one data frame
df_raw <- do.call(rbind, lapply(files, read_tsv, col_types = cols()))

############### !!!! DON'T RUN THIS AFTER NEXT PULL !!!! ################
# switch text domain numeric to biology = 0, physics = 1x
df_raw$text_domain_numeric <- ifelse(
    df_raw$text_domain_numeric == 0, 1, 0
)
############### !!!! DON'T RUN THIS AFTER NEXT PULL !!!! ################)

z_score <- function(x) {
    return((x - mean(x)) / sd(x))
}

remove_outlier <- function(df, measure) {
    # make copy of df
    df_proc <- df
    measure_array <- as.numeric(df_proc[[measure]])
    #  log transform all reading times that are not 0
    measure_array[measure_array != 0] <- log(measure_array[measure_array != 0])
    z_score <- z_score(measure_array)
    abs_z_score <- abs(z_score)
    df_proc$outlier <- abs_z_score > 3
    #  print number of outliers / total number of reading times
    print(paste(sum(df_proc$outlier), "/", length(df_proc$outlier)))
    #  remove outliers
    df_proc <- df_proc[df_proc$outlier == FALSE, ]
    return(df_proc)
}

preprocess <- function(df) {
    rm_df <- df
    rm_df$surprisal <- rm_df$`sent_surprisal_gpt2-large`
    #  generate new column with 1 if reader is expert in domain of text
    rm_df$expert_in_domain <- ifelse(
        rm_df$text_domain_numeric == rm_df$reader_discipline_numeric &
            rm_df$level_of_studies_numeric == 1, 1, 0
    )

    # remove outliers for word features
    rm_df <- remove_outlier(rm_df, "surprisal")
    rm_df <- remove_outlier(rm_df, "annotated_type_frequency_normalized")
    rm_df <- remove_outlier(rm_df, "word_length")

    # get rid of 0s in annotated type frequency
    rm_df <- rm_df[rm_df$annotated_type_frequency_normalized != 0, ]
    rm_df$log_freq <- log(rm_df$annotated_type_frequency_normalized)
    
    # standardize predictors: surprisal, log_freq, word_length
    rm_df <- rm_df %>%
    mutate(
        surprisal = scale(surprisal),
        log_freq = scale(log_freq),
        word_length = scale(word_length)
    )

    rm_df$reader_id <- as.factor(rm_df$reader_id)
    rm_df$expert_in_domain <- as.factor(rm_df$expert_in_domain)
    return(rm_df)
}

df <- preprocess(df_raw)
#  check if difference in exp. vs non. exp

fit_linear_model <- function(
        data, target, predictors,
        log_transform = FALSE, remove_zeros = FALSE, remove_outliers = FALSE) {
    data_proc <- data
    if (remove_zeros) {
        data_proc <- data[data[[target]] != 0, ]
    }
    if (remove_outliers) {
        data_proc <- remove_outlier(data_proc, target)
    }
    # log transform target variable if not 0
    if (log_transform) {
        data_proc[[target]] <- ifelse(
            data_proc[[target]] == 0, 0, log(data_proc[[target]]))
    }
    formula <- paste0(target, "~ (1|reader_id) +", predictors)
    model <- lmerTest::lmer(formula, data = data_proc)
    return(model)
}

fit_count_model <- function(data, target, predictors) {
    formula <- paste0(target, "~ (1|reader_id) +", predictors)
    model <- glmer(formula, data = data, family = poisson)
    return(model)
}

fit_binomial_model <- function(data, target, predictors) {
    formula <- paste0(target, "~ (1|reader_id) +", predictors)
    model <- glmer(formula, data = data, family = binomial,
                   control = glmerControl(optimizer = "bobyqa"))
    return(model)
}

fit_model <- function(data, data_type, target, predictors,
                      log_transform = FALSE, remove_zeros = FALSE, 
                      remove_outliers = FALSE) {
    if (data_type == "logreg") {
        model <- fit_binomial_model(data, target, predictors)
    } else if (data_type == "count") {
        model <- fit_count_model(data, target, predictors)
    } else if (data_type == "linear") {
        model <- fit_linear_model(
            data, target, predictors,
            log_transform, remove_zeros, remove_outliers
        )
        return(model)
    }
}

fit_models <- function(df, reading_measure_df, predictors,
                       log_transform = FALSE, remove_zeros = FALSE,
                       remove_outliers = FALSE) {
    results <- data.frame(
        reading_measure = character(),
        estimate = numeric(),
        std.error = numeric(),
        p.value = numeric(),
        predictor = character(),
        significance = character()
    )
    #  fit models for each reading measure
    for (i in seq_len(nrow(reading_measure_df))) {
        #  get reading measure and test type
        rm <- reading_measure_df$reading_measure[i]
        test_type <- reading_measure_df$test_type[i]
        #  fit model
        model <- fit_model(
            df, test_type, rm, predictors,
            log_transform, remove_zeros, remove_outliers
        )
        #  get summary
        summary <- summary(model)$coefficients
        # split predictor str at "+" into vector
        predictor_list <- strsplit(predictors, "\\s+\\+\\s+")[[1]]
        # replace expert_in_domain with expert_in_domain1
        predictor_list <- gsub(
            "expert_in_domain", "expert_in_domain1", predictor_list)
        for (pred in predictor_list) {
            #  get estimate, std.error, p.value for each predictor
            estimate <- summary[pred, 1]
            std_error <- summary[pred, 2]
            p.value <- summary[pred, ncol(summary)]
            #  add to results df
            results <- rbind(results, data.frame(
                reading_measure = rm,
                predictor = pred,
                estimate = estimate,
                std_error = std_error,
                p.value = p.value,
                significance = ifelse(p.value < 0.05, "*", " ")
            ))
        }
    }
    return(results)
}

# CONSTANTS
rm_of_interest <- c("RRT", "FPRT", "TFT", "FPReg")
rm_of_interest_test_type <- c(rep("linear", 3), rep("logreg", 1))
rm_df <- data.frame(
    reading_measure = rm_of_interest, test_type = rm_of_interest_test_type
)

## Experiment 1: rm ~ (1|subjId) + surprisal + log_freq + word_length + expert_in_domain
wf_preds <- "word_length + surprisal + log_freq + expert_in_domain"
results_wordfeat <- fit_models(
    df, rm_df, wf_preds, 
    log_transform = TRUE, remove_zeros = TRUE, remove_outliers = TRUE)
write.csv(results_wordfeat, "results_wordfeat.csv", row.names = FALSE)

## Experiment 2: rm ~ (1|subjId) + surprisal + log_freq + word_length + expert_in_domain
exp_preds <- "expert_in_domain"
results_exp <- fit_models(df, rm_df, exp_preds)