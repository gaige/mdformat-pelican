a test
.
Title: a title

This is the input Markdown test,
then below add the expected output.
.
Title: a title

This is the input Markdown test,
then below add the expected output.
.

another test
.
Title: With Markdown

Some *markdown*

* a
* b
- c
.
Title: With Markdown

Some *markdown*

- a
- b

* c
.


Test links
.
Title: Link test
Date: 2021-03-28 05:37

[google](https://google.com)
[local]({filename}/a/file)
[tag]({tag}funny_tag)
.
Title: Link test
Date: 2021-03-28 05:37

[google](https://google.com)
[local]({filename}/a/file)
[tag]({tag}funny_tag)
.

Test Image references
.
Title: Link test 2
Date: 2021-03-28 05:37

![google](https://google.com)
![local]({filename}/a/file)
![tag]({tag}funny_tag)
.
Title: Link test 2
Date: 2021-03-28 05:37

![google](https://google.com)
![local]({filename}/a/file)
![tag]({tag}funny_tag)
.


Test fix old references
.
Title: Bar Test
Date: 2021-03-28 05:38

![google](https://google.com)
![local](|filename|/a/file)
![tag](|tag|funny_tag)
.
Title: Bar Test
Date: 2021-03-28 05:38

![google](https://google.com)
![local]({filename}/a/file)
![tag]({tag}funny_tag)
.
