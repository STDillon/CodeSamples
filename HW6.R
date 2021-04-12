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

caret.control <- trainControl(method = "cv", number = 3)

set.seed(13)
rpart.cv <- train(label ~ ., data = train, method = "rpart", trControl = caret.control, tuneLength = 15)
rpart.cv
rpart.best <- rpart.cv$finalModel
rpart.best

fancyRpartPlot(rpart.best)
rsq.rpart(rpart.best)

treee <- predict(rpart.best, newdata = test, type = "class")
treee %>%
  head()

###END DECISION TREE/START NAIVE BAYES###

x = trainNB[,-1]
y = trainNB$label

NB <- naiveBayes(train[,-1],label)
NB
#NB.cv <- train(x,y,'nb', trControl = caret.control)
NB.cv <- train(label ~ ., data = train, method='nb', trControl = caret.control)
NB.cv
NB.best <- NB.cv$finalModel

pred <- predict(NB.best,newdata=test,type="class")
pred %>%
  head()
