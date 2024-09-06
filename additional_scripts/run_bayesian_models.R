#!/usr/bin/env Rscript
suppressPackageStartupMessages({
    library(boot)
    library(readr)
    library(tidyr)
    library(dplyr)
    library(stringr)
    library(MASS)
    library(brms)
    library(optparse)
    library(cmdstanr)
})

option_list = list(
    make_option(c("-i", "--iterations"), type = "integer", default = 4000,
                help = "number of iterations"),
    make_option(c("-r", "--respvar"), type = "integer", default = 1,
                help = "response variable"),
    make_option(c("-d", "--downsample"), type = "logical", default = FALSE,
                help = "downsample oldest and youngest readers")
)

opt_parser <- OptionParser(option_list = option_list)
opt <- parse_args(opt_parser)
options(mc.cores = parallel::detectCores())
ITERATIONS <- opt$iterations

resp_var <- opt$respvar
downsample <- opt$downsample

preprocess <- function(df) {
    rm_df <- df
    rm_df$surprisal <- rm_df$`sent_surprisal_gpt2-large`
    #  generate new column with 1 if reader is expert in domain of text
    rm_df$expert_in_domain <- ifelse(
        rm_df$text_domain_numeric == rm_df$reader_domain_numeric &
            rm_df$expert_status_numeric == 1, 1, 0
    )

    # min type freq that is not 0
    min_freq <- min(rm_df$lemma_frequency_normalized[rm_df$lemma_frequency_normalized > 0])
    # set 0 values to min_freq
    rm_df$lemma_frequency_normalized <- ifelse(
        rm_df$lemma_frequency_normalized == 0, min_freq,
        rm_df$lemma_frequency_normalized
    )
    rm_df$log_freq <- log(rm_df$lemma_frequency_normalized)

    # make age numeric
    rm_df$age <- as.numeric(rm_df$age)
    # standardize predictors: surprisal, log_freq, word_length
    rm_df <- rm_df %>%
        mutate(
            surprisal = scale(surprisal),
            log_freq = scale(log_freq),
            word_length = scale(word_length),
            age = scale(age)
        )

    rm_df$reader_id <- as.factor(rm_df$reader_id)
    rm_df$expert_in_domain <- as.factor(rm_df$expert_in_domain)
    rm_df$reader_domain_numeric <- as.factor(rm_df$reader_domain_numeric)
    rm_df$is_expert_technical_term <- as.factor(rm_df$is_expert_technical_term)
    return(rm_df)
}


fit_linear_model <- function(data, target, predictors) {
    data_proc <- data
    formula <- paste0(target, "~ (1|reader_id) +", predictors)
    data_proc <- data[data[[target]] != 0, ]
    model <- brm(
        formula = formula,
        data = data_proc,
        family = lognormal(),
        prior = c(
            prior(normal(6, 1.5), class = Intercept),
            prior(normal(0, 1), class = sigma),
            prior(normal(0, 1), class = b, coef = surprisal),
            prior(normal(0, 1), class = b, coef = log_freq),
            prior(normal(0, 1), class = b, coef = word_length),
            prior(normal(0, 1), class = b, coef = age)
        ),
        warmup = ITERATIONS / 4,
        iter = ITERATIONS,
        chains = 4,
        cores = 4,
        seed = 123,
        backend = "cmdstanr"
    )
    return(model)
}

fit_binomial_model <- function(data, target, predictors) {
    formula <- paste0(target, "~ (1|reader_id) +", predictors)
    model <- brm(
        formula = formula,
        data = data,
        family = bernoulli(link = "logit"),
        prior = c(
            prior(normal(0, 4), class = Intercept),
            prior(normal(0, 1), class = b, coef = surprisal),
            prior(normal(0, 1), class = b, coef = log_freq),
            prior(normal(0, 1), class = b, coef = word_length),
            prior(normal(0, 1), class = b, coef = age)
        ),
        warmup = ITERATIONS / 4,
        iter = ITERATIONS,
        chains = 4,
        cores = 4,
        seed = 123,
        backend = "cmdstanr"
    )
    return(model)
}

fit_model <- function(data, data_type, target, predictors) {
    if (data_type == "logreg") {
        model <- fit_binomial_model(data, target, predictors)
    } else if (data_type == "count") {
        model <- fit_count_model(data, target, predictors)
    } else if (data_type == "linear") {
        model <- fit_linear_model(
            data, target, predictors
        )
        return(model)
    }
}

fit_models <- function(df, reading_measure_df, predictors) {
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
            df, test_type, rm, predictors
        )
        #  save model
        saveRDS(model, paste0("models/", rm, "_ds.rds"))
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

if (downsample == TRUE) {
    df_raw <- df_raw[!is.na(df_raw$age), ]
    oldest <- df_raw %>%
        dplyr::select(age, reader_id) %>%
        distinct() %>%
        arrange(desc(age))

    # get ids of 16 oldest
    oldest_ids <- oldest$reader_id[1:16]
    # remove oldest readers from df_raw
    df_raw <- df_raw[!df_raw$reader_id %in% oldest_ids, ]

    # remove 4 youngest
    youngest <- df_raw %>%
        dplyr::select(age, reader_id) %>%
        distinct() %>%
        arrange(age)

    # get ids of 4 youngest
    youngest_ids <- youngest$reader_id[1:4]
    # remove youngest readers from df_raw
    df_raw <- df_raw[!df_raw$reader_id %in% youngest_ids, ]
}

df <- preprocess(df_raw)

# CONSTANTS
rm_of_interest <- c("RRT", "FPRT", "TFT", "FPReg")
rm_of_interest_test_type <- c(rep("linear", 3), rep("logreg", 1))
rm_of_interest <- rm_of_interest[resp_var]
rm_of_interest_test_type <- rm_of_interest_test_type[resp_var]
rm_df <- data.frame(
    reading_measure = rm_of_interest, test_type = rm_of_interest_test_type
)

# nolint start
preds <- "word_length + surprisal + log_freq + age + expert_in_domain + reader_domain_numeric + expert_in_domain:reader_domain_numeric + word_length:expert_in_domain + surprisal:expert_in_domain + log_freq:expert_in_domain + is_expert_technical_term"
# nolint end

results_wordfeat <- fit_models(
    df, rm_df, preds
)
write.csv(results_wordfeat, paste0("coefficients/results_predictor_coefficients", resp_var, ".csv"), row.names = FALSE)
