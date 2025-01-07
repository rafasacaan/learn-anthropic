# Chunking Strategies for LLM Applications
Taken from [pinecone](https://www.pinecone.io/learn/chunking-strategies/)


Finding the optimal chunk size for the documents in the corpus is crucial to ensuring that the search results are accurate and relevant.

As a rule of thumb, if the chunk of text makes sense without the surrounding context to a human, it will make sense to the language model as well


# Embedding short and long content

The length of the query also influences how the embeddings relate to one another. A shorter query, such as a single sentence or phrase, will concentrate on specifics and may be better suited for matching against sentence-level embeddings.

A longer query that spans more than one sentence or a paragraph may be more in tune with embeddings at the paragraph or document level because it is likely looking for broader context or themes.


# Chunking Considerations


1. **What is the nature of the content being indexed?** Are you working with long documents, such as articles or books, or shorter content, like tweets or instant messages? The answer would dictate both which model would be more suitable for your goal and, consequently, what chunking strategy to apply.

2. **Which embedding model are you using, and what chunk sizes does it perform optimally on?** For instance, sentence-transformer models work well on individual sentences, but a model like text-embedding-ada-002 performs better on chunks containing 256 or 512 tokens.

3. **What are your expectations for the length and complexity of user queries? Will they be short and specific or long and complex?** This may inform the way you choose to chunk your content as well so that there’s a closer correlation between the embedded query and embedded chunks.

4. **How will the retrieved results be utilized within your specific application?** For example, will they be used for semantic search, question answering, summarization, or other purposes? For example, if your results need to be fed into another LLM with a token limit, you’ll have to take that into consideration and limit the size of the chunks based on the number of chunks you’d like to fit into the request to the LLM.


# Chunking methods

## Fixed-size chunking

This is the most common and straightforward approach to chunking: we simply decide the number of tokens in our chunk and, optionally, whether there should be any overlap between them. In general, we will want to keep some overlap between chunks to make sure that the semantic context doesn’t get lost between chunks. Fixed-sized chunking will be the best path in most common cases. Compared to other forms of chunking, fixed-sized chunking is computationally cheap and simple to use since it doesn’t require the use of any NLP libraries.

Example using LangChain.
```
text = "..." # your text

from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator = "\n\n",
    chunk_size = 256,
    chunk_overlap  = 20
)
docs = text_splitter.create_documents([text])
```

## “Content-aware” Chunking

These are a set of methods for taking advantage of the nature of the content we’re chunking and applying more sophisticated chunking to it. Here are some examples:

### 1. Sentence splitting
As we mentioned before, many models are optimized for embedding sentence-level content. Naturally, we would use sentence chunking, and there are several approaches and tools available to do this, including:

- **Naive splitting**: The most naive approach would be to split sentences by periods (“.”) and new lines. While this may be fast and simple, this approach would not take into account all possible edge cases. Here’s a very simple example:

```
text = "..." # your text
docs = text.split(".")
```
- **NLTK**: The Natural Language Toolkit (NLTK) is a popular Python library for working with human language data. It provides a sentence tokenizer that can split the text into sentences, helping to create more meaningful chunks. For example, to use NLTK with LangChain, you can do the following:

```
text = "..." # your text
from langchain.text_splitter import NLTKTextSplitter
text_splitter = NLTKTextSplitter()
docs = text_splitter.split_text(text)
```

- **spaCy**: spaCy is another powerful Python library for NLP tasks. It offers a sophisticated sentence segmentation feature that can efficiently divide the text into separate sentences, enabling better context preservation in the resulting chunks. For example, to use spaCy with LangChain, you can do the following:

```
text = "..." # your text
from langchain.text_splitter import SpacyTextSplitter
text_splitter = SpaCyTextSplitter()
docs = text_splitter.split_text(text)
```

### 2. Recursive chunking

Recursive chunking divides the input text into smaller chunks in a hierarchical and iterative manner using a set of separators. If the initial attempt at splitting the text doesn’t produce chunks of the desired size or structure, the method recursively calls itself on the resulting chunks with a different separator or criterion until the desired chunk size or structure is achieved. This means that while the chunks aren’t going to be exactly the same size, they’ll still “aspire” to be of a similar size.

```
text = "..." # your text
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 256,
    chunk_overlap  = 20
)

docs = text_splitter.create_documents([text])
```

### 3. Specialized chunking
Markdown and LaTeX are two examples of structured and formatted content you might run into. In these cases, you can use specialized chunking methods to preserve the original structure of the content during the chunking process.

- **Markdown**: Markdown is a lightweight markup language commonly used for formatting text. By recognizing the Markdown syntax (e.g., headings, lists, and code blocks), you can intelligently divide the content based on its structure and hierarchy, resulting in more semantically coherent chunks. For example:

```
from langchain.text_splitter import MarkdownTextSplitter
markdown_text = "..."

markdown_splitter = MarkdownTextSplitter(chunk_size=100, chunk_overlap=0)
docs = markdown_splitter.create_documents([markdown_text])
```

- **LaTex**: LaTeX is a document preparation system and markup language often used for academic papers and technical documents. By parsing the LaTeX commands and environments, you can create chunks that respect the logical organization of the content (e.g., sections, subsections, and equations), leading to more accurate and contextually relevant results. For example:

```
from langchain.text_splitter import LatexTextSplitter
latex_text = "..."
latex_splitter = LatexTextSplitter(chunk_size=100, chunk_overlap=0)
docs = latex_splitter.create_documents([latex_text])
```

### 4. Semantic chunking

A new experimental technique for approaching chunking was first introduced by Greg Kamradt. In his notebook, Kamradt rightfully points to the fact that a global chunking size may be too trivial of a mechanism to take into account the meaning of segments within the document. If we use this type of mechanism, we can’t know if we’re combining segments that have anything to do with one another.

Luckily, if you’re building an application with LLMs, you most likely already have the ability to create embeddings - and embeddings can be used to extract the semantic meaning present in your data. This semantic analysis can be used to create chunks that are made up sentences that talk about the same theme or topic.

Here are the steps that make semantic chunking work:

1. Break up the document into sentences.
2. Create sentence groups: for each sentence, create a group containing some sentences before and after the given sentence. The group is essentially “anchored” by the sentence use to create it. You can decide the specific numbers before or after to include in each group - but all sentences in a group will be associated with one “anchor” sentence.
3. Generate embeddings for each sentence group and associate them with their “anchor” sentence.
4. Compare distances between each group sequentially: When you look at the sentences in the document sequentially, as long as the topic or theme is the same - the distance between the sentence group embedding for a given sentence and the sentence group preceding it will be low. On the other hand, higher semantic distance indicates that the theme or topic has changed. This can effectively delineate one chunk from the next.

# Figuring out the best chunk size for your application

1. **Preprocessing your Data** - You need to first pre-process your data to ensure quality before determining the best chunk size for your application. For example, if your data has been retrieved from the web, you might need to remove HTML tags or specific elements that just add noise.

2. **Selecting a Range of Chunk Sizes** - Once your data is preprocessed, the next step is to choose a range of potential chunk sizes to test. As mentioned previously, the choice should take into account the nature of the content (e.g., short messages or lengthy documents), the embedding model you’ll use, and its capabilities (e.g., token limits). The objective is to find a balance between preserving context and maintaining accuracy. Start by exploring a variety of chunk sizes, including smaller chunks (e.g., 128 or 256 tokens) for capturing more granular semantic information and larger chunks (e.g., 512 or 1024 tokens) for retaining more context.

3. **Evaluating the Performance of Each Chunk Size** - In order to test various chunk sizes, you can either use multiple indices or a single index with multiple namespaces. With a representative dataset, create the embeddings for the chunk sizes you want to test and save them in your index (or indices). You can then run a series of queries for which you can evaluate quality, and compare the performance of the various chunk sizes. This is most likely to be an iterative process, where you test different chunk sizes against different queries until you can determine the best-performing chunk size for your content and expected queries.

