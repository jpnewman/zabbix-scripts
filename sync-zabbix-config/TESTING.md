
# Testing

## Lint python script

~~~
flake8 **/*.py
~~~

## Code Metrics

~~~
radon cc . -a -nc
~~~

## UnitTest

~~~
py.test --html=report.html
~~~

## Line Count

~~~
find . -name '*.py' | xargs wc -l
~~~
