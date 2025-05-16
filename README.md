# CN-US-EU-JP-Patent_2020-2025
> **Abstract**: This dataset contains patent documents from **China, the United States, Europe, and Japan** spanning from January 1, 2020, to March 5, 2025. Data source: Google Patents. Data format: HTML. Data volume: approximately 11 million records. The dataset has undergone preprocessing to remove some low-quality or corrupted patents.

## Dataset address
[[`Kaggle`](https://www.kaggle.com/api/v1/datasets/download/weiran11/patent-test)]

# Downloading
## Path
Donwload repo:
```sh
kaggle datasets download weiran11/patent-test
```
or
```sh
curl -L -o ~/Downloads/patent-test.zip\
  https://www.kaggle.com/api/v1/datasets/download/weiran11/patent-test
```

# Dataset introduction

## Dataset size
|    File type    | Size |   
| :-----------: | :-----------------: |
|  zip  |      --G       | 
| txt |      --G       | 

## Folder hierarchy
```
.
├── README.md
├── cn
│   └── 0_txt.zip
│       └── [CN119xxxxxxx.html]
│   ...
│   └── 15_txt.zip
│       └── [CN111xxxxxxx.html]
├── us
│   └── 2020-0_txt.zip
│       └── [US202000xxxxx.html]
│   ...
│   └── 2025-0_txt.zip
│       └── [US202500xxxxx.html]
├── eu
│   └── 0_txt.zip
│       └── [EP44xxxxx.html]
│   ...
│   └── 6_txt.zip
│       └── [EP38xxxxx.html]
├── jp
│   └── 2020-0_txt.zip
│       └── [JP20200xxxxx.html]
│   ...
│   └── 2025-0_txt.zip
│       └── [JP20250xxxxx.html]
```
## File structure
Each patent corresponds to a text file with the same name.  
The file content is a single-line dictionary, where the key is the field name and the value is the field content.  
{'Field 1': 'Content 1', 'Field 2': ['Content 2-1', 'Content 2-2'], 'Field 3': [{'Field 3-1-1': 'Content 3-1-1', 'Field 3-1-2': 'Content 3-1-2'}, {'Field 3-2', 'Content 3-2'}]}

## Schema
|    Num    | Key |  Schema   |  Notes  |
| :-----------: | :-----------------: | :-------------: | :-------------: |
| 1  |  publication_number            |  |  |
| 2  |  title                         |  |  |
| 3  |  authority                     |  |  |
| 4  |  prior_art_keywords            |  |  |
| 5  |  legal_status                  |  |  |
| 6  |  application_number            |  |  |
| 7  |  inventors                     |  |  |
| 8  |  current_assignee              |  |  |
| 9  |  original_assignee             |  |  |
| 10 |  abstract                      |  |  |
| 11 |  priority_date                 |  |  |
| 12 |  filing_date                   |  |  |
| 13 |  publication_date              |  |  |
| 14 |  classifications               |  |  |
| 15 |  definitions                   |  |  |
| 16 |  landscapes                    |  |  |
| 17 |  description                   |  |  |
| 18 |  claims                        |  |  |
| 19 |  n_claims                      |  |  |
| 20 |  family_id                     |  |  |
| 21 |  citations                     |  |  |
| 22 |  n_citations                   |  |  |
| 23 |  cited_by                      |  |  |
| 24 |  n_citedby                     |  |  |
| 25 |  families_citing_this_family   |  |  |
| 26 |  n_fctf                        |  |  |
| 27 |  family_cites_families         |  |  |
| 28 |  n_fcf                         |  |  |

# Dataset cleaning
n_claims (number of claims)  
n_citations / n_citedby (number of citations)  
n_fctf (number of families_citing_this_family)  
n_fcf (number of family_cites_families)  
Recommended: n_claims <= 5 and max(n_citations / n_citedby, n_fctf, n_fcf) <= 3

# Copyright Notice

**Patent Dataset**

This dataset contains patents data crawled from Google Patents.

**Data Source**
The data is sourced from Google Patents Public Datasets. For more information, see [Google Patents Public Datasets](https://github.com/google/patents-public-data)[^5^].


# Terms of Use

**License**
This dataset is licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to use, modify, and distribute this dataset, provided that you give appropriate credit to the original source.

**Usage**
Please ensure that any use of this dataset complies with the terms of the CC BY 4.0 license. If you make any modifications or create derivative works, please clearly indicate the changes and provide attribution to the original dataset.

**Important Notes**
- The data is provided "as is" without any warranty or guarantee of accuracy.
- Any use of this dataset must comply with the terms and conditions of Google Patents Public Datasets.


# Citation
```
Qmai. (2025). CN-US-EU-JP-Patent_2020-2025 (Version 1.0) [Data set]. GitHub. https://github.com/liuquan-ustc-qmai/CN-US-EU-JP-Patent_2020-2025
```
