# fanfic_thesis

This repo contains the code used for the Master's Thesis for Mia Jacobsen, MSc. Cognitive Science, Aarhus University:
- More than just Porn: A Multidimensional Analysis of Fanfiction

This includes the code for scraping the fanfiction texts, creating the snippets which are run through Nini's (2019) MAT, and the code for the statistical analysis.

## Repo structure
The repo is structured as follows:

```
├── src                                     <- The main folder for code 
|   ├── analysis                             <- the folder for scripts preparing the texts for analysis
|   |  ├── prep_data.py                      <- the scipt for creating fanfiction snippets
|   |  ├── prep_source.py                    <- the scipt for creating source text snippets
|   |  └── utils.py                          <- a scipt containing helper functions
|   ├── scraping                            <- the folder for scripts pertaining to scraping the fanfiction texts
|   |  ├── links_scraper.py                  <- the scipt for retrieving links to fanfiction based on a search URL
|   |  ├── text_scraper.py                   <- the scipt for retrieving the text for the linked works 
|   |  └── utils.py                          <- a scipt containing helper functions
|   └── statistics                          <- the folder for scripts and figures that pertain to the statistical analysis
|   |  ├── RQ1.Rmd                           <- the R Markdown containing the code for the first research question analysis
|   |  ├── RQ2.Rmd                           <- the R Markdown containing the code for the second research question analysis
|   |  ├── rq1_plot.png                      <- the first figure for RQ1
|   |  ├── rq1_plot_2.png                    <- the second figure for RQ1 
|   |  └── rq2_plot.png                      <- the figure for RQ2
├── README.md                               <- The top-level README for this project
└── requirements.txt                        <- The Python packages necessary for running the Python code in the repo
```
