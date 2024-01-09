#!/usr/bin/env Rscript
library(boot)
library(readr)
library(tidyr)
library(dplyr)
library(stringr)
library(MASS)
library(brms)
library(optparse)

option_list = list(
    make_option(c("-e", "--experiment"), type = "integer", default = NULL,
                help = "type of experiment"),
    make_option(c("-i", "--iterations"), type = "integer", default = 3000,
                help = "number of iterations")
)

opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)
options(mc.cores = parallel::detectCores())
ITERATIONS <- opt$iterations
EXP <- opt$experiment

if (!dir.exists("models")) {
    dir.create("models")
}

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
        rm_df$text_domain_numeric == rm_df$reader_domain_numeric &
            rm_df$expert_status_numeric == 1, 1, 0
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
    rm_df$is_expert_technical_term <- as.factor(rm_df$is_expert_technical_term)
    return(rm_df)
}

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
    model <- brm(
        formula = formula,
        data = data_proc,
        family = gaussian(link = "identity"),
        warmup = ITERATIONS / 4,
        iter = ITERATIONS,
        chains = 4,
        cores = 4,
        seed = 123
    )
    return(model)
}

fit_count_model <- function(data, target, predictors) {
    formula <- paste0(target, "~ (1|reader_id) +", predictors)
    model <- brm(
        formula = formula,
        data = data,
        family = poisson(link = "log"),
        warmup = ITERATIONS / 4,
        iter = ITERATIONS,
        chains = 4,
        cores = 4,
        seed = 123
    )
    return(model)
}

fit_binomial_model <- function(data, target, predictors) {
    formula <- paste0(target, "~ (1|reader_id) +", predictors)
    model <- brm(
        formula = formula,
        data = data,
        family = bernoulli(link = "logit"),
        warmup = ITERATIONS / 4,
        iter = ITERATIONS,
        chains = 4,
        cores = 4,
        seed = 123
    )
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
        sd = numeric(),
        ci_lower = numeric(),
        ci_upper = numeric(),
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
        #  save model
        saveRDS(model, paste0("models/", rm, "_", EXP, ".rds"))
        fixed_effects <- fixef(model)
        # split predictor str at "+" into vector
        for (pred in rownames(fixed_effects)) {
            # get estimate, std.error, p.value for each predictor
            estimate <- fixed_effects[pred, "Estimate"]
            sd <- fixed_effects[pred, "Est.Error"]
            ci_lower <- fixed_effects[pred, "Q2.5"]
            ci_upper <- fixed_effects[pred, "Q97.5"]
            #  add to results df
            results <- rbind(results, data.frame(
                reading_measure = rm,
                predictor = pred,
                estimate = estimate,
                sd = sd,
                ci_lower = ci_lower,
                ci_upper = ci_upper,
                significance = ifelse((ci_lower > 0 | ci_upper < 0), "*", "ns")
            ))
        }
        rm(model)
    }
    return(results)
}

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
##########

df <- preprocess(df_raw)

# CONSTANTS
rm_of_interest <- c("RRT", "FPRT", "TFT", "FPReg")
rm_of_interest_test_type <- c(rep("linear", 3), rep("logreg", 1))
rm_df <- data.frame(
    reading_measure = rm_of_interest, test_type = rm_of_interest_test_type
)

# nolint start
experiments <- c(
    "word_length + surprisal + log_freq + expert_in_domain",
    "word_length + surprisal + log_freq + expert_in_domain + is_expert_technical_term",
    "word_length + surprisal + log_freq + expert_in_domain*is_expert_technical_term",
    "word_length + surprisal + log_freq + expert_in_domain + word_length:expert_in_domain + surprisal:expert_in_domain + log_freq:expert_in_domain",
    "word_length + surprisal + log_freq + expert_in_domain + word_length:expert_in_domain + surprisal:expert_in_domain + log_freq:expert_in_domain + is_expert_technical_term",
    "word_length + surprisal + log_freq + expert_in_domain + word_length:expert_in_domain + surprisal:expert_in_domain + log_freq:expert_in_domain + is_expert_technical_term + expert_in_domain:is_expert_technical_term"
)


preds <- experiments[EXP]
results_wordfeat <- fit_models(
    df, rm_df, preds,
    log_transform = TRUE, remove_zeros = TRUE, remove_outliers = TRUE
)
write.csv(results_wordfeat, paste0("results_predictor_set", EXP, ".csv"), row.names = FALSE)
# nolint end