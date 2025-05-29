# CN-US-EU-JP-Patent_2020-2025
> **Abstract**: This dataset contains patent documents from ***China, the United States, Europe, and Japan*** spanning from January 1, 2020, to March 5, 2025. Data source: Google Patents. Data format: TXT. Data volume: approximately 7 million records. The dataset has undergone preprocessing to remove some low-quality or corrupted patents.

## Dataset address
[[`OpenXLab`](https://openxlab.org.cn/datasets/lweiranl/CUEJ2025/tree/main)]  

## Downloading
### OpenXLab
Download repo:
```sh
openxlab dataset get -r lweiranl/CUEJ2025 -t /path/to/local/folder
```
Download file：
```sh
openxlab dataset download -r lweiranl/CUEJ2025 -s ./patent_use/cn_use_1.zip -t /path/to/local/folder
```

# Dataset introduction
Due to the large number of patents in the dataset, the original HTML files contained a significant amount of redundant fields, which occupied substantial storage space. Therefore, we extracted the key fields of the patents, converted them into TXT files stored in a dictionary format, and finally compressed them into a ZIP file. This step reduced the dataset size to 5% of its original size.

## Dataset size
|    File type    |    Size    |   
| :-----------: | :-------------: |
|  HTML  |       &nbsp; 2391 GB &nbsp;       | 
|  HTML(zip)  |       &nbsp; 306 GB &nbsp;       | 
|  TXT  |       &nbsp; 834 GB &nbsp;       |
|  TXT(cleaning)  |       &nbsp; **567 GB** &nbsp;       |
|  TXT(cleaning,zip)  |       &nbsp; **118 GB** &nbsp;       |

## Folder hierarchy
<!--origin
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
-->
```
patent_use
├── cn_use_1.zip
│   └── [CN119xxxxxxx.txt]
├── ...
├── cn_use_4.zip
│   └── [CN111xxxxxxx.txt]
├── us_use_1.zip
│   └── [US202500xxxxx.txt]
├── ...
├── us_use_5.zip
│   └── [US202000xxxxx.txt]
├── eu_use_1.zip
│   └── [EP44xxxxx.txt]
├── eu_use_2.zip
│   └── [EP38xxxxx.txt]
├── jp_use_1.zip
│   └── [JP20250xxxxx.txt]
├── jp_use_2.zip
│   └── [JP20200xxxxx.txt]
```

## File structure
Each patent corresponds to a text file with the same name.  
The file content is a single-line dictionary, where the key is the field name and the value is the field content.  
```python
{
  'Field 1': 'Content 1', 
  'Field 2': ['Content 2-1', 'Content 2-2'], 
  'Field 3': [{'Field 3-1-1': 'Content 3-1-1', 'Field 3-1-2': 'Content 3-1-2'}, {'Field 3-2', 'Content 3-2'}]
}
*The txt file contains a dictionary that occupies only a single line.
```

## Schema
|    Num    | Schema |  Example   |
| :-----------: | :-----------------: | :-------------: |
| 1  |  publication_number            | US20240023456A1 |
| 2  |  title                         | Semiconductor device and method... |
| 3  |  authority                     | ['US', 'United States'] |
| 4  |  prior_art_keywords            | ['layer', 'mtj', 'sot'...] |
| 5  |  legal_status                  | Pending |
| 6  |  application_number            | US17/887,530 |
| 7  |  inventors                     | ['Hui-Lin WANG'] |
| 8  |  current_assignee              | United Microelectronics Corp |
| 9  |  original_assignee             | United Microelectronics Corp |
| 10 |  abstract                      | A method for fabricating... |
| 11 |  priority_date                 | 2022-07-13 |
| 12 |  filing_date                   | 2022-08-15 |
| 13 |  publication_date              | 2024-01-18 |
| 14 |  classifications               | [{'code': 'H10N50/01', 'description': 'Manufacture or treatment'}...] |
| 15 |  definitions                   | [{'subject': 'the invention', 'definition': 'relates to a semiconductor...', 'num_attr': '0001'}...] |
| 16 |  landscapes                    | [{'name': 'Engineering & Computer Science', 'type': 'AREA'}...] |
| 17 |  description                   | BACKGROUND OF THE INVENTION\n1. Field of the Invention... |
| 18 |  claims                        | What is claimed is:\n \n 1. A method for fabricating semiconductor device... |
| 19 |  n_claims                      | 19 |
| 20 |  family_id                     | ID=89509667 |
| 21 |  citations                     | ['US20170117323A1\n(en)\n*\n2015-10-22...', ...] |
| 22 |  n_citations                   | 4 |
| 23 |  cited_by                      | None |
| 24 |  n_citedby                     | 0 |
| 25 |  families_citing_this_family   | None |
| 26 |  n_fctf                        | 0 |
| 27 |  family_cites_families         | None |
| 28 |  n_fcf                         | 0 | 

*For strings, default=None; for numbers, default=0. 

## Dataset cleaning
| Conditional fields | Introduction |
| :----------------: | :----------: |
| n_claims | number of claims |  
| n_citations | number of citations |
| n_citedby | number of citations |
| n_fctf | number of families_citing_this_family |
| n_fcf | number of family_cites_families |

**Recommendations:**  
| Aspect | Task Indicators | Quality Indicators |
| :---- | :------------- | :---------------- |
| Reason | Key Field Missing | Low Requirement Count or Citation Count |
| For recent two years | `publication_number` is None *or* <br> `classification` is None | `n_claims` <= 0 *or* <br> max(`n_citations`, `n_citedby`, `n_fctf`, `n_fcf`) <= 0 |
| For other years | `publication_number` is None *or* <br> `classification` is None | `n_claims` <= 5 *or* <br> max(`n_citations`, `n_citedby`, `n_fctf`, `n_fcf`) <= 2 |  

*We applied the same cleaning conditions to this dataset.

**Code**  
`get_more_info.py`
```
html -> txt
base on python Beautifulsoup
```
`store_use.py`
```
data cleaning
```
`CN_EU_multi_threaded_crawler.py`
```
A crawler for downloading patents from China and the European Union (with sequential serial numbers)
has been implemented using multithreading for acceleration.
```
`US_JP_multi_threaded_crawler.py`
```
A crawler for downloading patents from the United States and Japan (serial numbers categorized by year)
has been implemented using multithreading for acceleration.
```

## Copyright Notice

**`Patent Dataset`**  
This dataset contains patents data crawled from Google Patents.  

**`Data Source`**  
The data is sourced from Google Patents Public Datasets. For more information, see [Google Patents Public Datasets](https://github.com/google/patents-public-data).


## Terms of Use

**`License`**  
This dataset is licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to use, modify, and distribute this dataset, provided that you give appropriate credit to the original source.

**`Usage`**  
Please ensure that any use of this dataset complies with the terms of the CC BY 4.0 license. If you make any modifications or create derivative works, please clearly indicate the changes and provide attribution to the original dataset.

**`Important Notes`**  
- The data is provided "as is" without any warranty or guarantee of accuracy.
- Any use of this dataset must comply with the terms and conditions of Google Patents Public Datasets.


## Citation
```
Quan Liu, Hongfei Bao, Jiameng Zhang. University of Science and Technology China, Qmai Inc. (2025). CN-US-EU-JP-Patent_2020-2025 (Version 1.0) [Data set]. GitHub. https://github.com/liuquan-ustc-qmai/CN-US-EU-JP-Patent_2020-2025
```
