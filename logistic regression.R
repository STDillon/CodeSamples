install.packages("data.table")
library("data.table")


train <- read.csv("/Users/yao/Desktop/IST707/project/trainclean.csv",  stringsAsFactors = FALSE)
testing <- read.csv("/Users/yao/Desktop/IST707/project/testing.csv", stringsAsFactors = FALSE)
# drop unused column, "x","x1"
# change column name "Unnamed..0" to "MachineIdentifier"
train[1:5,]
train <- train[,-1]
colnames(train)[colnames(train) == "Unnamed..0"] <- "MachineIdentifier"
testing <- testing[,-1:-2]
colnames(testing)[colnames(testing) == "Unnamed..0"] <- "MachineIdentifier"
colnames(train)
#"HasDetections","MachineIdentifier",
#"Processor","EngineVersion",
#"AppVersion", "SmartScreen",
#"AVProductStatesIdentifierCategory",
#"IeVerIdentifier",
#"Census_PrimaryDiskTotalCapacity",
#"Wdft_IsGamer"
train.raw <- train[, c(62, 3, 18, 4, 27, 8, 26, 35, 60)]
#logistic 
colnames(train.raw)
View(train.raw)
model <- glm(HasDetections ~
               Processor +
               EngineVersion +
               AppVersion +
               SmartScreen +
               AVProductStatesIdentifier +
               IeVerIdentifier +
               Census_PrimaryDiskTotalCapacity +
               Wdft_IsGamer,
             data = train.raw,
             family = "binomial")
gc()

# making prediction
prob <- predict(model, newdata = testing, type = "response")
testing$predict <- prob
View(testing)
