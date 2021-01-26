# Easy Graph Visualization of SRCML

```bash
$ srcml example/code.java > example/code.srcml
$ srcml2dot example/code.srcml example/code.dot
$ dot -Tpng example/code.dot > example/code_topdown.png
$ neato -Tpng example/code.dot > example/code_spider.png 
```

