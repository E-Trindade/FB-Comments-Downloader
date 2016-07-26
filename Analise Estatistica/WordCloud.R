library('tm')
library('wordcloud')

com_ds <- read.delim("ComentariosRp.csv", encoding="UTF-8")
PALAVRAS_MAIS_COMUNS <- c('a', 'ante', 'perante', 'após', 'até', 'com', 'contra', 'de', 'desde', 'em', 'entre', 'para', 'por', 'sem', 'sob', 'sobre', 'trás', 'atrás', 'dentro', 'de', 'para', 'com', 'como', 'durante', 'exceto', 'fora', 'mediante', 'salvo', 'segundo', 'senão', 'visto', 'e', 'mas', 'no', 'que', 'porque', 'www', 'https', 'watch', 'não', 'http', '2015-09-30')

msgs <- list(as.character(com_ds$Conteudo))

corpus <- Corpus(VectorSource(msgs))
my_tdm <- TermDocumentMatrix(corpus)
m <- as.matrix(my_tdm)
words <- sort(rowSums(m), decreasing = T)
my_data <- data.frame(word=names(words), freq=words)


# View(my_data)

#Limpando preposicoes e conjuncoes
my_data_clean = my_data[!(my_data$word %in% PALAVRAS_MAIS_COMUNS),]

wordcloud(words=my_data_clean$word, 
          freq=my_data_clean$freq, 
          max.words = 100,
          random.order = F,
          color = brewer.pal(8, 'Dark2'),
          min.freq = 50
          )