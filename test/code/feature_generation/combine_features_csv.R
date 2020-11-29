data1 <- read.csv("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/sarcasm_gen_features.csv")
data2 <- read.csv("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/sarcasm_emoji.csv")
data3 <- c(data1,data2)
data4 <- read.csv("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/sarcasm_word_embedding_features.csv")
data5 <- c(data3,data4)
write.csv(data5,file = "/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/sarcasm_final_features.csv",row.names = FALSE)



data1 <- read.csv("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/nonsarcasm_gen_features.csv")
data2 <- read.csv("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/nonsarcasm_emoji.csv")
data3 <- c(data1,data2)
data4 <- read.csv("/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/nonsarcasm_word_embedding_features.csv")
data5 <- c(data3,data4)
write.csv(data5,file = "/home/nam/Desktop/NLP/sarcasm_detection/Sarcasm-Detection-Twitter/test/data/nonsarcasm_final_features.csv",row.names = FALSE)