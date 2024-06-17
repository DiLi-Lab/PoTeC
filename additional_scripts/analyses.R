#!/usr/bin/env Rscript
library(boot)
library(readr)
library(tidyr)
library(dplyr)
library(stringr)
library(MASS)
library(ggplot2)
library(lemon)

# detect all files
files <- list.files(
    pattern = "*tsv",
    path = "eyetracking_data/reader_rm_wf",
    full.names = TRUE
)

#  load all files into one data frame
df_raw <- do.call(rbind, lapply(files, read_tsv, col_types = cols()))


preprocess <- function(rm_df) {
    #  generate new column with 1 if reader is expert in domain of text
    rm_df$expert_in_domain <- ifelse(
        rm_df$text_domain_numeric != rm_df$reader_domain_numeric &
            rm_df$expert_status_numeric == 1, 1, 0
    )

    # smooth type_freq_normalized: add 1 to all values
    rm_df$type_frequency_normalized <- rm_df$type_frequency_normalized + 1
    # check if 0 in type_freq_normalized
    # sum(df$type_frequency_normalized == 0)
    rm_df$log_freq <- log(rm_df$type_frequency_normalized)

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

rm <- colnames(df)[55:73]
# compute absolute values for all columns in rm for df
df[, rm] <- abs(df[, rm])

#  compute mean and standard deviation of reading measures for
# each participant and text
rm_per_reader_text <- df %>%
    group_by(reader_id, text_id) %>%
    summarize(
        expert_status_numeric = unique(expert_status_numeric),
        domain_expert_status_numeric = unique(domain_expert_status_numeric),
        across(rm, .fns = list(mean = mean, sd = sd), na.rm = TRUE)
    )


# TODO include text_domain_numeric?
rm_per_reader <- df %>%
    group_by(reader_id) %>%
    summarize(
        expert_status_numeric = unique(expert_status_numeric),
        domain_expert_status_numeric = unique(domain_expert_status_numeric),
        across(rm, .fns = list(mean = mean, sd = sd), na.rm = TRUE)
    )


df_reader_features <- df[, c("reader_id", "expert_in_domain", rms)]
df_reader_features$expert_in_domain <- ifelse(
    df_reader_features$expert_in_domain == 1, "expert", "non-expert"
)
df_reader_features$expert_in_domain <- as.factor(
    df_reader_features$expert_in_domain
)
df_reader_features$expert_in_domain <- factor(
    df_reader_features$expert_in_domain,
    levels = c("non-expert", "expert")
)

rm_per_reader <- df_reader_features %>%
    group_by(reader_id, expert_in_domain) %>%
    summarize(
        across(rms, .fns = list(mean = mean, sd = sd), na.rm = TRUE)
    )

reader_characteristics_long <- gather(
    rm_per_reader, "feature", "value",
    -expert_in_domain, -reader_id
)

rm_plot <- ggplot(reader_characteristics_long, aes(
    x = factor(0),
    y = value,
    fill = expert_in_domain
)) +
    geom_boxplot() +
    xlab("Measures") +
    ylab("") +
    facet_wrap(. ~ feature, scales = "free") +
    theme_light()
ggsave("plots/reader_characteristics_together.png", width = 12, height = 12, dpi = 400)


##  WITH BIO/PHYS
df_reader_features <- df[, c("reader_id", "expert_in_domain", "text_domain_numeric", rms)]

#  recode expert in domain to expert and non-expert
df_reader_features$expert_in_domain <- ifelse(
    df_reader_features$expert_in_domain == 1, "Expert reading", "Non-expert reading"
)
df_reader_features$expert_in_domain <- as.factor(
    df_reader_features$expert_in_domain
)
df_reader_features$expert_in_domain <- factor(
    df_reader_features$expert_in_domain,
    levels = c("Non-expert reading", "Expert reading")
)
df_reader_features$text_domain_numeric <- ifelse(
    df_reader_features$text_domain_numeric == 0, "Biology", "Physics"
)
df_reader_features$text_domain_numeric <- as.factor(
    df_reader_features$text_domain_numeric
)

rm_per_reader <- df_reader_features %>%
    group_by(reader_id, expert_in_domain, text_domain_numeric) %>%
    summarize(
        across(rms, .fns = list(mean = mean, sd = sd), na.rm = TRUE)
    )

include_rm <- c("TFT_mean", "FPRT_mean", "FPReg_mean", "RR_mean", "Fix_mean", "FRT_mean")
#  remove all columns after expert_in_domain that are not in include_rm
rm_per_reader <- rm_per_reader[, c("reader_id", "expert_in_domain", "text_domain_numeric", include_rm)]

reader_characteristics_long <- gather(
    rm_per_reader, "feature", "value",
    -expert_in_domain, -reader_id, -text_domain_numeric
)

rm_plot <- ggplot(reader_characteristics_long, aes(
    x = text_domain_numeric,
    y = value,
    fill = expert_in_domain
)) +
    geom_boxplot() +
    xlab("Reading measures") +
    ylab("") +
    scale_fill_discrete(name = "Reading type") +
    facet_wrap(. ~ feature, scales = "free") +
    theme_light()
ggsave("plots/reader_characteristics.png", width = 10, height = 8, dpi = 300)

# print textfeat_summary to csv
write.csv(textfeat_summary, "textfeat_summary.csv", row.names = FALSE)

### text feats


# detect all files
stim_files <- list.files(
    pattern = "surprisal*",
    path = "stimuli/word_features",
    full.names = TRUE
)

#  load all files into one data frame
stim_df <- do.call(rbind, lapply(stim_files, read_tsv, col_types = cols()))

# convert annotated type frequency to log
stim_df$log_freq <- log(stim_df$annotated_type_frequency_normalized)
#  text characteristics
# mean and sd surprisal, word length, word frequency
word_features <- c(
    "word", "text_id", "surprisal", "log_freq", "word_length"
)

# subset df with only word features
df_word_features <- stim_df[, word_features]

#  new variable with text domain. if text_id contains b, biology, else physics
df_word_features$text_domain <- ifelse(
    str_detect(df_word_features$text_id, "b"), "Biology", "Physics"
)

# rename word features
colnames(df_word_features)[3:5] <- c("Surprisal", "Log-frequency", "Word length")

text_characteristics_long <- gather(
    df_word_features, "feature", "value", -word, -text_id, -text_domain
)

text_characteristics_long$text_domain <- as.factor(
    text_characteristics_long$text_domain
)
textchar_plot <- ggplot(text_characteristics_long, aes(
    x = factor(0), y = value, fill = text_domain
)) +
    geom_boxplot() +
    xlab("Text features") +
    ylab("") +
    facet_wrap(. ~ feature, scales = "free") +
    scale_fill_discrete(name = "Text domain") +
    theme_light() +
    theme(axis.text.x = element_blank())
ggsave("plots/text_characteristics.png", width = 8, height = 4, dpi = 200)


textfeat_summary <- df_word_features %>%
    group_by(text_domain) %>%
    summarize(
        across(word_features[3:5], .fns = list(mean = mean, sd = sd), na.rm = TRUE)
    )


### model analyses
result_files <- list.files(
    pattern = ".*csv",
    path = "analyses/",
    full.names = TRUE
)

#  load all files into one data frame and add file name as column
df_results <- do.call(rbind, lapply(result_files, read_csv, col_types = cols()))

results_df <- result_files %>% 
    lapply(read_csv) %>% # read all the files at once
    bind_rows(.id = "id")

results_df$predictor <- as.factor(results_df$predictor)
levels(results_df$predictor) <- c(
    "Expert reading", "Expert reading * Reader discipline", "Intercept", "Expert technical term",
    "Log-freq", "Log-freq * Expert reading", "Reader discipline", "Surprisal", "Surprisal * Expert reading",
    "Word length", "Word length * Expert reading"
)

# reorder levels
results_df$predictor <- factor(
    results_df$predictor,
    levels = c(
        "Intercept", "Expert reading", "Reader discipline", "Expert reading * Reader discipline", "Expert technical term", 
        "Log-freq", "Log-freq * Expert reading",  "Surprisal", "Surprisal * Expert reading",
        "Word length", "Word length * Expert reading"
    )
)

# create new var: "binary" if reading_measure is FPreg, else "continuous"
results_df$reading_measure_binary <- ifelse(
    results_df$reading_measure == "FPReg", "binary", "continuous"
)
results_df$reading_measure_binary <- as.factor(results_df$reading_measure_binary)

for (i in 1:4) {
    # remove intercept
    plt_data <- results_df %>% filter(predictor != "Intercept")
    plt_data <- plt_data %>% filter(id == i)

    p <- ggplot(
        plt_data,
        aes(
            x = predictor, y = estimate,
            colour = reading_measure, position = "dodge"
        )
    ) +
        scale_x_discrete(guide = guide_axis(angle = 25)) +
        # scale_color_manual(values=colors) +
        geom_point(
            position = position_dodge(width = .5), size = 1.2, shape = 20
        ) +
        geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper),
            width = .25, position = position_dodge(width = .5), linewidth = 0.4
        ) +
        # facet_wrap(reading_measure ~ .) +
        facet_wrap(reading_measure_binary ~ .,  scales = "free_y", strip.position = "left",
             labeller = as_labeller(c(binary = "Posterior effect estimate (log-odds)", continuous = "Posterior effect estimate (log-ms)") ) )  +
        ylab(NULL) +
        theme(strip.background = element_blank(),
           strip.placement = "outside") +
        geom_hline(yintercept = 0, linetype = "dashed", color = "grey51") +
        xlab("Predictor") +
        # ylab("Posterior effect estimate") +
        theme_light() +
        # decrease font size of x axis ticks
        # theme(axis.text.x = element_text(size = 6)) +
        # change color of fill
        theme(legend.position = "top", legend.box = "horizontal") +
        guides(colour = guide_legend(label.position = "bottom")) +
        guides(colour = guide_legend(title = "Reading measure"))
    ggsave(paste0("plots/lmm_", i, ".jpeg"), width = 10, height = 5, dpi = 200)
}
 