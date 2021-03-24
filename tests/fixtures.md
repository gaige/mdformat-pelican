a test
.
This is the input Markdown test,
then below add the expected output.
.
This is the input Markdown test,
then below add the expected output.
.

another test
.
Some *markdown*

* a
* b
- c
.
Some *markdown*

- a
- b

* c
.


Test links
.
[google](https://google.com)
[local]({filename}/a/file)
[tag]({tag}funny_tag)
.
[google](https://google.com)
[local]({filename}/a/file)
[tag]({tag}funny_tag)
.

Test Image references
.
![google](https://google.com)
![local]({filename}/a/file)
![tag]({tag}funny_tag)
.
![google](https://google.com)
![local]({filename}/a/file)
![tag]({tag}funny_tag)
.


Test fix old references
.
![google](https://google.com)
![local](|filename|/a/file)
![tag](|tag|funny_tag)
.
![google](https://google.com)
![local]({filename}/a/file)
![tag]({tag}funny_tag)
.
