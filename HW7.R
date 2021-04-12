library(dplyr)
library(tidyverse)
library(rpart)
library(RColorBrewer)
library(gbm)
library(rpart.plot)
library(caret)
library(fancyRpartPlot)
library(rattle)
library(e1071)
library(h2o)
setwd("C:/School/IST707")

df <- read.csv("kagtrain.csv")
train <- sample_n(df, 1400)
test <- read.csv("kagtest.csv")
testDT <- test
testNB <- test
train1 <- train
train1$label <- NULL
train <- train %>% 
  mutate(label = as.factor(label))

label <- as.factor(train[,1])

control <- trainControl(method = "cv", number = 3)

set.seed(13)
svm <- train(x3,y,method = "svmRadial",trControl = control)

#set.seed(2019)
#fx_knn <- train(x3,y,
#               method = "knn",
               trControl = control)

