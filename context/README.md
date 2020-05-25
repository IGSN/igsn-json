# Some notes on context development

## Thoughts
In order to build out the graph we need to be able to at the minimum have an ID for the 
data graph for a sample.  In this example I used

```
  "@id": "http://example.org/id/igsn/ID",
  "@type": "https://igsn.org/voc/v1/Sample",
```

We could also set a in context like:
```
  {
  "@context": {
    "@base": "http://example.org/",
    "igsnvoc": "https://igsn.org/voc/v1/",
    "schema": "https://schema.org/",
```

which would allow a simpler

 ``` 
 "@id": "namespace/ID",
 ```
 in the body now.  

 ## Questions

* can we set a default type in the context?   I have not found this if we can