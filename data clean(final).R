ibm <- read.csv("/Users/yao/downloads/IBM HR Data.csv", header = T, stringsAsFactors = F)
#View(ibm)
dim(ibm)
str(ibm)


#drop na value
#convet empty cell into NA
ibm[ibm==""] <- NA
ibm = ibm[complete.cases(ibm),]



# convert attrition into numbers
#curremt employee: 0
# others :1
unique(ibm$Attrition)
library(dplyr)
ibm$Attrition=dplyr::recode(ibm$Attrition, "Voluntary Resignation"='1', "Current employee"='0', "Termination"='1')
#View(ibm)
unique(ibm$Attrition)
str(ibm)

# convert gender into binary
#male : 1 
#female : 0
ibm$Gender=dplyr::recode(ibm$Gender, "Male"='1', "Female"='0')
unique(ibm$Gender)

# convert OVER 18 into binary
# yes: 1
# no: 0
ibm$Over18 = dplyr::recode(ibm$Over18, "Y"='1', "N" = '0')
unique(ibm$Over18)
#convert overtime into binary
# yes: 1
# no : 0
ibm$OverTime = dplyr::recode(ibm$OverTime, "Yes" = '1', "No" = "0")
unique(ibm$OverTime)

# one hot encode for the rest of categorical variables
# before one hot encoding, change target column type into factor
str(ibm)
ibm$BusinessTravel <- as.factor(ibm$BusinessTravel)
ibm$Department <- as.factor(ibm$Department)
ibm$MaritalStatus <- as.factor(ibm$MaritalStatus)
ibm$JobRole <- as.factor(ibm$JobRole)
ibm$Employee.Source <- as.factor(ibm$Employee.Source)
ibm$EducationField <- as.factor(ibm$EducationField)
ibm$NumCompaniesWorked <- as.factor(ibm$NumCompaniesWorked)
str(ibm)

install.packages("data.table")
install.packages("mltools")
library(data.table)
library(mltools)
ibm <- as.data.table(ibm)
ibm_oh <- one_hot(ibm)    
View(ibm_oh)

dim(ibm_oh)
str(ibm_oh)
#joblevel right skewed
hist(as.numeric(ibm_oh$JobLevel))

#monthly income right skewed
hist(as.numeric(ibm_oh$MonthlyIncome))
#numcompanies worked right skewed
hist(as.numeric(ibm_oh$NumCompaniesWorked))
#percent salary hike right skewed
hist(as.numeric(ibm_oh$PercentSalaryHike))
#stock option level right skewed
hist(as.numeric(ibm_oh$StockOptionLevel))
#year at company right skewed
hist(as.numeric(ibm_oh$YearsAtCompany))
#year since last promotion right skewed
hist(as.numeric(ibm_oh$YearsSinceLastPromotion))

# Delete standard hours, over 18, employee count
# because there value in each column is same
ibm_oh <- ibm_oh[,-c("EmployeeCount", "Over18", "StandardHours","Application.ID")]
str(ibm_oh)
#change target variable type into factor
ibm_oh$Attrition <- factor(ibm_oh$Attrition)
ibm_oh$DistanceFromHome <- as.integer(ibm_oh$DistanceFromHome)
ibm_oh$EmployeeNumber <- as.integer(ibm_oh$EmployeeNumber)
ibm_oh$Gender <- as.integer(ibm_oh$Gender)
ibm_oh$HourlyRate <- as.integer(ibm_oh$HourlyRate)
ibm_oh$JobSatisfaction <- as.integer(ibm_oh$JobSatisfaction)
ibm_oh$MonthlyIncome <- as.integer(ibm_oh$MonthlyIncome)
ibm_oh$OverTime <- as.integer(ibm_oh$OverTime)
ibm_oh$PercentSalaryHike <- as.integer(ibm_oh$PercentSalaryHike)

write.csv(ibm_oh, "/Users/yao/Desktop/IST707/hw8-final/ibm.csv")
# set train and test data
str(ibm_oh)
install.packages("caTools")
#library(caTools)
#set.seed(123)
split <- floor(nrow(ibm_oh)*0.75)

ibm_oh <- ibm_oh[sample(nrow(ibm_oh)),]
ibm_train <- ibm_oh[1:split, ]
ibm_test <- ibm_oh[(split+1):nrow(ibm_oh),]

# check the count of unique value in the target variable
as.data.frame(table(ibm_train$Attrition))

# loading DMwR to balance the unbalanced class
install.packages("DMwR")
library(DMwR)

#Smote : synthetic minorith oversampling thechnique to handle
# class imbalancy in binary classification

ibm_train_balance <- SMOTE(Attrition ~., ibm_train, perc.over = 200, k=5)
as.data.frame(table(ibm_train_balance$Attrition))

install.packages("caret")
library(caret)

log_ibm <- glm(Attrition~. , data = ibm_train_balance, family = binomial)
summary(log_ibm)

#delete column with high p value

log_predict <- predict(log_ibm, ibm_test, type = 'response')
?predict()


#confusion matrix
table(ibm_test$Attrition, log_predict > 0.5)

#ROC cureve
#install.packages("ROCR")
library(ROCR)
rocpred <- prediction(log_predict, ibm_test$Attrition)
rocperf <- performance(rocpred, 'tpr', 'fpr')
plot(rocperf, colorize = TRUE, text.adj =c(-0.2,1.7))

# ramdon forest 
install.packages('randomForest')
install.packages("e1071")
library('randomForest')
library('e1071')

rf_ibm <- randomForest(Attrition~., ntree = 100,
                       data = ibm_train_balance)

