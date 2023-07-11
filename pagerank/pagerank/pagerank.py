import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages_list = corpus.keys()
    if corpus[page]:
        output_dict = {page: (1-damping_factor)/len(pages_list) for page in pages_list}
        for link in corpus[page]:
            output_dict[link] += damping_factor/len(corpus[page])
    else:
        output_dict = {page: 1/len(pages_list) for page in pages_list}
    return output_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages_list = list(corpus.keys())
    output_dict = {page: 0.0 for page in pages_list}
    for i in range(n):
        if i == 0:
            last_page = random.choice(pages_list)
            output_dict[last_page] += 1
            continue
        transition_probabilites = transition_model(corpus, last_page, damping_factor)
        last_page = random.choices(
            population=list(transition_probabilites.keys()),
            weights=list(transition_probabilites.values()),
            k=1
        )[0]
        output_dict[last_page] += 1
    output_dict = {page: value / n for page, value in output_dict.items()}
    return output_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    corpus_iteration = corpus.copy()
    for page in corpus_iteration:
        if len(corpus_iteration[page]) == 0:
            corpus_iteration[page] = {page for page in corpus_iteration}
    pages = corpus_iteration.keys()
    number_of_pages = len(corpus_iteration.keys())
    output_dict = {page: 1/number_of_pages for page in pages}
    error = 1
    max_error = 0.001
    while error > max_error:
        error = 0
        loop_dict = output_dict.copy()
        for page in loop_dict:
            first_condition = (1 - damping_factor) / number_of_pages
            second_condition = 0.0
            for corpus_page in corpus_iteration.keys():
                if page in corpus_iteration[corpus_page]:
                    second_condition += loop_dict[corpus_page] / len(corpus_iteration[corpus_page])
            second_condition *= damping_factor
            current_pagerank = first_condition + second_condition
            if abs(current_pagerank - loop_dict[page]) > error:
                error = abs(current_pagerank - loop_dict[page])
            output_dict[page] = current_pagerank
    while sum(output_dict.values()) != 1:
        sum_values = sum(output_dict.values())
        for page in output_dict:
            output_dict[page] /= sum_values
    return output_dict


if __name__ == "__main__":
    main()
