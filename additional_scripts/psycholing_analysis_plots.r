#!/usr/bin/env Rscript
library(readr)
library(tidyr)
library(dplyr)
library(stringr)
library(MASS)
library(ggplot2)
library(lemon)
library(brms)


### model analyses
result_files <- list.files(
    pattern = ".csv",
    path = "coefficients/ds",
    full.names = TRUE
)

#  load all files into one data frame and add file name as column
df_results <- do.call(rbind, lapply(result_files, read_csv, col_types = cols()))

results_df <- result_files %>% 
    lapply(read_csv) %>% # read all the files at once
    bind_rows(.id = "id")

# for each reading measure
# for each predictor (except for Intercept)
# back transform
# mean = as.vector(exp(intercept, estimate) * exp(predictor, estimate) - exp(intercept, estimate))[[1]]
# ci_lower = as.vector(exp(intercept, estimate) * exp(predictor, ci_lower) - exp(intercept, estimate))[[1]]
# ci_upper = as.vector(exp(intercept, estimate) * exp(predictor, ci_upper) - exp(intercept, estimate))[[1]]

all_predictors <- unique(results_df$predictor)
# remove intercept from all_predictors
all_predictors <- all_predictors[all_predictors != "Intercept"]
all_reading_measures <- unique(results_df$reading_measure)
for (rm in all_reading_measures) {
    for (pred in all_predictors) {
        # get the intercept
        intercept <- results_df %>% filter((predictor == "Intercept" & reading_measure == rm)) %>% dplyr::select(estimate) %>% pull()
        # get the estimate
        estimate_pulled <- results_df %>% filter(predictor == pred & reading_measure == rm) %>% dplyr::select(estimate) %>% pull()
        # get the ci_lower
        ci_lower_pulled <- results_df %>% filter(predictor == pred & reading_measure == rm) %>% dplyr::select(ci_lower) %>% pull()
        # get the ci_upper
        ci_upper_pulled <- results_df %>% filter(predictor == pred & reading_measure == rm) %>% dplyr::select(ci_upper) %>% pull()
        # back transform
        estimate_new <- as.vector(exp(intercept) * exp(estimate_pulled) - exp(intercept))[[1]]
        ci_lower_new <- as.vector(exp(intercept) * exp(ci_lower_pulled) - exp(intercept))[[1]]
        ci_upper_new <- as.vector(exp(intercept) * exp(ci_upper_pulled) - exp(intercept))[[1]]
        # update the data frame
        results_df <- results_df %>% mutate(
            # replace the estimate
            estimate = ifelse(predictor == pred & reading_measure == rm, estimate_new, estimate),
            # replace the ci_lower
            ci_lower = ifelse(predictor == pred & reading_measure == rm, ci_lower_new, ci_lower),
            # replace the ci_upper
            ci_upper = ifelse(predictor == pred & reading_measure == rm, ci_upper_new, ci_upper)
        )
    }
}


results_df$predictor <- as.factor(results_df$predictor)
levels(results_df$predictor) <- c(
    "Age", "Expert reading", "Expert reading * Reader discipline", "Intercept", "Expert technical term",
    "Log-freq", "Log-freq * Expert reading", "Reader discipline", "Surprisal", "Surprisal * Expert reading",
    "Word length", "Word length * Expert reading"
)

# reorder levels
results_df$predictor <- factor(
    results_df$predictor,
    levels = c(
        "Intercept", "Age", "Expert reading", "Reader discipline", "Expert reading * Reader discipline", "Expert technical term", 
        "Log-freq", "Log-freq * Expert reading",  "Surprisal", "Surprisal * Expert reading",
        "Word length", "Word length * Expert reading"
    )
)

# create new var: "binary" if reading_measure is FPreg, else "continuous"
results_df$reading_measure_binary <- ifelse(
    results_df$reading_measure == "FPReg", "binary", "continuous"
)
results_df$reading_measure_binary <- as.factor(results_df$reading_measure_binary)

# remove intercept
plt_data <- results_df %>% filter(predictor != "Intercept")
# plt_data <- plt_data %>% filter(id == i)
p <- ggplot(
    plt_data,
    aes(
        x = predictor, y = estimate,
        colour = reading_measure, position = "dodge", group = reading_measure
    )
) +
    scale_x_discrete(guide = guide_axis(angle = 25)) +
    # scale_color_manual(values=colors) +
    geom_point(
        # aes(shape=significance), position = position_dodge(width = .5), size = 1.4
        # open circles instead of points
        position = position_dodge(width = .5), size = 0.8, shape = 1
    ) +
    geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper),
        width = .25, position = position_dodge(width = .5), linewidth = 0.4
    ) +
    # facet_wrap(reading_measure ~ .) +
    facet_wrap(reading_measure_binary ~ .,  scales = "free_y", strip.position = "left",
         labeller = as_labeller(c(binary = "Posterior effect estimate (proportions)", continuous = "Posterior effect estimate (ms)") ) )  +
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
    guides(colour = guide_legend(title = "Reading measure")) +
    # scale_shape_manual(values = c("*" =16, "ns"  = 1)) +
    scale_color_brewer(palette="Dark2") +
    guides(shape = "none")


ggsave("plots/pl_analyses_ds.pdf", width = 10, height = 5, dpi = 200)

model_fit <- readRDS("models_new/TFT_new.rds")
conditions <- data.frame(log_freq = 0:500)

var_of_interest <- c(
    "surprisal:expert_in_domain"
)

for (vai in var_of_interest) {
    ce <- conditional_effects(model_fit, effects = vai, select_points = 0.07)
    plt <- plot(ce, points = TRUE, rug = TRUE, theme = theme_light(), point_args = list(size=0.3, alpha=0.7), line_args = list(linewidth=0.5))[[1]] +
    ggplot2::xlim(-1.1, 1.3) + ggplot2::ylim(0, 900) + ggplot2::theme(legend.position = c(0.5,0.85))  +
    ggplot2::theme(axis.text.x = ggplot2::element_text(size = 12), axis.text.y = ggplot2::element_text(size = 12), axis.title = ggplot2::element_text(size = 15)) +
    ggplot2::guides(fill=guide_legend(title=""), colour=guide_legend(title="")) +
    ggplot2::scale_fill_discrete(labels=c("non-expert reading", "expert reading")) +
    ggplot2::scale_color_discrete(labels=c("non-expert reading", "expert reading")) +
    ggplot2::xlab("Surprisal")
    ggsave(paste0("plots/ce_", vai, ".pdf"), plt, width = 5, height = 5, dpi = 100)
}

var_of_interest <- c(
    "log_freq:expert_in_domain"
)

for (vai in var_of_interest) {
    ce <- conditional_effects(model_fit, effects = vai, select_points = 0.07)
    plt <- plot(ce, points = TRUE, rug = TRUE, theme = theme_light(), point_args = list(size=0.3, alpha=0.7), line_args = list(size=0.5))[[1]] +
    ggplot2::theme(legend.position = c(0.7,0.85)) + ggplot2::ylim(0, 900) +ggplot2::xlim(-1.6, 1) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(size = 12), axis.text.y = ggplot2::element_text(size = 12), axis.title = ggplot2::element_text(size = 15)) +
    ggplot2::guides(fill=guide_legend(title=""), colour=guide_legend(title="")) +
    ggplot2::scale_fill_discrete(labels=c("non-expert reading", "expert reading")) +
    ggplot2::scale_color_discrete(labels=c("non-expert reading", "expert reading")) +
    ggplot2::xlab("Log-lemma frequency")
    ggsave(paste0("plots/ce_", vai, ".pdf"), plt, width = 5, height = 5, dpi = 100)
}
 
var_of_interest <- c(
    "word_length:expert_in_domain"
)

for (vai in var_of_interest) {
    ce <- conditional_effects(model_fit, effects = vai, select_points = 0.07)
    plt <- plot(ce, points = TRUE, rug = TRUE, theme = theme_light(), point_args = list(size=0.3, alpha=0.7), line_args = list(size=0.5))[[1]] +
    ggplot2::theme(legend.position = c(0.2,0.85)) + ggplot2::ylim(0, 900) +ggplot2::xlim(-1.2, 1) +
    ggplot2::theme(axis.text.x = ggplot2::element_text(size = 12), axis.text.y = ggplot2::element_text(size = 12), axis.title = ggplot2::element_text(size = 15)) +
    ggplot2::guides(fill=guide_legend(title=""), colour=guide_legend(title="")) +
    ggplot2::scale_fill_discrete(labels=c("non-expert reading", "expert reading")) +
    ggplot2::scale_color_discrete(labels=c("non-expert reading", "expert reading")) +
    ggplot2::xlab("Word length")
    ggsave(paste0("plots/ce_", vai, ".pdf"), plt, width = 5, height = 5, dpi = 100)
}
 